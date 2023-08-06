##region ImportThisModule
from FormatRosterData.Misc import *
from FormatRosterData.FormatData import *
from FormatRosterData.WebsiteScraping import *
##endregion

import warnings
warnings.simplefilter('always')
def custom_formatwarning(msg, *args, **kwargs):
    # ignore everything except the message
    return str(msg) + '\n'
warnings.formatwarning = custom_formatwarning
