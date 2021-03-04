from read_nl import read_nl

def query( hr, mn, T, outpt ):
    # Input: hour, minute, temperature, output
    
    # Reads namelist every time, allowing user to
    #  change settings without halting operation
    nml_opts = read_nl()
    
    # Thresholds (target temps) and time dependencies
    ## Just day/night phase are possible now. Middle phases
    ##  may come later but there's no need at present.
    ## Other scheduling considerations such as day of week
    ##  or seasonal dependence may be worthwhile.
    if hr >= nml_opts["np_begin_hr"] or hr <= nml_opts["np_end_hr"]:
        if hr == nml_opts["np_begin_hr"]:
            if mn >= nml_opts["np_begin_mn"]:
                TT = nml_opts["np_temp"]
            else:
                TT = nml_opts["dp_temp"]
        elif hr == nml_opts["np_end_hr"]:
            if mn < nml_opts["np_end_mn"]:
                TT = nml_opts["np_temp"]
            else:
                TT = nml_opts["dp_temp"]
        else:
            TT = nml_opts["np_temp"]
    else:
        TT = nml_opts["dp_temp"]
    
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