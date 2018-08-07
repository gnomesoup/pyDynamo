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

phases = FilteredElementCollector(doc)
phases = phases.OfClass(Phase)

for phase in phases:
    for name in names:
        if phase.Name == name:
            outList.append(phase)
            nameList.append(phase.Name)

OUT = [outList, nameList]
