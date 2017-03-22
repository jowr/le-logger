import xlrd
import numpy as np

from functions import isnat

class ExcelFile():
    class ExcelValueError(ValueError): pass  # base exception class
    class ExcelTypeError(TypeError): pass

    def __init__(self, file):
        self.file = file

    #def is_xlsx(self, file):
    #    #use openpyxl?
    #    return file.filename.rsplit('.', 1)[1] in ['xlsx', 'xlsm', 'xltx', 'xltm']
    #def is_xls(self, file):
    #    return file.filename.rsplit('.', 1)[1] in ['xls']    

    def xlLoad(self,theSheet=0):
        # Read the stream instead of passing the file name
        xlBook = xlrd.open_workbook(file_contents=self.file.read())
        self.xlSheet = xlBook.sheet_by_index(theSheet)
        #return xlSheet

    def xlInfo(self):
        res = 'Logger serial: ' + str(self.xlSheet.cell_value(9, 1)) + '\n'
        return res

    def xlSerial(self):
        return str(self.xlSheet.cell_value(9, 1))

    def xlData_datetime(self, row, col):
        xlType = self.xlSheet.cell_type(row, col)
        if xlType == xlrd.XL_CELL_TEXT or xlType == xlrd.XL_CELL_DATE:
            string_var = unicode(self.xlSheet.cell_value(row, col))
            string_var = u'20' + string_var.replace(' ','T')
            string_var = string_var.replace('/','-')
            try:
                return np.datetime64(string_var)
            except Exception as e:
                return np.datetime64('NAT')
        else:
            return np.datetime64('NAT')

    def xlData_float(self, row, col):
        xlType = self.xlSheet.cell_type(row, col)
        if xlType == xlrd.XL_CELL_NUMBER:
            try:
                return float(self.xlSheet.cell_value(row, col))
            except Exception as e:
                return np.NaN
        else:
            return np.NaN

    def xlData(self):
        row_offset = 19
        rows = max(0,min(self.xlSheet.nrows,25000)-row_offset)
        arr = np.empty(rows)
        res = dict(info='', time=np.empty_like(arr, dtype='datetime64[s]'), temperature=np.empty_like(arr), humidity=np.empty_like(arr))
        for i in range(rows):
            idx = row_offset+i
            res['time'][i] = self.xlData_datetime(idx,1)
            res['temperature'][i] = self.xlData_float(idx, 2)
            res['humidity'][i] = self.xlData_float(idx, 3)
           
        #cells = self.xlSheet.col_slice(1,19,None)
        #res['info'] += 'Time values: ' + str(len(cells)) + '\n'
        #cells = self.xlSheet.col_slice(2,19,None)
        #res['info'] += 'Temperature values: ' + str(len(cells)) + '\n'
        #cells = self.xlSheet.col_slice(3,19,None)
        #res['info'] += 'Humidity values: ' + str(len(cells)) + '\n'
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

    