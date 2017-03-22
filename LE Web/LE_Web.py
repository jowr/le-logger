from __future__ import print_function
import io, os, sys


BASE_PATH = os.path.realpath(os.path.join(os.path.dirname(os.path.dirname(__file__)),'webapp'))
if BASE_PATH not in sys.path:
    sys.path = [BASE_PATH] + sys.path

if False:
    from excel import ExcelFile

    with io.open(os.path.join(BASE_PATH,'..','..','TempMon.data','20170321_LE02.xls'),'rb') as file:
        xlFile = ExcelFile(file)
        xlFile.xlLoad()
        #print(xlFile.xlInfo())
        print(xlFile.xlSerial())
        print(xlFile.xlData())

if True:
    from database import Campaign, DataSet
    from app import test_database
    test = test_database()
