#from read_nl import read_nl
from locator import get_min_dist

def query( lt, T, outpt, nml_opts ):
    # Input: local time, temperature, current relay status
    hr = lt[3]
    mn = lt[4]

    # Reads namelist every time, allowing user to
    #  change settings without halting operation
    #nml_opts = read_nl()

    # Get number of phases specified
    n_phase = len( nml_opts['phase_hr'] )
    if n_phase !=  len( nml_opts['phase_min'] ) or n_phase !=  len( nml_opts['phase_T'] ):
        raise RuntimeWarning( 'WARNING: Phase configuration mismatch! \n Namelist is incorrectly filled and thermopi may not function properly.' )

    # Thresholds (target temps; TT) and time dependencies
    # For monophase configuration
    if n_phase == 1:
        TT = nml_opts["phase_T"]
    # For the final phase (because it sometimes spans midnight)
    elif (hr == nml_opts["phase_hr"][0]  and mn < nml_opts["phase_min"][0]  ) or \
         (hr == nml_opts["phase_hr"][-1] and mn >= nml_opts["phase_min"][-1]) or \
          hr > nml_opts["phase_hr"][-1]  or  hr < nml_opts["phase_hr"][0]:
        TT = nml_opts["phase_T"][-1]
    # For all phases except the final
    elif n_phase > 2:
        for phase in range( n_phase-1 ):
            if ( (
                   hr > nml_opts["phase_hr"][phase]  or
                  (hr == nml_opts["phase_hr"][phase] and mn >= nml_opts["phase_min"][phase])
                 )
                 and
                 (
                   hr < nml_opts["phase_hr"][phase+1]  or
                  (hr == nml_opts["phase_hr"][phase+1] and mn < nml_opts["phase_min"][phase+1])
                 )
               ):
                TT = nml_opts["phase_T"][phase]
                break
    # For diphase configuration (work already done in final phase statement)
    else:
        TT = nml_opts["phase_T"][0]

    # Locator
    if nml_opts['locator']:
        try:
            if get_min_dist() > nml_opts['radius']:
                TT = nml_opts['away_T']
        except:
            print( "%02d%02d%02d_%02d:%02d:%02d - Unable to retrieve location data!" %
                   (lt[0], lt[1], lt[2], lt[3], lt[4], lt[5]) )

    # If output is True/False, check threshold
    if outpt:
        if T >= TT + nml_opts["up_tol"]:
            return False
        else:
            return None
    else:
        if T <= TT - nml_opts["dn_tol"]:
            return True
        else:
            return None
