import clr
import re
from System.IO import File

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.AddReference('RevitNodes')
import Revit
clr.ImportExtensions(Revit.Elements)

doc = DocumentManager.Instance.CurrentDBDocument
app = doc.Application

docPath = doc.PathName
docPath = re.findall(r"^.*\\", docPath)[0]

categories = IN[0]
if not isinstance(categories, list):
    categories = [categories]
saveBool = IN[1]
elements = []
outList = []

collector = FilteredElementCollector(doc).OfClass(Family)
for family in collector:
    for category in categories:
        if family.FamilyCategoryId.ToString() == category.Id.ToString():
            elements.append(family)

for element in elements:
    eName = element.Name
    famPath = docPath + eName + ".rfa"
    if saveBool:
        try:
            if File.Exists(famPath):
                File.Delete(famPath)
            famDoc = doc.EditFamily(element)
            famDoc.SaveAs(famPath)
            famDoc.Close(True)
            outList.append(famPath)
        except Exception, exception:
            outList.append(eName + ": " + str(exception))
    else:
        outList.append("Test: " + famPath)

OUT = outList
