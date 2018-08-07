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

views = UnwrapElement(IN[0])
elementList = UnwrapElement(IN[1])

outList = []

for view, elements in zip(views, elementList):
    hiddenList = []
    for element in elements:
        hidden = element.IsHidden(view)
        category = element.Category
        while (not hidden) and (category is not None):
            try:
                hidden = not category.get_Visible(view)
                category = category.Parent
            except:
                category = None
        hiddenList.append(hidden)
    outList.append(hiddenList)

OUT = outList
