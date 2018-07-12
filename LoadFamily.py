import clr

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

family = clr.Reference[Family]()

filePaths = IN[0]
if not isinstance(filePaths, list):
    filePaths = [filePaths]
loadBool = IN[1]
outList = []

# Ensure loaded families can overwrite existing families.
class FamilyOptions(IFamilyLoadOptions):
	def OnFamilyFound(self, familyInUse, overwriteParameterValues):
		overwriteParameterValues = True
		return True
	def OnSharedFamilyFound(self, sharedFamily, familyInUse, source, overwriteParameterValues):
		overwriteParameterValues = True
		return True

if loadBool:
    TransactionManager.Instance.EnsureInTransaction(doc)
    for filePath in filePaths:
        try:
            doc.LoadFamily(filePath, FamilyOptions(), family)
            outList.append(family)
        except:
            outList.append("Fail")
    TransactionManager.Instance.TransactionTaskDone()
else:
    outList = filePaths

OUT = outList
