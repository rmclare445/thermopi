import os
from info.keys import cspath
try:
    import pygsheets
except ImportError:
    print("Could not import pygsheets!")

# Default Google Sheets file
sheetname = 'log.state'

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

def write_state( temp, hum, stat, lt, gsheet ):
    # Write to continuous state log
    dtg, htg = dtg_htg( lt )
    entry = "%s, %s, %0.1f, %02d, %s\n" % (dtg, htg, temp, hum, stat)
    with open("logs/log.state", "a") as f:
        f.write( entry )
    if gsheet:
        try:
            gc = pygsheets.authorize(client_secret=cspath)
            sh = gc.open(sheetname)
            wks = sh.sheet1
            wks.update_values('A2', [[dtg, htg, "%0.1f"%temp, "%02d"%hum, stat]])
        except Exception as e:
            print( "pygsheet error!" )
            print( e )

def write_ops( lt, status=None, T=None, bulletin=None ):
    dtg, htg = dtg_htg( lt )
    if bulletin is not None:
        entry = bulletin
    else:
        entry = "Furnace on, " if status else "Furnace off, "
        entry = entry + "room temp %0.1f" % T
    with open("logs/log.ops_%s" % dtg, "a") as f:
        f.write( "%s - %s\n" % (htg, entry) )
