nml_error_dp_default = 70   ## in case of bogus nml temps
nml_error_np_default = 66

def read_nl( ):

    nml_opts = {}

    with open("namelist.txt", "r") as f:
        lines = f.readlines()
        
    for line in lines:
        
        # Must add new elif for each new nl variable
        if "#" in line:
            pass
        elif "np_begin_hr" in line:
            exec( "global np_begin_hr; " + line )
            nml_opts["np_begin_hr"] = int(np_begin_hr)
        elif "np_begin_mn" in line:
            exec( "global np_begin_mn; " + line )
            nml_opts["np_begin_mn"] = int(np_begin_mn)
        elif "np_end_hr" in line:
            exec( "global np_end_hr; "   + line )
            nml_opts["np_end_hr"]   = int(np_end_hr)
        elif "np_end_mn" in line:
            exec( "global np_end_mn; "   + line )
            nml_opts["np_end_mn"]   = int(np_end_mn)
        elif "np_temp" in line:
            exec( "global np_temp; "     + line )
            nml_opts["np_temp"]     = float(np_temp)
        elif "dp_temp" in line:
            exec( "global dp_temp; "     + line )
            nml_opts["dp_temp"]     = float(dp_temp)
        elif "up_tol" in line:
            exec( "global up_tol; "      + line )
            nml_opts["up_tol"]      = float(up_tol)
        elif "dn_tol" in line:
            exec( "global dn_tol; "      + line )
            nml_opts["dn_tol"]      = float(dn_tol)
        elif "freq" in line:
            exec( "global freq; "        + line )
            nml_opts["freq"]        = float(freq)
            
    # Bogus fix
    if nml_opts["dp_temp"] >= 100:
        nml_opts["dp_temp"] = nml_error_dp_default
    if nml_opts["np_temp"] >= 100:
        nml_opts["np_temp"] = nml_error_np_default
            
    return nml_opts
    
def get_freq( ):
    # Only returns frequency
    return read_nl( )["freq"]

## Maybe add a function to reset nl to default values

if __name__ == "__main__":
    print( read_nl() )