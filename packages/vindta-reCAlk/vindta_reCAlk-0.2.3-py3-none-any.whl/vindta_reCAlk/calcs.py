#!/usr/local/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import
from io import open
import warnings as _warnings
import pandas as pd
import os
import numpy as np
from datetime import datetime
_warnings.filterwarnings("ignore", category=RuntimeWarning)

FileNotFoundError = IOError if "FileNotFoundError" not in locals() else FileNotFoundError


def main():
    pass


def dbs_has_min_columns(column_name_list):
    """
    Function determines if DBS headers passed contain the required
    columns.
    """

    compulsory_header_cols = set([
        'runtype',
        'station',
        'cast',
        'niskin',
        'depth',
        'bottle',
        'date',
        'time',
        'temp',
        'salt',
        'po4',
        'sio4',
        'acidconcL',
        'pipVol',
        'aciddens',
        'pKchoice',
        'CRMCT',
        'CRMAT',
        'calcID',
        'DIC',
    ])

    missing_header_cols = compulsory_header_cols - set(column_name_list)

    if any(missing_header_cols):
        raise UserWarning(
            "The header is missing compulsory header columns: " +
            str(missing_header_cols).replace('{', '').replace('}', ''))
    else:
        return True


def dbs_to_excel(dbs_filename, datfiles_dir, xls_filename,
                 date_fmt='%m/%d/%y %H:%M',
                 acidconcL=0.1, aciddens=1.02266027,
                 pipVol=97.846, pKchoice=13, po4=0.5, sio4=2.5,
                 factorCT=1.0, pK1=5.0, pK_constant=1.0, verbose=False,
                 header=('runtype', 'bottle', 'station', 'cast', 'niskin',
                         'depth', 'temp', 'salt', 'counts', 'runtime', 'DIC',
                         'factorCT', 'blank', 'RecalcCT', 'lastCRMCT', 'CRMCT',
                         'lastCRMAT', 'CRMAT', 'batch', 'alk', 'RecalcAT', 'rms',
                         'calcID', 'acidconcL', 'aciddens', 'pipVol', 'comment',
                         'lat', 'lon', 'date', 'time', 'CellID')):

    import inspect
    from datetime import datetime as dt

    # get the keyword arguments that have a default value
    # keyword arguements are identified by the number of values with defaults
    argspec = inspect.getargspec(dbs_to_excel)
    kwargs = argspec.args[-len(argspec.defaults):]
    kwargs.remove('header')
    kwargs.remove('date_fmt')

    data = []
    with open(dbs_filename, encoding='latin9') as dbs:
        for line in dbs:
            if line.startswith('bottle'):
                data += line.strip().split('\t'),

    df = pd.DataFrame(data, columns=header)

    dbs_has_min_columns(np.r_[df.columns.values, kwargs])

    df['analysis_date'] = df.date + ' ' + df.time
    try:
        df['analysis_date'] = df.analysis_date.apply(lambda d: dt.strptime(d, date_fmt))
    except ValueError as e:
        for i in df.index:
            try:
                dt.strptime(df.loc[i, 'analysis_date'], date_fmt)
            except ValueError as e:
                raise ValueError('Invalid date found at {} ({})'.format(df.loc[i, 'bottle'], str(e)))

    # reorder analysis_date to the end of the DataFrame and find only bottles
    df = df[df.columns.tolist()[1:] + df.columns[0:1].tolist()]
    df = df[df.runtype == 'bottle']
    df.loc[:, 'bottle'] = df.bottle.str.strip()

    # create filenames for dat
    fname = datfiles_dir + '/{station:s}-{cast:s}  {niskin:s}  ({depth:s}){bottle}.dat'
    df['datfilename'] = [fname.format(**df.loc[i].to_dict()) for i in df.index]

    # assign the keyword arguments to the dataframe.
    # The wrong keywords have been removed earlier (header)
    for key in kwargs:
        df.loc[:, key] = locals()[key]

    if verbose:
        print('INITIAL CALCULATION\n' + '-' * 60)
    for i in df.index:  # every line
        if verbose:
            print(pretty_path(df.datfilename[i]), end='')

        err = ''
        try:
            vols, emfs, tempC, msg = read_dat(df.datfilename[i])
            err += msg
            conc, ALK, pK1, pKstr, resid = recalcAlk_leastsq(
                try_float(df.salt[i]),
                tempC,
                try_float(df.po4[i]),
                try_float(df.sio4[i]),
                try_float(df.pipVol[i]),
                try_float(df.acidconcL[i]),
                try_float(df.aciddens[i]),
                vols, emfs,
                int(df.pKchoice[i]))

            # Assign new values to the matrix
            df.loc[i, 'RecalcAT'] = np.nan
            var_names = ['acidconcL', 'RecalcAT', 'rms', 'pK1', 'pK_constant']
            df.loc[i, var_names] = conc, ALK, np.mean(resid), pK1, pKstr

        except ValueError as e:
            err += ": Something wrong with dat file ({})".format(e)
        except FileNotFoundError as e:
            err += ": File does not exist"
        except IndexError as e:
            err += ": Error in recalculation ({})".format(e)

        if verbose:
            print(err)
        df.loc[i, 'comment'] = err

    df.loc[:, 'RecalcCT'] = df.DIC.apply(try_float) * df.factorCT.apply(try_float)

    if xls_filename:
        write_dbs_to_excel(df, xls_filename, dbs_filename)

    return df


def write_dbs_to_excel(data, xls_filename, dbs_filename="[not given]"):

    time = datetime.today().strftime("%d %B %Y at %H:%M")
    readme = [
        "This file was created from the dbs file {} on {}".format(dbs_filename, time),
        "An initial TA recalculation was performed with default acid and nutrient concentrations."
    ]
    info = pd.DataFrame(readme, columns=['README'])

    writer = pd.ExcelWriter(xls_filename)
    info.to_excel(writer, 'README', index=False)
    data.to_excel(writer, 'initial_calc', index=False)
    writer.save()


def recalculate_CO2_from_excel(xls_filename):

    print("""
        Note that this function should only be used once you have run the
        VINDTA_recALK.dbs_to_excel. You need to fill in the in-situ
        temperature, salinity, and nutrient data.
        \n""".replace('  ', '')[1:])

    df = pd.read_excel(xls_filename, 'initial_calc')
    df = df.sort_values('analysis_date')

    df = calc_crm_acidconc(df)
    df.loc[:, 'factorCT'] = df.CRMCT / df.DIC
    df = get_batch_indicies(df)

    for b in df.analysis_batch.unique():
        batch = df.analysis_batch == b
        crm = df.bottle.str.upper().str.startswith('CRM')
        i = crm & batch
        j = batch & ~crm
        df.loc[j, 'acidconcL'] = df.loc[i, 'acidconcL'].median()
        df.loc[j, 'factorCT'] = df.loc[i, 'factorCT'].median()

    nans = df.acidconcL.isnull()
    df.loc[nans, 'comment'] = 'acidconcL and factorCT were interpolated'
    df.loc[:, 'acidconcL'] = df.acidconcL.interpolate()
    df.loc[:, 'factorCT'] = df.factorCT.interpolate()

    print('\nRECALCULATING ALL BOTTLES\n' + '-' * 60)
    for i in df.index:  # every line
        print(pretty_path(df.datfilename[i]), end='')

        err = ''
        try:
            vols, emfs, tempC, msg = read_dat(df.datfilename[i])
            err += msg + ' '
            conc, ALK, pK1, pKstr, resid = recalcAlk_leastsq(
                df.salt[i], tempC,
                df.po4[i], df.sio4[i],
                df.pipVol[i],
                df.acidconcL[i],
                df.aciddens[i],
                vols, emfs,
                df.pKchoice[i])

            # Assign new values to the matrix
            var_names = ['acidconcL', 'RecalcAT', 'rms', 'pK1', 'pK_constant']
            df.loc[i, var_names] = conc, ALK, np.mean(resid), pK1, pKstr

        except FileNotFoundError:
            err += " File not found"
        except ValueError:
            err += " Something wrong with dat file"
        except IndexError:
            err += ' Error in recalculation'

        print(err)
    df['RecalcCT'] = df.DIC * df.factorCT

    from openpyxl import load_workbook
    book = load_workbook(xls_filename)
    writer = pd.ExcelWriter(xls_filename, engine='openpyxl')
    writer.book = book
    writer.sheets = dict((ws.title, ws) for ws in book.worksheets)

    df.to_excel(writer, 'reculculated', index=False)
    writer.save()
    print('=' * 60 + '\n')

    time_saved = df.calcID.sum() * 0.75 / 60.
    print('vindta_reCAlk saved you more than {} hours of your life'.format(time_saved))

    return df


def try_float(s):
    try:
        return float(s)
    except Exception:
        return np.NaN


def read_dat(dat_fname):
    raw = open(dat_fname, 'r', encoding='latin9').readlines()
    dat = np.array([line.split() for line in raw[2:]]).T.astype(float)
    vols, emfs, tempC = dat
    msg = ''
    if all(vols == 0):
        vols = np.arange(0, 0.15 * 35, 0.15)[:len(emfs)]
        msg += 'bad .dat - volumes generaged'

    return vols, emfs, tempC, msg


def calc_crm_acidconc(df):
    """
    Calculate a new Alkalinity acid factor/concentration for CRMs.
    1. Alkalinity is initially calculated and a difference from the CRM and measured alkalinity
    2. A correction factor is added to the acid concentration based on the difference
    3. Recalculate alkalinity using updated acid concentration
    4. Repeat steps 2 and 3 until the Alkalinity difference is < 0.001
    """

    print('\nCORRECTING CRMs\n' + '-' * 70)
    for i in df.index:
        bot = df.datfilename[i]
        if 'crm' in bot.lower():
            bot_print = pretty_path(bot)
            try:
                vols, emfs, tempC, _ = read_dat(df.datfilename[i])
                _, ALK, _, _, _ = recalcAlk_leastsq(
                    df.salt[i], tempC,
                    df.po4[i],
                    df.sio4[i],
                    df.pipVol[i],
                    df.acidconcL[i],
                    df.aciddens[i],
                    vols,
                    emfs,
                    df.pKchoice[i])
                diff = df.CRMAT[i] - ALK

                # loop that only stops when threshold is met.
                # changes the acidfactor while diff > threshold
                while (diff < -1e-3) | (diff > 1e-3):
                    df.loc[i, 'acidconcL'] += diff * 4.9e-5  # new acid concentration
                    acid_conc, ALK, _, _, _ = recalcAlk_leastsq(
                        df.salt[i],
                        tempC,
                        df.po4[i],
                        df.sio4[i],
                        df.pipVol[i],
                        df.acidconcL[i],
                        df.aciddens[i],
                        vols,
                        emfs,
                        df.pKchoice[i])
                    diff = df['CRMAT'][i] - ALK  # difference again
                    df.loc[i, 'calcID'] += 1

                    if df['calcID'][i] >= 30:
                        df.loc[i, 'acidconcL'] = np.NaN
                        break
                if df.calcID[i] < 30:
                    txt = '{} after {}  iterations'.format(
                        bot_print, df['calcID'][i])
                    print(txt)
                else:
                    print(bot_print, 'acid factor not converging after 30 iterations. Values set to NaN')
            except ValueError as e:
                print(bot_print, ": Something wrong with dat file", sep='')
            except FileNotFoundError:
                print(bot_print, ": does not exist", sep='')
    print('=' * 70)
    return df


def get_batch_indicies(df):

    # samples > 5hrs apart (300 min)
    new_batch_inds = np.abs(df.analysis_date.diff().astype('timedelta64[m]')) > 300
    df['analysis_batch'] = new_batch_inds.cumsum()

    return df


def pretty_path(path, nice_len=60):
    import numpy as np

    nice_len -= 4

    locs = [i for i, c in enumerate(path[::-1]) if c == '/']
    diff = np.array(locs) - nice_len
    mindif_idx = np.argmin(np.abs(diff))
    idx = locs[mindif_idx]
    return '.../' + path[-idx:]


def recalcAlk_leastsq(sal, tempC, po4, si, samplevol, acidconcKG, aciddens, Vols, Emfs, pKconst):
    """
    This is the "master script" for the VINDTA_recalc_leastsq.py file.
    The script was orignally written by A.G. Dickson in 1993 and then
    coded into Python by Luke Gregor in 2011.
    Note
    INPUT:  The input has been adapted for VINDTA outputs [units].
        sal =         salinity [psu]
        tempC =       Temperature [degC]
        po4 =         Phosphate [umol/kg]
        si =          Silicate [umol/kg]
        samplevol =   Sample Volume [mL]
        acidconcKG =  Acid Concentration [mol/kg]
        aciddens =    Acid Density [kg/L]
        Vols =        array of acid volumes [mL]
        Emfs =        array of voltages [mV]
        pKconst =     1 - Roy et al, 1993
                      2 - Goyet and Poisson, 1989
                      3 - Hansson refit by Dickson and Millero, 1987
                      4 - Mehrbach refit by Dickson and Millero, 1987
                      5 - Hansson and Mehrbach refit BY Dickson & Millero, 1987
                      6 - Mehrbach et al, 1973
                      7 - Millero, 1979
                      8 - Cai and Wang, 1998
                      9 - Lueker et al, 2000
                      10- Mojica Prieto and Millero, 2002
                      11- Millero et al, 2002
                      12- Millero, 2006
                      13- Millero, 2010

    OUTPUT:
        Acid Concentration [mol/kg]
        Alkalinity [umol/kg]
        pK1
        pK1 + pK2 constant choice
        residuals from the calculations
    """

    def SetUp(S, T, PT, SiT, C, DAcid, V, V0, E, pKconst):
        """Subroutine to set up calculation ready for optimisation

        Written by A.G. Dickson (from Fortran script)
        Transcribed by L. Gregor

        INPUT:  S  [psu]
            T  [degC]
            PT [mol/kg]
            SiT[mol/kg]
            V0 [cm3]
            DAcid [g/cm3]
            V  [cm3]
            E  [V]
        OUTPUT: H  []
            W  [g]
            t  [tot concts]
            k  [equ consts]
            X0 [initial estimates]
        """

        if (S < 5) | np.isnan(S):  # Seawater sample
            print(": Sample has salinity < 5 PSU or NaN", end='')

        W0 = V0 * DensSW(S, T)  # mass of sample titrated [g]
        # values for total concentrations (output global)
        t = ConcnsSW(S, PT, SiT)
        # values for equilibrium constants (output global)
        k = ConstsSW(S, T, t, pKconst)
        # pH conversion factor from free to total scale
        Z = 1. + t[-2] / k[-3]

        # Calculate Nernst Factor: E = E0 +/- (RT/F) ln[H]
        KNernst = 8.31451 * (273.15 + T) / 96485.309
        if E[0] > E[-1]:
            KNernst = -KNernst

        # mass of acid titrant at each titration point [g]
        W = V * DAcid

        # Estimate E0 using last two titration points (at low pH)
        # slightly different to Fortran script
        E0 = EstimE0(W0, W, E, C, KNernst)

        # Calculate [H] using this initial estimate of E0
        H = np.exp((E - E0) / KNernst)

        # Creating initial solution vector for the least-squares funcion
        X0 = [1., 2., 2., 1.]

        return H, W, W0, Z, t, k, X0

    def FCN(X, H, W, W0, C, Z, t, k, **kwds):
        PT, SiT, BT, ST, FT = t
        K0, K1, K2, KB, K1P, K2P, K3P, KSi, KS, KF, KW = k
        F = X[0]
        AT = X[1] * 1e-3
        CT = X[2] * 1e-3
        K1 = X[3] * 1e-6

        Denom = (F * H) ** 2. + K1 * F * H + K1 * K2
        alkCT = CT * K1 * (F * H + 2. * K2) / Denom
        alkBT = BT / (1. + F * H / KB)
        alkPT = PT * ((K1P * K2P * F * H + 2. * K1P * K2P * K3P - (F * H) ** 3.) /
                      ((F * H) ** 3. + K1P * (F * H) ** 2. + K1P * K2P * F * H + K1P * K2P * K3P))
        alkSiT = SiT / (1. + F * H / KSi)
        alkST = ST / (1. + KS * Z / (F * H))
        alkFT = FT / (1. + KF / (F * H))
        OH = KW / (F * H)
        AcidAdd = (W0 + W) / W0 * (F * H / Z - OH) - (W / W0) * C

        Residual = AT - alkCT - alkBT - alkPT - alkSiT + alkST + alkFT + AcidAdd

        return Residual

    # Subroutines to SetUp #
    def DensSW(S, T):
        """Function to caclulate the density of sea water.
        Based on Millero and Poisson (1981) Deep-Sea Res. 28, 625.

        Written by A.G. Dickson (from Fortran script)
        Transcribed to Python by L. Gregor

        INPUT:  S [psu]
                T [degC]
        OUTPUT: DensSW
        """
        # Calculate seawater density (using sample's S titration
        # temperature (temperature is assumed constant during run)
        a0 = 999.842594
        a1 = 6.793952e-2
        a2 = -9.095290e-3
        a3 = 1.001685e-4
        a4 = -1.120083e-6
        a5 = 6.536332e-9

        b0 = 8.24493e-1
        b1 = -4.0899e-3
        b2 = 7.6438e-5
        b3 = -8.2467e-7
        b4 = 5.3875e-9

        c0 = -5.72466e-3
        c1 = +1.0227e-4
        c2 = -1.6546e-6

        d0 = 4.8314e-4

        DensSW = (a0 + (a1 + (a2 + (a3 + (a4 + a5 * T) * T) * T) * T) * T) + \
                 (b0 + (b1 + (b2 + (b3 + b4 * T) * T) * T) * T) * S + \
                 (c0 + (c1 + c2 * T) * T) * S * np.sqrt(S) + d0 * S ** 2
        DensSW /= 1000.

        return DensSW

    def ConcnsSW(S, PT, SiT):
        """Subroutine to calculate appropriate total concentrations,
        for seawater of salinity of, S.

        Written by A.G. Dickson (from Fortran script)
        Transcribed to Python by L. Gregor

        INPUT:  S [psu]
        OUTPUT: BT [mol/kg-soln]
              ST [mol/kg-soln]
              FT [mol/kg-soln]
        """
        # Uppstron (1974) Deep-Sea Res. 21, 161.
        BT = (0.000232 / 10.811) * (S / 1.80655)

        # Morris and Riley (1966) Deep-Sea Res. 13, 699.
        ST = (0.1400 / 96.062) * (S / 1.80655)

        # Riley (1965) Deep-Sea Res 12, 219.
        FT = (0.000067 / 18.998) * (S / 1.80655)

        return PT, SiT, BT, ST, FT

    def ConstsSW(S, T, t, pKconst):
        """Taken from the matlab script as it works
        need to rewrite this - also for option of other constants"""
        PT, SiT, BT, ST, FT = t

        IonS = 19.924 * S / (1000. - 1.005 * S)
        TK = T + 273.15

        # Boric acid, DOEv3 compliant:
        lnKB = (-8966.9 - 2890.53 * (S ** 0.5) - 77.942 * S) / TK
        lnKB = lnKB + (1.728 * S ** (3. / 2.) - 0.0996 * S ** 2.) / TK
        lnKB = lnKB + (148.0248 + 137.1942 * S ** 0.5 + 1.62142 * S)
        lnKB = lnKB + (-24.4344 - 25.085 * S ** 0.5 - .2474 * S) * np.log(TK)
        lnKB = lnKB + (.053105 * S ** 0.5) * TK
        KB = np.exp(lnKB)

        # Bisulfate ion, DOEv3 compliant:
        lnKS = -4276.1 / TK + 141.328 - 23.093 * np.log(TK)
        lnKS = lnKS + (-13856 / TK + 324.57 - 47.986 * np.log(TK)) * (IonS) ** 0.5
        lnKS = lnKS + (35474 / TK - 771.54 + 114.723 * np.log(TK)) * IonS
        lnKS = lnKS - (2698 / TK) * (IonS) ** (3. / 2.) + (1776 / TK) * IonS ** 2.
        lnKS = lnKS + np.log(1. - .001005 * S)
        KS = np.exp(lnKS)

        # ##################
        # The DOEv3 method causes problems with X2-optimization under extremely
        # high DIC levels (hydrothermal vents, etc.). Seems to be related to KF
        # DOEv2's KF does a lot better, so i'm using that.
        # For regular samples there's no big difference.
        # ##################
        # Hydrogen fluoride, DOEv3 compliant (as from Perez & Fraga, 1987):
        # lnKF = 874 ./ TK - 9.68 + 0.111 .* S .** 0.5
        # KF   = exp(lnKF)
        # ##################
        # Hydrogen fluoride, DOEv2 compliant (as from Dickson & Riley, 1979a):
        IonS = 19.924 * S / (1000. - 1.005 * S)
        lnKF = (1590.2 / TK - 12.641 + 1.525 *
                (IonS) ** 0.5) + np.log(1. - .001005 * S)
        KF = np.exp(lnKF) * (1. + ST / KS)  # convert from free to total pH scale
        # ##################

        # Water, DOEv3 compliant:
        lnKW = 148.9652 - 13847.26 / TK - 23.6521 * np.log(TK)
        lnKW = lnKW + (-5.977 + 118.67 / TK + 1.0495 * np.log(TK)) * S ** 0.5
        lnKW = lnKW - .01615 * S
        KW = np.exp(lnKW)

        # Phosporic acid K1, DOEv3 compliant
        lnKP1 = -4576.752 / TK + 115.525 - 18.453 * np.log(TK)
        lnKP1 = lnKP1 + (-106.736 / TK + .69171) * S ** 0.5
        lnKP1 = lnKP1 + (-.65643 / TK - .01844) * S
        K1P = np.exp(lnKP1)

        # Phosporic acid K2, DOEv3 compliant
        lnKP2 = -8814.715 / TK + 172.0883 - 27.927 * np.log(TK)
        lnKP2 = lnKP2 + (-160.34 / TK + 1.3566) * S ** 0.5
        lnKP2 = lnKP2 + (.37335 / TK - .05778) * S
        K2P = np.exp(lnKP2)

        # Phosporic acid K3, DOEv3 compliant
        lnKP3 = -3070.75 / TK - 18.141
        lnKP3 = lnKP3 + (17.27039 / TK + 2.81197) * S ** 0.5
        lnKP3 = lnKP3 + (-44.99486 / TK - .09984) * S
        K3P = np.exp(lnKP3)

        # Silicic acid, DOEv3 compliant:
        lnKSi = -8904.2 / TK + 117.385 - 19.334 * np.log(TK)
        lnKSi = lnKSi + (-458.79 / TK + 3.5913) * (IonS) ** 0.5
        lnKSi = lnKSi + (188.74 / TK - 1.5998) * IonS
        lnKSi = lnKSi + (-12.1652 / TK + .07871) * IonS ** 2.
        lnKSi = lnKSi + np.log(1. - .001005 * S)
        KSi = np.exp(lnKSi)

        lnK0 = (-60.2409 + 93.4517 * (100 / TK) + 23.3585 * np.log(TK / 100) +
                S * (0.023517 - 0.023656 * (TK / 100) + 0.0047036 * (TK / 100) ** 2.))
        K0 = np.exp(lnK0)

        SWStoTOT = (1. + ST / KS) / (1. + ST / KS + FT / KF)
        K1, K2 = ConstsK1K2(S, TK, pKconst, SWStoTOT)

        return K0, K1, K2, KB, K1P, K2P, K3P, KSi, KS, KF, KW

    def DesnNaCl(CNaCl, T):
        """Function to calculate the density of a sodium chloride solution.
        Based on equation by Lo Surdo et al.
          J. Chem. Thermodynamics 14, 649 (1982)

        Written by A.G. Dickson (from Fortran script)
        Transcribed to Python by L. Gregor

        INPUT:  CNaCl - conc of sodium chloride [mol/kg-soln]
              T [degC]
        OUTPUT: DensNaCl
        """
        mNaCl = CNaCl / (1. - 0.058443 * CNaCl)  # molality

        # density of SMOW [kg/m3]
        DH2O = (999.842594 + 6.793952e-2 * T - 9.095290e-3 * T ** 2. +
                1.001685e-4 * T ** 3. - 1.120083e-6 * T ** 4. - 6.53633e-9 * T ** 5.)

        # density of NaCl (kg/m3)
        DNaCl = (DH2O + mNaCl * (46.5655 - 0.2341 * T + 3.4128e-3 * T ** 2. -
                                 2.7030e-5 * T ** 3. + 1.4037e-7 * T ** 4) +
                 mNaCl ** 1.5 * (-1.8527 + 5.3956e-2 * T - 6.2635e-4 * T ** 2.) +
                 mNaCl ** 2. * (-1.6368 - 9.5653e-4 * T + 5.2829e-5 * T ** 2.) +
                 0.2274 * mNaCl ** 2.5)

        DensNaCl = 1.e-3 * DNaCl

        return DensNaCl

    def ConstsNaCl(CNaCl, T):
        """Subroutine to calculate values of dissociation constants,
        appropriateto a sodium chloride solution of concentration,
        CNaCl, and temperature, T.

        Written by A.G. Dickson (from Fortran script)
        Transcribed to Python by L. Gregor

        INPUT:  CNaCl - conc of sodium chloride [mol/kg-soln]
              T [degC]
        OUTPUT: K1,K2
              KW
        """
        global K1, K2, KW

        # TK = 273.15 + T
        # Dyrssen and Hansson (1973) Mar. Chem. 1, 137.
        K1 = np.exp(-13.82)
        K2 = np.exp(21.97)
        KW = np.exp(-31.71)

        return K1, K2, KW

    def EstimE0(W0, W, E, C, KNernst):
        """This subroutine estimates an initial value of E0 using a Gran
        function an the last two titration points to estimate AT.
        [H] is calculated at those 2 points and an average E0 estimated.

        Written by A.G. Dickson (from Fortran script)
        Transcribed to Python by L. Gregor

        INPUT:  W0 [g]
              W  [g]
              E  [V]
              C  [mol/kg]
              KNernst [V]
        OUTPUT: E0 [V]
        """
        WA = W[-2]
        WB = W[-1]
        EA = E[-2]
        EB = E[-1]

        # Calculate gran function (W0+W) exp(E/K) and fit to y = a0 + a1*x
        #   A1 = (yB - yA) / (xB - xA)
        #   A0 = yA - A1*xA
        A1 = ((W0 + WB) * np.exp(EB / KNernst) - (W0 + WA) * np.exp(EA / KNernst)) / (WB - WA)
        A0 = (W0 + WA) * np.exp(EA / KNernst) - A1 * WA

        # Estimate of TA
        AT = (-A1 / A0) * C / W0
        # Calculate [H] at those 2 points and hence an average E0
        HA = (WA * C - W0 * AT) / (W0 + WA)
        HB = (WB * C - W0 * AT) / (W0 + WB)
        E0 = (EA - KNernst * np.log(HA) + EB - KNernst * np.log(HB)) / 2.

        return E0

    def ConstsK1K2(S, TK, n, SWStoTOT):
        # These constants were taken from the CO2SYS_calc
        # script for MATLAB (van Heuven et al. 2011)
        # see their script for more details on dissociation constants
        # http://cdiac.ornl.gov/oceans/co2rprt.html

        if n == 1:  # ROY et al, 1993
            # ROY et al, Marine Chemistry, 44:249-267, 1993
            lnK1 = (2.83655 - 2307.1266 / TK - 1.5529413 * np.log(TK) +
                    (-0.20760841 - 4.0484 / TK) * np.sqrt(S) + 0.08468345 * S -
                    0.00654208 * np.sqrt(S) * S)
            K1 = np.exp(lnK1) * (1 - 0.001005 * S) / SWStoTOT  # convert to SWS pH scale
            lnK2 = (-9.226508 - 3351.6106 / TK - 0.2005743 * np.log(TK) +
                    (-0.106901773 - 23.9722 / TK) * np.sqrt(S) + 0.1130822 * S -
                    0.00846934 * np.sqrt(S) * S)
            K2 = np.exp(lnK2) * (1 - 0.001005 * S) / SWStoTOT  # convert to SWS pH scale

        if n == 2:  # GOYET AND POISSON, 1989
            # GOYET AND POISSON, Deep-Sea Research, 36(11):1635-1654
            pK1 = 812.27 / TK + 3.356 - 0.00171 * S * np.log(TK) + 0.000091 * S ** 2
            K1 = 10 ** (-pK1)  # this is on the SWS pH scale in mol/kg-SW
            pK2 = 1450.87 / TK + 4.604 - 0.00385 * S * np.log(TK) + 0.000182 * S ** 2
            K2 = 10 ** (-pK2)  # this is on the SWS pH scale in mol/kg-SW

        if n == 3:
            # HANSSON refit BY DICKSON AND MILLERO
            # Dickson and Millero, Deep-Sea Research,
            #       34(10):1733-1743, 1987
            pK1 = 851.4 / TK + 3.237 - 0.0106 * S + 0.000105 * S ** 2
            K1 = 10 ** (-pK1)  # this is on the SWS pH scale in mol/kg-SW
            pK2 = -3885.4 / TK + 125.844 - 18.141 * np.log(TK) - 0.0192 * S + 0.000132 * S ** 2
            K2 = 10 ** (-pK2)  # this is on the SWS pH scale in mol/kg-SW

        if n == 4:  # MEHRBACH refit BY DICKSON AND MILLERO 1987
            # Dickson and Millero, Deep-Sea Research,
            #       34(10):1733-1743, 1987
            pK1 = 3670.7 / TK - 62.008 + 9.7944 * np.log(TK) - 0.0118 * S + 0.000116 * S ** 2
            K1 = 10 ** (-pK1)  # this is on the SWS pH scale in mol/kg-SW
            # This is in Table 4 on p. 1739.
            pK2 = 1394.7 / TK + 4.777 - 0.0184 * S + 0.000118 * S ** 2
            K2 = 10 ** (-pK2)  # this is on the SWS pH scale in mol/kg-SW

        if n == 5:
            # HANSSON and MEHRBACH refit BY DICKSON AND MILLERO 1987
            # Dickson and Millero, Deep-Sea Research,
            #       34(10):1733-1743, 1987
            pK1 = 845 / TK + 3.248 - 0.0098 * S + 0.000087 * S ** 2
            K1 = 10 ** (-pK1)  # this is on the SWS pH scale in mol/kg-SW
            # This is in Table 5 on p. 1740.

            pK2 = 1377.3 / TK + 4.824 - 0.0185 * S + 0.000122 * S ** 2
            K2 = 10 ** (-pK2)  # this is on the SWS pH scale in mol/kg-SW

        # if n == 6:
        #     # GEOSECS and Peng et al use K1, K2 from Mehrbach et al,
        #     # Limnology and Oceanography, 18(6):897-907, 1973.
        #     pK1 = - 13.7201 + 0.031334 * TK + 3235.76 / TK + 1.3e-5 * S * TK - 0.1032 * S ** 0.5
        #     K1 = 10 ** (-pK1) / fH  # convert to SWS scale
        #
        #     pK2 = 5371.9645 + 1.671221 * TK + 0.22913 * S + 18.3802 * np.log10(S) \
        #           - 128375.28 / TK - 2194.3055 * np.log10(TK) - 8.0944e-4 * S * TK \
        #           - 5617.11 * np.log10(S) / TK + 2.136 * S / TK
        #     # pK2 is not defined for S=0, since log10(0)=-inf
        #     K2 = 10 ** (-pK2) / fH  # convert to SWS scale

        if n == 7:
            # PURE WATER CASE
            # Millero, F. J., Geochemica et Cosmochemica Acta
            #       43:1651-1661, 1979:
            lnK1 = 290.9097 - 14554.21 / TK - 45.0575 * np.log(TK)
            K1 = np.exp(lnK1)

            lnK2 = 207.6548 - 11843.79 / TK - 33.6485 * np.log(TK)
            K2 = np.exp(lnK2)

        if n == 8:  # From Cai and Wang 1998
            # From Cai and Wang 1998, for estuarine use.
            fH = 1.29 - 0.00204 * TK + (0.00046 - 0.00000148 * TK) * S * S
            F1 = 200.1 / TK + 0.3220
            pK1 = 3404.71 / TK + 0.032786 * TK - 14.8435 - 0.071692 * F1 * S ** 0.5 + 0.0021487 * S
            K1 = 10 ** -pK1 / fH  # convert to SWS scale
            F2 = -129.24 / TK + 1.4381
            pK2 = 2902.39 / TK + 0.02379 * TK - 6.4980 - 0.3191 * F2 * S ** 0.5 + 0.0198 * S
            K2 = 10 ** -pK2 / fH  # convert to SWS scale

        if n == 9:  # From Lueker, Dickson, Keeling, 2000
            # From Lueker, Dickson, Keeling, 2000
            pK1 = 3633.86 / TK - 61.2172 + 9.6777 * np.log(TK) - 0.011555 * S + 0.0001152 * S ** 2
            K1 = 10 ** -pK1 / SWStoTOT  # convert to SWS pH scale

            pK2 = 471.78 / TK + 25.929 - 3.16967 * np.log(TK) - 0.01781 * S + 0.0001122 * S ** 2
            K2 = 10 ** -pK2 / SWStoTOT  # convert to SWS pH scale

        if n == 10:  # Mojica Prieto and Millero 2002
            # Mojica Prieto and Millero. 2002.
            # Geochim. et Cosmochim. Acta. 66(14) 2529-2540.
            pK1 = -43.6977 - 0.0129037 * S + 1.364e-4 * S ** 2 + 2885.378 / TK + 7.045159 * np.log(TK)
            K1 = 10 ** -pK1  # this is on the SWS pH scale in mol/kg-SW

            pK2 = (-452.0940 + 13.142162 * S - 8.101e-4 * S ** 2 +
                   21263.61 / TK + 68.483143 * np.log(TK) +
                   (-581.4428 * S + 0.259601 * S ** 2) / TK - 1.967035 * S * np.log(TK))
            K2 = 10 ** -pK2  # this is on the SWS pH scale in mol/kg-SW

        if n == 11:  # Millero et al., 2002
            # Millero et al., 2002. Deep-Sea Res. I (49) 1705-1723.
            pK1 = 6.359 - 0.00664 * S - 0.01322 * TK + 4.989e-5 * TK ** 2
            K1 = 10 ** -pK1  # this is on the SWS pH scale in mol/kg-SW

            pK2 = 9.867 - 0.01314 * S - 0.01904 * TK + 2.448e-5 * TK ** 2
            K2 = 10 ** -pK2  # this is on the SWS pH scale in mol/kg-SW

        if n == 12:  # From Millero 2006
            # Millero, Graham, Huang, Bustos-Serrano, Pierrot.
            #      Mar.Chem. 100 (2006) 80-94
            pK1_0 = -126.34048 + 6320.813 / TK + 19.568224 * np.log(TK)
            A_1 = 13.4191 * S ** 0.5 + 0.0331 * S - 5.33e-5 * S ** 2
            B_1 = -530.123 * S ** 0.5 - 6.103 * S
            C_1 = -2.06950 * S ** 0.5
            pK1 = A_1 + B_1 / TK + C_1 * np.log(TK) + pK1_0
            K1 = 10 ** -pK1
            pK2_0 = -90.18333 + 5143.692 / TK + 14.613358 * np.log(TK)
            A_2 = 21.0894 * S ** 0.5 + 0.1248 * S - 3.687e-4 * S ** 2
            B_2 = -772.483 * S ** 0.5 - 20.051 * S
            C_2 = -3.3336 * S ** 0.5
            pK2 = A_2 + B_2 / TK + C_2 * np.log(TK) + pK2_0
            K2 = 10 ** -pK2

        if n == 13:  # From Millero, 2010
            # Marine and Freshwater Research, v. 61, p. 139-142.
            pK10 = -126.34048 + 6320.813 / TK + 19.568224 * np.log(TK)
            # This is from their table 2, page 140.
            A1 = 13.4038 * S ** 0.5 + 0.03206 * S - 5.242e-5 * S ** 2
            B1 = -530.659 * S ** 0.5 - 5.8210 * S
            C1 = -2.0664 * S ** 0.5
            pK1 = pK10 + A1 + B1 / TK + C1 * np.log(TK)
            K1 = 10 ** -pK1
            pK20 = -90.18333 + 5143.692 / TK + 14.613358 * np.log(TK)
            A2 = 21.3728 * S ** 0.5 + 0.1218 * S - 3.688e-4 * S ** 2
            B2 = -788.289 * S ** 0.5 - 19.189 * S
            C2 = -3.374 * S ** 0.5
            pK2 = pK20 + A2 + B2 / TK + C2 * np.log(TK)
            K2 = 10 ** -pK2

        return K1, K2

    from scipy.optimize import leastsq
    import numpy as np

    global pKstring

    pKstring = ['',
                'Roy et al, 1993',
                'Goyet and Poisson, 1989',
                'Hansson refit by Dickson and Millero, 1987',
                'Mehrbach refit by Dickson and Millero, 1987',
                'Hansson and Mehrbach refit BY Dickson and Millero, 1987',
                'Mehrbach et al, 1973',
                'Millero, 1979',
                'Cai and Wang, 1998',
                'Lueker et al, 2000',
                'Mojica Prieto and Millero, 2002',
                'Millero et al, 2002',
                'Millero, 2006',
                'Millero, 2010']

    S = sal  # psu
    T = tempC  # degC
    PT = po4 * 1e-6  # mol/kg from umol/kg
    SiT = si * 1e-6  # mol/kg from umol/kg
    V0 = samplevol  # mL or cm3
    C = acidconcKG  # mol/kg
    DAcid = aciddens  # kg/L
    V = np.array(Vols)  # mL
    E = np.array(Emfs) * 1e-3  # V form mV

    H, W, W0, Z, t, k, X0 = SetUp(S, T, PT, SiT, C, DAcid, V, V0, E, pKconst)

    X, covarience, info, mesg, ier = leastsq(FCN, X0,
                                             args=(H, W, W0, C, Z, t, k),
                                             full_output=1,
                                             xtol=0.0001)

    residuals = FCN(X, H, W, W0, C, Z, t, k)

    F, AT, CT, K1 = X

    return C, AT * 1e3, -np.log10(K1 * 1e-6), pKstring[pKconst], residuals


if __name__ == '__main__':

    print(os.getcwd())
    dbs_filename = '../CSIR.dbs'
    datfiles_dir = '../CSIR'
    exl_filename = '../vindta_reCAlk/Win2017_test.xlsx'

    df = dbs_to_excel(dbs_filename, datfiles_dir, exl_filename, verbose=True)
