import clr
import re
from System.IO import File, Directory, Path

clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

doc = DocumentManager.Instance.CurrentDBDocument
app = doc.Application

filePaths = IN[0]
if not isinstance(filePaths, list):
    filePaths = [filePaths]

outList = []
openOptions = OpenOptions()
openOptions.DetachFromCentralOption = DetachFromCentralOption.DetachAndPreserveWorksets
openOptions.Audit = True

tempPath = Path.GetTempPath()
tempFile = "c:/revitTemp.rvt"

for f in filePaths:
    if File.Exists(f):
        try:
            modelPath = ModelPathUtils.ConvertUserVisiblePathToModelPath(f)
            upgradeDoc = app.OpenDocumentFile(modelPath, openOptions)
            # upgradeDoc = DocumentManager.Instance.CurrentDBDocument
            # upgradeDoc.SaveAs()
            title = upgradeDoc.Title
            p = upgradeDoc.PathName
            upgradeDoc.Close()
            outList.append(title + p)
            # outList.append("Exists: " + f)
        except Exception, exception:
            outList.append(exception)
    else:
        outList.append("File does not exist: " + f)

# Directory.Delete(tempPath)

OUT = outList
