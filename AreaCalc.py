import clr

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager

doc = DocumentManager.Instance.CurrentDBDocument

areaSchemes = IN[0]
if not isinstance(areaSchemes, list):
    areaSchemes = [areaSchemes]

outList = []

class areaCalcArea():
    # def __init__(self):
    def __init__(self,
                 name = "",
                 areaType = "",
                 level = "",
                 number = "",
                 area = 0):
        self.Name = name
        self.Number = number
        self.AreaType = areaType
        self.Level = level
        self.Area = area
        self.Exclusion = 0
        self.Tenant = 0
        self.Ancillary = 0
        self.Amenity = 0
        self.BuildingService = 0
        self.Circulation = 0
        self.Sort = 0
        self.RowNumber = None
        self.SectionStartRow = None
    def ByRevitArea(self, revitArea):
        self.Name = revitArea.GetParameters("Name")[0].AsString()
        self.Number = revitArea.Number.ToString()
        self.Area = round(revitArea.Area, 2)
        self.Level = revitArea.Level.Name
        self.AreaType = revitArea.GetParameters("Area Calc")[0].AsString()
        if self.AreaType == "Major Vertical Penetration":
            self.Exclusion = self.Area
            self.Name = "MAJOR VERTICAL PENETRATION"
            self.Sort = 3
        elif (self.AreaType == "Storage" or
            self.AreaType == "Occupant Storage Area" or
            self.AreaType == "Parking Area" or
            self.AreaType == "Parking" or
            self.AreaType == "Building Amenity Area" or
            self.AreaType == "Unenclosed Building Feature"):
            self.Exclusion = self.Area
            self.Sort = 2
        else:
            self.Exclusion = 0
        if (self.AreaType == "Tenant Area" or
            self.AreaType == "Occupant Area"):
            self.Tenant = self.Area
        else:
            self.Tenant = 0
        if (self.AreaType == "Tenant Ancillary Area"):
            self.Ancillary = self.Area
        else:
            self.Ancillary = 0
        if (self.AreaType == "Base Building Circulation" or
            self.AreaType == "Floor Service Area"):
            self.Circulation = self.Area
            self.Sort = 2
        else:
            self.Circulation = 0
    def AddAreas(self, addArea):
        if addArea.Area > 0:
            self.Area = self.Area + addArea.Area
        if addArea.Ancillary > 0:
            self.Ancillary = self.Ancillary + addArea.Ancillary
        if addArea.Tenant > 0:
            self.Tenant = self.Tenant + addArea.Tenant
        if addArea.Circulation > 0:
            self.Circulation = self.Circulation + addArea.Circulation
        if addArea.Exclusion > 0:
            self.Exclusion = self.Exclusion + addArea.Exclusion
    def ItemizeCheck(self):
        if (self.Area <= 0 or
            (self.Ancillary <= 0 and
             self.Tenant <= 0 and
             self.Exclusion <= 0 and
             self.AreaType != "Total")):
            return False
        else:
            return True
    def Itemize(self):
        return [self.RowNumber,
                self.Number,
                self.Name,
                self.AreaType,
                self.Area,
                self.Exclusion,
                self.Tenant,
                self.Ancillary,
                self.Circulation]
    def MakeRowMethodA(self, lastRow):
        if self.AreaType == "Total":
            if self.Circulation <= 0:
                circulation = ""
            else:
            return ["Floor Totals",
                    self.Area,
                    "=SUBTOTAL(9,C" + str(self.SectionStartRow)+ ":C" + str(self.RowNumber - 1) + ")",
                    "=B" + str(self.RowNumber) + "-C" + str(self.RowNumber),
                    "",
                    "=SUBTOTAL(9,F" + str(self.SectionStartRow) + ":F" + str(self.RowNumber - 1) + ")",
                    "=SUBTOTAL(9,G" + str(self.SectionStartRow) + ":G" + str(self.RowNumber - 1) + ")",
                    "=F" + str(self.RowNumber) + "+G" + str(self.RowNumber),
                    "=SUBTOTAL(9,I" + str(self.SectionStartRow) + ":I" + str(self.RowNumber - 1) + ")",
                    "=H" + str(self.RowNumber) + "+I" + str(self.RowNumber),
                    "=SUBTOTAL(9,K" + str(self.SectionStartRow) + ":K" + str(self.RowNumber - 1) + ")",
                    "=D" + str(self.RowNumber) + "-J" + str(self.RowNumber) + "-K" + str(self.RowNumber),
                    "=(J" + str(self.RowNumber) + "+L" + str(self.RowNumber) + ")/J" + str(lastRow),
                    "=H" + str(self.RowNumber) + "*M" + str(self.RowNumber),
                    "=(I" + str(self.RowNumber) + "*M" + str(self.RowNumber) + ")+K" + str(lastRow),
                    "=D$" + str(lastRow) + "/(D$" + str(lastRow) +  "-O$" + str(lastRow) + ")",
                    "=N" + str(self.RowNumber) + "*P" + str(self.RowNumber),
                    ""]
        else:
            if self.Exclusion <= 0:
                exclusion = ""
            else:
                exclusion = self.Exclusion
            if self.Tenant <= 0:
                tenant = ""
            else:
                tenant = self.Tenant
            if self.Ancillary <= 0:
                ancillary = ""
            else:
                ancillary = self.Ancillary
            if self.Circulation <= 0:
                circulation = ""
            else:
                circulation = self.Circulation
            if self.Amenity <= 0:
                amenity = ""
            else:
                amenity = self.Amenity

            return [self.Level,
                    "",
                    exclusion,
                    "",
                    self.Name,
                    tenant,
                    ancillary,
                    "=F" + str(self.RowNumber) + "+G" + str(self.RowNumber),
                    amenity,
                    "=H" + str(self.RowNumber) + "+I" + str(self.RowNumber),
                    "",
                    circulation,
                    "=D$" + str(lastRow) + "/H$" + str(lastRow),
                    "=H" + str(self.RowNumber) + "*K" + str(self.RowNumber)]
    def MakeRowMethodB(self, lastRow):
        if self.AreaType == "Total":
            if self.Circulation <= 0:
                circulation = ""
            else:
                circulation = self.Circulation
            return ["Floor Totals",
                    self.Area,
                    "=SUBTOTAL(9,C" + str(self.SectionStartRow)+ ":C" + str(self.RowNumber - 1) + ")",
                    "=B" + str(self.RowNumber) + "-C" + str(self.RowNumber),
                    "",
                    "=SUBTOTAL(9,F" + str(self.SectionStartRow) + ":F" + str(self.RowNumber - 1) + ")",
                    "=SUBTOTAL(9,G" + str(self.SectionStartRow) + ":G" + str(self.RowNumber - 1) + ")",
                    "=SUBTOTAL(9,H" + str(self.SectionStartRow) + ":H" + str(self.RowNumber - 1) + ")",
                    circulation,
                    "=D" + str(self.RowNumber) + "-H" + str(self.RowNumber) + "-I" + str(self.RowNumber),
                    "=D$" + str(lastRow) + "/H$" + str(lastRow),
                    "=H" + str(self.RowNumber) + "*K" + str(self.RowNumber)]
        else:
            if self.Exclusion <= 0:
                exclusion = ""
            else:
                exclusion = self.Exclusion
            if self.Tenant <= 0:
                tenant = ""
            else:
                tenant = self.Tenant
            if self.Ancillary <= 0:
                ancillary = ""
            else:
                ancillary = self.Ancillary

            return [self.Level,
                    "",
                    exclusion,
                    "",
                    self.Name,
                    tenant,
                    ancillary,
                    "=F" + str(self.RowNumber) + "+G" + str(self.RowNumber),
                    "",
                    "",
                    "=D$" + str(lastRow) + "/H$" + str(lastRow),
                    "=H" + str(self.RowNumber) + "*K" + str(self.RowNumber)]
    @staticmethod
    def HeaderMethodA():
        header = [list("ABCDEFGHIJKLMNOPQR")]
        header.append(["Input",
                       "Input",
                       "Input & ID",
                       "'= B - C",
                       "Input",
                       "Input & ID",
                       "Input & ID",
                       "'= F + G",
                       "Input & ID",
                       "'= H + I",
                       "Input & ID",
                       "'= D - J - K",
                       "'= (J + L) / J",
                       "'= H * M",
                       "'= (I * M) + K"
                       "'= ΣD / (ΣH - ΣO)",
                       "'= N * P",
                       "'= Q / H"])
        header.append(["Floor Level",
                       "Boundary Area (IPMS 2)",
                       "Rentable Exclusions",
                       "Floor Rentable Area",
                       "Space ID",
                       "Tenant Area (IPMS 3)",
                       "Tenant Ancillary Area",
                       "Occupant Area",
                       "Building Amenity Area",
                       "Floor Usable Area",
                       "Building Service Area",
                       "Floor Service Area",
                       "Floor Allocation Ratio",
                       "Floor Allocation",
                       "Building Service & Amenity Area",
                       "Builing Allocation Ratio",
                       "Rentable Area",
                       "Load Factor A"])
        return header
    @staticmethod
    def HeaderMethodB():
        header = [list("ABCDEFGHIJKL")]
        header.append(["Input",
                       "Input",
                       "Input & ID",
                       "'= B - C",
                       "Input",
                       "Input & ID",
                       "Input & ID",
                       "'= F + G",
                       "Input",
                       "'= D - H - I",
                       "'= ΣD / ΣH",
                       "'= H * K"])
        header.append(["Floor Level",
                      "Boundary Area (IPMS 2)",
                      "Rentable Exclusions",
                      "Floor Rentable Area",
                      "Space ID",
                      "Tenant Area",
                      "Tenant Ancillary Area",
                      "Occupant Area",
                      "Base Building Circulation",
                      "Service & Amenity Area",
                      "Load Factor B",
                      "Rentable Area"])
        return header

filter = AreaFilter()
areas = FilteredElementCollector(doc).WherePasses(filter).ToElements()
levels = FilteredElementCollector(doc).OfClass(Level).ToElements()
levels = sorted(levels, key = lambda x: x.Elevation)
levels = [level.Name.ToString() for level in levels]

for areaScheme in areaSchemes:
    schemeAreas = []
    schemeRows = areaCalcArea.HeaderMethodB()
    row = 4
    firstRow = row
    for level in levels:
        levelAreas = []
        levelTotal = areaCalcArea(level, "Total", level)
        levelTotal.Sort = 4
        for area in areas:
            if (area.AreaScheme.Name.ToString() == areaScheme
                and area.Level.Name.ToString() == level):
                try:
                    parsedArea = areaCalcArea()
                    parsedArea.ByRevitArea(area)
                    levelTotal.AddAreas(parsedArea)
                    levelAreas.append(parsedArea)
                except Exception, e:
                    schemeAreas.append(e)
        levelAreas.append(levelTotal)
        areaNames = set([area.Name for area in levelAreas])
        areaNames = list(areaNames)
        joinedAreas = dict.fromkeys(areaNames)
        for name in joinedAreas.keys():
            for area in levelAreas:
                if name == area.Name:
                    if joinedAreas[name] is None:
                        joinedAreas[name] = area
                    else:
                        (joinedAreas[name]).AddAreas(area)
        joinedAreas = sorted(joinedAreas.values(), key = lambda x: x.Name)
        joinedAreas.sort(key = lambda x: x.Sort)
        sectionStartRow = row
        for area in joinedAreas:
            if area.ItemizeCheck():
                area.RowNumber = row
                row = row + 1
                if area.AreaType == "Total":
                    area.SectionStartRow = sectionStartRow
                    sectionStartRow = row
                schemeAreas.append(area)
    for area in schemeAreas:
        schemeRows.append(area.MakeRowMethodB(row))
    schemeRows.append(["Building Totals (Σ)",
                       "=Sum(B" + str(firstRow) + ":B" + str(row - 1) + ")",
                       "=SUBTOTAL(9,C" + str(firstRow) + ":C" + str(row - 1) + ")",
                       "=Sum(D" + str(firstRow) + ":D" + str(row - 1) + ")",
                       "",
                       "=SUBTOTAL(9,F" + str(firstRow) + ":F" + str(row - 1) + ")",
                       "=SUBTOTAL(9,G" + str(firstRow) + ":G" + str(row - 1) + ")",
                       "=F" + str(row) + "+G" + str(row),
                       "=Sum(I" + str(firstRow) + ":I" + str(row - 1) + ")",
                       "=D" + str(row) + "-H" + str(row) + "-I" + str(row),
                       "=D$" + str(row) + "/H$" + str(row),
                       "=H" + str(row) + "*K" + str(row)])
    outList.append(schemeRows)
OUT = outList
