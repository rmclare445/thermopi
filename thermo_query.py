import read_nl as nl

def query( hr, mn, T, outpt ):
    # Input: hour, minute, temperature, output
    
    # Reads namelist every time, allowing user to
    # change settings without halting operation
    nl_opts = nl.read_nl()
    
    # Thresholds and time dependencies
    # Should use minutes at some point
    if hr >= nl_opts["np_begin"] or hr < nl_opts["np_end"]:
        TT = nl_opts["np_temp"]
    else:
        TT = nl_opts["dp_temp"]
    
    # If output is True/False, check threshold
    if outpt:
        if T >= TT + nml_opts["thresh"]:
            return False
        else:
            return None
    else:
        if T <= TT - nml_opts["thresh"]:
            return True
        else:
            return None