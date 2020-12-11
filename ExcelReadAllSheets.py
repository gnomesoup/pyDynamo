import clr

clr.AddReference('Microsoft.Office.Interop.Excel, Version=11.0.0.0, Culture=neutral, PublicKeyToken=71e9bce111e9429c')
from Microsoft.Office.Interop import Excel
from System.Runtime.InteropServices import Marshal

paths = IN[0]
if not isinstance(paths, list):
    paths = [paths]

outList = []

for path in paths:
    wsCollection = []
    try:
        # Instantiate the Excel Application
        ex = Excel.ApplicationClass()
        # Make it Visible for us all to see
        ex.Visible = False
        # Disable Alerts - Errors Ignore them, they're probably not important
        ex.DisplayAlerts = False
        # Workbook 
        workbook = ex.Workbooks.Open(path)
        # WorkSheet
        ws = workbook.Worksheets
        for sheet in ws:
            sheetCollection = []
            # Cell range
            rowCollection = None
            data = sheet.UsedRange
            for row in data.Rows:
                if rowCollection is None:
                    rowCollection = ["Department"]
                else:
                    rowCollection = [sheet.Name]
                allNull = True
                for column in row.Columns:
                    value = column.Value2
                    if value is not None:
                        allNull = False
                    rowCollection.append(column.Value2)
                if not allNull:
                    sheetCollection.append(rowCollection)
            Marshal.ReleaseComObject(sheet)
            if sheetCollection:
                wsCollection.append(sheetCollection)
        ex.ActiveWorkbook.Close(False)
        Marshal.ReleaseComObject(ws)
        Marshal.ReleaseComObject(workbook)
        Marshal.ReleaseComObject(ex)
    except Exception as e:
        wsCollection.append(e)
    outList.append(wsCollection)
OUT = outList
        
