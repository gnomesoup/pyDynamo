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

elementType = IN[1]
regex = IN[2]

outList = []

openOptions = OpenOptions()
openOptions.DetachFromCentralOption = DetachFromCentralOption.DetachAndPreserveWorksets

for f in filePaths:
    if File.Exists(f):
        try:
            modelPath = ModelPathUtils.ConvertUserVisiblePathToModelPath(f)
            sourceDoc = app.OpenDocumentFile(modelPath, openOptions)
            collector = FilteredElementCollector(sourceDoc)
            elements = collector.OfClass(elementType)
            copyElementIds = []
            for element in elements:
                # if re.search(regex, element.Name):
                if re.match(regex, element.LookupParameter("Type Name").AsString()):
                    # outList.append(element)
                    copyElementIds.append(element.Id)
        except Exception, exception:
            outList.append(exception)
        try:
            TransactionManager.Instance.EnsureInTransaction(doc)
            ElementTransformUtils.CopyElements(sourceDoc, List[ElementId](copyElementIds), doc, None, CopyPasteOptions())
            TransactionManager.Instance.TransactionTaskDone()
            sourceDoc.Close(False)
        except Exception, exception:
            outList.append(exception)
    else:
        outList.append("File does not exist: " + f)

OUT = outList
