import xlrd

class ExcelFile():
    class ExcelValueError(ValueError): pass  # base exception class
    class ExcelTypeError(TypeError): pass

    def xlLoad(self,theFile,theSheet=0):
        xlBook = xlrd.open_workbook(theFile)
        xlSheet = xlBook.sheet_by_index(theSheet)
        return xlSheet

    def xlSerial(self,theFile):
        xlSheet = self.xlLoad(theFile,theSheet=0)
        return xlSheet.cell_value(10, 2)



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

    