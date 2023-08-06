"""
This file contains the default parameters for the
setup files and also contains the range of possible
values in a seperate dictionary.
"""

defaults = {
    'date_fmt': [
        'mm/dd/yy HH:MM',
        'mm/dd/yyyy HH:MM',
        'dd/mm/yy HH:MM',
        'dd/mm/yyyy HH:MM',
        'yyyy/mm/dd HH:MM'],
    'acidconcL': 0.1,
    'aciddens': 1.02266027,
    'pipVol': 97.846,
    'po4': 0.5,
    'sio4': 2.5,
    'factorCT': 1.0,
    'pK1': 5.0,
    'pKchoice': [
        "Millero, 2010",
        "Millero, 2006",
        "Millero et al, 2002",
        "Mojica Prieto and Millero, 2002",
        "Lueker et al, 2000",
        "Cai and Wang, 1998",
        "Roy et al, 1993",
        "Goyet and Poisson, 1989",
        "Hansson and Mehrbach refit BY Dickson & Millero, 1987",
        "Mehrbach refit by Dickson and Millero, 1987",
        "Hansson refit by Dickson and Millero, 1987",
        "Millero, 1979",
        "Mehrbach et al, 1973"],
    'header': (
        'runtype', 'bottle', 'station', 'cast', 'niskin',
        'depth', 'temp', 'salt', 'counts', 'runtime',
        'DIC', 'factorCT', 'blank', 'RecalcCT',
        'lastCRMCT', 'CRMCT', 'lastCRMAT', 'CRMAT',
        'batch', 'ALK', 'RecalcAT', 'rms', 'calcID',
        'acidconcL', 'aciddens', 'pipVol', 'comment',
        'lat', 'lon', 'date', 'time', 'CellID'),
}
