import unittest
# import numpy.testing as npt
# import numpy as np
import oxyba as ox

# SOURCE
# http://www.ulb.ac.be/cours/solvay/farber/Ofin/LELAND94%20Revised%202003%20Class%20presentation.XLS

# test cases


class Test_Leland94(unittest.TestCase):

    def test1(self):
        # Exo Coupon/Bankruptcy, Unprotected Debt
        V = 100  # asset value of unlevered firm
        s = 0.20  # volatility of unlevered firm
        r = 0.06  # riskfree rate
        a = 0.50  # bankruptcy costs
        t = 0.35  # corp tax rate
        C = 5.00  # exogenous bankruptcy case
        d = None  # 100% retained profits
        PosEq = False  # unprotected

        # compute
        D, E, W, T, B, VB, PV, lr, yld, sprd, X, C, A = ox.leland94(
            V, s, r, a, t, C, d, PosEq)

        # check
        self.assertAlmostEqual(D, 79.11, places=2)
        self.assertAlmostEqual(E, 46.74, places=2)
        self.assertAlmostEqual(W, 125.85, places=2)
        self.assertAlmostEqual(T, 27.21, places=2)
        self.assertAlmostEqual(B, 1.36, places=2)
        self.assertAlmostEqual(VB, 40.625, places=2)
        self.assertAlmostEqual(PV, 0.07, places=2)
        self.assertAlmostEqual(lr, 0.63, places=2)
        self.assertAlmostEqual(yld, 0.0632, places=4)
        self.assertAlmostEqual(sprd, 32, places=0)
        self.assertAlmostEqual(X, 3.00, places=0)

    def test2(self):
        # Endo Coupon/Bankruptcy, Unprotected Debt
        V = 100  # asset value of unlevered firm
        s = 0.20  # volatility of unlevered firm
        r = 0.06  # riskfree rate
        a = 0.50  # bankruptcy costs
        t = 0.35  # corp tax rate
        C = None  # endogenous bankruptcy case
        d = None  # 100% retained profits
        PosEq = False  # unprotected

        # compute
        D, E, W, T, B, VB, PV, lr, yld, sprd, X, C, A = ox.leland94(
            V, s, r, a, t, C, d, PosEq)

        # check
        self.assertAlmostEqual(D, 96.27, places=2)
        self.assertAlmostEqual(E, 32.17, places=2)
        self.assertAlmostEqual(W, 128.44, places=2)
        self.assertAlmostEqual(T, 32.33, places=2)
        self.assertAlmostEqual(B, 3.89, places=2)
        self.assertAlmostEqual(VB, 52.82, places=2)
        self.assertAlmostEqual(PV, 0.15, places=2)
        self.assertAlmostEqual(lr, 0.75, places=2)
        self.assertAlmostEqual(yld, 0.0675, places=4)
        self.assertAlmostEqual(sprd, 75, places=0)

    def test3(self):
        # Exo Coupon/Bankruptcy, Protected Debt
        V = 100  # asset value of unlevered firm
        s = 0.20  # volatility of unlevered firm
        r = 0.06  # riskfree rate
        a = 0.50  # bankruptcy costs
        t = 0.35  # corp tax rate
        C = 5.00  # exogenous bankruptcy case
        d = None  # 100% retained profits
        PosEq = True  # Protected

        # compute
        D, E, W, T, B, VB, PV, lr, yld, sprd, X, C, A = ox.leland94(
            V, s, r, a, t, C, d, PosEq)

        # check
        self.assertAlmostEqual(D, 67.88, places=2)
        self.assertAlmostEqual(E, 41.54, places=2)
        self.assertAlmostEqual(W, 109.43, places=2)
        self.assertAlmostEqual(T, 20.04, places=2)
        self.assertAlmostEqual(B, 10.62, places=2)
        self.assertAlmostEqual(VB, 67.88, places=2)
        self.assertAlmostEqual(PV, 0.31, places=2)
        self.assertAlmostEqual(lr, 0.62, places=2)
        self.assertAlmostEqual(yld, 0.0737, places=4)
        self.assertAlmostEqual(sprd, 137, places=0)


# run
if __name__ == '__main__':
    unittest.main()
