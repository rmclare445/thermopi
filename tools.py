def C_to_F( C ):
    # Convert Celsius to Fahrenheit
    return C * (9/5.) + 32.
    
def pert( q, Qs ):
    # Perturbation magnitude from mean
    return abs(q - (sum(Qs)/len(Qs)))
    
def update( t, tt ):
    # Store new value, discard oldest
    tt.append(t)
    return tt[1:]
