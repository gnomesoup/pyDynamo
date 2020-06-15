import clr

clr.AddReference("RevitAPI")
from Autodesk.Revit import DB

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

if not isinstance(IN[0], list):
    areas = [IN[0]]
else:
    areas = IN[0]
areas = UnwrapElement(areas)

outList = []
for area in areas:
    boundaries = area.GetBoundarySegments(DB.SpatialElementBoundaryOptions())
    bOut = []
    for bGroup in boundaries:
        bOut.append([(b.GetCurve()).ToProtoType() for b in bGroup])
    outList.append(bOut)
OUT = outList