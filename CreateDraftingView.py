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


# The inputs to this node will be stored as a list in the IN variables.
viewNames = IN[0]
# Make the input a list if it isn't already
if not isinstance(viewNames, list):
	viewNames = [viewNames]

viewScales = IN[1]
if not isinstance(viewScales, list):
    viewScales = [viewScales] * len(viewNames)

# Assign the view to a browser folder if the project supports it
browserFolderParameterName = IN[2]
if isinstance(browserFolderParameterName, list):
    browserFolderParameterName = browserFolderParameterName[0]

browserFolderNames = IN[3]
if not isinstance(browserFolderNames, list):
    browserFolderNames = [browserFolderNames] * len(viewNames)
outList = []

# Get a list of the current views in the project
collector = FilteredElementCollector(doc)
filter = ElementCategoryFilter(BuiltInCategory.OST_Views)
views = collector.WherePasses(filter).WhereElementIsNotElementType().ToElements()

# Get id of ViewFamilyType
collector = FilteredElementCollector(doc)
viewTypes = collector.OfClass(ViewFamilyType).ToElements()
for viewType in viewTypes:
	if viewType.ToDSType(True).Name == "Drafting View":
		draftingId = viewType.Id

# Go through the list of views to look for a match
# Make the view if no match is found
for viewName, viewScale, browserFolderName in zip(viewNames, viewScales, browserFolderNames):
	matchedView = []
	for view in views:
		makeView = True
		if view.Name == viewName:
			matchedView = view
			break
	if matchedView:
		outList.append(matchedView)
	else:
		TransactionManager.Instance.EnsureInTransaction(doc)
		view = ViewDrafting.Create(doc, draftingId)
		view.Name = viewName
		view.Scale = viewScale
        if browserFolderParameterName:
		    parameter = view.LookupParameter(browserFolderParameterName)
		    if parameter:
			    parameter.Set(browserFolderName)
		TransactionManager.Instance.TransactionTaskDone()
		outList.append(view)

OUT = outList
