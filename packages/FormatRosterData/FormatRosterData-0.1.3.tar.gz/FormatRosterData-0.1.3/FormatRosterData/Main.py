##region Setttings
sFileName = "ExampleStart.xlsx"
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
    with TM.WorkspaceContext("Output",bCDInto=True,bPreDelete=True):
        iTotalErrorCount = 0
        for sFileName in os.listdir("../res/Unformatted"):
            if sFileName.split(".")[-1] != "xlsx" or "~$" in sFileName or "template" in sFileName.lower():
                print("sFileName(IGNORED): "+sFileName)
                continue
            print("sFileName:"+sFileName)
            sFilePath = "../res/Unformatted/"+sFileName
            #---Open file
            vWorkbook = openpyxl.load_workbook(sFilePath)
            vSheet = vWorkbook.active
            vNewWorkbook = openpyxl.Workbook()
            vNewSheet = vNewWorkbook.active
            #---Edit
            bSuccess = True
            bSuccess &= FRD.SplitName(vSheet,vNewSheet)
            bSuccess &= FRD.SplitTown(vSheet,vNewSheet)
            bSuccess &= FRD.TranslateHeight(vSheet,vNewSheet)
            if not "women" in sFileName.lower():
                bSuccess &= FRD.GetWeight(vSheet,vNewSheet)
            bSuccess &= FRD.GetSchoolyear(vSheet,vNewSheet)
            bSuccess &= FRD.AppendOldSheet(vSheet,vNewSheet)
            #---Save
            if not bSuccess:
                print("SaveName:"+sFileName.split(".")[0]+"_Reformatted(ERRORS).xlsx")
                vNewWorkbook.save(sFileName.split(".")[0]+"_Reformatted(ERRORS).xlsx")
                iTotalErrorCount += 1
            else:
                print("SaveName:"+sFileName.split(".")[0]+"_Reformatted.xlsx")
                vNewWorkbook.save(sFileName.split(".")[0]+"_Reformatted.xlsx")
    if iTotalErrorCount:
        print("TOTAL ERRORS`iTotalErrorCount:"+str(iTotalErrorCount))
    else:
        print("Success`iTotalErrorCount:"+str(iTotalErrorCount))

try:
    Main()
except PermissionError:
    print("PERMISSION_ERROR\n\tI'd recommend to just try again.\n\tOtherwise, close all extra programs and then retry.")
if bPause:
    TM.DisplayDone()
