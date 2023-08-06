from . import rep_spline
from . import rep_basis

from .rep_model import EnergyEquationDescription

import numpy as np
from sklearn import linear_model


class GeneralSolver():
    def __init__(self, solver=linear_model.LinearRegression()):
        self.solver = solver
    
    def solve(self, model, builder):
        #avaliable only for Spline model
        if (not isinstance(model.rep_models[0], rep_basis.BasisRepulsiveModel)):
            raise RuntimeError('The repulsive potential is not represented by basis functions')
        
        eqmat = np.concatenate([ x.equ_block for x in builder.equation_descriptions ])
        vref = np.concatenate([ x.ref_block for x in builder.equation_descriptions ])

        all_missing_atoms = list(set(sum([ list(x.missing_atom_counts.keys()) for x in builder.equation_descriptions if isinstance(x, EnergyEquationDescription) ], [])))
        final_mat = builder._extend_atomic_energy_equations(all_missing_atoms, eqmat)

        self.solver.fit(final_mat, vref)
        # #transform back for all coefficients
        a4 = self.solver.coef_[:eqmat.shape[1]]
        builder.fitted_atom_energy = { k: self.solver.coef_[eqmat.shape[1]+i] for i, k in enumerate(all_missing_atoms) }      

        model.resulting_repulsives = []

        shift = 0
        for ind in range(len(model.rep_names)):
            rep_name = model.rep_names[ind]
            rep_model = model.rep_models[ind]
            nvar = rep_model.num_variables

            coeffs = a4[shift:shift+nvar] 
            shift += nvar

            newrep = rep_basis.PolynomialRepulsive(rep_name, rep_model.cutoff, coeffs, rep_model.minimal_order, rep_model.start)
            spl_rep = newrep.to_spline4()
            model.resulting_repulsives.append(spl_rep)
        
        return a4

class ContinuitySolver():
    def __init__(self, continuous_order=3, solver=linear_model.LinearRegression()):
        self.continuous_order = continuous_order
        self.solver = solver

    def make_Q_R_S_matrix(self, dx, size):
        """ Get the continuity condition equations
        """
        mat_full = np.zeros( (size, size+1))
        mat_shift_full = np.zeros( (size, size+1))

        for i in range(0, size):
            for j in range(i, size+1):
                mat_shift_full[i, j] = 1.0*dx**(j-i)
                if (i==0):
                    mat_full[i, j] = 1.0
                else:
                    mat_full[i, j] = mat_full[i-1, j-1]*j

        final_mat = mat_full*mat_shift_full
        Q_mat = final_mat[0:size, 0:size]
        S_mat = final_mat[0:size, size-5:size+1]
        R_mat = np.diagflat(np.diag(Q_mat))*-1
        
        return Q_mat, R_mat, S_mat
    
    def make_Q_R_matrix(self, dx, nvar, order):
        nrows = order+1
        ncols = nvar
        mat_full = np.zeros( (nrows, ncols))
        mat_shift_full = np.zeros( (nrows, ncols))
        for i in range(0, nrows):
            for j in range(i, ncols):
                mat_shift_full[i, j] = 1.0*dx**(j-i)
                if (i==0):
                    mat_full[i, j] = 1.0
                else:
                    mat_full[i, j] = mat_full[i-1, j-1]*j

        final_mat = mat_full*mat_shift_full
        R_mat = np.diagflat(np.diag(final_mat))*-1
        
        return final_mat, R_mat

    def solve(self, model, builder):
        #avaliable only for Spline model
        if (not isinstance(model.rep_models[0], rep_spline.Spline4RepulsiveModel)):
            raise RuntimeError('The repulsive potential is not represented by Spline functions')

        #transform the equations using continuous conditions
        #define the dimension of the matrices
        nsplines = sum([ len(x.spline_models) for x in model.rep_models])
        nvar = model.rep_models[0].spline_models[0].num_variables
        block_size = self.continuous_order+1
        w_block_size = nvar-block_size
        mat_T = np.zeros( ((block_size*nsplines), (block_size*nsplines)))
        mat_W = np.zeros( ((block_size*nsplines), (w_block_size*nsplines)))

        ind = 0
        for spline_model in model.rep_models:
            knots = spline_model.knots
            for i in range(len(knots)-1):
                dx = knots[i+1] - knots[i]
                Q_mat, R_mat, S_mat = self.make_Q_R_S_matrix(dx, block_size)
                mat_T[ind*block_size:(ind+1)*block_size, ind*block_size:(ind+1)*block_size] = Q_mat
                if (i < len(knots)-2):
                    mat_T[ind*block_size:(ind+1)*block_size, (ind+1)*block_size:(ind+2)*block_size] = R_mat
                mat_W[ind*block_size:(ind+1)*block_size, (ind)*w_block_size:(ind+1)*w_block_size] = S_mat
                ind += 1

        eqmat = np.concatenate([ x.equ_block for x in builder.equation_descriptions ])
        vref = np.concatenate([ x.ref_block for x in builder.equation_descriptions ])
        
        #make eqmat separately for e3 and e4
        e3_index = sum([list(range(i, i+block_size )) for i in range(0, eqmat.shape[1]-block_size, nvar)], [])
        e3 = eqmat[:, e3_index]
        e4_index = sum([list(range(i, i+w_block_size )) for i in range(block_size, eqmat.shape[1], nvar)], [])
        e4 = eqmat[:, e4_index]       
        mat_T_inv_W = np.dot(np.linalg.inv(mat_T), -mat_W)
        mat_A  = np.dot(e3, mat_T_inv_W) + e4


        #adding missing atoms
        #get missing atom vector
        all_missing_atoms = list(set(sum([ list(x.missing_atom_counts.keys()) for x in builder.equation_descriptions if isinstance(x, EnergyEquationDescription) ], [])))
        final_mat = builder._extend_atomic_energy_equations(all_missing_atoms, mat_A)

        #solve with regularization solver
        self.solver.fit(final_mat, vref)

        #transform back for all coefficients

        a4 = self.solver.coef_[:mat_A.shape[1]]
        builder.fitted_atom_energy = { k: self.solver.coef_[mat_A.shape[1]+i] for i, k in enumerate(all_missing_atoms) }      
        a3 = np.dot(mat_T_inv_W, a4)


        model.resulting_repulsives = []
        vunknowns = []
        shift = 0
        for ind in range(len(model.rep_names)):
            rep_name = model.rep_names[ind]
            rep_model = model.rep_models[ind]
            knots = rep_model.knots

            coeffs = []
            for i in range(len(knots)-1):
                coeffs.append( np.append(a3[shift*block_size:shift*block_size+block_size], a4[shift:shift+w_block_size] ))
                vunknowns += a3[shift*block_size:shift*block_size+block_size].tolist()
                vunknowns += a4[shift:shift+w_block_size].tolist()
                shift += 1
            
            
            spl_rep = rep_spline.RepulsivePotenial(rep_name, knots, coeffs)
            model.resulting_repulsives.append(spl_rep)

        return np.array(vunknowns)

class ContinuityAdapter():
    def __init__(self, continuous_order=3):
        self.continuous_order = continuous_order
        

    def make_Q_R_S_matrix(self, dx, size):
        """ Get the continuity condition equations
        """
        mat_full = np.zeros( (size, size+1))
        mat_shift_full = np.zeros( (size, size+1))

        for i in range(0, size):
            for j in range(i, size+1):
                mat_shift_full[i, j] = 1.0*dx**(j-i)
                if (i==0):
                    mat_full[i, j] = 1.0
                else:
                    mat_full[i, j] = mat_full[i-1, j-1]*j

        final_mat = mat_full*mat_shift_full
        Q_mat = final_mat[0:size, 0:size]
        S_mat = final_mat[0:size, size-5:size+1]
        R_mat = np.diagflat(np.diag(Q_mat))*-1
        
        return Q_mat, R_mat, S_mat
    
    def make_Q_R_matrix(self, dx, nvar, order):
        nrows = order+1
        ncols = nvar
        mat_full = np.zeros( (nrows, ncols))
        mat_shift_full = np.zeros( (nrows, ncols))
        for i in range(0, nrows):
            for j in range(i, ncols):
                mat_shift_full[i, j] = 1.0*dx**(j-i)
                if (i==0):
                    mat_full[i, j] = 1.0
                else:
                    mat_full[i, j] = mat_full[i-1, j-1]*j

        final_mat = mat_full*mat_shift_full
        R_mat = np.diagflat(np.diag(final_mat))*-1
        
        return final_mat, R_mat

    def setup(self, model):
        #avaliable only for Spline model
        if (not isinstance(model.rep_models[0], rep_spline.Spline4RepulsiveModel)):
            raise RuntimeError('The repulsive potential is not represented by Spline functions')

        #transform the equations using continuous conditions
        #define the dimension of the matrices
        nsplines = sum([ len(x.spline_models) for x in model.rep_models])
        nvar = model.rep_models[0].spline_models[0].num_variables
        self.block_size = self.continuous_order+1
        self.w_block_size = nvar-self.block_size
        mat_T = np.zeros( ((self.block_size*nsplines), (self.block_size*nsplines)))
        mat_W = np.zeros( ((self.block_size*nsplines), (self.w_block_size*nsplines)))

        ind = 0
        for spline_model in model.rep_models:
            knots = spline_model.knots
            for i in range(len(knots)-1):
                dx = knots[i+1] - knots[i]
                Q_mat, R_mat, S_mat = self.make_Q_R_S_matrix(dx, self.block_size)
                mat_T[ind*self.block_size:(ind+1)*self.block_size, ind*self.block_size:(ind+1)*self.block_size] = Q_mat
                if (i < len(knots)-2):
                    mat_T[ind*self.block_size:(ind+1)*self.block_size, (ind+1)*self.block_size:(ind+2)*self.block_size] = R_mat
                mat_W[ind*self.block_size:(ind+1)*self.block_size, (ind)*self.w_block_size:(ind+1)*self.w_block_size] = S_mat
                ind += 1

        self.mat_T_inv_W = np.dot(np.linalg.inv(mat_T), -mat_W)
        self.model = model


    def transform(self, a4):
        a3 = np.dot(self.mat_T_inv_W, a4)

        vunknowns = []
        shift = 0
        for ind in range(len(self.model.rep_names)):
            rep_model = self.model.rep_models[ind]
            knots = rep_model.knots

            coeffs = []
            for i in range(len(knots)-1):
                coeffs.append( np.append(a3[shift*self.block_size:shift*self.block_size+self.block_size], a4[shift:shift+self.w_block_size] ))
                vunknowns += a3[shift*self.block_size:shift*self.block_size+self.block_size].tolist()
                vunknowns += a4[shift:shift+self.w_block_size].tolist()
                shift += 1
        return np.array(vunknowns)



# def solve_with_continuous_condition2(self, modelcollection, continuous_order=3):
        
    #     #avaliable only for Spline model
    #     if (not isinstance(modelcollection.rep_models[0], rep_spline.Spline4RepulsiveModel)):
    #         raise RuntimeError('The repulsive potential is not represented by Spline functions')
        
    #     #define the dimension of the matrices
    #     nsplines = sum([ len(x.spline_models) for x in modelcollection.rep_models])
    #     nvar = modelcollection.rep_models[0].spline_models[0].num_variables
        
    #     block_size = continuous_order+1
    #     w_block_size = nvar-block_size
    #     mat_C = np.zeros( ((block_size*nsplines), modelcollection.get_total_num_variables()) )
    #     vec_D = np.zeros( (block_size*nsplines) )               
        
    #     # print('Size of T and W ', mat_T.shape, mat_W.shape)
    #     # ref_vref = np.genfromtxt('../ref/vref.dat')
    #     # ref_eqmat = np.genfromtxt('../ref/eqmat.dat')

    #     ind = 0
    #     for spline_model in modelcollection.rep_models:
    #         knots = spline_model.knots
    #         for i in range(len(knots)-1):
    #             dx = knots[i+1] - knots[i]
    #             Q_mat, R_mat = self.make_Q_R_matrix(dx, nvar, continuous_order)
    #             mat_C[ind*block_size:(ind+1)*block_size, ind*nvar:(ind+1)*nvar] = Q_mat
                
    #             if (i < len(knots)-2):
    #                 mat_C[ind*block_size:(ind+1)*block_size, (ind+1)*nvar:(ind+1)*nvar+block_size] = R_mat

    #             ind += 1

    #     eqmat = np.concatenate([ x.equ_block for x in self.equation_descriptions ])
    #     vref = np.concatenate([ x.ref_block for x in self.equation_descriptions ])
        
    #     t, r, res, x, info = scipy.linalg.lapack.dgglse(eqmat, mat_C, vref, vec_D)

    #     print(x)
    #     modelcollection.resulting_repulsives = []
    #     shift = 0
    #     for ind in range(len(modelcollection.rep_names)):
    #         rep_name = modelcollection.rep_names[ind]
    #         rep_model = modelcollection.rep_models[ind]
    #         knots = rep_model.knots

    #         coeffs = []
    #         for i in range(len(knots)-1):
    #             coeffs.append( x[shift:shift+nvar] )
    #             shift += nvar
            
    #         spl_rep = spline_rep.RepulsivePotenial(rep_name, knots, coeffs)
    #         with open('{}.skf'.format(rep_name), 'w') as fout:
    #             print(spl_rep, file=fout)
    #         modelcollection.resulting_repulsives.append(spl_rep)