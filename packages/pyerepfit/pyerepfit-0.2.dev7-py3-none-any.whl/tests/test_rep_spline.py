
import pyerepfit.rep_spline
import pytest
from numpy.testing import assert_almost_equal
import io

class TestSpline3():   
    def setup(self):
        self.spl_rep = pyerepfit.rep_spline.Spline3(1.0, 2.0, *[0.2, 0.3, 0.4, 0.5])

    def test_init(self):
        assert self.spl_rep.r0 == 1.0
        assert self.spl_rep.r1 == 2.0
        assert self.spl_rep.a0 == 0.2
        assert self.spl_rep.a1 == 0.3
        assert self.spl_rep.a2 == 0.4
        assert self.spl_rep.a3 == 0.5

    def test_eval_wrong_r1(self):
        with pytest.raises(ValueError):
            self.spl_rep.eval(0.0)
    
    def test_eval_wrong_r2(self):
        with pytest.raises(ValueError):
            self.spl_rep.eval(2.1)

    def test_eval_wrong_derv1(self):
        with pytest.raises(ValueError):
            self.spl_rep.eval(1.0, -1)
        
    def test_eval_wrong_derv2(self):
        with pytest.raises(ValueError):
            self.spl_rep.eval(1.0, 3)
        


    @pytest.mark.parametrize("derv, r, expected", [
        (0, 1.0, 0.2),
        (1, 1.0, 0.3),
        (2, 1.0, 0.8),  
        (0, 2.0, 1.4),
        (1, 2.0, 2.6),
        (2, 2.0, 3.8),
    ])
    def test_eval(self, derv, r, expected):
        assert self.spl_rep.eval(r, derv) == expected
    
    def test_str(self):
        assert str(self.spl_rep) == '1.000000     2.000000       2.000000000000E-01   3.000000000000E-01   4.000000000000E-01   5.000000000000E-01'

class TestSpline4():   
    def setup(self):
        self.spl_rep = pyerepfit.rep_spline.Spline4(1.0, 2.0, *[0.2, 0.3, 0.4, 0.5, 0.6])

    def test_init(self):
        assert self.spl_rep.r0 == 1.0
        assert self.spl_rep.r1 == 2.0
        assert self.spl_rep.a0 == 0.2
        assert self.spl_rep.a1 == 0.3
        assert self.spl_rep.a2 == 0.4
        assert self.spl_rep.a3 == 0.5
        assert self.spl_rep.a4 == 0.6

    def test_eval_wrong_r1(self):
        with pytest.raises(ValueError):
            self.spl_rep.eval(0.0)
    
    def test_eval_wrong_r2(self):
        with pytest.raises(ValueError):
            self.spl_rep.eval(2.1)

    def test_eval_wrong_derv1(self):
        with pytest.raises(ValueError):
            self.spl_rep.eval(1.0, -1)
        
    def test_eval_wrong_derv2(self):
        with pytest.raises(ValueError):
            self.spl_rep.eval(1.0, 4)
        


    @pytest.mark.parametrize("derv, r, expected", [
        (0, 1.0, 0.2),
        (1, 1.0, 0.3),
        (2, 1.0, 0.8),  
        (3, 1.0, 3.0),  
        (0, 2.0, 2.0),
        (1, 2.0, 5.0),
        (2, 2.0, 11.0),
        (3, 2.0, 17.4),
    ])
    def test_eval(self, derv, r, expected):
        assert self.spl_rep.eval(r, derv) == expected
    
    def test_str(self):
        assert str(self.spl_rep) == '1.000000     2.000000       2.000000000000E-01   3.000000000000E-01   4.000000000000E-01   5.000000000000E-01   6.000000000000E-01'

class TestSpline5():   
    def setup(self):
        self.spl_rep = pyerepfit.rep_spline.Spline5(1.0, 2.0, *[0.2, 0.3, 0.4, 0.5, 0.6, 0.7])

    def test_init(self):
        assert self.spl_rep.r0 == 1.0
        assert self.spl_rep.r1 == 2.0
        assert self.spl_rep.a0 == 0.2
        assert self.spl_rep.a1 == 0.3
        assert self.spl_rep.a2 == 0.4
        assert self.spl_rep.a3 == 0.5
        assert self.spl_rep.a4 == 0.6
        assert self.spl_rep.a5 == 0.7

    def test_eval_wrong_r1(self):
        with pytest.raises(ValueError):
            self.spl_rep.eval(0.0)
    
    def test_eval_wrong_r2(self):
        with pytest.raises(ValueError):
            self.spl_rep.eval(2.1)

    def test_eval_wrong_derv1(self):
        with pytest.raises(ValueError):
            self.spl_rep.eval(1.0, -1)
        
    def test_eval_wrong_derv2(self):
        with pytest.raises(ValueError):
            self.spl_rep.eval(1.0, 4)
        


    @pytest.mark.parametrize("derv, r, expected", [
        (0, 1.0, 0.2),
        (1, 1.0, 0.3),
        (2, 1.0, 0.8),  
        (3, 1.0, 3.0),  
        (0, 2.0, 2.7),
        (1, 2.0, 8.5),
        (2, 2.0, 25.0),
        (3, 2.0, 59.4),
    ])
    def test_eval(self, derv, r, expected):
        assert self.spl_rep.eval(r, derv) == expected
    
    def test_str(self):
        assert str(self.spl_rep) == '1.000000     2.000000       2.000000000000E-01   3.000000000000E-01   4.000000000000E-01   5.000000000000E-01   6.000000000000E-01   7.000000000000E-01'

class TestSpline4Model():

    def setup(self):
        self.model = pyerepfit.rep_spline.Spline4Model(1.0, 2.0)
    
    def test_init(self):
        assert self.model.x1 == 1.0
        assert self.model.x2 == 2.0
        assert self.model.num_variables == 5

    @pytest.mark.parametrize("derv, r, expected", [
        (0, 1.0, [1.    , 0.0   , 0.0  , 0.0 , 0.0]),
        (0, 1.5, [1.    , 0.5   , 0.25  , 0.125 , 0.0625]),
        (0, 2.0, [1.    , 1.0   , 1.0  , 1.0 , 1.0]),

        (1, 1.0, [0.    , 1.0   , 0.0  , 0.0 , 0.0]),
        (1, 1.5, [0.    , 1.0   , 1.0  , 0.75 , 0.5]),
        (1, 2.0, [0.    , 1.0   , 2.0  , 3.0 , 4.0]),

        (2, 1.0, [0.    , 0.0   , 2.0  , 0.0 , 0.0]),
        (2, 1.5, [0.    , 0.0   , 2.0  , 3.0 , 3.0]),
        (2, 2.0, [0.    , 0.0   , 2.0  , 6.0 , 12.0]),

        (3, 1.0, [0.    , 0.0   , 0.0  , 6.0 , 0.0]),
        (3, 1.5, [0.    , 0.0   , 0.0  , 6.0 , 12.0]),
        (3, 2.0, [0.    , 0.0   , 0.0  , 6.0 , 24.0]),
    ])
    def test_get_row(self, derv, r, expected):
        row = self.model.get_row(r, derv)
        assert_almost_equal(row, expected)

    def test_eval_wrong_order(self):
        with pytest.raises(ValueError):
            self.model.get_row(1.5, -1)
    
    def test_eval_wrong_order2(self):
        with pytest.raises(ValueError):
            self.model.get_row(1.5, 4)

class TestSpline4RepulsiveModel():
    def setup(self):
        self.model = pyerepfit.rep_spline.Spline4RepulsiveModel([1.0, 2.0, 3.0])
    
    def test_init(self):
        assert self.model.cutoff == 3.0
        assert self.model.knots == [1.0, 2.0, 3.0]
        assert len(self.model.spline_models) == 2
        
        assert isinstance(self.model.spline_models[0], pyerepfit.rep_spline.Spline4Model)
        assert isinstance(self.model.spline_models[1], pyerepfit.rep_spline.Spline4Model)

        assert self.model.spline_models[0].x1 == 1.0
        assert self.model.spline_models[0].x2 == 2.0

        assert self.model.spline_models[1].x1 == 2.0
        assert self.model.spline_models[1].x2 == 3.0

        assert self.model.num_variables == 10
    
    @pytest.mark.parametrize("derv, r, expected", [
        (0, 1.0, [1.    , 0.0   , 0.0  , 0.0   , 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
        (0, 1.5, [1.    , 0.5   , 0.25 , 0.125 , 0.0625, 0.0, 0.0, 0.0, 0.0, 0.0]),
        (1, 1.0, [0.    , 1.0   , 0.0  , 0.0 , 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
        (1, 1.5, [0.    , 1.0   , 1.0  , 0.75 , 0.5, 0.0, 0.0, 0.0, 0.0, 0.0]),
        (2, 1.0, [0.    , 0.0   , 2.0  , 0.0 , 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
        (2, 1.5, [0.    , 0.0   , 2.0  , 3.0 , 3.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
        (3, 1.0, [0.    , 0.0   , 0.0  , 6.0 , 0.0,  0.0, 0.0, 0.0, 0.0, 0.0]),
        (3, 1.5, [0.    , 0.0   , 0.0  , 6.0 , 12.0, 0.0, 0.0, 0.0, 0.0, 0.0]),

        (0, 2.0, [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0]),       
        (1, 2.0, [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0]),
        (2, 2.0, [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 0.0, 0.0]),
        (3, 2.0, [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 6.0, 0.0,]),

        (0, 3.0, [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0]),       
        (1, 3.0, [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 2.0, 3.0, 4.0]),
        (2, 3.0, [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 6.0, 12.0]),
        (3, 3.0, [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 6.0, 24.0]),
    ])
    def test_get_row(self, derv, r, expected):
        row = self.model.get_row(r, derv)
        assert_almost_equal(row, expected)

    def test_description(self):
        assert self.model.description() == "Fourth-order spline-type repulsive potential"
    
    def test_str(self):
        assert str(self.model) == "Knots:   1.0000  2.0000  3.0000 bohr"

example_rep3 = """
Spline
56  4.8
2.152199575935475e+00  3.588744214431140e+00  -1.258017874873710e-01
2.00000  2.05000  3.630700389745626e-01  -1.052149737598174e+00  1.132218109539706e+00  -5.292659128856522e-01
2.05000  2.10000  3.132269391293926e-01  -9.428974209908465e-01  1.052828222606858e+00  -5.089503803087194e-01
2.10000  2.15000  2.686505198388286e-01  -8.414317265824756e-01  9.764856655605501e-01  -4.916781786921479e-01
2.15000  2.20000  2.289586879012698e-01  -7.474707463666119e-01  9.027339387567281e-01  -4.735905192759857e-01
2.20000  2.25000  1.937827866149213e-01  -6.607492813855086e-01  8.316953608653299e-01  -4.557213600958141e-01
2.25000  2.30000  1.627675957777974e-01  -5.809976554996945e-01  7.633371568509580e-01  -4.377936577707102e-01
2.30000  2.35000  1.355713316877188e-01  -5.079473922478793e-01  6.976681081853517e-01  -4.198816277900722e-01
2.35000  2.40000  1.118656471423143e-01  -4.413296936377693e-01  6.346858640168406e-01  -4.019654515768903e-01
2.40000  2.45000  9.133563143902092e-02  -3.808758481229121e-01  5.743910462803072e-01  -3.840501879493335e-01
2.45000  2.50000  7.367981037508232e-02  -3.263171199045011e-01  5.167835180879069e-01  -3.661354202107031e-01
2.50000  2.55000  5.861014624755075e-02  -2.773847837472909e-01  4.618632050563016e-01  -3.482177563324008e-01
2.55000  2.60000  4.585203785328545e-02  -2.338100964141539e-01  4.096305416064417e-01  -3.303111811223207e-01
2.60000  2.65000  3.514432048895352e-02  -1.953243761119269e-01  3.600838644380933e-01  -3.123631473808537e-01
2.65000  2.70000  2.623926595102983e-02  -1.616587132734741e-01  3.132293923309654e-01  -2.945698590931681e-01
2.70000  2.75000  1.890258253579685e-02  -1.325450479835762e-01  2.690439134669900e-01  -2.761990475278524e-01
2.75000  2.80000  1.291341503934456e-02  -1.077121494933362e-01  2.276140563378123e-01  -2.599835836077506e-01
2.80000  2.85000  8.064344757571326e-03  -8.690062073661312e-02  1.886165187966498e-01  -2.293296117042458e-01
2.85000  2.90000  4.162188816269246e-03  -6.975894094472990e-02  1.542170770410128e-01  -1.839332763238809e-01
2.90000  2.95000  1.036792802094807e-03  -5.571673281305778e-02  1.266270855924307e-01  -1.416038551163948e-01
2.95000  3.00000  -1.450176606466567e-03  -4.411605316718761e-02  1.053865073249714e-01  -9.535449998660865e-02
3.00000  3.05000  -3.404432309011839e-03  -3.429256118459007e-02  9.108333232698014e-02  -7.154236570823580e-02
3.05000  3.10000  -4.900294833137417e-03  -2.572079569470385e-02  8.035197747074481e-02  -6.996967463328146e-02
3.10000  3.15000  -5.994200883524913e-03  -1.821037050737895e-02  6.985652627575253e-02  -6.507038257991177e-02
3.15000  3.20000  -6.738211891026966e-03  -1.171274574915305e-02  6.009596888876580e-02  -6.106245057198321e-02
3.20000  3.25000  -7.181242062584203e-03  -6.161117239566319e-03  5.093660130296827e-02  -5.681567936068926e-02
3.25000  3.30000  -7.369058381225185e-03  -1.493574704474676e-03  4.241424939886491e-02  -5.263290491740509e-02
3.30000  3.35000  -7.344280606066432e-03  2.353103448531265e-03  3.451931366125418e-02  -4.843298260546413e-02
3.35000  3.40000  -7.146381272312415e-03  5.441787445115717e-03  2.725436627043452e-02  -4.423765500016908e-02
3.40000  3.45000  -6.811685691255565e-03  7.835441659657893e-03  2.061871802040918e-02  -4.004109643681834e-02
3.45000  3.50000  -6.373371950276248e-03  9.597005238422681e-03  1.461255355488640e-02  -3.584486699923454e-02
3.50000  3.55000  -5.861470912842804e-03  1.078942409141706e-02  9.235823505001238e-03  -3.164855201646169e-02
3.55000  3.60000  -5.302866218511507e-03  1.147564230179372e-02  4.488540702532001e-03  -2.745225008889184e-02
3.60000  3.65000  -4.721294282926600e-03  1.171860449638023e-02  3.707031891982038e-04  -2.325598148537122e-02
3.65000  3.70000  -4.137344297820266e-03  1.158125495415977e-02  -3.117694033607467e-03  -1.905956653076284e-02
3.70000  3.75000  -3.568458231012639e-03  1.112653880181830e-02  -5.976629013221909e-03  -1.486370365641335e-02
3.75000  3.80000  -3.028930826411832e-03  1.041739812307301e-02  -8.206184561683903e-03  -1.066577881192974e-02
3.80000  3.85000  -2.529909604013884e-03  9.516786325815148e-03  -9.806051383473359e-03  -6.475549767741770e-03
3.85000  3.90000  -2.079394859902776e-03  8.487614564209744e-03  -1.077738384863463e-02  -2.256599492859928e-03
3.90000  3.95000  -1.682239666250484e-03  7.392951683149835e-03  -1.111587377256362e-02  1.855161660056297e-03
3.95000  4.00000  -1.340149871316892e-03  6.295278018343890e-03  -1.083759952355517e-02  6.366958069743156e-03
4.00000  4.05000  -1.051684099449869e-03  5.259270251511450e-03  -9.882555813093701e-03  8.208348530459719e-03
4.05000  4.10000  -8.124009328407240e-04  4.332577284180531e-03  -8.651303533524748e-03  7.379333046066975e-03
4.10000  4.15000  -6.164779108347515e-04  3.522791928673562e-03  -7.544403576614706e-03  6.950352806822708e-03
4.15000  4.20000  -4.583305292417554e-04  2.820479217063252e-03  -6.501850655591284e-03  6.414183488087169e-03
4.20000  4.25000  -3.327594220915605e-04  2.218400527664780e-03  -5.539723132378212e-03  5.906735242167050e-03
4.25000  4.30000  -2.349503616339964e-04  1.708728728743213e-03  -4.653712846053158e-03  5.391591784475410e-03
4.30000  4.35000  -1.604742583389095e-04  1.283794382521464e-03  -3.844974078381849e-03  4.878508101056565e-03
4.35000  4.40000  -1.052871608961590e-04  9.358857854412045e-04  -3.113197863223367e-03  4.364880532313502e-03
4.40000  4.45000  -6.573025621561754e-05  6.573026031112155e-04  -2.458465783376333e-03  3.851368730600788e-03
4.45000  4.50000  -3.852986942717257e-05  4.403412902530888e-04  -1.880760473786216e-03  3.337937746081631e-03
4.50000  4.55000  -2.079746388072352e-05  2.772997759700799e-04  -1.380069811873973e-03  2.824067725772407e-03
4.55000  4.60000  -1.002964114618293e-05  1.604733027259760e-04  -9.564596530081139e-04  2.311873031416012e-03
4.60000  4.65000  -4.108141013477434e-06  8.216638516078486e-05  -6.096786982957135e-04  1.793416069048865e-03
4.65000  4.70000  -1.299841492546341e-06  3.464913584907952e-05  -3.406662879383799e-04  1.298332852764132e-03
4.70000  4.75000  -2.567588133428004e-07  1.032000345097257e-05  -1.459163600237608e-04  7.160169201494927e-04
4.75000  4.80000  -1.604742583488725e-08  1.098494349717707e-06  -3.851382200133723e-05  9.582369475487212e-04  -1.442677002340099e-02  8.894386417603511e-02
"""

example_rep4 = """
Spline4
4 4.800000
2.064770E+00 3.430665E+00 -1.313964E-01
2.000000     2.800000       3.657484865592E-01  -1.026489637553E+00   1.059732285307E+00  -4.502032679200E-01   5.318553406119E-02
2.800000     3.000000       1.406616069020E-02  -8.638428171020E-02   1.834768930941E-01  -2.800095589242E-01   2.717356162289E-01
3.000000     4.000000       2.323080586501E-03  -3.789913182411E-02   8.068770563459E-02  -6.262106594100E-02   1.688155289978E-02
4.000000     4.800000      -6.278586442383E-04   3.139293221192E-03  -5.886174789735E-03   4.905145658112E-03  -1.532858018160E-03
"""

example_rep4_wrong1 = """
Spline4
3 4.800000
2.064770E+00 3.430665E+00 -1.313964E-01
2.000000     2.800000       3.657484865592E-01  -1.026489637553E+00   1.059732285307E+00  -4.502032679200E-01   5.318553406119E-02
2.800000     3.000000       1.406616069020E-02  -8.638428171020E-02   1.834768930941E-01  -2.800095589242E-01   2.717356162289E-01
3.000000     4.000000       2.323080586501E-03  -3.789913182411E-02   8.068770563459E-02  -6.262106594100E-02   1.688155289978E-02
4.000000     4.800000      -6.278586442383E-04   3.139293221192E-03  -5.886174789735E-03   4.905145658112E-03  -1.532858018160E-03
"""

example_rep4_wrong2 = """
Spline4
5 4.800000
2.064770E+00 3.430665E+00 -1.313964E-01
2.000000     2.800000       3.657484865592E-01  -1.026489637553E+00   1.059732285307E+00  -4.502032679200E-01   5.318553406119E-02
2.800000     3.000000       1.406616069020E-02  -8.638428171020E-02   1.834768930941E-01  -2.800095589242E-01   2.717356162289E-01
3.000000     4.000000       2.323080586501E-03  -3.789913182411E-02   8.068770563459E-02  -6.262106594100E-02   1.688155289978E-02
4.000000     4.800000      -6.278586442383E-04   3.139293221192E-03  -5.886174789735E-03   4.905145658112E-03  -1.532858018160E-03
"""

example_rep4_wrong3 = """
Spline4
4 4.700000
2.064770E+00 3.430665E+00 -1.313964E-01
2.000000     2.800000       3.657484865592E-01  -1.026489637553E+00   1.059732285307E+00  -4.502032679200E-01   5.318553406119E-02
2.800000     3.000000       1.406616069020E-02  -8.638428171020E-02   1.834768930941E-01  -2.800095589242E-01   2.717356162289E-01
3.000000     4.000000       2.323080586501E-03  -3.789913182411E-02   8.068770563459E-02  -6.262106594100E-02   1.688155289978E-02
4.000000     4.800000      -6.278586442383E-04   3.139293221192E-03  -5.886174789735E-03   4.905145658112E-03  -1.532858018160E-03
"""

class TestRepulsivePotenial():
    
    def test_from_file_spline3(self):
        from unittest import mock
        fake_file = io.StringIO(example_rep3)
        with mock.patch("builtins.open", return_value=fake_file, create=True):
            rep = pyerepfit.rep_spline.RepulsivePotenial.from_file('C-C.skf')
            assert rep.name == 'C-C.skf'
            assert rep.cutoff == 4.8

    def test_from_file_spline4(self):
        from unittest import mock
        fake_file = io.StringIO(example_rep4)
        with mock.patch("builtins.open", return_value=fake_file, create=True):
            rep = pyerepfit.rep_spline.RepulsivePotenial.from_file('C-C.skf')
            assert rep.name == 'C-C.skf'
            assert rep.cutoff == 4.8
    
    def test_from_file_spline_wrong(self):
        from unittest import mock
        fake_file = io.StringIO(example_rep4_wrong1)
        with mock.patch("builtins.open", return_value=fake_file, create=True):
            with pytest.raises(ValueError):
                pyerepfit.rep_spline.RepulsivePotenial.from_file('C-C.skf')
        fake_file = io.StringIO(example_rep4_wrong2)
        with mock.patch("builtins.open", return_value=fake_file, create=True):
            with pytest.raises(ValueError):
                pyerepfit.rep_spline.RepulsivePotenial.from_file('C-C.skf')
        fake_file = io.StringIO(example_rep4_wrong3)
        with mock.patch("builtins.open", return_value=fake_file, create=True):
            with pytest.raises(ValueError):
                pyerepfit.rep_spline.RepulsivePotenial.from_file('C-C.skf')
        fake_file = io.StringIO()
        with mock.patch("builtins.open", return_value=fake_file, create=True):
            with pytest.raises(RuntimeError):
                pyerepfit.rep_spline.RepulsivePotenial.from_file('C-C.skf')
    

    def test_calc_exp(self):
        knots = [2.0, 2.8, 3.0, 4.0, 4.8]
        coeffs = [
            [3.657484865592E-01,  -1.026489637553E+00,   1.059732285307E+00,  -4.502032679200E-01,   5.318553406119E-02],
            [1.406616069020E-02,  -8.638428171020E-02,   1.834768930941E-01,  -2.800095589242E-01,   2.717356162289E-01],
            [2.323080586501E-03,  -3.789913182411E-02,   8.068770563459E-02,  -6.262106594100E-02,   1.688155289978E-02],
            [-6.278586442383E-04,   3.139293221192E-03,  -5.886174789735E-03,   4.905145658112E-03,  -1.532858018160E-03]
        ]
        rep = pyerepfit.rep_spline.RepulsivePotenial('C-C', knots, coeffs, calc_exp=True)
        assert rep.expA == pytest.approx(2.064770E+00)
        assert rep.expB == pytest.approx(3.430665E+00)
        assert rep.expC == pytest.approx(-1.313964E-01)
    
    def test_wrong_init(self):
        knots = [2.0, 2.8, 3.0, 4.0, 4.8]
        with pytest.raises(ValueError):
            pyerepfit.rep_spline.RepulsivePotenial('C-C', knots, [[]], calc_exp=True)
        
    
    def test_imcomplete_spline3(self):
        knots = [2.0, 2.8, 3.0, 4.0, 4.8]
        coeffs = [
            [3.657484865592E-01,  -1.026489637553E+00,   1.059732285307E+00,  -4.502032679200E-01],
            [1.406616069020E-02,  -8.638428171020E-02,   1.834768930941E-01,  -2.800095589242E-01,   2.717356162289E-01],
            [2.323080586501E-03,  -3.789913182411E-02,   8.068770563459E-02,  -6.262106594100E-02,   1.688155289978E-02],
            [-6.278586442383E-04,   3.139293221192E-03,  -5.886174789735E-03,   4.905145658112E-03,  -1.532858018160E-03]
        ]
        rep = pyerepfit.rep_spline.RepulsivePotenial('C-C', knots, coeffs, calc_exp=True)
        assert rep.splines[0].r0 == 2.0
        assert rep.splines[0].r1 == 2.8
        assert rep.splines[0].a1 == pytest.approx(-1.026489637553E+00)
        assert rep.splines[0].a3 == pytest.approx(-4.502032679200E-01)
        assert rep.splines[-1].r0 == 4.0
        assert rep.splines[-1].r1 == 4.8
        assert rep.splines[-1].a4 == pytest.approx(-1.532858018160E-03)
        assert rep.splines[-1].a5 == 0.0
    
    def test_init_spline3(self):
        knots = [2.0, 2.8, 3.0, 4.0, 4.8]
        coeffs = [
            [3.630700389745626e-01,  -1.052149737598174e+00,  1.132218109539706e+00,  -5.292659128856522e-01],
            [1.406616069020E-02,  -8.638428171020E-02,   1.834768930941E-01,  -2.800095589242E-01,   2.717356162289E-01],
            [2.323080586501E-03,  -3.789913182411E-02,   8.068770563459E-02,  -6.262106594100E-02,   1.688155289978E-02],
            [-6.278586442383E-04,   3.139293221192E-03,  -5.886174789735E-03,   4.905145658112E-03,  -1.532858018160E-03, 0.002]
        ]
        rep = pyerepfit.rep_spline.RepulsivePotenial('C-C', knots, coeffs, calc_exp=True)
        assert rep.splines[0].r0 == 2.0
        assert rep.splines[0].r1 == 2.8
        assert rep.splines[0].a1 == pytest.approx(-1.052149737598174e+00)
        assert rep.splines[0].a3 == pytest.approx(-5.292659128856522e-01)
        assert rep.splines[-1].r0 == 4.0
        assert rep.splines[-1].r1 == 4.8
        assert rep.splines[-1].a4 == pytest.approx(-1.532858018160E-03)
        assert rep.splines[-1].a5 == 0.002
        assert rep.expA == pytest.approx(2.152199575935475e+00)
        assert rep.expB == pytest.approx(3.588744214431140e+00)
        assert rep.expC == pytest.approx(-1.258017874873710e-01)
    
    def test_wrong_2(self):
        knots = [2.0, 2.8, 3.0, 4.0, 4.8]
        coeffs = [
            [3.657484865592E-01,  -1.026489637553E+00,   1.059732285307E+00],
            [1.406616069020E-02,  -8.638428171020E-02,   1.834768930941E-01,  -2.800095589242E-01,   2.717356162289E-01],
            [2.323080586501E-03,  -3.789913182411E-02,   8.068770563459E-02,  -6.262106594100E-02,   1.688155289978E-02],
            [-6.278586442383E-04,   3.139293221192E-03,  -5.886174789735E-03,   4.905145658112E-03,  -1.532858018160E-03]
        ]
        with pytest.raises(ValueError):
            pyerepfit.rep_spline.RepulsivePotenial('C-C', knots, coeffs, calc_exp=True)
        
    def test_print_spline3(self):
        from unittest import mock
        fake_file = io.StringIO(example_rep3)
        with mock.patch("builtins.open", return_value=fake_file, create=True):
            rep = pyerepfit.rep_spline.RepulsivePotenial.from_file('C-C.skf')
            
            expected = """Spline
56 4.800000
2.152200E+00 3.588744E+00 -1.258018E-01"""
            res_str = str(rep)[:len(expected)]
            assert res_str == expected

    def test_print_spline4(self):
        from unittest import mock
        fake_file = io.StringIO(example_rep4)
        with mock.patch("builtins.open", return_value=fake_file, create=True):
            rep = pyerepfit.rep_spline.RepulsivePotenial.from_file('C-C.skf')
            expected = """Spline4
4 4.800000
2.064770E+00 3.430665E+00 -1.313964E-01"""
            res_str = str(rep)[:len(expected)]
            assert res_str == expected