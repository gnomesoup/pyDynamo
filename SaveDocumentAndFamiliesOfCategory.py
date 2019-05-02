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

sourcePaths = IN[0]
if not isinstance(sourcePaths, list):
    sourcePaths = [sourcePaths]
filePaths = IN[1]
if not isinstance(filePaths, list):
    filePaths = [filePaths]
run = IN[2]

def SaveFamiliesOfCategory(doc, run):
    elements = []
    familyList = []
    docPath = doc.PathName
    docPath = re.findall(r"^.*\\", docPath)[0]
    saveAsOptions = SaveAsOptions()
    saveAsOptions.OverwriteExistingFile = True
    category = doc.ProjectInformation.LookupParameter("Author").AsString()
    if not category:
        return "No category set to Author parameter"
    else:
        categories = doc.Settings.Categories
        category = categories.get_Item(category)
    collector = FilteredElementCollector(doc).OfClass(Family)
    for family in collector:
        if family.FamilyCategoryId.ToString() == category.Id.ToString():
            elements.append(family)
    for element in elements:
        eName = element.Name
        famDirectory = docPath + category.Name + "\\"
        famPath = famDirectory + eName + ".rfa"
        famPathBackup = famDirectory + eName + ".0001.rfa"
        if run:
            if not Directory.Exists(famDirectory):
                Directory.CreateDirectory(famDirectory)
            if File.Exists(famPath):
                File.Delete(famPath)
            famDoc = doc.EditFamily(element)
            famDoc.SaveAs(famPath, saveAsOptions)
            famDoc.Close(False)
            familyList.append(famPath)
            if File.Exists(famPathBackup):
                File.Delete(famPathBackup)
        else:
            familyList.append(famPath)
    return familyList

projectList = []
familyLists = []
for sourcePath, filePath in zip(sourcePaths, filePaths):
    doc = False
    if File.Exists(sourcePath):
        try:
            openOptions = OpenOptions()
            openOptions.DetachFromCentralOption = DetachFromCentralOption.DetachAndDiscardWorksets
            openOptions.Audit = True
            saveAsOptions = SaveAsOptions()
            saveAsOptions.OverwriteExistingFile = True
            modelPath = ModelPathUtils.ConvertUserVisiblePathToModelPath(filePath)
            if run:
                doc = app.OpenDocumentFile(sourcePath, openOptions)
                doc.SaveAs(filePath, saveAsOptions)
            else:
                projectList.append(filePath)
                familyLists.append("Run not set")
                continue
        except exception, Exception:
            projectList.append(exception)
            continue
        if doc:
            projectList.append(doc.Title)
            try:
                familyList = SaveFamiliesOfCategory(doc, run)
                familyLists.append(familyList)
            except:
                familyLists.append("Family Export Failed")
            doc.Close(False)
        else:
            familyLists.append("No document available")
    else:
        projectList.append("File Does Not Exist")

OUT = [projectList, familyLists]
