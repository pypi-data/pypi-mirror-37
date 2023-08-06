#!/usr/bin/env python3

import subprocess
import tempfile
import os
import scipy.constants
import numpy
# from erepfit import *

def Bool2YesNo(value):
    if (value):
        return "Yes"
    else:
        return "No"

def evaluate_atom(dftb_path, dftb_input, skfileinfo):
    with tempfile.TemporaryDirectory() as tmp:
        with open(os.path.join(tmp, 'dftb_in.hsd'), 'w') as fout:
            #copy the template input
            with open(dftb_input, 'r') as fin:
                fout.write(fin.read())
            #add SK file info
            skfileinfo.to_hsd(fout)
            print('*ParserOptions = {', file=fout)
            print('    !IgnoreUnprocessedNodes = Yes', file=fout)
            print('}', file=fout)
        
        res = subprocess.run([dftb_path], stdout=subprocess.PIPE, cwd=tmp)
        if (res.returncode == 0):
            try:
                with open(os.path.join(tmp,'detailed.out'), 'r') as fin:
                    for line in fin:
                        if 'Total energy' in line:
                            return float(line.split()[2])
            except:
                raise RuntimeError(res.stdout.decode())
        else:
            raise RuntimeError(res.stdout.decode())            



def evaluate_system(dftb_path, system, skfileinfo, dftb_options):
    with tempfile.TemporaryDirectory() as tmp:
        with open(os.path.join(tmp, 'dftb_in.hsd'), 'w') as fout:
            #copy the template input
            with open(system.template_input, 'r') as fin:
                fout.write(fin.read())
            #add SK file info
            skfileinfo.to_hsd(fout)
            system.to_hsd(fout)

            if 'hubbard_derivatives' in dftb_options:
                print('+Hamiltonian = +DFTB {', file=fout)
                print('   *HubbardDerivs = {', file=fout)
                for k, v in dftb_options['hubbard_derivatives'].items():
                    print('        !{} = {}'.format(k,v), file=fout)
                print('    }', file=fout)
                print('}', file=fout)

            print('*Options = {', file=fout)
            print('    !WriteAutotestTag = Yes', file=fout)
            print('}', file=fout)
            print('*Analysis = {', file=fout)
            print('    !CalculateForces = Yes', file=fout)
            print('}', file=fout)
            print('*ParserOptions = {', file=fout)
            print('    !IgnoreUnprocessedNodes = Yes', file=fout)
            print('}', file=fout)
            
        
        
        res = subprocess.run([dftb_path], stdout=subprocess.PIPE, cwd=tmp)
        if (res.returncode == 0):
            try:
                with open(os.path.join(tmp,'autotest.tag'), 'r') as fin:
                    for line in fin:
                        if line.startswith('total_energy'):
                            line = next(fin)
                            total_energy = float(line)
                        elif line.startswith('repulsive_energy'):
                            line = next(fin)
                            rep_energy = float(line)
                        elif line.startswith('repulsive_forces'):
                            entry = line.split(':')[3]
                            nrow = int(entry.split(',')[1])
                            rep_forces = []
                            for i in range(nrow):
                                line = next(fin)
                                rep_forces.append(list(map(float, line.split())))
                        elif line.startswith('forces'):
                            entry = line.split(':')[3]
                            nrow = int(entry.split(',')[1])
                            forces = []
                            for i in range(nrow):
                                line = next(fin)
                                forces.append(list(map(float, line.split())))
                elec_energy = (total_energy - rep_energy)
                elec_forces = ((numpy.array(forces)-numpy.array(rep_forces))).tolist()
                # print(system.name, '{:20.12f}'.format(elec_energy))
                # for line in elec_forces:
                #     print('{:20.12f} {:20.12f} {:20.12f}'.format(*line))
                return total_energy, elec_energy, elec_forces
                            
            except:
                with open(os.path.join(tmp, 'dftb_in.hsd'), 'r') as f:
                    print(f.read())
                raise RuntimeError(res.stdout.decode())  

                
        else:
            raise RuntimeError(res.stdout.decode())  

def evaluate(erepfit_input):
    from tqdm import tqdm
    
    print('Starting evaluation...')
    print('')
    
    dftb_path = erepfit_input.options['toolchain']['path']

    for atom_symbol, atom_energy in erepfit_input.atomic_energy.items():
        if (type(atom_energy) != float):
            res = evaluate_atom(dftb_path, atom_energy, erepfit_input.electronic_slater_koster_files)
            erepfit_input.atomic_energy[atom_symbol] = res

    # size = len(erepfit_input.systems)
    for _, system in enumerate(tqdm(erepfit_input.systems)):
        _, elec_energy, elec_forces = evaluate_system(dftb_path, system, erepfit_input.electronic_slater_koster_files, erepfit_input.dftb_options)
        system.elec_data = {}
        system.elec_data['elec_energy'] = elec_energy
        system.elec_data['elec_forces'] = elec_forces
    

def test_dftb_binary(dftb_path):
    with tempfile.TemporaryDirectory() as tmp:
        res = subprocess.run([dftb_path], stdout=subprocess.PIPE, cwd=tmp)
        if (res.returncode == 0):
            for line in res.stdout.decode().splitlines():
                if ('DFTB+ paramerization version by Chien-Pin Chou:' in line):
                    version = int(line.split(':')[1])
                    if (version >= 20180919):
                        return True
        else:
            return False
    return False