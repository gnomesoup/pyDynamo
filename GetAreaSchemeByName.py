import clr

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager

doc = DocumentManager.Instance.CurrentDBDocument

if not isinstance(IN[0], list):
    names = [IN[0]]
else:
    names = IN[0]
names = UnwrapElement(names)

areaSchemes = FilteredElementCollector(doc)
areaSchemes = areaSchemes.OfClass(AreaSchemes)

outList = []
for name in names:
    for scheme in areaSchemes:
        if scheme.Name == name:
            outList.append(scheme)

OUT = outList
