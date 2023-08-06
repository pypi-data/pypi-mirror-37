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
        iTotalErrorFileCount = 0
        for sFileName in os.listdir("../res/Input"):
            if sFileName.split(".")[-1] != "xlsx" or "~$" in sFileName or "template" in sFileName.lower():
                print("sFileName(IGNORED): "+sFileName)
                continue
            print("sFileName:"+sFileName)
            sFilePath = "../res/Input/"+sFileName
            #---Open file
            vWorkbook = openpyxl.load_workbook(sFilePath)
            vSheet = vWorkbook.active
            vNewWorkbook = openpyxl.Workbook()
            vNewSheet = vNewWorkbook.active
            #---Edit
            bSuccess = True
            bSuccess &= FRD.FormatName(vSheet,vNewSheet)
            bSuccess &= FRD.FormatHometown(vSheet,vNewSheet)
            bSuccess &= FRD.FormatHeight(vSheet,vNewSheet)
            if not "women" in sFileName.lower():
                bSuccess &= FRD.FormatWeight(vSheet,vNewSheet)
            bSuccess &= FRD.FormatSchoolyear(vSheet,vNewSheet)
            bSuccess &= FRD.AppendOldSheet(vSheet,vNewSheet)
            #---Save
            if not bSuccess:
                print("SaveName:"+sFileName.split(".")[0]+"_Reformatted(ERRORS).xlsx")
                vNewWorkbook.save(sFileName.split(".")[0]+"_Reformatted(ERRORS).xlsx")
                iTotalErrorFileCount += 1
            else:
                print("SaveName:"+sFileName.split(".")[0]+"_Reformatted.xlsx")
                vNewWorkbook.save(sFileName.split(".")[0]+"_Reformatted.xlsx")
    if iTotalErrorFileCount:
        print("TOTAL ERRORS`iTotalErrorFileCount:"+str(iTotalErrorFileCount))
    else:
        print("Success`iTotalErrorFileCount:"+str(iTotalErrorFileCount))

try:
    Main()
except PermissionError:
    print("PERMISSION_ERROR\n\tI'd recommend to just try again.\n\tOtherwise, close all extra programs and then retry.")
if bPause:
    TM.DisplayDone()
