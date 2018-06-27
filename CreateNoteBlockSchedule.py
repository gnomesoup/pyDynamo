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
app = doc.Application

viewNames = IN[0]
familySymbols = UnwrapElement(IN[1])
outList = []

# Get a list of the current views in the project
collector = FilteredElementCollector(doc)
filter = ElementCategoryFilter(BuiltInCategory.OST_Views)
views = collector.WherePasses(filter).WhereElementIsNotElementType().ToElements()

# Get id of ViewFamilyType
# collector = FilteredElementCollector(doc)
# viewTypes = collector.OfClass(ViewFamilyType).ToElements()
# for viewType in viewTypes:
#     if viewType.ToDSType(True).Name == "Schedule View":
#         scheduleId = viewType.Id

# Find out if the view already exists
# Make the view if no match it found
for viewName, familySymbol in zip(viewNames, familySymbols):
    matchedView = []
    for view in views:
        makeView = True
        if view.Name == view:
            matchedView = view
            break
    if matchedView:
        outList.append(matchedView)
    else:
        TransactionManager.Instance.EnsureInTransaction(doc)
        view = ViewSchedule.CreateNoteBlock(doc, familySymbol.Id)
        view.Name == viewName
        TransactionManager.Instance.TransactionTaskDone()
        outList.append(view)

OUT = outList
