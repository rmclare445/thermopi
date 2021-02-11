def C_to_F( C ):
    return C * (9/5.) + 32.
    
def pert( q, Qs ):
    return abs(q - (sum(Qs)/len(Qs)))
    
def update( t, tt ):
    tt.append(t)
    return tt[1:]