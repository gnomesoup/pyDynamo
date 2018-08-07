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

parameterCategories = IN[1]
# Check if categories is a list
if not isinstance(parameterCategories, list):
    categories = [parameterCategories]

sharedParameterGroup = IN[2]

sharedParameterFile = IN[3]

outList = []


def dyCreateParameter(doc, parameterName, parameterCategories, parameterGroup, tempSharedParameterFile):
    ## Add a shared parameter if it doesn't exist otherwise
    ## Return true if succeeded
    ## Return false on fail
    try:
        app = doc.Application
        # tempSharedParamFile = "S:\\01 BIM\\Support\\WHA Shared Parameters.txt"
        # Set the parameter to shared file
        if tempSharedParameterFile:
            originalSharedParamFile = app.SharedParametersFilename
            app.SharedParametersFilename = tempSharedParamFile
        sharedParamFile = app.OpenSharedParameterFile()
        # Drill down to the group
        groupName = sharedParamFile.Groups.get_Item(parameterGroup)
        # Get shared parameter from group
        externalDefinition = groupName.Definitions.get_Item(parameterName)
        # categories = doc.Settings.Categories
        # category = categories.get_Item(BuiltInCategory.OST_ProjectInformation)
        TransactionManager.Instance.EnsureInTransaction(doc)
        categorySet = app.Create.NewCategorySet()
        for category in parameterCategories:
            categorySet.Insert(UnwrapElement(category))
        if doc.IsFamilyDocument:
            familyManager = doc.FamilyManager
            newParameter = familyManager.AddParameter(externalDefinition,
                                                      BuiltInParameterGroup.PG_GEOMETRY,
                                                      False)
        else:
            newInstanceBinding = app.Create.NewInstanceBinding(categorySet)
            newParameter = doc.ParameterBindings.Insert(externalDefinition,
                                    newInstanceBinding,
                                    BuiltInParameterGroup.PG_IDENTITY_DATA)
        if tempSharedParameterFile:
            app.SharedParametersFilename = originalSharedParamFile
        TransactionManager.Instance.TransactionTaskDone()
        return newParameter
    except Exception, e:
        return e

for name, categories in zip(parameterNames, parameterCategories):
    if not isinstance(categories, list):
        categories = [categories]
    newParameter = dyCreateParameter(doc, name, categories, sharedParameterGroup, sharedParameterFile)
    try:
        outList.append(newParameter.ToDSType(True))
    except:
        outList.append(newParameter.Definition.Name)

OUT = outList
