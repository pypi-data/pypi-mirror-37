##region Setttings
bPause = True
##endregion
##region Imports
import os
import FormatRosterData as FRD
import openpyxl
import TM_CommonPy as TM
import traceback
##endregion

def Main():
    vRoster = GetRoster('http://www.espn.com/mens-college-basketball/team/roster/_/id/84')
    print(TM.Narrate(vRoster))

try:
    Main()
except PermissionError:
    print("PERMISSION_ERROR\n\tI'd recommend to just try again.\n\tOtherwise, close all extra programs and then retry.")
    TM.DisplayDone()
except Exception as e:
    TM.DisplayException(e)
else:
    if bPause:
        TM.DisplayDone()
