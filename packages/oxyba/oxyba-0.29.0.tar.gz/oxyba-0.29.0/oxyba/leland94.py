
def leland94(V, s, r, a, t, C=None, d=None, PosEq=False):
    """Leland94 Capital Structure model, Corporate Bond valuation model

    Parameters:
    -----------
    V : float
        Asset Value of the unlevered firm

    s : float
        Volatility s of the asset value V of the unlevered firm

    r : float
        Risk free rate

    a : float
        Bankruptcy cost

    t : float
        Corporate tax rate

    C : float
        (option, default C=None)
        The Coupon in $ per $100.
        - If C>0 then exogenous bancruptcy case, i.e.
            a failure to pay credit event is triggered
            when the firm cannot pay the coupon C
        - If C=None then an endogenous bankcruptcy case,
            i.e. the management can set endogenously an
            'optimal' coupon: min VB, max W=E+D, E>=0
             (see pp.1222).
            The internally computed 'optimal' coupon
             is retured as output argument.

    d : float
        (optional, default d=None)
        Required dividend by investors, or resp the net cash
        payout by the firm.
        - if d=None then 100% retained profits
        - if d>0 then d is the fixed dividend rate proportional
            to the firm's asset value.
        The intermediate result 'X' dependends on 'd'.

    PosEq : bool
        (optional, default PosEq=False)
        If True, then enforce a positive net worth, i.e. obligors demand a
        "protected bond covenant with positive net worth requirement"
        (pp.1233) [dt. Positive Eigenkapitalbasis]


    Returns:
    --------
    D : float
        Value of debt (p.1219)
        [dt. Wert des Fremdkapital]

    E : float
        Value of equity Wert (p.1221)
        [dt. Eigenkapitalwert]

    W : float
        Value of levered company, or Total value of the firm (p.1221)
        [dt. Firmenwert]

            W = V + T - B
            W = D + E

    T : float
        Value of tax benefit (p.1220)
        [dt. Steuervorteil]

    B : float
        Value of bankruptcy costs (p.1220)
        [dt. Insolvenzkosten]

    VB : float
        Level of bankruptcy, i.e. the asset value V at which
        bankruptcy is declared [dt. Restwert bei Insolvenz]
        - if PosEq=False then formula in pp.1222
        - if PosEq=True then the covenant "VB - D = 0" is
            applied to protect creditors (pp.1233)

    PV : float
        PV of $1 if bankruptcy (p.1219)
        [dt. Kapitalwert 1 GE bei Insolvenz]

    Returns (shiny financial metrics):
    ----------------------------------

    lr : float
        Leverage Ratio [dt. Kredithebel]
        i.e. value of debt divided by value of levered firm value

            D / W

    yld : float
        Yield on Debt [dt. Fremdkapitalrendite]
        i.e. coupon in $ divided by value of debt

            C / D

    sprd : float
        Yield Spread in bp [dt. Kreditspread in bp]
        i.e. yield on debt minus riskfree rate converted to bps

            (C/D - r) * 10000

    Returns (intermediate results):
    -------------------------------

    X : float
        Net Cash Payout X will differ depending on the
        dividend policy.
        - If d=None, then 100% retained profits (p.1218)
          [dt. Thesaurierend]
        - If d>0, then fixed dividend per firm value (p.1241)
          [dt. Prozentuale Dividendenausschüttung]
        (intermediate result)

    C : float
        The Coupon in $ per $100.
        - If input argument is C>0 then the input
          argument C is returned as is (exogenous brankruptcy
          case).
        - If input argument C=None, then the internally
          computed 'optimal' coupon the the endogenous
          brankruptcy case is returned (pp.1222)
        (intermediate result)

    A : float
        Annuity value (Wert der Annuitaet), "A=C/r",
        The coupon (in $) divded by the risk-free rate.
        (intermediate result)


    Examples:
    ---------

    PosEq: No (False), Pos Net Worth covenant (True)
    Coupon: Endo (C=None), Exo (C>0)

    Source:
    -------
    Leland, Hayne E. 1994. "Corporate Debt Value, Bond Covenants, and
        Optimal Capital Structure." The Journal of Finance 49 (4): 1213–52.
        https://doi.org/10.1111/j.1540-6261.1994.tb02452.x.

    """

    # subfunction for
    def netcashpayout_by_dividend(r, d, s):
        """net cash payout proportional to the firm's asset value
            for a given required dividend rate (p.1241)
        """
        import math
        s2 = s * s
        tmp = r - d - 0.5 * s2
        return (tmp + math.sqrt(tmp * tmp + 2.0 * s2 * r)) / s2

    def optimal_coupon(V, r, a, t, X):
        """Coupon for the endogenous bankcruptcy case (pp.1222)"""
        m = ((1.0 - t) * X / (r * (1.0 + X)))**X / (1.0 + X)
        h = (1.0 + X + a * (1 - t) * X / t) * m
        return V * ((1.0 + X) * h)**(-1.0 / X)

    def positivenetworth_target(VB, V, a, A, X):
        """protected bond covenant with positive net worth requirement"""
        return VB - A - ((1.0 - a) * VB - A) * (VB / V)**X

    # (1a) Net Cash Payout 'X'
    if d is None:
        # Net cash Payout if 100% retained profits (p.1218)
        X = (2.0 * r) / (s * s)
    else:
        # net cash payout proportional to the firm's asset value
        # for a given required dividend rate (p.1241)
        X = netcashpayout_by_dividend(r, d, s)

    # (1b) Optimal coupon of the endogenous bankruptcy
    #   case (p.1222ff.)
    if C is None:
        C = optimal_coupon(V, r, a, t, X)

    # (1c) Wert der Annuitaet
    A = C / r

    # (2a) Level of bankruptcy VB (pp.1222)
    VB = (1.0 - t) * C / (r + 0.5 * s * s)

    # (2b) protected bond covenant with positive net worth
    # requirement (pp.1233)
    if PosEq:
        from scipy.optimize import fsolve
        VB = fsolve(func=positivenetworth_target, x0=VB, args=(V, a, A, X))
        VB = float(VB)

    # (3a) PV of $1 if bankruptcy (p.1219)
    PV = (VB / V)**X

    # (3b) Value of debt (p.1219)
    D = A + ((1.0 - a) * VB - A) * PV

    # (3c) Value of bankruptcy costs (p.1220)
    B = a * VB * PV

    # (3d) Value of tax benefit (p.1220)
    T = t * A * (1.0 - PV)

    # (3e) Total value of the firm, or Value of levered company (p.1221)
    W = V + T - B

    # (3f) Value of equity (p.1221)
    E = W - D

    # (4a) Leverage Ratio
    lr = D / W

    # (4b) Yield on Debt
    yld = C / D

    # (4c) Yield Spread in bp
    sprd = (yld - r) * 10000.0

    # return results
    return D, E, W, T, B, VB, PV, lr, yld, sprd, X, C, A


def leland94_print(V, s, r, a, t, C, d, PosEq,
                   D, E, W, T, B, VB, PV,
                   lr, yld, sprd, X, C2, A):
    print('Input Parameters:')
    print('{0:>30s}: {1:8.2f}$'.format('(unlevered) Asset Value', V))
    print('{0:>30s}: {1:8.2f} '.format('Volatility', s))
    print('{0:>30s}: {1:8.2f}%'.format('Risk free rate', r * 100))
    print('{0:>30s}: {1:8.2f}%'.format('Bankruptcy cost', a * 100))
    print('{0:>30s}: {1:8.2f}%'.format('Corp. Tax Rate', t * 100))
    if C is not None:
        print('{0:>30s}: {1:8.2f}$'.format('(exogenous) Coupon', C))
    if d is not None:
        print('{0:20s}: {1:8.2f}%'.format('Required Dividend', d * 100))
    print('{0:>30s}: {1:s}'.format('Debt Covenant',
                                   'protected' if PosEq else 'unprotected'))

    print('\nResults:')
    print('{0:>30s}: {1:8.2f}$'.format('Debt Value', D))
    print('{0:>30s}: {1:8.2f}$'.format('Equity Value', E))
    print('{0:>30s}: {1:8.2f}$'.format('(levered) Firm Value', W))
    print('{0:>30s}: {1:8.2f}$'.format('Tax Benefit', T))
    print('{0:>30s}: {1:8.2f}$'.format('Bankruptcy Costs', B))
    print('{0:>30s}: {1:8.2f}$'.format('Bankruptcy Threshold', VB))
    print('{0:>30s}: {1:8.2f}$'.format('PV of $1 if Bankruptcy', PV))

    print('\nMetrics:')
    print('{0:>30s}: {1:8.2f}'.format('Leverage Ratio', lr))
    print('{0:>30s}: {1:8.2f}%'.format('Yield on Debt', yld * 100))
    print('{0:>30s}: {1:8.2f}bps'.format('Yield Spread', sprd))

    print('\nIntermediate Results:')
    print('{0:>30s}: {1:8.2f}$'.format('Net Cash Payout', X))
    if C is None:
        print('{0:>30s}: {1:8.2f}$'.format('(endogenous) Coupon', C2))
    print('{0:>30s}: {1:8.2f}$'.format('Annuity Value', A))
