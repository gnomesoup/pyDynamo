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

def createWorkset(doc, name, isVisible = True):
    try:
        TransactionManager.Instance.EnsureInTransaction(doc)
        worksetTable = doc.GetWorksetTable()
        if worksetTable.IsWorksetNameUnique(doc, name):
            newWorkset = Workset.Create(doc, name)
            if not isVisible:
                defaultVisibility = WorksetDefaultVisibilitySettings.GetWorksetDefaultVisibilitySettings(doc)
                defaultVisibility.SetWorksetVisibility(newWorkset.Id, False)
            TransactionManager.Instance.TransactionTaskDone()
            return newWorkset.Name
    except Exception, e:
        return e

## Workset Setup

errorList = []
outNames = []
outId = []
outList = []

worksetTable = doc.GetWorksetTable()

if doc.IsWorkshared:
    worksets = FilteredWorksetCollector(doc).OfKind(WorksetKind.UserWorkset)
    for workset in worksets:
        try:
            TransactionManager.Instance.EnsureInTransaction(doc)
            if workset.Name.ToString() == "Workset1":
                worksetTable.RenameWorkset(doc, workset.Id, "WHA General")
                outList.append(workset.Name)
            else:
                outList.append(workset.Name)
            TransactionManager.Instance.TransactionTaskDone()
        except Exception, e:
            errorList.append(e)

    outList.append(createWorkset(doc, "Shared Levels and Grids"))
    outList.append(createWorkset(doc, "Hidden - Legend"))
    outList.append(createWorkset(doc, "Hidden - Egress", False))
    outList.append(createWorkset(doc, "Hidden - Links"))

else:
    errorList.append("Project is not workshared")

OUT = [outList, errorList]
