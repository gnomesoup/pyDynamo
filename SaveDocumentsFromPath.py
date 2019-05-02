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
run = IN[1]

outList = []
openOptions = OpenOptions()
# openOptions.DetachFromCentralOption = DetachFromCentralOption.DetachAndPreserveWorksets
openOptions.DetachFromCentralOption = DetachFromCentralOption.DetachAndDiscardWorksets
openOptions.Audit = True
saveAsOptions = SaveAsOptions()
saveAsOptions.OverwriteExistingFile = True

for f in filePaths:
    if File.Exists(f):
        try:
            modelPath = ModelPathUtils.ConvertUserVisiblePathToModelPath(f)
            if run:
                upgradeDoc = app.OpenDocumentFile(modelPath, openOptions)
                # upgradeDoc = DocumentManager.Instance.CurrentDBDocument
                title = upgradeDoc.Title
                p = upgradeDoc.PathName
                if p != f:
                    upgradeDoc.SaveAs(f, saveAsOptions)
                    p = upgradeDoc.PathName
                    upgradeDoc.Close(False)
                else:
                    upgradeDoc.Close()
                outList.append(p)
            else:
                outList.append(modelPath)
                # outList.append("Exists: " + f)
        except Exception, exception:
            outList.append(exception)
    else:
        outList.append("File does not exist: " + f)

# Directory.Delete(tempPath)


OUT = outList
