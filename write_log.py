import os

# Make logs directory
try:
    os.mkdir('logs')
except:
    pass

# Remove previous system logs on startup
try:
    os.remove("logs/log.stdout")
    os.remove("logs/log.stderr")
except:
    pass

def dtg_htg( lt ):
    dtg = "%04d%02d%02d" % ( lt[0], lt[1], lt[2] )      # date time group
    htg = "%02d:%02d:%02d" % ( lt[3], lt[4], lt[5] )    # hour time group
    return dtg, htg

def write_state( temp, hum, stat, lt ):
    # Write to continuous state log and publish current reading
    dtg, htg = dtg_htg( lt )
    entry = "%s, %s, %0.1f, %02d, %s\n" % (dtg, htg, temp, hum, stat)
    with open("logs/log.state", "a") as f:
        f.write( entry )
    with open("logs/log.now", "w") as f:
        f.write( entry )

def write_ops( lt, status=None, T=None, bulletin=None ):
    dtg, htg = dtg_htg( lt )
    if bulletin is not None:
        entry = bulletin
    else:
        entry = "Furnace on, " if status else "Furnace off, "
        entry = entry + "room temp %0.1f" % T
    with open("logs/log.ops_%s" % dtg, "a") as f:
        f.write( "%s - %s\n" % (htg, entry) )
