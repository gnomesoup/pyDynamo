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
if not isinstance(viewNames, list):
    viewNames = [viewNames]

families = IN[1]
if not isinstance(families, list):
    families = [families]
families = UnwrapElement(families)

outList = []

# Get a list of the current views in the project
collector = FilteredElementCollector(doc)
filter = ElementCategoryFilter(BuiltInCategory.OST_Views)
views = collector.WherePasses(filter).WhereElementIsNotElementType().ToElements()

# Find out if the view already exists
# Make the view if no match it found
for viewName, family in zip(viewNames, families):
    matchedView = []
    for view in views:
        makeView = True
        if view.Name == view:
            matchedView = view
            break
    if matchedView:
        outList.append(matchedView)
    else:
        try:
            TransactionManager.Instance.EnsureInTransaction(doc)
            view = ViewSchedule.CreateNoteBlock(doc, family.Id)
            view.Name == viewName
            TransactionManager.Instance.TransactionTaskDone()
            outList.append(view)
        except Exception, e:
            outList.append(e)

OUT = outList
