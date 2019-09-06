# -*- coding: utf-8 -*-

from math import pi
from collections import namedtuple
from copy import copy
from scipy.constants import mu_0
from math import inf

C_RHO = 8.9 * 1e-6  # kg/mm3
C_RHO_CU = 2.14 #2.42  # resistivity constant in 75 C
C_RHO_FE = 7.65 * 1e-6  # kg/mm3
C_MU_0 = 4. * pi * 10 ** -7.  # Vs/Am

INFEASIBLE = -1
C_WIN_MIN = 10.  # minimal width for the windings

# constants
RHO_CU = 0.0216  # 0.0216        # ohm * mm2 / m
RHO_COPPER = 8960.0  # kg/m3
# ---------------------------------------------------------------------


# a dictionary for storing independent parameters:
independent_variables = namedtuple('individual', ['r_c', 'b_c', 'j_in', 'j_ou', 'j_reg', 'h_in', 'm_gap'])

dependent_param = {'core_loss': 0.,
                   'load_loss': 0.,
                   'r_in': 0., 'r_ou': 0., 'r_reg': 0.,
                   't_in': 0., 't_ou': 0., 't_reg': 0.,
                   'h_ou': 0., 'h_reg': 0.,
                   'm_in': 0., 'm_ou': 0., 'm_reg': 0., 'c_mass': 0.,
                   'e_in': 0., 'e_ou': 0., 'e_reg': 0.,
                   'sci': 0., 's': 0., 'ph_pow': 0.,
                   'dc_in': 0., 'dc_ou': 0., 'dc_reg': 0.,
                   'ec_in': 0., 'ec_ou': 0., 'ec_reg': 0.,
                   'turn_voltage': 0.,
                   }


class Dependent_Params:

    def __init__(self):
        self.core_loss = 0.
        self.load_loss = 0.
        self.r_in = 0.
        self.r_ou = 0.
        self.r_reg = 0.
        self.t_in = 0.
        self.t_ou = 0.
        self.t_reg = 0.
        self.h_ou = 0.
        self.h_reg = 0.
        self.m_in = 0.
        self.m_ou = 0.
        self.m_reg = 0.
        self.c_mass = 0.
        self.core_mass = 0.
        self.e_in = 0.
        self.e_ou = 0.
        self.e_reg = 0.
        self.sci = 0.
        self.s = 0.
        self.ph_pow = 0.
        self.dc_in = 0.
        self.dc_ou = 0.
        self.dc_reg = 0.
        self.ec_in = 0.
        self.ec_ou = 0.
        self.ec_reg = 0.
        self.turn_voltage = 0.
        self.wh = 0.  # window height -- for the FEM model
        self.feasible = 0  # feasible is 0


class Parameters:
    """
    Container for the optimized transformer data
    """

    def __init__(self):
        self.power = 40000.  # [kVA]
        self.ph_num = 3.  # phase number
        self.freq = 50.  # [Hz]
        self.ff_in = 0.7  # filling factor in the inner winding
        self.ff_ou = 0.6  # filling factor in the outer winding
        self.ff_reg = 0.6  # filling factor of the regulating winding
        self.ff_c = 0.9  # filling factor in the core
        self.u_in_line = 20.  # line voltage in the inner winding
        self.u_in = 20.  # phase voltage in the inner terminal [kV]
        self.in_ins_ax = 3.5
        self.in_ins_rad = 0.5
        self.in_ins_s = 0.1  # ctx
        self.ou_ins_ax = 4.0
        self.ou_ins_rad = 0.4
        self.ou_ins_s = 0.3  # ctx
        self.con_fact_in = 1.  # connection factor in the case of the inner winding --> 1 <-- for this case
        self.con_fact_ou = 1.  # connection factor in the case of the outer winding --> 1 <-- for this case
        self.u_out = 120. / 3. ** 0.5  # phase voltage in the outer terminal [kV]
        self.u_out_line = 120.
        self.drop = 0.115  # short circuit impedance
        self.drop_tol = 0.03  # 3 [%]
        self.ei = 170.  # end insulation distance in [mm]
        self.gap = 38.  # minimum distance for the main insulation [mm]
        self.gap_core = 20.  # distance between the core and the inner winding [mm]
        self.phase_distance = 40.  # distance between the different phases in [mm]
        self.alpha = 0.95  # ratio of the outer and the inner winding
        self.beta = 0.89  # ration of the regulating and the inner winding
        self.f_bf = 1.2  # core building factor
        self.bin_reg = False # built in regulation
        # regulation
        self.reg_range = 0.05  # regulation range/ half of the nominal, because of the diverter switch

        # costs
        self.ll_c = 3000.  # load loss cost [eur/kw]
        self.nll_c = 5000.  # no load loss cost [eur/kw]
        self.win_c = 10.  # insulated wire cost in the inner winding [eur/kg]
        self.wout_c = 8.  # insulated wire cost in the outer winding [eur/kg]
        self.wreg_c = 7.
        self.cc = 3.  # electrical steel cost in [eur/kg]


def calc_dependent_variables(ind, para):
    """
    Calculates the non-magnetic/electrical parameters of the model.

    :param ind: the independent parameters of the model, which defines and 'individual' solution
    :param param: the required parameters or the different limits from the standards, technology ...
    :return: a dictionary with the dependent key-design variables
    """
    dep = Dependent_Params()

    # calculating derived parameters

    # 1/ phase power
    dep.ph_pow = para.power / para.ph_num

    # 2/ turn voltage
    dep.turn_voltage = turn_voltage(ind.b_c, ind.r_c, para.ff_c, para.freq)

    # 3/ winding thickness - inner
    dep.t_in = calc_inner_width(dep.ph_pow, ind.h_in, para.ff_in, ind.j_in, dep.turn_voltage)

    # check the 'strength' of the coil if it's smaller than a technological limit, the solution is infeasible
    if dep.t_in < C_WIN_MIN:
        dep.feasible = INFEASIBLE
        return copy(dep)

    # 4/ winding thickness -- outer winding
    dep.h_ou = ind.h_in * para.alpha
    dep.t_ou = calc_inner_width(dep.ph_pow, dep.h_ou, para.ff_ou, ind.j_ou, dep.turn_voltage)

    # check the strength of the coil
    if dep.t_ou < C_WIN_MIN:
        dep.feasible = INFEASIBLE
        return copy(dep)

    # 5/ regulating winding thickness
    dep.h_reg = ind.h_in * para.beta

    if para.reg_range > 1e-6 and para.bin_reg is False:
        dep.t_reg = calc_t_reg(para.reg_range, ind.h_in, para.beta,
                               dep.ph_pow, ind.j_reg, para.ff_reg, dep.turn_voltage)
    else:
        if para.bin_reg is True:
            dep.t_reg = 0.

    # 6/ innder winding radius
    dep.r_in = inner_winding_radius(ind.r_c, para.gap_core, dep.t_in)

    # 7/ outer winding radius
    dep.r_ou = outer_winding_radius(dep.r_in, dep.t_in, ind.m_gap, dep.t_ou)

    # 8/ regulating winding radius
    if para.reg_range > 1e-6 and para.bin_reg is False:
        dep.r_reg = rad_reg_winding_outer(dep.r_ou, dep.t_ou, para.gap, dep.t_reg)
    else:
        if para.bin_reg is True:
            dep.r_reg = 0.

        if para.bin_reg is True:
            dep.t_reg = dep.t_ou
            dep.h_ou = dep.h_ou*1.-para.reg_range


    # 9/ calculating the window width wothout the regulating winding
    if para.reg_range > 1e-6:
        gap_r = ind.m_gap
    else:
        gap_r = 0.

    dep.s = window_width(para.gap_core, dep.t_in, dep.t_ou, ind.m_gap, dep.t_reg, gap_r,
                         para.phase_distance)  # TODO: this variable is missing somehow from the previous optimization model

    # 10/ calculating winding masses and losses
    dep.m_in = winding_mass(para.ph_num, dep.r_in, dep.t_in, ind.h_in, para.ff_in)
    dep.m_ou = winding_mass(para.ph_num, dep.r_ou, dep.t_ou, dep.h_ou, para.ff_ou)

    if para.reg_range > 1e-6:
        dep.m_reg = winding_mass(para.ph_num, dep.r_reg, dep.t_reg, dep.h_reg, para.ff_reg)
    else:
        dep.m_reg = 0.
    # 11/ calculating the core mass
    dep.c_mass = core_mass(ind.r_c, para.ff_c, ind.h_in, para.ei, dep.s, para.phase_distance / 2.)
    dep.core_loss = core_loss_unit(ind.b_c, dep.c_mass, para.f_bf)

    # 12/ window height
    dep.wh = ind.h_in + para.ei

    return copy(dep)


def fem_analytics(ind, para, dep, w_in, w_ou, bmax):
    """

    :param ind:
    :param para:
    :param dep:
    :param w_in:
    :param w_ou:
    :return:
    """
    # dc losses
    # trick - calculates the 'linear component' of the weight for a more precise dc loss calculation
    dep.e_in = winding_mass(para.ph_num, dep.t_in, dep.t_in, ind.h_in, para.ff_in)
    dep.e_ou = winding_mass(para.ph_num, dep.t_ou, dep.t_ou, dep.h_ou, para.ff_ou)
    dep.e_reg = winding_mass(para.ph_num, dep.t_reg, dep.t_reg, dep.h_reg, para.ff_reg)

    dep.dc_in = winding_dc_loss(dep.m_in, ind.j_in) + winding_dc_loss(dep.e_in, ind.j_in)
    dep.dc_ou = winding_dc_loss(dep.m_ou, ind.j_ou) + winding_dc_loss(dep.e_ou, ind.j_ou)

    # the ac losses calculated from maximal value of the leakage flux and the value of the bmax in the airgap
    v_in = copper_volume(para.ff_in, dep.r_in, dep.t_in, ind.h_in)
    v_ou = copper_volume(para.ff_ou, dep.r_ou, dep.t_ou, dep.h_ou)

    dep.ec_in = p_eddy(v_in, bmax, para.freq, w_in, para.ph_num)*1e-3
    dep.ec_ou = p_eddy(v_ou, bmax, para.freq, w_ou, para.ph_num)*1e-3

    dep.load_loss = dep.dc_in + dep.dc_ou + dep.ec_in + dep.ec_ou

    return


def fem_analytics_improved_model(ind, para, dep, w_in, bmax_in, w_ou, bmax_ou, w_ou_top, bmax_ou_top):
    """

    :param ind:
    :param para:
    :param dep:
    :param w_in:
    :param w_ou:
    :return:
    """
    # dc losses
    # trick - calculates the 'linear component' of the weight for a more precise dc loss calculation
    dep.e_in = winding_mass(para.ph_num, dep.t_in, dep.t_in, ind.h_in, para.ff_in)
    dep.e_ou = winding_mass(para.ph_num, dep.t_ou, dep.t_ou, dep.h_ou, para.ff_ou)
    dep.e_reg = winding_mass(para.ph_num, dep.t_reg, dep.t_reg, dep.h_reg, para.ff_reg)

    dep.dc_in = winding_dc_loss(dep.m_in, ind.j_in) + winding_dc_loss(dep.e_in, ind.j_in)
    dep.dc_ou = winding_dc_loss(dep.m_ou, ind.j_ou) + winding_dc_loss(dep.e_ou, ind.j_ou)

    # the ac losses calculated from maximal value of the leakage flux and the value of the bmax in the airgap
    v_in = copper_volume(para.ff_in, dep.r_in, dep.t_in, ind.h_in)
    v_ou = copper_volume(para.ff_ou, dep.r_ou, dep.t_ou, dep.h_ou)

    dep.ec_in = p_eddy(v_in, bmax_in, para.freq, w_in, para.ph_num)*1e-3
    dep.ec_ou = p_eddy(v_ou, bmax_ou, para.freq, w_ou, para.ph_num)*1e-3
    dep.ec_ou += p_eddy(v_ou, bmax_ou_top, para.freq, w_ou_top, para.ph_num)*1e-3

    dep.load_loss = dep.dc_in + dep.dc_ou + dep.ec_in + dep.ec_ou

    return


def b_gap(n, i, h_w):
    """
    peak value of the induction in the main gap
    @param winding: is the result of the optimization
    This value is calculated from the constants of this calculation
    """
    return (2. ** 0.5) * mu_0 * n * i / (h_w * 1e-3)


def p_eddy(vol, b_gp, omega, w, ph_n):
    """
    mean value of the eddy loss
    """
    print('b_gp',b_gp)
    return (omega ** 2.) * ((w * 1e-3) ** 2.) / 24. / (RHO_CU * 1e-8) * vol * (b_gp ** 2.) / 3.


def copper_volume(ff, rm, t, h):
    """
    Calculates the copper volume in [m^3]

    :param ff: filling factor [0-1]
    :param rm: mean radius [mm]
    :param t: winding thickness [mm]
    :param h: winding height [mm]
    :return:
    """

    return ff * 2. * rm * pi * t * h * 1e-9


def calc_analytically(ind, para, dep):
    """
    analytically calculates every function for the dc losses

    :param ind: individual -- list of teh independent parameters --
    :param para: required parameters
    :param dep: dependent parameters
    :return:
    """

    # short circuit impedance
    dep.sci = short_circuit_impedance(para.power, para.ph_num,
                                      para.freq, para.alpha, dep.turn_voltage,
                                      ind.h_in, dep.s, dep.r_in, dep.t_in, dep.r_ou,
                                      dep.t_ou, ind.m_gap)

    # dc losses
    # trick - calculates the 'linear component' of the weight for a more precise dc loss calculation
    dep.e_in = winding_mass(para.ph_num, dep.t_in, dep.t_in, ind.h_in, para.ff_in)
    dep.e_ou = winding_mass(para.ph_num, dep.t_ou, dep.t_ou, dep.h_ou, para.ff_ou)
    dep.e_reg = winding_mass(para.ph_num, dep.t_reg, dep.t_reg, dep.h_reg, para.ff_reg)

    dep.dc_in = winding_dc_loss(dep.m_in, ind.j_in) + winding_dc_loss(dep.e_in, ind.j_in)
    dep.dc_ou = winding_dc_loss(dep.m_ou, ind.j_ou) + winding_dc_loss(dep.e_ou, ind.j_ou)

    # the losses in the regulating winding is assumed zero in this case,
    # because of the assumption that the transformer contains an inverter switch and the optimization is made for the
    # nominal tapping position, when the regulating winding is inactive

    dep.ec_in = winding_dc_loss(dep.m_in, ind.j_in) * dep.sci + winding_dc_loss(dep.e_in, ind.j_in) * dep.sci
    dep.ec_ou = winding_dc_loss(dep.m_ou, ind.j_ou) * dep.sci + winding_dc_loss(dep.e_ou, ind.j_ou) * dep.sci

    dep.load_loss = dep.dc_in + dep.dc_ou + dep.ec_in / 2. + dep.ec_ou / 2.

    return


def eval_objective(param, dep, sci_tol, sci, calc_sci):
    """
    Gives back the calculated TOC for the defined transformer.
    TOC - sum of the cost of the core and the windings and the capitalized cost of the windings

    This function calculates the losses and the short circuit impedance by the usage of a finite element code.

    :return: the value of the objective function
    """

    # toc = inf
    #
    # if calc_sci <= sci * (1 + sci_tol) and calc_sci >= sci * (1 - sci_tol):
    #
    #     toc = capitalized_cost(dep.c_mass, param.cc,
    #                            dep.m_in, param.win_c,
    #                            dep.m_ou, param.wout_c,
    #                            dep.load_loss, param.ll_c,
    #                            dep.core_loss, param.nll_c)

    toc = capitalized_cost(dep.c_mass, param.cc,
                           dep.m_in, param.win_c,
                           dep.m_ou, param.wout_c,
                           dep.load_loss, param.ll_c,
                           dep.core_loss, param.nll_c)

    # search with penalty
    #if sci_tol<1:
    #    if calc_sci <= sci * (1 + sci_tol) or calc_sci >= sci * (1 - sci_tol):
    #        toc += abs(sci - calc_sci)*1e6

    # exclude the wrong solutions
    if calc_sci <= sci * (1 + sci_tol) or calc_sci >= sci * (1 - sci_tol):
            toc += -1 #abs(sci - calc_sci)*1e6

    return toc


def objective_function(variables, *param):
    """
    The independent variables of the optimization model:
    ----------------------------------
        r_c   - core radius from 200 [mm] to 600 [mm] step 5 [mm]
        b_c   - flux density in the column from 1.3 [T] to 1.73 [T] step 0.01 [T]
        j_in  - current density in the inner winding from 0.5 [A/mm2] to 4 [A/mm^2] step 0.01 [A/mm2]
        j_out - current density in the outer winding from 0.5 [A/mm2] to 4 [A/mm^2] step 0.01 [A/mm2]
        h_in  - inner winding height in [mm] from 500 [mm] to 3500 [mm] step 10 mm
        main gap - from gap to 2.5xgap in [mm] step mm
    """

    # independent variables
    r_c, b_c, j_in, j_out, h_in, m_gap = variables

    para = Parameters()

    # calculating derived parameters
    ph_pow = para.power / para.ph_num

    # turn voltage
    tv = turn_voltage(b_c, r_c, para.ff_c, para.freq)

    # Winding Geometry ---------
    # winding thickness - inner
    t_in = calc_inner_width(ph_pow, h_in, para.ff_in, j_in, tv)

    # check the strength of the coil
    if t_in < C_WIN_MIN:
        return INFEASIBLE

    # winding thickness - outer
    h_out = h_in * para.alpha
    t_out = calc_inner_width(ph_pow, h_out, para.ff_ou, j_out, tv)

    # check the strength of the coil
    if t_out < C_WIN_MIN:
        return INFEASIBLE

    # radius calculation
    r_in = inner_winding_radius(r_c, para.gap_core, t_in)
    r_out = outer_winding_radius(r_in, t_in, m_gap, t_out)

    s = window_width(para.gap_core, t_in, t_out, m_gap, 0., 0., 0)  # without regulating winding

    # check the short circuit impedance
    z = short_circuit_impedance(para.power, para.ph_num, para.freq, para.alpha, tv, h_in, s,
                                r_in, t_in, r_out, t_out, m_gap)

    if (z < (1. - para.drop_tol) * para.drop) or (z > (1. + para.drop_tol) * para.drop):
        return INFEASIBLE

    # calculating winding masses and losses
    wm_in = winding_mass(para.ph_num, r_in, t_in, h_in, para.ff_in)
    wm_out = winding_mass(para.ph_num, r_out, t_out, h_out, para.ff_ou)

    w_in_loss = winding_dc_loss(wm_in, j_in) * (
            1. + opt_win_eddy_loss(t_in * homogenous_insulation_ff(para.ff_in), t_in))
    w_out_loss = winding_dc_loss(wm_out, j_out) * (
            1. + opt_win_eddy_loss(t_out * homogenous_insulation_ff(para.ff_ou), t_out))

    ll = w_in_loss + w_out_loss

    # calculating core losses and masses
    c_mass = core_mass(r_c, para.ff_c, h_in, para.ei, s, para.phase_distance)
    nll = core_loss_unit(b_c, c_mass, para.f_bf)

    return capitalized_cost(c_mass, para.cc,
                            wm_in, para.win_c,
                            wm_out, para.wout_c,
                            ll, para.ll_c,
                            nll, para.nll_c)


def test_object():
    p = Parameters()

    r_c = 320.
    b_c = 1.6
    j_in = 2.
    j_out = 2.
    h_in = 1150.
    m_gap = 40.

    var = r_c, b_c, j_in, j_out, h_in, m_gap

    assert round(objective_function(var, p), 0) == 574212.


def phase_current(sb, ub, con_fact):
    """

    :param sb: nominal power [MVA]
    :param ub: line voltage
    :param con_fact: connection factor --- 1 for delta --- sqrt(3) for star connection --- sqrt(2)/2. for zig-zag
    :return:
    """
    return sb * 1e3 / ub / 3. ** 0.5 / con_fact


def winding_mass(m, r_m, t, h, ff):
    """
    Winding mass in m phase.

    m [#] is the number of phases
    r_m in [mm] is the mean radius of the winding.
    t in [mm] is the thickness of the winding.
    h in [mm] is the height of the winding.
    ff is the copper filling factor

    The typical values of the filling factors are. 40 <ff << 70
    """
    return m * r_m * 2. * pi * t * h * ff * C_RHO


def winding_dc_loss(mass, j):
    """
    This function is estimate the loss of the winding from the geometry of
    the winding and the copper filling factor.

    -> j in [A/mm2] is the current density.
    """
    dc_loss = C_RHO_CU * mass * j ** 2.

    return dc_loss * 1e-3


def homogenous_insulation_ff(ff):
    """
    If we assumes that the horizontal ff = vertical ff, the
    function give back the insulation horizontal filling factor
    """

    return (1. - ff) ** 0.5


def opt_win_eddy_loss(v_k, k):
    """
    This function approximates the optimal eddy loss in the assumed optimal winding system.
    From the insulation, and winding width parameters.

    Source:
    Elektrotechnika, Újházy Géza, 1969/10-11,
    Erőátviteli Transzformátorok tekercsrendszerének a méretezése
    """

    return v_k / (3. * v_k + 2. * k)


def sum_winding_loss(dc_loss, eddy_loss):
    """
    This function give back the sum of the estimated eddy and dc loss in the
    winding.
    """
    return dc_loss * (1. + eddy_loss)


def core_loss_unit(ind, m_c, f_bf):
    """
    This function calculates the core loss in kW/ at the given induction
    based on mediumloss

    The calculation based on a posynomial formula:

    P_nll = M_c*f_bf*[a + c*B + d*B^b + e*B^3 + f*B^4 + g*B^4] * 10^-3

    x P_nll is the no-load loss
    x M_c is the core mass in [kg]
    x f_bf is the building factor
    x B is the induction in the column (ind)

    Fitted values (medium loss):

    """

    # most eleg ennyi
    a = 1. * 0.0417580576
    b = 3.1
    c = 1.73506161432 * 0.0417580576
    d = 1.50521940274 * 0.0417580576
    e = 0.87054946894 * 0.0417580576
    f = 0.377614241733 * 0.0417580576
    g = 0.13103679517 * 0.0417580576

    return m_c * f_bf * (a + c * ind + d * ind ** b + e * ind ** 3. + f * ind ** 4. + g * ind ** 5.) * 10 ** (-3.)


def core_mass(r_c, ff_c, h, ei, s, m):
    """
    This function estimates the mass of different types of transformer cores

    mass = m_column + m_yoke + m_corner + m_sl

    x m_column - mass of columns in  [kg]
    x m_yoke   - mass of yokes in    [kg]
    x m_corner - mass of corners in  [kg]
    x m_sl     - mass of side-leg in [kg]

    a = r_c**2.*pi*ff_c*rho_fe

    m_corner = a*(c*r_c*sigma**2.*gamma)
    m_column = a*o*(h+ei)
    m_yoke = a*(s*sn+m*mn)
    m_sl = a*p*h*(h+ei)

    x h    - inner winding height in [mm]
    x ei   - end insulation bottom in[mm]
    x s    - window width in [mm]
    x sn   - number of s in a transformer shape [#]
    x m    - phase insulation [mm]
    x mn   - number of main insulation in the core [#]

    3 phase 3 legged core:
    """
    o = 3.  # number of columns
    p = 0.  # number of side-legs
    c = 6.  # number of corners corner
    sn = 8.  # number of s
    mn = 4.  # number of main insulation
    sigma = 1.  # leg/column & yoke/column
    gamma = 1.025

    a = r_c ** 2. * pi * ff_c * C_RHO_FE

    m_corner = a * (c * r_c * sigma ** 2. * gamma + c * r_c * sigma)
    m_column = a * o * (h + ei)
    m_yoke = a * (s * sn + m * mn)
    m_sl = a * p * (h + ei) * sigma ** 2.

    print('column', m_column)
    print('yoke', m_yoke)
    print('corner', m_corner)

    return m_column + m_yoke + m_corner + m_sl


def window_width(g_core, t_in, t_out, g, t_r, g_r, p_d):
    """
    is the calculated winding width if there

    x g_core - is the distance between the core and the inner winding in [mm]
    x t_in   - is the thickness of the inner winding  in [mm]
    x t_out  - is the thickness of the outer winding  in [mm]
    x g is   - is the main gap in [mm]
    x t_r    - is the width of the regulating winding in [mm]
    x g_r    - is the distance between the outer winding and the regulating winding [mm]
    x p_d    - phase distance betwen the different phases
    """

    return g_core + t_in + t_out + g + t_r + g_r + p_d


def turn_voltage(ind, r_c, ff_c, freq):
    """
    This function calculates the turn voltage from the core area, the frequency and the flux density in the core.
    [V]
    """
    area = r_c ** 2. * pi * ff_c

    return ind * area * 4.44 * 1e-6 * freq


def short_circuit_impedance(b_pow, p_num, freq, alpha, turn_v, h, s,
                            r_in, t_in, r_ou, t_ou, g):
    """
    Short-circuit impedance calculation

    TODO: should be improved as in the other paper

    b_pow - built-in power  [kVA]
    p_num - phase number [#]
    freq  - frequency  [Hz]
    alpha - ratio of the outer and inner winding
    ff_c  - core filling factor
    turn_v- turn voltage [V]
    h     - height of the inner window [mm]
    s     - width of working window [mm]
    g     . main insulation width [mm]
    """

    p_pow = b_pow / p_num
    imp_con = 4. * pi ** 2. * C_MU_0 * freq * p_pow / turn_v ** 2. / (h * (1 + alpha) / 2. + 0.32 * s)
    a = r_in * t_in / 3.
    b = r_ou * t_ou / 3.
    c = (r_in + t_in / 2. + g / 2.) * g

    return imp_con * (a + b + c) * 100. # to get the values in the appropriate units


def capitalized_cost(c_mass, c_material_price,
                     w_mass_in, w_c_in,
                     w_mass_ou, w_c_out,
                     ll, ll_cost,
                     nll, nll_cost):
    """
    Objective function
    Simple capitalized cost calculation, only the active part with filling factors
    """

    return c_mass * c_material_price + w_mass_in * w_c_in + w_mass_ou * w_c_out + ll * ll_cost + nll * nll_cost


def inner_winding_radius(r_c, g_core, t_in):
    """
    Calculates the inner winding radius in the following cases:

    Core || Inner Main || Outer Main
    Core || Inner Main || Outer Main || Regulating
    Core || Inner Main || Regulating || Outer Main
    """
    return r_c + g_core + t_in / 2.


def outer_winding_radius(r_in, t_in, g, t_out):
    """
    Calculates the inner winding radius in the following cases:

    Core || Inner Main || Outer Main
    Core || Inner Main || Outer Main || Regulating
    """
    return r_in + t_in / 2. + g + t_out / 2.


def winding_power(width, height, ff_w, j_, u_t):
    """
    Calculates the power of the winding

    x width - winding width in [mm]
    x height- winding height in [mm]
    x ff_w  - filling factor [-]
    """

    return width * height * u_t * ff_w * j_ * 1e-3  # kVA


def calc_inner_width(s_p, h_, ff_w, j_, u_t):
    """
    Calculates the inner width from the height and the power

    s_p   - phase power in kVA
    h_    - winding height
    ff_w  - winding filling factor
    j_    - current density [A/mm2]
    """
    return s_p / h_ / ff_w / j_ / u_t * 1e3  # mm


def calculate_turn_num(win_voltage, turn_voltage):
    """
    win_voltage in [kV]
    turn_voltage in [V]
    """
    return round(win_voltage / turn_voltage * 1e3, 1)


def calc_t_reg(reg_range, h_in, hfact, P_nom, j_reg, ff_reg, u_t):
    """
    reg_range         - is the (regulating winding capacity)/(main, regulated winding capacity)
    h_in              - is the height of the inner winding (reference)
    reg_height_factor - is the ratio of the regulating and the reference winding
    reg_w_min         - is the minimal width of the regulating winding
    P_nom             - is the phase power of the main winding in kVA
    j_reg             - is the current density in the regulating winding
    ff_reg            - is the filling factor of the regulating winding
    u_t               - is the turn voltage
    """

    t_reg = P_nom * reg_range / (h_in * hfact) / ff_reg / j_reg / u_t * 1e3;

    if (t_reg < C_WIN_MIN):
        t_reg = C_WIN_MIN

    return t_reg


def rad_reg_winding_outer(r_ou, t_ou, g_min, t_reg):
    """
    r_ou  - outer winding diameter
    t_ou  - outer winding thickness
    g_min - minimum main insulation thickness
    t_reg - regulating winding thickness

    :return:
    """

    return r_ou + t_ou / 2. + g_min + t_reg / 2.
