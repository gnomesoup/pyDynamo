import clr

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager

# clr.AddReference("RevitNodes")
# import Revit
# clr.ImportExtensions(Revit.Elements)

doc = DocumentManager.Instance.CurrentDBDocument

families = FilteredElementCollector(doc).OfClass(Family).ToElements()

desiredCategories = [
"Generic Annotations",
"Spot Elevation Symbols",
"View Reference",
"Span Direction Symbol",
"Structural Beam System Tags",
"Structural Framing Tags",
"Windows",
"Stair Landing Tags",
"Stair Run Tags",
"Stair Support Tags",
"Stair Tags",
"Division Profiles",
"Supports",
"Callout Heads",
"Elevation Marks",
"Level Heads",
"Grid Heads",
"Revision Cloud Tags",
"Door Tags",
"Wall Tags",
"Specialty Equipment Tags",
"Railing Tags",
"Section Marks",
"Material Tags",
"Plumbing Fixture Tags",
"Ceiling Tags",
"Title Blocks",
"View Titles",
"Generic Model Tags",
"Room Tags",
"Area Tags",
"Keynote Tags",
"Lighting Fixture Tags"
]

familyCategories = []
userFamilies = []
for family in families:
    if family.IsUserCreated:
        if family.FamilyCategory.Name.ToString() in desiredCategories:
            userFamilies.append(family)
            familyCategories.append(family.FamilyCategory.Name)

OUT = [userFamilies, familyCategories]
