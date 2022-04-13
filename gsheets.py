import pygsheets
from write_log import dtg_htg
from info.keys import cspath

# Default Google Sheets file name
sheetname = 'log.state'
# Authorize Google API connection
try:
    gc = pygsheets.authorize(client_secret=cspath)
except:
    print( "Sheets auth failed!" )

def gsheet_entry( lt, temp, hum, stat ):
    # Send updated entry to Google Sheets
    dtg, htg = dtg_htg( lt )
    entry = [[dtg, htg, "%0.1f"%temp, "%02d"%hum, stat]]
    try:
        sh = gc.open(sheetname)
        wks = sh.sheet1
        wks.update_values('A2', entry)
    except Exception as e: print(e)

def gsheet_entries( ):
    # Send last 100 lines from log.state to Google Sheets
    entries = []
    with open( "logs/log.state", "r" ) as f:
        content = f.readlines()
    n = min( len(content), 100 )
    content = content[-n:]
    for entry in content:
        entries.append( entry[:-1].replace(" ","").split(',') )
    entries.reverse()
    try:
        sh = gc.open(sheetname)
        wks = sh.sheet1
        wks.update_values('A2', entries)
    except Exception as e: print(e)

if __name__ == "__main__":
    gsheet_entries( )
