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

views = UnwrapElement(IN[0])
outList = []

for view in views:
    collected = []
    collection = FilteredElementCollector(doc, view.Id)
    collection = collection.WhereElementIsNotElementType()
    collection = collection.OfCategory(BuiltInCategory.OST_Viewers)
    # for element in collection:
    #     # collected.append(element.ToDSType(True))
    #     parameterId = BuiltInParameter.SECTION_PARENT_VIEW_NAME
    #     collected.append(element.GetParameter(parameterId))
    for element in collection:
        collected.append(element.ToDSType(True))
    outList.append(collected)


OUT = outList
