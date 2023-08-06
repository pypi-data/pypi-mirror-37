#!/usr/bin/env python3

import pymatgen as mg
import os
import uuid

import io

class SKFileInfo:
    def __init__(self, data):
        self.type2filenames = data.get('type2filenames', False)
        if (self.type2filenames):
            self.suffix = data.get('suffix', ".skf")
            self.prefix = data.get('prefix', "./")
            self.lowercase = data.get('lowercase', False)
            self.separator = data.get('separator', '-')
            self.max_angular_momentum = data.get('max_angular_momentum', dict())
        else:
            self.skfiles = data.get('skfiles', dict())

    
    def bool2YesNo(self, val):
        if (val):
            return "Yes"
        else:
            return "No"
  
    def to_hsd(self, fout):
        print('\n+Hamiltonian = +DFTB{', file=fout)        
        if (self.type2filenames):
            print('    !SlaterKosterFiles = !Type2Filenames{', file=fout)
            print('      !Prefix = "{}"'.format(self.prefix), file=fout)
            print('      !Suffix = "{}"'.format(self.suffix), file=fout)
            print('      !Separator = "{}"'.format(self.separator), file=fout)
            print('      !LowerCaseTypeName = {}'.format(self.bool2YesNo(self.lowercase)), file=fout)
            print('    }', file=fout)

            print('    !MaxAngularMomentum = {', file=fout)
            for k, v in self.max_angular_momentum.items():
                print('      {} = "{}"'.format(k, v), file=fout)
            print('    }', file=fout)

        else:
            print('    !SlaterKosterFiles = {', file=fout)
            for k, v in self.skfiles.items():
                print('      {} = {}'.format(k, v), file=fout)
            print('    }', file=fout)

            print('    !MaxAngularMomentum = {', file=fout)
            for k, v in self.max_angular_momentum.items():
                print('      {} = "{}"'.format(k, v), file=fout)
            print('    }', file=fout)
        print('}', file=fout)
    
    def adjust_path(self, basepath=os.curdir):
        if (self.type2filenames):
            if not os.path.isabs(self.prefix):
                self.prefix = os.path.join(basepath, self.prefix)
        else:
            l_maps = {}
            for k, v in self.skfiles.items():
                if os.path.isabs(v):
                    l_maps[k] = v
                else:
                    l_v = os.path.join(basepath, v)
                    l_maps[k] = l_v
            self.skfiles = l_maps

class Geometry:
    def __init__(self, jsondata):
        self.charge = jsondata.get("charge", 0)
        self.coordinates = jsondata.get("coordinates", list())

        if ('spin' in jsondata):
            self.spin = jsondata.get('spin', 1)
        if ('spinpol' in jsondata):
            self.spinpol = jsondata.get('spinpol', False)

        if ('lattice_vectors' in jsondata):
            self.lattice_vectors = jsondata['lattice_vectors']
            self.fractional_coordinates = jsondata['fractional_coordinates']
            self.scaling_factor = jsondata['scaling_factor']
            self.kpoints = jsondata['kpoints']

    def ispbc(self):
        return hasattr(self, 'lattice_vectors')

    def get_coordinate_struct(self):
        symbols = [x[0] for x in self.coordinates]
        coords = [x[1:4] for x in self.coordinates]
        if (hasattr(self, 'lattice_vectors')):
            lattice = mg.Lattice(self.lattice_vectors)
            mole = mg.Structure(lattice=lattice, species=symbols, coords=coords, coords_are_cartesian=(not self.fractional_coordinates))
        else:
            if (hasattr(self, 'spin')):
                mole = mg.Molecule(species=symbols, coords=coords, charge=self.charge, spin_multiplicity=self.spin)
            else:
                mole = mg.Molecule(species=symbols, coords=coords, charge=self.charge)
        return mole

class System:
    def __init__(self, jsondata):
        self.name = jsondata.get("name", "")
        self.template_input = jsondata.get("template_input", '')
        self.uuid = jsondata.get('uuid', uuid.uuid4() )
        self.geometry = Geometry(jsondata.get("geometry", dict()))

        if ('elec_data' in jsondata):
            self.elec_data =  jsondata['elec_data']

    def to_hsd(self, fout):
        # fout = io.StringIO()
        
        #write geometry
        symbols = [x[0] for x in self.geometry.coordinates]
        coords = [x[1:4] for x in self.geometry.coordinates]

        elements = list(set(symbols))
        pbc = False

        if (hasattr(self.geometry, 'lattice_vectors')):
            pbc = True

        print('!Geometry = !GenFormat{', file=fout)
        # fractional = False
        if (not pbc):
            print('{} C'.format(len(symbols)), file=fout)
        else:
            if (self.geometry.fractional_coordinates):
                print('{} F'.format(len(symbols)), file=fout)
                # fractional = True
            else:
                print('{} S'.format(len(symbols)), file=fout)
        print(' '.join(elements),file=fout)
        for i in range(len(symbols)):
            print('{} {} {:20.12F} {:20.12F} {:20.12F}'.format(
                i+1, elements.index(symbols[i])+1, *coords[i]
            ), file=fout)
        if (pbc):
            print("0.0 0.0 0.0", file=fout)
            for i in range(3):
                print('{:20.12F} {:20.12F} {:20.12F}'.format(
                *self.geometry.lattice_vectors[i]
            ), file=fout)
        print('}', file=fout)

        #write Hamiltonian
        print('\n+Hamiltonian = +DFTB{', file=fout)
        print('   !Charge = {}'.format(self.geometry.charge), file=fout)
        if (pbc):
            if ('supercell_folding' in self.geometry.kpoints):
                print('   !KPointsAndWeights = SupercellFolding{', file=fout)
                for line in self.geometry.kpoints['supercell_folding']:
                    print('    {} {} {}'.format(*line), file=fout)
                print('    }', file=fout)
            else:
                raise RuntimeError('Not implemented')
        print('}', file=fout)
            
class EnergyEquation:
    def __init__(self, jsondata):
        self.energy = jsondata['energy']
        self.unit = jsondata.get('unit', 'kcal/mol')
        self.name = jsondata['name']
        self.uuid = jsondata['uuid']
        self.weight = jsondata.get('weight', 1.0)

class ReactionItem:
    def __init__(self, jsondata):
        self.coefficient = jsondata['coefficient']
        self.name = jsondata['name']
        self.uuid = jsondata['uuid']
    
class ReactionEquation:
    def __init__(self, jsondata):
        self.energy = jsondata['energy']
        self.unit = jsondata.get('unit', 'kcal/mol')
        self.name = jsondata['name']
        self.uuid = jsondata['uuid']
        self.weight = jsondata.get('weight', 1.0)
        self.products = [ReactionItem(x) for x in jsondata['products']]
        self.reactants = [ReactionItem(x) for x in jsondata['reactants']]
    
    def __str__(self):
        fout = io.StringIO()
        print('Reaction: {}'.format(self.name), file=fout)
        print('Energy: {:20.12f} {:8s}'.format(self.energy, self.unit), file=fout)       
        print('Reactants and coefficients:', file=fout)
        for item in self.reactants:
            print('    {:8.3f} {}'.format(item.coefficient, item.name), file=fout)
        print('Products and coefficients:', file=fout)
        for item in self.products:
            print('    {:8.3f} {}'.format(item.coefficient, item.name), file=fout)
        return fout.getvalue()

    

class ForceEquation:
    def __init__(self, jsondata):       
        self.name = jsondata['name']
        self.uuid = jsondata['uuid']
        self.weight = jsondata.get('weight', 1.0)
        if ('reference_force') in jsondata:
            self.reference_force = jsondata['reference_force']
        if 'fitting_indexes' in jsondata:
            self.fitting_indexes = jsondata['fitting_indexes']

class AdditionalEquation:
    def __init__(self, jsondata):
        self.unit = jsondata.get('unit', 'bohr')
        self.distance = jsondata['distance']
        self.derivative = jsondata['derivative']
        self.value = jsondata['value']
        self.weight = jsondata.get('weight', 1.0)
        
class ErepfitInput:
    def __init__(self, jsondata):
        self.electronic_slater_koster_files = SKFileInfo(jsondata['electronic_slater_koster_files'])
        self.atomic_energy = jsondata.get('atomic_energy', dict())
        
        self.external_repulsive_potentials = jsondata.get('external_repulsive_potentials', dict())
        self.dftb_options = jsondata.get('dftb_options', dict())
        self.potential_grids = jsondata.get('potential_grids', dict())
        self.options = jsondata.get('options', dict())
        self.systems = [System(system) for system in jsondata.get('systems', list())]
        self.equations = {}
        node = jsondata.get('equations', dict())
        keywords = [
            ('energy', EnergyEquation),
            ('force', ForceEquation), 
            ('reaction', ReactionEquation)
        ]
        for key, clas in keywords:
            if (key in node):
                self.equations[key] = [clas(x) for x in node[key] ]
        if ('additional' in node):
             self.equations['additional'] = {'{}-{}'.format(*sorted(k.split('-'))): [AdditionalEquation(x) for x in v] for k, v in node['additional'].items() }

