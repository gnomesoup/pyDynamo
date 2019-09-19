import clr

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

levels = UnwrapElement(IN[0])

outList = []

for level in levels:
    outList.append(level.Document.GetElement((level.FindAssociatedPlanViewId())))

OUT = outList
