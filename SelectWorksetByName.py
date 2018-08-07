import clr

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager

doc = DocumentManager.Instance.CurrentDBDocument

names = IN[0]
if not isinstance(names, list):
    names = [names]
outList = []
nameList = []
idList = []

worksets = FilteredWorksetCollector(doc)
worksets = worksets.OfKind(WorksetKind.UserWorkset)

if doc.IsWorkshared:
    for workset in worksets:
        for name in names:
            if workset.Name.ToString() == name:
                try:
                    outList.append(workset.ToDSType(True))
                except:
                    outList.append(workset)
                nameList.append(workset.Name.ToString())
                idList.append(workset.Id)
else:
    outList.append("Project is not workshared")

OUT = [outList, nameList, idList]
