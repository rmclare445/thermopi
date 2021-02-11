def write_log( string ):
    with open("state.log", "a") as f:
        f.write( string + "\n" )
        f.close()