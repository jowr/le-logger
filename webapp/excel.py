import xlrd
import datetime
import numpy as np

from functions import isnat

class ExcelFile(object):
    class ExcelValueError(ValueError): pass
    class ExcelTypeError(TypeError): pass

    def __init__(self, file=None):
        self.reset()
        self._file = file

    def reset(self):
        self._file = None
        self._xlSheet = None
        self._time = None
        self._temperature = None
        self._humidity = None
        self._serial = None
        self._valid = None

    @property
    def file(self):
        """Get or set the data source by means of a file stream, requires the 
        file.read() method to be present in the passed object.
        """
        return self._file

    @file.setter
    def file(self, value):
        self.reset()
        self._file = value

    def time_datetime(self):
        """The time series as a list of the type datetime objects.
        """
        arr = [datetime.datetime.now()] * self.time.size
        for i in range(self.time.size):
            arr[i] = self.time[i].astype('O')
        return arr
        #return self._time

    @property
    def time(self):
        """The time series as a numpy array of the type datetime64.
        """
        return self._time[self._valid]

    @property
    def temperature(self):
        """The temperature as a numpy array, note that the logger 
        saves data in degrees Celsius and not Kelvin.
        """
        return self._temperature[self._valid]

    @property
    def humidity(self):
        """The humidity data as a numpy array, data is logged as
        relative humidity.
        """
        return self._humidity[self._valid]

    @property
    def serial(self):
        """The serial of the logger, extracted from the Excel sheet.
        """
        return self._serial

    #def is_xlsx(self, file):
    #    #use openpyxl?
    #    return file.filename.rsplit('.', 1)[1] in ['xlsx', 'xlsm', 'xltx', 'xltm']
    #def is_xls(self, file):
    #    return file.filename.rsplit('.', 1)[1] in ['xls']    

    def xlLoad(self,theSheet=0):
        if self._xlSheet is None:
            # Read the stream instead of passing the file name
            if self._file is not None:
                xlBook = xlrd.open_workbook(file_contents=self._file.read())
                self._xlSheet = xlBook.sheet_by_index(theSheet)
                self._xlData()
            else:
                raise ExcelValueError("No file stream available, set the file property.")

    def _xlData_datetime(self, row, col):
        #self.xlLoad()
        #xlType = self._xlSheet.cell_type(row, col)
        #if xlType == xlrd.XL_CELL_TEXT or xlType == xlrd.XL_CELL_DATE:
        string_var = unicode(self._xlSheet.cell_value(row, col))
        string_var = u'20' + string_var.replace(' ','T')
        string_var = string_var.replace('/','-')
        try:
            value = self._xlSheet.cell_value(row, col)
            if value != "NC":
                return np.datetime64(string_var)
            else:
                return np.datetime64('NAT')
        except Exception as e:
            return np.datetime64('NAT')
        #else:
        #    return np.datetime64('NAT')

    def _xlData_float(self, row, col):
        #self.xlLoad()
        #xlType = self._xlSheet.cell_type(row, col)
        #if xlType == xlrd.XL_CELL_NUMBER:
        try:
            value = self._xlSheet.cell_value(row, col)
            if value != "NC":
                return float(value)
            else:
                return np.NaN
        except Exception as e:
            return np.NaN
        #else:
        #    return np.NaN

    def _xlData(self):
        #self.xlLoad()
        self._serial = str(self._xlSheet.cell_value(9, 1))

        row_offset = 19
        rows = max(0,min(self._xlSheet.nrows,20000)-row_offset)
        arr = np.empty(rows)

        self._time = np.empty_like(arr, dtype='datetime64[s]')
        self._temperature = np.empty_like(arr)
        self._humidity = np.empty_like(arr)
        for i in range(rows):
            idx = row_offset+i
            self._time[i] = self._xlData_datetime(idx,1)
            self._temperature[i] = self._xlData_float(idx, 2)
            self._humidity[i] = self._xlData_float(idx, 3)
           
        #cells = self.xlSheet.col_slice(1,19,None)
        #res['info'] += 'Time values: ' + str(len(cells)) + '\n'
        #cells = self.xlSheet.col_slice(2,19,None)
        #res['info'] += 'Temperature values: ' + str(len(cells)) + '\n'
        #cells = self.xlSheet.col_slice(3,19,None)
        #res['info'] += 'Humidity values: ' + str(len(cells)) + '\n'

        #arr.fill(3)
        #self._valid = arr == (np.logical_not(isnat(self._time)) + np.isfinite(self._temperature) + np.isfinite(self._humidity))

        self._valid = np.ones_like(arr, dtype='bool')

        self._valid = np.logical_and(self._valid, np.logical_not(isnat(self._time)))
        self._valid = np.logical_and(self._valid, np.isfinite(self._temperature))
        self._valid = np.logical_and(self._valid, np.isfinite(self._humidity))

        #self._valid = np.logical_and(np.logical_not(isnat(self._time)), np.isfinite(self._temperature))
        #self._valid = np.logical_and(self._valid, np.isfinite(self._humidity))


    def xlInfo(self):
        self.xlLoad()
        res = 'Logger serial: ' + str(self._xlSheet.cell_value(9, 1)) + '\n'
        return res


#def get_col_num(s):
#    """integer from excel letters"""
#    rem = s[:-1]
#    if rem == "":
#        return ord(s) - 64
#    else:
#        return 26*get_col_num(s[:-1]) + ord(s[-1]) - 64



#def getNumeric(xlSheet,xlRow,xlCol,strict=True):
#    """Sheet object, row number, column number or letter"""
#    try:
#        xlIntCol = int(xlCol)
#    except:
#        xlIntCol = get_col_num(xlCol)
#    xlCol = xlIntCol
#    xlType = xlSheet.cell_type(xlRow, xlCol)
#    if xlType == xlrd.XL_CELL_EMPTY:
#        if strict: raise ValueError("An empty cell was found in cell {0:d}:{1:d}, that should not happen.".format(xlRow, xlCol))
#        else: value = None
#    elif xlType == xlrd.XL_CELL_TEXT:
#        if strict: raise ValueError("Text was found in cell {0:d}:{1:d}, that should not happen.".format(xlRow, xlCol))
#        else: value = None
#    elif xlType == xlrd.XL_CELL_NUMBER:
#        value = float(xlSheet.cell_value(xlRow, xlCol))
#    elif xlType == xlrd.XL_CELL_DATE:
#        if strict: raise ValueError("A date was found in cell {0:d}:{1:d}, that should not happen.".format(xlRow, xlCol))
#        else: value = xlrd.xldate_as_tuple(xlSheet.cell_value(xlRow, xlCol), xlSheet.datemode)
#    elif xlType == xlrd.XL_CELL_BOOLEAN:
#        if strict: raise ValueError("A boolean value was found in cell {0:d}:{1:d}, that should not happen.".format(xlRow, xlCol))
#        else: value = bool(xlSheet.cell_value(xlRow, xlCol))
#    else:
#        if strict: raise ValueError("An unknown cell type was found in cell {0:d}:{1:d}, that should not happen.".format(xlRow, xlCol))
#        value = float(xlSheet.cell_value(xlRow, xlCol))
#    return value


#def xlLoad(theFile,theSheet,theColumns,theHeaders):
#    xlBook = xlrd.open_workbook(theFile)
#    xlSheet = xlBook.sheet_by_index(theSheet)
#    data = []
#    for xlRow in range(min(xlSheet.nrows,32e3)):
#        row = []
#        if xlRow in theHeaders: continue
#        #for xlCol in range(min(xlSheet.ncols,3)):
#        for xlCol in theColumns: 
#            value = getNumeric(xlSheet,xlRow, xlCol)
#            row.append(value)
#        data.append(row)
#    return data 


#def xlImport(theFile,theSheet,cell_mapping):
#    """File path, sheet number and dict with database table fields and cell coordinates"""
#    xlBook = xlrd.open_workbook(theFile)
#    xlSheet = xlBook.sheet_by_index(theSheet)
#    data = {}
#    for cell in cell_mapping:
#        if cell is None or cell_mapping[cell] is None: continue
#        if len(str(cell)) < 1 or len(cell_mapping[cell]) != 2: continue
#        xlCol = get_col_num(cell_mapping[cell][0])-1
#        xlRow = cell_mapping[cell][1]-1
#        data[cell] = abs(getNumeric(xlSheet,xlRow,xlCol,strict=False))
#        if cell.startswith("f_p_"):
#            data[cell] = data[cell]/100.0
#    return data 
        
# 
# 
# 
# db[tablename].insert(**{fieldname:value})

#dataquery = (db.t_measurement.id > 0) # (db.t_measurement.f_datatable != None) #| (db.mytable.myfield > 'A')
#datarows = db(dataquery).select()
#datatables = []; datafiles = []; dataimport = []
#for row in datarows:
#    datatables.append(get_datatable(row))
#    datafiles.append(row.f_datafile)
#    
#    xlPath = os.path.join(request.folder,'uploads',row.f_datafile)
#    if not os.path.isfile(xlPath) or not row.f_import:
#        print "Skipping row "+str(row.id)
#        continue
#    print "Importing row "+str(row.id)
#    xlData = xlImport(xlPath,1,meas_mapping)
#    xlData["f_import"] = False
#    db.t_measurement[row.id] = xlData

    