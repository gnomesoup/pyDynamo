import clr
import re
from System.IO import File, Directory

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
outList = []

collector = FilteredElementCollector(doc).OfClass(Family)
for category in categories:
    elements = []
    for family in collector:
        if family.FamilyCategoryId.ToString() == category.Id.ToString():
            elements.append(family)

    famDirectory = docPath + category.Name + "\\"
    if saveBool:
        if not Directory.Exists(famDirectory):
            Directory.CreateDirectory(famDirectory)

    for element in elements:
        eName = element.Name
        famPath = famDirectory + eName + ".rfa"
        famPathBackup = famDirectory + eName + ".0001.rfa"
        if saveBool:
            try:
                if not Directory.Exists(famDirectory):
                    Directory.CreateDirectory(famDirectory)
            except:
                outList.append("Could not create directory")
            try:
                if File.Exists(famPath):
                    File.Delete(famPath)
                famDoc = doc.EditFamily(element)
                famDoc.SaveAs(famPath)
                famDoc.Close(False)
                outList.append(famPath)
                if File.Exists(famPathBackup):
                    File.Delete(famPathBackup)
            except:
                outList.append("Export Error: " + eName)
        else:
            outList.append("Test: " + famPath)

OUT = outList
