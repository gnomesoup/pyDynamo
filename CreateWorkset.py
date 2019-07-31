import clr

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument

names = IN[0]
if not isinstance(names, list):
    names = [names]

outList = []

if doc.IsWorkshared:
    worksets = FilteredWorksetCollector(doc).OfKind(WorksetKind.UserWorkset)
    for workset in worksets:
        for name in names:
            TransactionManager.Instance.EnsureInTransaction(doc)
            try:
                if WorksetTable.IsWorksetNameUnique(doc, name):
                    newWorkset = Workset.Create(doc, name)
                    outList.append(newWorkset)
                else:
                    outList.append(workset)
            except Exception, e:
                outList.append(e)
            TransactionManager.Instance.TransactionTaskDone()
else:
    outList.append("Project is not workshared")
OUT = outList
