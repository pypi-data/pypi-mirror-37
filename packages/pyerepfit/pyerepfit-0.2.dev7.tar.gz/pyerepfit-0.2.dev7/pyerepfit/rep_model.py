#!/usr/bin/env python3
import pymatgen as mg
import pymatgen.core.units
import math
import numpy as np
import io
import textwrap
from collections import namedtuple

from typing import Dict, List, Any

from sklearn import linear_model

from . import utils

from . import rep_spline
from . import rep_basis

class RepulsiveModelCollection:
    """ General class for the collection of the repulsive potential model

    """

    def __init__(self, rep_names, rep_models):
        self.rep_names = []
        self.rep_models = []
        self.resulting_repulsives = []
        self.all_names = {}
        self.shifts = {}
        self.max_cutoff = 0.0

        s_rep_names = []
        s_rep_model = []
        for name, model in zip(rep_names, rep_models):
            elems = name.split('-')
            sorted_name = '{}-{}'.format(*sorted(elems))
            s_rep_names.append(sorted_name)
            s_rep_model.append(model)

        shift = 0
        for name, model in sorted(zip(s_rep_names, s_rep_model), key=lambda x: x[0]):
            if (name not in self.all_names):
                self.all_names[name] = model
                elems = name.split('-')
                reversed_name = '{}-{}'.format(*reversed(elems))
                self.all_names[reversed_name] = model
                self.rep_names.append(name)
                self.rep_models.append(model)
                self.shifts[name] = shift
                self.shifts[reversed_name] = shift
                self.max_cutoff = max(self.max_cutoff, model.cutoff)
                shift += model.num_variables
        
        self.total_num_variables = sum([x.num_variables for x  in self.rep_models])

    def description(self):
        fout = io.StringIO()
        print('Potential type: {}'.format(self.rep_models[0].description()), file=fout)
        print('Number of repulsive potentials: {}'.format(len(self.rep_models)), file=fout)
        print('Number of variables: {}'.format(self.get_total_num_variables()), file=fout)
        
        print('Repulsive potenial description:', file=fout)
        for rep_name, rep_model in zip(self.rep_names, self.rep_models):
            print('  {}'.format(rep_name), file=fout)
            print(textwrap.indent(str(rep_model), "    "), file=fout)

        print("", file=fout)
        return fout.getvalue()

    def get_shift(self, name):       
        return self.shifts.get(name, -1)

    def get_num_variables(self, name):
        return self.all_names[name].num_variables        
    
    def get_total_num_variables(self):
        return self.total_num_variables

    def get_row(self, name, r, derv=0):
        return self.all_names[name].get_row(r, derv)
    

class EquationDescription:
    def __init__(self, equ_type: str, equation_item, equ_block, ref_block) -> None:
        self.equ_type = equ_type
        self.equation_item = equation_item
        self.equ_block = equ_block
        self.ref_block = ref_block

class EnergyEquationDescription(EquationDescription):
    def __init__(self, equation_item, equ_block, ref_block, missing_atom_counts):
        super().__init__("energy", equation_item, equ_block, ref_block)
        self.missing_atom_counts = missing_atom_counts
        

class RepulsivePotentialEquationBuilder():
    def __init__(self, evaluated_erepfit_input):

        self.evaluated_erepfit_input = evaluated_erepfit_input

        #building a haspmap for easy reference.
        self.uuidmap = {}
        for system in self.evaluated_erepfit_input.systems:
            self.uuidmap[system.uuid] = system

        #equations for each of systems        
        self.equation_descriptions = []

        #load external repulsive potentials
        self.external_repulsive_potentials = { k: rep_spline.RepulsivePotenial.from_file(v) for k, v in self.evaluated_erepfit_input.external_repulsive_potentials.items()}
    
    def calc_dist_matrix(self, mole, cutoff):
        """ Get the distance and displacement matrix in bohr for all pairs
        """ 
        res = {}
        cutoff_ang = cutoff/mg.core.units.ang_to_bohr
        if (isinstance(mole, mg.Structure)):
            for ind, site in enumerate(mole.sites):
                neighbors = mole.get_neighbors(site, cutoff_ang, include_index=True)
                for n_site, n_r, n_index in neighbors:
                    r_in_bohr = n_r*mg.core.units.ang_to_bohr
                    vec = ((site.coords - n_site.coords)/n_r)
                    if ( (ind, n_index) in res):
                        res[(ind, n_index)].append( (r_in_bohr, vec) )
                    else:
                        res[(ind, n_index)] = [ (r_in_bohr, vec) ]
        else:
            for ind, site in enumerate(mole.sites):
                for ind2, site2 in enumerate(mole.sites):
                    if (ind == ind2):
                        continue
                    vec = site.coords - site2.coords
                    n_r = math.sqrt(sum(vec*vec))
                    r_in_bohr = n_r*mg.core.units.ang_to_bohr
                    p_vec = vec/n_r
                    if (r_in_bohr > cutoff):
                        continue
                    if ( (ind, ind2) in res):
                        res[(ind, ind2)].append( (r_in_bohr, p_vec) )
                    else:
                        res[(ind, ind2)] = [ (r_in_bohr, p_vec) ]
        return res

    def get_dist_matrix(self, system, max_cutoff):
        if system.uuid in self.dist_matrix_uuids:
            dist_matrix = self.dist_matrix_uuids[system.uuid]
            return dist_matrix
        else:
            dist_matrix = self.calc_dist_matrix(system.geometry.get_coordinate_struct(), max_cutoff)
            self.dist_matrix_uuids[system.uuid] = dist_matrix
            return dist_matrix

    def make_energy_block(self, system, dist_matrix, modelcollection, external_reps):
        num_rows = 1
        equ_block = np.zeros( (num_rows, modelcollection.get_total_num_variables()) )
        ref_block = np.zeros( num_rows )
        
        for k, dis in dist_matrix.items():
            ind1, ind2 = k
            rep_name = '{}-{}'.format(system.geometry.coordinates[ind1][0], system.geometry.coordinates[ind2][0])
            shift = modelcollection.get_shift(rep_name)
            if (shift > -1):
                for r, _ in dis:
                    row = modelcollection.get_row(rep_name, r, 0)*0.5
                    lens = len(row)
                    equ_block[0, shift:shift+lens] += row
            elif (rep_name in external_reps):
                for r, _ in dis:
                    ene = external_reps[rep_name].eval(r)
                # print('Add external: {} {} {}'.format(rep_name, r_in_bohr, ene))
                    ref_block -= ene
            else:
                raise RuntimeError('Rep not found: {}'.format(rep_name))
        return equ_block, ref_block
    
    def make_force_block(self, system, dist_matrix, modelcollection, external_reps, construct_indexes):
        
        num_rows = 3*len(construct_indexes)
        if num_rows == 0:
            return [], []

        equ_block = np.zeros( (num_rows, modelcollection.get_total_num_variables()))
        ref_block = np.zeros( num_rows )
        
        construct_indexes_index = list(construct_indexes)
        for k, dis in dist_matrix.items():
            ind1, ind2 = k
            if (ind1 not in construct_indexes):
                continue
            ind = construct_indexes_index.index(ind1)
            rep_name = '{}-{}'.format(system.geometry.coordinates[ind1][0], system.geometry.coordinates[ind2][0])
            shift = modelcollection.get_shift(rep_name)
            if (shift > -1):
                for r, vec in dis:
                    row = modelcollection.get_row(rep_name, r, 1)
                    lens = len(row)
                    for xyz in range(3):
                        equ_block[ ind*3+xyz , shift:shift+lens ] += (-row*vec[xyz])
                    
            elif (rep_name in external_reps):
                for r, vec in dis:
                    values = external_reps[rep_name].eval(r, 1)
                    for xyz in range(3):
                        ref_block[ind*3+xyz] -= -values*ref_block[xyz]
            else:
                raise RuntimeError('Rep not found: {}'.format(rep_name))
            
        return equ_block, ref_block


    def build_linear_equations(self, modelcollection: RepulsiveModelCollection):
        
        self.modelcollection = modelcollection
        self.fitted_atom_energy: Dict[str, float] = {}

        # get the maximal cutoff of all repulsive potentials
        max_cutoff:float = max([x.cutoff for x in self.modelcollection.rep_models])
        if (len(self.external_repulsive_potentials) > 0):
            max_cutoff = max(max_cutoff, max([v.cutoff for k, v in self.external_repulsive_potentials.items()]))

        self.dist_matrix_uuids :Dict[str, Dict[tuple, list]] = {}
        
        #atomization energy equations
        self._build_energy_equations(max_cutoff)

        #force equations
        self._build_force_equations(max_cutoff)
    
        #additional equations
        self._build_additional_equations()
        
        #reaction equations
        self._build_reaction_equations(max_cutoff)

    def _build_reaction_equations(self, max_cutoff: float) -> None:
        for reaction_item in self.evaluated_erepfit_input.equations['reaction']:
            react_energy = utils.get_energy_in_au(reaction_item.energy, reaction_item.unit)

            if (reaction_item.weight < 1.0e-4):
                continue

            final_equ_block = np.zeros( (1, self.modelcollection.get_total_num_variables()) )
            final_ref_block = np.zeros( 1 )

            elec_reaction_energy = 0.0
            for item in reaction_item.products:
                system = self.uuidmap[item.uuid]
                dist_matrix = self.get_dist_matrix(system, max_cutoff)
                
                equ_block, ref_block = self.make_energy_block(system, dist_matrix, self.modelcollection, self.external_repulsive_potentials)
                final_equ_block += equ_block*item.coefficient
                final_ref_block += ref_block*item.coefficient
                elec_reaction_energy += system.elec_data['elec_energy']*item.coefficient

            for item in reaction_item.reactants:
                system = self.uuidmap[item.uuid]
                dist_matrix = self.get_dist_matrix(system, max_cutoff)

                equ_block, ref_block = self.make_energy_block(system, dist_matrix, self.modelcollection, self.external_repulsive_potentials)
                final_equ_block -= equ_block*item.coefficient
                final_ref_block -= ref_block*item.coefficient
                elec_reaction_energy -= system.elec_data['elec_energy']*item.coefficient


            final_ref_block += react_energy - elec_reaction_energy

            desc = EquationDescription('reaction', reaction_item, final_equ_block*reaction_item.weight, final_ref_block*reaction_item.weight)
            self.equation_descriptions.append(desc)

    def _build_additional_equations(self) -> None:
        for rep_name, items in sorted(self.evaluated_erepfit_input.equations['additional'].items(), key=lambda x:x[0]):
            shift = self.modelcollection.get_shift(rep_name)
            if (shift > -1):
                equ_block = np.zeros( (len(items), self.modelcollection.get_total_num_variables()) )
                ref_block = np.zeros( len(items) )
                for ind, item in enumerate(items):
                    r = utils.get_length_in_au(item.distance, item.unit)
                    row = self.modelcollection.get_row(rep_name, r, item.derivative)
                    lens = len(row)
                    equ_block[ind, shift:shift+lens] += row*item.weight
                    ref_block[ind] = item.value*item.weight

                desc = EquationDescription('additional', item, equ_block, ref_block)
                desc.rep_name = rep_name
                self.equation_descriptions.append(desc)
            else:
                continue

    def _build_force_equations(self, max_cutoff: float) -> None:
        for item in self.evaluated_erepfit_input.equations['force']:
            if (item.weight < 1.0e-4):
                continue
            # Get the bond distances.
            system = self.uuidmap[item.uuid]
            dist_matrix = self.get_dist_matrix(system, max_cutoff)

            fitting_indexes = list(range(len(system.geometry.coordinates)))
            if hasattr(item, 'reference_force'):
                if hasattr(item, 'fitting_indexes'):
                    fitting_indexes = item.fitting_indexes
                else:
                    item['fitting_indexes'] = fitting_indexes

            equ_block, ref_block = self.make_force_block(system, dist_matrix, self.modelcollection, self.external_repulsive_potentials, fitting_indexes)


            if (len(ref_block) == 0):
                continue

            total_forces = np.zeros( ref_block.shape )
            if hasattr(item, 'reference_force'):
                total_forces = np.array([item.reference_force[i] for i in fitting_indexes]).flatten()

            ref_e_forces = np.array([ system.elec_data['elec_forces'][i] for i in fitting_indexes ]).flatten()
            # print(ref_block.shape, ref_e_forces.shape, total_forces.shape)
            ref_block =  (total_forces -  ref_e_forces) - ref_block

            desc = EquationDescription('forces', item, equ_block*item.weight, ref_block*item.weight)
            self.equation_descriptions.append(desc)

    def _build_energy_equations(self, max_cutoff: float) -> None:
        for item in self.evaluated_erepfit_input.equations['energy']:
            if (item.weight < 1.0e-4):
                continue
            # Get the bond distances.
            system = self.uuidmap[item.uuid]
            dist_matrix = self.get_dist_matrix(system, max_cutoff)

            missing_atom_counts = {}
            e_atom = 0.0
            for line in system.geometry.coordinates:
                symbol = line[0]
                if symbol not in self.evaluated_erepfit_input.atomic_energy:
                    value = missing_atom_counts.get(symbol, 0)
                    missing_atom_counts[symbol] = value+1
                else:
                    e_atom += self.evaluated_erepfit_input.atomic_energy[symbol]

            e_ea_dft = utils.get_energy_in_au(item.energy, item.unit)
            e_rep_dftb = e_atom - system.elec_data['elec_energy'] - e_ea_dft

            equ_block, ref_block = self.make_energy_block(system, dist_matrix, self.modelcollection, self.external_repulsive_potentials)
            ref_block = -ref_block + e_rep_dftb

            desc = EnergyEquationDescription(item, equ_block*item.weight, ref_block*item.weight, missing_atom_counts)
            self.equation_descriptions.append(desc)


    

    def _extend_atomic_energy_equations(self, all_missing_atoms, matrix) -> None:
        if (len(all_missing_atoms) == 0):
            return matrix
        atom_columns = len(all_missing_atoms)
        new_matrix = np.zeros( (matrix.shape[0], matrix.shape[1]+atom_columns) ) 
        new_matrix[:, :matrix.shape[1]] = matrix

        ind = 0
        for desc in self.equation_descriptions:
            if isinstance(desc, EnergyEquationDescription):
                for i in range(atom_columns):
                    new_matrix[ind, matrix.shape[1]+i] = -(desc.missing_atom_counts.get(all_missing_atoms[i], 0))*desc.equation_item.weight            
            ind += desc.equ_block.shape[0]
        return new_matrix
        

    
    def get_residuals(self) -> List[Any]:
        fout = io.StringIO()
        return sum([sum(res.residual*res.residual) for res in self.print_residuals(fout)])

    def print_residuals(self, output_stream) -> List[Any]:
        Residual = namedtuple('Residual', ['description', 'residual'])
        residuals = []
        print("", file=output_stream)

        if (len(self.fitted_atom_energy) > 0):
            print('Fitted Atom Energies:', file=output_stream)
            for k, v in sorted(self.fitted_atom_energy.items()):
                print(' {:<3s}: {:20.12f} Hartree'.format(k,v), file=output_stream)
        print("", file=output_stream)

        print("Energy Equation Residuals", file=output_stream)
        vunknowns = np.array(self.vunknowns)
        for desc in [x for x in self.equation_descriptions if x.equ_type == 'energy']:
            item = desc.equation_item
            atom_energy = sum([self.fitted_atom_energy[k]*v for k, v in desc.missing_atom_counts.items()]) * item.weight
            res = (np.dot(desc.equ_block, vunknowns) - atom_energy - desc.ref_block) / item.weight
            residuals.append(Residual(desc, res))
            print('{:10.4f} {:9s} {}'.format(utils.get_energy_from_au(res[0], item.unit), item.unit, item.name), file=output_stream)
        
        print("", file=output_stream)
        print("Force Equation Residuals (Ha/bohr)", file=output_stream)
        for desc in [x for x in self.equation_descriptions if x.equ_type == 'forces']:
            item = desc.equation_item
            res = ((np.dot(desc.equ_block, vunknowns) - desc.ref_block) / item.weight)
            print(item.name, item.weight, file=output_stream)
            system = self.uuidmap[item.uuid]
            residuals.append(Residual(desc, res))
            if hasattr(item, 'fitting_indexes'):
                for i in range(0, int(len(res)/3)):
                    print(' {:3s} {:20.12f} {:20.12f} {:20.12f}'.format(system.geometry.coordinates[item.fitting_indexes[i]][0], 
                        res[i*3], res[i*3+1], res[i*3+2]), file=output_stream)
            else:
                for i in range(0, int(len(res)/3)):
                    print(' {:3s} {:20.12f} {:20.12f} {:20.12f}'.format(system.geometry.coordinates[i][0], 
                        res[i*3], res[i*3+1], res[i*3+2]), file=output_stream)
            print("", file=output_stream)

        print("", file=output_stream)
        print("Addition Equation Residuals (Ha)", file=output_stream)
        for desc in [x for x in self.equation_descriptions if x.equ_type == 'additional']:
            item = desc.equation_item
            rep_name = desc.rep_name
            res = np.dot(desc.equ_block, vunknowns) - desc.ref_block           
            residuals.append(Residual(desc, res))
            for i in range(len(res)):
                print('  {:<6s} {:20.12f}'.format(rep_name, res[i]), file=output_stream)

        print("", file=output_stream)
        print("Reaction Equation Residuals (Ha)", file=output_stream)
        for desc in [x for x in self.equation_descriptions if x.equ_type == 'reaction']:
            item = desc.equation_item
            res = (np.dot(desc.equ_block, vunknowns) - desc.ref_block ) / item.weight
            residuals.append(Residual(desc, res))
            for i in range(len(res)):
                print('{:10.4f} {:9s} {}'.format(utils.get_energy_from_au(res[i], item.unit), item.unit, item.name), file=output_stream)
        print("", file=output_stream)
        return residuals



    def solve(self, modelcollection, solver):
        self.vunknowns = solver.solve(modelcollection, self)
        