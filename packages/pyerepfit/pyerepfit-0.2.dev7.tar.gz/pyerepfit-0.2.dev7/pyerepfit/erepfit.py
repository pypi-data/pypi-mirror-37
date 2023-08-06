#!/usr/bin/env python3

import argparse
import os
import sys
import json
import jsonschema
import yaml
import jsonpickle
import numpy as np

from . import evaluator
from .inputdata import ErepfitInput
from .rep_basis import PolynomialRepulsive, BasisRepulsiveModel
from .rep_spline import RepulsivePotenial, Spline4RepulsiveModel
from . import rep_model
from . import utils
from . import equation_solver
import os

from pyerepfit import __version__

class Erepfit:

    def __init__(self, output_stream=sys.stdout):
        self.output_stream = output_stream

    def print_header(self):
        print(
"""
===============================================================================

        PyErepfit v{}
        Powered by Chien-Pin Chou

===============================================================================
""".format(__version__), file=self.output_stream
        )

    def load_input(self, options):
        parser = argparse.ArgumentParser()
        parser.add_argument("-y", dest='yaml', help='Parse input as YAML format', action='store_true')
        parser.add_argument("-e", dest='evaluate_only', help='Evaluate the DFTB only', action='store_true')
        parser.add_argument("-f", dest='fitting_only', help='Fitting the repulsive only', action='store_true')
        self.hasPrint = False
        try:
            import matplotlib.pyplot
            parser.add_argument("-p", dest='print', help='Print the repulsive to eps', action='store_true')
            self.hasPrint = True
        except:
            pass
        parser.add_argument("-o", dest='output_file', help='Output file', type=str)
        parser.add_argument("input_file_path", help="Input file path")

        self.opt = parser.parse_args(options)

        if (self.opt.output_file):
            self.output_stream = open(self.opt.output_file, 'w')
    
        print('Reading input schema.', file=self.output_stream)
        with open(os.path.join(os.path.dirname(__file__), 'erepfit_input_schema.json'), 'r') as f:
            input_schema = json.load(f)

        if (self.opt.yaml):
            print('Reading input file as YAML', file=self.output_stream)
            with open(self.opt.input_file_path, 'r') as f:
                input_file = yaml.load(f)
        else:
            print('Reading input file as JSON', file=self.output_stream)
            with open(self.opt.input_file_path, 'r') as f:
                input_file = json.load(f)

        print('Validate input file.', file=self.output_stream)
        jsonschema.validate(input_file, input_schema)

        self.input = ErepfitInput(input_file)

    def initialize_solver(self):
        if (self.input.options.get("potential_type") == "polynomial"):
            self.solver = equation_solver.GeneralSolver()
        else:
            self.solver = equation_solver.ContinuitySolver(3)

    def initialize_skfile_path(self):
        self.input.electronic_slater_koster_files.adjust_path(os.path.abspath(os.curdir))

    def initialize_model(self):       
        rep_models = []
        rep_names = []
        poten_type = self.input.options.get("potential_type")
        
        for k, v in self.input.potential_grids.items():
            if (k in self.input.external_repulsive_potentials):
                print('Repulsive {} found in external repulsuive potentials, will not be fitted.'.format(k), file=self.output_stream)
                continue
            if (poten_type == "polynomial"):
                cutoff = v['knots'][-1]
                model = BasisRepulsiveModel(cutoff, minimal_order=3, order=9, start=v['knots'][0])
            else: 
                model = Spline4RepulsiveModel(v['knots'])
            rep_names.append(k)
            rep_models.append(model)

        self.collection = rep_model.RepulsiveModelCollection(rep_names, rep_models)      

        print("", file=self.output_stream)
        print(self.collection.description(), file=self.output_stream)

    def evaluate_elec_data(self):
        print('Testing DFTB implementation for parameterization...', file=self.output_stream)
        dftb_path = self.input.options['toolchain']['path']
        if not os.path.isabs(dftb_path):
            dftb_path = os.path.expanduser(dftb_path)
        dftb_path = os.path.expandvars(dftb_path)
        if not os.path.isabs(dftb_path):
            dftb_path = utils.which(dftb_path)

        succ = evaluator.test_dftb_binary(dftb_path)
        if (succ):
            print('  {} => working'.format(dftb_path), file=self.output_stream)
        else:
            print('  {} => not working'.format(dftb_path), file=self.output_stream)
            sys.exit(1)
        
        evaluator.evaluate(self.input)
        print('\nEvaluate DFTB...done', file=self.output_stream)

        jsonpickle.set_encoder_options('simplejson', indent=4)
        jsonpickle.set_encoder_options('json', indent=4)
        
        filename = 'evaluated_{}.json'.format(os.path.basename(self.opt.input_file_path))
        with open(filename, 'w') as f:
            js = jsonpickle.encode(self.input, unpicklable=False)
            print(js, file=f)
            print('Evaluated input file has been saved as {}'.format(filename))

    def build(self):
        self.builder = rep_model.RepulsivePotentialEquationBuilder(self.input)
        self.builder.build_linear_equations(self.collection)

    def write_bond_statistic_graphs(self, filename='bond_length.pdf'):
        from matplotlib.backends.backend_pdf import PdfPages
        import matplotlib.pyplot as plt
        import datetime
        pair_bond_data = {}
        for uuid, dist_matrix in self.builder.dist_matrix_uuids.items():
            system = self.builder.uuidmap[uuid]
            for index_pair, dist_vector in dist_matrix.items():
                elem1 = system.geometry.coordinates[index_pair[0]][0]
                elem2 = system.geometry.coordinates[index_pair[1]][0]
                if elem1 > elem2 :
                    continue
                poten_name = '{}-{}'.format(elem1, elem2)
                if poten_name not in self.final_repulsive_potentials:
                    continue
                distances = [x[0] for x in dist_vector if x[0] <= self.final_repulsive_potentials[poten_name].knots[-1]]
                if (elem1, elem2) not in pair_bond_data:
                    pair_bond_data[(elem1, elem2)] = np.array([])
                    
                pair_bond_data[(elem1, elem2)] = np.append(pair_bond_data[(elem1, elem2)], distances)
        with PdfPages(filename) as pdf:
            for k, v in pair_bond_data.items():
                plt.figure(figsize=(5, 5))
                plt.hist(v, bins=50)
                plt.xlabel('Distance [bohr]')
                plt.title('{}-{}'.format(*k))
                pdf.savefig()  
                plt.close()

            d = pdf.infodict()
            d['Title'] = 'Bond Length'
            d['CreationDate'] = datetime.datetime.today()

    def solve(self):
        self.builder.solve(self.collection, self.solver)
    
    def print_residuals(self):
        self.builder.print_residuals(self.output_stream)

        self.final_repulsive_potentials = {}
        for ind in range(len(self.collection.rep_names)):
            rep_name = self.collection.rep_names[ind]
            spl_rep = self.collection.resulting_repulsives[ind]
            reversed_rep_name = '{}-{}'.format(*reversed(rep_name.split('-')))
            self.final_repulsive_potentials[rep_name] = spl_rep
            self.final_repulsive_potentials[reversed_rep_name] = spl_rep

    def write(self):
        print('Resulting Repulsive Potentials:', file=self.output_stream)
        output_prefix = self.input.options.get("output_prefix", "./")
        os.makedirs(output_prefix, exist_ok=True)
        
        for ind in range(len(self.collection.rep_names)):
            rep_name = self.collection.rep_names[ind]
            spl_rep = self.collection.resulting_repulsives[ind]
            reversed_rep_name = '{}-{}'.format(*reversed(rep_name.split('-')))
        
            with open(os.path.join(output_prefix, '{}.skf'.format(rep_name)), 'w') as fout:
                print(spl_rep, file=fout)
            if (reversed_rep_name != rep_name):
                with open(os.path.join(output_prefix, '{}.skf'.format(reversed_rep_name)), 'w') as fout:
                    print(spl_rep, file=fout)

            print(rep_name, file=self.output_stream)
            print(spl_rep, file=self.output_stream)

            if (self.hasPrint and self.opt.print):
                import matplotlib.pyplot as plt
                plt.figure()
                output_fig = os.path.join(output_prefix, '{}.eps'.format(rep_name))

                plt.title(rep_name)
                # plt.ylim(-2, 2)

                styles = ['c--', 'r--', 'g--']
                labels = ['Rep. Potential', '1st derivative', '2nd derivative']
                for i in range(3):
                    xs = np.linspace(spl_rep.knots[0]-0.2, spl_rep.knots[-1], num=100)
                    ys = []
                    for r in xs:
                        v = spl_rep.eval(r, i)
                        ys.append(v)
                    if (i==0):
                        maxv = max(ys)
                        minv = min(ys)
                        plt.ylim(min(minv, max(-0.5, -maxv)), maxv)
                    plt.plot(xs, ys, styles[i], linewidth=1, label=labels[i])

                plt.legend(loc='upper right')
                plt.xlabel('Diatomic Distance [a.u.]')
                plt.ylabel('Energy [a.u.]')
                plt.savefig(output_fig, format='eps')


    def run(self, options):       
        self.print_header()
        self.load_input(options)
        
        # if only evaluate electronic reference values
        if (self.opt.evaluate_only or not self.opt.fitting_only):
            self.initialize_skfile_path()
            self.evaluate_elec_data()

        if (self.opt.fitting_only or not self.opt.evaluate_only):
            self.initialize_model()
            self.initialize_solver()
            self.build()
            self.solve()
            self.print_residuals()
            self.write()
            self.write_bond_statistic_graphs()

        print('End of pyerepfit Program', file=self.output_stream)        
        

if __name__ == '__main__':
    erepfit = Erepfit()
    erepfit.run(sys.argv[1:])
    



