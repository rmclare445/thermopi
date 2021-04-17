def read_nl( ):

    nml_opts = {}

    with open("namelist.txt", "r") as f:
        lines = f.readlines()
        
    for line in lines:
        
        # Must add new elif for each new nl variable
        if "#" in line:
            pass
        elif "n_phase" in line:
            exec( "global n_phase; "     + line )
            nml_opts["n_phase"]     = int(n_phase)
        elif "phase_hr" in line:
            exec( "global phase_hr; "    + line )
            nml_opts["phase_hr"]     = int(phase_hr)
        elif "phase_min" in line:
            exec( "global phase_min; "   + line )
            nml_opts["phase_min"]     = int(phase_min)
        elif "phase_T" in line:
            exec( "global phase_T; "     + line )
            nml_opts["phase_T"]     = int(phase_T)
        elif "up_tol" in line:
            exec( "global up_tol; "      + line )
            nml_opts["up_tol"]      = float(up_tol)
        elif "dn_tol" in line:
            exec( "global dn_tol; "      + line )
            nml_opts["dn_tol"]      = float(dn_tol)
        elif "freq" in line:
            exec( "global freq; "        + line )
            nml_opts["freq"]        = float(freq)
            
    return nml_opts
    
def get_freq( ):
    # Only returns frequency
    return read_nl( )["freq"]

## Maybe add a function to reset nl to default values

if __name__ == "__main__":
    print( read_nl() )