import clr
import math

# Import ToDSType(bool) extension method
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

# Import geometry conversion extension methods
clr.ImportExtensions(Revit.GeometryConversion)

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

# Imports Ilists module into python
clr.AddReference("System")
from System.Collections.Generic import List as cList

# Ilist Application
# New_List = cList[ElementId]("elements")

# Standard areas for Current Document, Active UI and application
doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application
uidoc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument

if not isinstance(IN[0], list):
    curves = [IN[0]]
else:
    curves = IN[0]
curves = UnwrapElement(curves)

if not isinstance(IN[1], list):
    views = [IN[1]]
else:
    views = IN[1]
views = UnwrapElement(views)

if not isinstance(IN[2], list):
    planes = [IN[2]]
else:
    planes = IN[2]
planes = UnwrapElement(planes)

outList = []

def toXYZ(fPoint):
    return XYZ(fPoint.X, fPoint.Y, fPoint.Z)

TransactionManager.Instance.EnsureInTransaction(doc)

plane = planes[0]
view = views[0]
planeOrigin = plane.Origin
planeOriginXYZ = XYZ(planeOrigin.X, planeOrigin.Y, planeOrigin.Z)
planeNormal = plane.Normal
planeNormalXYZ = XYZ(planeNormal.X, planeNormal.Y, planeNormal.Z)
apiPlane = Plane.Create(Frame(XYZ(0,0,0), XYZ(1,0,0), XYZ(0,1,0), XYZ(0, 0, 1)))
sketchPlane = SketchPlane.Create(doc, apiPlane)

for curve in curves:
    try:
        curveType = (curve.GetType()).Name
        if curveType == "Line":
            startPoint = toXYZ(curve.StartPoint)
            endPoint = toXYZ(curve.EndPoint)
            newCurve = Line.CreateBound(startPoint, endPoint)
        elif curveType == "Arc":
            arcCenter = toXYZ(curve.CenterPoint)
            arcPlane = Plane.CreateByNormalAndOrigin(toXYZ(curve.Normal), arcCenter)
            arcRadius = curve.Radius
            angleStart = math.pi if curve.Normal.Z < 0 else 0
            arcStartAngle = angleStart + math.radians(curve.StartAngle)
            arcEndAngle = arcStartAngle + math.radians(curve.SweepAngle)
            newCurve = Arc.Create(arcPlane, arcRadius, arcStartAngle, arcEndAngle)
        else:
            continue
        areaLine = doc.Create.NewAreaBoundaryLine(sketchPlane, newCurve, view)
    except Exception, exception:
        areaLine = exception
    outList.append(areaLine)

TransactionManager.Instance.TransactionTaskDone()

OUT = outList
