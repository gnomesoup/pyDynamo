#Copyright(c) 2015, Konrad Sobon # @arch_laboratory, http://archi-lab.net
import clr
import sys
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

from System.Collections.Generic import *

# Import ToDSType(bool) extension method
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

# pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
# sys.path.append(pyt_path)
import re


#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

keySchedule = UnwrapElement(IN[0])
data = IN[1]
inputParams = IN[2]
upper = IN[3]

# "Start" the transaction
TransactionManager.Instance.EnsureInTransaction(doc)

tableData = keySchedule.GetTableData()
sectionData = tableData.GetSectionData(SectionType.Body)

currentRowCount = sectionData.NumberOfRows

n = 1
try:
    for row in data:
        if n > currentRowCount:
            sectionData.InsertRow(sectionData.LastRowNumber + 1)
        n = n + 1
except:
    pass

allKeys = FilteredElementCollector(doc).WhereElementIsNotElementType()
keyParams = []
outList = []

for key in allKeys:
    if key.OwnerViewId == keySchedule.Id:
        paramList = []
        for parameterName in inputParams:
            paramList.append(key.LookupParameter(str(parameterName)))
        keyParams.append(paramList)

try:
    for row, params in zip(data, keyParams):
        for value, param in zip(row, params):
            if isinstance(value, str):
                valueDecoded = value.decode('string_escape')
            else:
                valueDecoded = str(value).decode('string_escape')
            param.Set(valueDecoded)
except:
    pass

# "End" the transaction
TransactionManager.Instance.TransactionTaskDone()

# Assign your output to the OUT variable
OUT = outList
# public void CreateSubtitle(ViewSchedule schedule)
# {
#     TableData colTableData = schedule.GetTableData();

#     TableSectionData tsd = colTableData.GetSectionData(SectionType.Header);
#     tsd.InsertRow(tsd.FirstRowNumber + 1);
#     tsd.SetCellText(tsd.FirstRowNumber + 1, tsd.FirstColumnNumber, "Schedule of column top and base levels with offsets");
# }
