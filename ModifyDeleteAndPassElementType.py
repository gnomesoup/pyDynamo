import clr
import sys

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument
app = doc.Application

elements = UnwrapElement(IN[0])
deleteCheck = IN[1]
familyTypes = []
dList = []
eList = []

# go through the work of deleting passed elements
TransactionManager.Instance.EnsureInTransaction(doc)
for element in elements:
    try:
        elementId = element.Id
        if deleteCheck:
            listAdd = True
            # get the type ID of the element
            elementType = doc.GetElement(element.GetTypeId())
            # get a list of unique family types to pass along
            for familyType in familyTypes:
                if familyType.Id == elementType.Id:
                    listAdd = False
            if listAdd:
                familyTypes.append(elementType)
            # actually delete the element
            doc.Delete(elementId)
            # add the id of the deleted element to the out list
            dList.append(elementId)
        else:
            # if we aren't deleting elements pass the whole element
            eList.append(element)
    except:
        #if deleting fails pass the whole element
        eList.append(element)
TransactionManager.Instance.TransactionTaskDone()

# OUT[0] = list of unique family types
# OUT[1] = list of element IDs that were deleted
# OUT[2] = undeleted elements
OUT = [familyTypes, dList, eList]
