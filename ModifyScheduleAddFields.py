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

views = IN[0]
if not isinstance(views, list):
    views = [views]
views = UnwrapElement(views)

parameterNames = IN[1]
if not isinstance(parameterNames, list):
    parameterNames = [parameterNames]

outList = []

for view in views:
    try:
        fieldNames = []
        for parameterName in parameterNames:
            fields = view.Definition.GetSchedulableFields()
            for field in fields:
                if field.GetName(doc).ToString() == str(parameterName):
                    TransactionManager.Instance.EnsureInTransaction(doc)
                    view.Definition.AddField(field)
                    TransactionManager.Instance.TransactionTaskDone()
        outList.append(view)
    except Exception, e:
        outList.append(e)

OUT = outList
