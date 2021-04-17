from read_nl import read_nl

def query( hr, mn, T, outpt ):
    # Input: hour, minute, temperature, current relay status
    
    # Reads namelist every time, allowing user to
    #  change settings without halting operation
    nml_opts = read_nl()
    
    # Thresholds (target temps; TT) and time dependencies
    # For monophase configuration
    if nml_opts["n_phase"] == 1:
        TT = nml_opts["phase_T"]
    # For the final phase (because it sometimes spans midnight)
    elif (hr == nml_opts["phase_hr"][0] and mn < nml_opts["phase_min"][0]) or
         (hr == nml_opts["phase_hr"][-1] and mn >= nml_opts["phase_min"][-1]) or
          hr > nml_opts["phase_hr"][-1] or hr < nml_opts["phase_hr"][0]:
        TT = nml_opts["phase_T"][-1]
    # For all phases except the final
    elif nml_opts["n_phase"] > 2:
        for phase in range( nml_opts["n_phase"]-1 ):
            if ( ( 
                   hr > nml_opts["phase_hr"] or
                   (hr == nml_opts["phase_hr"][phase] and mn >= nml_opts["phase_min"][phase])
                 ) 
                 and 
                 ( 
                   (hr < nml_opts["phase_hr"][phase+1]) or
                   (hr == nml_opts["phase_hr"][phase+1] and mn < nml_opts["phase_min"][phase+1])
                 )
               ):
                TT = nml_opts["phase_T"][phase]
                break
    # For diphase configuration (work already done in final phase statement)
    else:
        TT = nml_opts["phase_T"][0]
    
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