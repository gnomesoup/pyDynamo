import clr

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager

clr.AddReference('RevitNodes')
import Revit
clr.ImportExtensions(Revit.Elements)

doc = DocumentManager.Instance.CurrentDBDocument
elementList = UnwrapElement(IN[0])
phase = UnwrapElement(IN[1])

outList = []

for element in elementList:
    try:
        room = element.get_FromRoom(phase)
        outList.append(room)
    except Exception, e:
        outList.append(e)
    # try:
    #     room = room.ToDSType(True)
    #     outList.append(room)
    # except Exception, e:
    #     outList.append(e)


OUT = outList
