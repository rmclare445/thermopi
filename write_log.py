def write_state( string ):
    with open("state.log", "a") as f:
        f.write( string + "\n" )

def write_err( entry, lt ):
    dtg = "%04d%02d%02d" % ( lt[0], lt[1], lt[2] )      # date time group
    htg = "%02d:%02d:%02d" % ( lt[3], lt[4], lt[5] )    # hour time group
    with open("log.err", "a") as f:
        f.write( "%s_%s - %s\n" % (dtg, htg, entry) )

def write_ops( stat, lt, temp ):
    dtg = "%04d%02d%02d" % ( lt[0], lt[1], lt[2] )      # date time group
    htg = "%02d:%02d:%02d" % ( lt[3], lt[4], lt[5] )    # hour time group
    entry = "Furnace on" if stat else "Furnace off"     # change of status entry
    with open("log.ops_%s" % dtg, "a") as f:
        f.write( "%s - %s, room temp %s\n" % (htg, entry, temp) )
