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
    elements = [IN[0]]
else:
    elements = IN[0]
elements = UnwrapElement(elements)

outList = []

for element in elements:
    try:
        areaScheme = element.AreaScheme
    except Exception, exception:
        areaScheme = exception
    outList.append(areaScheme)

OUT = outList
