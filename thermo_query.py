def query( hr, mn, T ):
    # Input: hour, minute, temperature

    if hr >= 22 or hr < 7:
        #TT = 66.5
        TT = 70.
    else:
        TT = 71.

    if T < TT:
        return True
    else:
        return False

