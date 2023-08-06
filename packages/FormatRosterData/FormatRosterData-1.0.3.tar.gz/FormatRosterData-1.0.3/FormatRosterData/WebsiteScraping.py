import os
import openpyxl
import TM_CommonPy as TM
import requests

def GetRoster(sURL):
    page = requests.get(sURL)
    return page
