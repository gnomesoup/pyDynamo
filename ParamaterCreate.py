# Enable Python support and load DesignScript library
import clr

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument
app = doc.Application


parameterNames = IN[0]
# Check if parameterNames is a list
if not isinstance(parameterNames, list):
    parameterNames = [parameterNames]

categories = IN[0]
# Check if categories is a list
if not isinstance(categories, list):
    categories = [categories]

outList = []

def dySetParameter(parameter, parameterValue):
    ## Set the value of a parameter and return true.
    ## Return false if it fails.
    try:
        TransactionManager.Instance.EnsureInTransaction(doc)
        parameter.Set(parameterValue)
        TransactionManager.Instance.TransactionTaskDone()
        return True
    except:
        return False

def dyCreateParameter(doc, parameterName):
    ## Add a shared parameter if it doesn't exist otherwise
    ## Return true if succeeded
    ## Return false on fail
    try:
        app = doc.Application
        tempSharedParamFile = "S:\\01 BIM\\Support\\WHA Shared Parameters.txt"
        # Set the parameter to shared file
        originalSharedParamFile = app.SharedParametersFilename
        app.SharedParametersFilename = tempSharedParamFile
        sharedParamFile = app.OpenSharedParameterFile()
        # Drill down to the group
        groupName = sharedParamFile.Groups.get_Item("Project Information")
        # Get shared parameter from group
        externalDefinition = groupName.Definitions.get_Item(parameterName)
        categories = doc.Settings.Categories
        category = categories.get_Item(BuiltInCategory.OST_ProjectInformation)
        TransactionManager.Instance.EnsureInTransaction(doc)
        categorySet = app.Create.NewCategorySet()
        categorySet.Insert(category)
        newInstanceBinding = app.Create.NewInstanceBinding(categorySet)
        doc.ParameterBindings.Insert(externalDefinition,
                                    newInstanceBinding,
                                    BuiltInParameterGroup.PG_IDENTITY_DATA)
        app.SharedParametersFilename = tempSharedParamFile
        TransactionManager.Instance.TransactionTaskDone()
        return True
    except:
        return False


for element in UnwrapElement(elements):
    try:
        # Find if parameter exists
        parameter = element.LookupParameter(parameterName)
        if not parameter:
            # Create the parameter
            dyCreateParameter(doc, parameterName)
            parameter = element.LookupParameter(parameterName)
        # Get the value of the parameter
        parameterValue = parameter.AsString()
        if not parameterValue or parameterUpdate:
            parameterValue = filePath
            dySetParameter(parameter, parameterValue)
        pList.append(parameterValue)
    except:
        pList.append("Error")
    eList.append(element)
# Place your code below this line

# Assign your output to the OUT variable.
OUT = pList
