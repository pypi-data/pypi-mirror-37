##region Setttings
bPause = True
sURL = 'http://www.espn.com/mens-college-basketball/team/roster/_/id/120' #'http://www.espn.com/mens-college-basketball/team/roster/'
##endregion
##region Imports
import os
import FormatRosterData as FRD
import openpyxl
import TM_CommonPy as TM
import traceback
import lxml.html
import requests
##endregion

def DigForText(vElem):
    for i in range(15):
        if not vElem.text is None:
            break;
        vElem = vElem[0]
    else:
        return ""
    return vElem.text

def Main():
    #vWorkbook = FRD.GetWorkbook(sURL)
    #sTitle = FRD.GetTitle(sURL)
    #vWorkbook.save("ScrapedData_"+sTitle+".xlsx")
    FRD.GetDict_NameToURL(sURL)
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
