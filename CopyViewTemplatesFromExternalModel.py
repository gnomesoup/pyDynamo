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

elementType = View
regex = IN[1]
run = IN[2]

outList = []

openOptions = OpenOptions()
openOptions.DetachFromCentralOption = DetachFromCentralOption.DetachAndPreserveWorksets

if run:
    for f in filePaths:
        if File.Exists(f):
            try:
                modelPath = ModelPathUtils.ConvertUserVisiblePathToModelPath(f)
                sourceDoc = app.OpenDocumentFile(modelPath, openOptions)
                collector = FilteredElementCollector(sourceDoc)
                elements = collector.OfClass(elementType)
                copyElementIds = []
                for element in elements:
                    if element.IsTemplate:
                        if re.search(regex, element.Name):
                            copyElementIds.append(element.Id)
                            outList.append(element.Name)
                TransactionManager.Instance.EnsureInTransaction(doc)
                copiedIds = ElementTransformUtils.CopyElements(sourceDoc, List[ElementId](copyElementIds), doc, Transform.Identity, CopyPasteOptions())
                TransactionManager.Instance.TransactionTaskDone()
                sourceDoc.Close(False)
            except Exception, exception:
                outList.append(exception)
        else:
            outList.append("File does not exist: " + f)
else:
    outList.append("Set run to \"true\"")



OUT = outList
