import clr

clr.AddReference('Microsoft.Office.Interop.Excel, Version=11.0.0.0, Culture=neutral, PublicKeyToken=71e9bce111e9429c')
from Microsoft.Office.Interop import Excel
from System.Runtime.InteropServices import Marshal
from System import Array

path = IN[0]

outList = []

# excel = Excel.ApplicationClass()
# excel.Visible = True
# excel.DisplayAlerts = False

# Open excel if not already running
excel = Marshal.GetActiveObject("Excel.Application")
# if excel is None:
#     excel = Excel.ApplicationClass()
# Make it Visiable for us all to see
# Disable Alerts - Errors Ignore them, they're probably not important
# Workbook
for workbook in excel.Workbooks:
    outList.append(workbook.FullName)
# workbook = excel.Workbooks.Open(path)
# # WorkSheet
# worksheet = workbook.Worksheets[1]
# i = 0
# # Cell range
# x1range = worksheet.Range["A1", "A4"]
# sheetName = IN[1]
# a = Array.CreateInstance(object, len(sheetName),1) # row and column

# while i < len(sheetName):
#     a[i,0] = sheetName[i]
#     i += 1

# x1range.Value2 = a

OUT = outList
