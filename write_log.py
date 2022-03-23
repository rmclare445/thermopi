def dtg_htg( lt ):
    dtg = "%04d%02d%02d" % ( lt[0], lt[1], lt[2] )      # date time group
    htg = "%02d:%02d:%02d" % ( lt[3], lt[4], lt[5] )    # hour time group
    return dtg, htg

def write_state( temp, hum, stat, lt ):
    dtg, htg = dtg_htg( lt )
    entry = "%s, %s, %0.1f, %02d, %s\n" % (dtg, htg, temp, hum, stat)
    with open("log.state", "a") as f:
        f.write( entry )

def write_err( entry, lt ):
    dtg, htg = dtg_htg( lt )
    with open("log.err", "a") as f:
        f.write( "%s, %s - %s\n" % (dtg, htg, entry) )

def write_ops( stat, lt, temp ):
    dtg, htg = dtg_htg( lt )
    entry = "Furnace on" if stat else "Furnace off"     # change of status entry
    with open("log.ops_%s" % dtg, "a") as f:
        f.write( "%s - %s, room temp %0.1f\n" % (htg, entry, temp) )
