#!/usr/bin/env python3

import os
import pymatgen as mg 
import pymatgen.core.units 

def which(file: str) -> str:
    for path in os.environ["PATH"].split(os.pathsep):
        if os.path.exists(os.path.join(path, file)):
            return os.path.join(path, file)

    return file

def get_energy_from_au(value: float, unit: str) -> float:
    if (unit.lower() == 'h'):
        return value
    elif (unit.lower() == 'ev'):
        return mg.core.units.Energy(value, 'Ha').to('eV')
    elif (unit.lower() == 'kcal/mol'):
        return value*627.50947415
    else:
        raise ValueError('Unknown unit: {}'.format(unit))


def get_energy_in_au(value: float, unit: str) -> float:
    if (unit.lower() == 'h'):
        return value
    elif (unit.lower() == 'ev'):
        return mg.core.units.Energy(value, 'eV').to('Ha')
    elif (unit.lower() == 'kcal/mol'):
        return value/627.50947415
    else:
        raise ValueError('Unknown unit: {}'.format(unit))

def get_length_in_au(value: float, unit: str) -> float:
    if (unit.lower() == 'bohr'):
        return value
    elif (unit.lower() == 'aa'):
        return value*mg.core.units.ang_to_bohr
    else:
        raise ValueError('Unknown unit: {}'.format(unit))
