def query( hr, mn, T, opt ):
    # Input: hour, minute, temperature, output
    
    # Thresholds and time dependencies
    # Should use minutes at some point
    ## Should really use a namelist for schedule
    ## hours as well as temperatures; this would
    ## enable altering these settings during operation
    if hr >= 22 or hr < 7:
        TT = 66.
    else:
        TT = 70.
    
    # If output is True/False, check threshold
    if opt:
        if T >= TT + 1.:
            return False
        else:
            return None
    else:
        if T <= TT - 1.:
            return True
        else:
            return None