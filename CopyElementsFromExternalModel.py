import clr
import re
from System.IO import File, Directory, Path

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

clr.AddReference("System")
from System.Collections.Generic import List

doc = DocumentManager.Instance.CurrentDBDocument
app = doc.Application

filePaths = IN[0]
if not isinstance(filePaths, list):
    filePaths = [filePaths]

elementTypes = IN[1]
if not isinstance(elementTypes, list):
    elementTypes = [elementTypes]
parameterNames = IN[2]
if not isinstance(parameterNames, list):
    parameterNames = [parameterNames]
regexs = IN[3]
if not isinstance(regexs, list):
    regexs = [regexs]
run = IN[4]

outList = []

openOptions = OpenOptions()
openOptions.DetachFromCentralOption = DetachFromCentralOption.DetachAndPreserveWorksets

if run:
    for f in filePaths:
        if File.Exists(f):
            modelPath = ModelPathUtils.ConvertUserVisiblePathToModelPath(f)
            sourceDoc = app.OpenDocumentFile(modelPath, openOptions)
            for elementType, parameterName, regex in zip(elementTypes, parameterNames, regexs):
                collector = FilteredElementCollector(sourceDoc)
                try:
                    elements = collector.OfClass(elementType)
                    copyElementIds = []
                    for element in elements:
                        if parameterName:
                            elementParameter = element.LookupParameter(parameterName)
                            if elementParameter is not None:
                                if re.search(regex, elementParameter.AsString()):
                                    copyElementIds.append(element.Id)
                        else:
                            copyElementIds.append(element.Id)
                    TransactionManager.Instance.EnsureInTransaction(doc)
                    copiedIds = ElementTransformUtils.CopyElements(sourceDoc, List[ElementId](copyElementIds), doc, None, CopyPasteOptions())
                    TransactionManager.Instance.TransactionTaskDone()
                    copiedElements = []
                    for copiedId in copiedIds:
                        copiedElements.append(doc.GetElement(copiedId))
                    outList.append(copiedElements)
                    # outList.append(copiedElements)
                except Exception, exception:
                    outList.append(copyElementIds)
            # sourceDoc.Close(False)
        else:
            outList.append("File does not exist: " + f)
else:
    outList.append("Set run to \"true\"")

OUT = outList
