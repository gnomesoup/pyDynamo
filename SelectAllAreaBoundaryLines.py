import clr

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument


if not isinstance(IN[0], list):
    views = [IN[0]]
else:
    views = IN[0]
views = UnwrapElement(views)

outList = []

for view in views:
    collector = FilteredElementCollector(doc, view.Id)
    collector = collector.WhereElementIsNotElementType()
    lines = collector.OfCategory(BuiltInCategory.OST_AreaSchemeLines).ToElementIds()
    outList = outList.append(lines)

OUT = outList
