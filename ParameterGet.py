import clr
import System

from System.Collections.Generic import *

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.AddReference('RevitAPIUI')
from Autodesk.Revit.UI import *
from Autodesk.Revit import Creation

doc = DocumentManager.Instance.CurrentDBDocument
uidoc = DocumentManager.Instance.CurrentUIDocument
app = doc.Application

tempFile = IN[0]
category = IN[1]

builtInCategory = System.Enum.ToObject(BuiltInCategory, category.Id)
cats = app.Create.NewCategorySet()
cats.Insert(doc.Settings.Categories.get_Item(builtInCategory))

originalFile = app.SharedParametersFilename
app.SharedParametersFilename = tempFile
sharedParameterFile = app.OpenSharedParameterFile()

GroupName = sharedParameterFile.Groups.get_Item("DYNAMO AND ADD-IN")
externalDefinition = GroupName.Definitions.get_Item("GROUP 1")

TransactionManager.Instance.EnsureInTransaction(doc)
newInstanceBinding = app.Create.NewInstanceBinding(cats)
doc.ParameterBindings.Insert(externalDefinition, newInstanceBinding, BuiltInParameterGroup.PG_TEXT)
TransactionManager.Instance.TransactionTaskDone()

app.SharedParametersFilename = originalFile