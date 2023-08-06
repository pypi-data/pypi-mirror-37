##region Settings
import os
bWriteLog = True
sLogFile = os.path.join(__file__,'..','FRDLog.log')
##endregion
##region LogInit
import logging
FRDLog = logging.getLogger(__name__)
FRDLog.setLevel(logging.DEBUG)
try:
    os.remove(sLogFile)
except (PermissionError,FileNotFoundError):
    pass
if bWriteLog:
    bLogFileIsOpen = False
    try:
        os.rename(sLogFile,sLogFile)
    except PermissionError:
        bLogFileIsOpen = True
    except FileNotFoundError:
        pass
    if not bLogFileIsOpen:
        FRDLog.addHandler(logging.FileHandler(sLogFile))
##endregion
