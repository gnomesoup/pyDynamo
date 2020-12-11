import clr

clr.AddReference('Microsoft.Office.Interop.Excel, Version=11.0.0.0, Culture=neutral, PublicKeyToken=71e9bce111e9429c')
from Microsoft.Office.Interop import Excel
from System.Runtime.InteropServices import Marshal

paths = IN[0]
if not isinstance(paths, list):
    paths = [paths]

outList = []

for path in paths:
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
        for sheet in workbook.Worksheets
        ws = workbook.Worksheets
        # Cell range

        ex.ActiveWorkbook.Close(False)
        Marshal.ReleaseComObject(ws)
        Marshal.ReleaseComObject(workbook)
        Marshal.ReleaseComObject(ex)
        outList.append(ws)
    except Exception as e:
        outList.append(e)
        
