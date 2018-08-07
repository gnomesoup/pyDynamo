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

elements = UnwrapElement(IN[0])
outList = []

for element in elements:
    outList.append(element.LookupParameter("HostId"))
    # collected = []
    # collection = FilteredElementCollector(doc, view.Id)
    # collection = collection.WhereElementIsNotElementType()
    # for element in collection:
    #     collected.append(element.ToDSType(True))
    # outList.append(collected)


OUT = outList
