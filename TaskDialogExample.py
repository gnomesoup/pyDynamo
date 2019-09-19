import clr

clr.AddReference('RevitAPIUI')
from Autodesk.Revit.UI import TaskDialog

run = IN[0]
if isinstance(run, list):
    run = run[0]

outList = []
if run:
    title = "Title"
    message = "Message"
    TaskDialog.Show(title, message)
    outList.append(message)
else:
    outList.append("Run set to false")

OUT = outList
