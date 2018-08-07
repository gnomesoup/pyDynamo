import clr
import sys
import re

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

clr.AddReference('RevitAPIUI')
from Autodesk.Revit.UI import *

clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

doc = DocumentManager.Instance.CurrentDBDocument
app = DocumentManager.Instance.CurrentUIApplication.Application

# Create an empty element id to assign to a material
# Doing so will make the material <By Category>
emptyElementId = ElementId(-1)

# Get the elements from the node
elements = IN[0]

# Placeholder for returned values
outList = []

# Start a transaction to make changes to the model
TransactionManager.Instance.EnsureInTransaction(doc)

# Go through all the elements passed in
# Get the parameters, make sure they are material parameters
# Get all the parameters that don't have to do with glass or glazing
# Set the element Id of the parameter to -1 to make it <By Category>
for element in UnwrapElement(elements):
    parameters = element.GetOrderedParameters()
    error = ""
    for parameter in parameters:
        if (parameter.Definition.ParameterType.ToString() == "Material"):
            matId = parameter.AsElementId()
            mat = doc.GetElement(matId)
            if (mat and not re.search("glass|glazing", mat.Name, re.IGNORECASE)):
                try:
                    parameter.Set(emptyElementId)
                except Exception, exception:
                    error = exception
    if error:
        outList.append(element.Name + ": " + error)
    else:
        outList.append(element)

# Complete our transaction
TransactionManager.Instance.TransactionTaskDone()

OUT = outList
