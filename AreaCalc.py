import clr

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

clr.AddReference('RevitAPIUI')
from Autodesk.Revit.UI import TaskDialog

clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager

doc = DocumentManager.Instance.CurrentDBDocument

areaSchemes = IN[0]
methods = IN[1]
if not isinstance(methods, list):
    methods = [methods]
for num, method in enumerate(methods):
    if not method:
        methods[num] = "A"
    elif method not in ["A", "B"]:
        methods[num] = "B"

if not isinstance(areaSchemes, list):
    areaSchemes = [areaSchemes]

outList = []

class areaCalcArea():
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
        self.SectionEndRow = None
    def ByRevitArea(self, method, revitArea):
        self.Name = revitArea.GetParameters("Name")[0].AsString()
        self.Number = revitArea.Number.ToString()
        self.Area = round(revitArea.Area, 2)
        self.Level = revitArea.Level.Name
        self.AreaType = revitArea.GetParameters("Area Calc")[0].AsString()

        # Check for major verticals
        if self.AreaType == "Major Vertical Penetration":
            self.Exclusion = self.Area
            self.Name = "MAJOR VERTICAL PENETRATION"
            self.Sort = 3
        # Check for exclusions
        elif (self.AreaType == "Storage" or
            self.AreaType == "Occupant Storage Area" or
            self.AreaType == "Parking Area" or
            self.AreaType == "Parking" or
            self.AreaType == "Unenclosed Building Feature"):
            self.Exclusion = self.Area
            self.Sort = 2

        # Check for amenity space. We need to handle this differently per method
        elif self.AreaType == "Building Amenity Area":
            if method == "A":
                self.Amenity = self.Area
            else:
                self.Exclusion = self.Area

        # Check for building service areas. This is only required for Method A
        elif (method == "A" and self.AreaType == "Building Service Area"):
            self.BuildingService = self.Area

        # Check for tenant space
        elif (self.AreaType == "Tenant Area" or
            self.AreaType == "Occupant Area"):
            self.Tenant = self.Area
        elif (self.AreaType == "Tenant Ancillary Area"):
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
        if addArea.Amenity > 0:
            self.Amenity = self.Amenity + addArea.Amenity
        if addArea.BuildingService > 0:
            self.BuildingService = self.BuildingService + addArea.BuildingService
    def ItemizeCheck(self):
        if self.Area <= 0:
            return False
        elif (self.AreaType is "Total" or
            self.AreaType is "BLANK"):
            return True
        elif (self.Ancillary <= 0 and
             self.Tenant <= 0 and
             self.Exclusion <= 0 and
             self.Amenity <= 0 and
             self.BuildingService <= 0):
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
    def ZeroToDashes(self):
        if self.Exclusion <= 0:
            self.Exclusion = "--"
        if self.Tenant <= 0:
            self.Tenant = "--"
        if self.Ancillary <= 0:
            self.Ancillary = "--"
        if self.Circulation <= 0:
            self.Circulation = "--"
        if self.Amenity <= 0:
            self.Amenity = "--"
        if self.Tenant <= 0:
            self.Tenant = "--"

    def MakeRow(self, method, lastRow):
        if method == "A":
            if self.AreaType == "Total":
                rNum = self.RowNumber
                sNum = self.SectionStartRow
                return ["Floor Totals",                                                                      #A
                        self.Area,                                                                           #B
                        "=SUBTOTAL(9,C" + str(sNum)+ ":C" + str(rNum - 1) + ")",                             #C
                        "=B" + str(rNum) + "-C" + str(rNum),                                                 #D
                        "",                                                                                  #E
                        "=SUBTOTAL(9,F" + str(sNum) + ":F" + str(rNum - 1) + ")",                            #F
                        "=SUBTOTAL(9,G" + str(sNum) + ":G" + str(rNum - 1) + ")",                            #G
                        "=F" + str(rNum) + "+G" + str(rNum),                                                 #H
                        "=SUBTOTAL(9,I" + str(sNum) + ":I" + str(rNum - 1) + ")",                            #I
                        "=H" + str(rNum) + "+I" + str(rNum),                                                 #J
                        "=SUBTOTAL(9,K" + str(sNum) + ":K" + str(rNum - 1) + ")",                            #K
                        "=D" + str(rNum) + "-J" + str(rNum) + "-K" + str(rNum),                              #L
                        "=ROUND((J" + str(rNum) + "+L" + str(rNum) + ")/J" + str(rNum) + ",4)",              #M
                        "=ROUND(H" + str(rNum) + "*M" + str(rNum) + ",2)",                                   #N
                        "=ROUND(I" + str(rNum) + "*M" + str(rNum) + ",2)+K" + str(rNum),                     #O
                        "=ROUND(D$" + str(lastRow) + "/(D$" + str(lastRow) +  "-O$" + str(lastRow) + "),4)", #P
                        "=ROUND(N" + str(rNum) + "*P" + str(rNum) + ",2)",                                   #Q
                        "--"]                                                                                #R

            elif self.AreaType == "BLANK":
                row = []
                for i in range(18):
                    row.append("")
                return row

            else:
                self.ZeroToDashes()
                # TODO redo for method A. This is method b
                rNum = self.RowNumber
                eNum = self.SectionEndRow
                return [self.Level,                                                                                      #A
                        "",                                                                                              #B
                        self.Exclusion,                                                                                  #C
                        "",                                                                                              #D
                        self.Name,                                                                                       #E
                        self.Tenant,                                                                                     #F
                        self.Ancillary,                                                                                  #G
                        "=SUMIF(F" + str(rNum) + ":G" + str(rNum) + ",\">0\")",                                          #H
                        self.Amenity,                                                                                    #I
                        "=SUMIF(H" + str(rNum) + ":I" + str(rNum) + ",\">0\")",                                          #J
                        self.BuildingService,                                                                            #K
                        "",                                                                                              #L
                        "=ROUND((J$" + str(eNum) + "+L$" + str(eNum) + ")/J$" + str(eNum) + ", 4)",                      #M
                        "=IF(COUNTIF(H" + str(rNum) + ",\">0\"),ROUND(H" + str(rNum) + "*M" + str(rNum) + ",2),\"--\")", #N
                        "=IF(COUNTIF(I" + str(rNum) + ",\">0\"),ROUND(I" + str(rNum) + "*M" + str(rNum) + ",2),0)+IF(COUNTIF(K" + str(rNum) + ",\">0\"),K" + str(rNum) + ",0)", #O
                        "=ROUND(D$" + str(lastRow) + "/(D$" + str(lastRow) + "-O$" + str(lastRow) + "),4)",              #P
                        "=IF(COUNTIF(H" + str(rNum) + ",\">0\"),ROUND(N" + str(rNum) + "*P" + str(rNum) + ",2),\"--\")", #Q
                        "=IF(COUNTIF(Q" + str(rNum) + ",\">0\"),ROUND(Q" + str(rNum) + "/H" + str(rNum) + ",4),\"--\")"] #R

        elif method == "B":
            if self.AreaType == "Total":
                if self.Circulation <= 0:
                    circulation = ""
                else:
                    circulation = self.Circulation
                return ["Floor Totals",                                                                       #A
                        self.Area,                                                                            #B
                        "=SUBTOTAL(9,C" + str(self.SectionStartRow)+ ":C" + str(self.RowNumber - 1) + ")",    #C
                        "=B" + str(self.RowNumber) + "-C" + str(self.RowNumber),                              #D
                        "--",                                                                                 #E
                        "=SUBTOTAL(9,F" + str(self.SectionStartRow) + ":F" + str(self.RowNumber - 1) + ")",   #F
                        "=SUBTOTAL(9,G" + str(self.SectionStartRow) + ":G" + str(self.RowNumber - 1) + ")",   #G
                        "=SUBTOTAL(9,H" + str(self.SectionStartRow) + ":H" + str(self.RowNumber - 1) + ")",   #H
                        circulation,                                                                          #I
                        "=D" + str(self.RowNumber) + "-H" + str(self.RowNumber) + "-I" + str(self.RowNumber), #J
                        "=D$" + str(lastRow) + "/H$" + str(lastRow),                                          #K
                        "=H" + str(self.RowNumber) + "*K" + str(self.RowNumber)]                              #L

            elif self.AreaType == "BLANK":
                row = []
                for i in range(12):
                    row.append("")
                return row

            else:
                if self.Exclusion <= 0:
                    exclusion = "--"
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
        else:
            return False


    @staticmethod
    def Header(method):
        if method == "A":
            header = [["" for i in range(18)]]
            header.append(list("ABCDEFGHIJKLMNOPQR"))
            header.append(["Input",             #A
                           "Input",             #B
                           "Input & ID",        #C
                           "'= B - C",          #D
                           "Input",             #E
                           "Input & ID",        #F
                           "Input & ID",        #G
                           "'= F + G",          #H
                           "Input & ID",        #I
                           "'= H + I",          #J
                           "Input & ID",        #K
                           "'= D - J - K",      #L
                           "'= (J + L) / J",    #M
                           "'= H * M",          #N
                           "'= (I * M) + K",    #O
                           "'= ΣD / (ΣH - ΣO)", #P
                           "'= N * P",          #Q
                           "'= Q / H"])         #R
            header.append(["Floor Level",                     #A
                           "Boundary Area (IPMS 2)",          #B
                           "Rentable Exclusions",             #C
                           "Floor Rentable Area",             #D
                           "Space ID",                        #E
                           "Tenant Area (IPMS 3)",            #F
                           "Tenant Ancillary Area",           #G
                           "Occupant Area",                   #H
                           "Building Amenity Area",           #I
                           "Floor Usable Area",               #J
                           "Building Service Area",           #K
                           "Floor Service Area",              #L
                           "Floor Allocation Ratio",          #M
                           "Floor Allocation",                #N
                           "Building Service & Amenity Area", #O
                           "Builing Allocation Ratio",        #P
                           "Rentable Area",                   #Q
                           "Load Factor A"])                  #R
            header.append(["" for i in range(18)])

        elif method == "B":
            header = [["" for i in range(12)]]
            header.append(list("ABCDEFGHIJKL"))
            header.append(["Input",        #A
                           "Input",        #B
                           "Input & ID",   #C
                           "'= B - C",     #D
                           "Input",        #E
                           "Input & ID",   #F
                           "Input & ID",   #G
                           "'= F + G",     #H
                           "Input",        #I
                           "'= D - H - I", #J
                           "'= ΣD / ΣH",   #K
                           "'= H * K"])    #L
            header.append(["Floor Level",               #A
                           "Boundary Area (IPMS 2)",    #B
                           "Rentable Exclusions",       #C
                           "Floor Rentable Area",       #D
                           "Space ID",                  #E
                           "Tenant Area",               #F
                           "Tenant Ancillary Area",     #G
                           "Occupant Area",             #H
                           "Base Building Circulation", #I
                           "Service & Amenity Area",    #J
                           "Load Factor B",             #K
                           "Rentable Area"])            #L
            header.append(["" for i in range(12)])

        else:
            header = False
        return header

    @staticmethod
    def GrandTotal(method, firstRow, row):
        if method == "A":
            # blankRow = ["" for i in range(18)]
            totalRow = ["Building Totals (Σ)",                                                  #A
                        "=Sum(B" + str(firstRow) + ":B" + str(row - 1) + ")",                   #B
                        "=SUBTOTAL(9,C" + str(firstRow) + ":C" + str(row - 1) + ")",            #C
                        "=Sum(D" + str(firstRow) + ":D" + str(row - 1) + ")",                   #D
                        "",                                                                     #E
                        "=SUBTOTAL(9,F" + str(firstRow) + ":F" + str(row - 1) + ")",            #F
                        "=SUBTOTAL(9,G" + str(firstRow) + ":G" + str(row - 1) + ")",            #G
                        "=F" + str(row) + "+G" + str(row),                                      #H
                        "=SUBTOTAL(9, I" + str(firstRow) + ":I" + str(row - 1) + ")",           #I
                        "=H" + str(row) + "+I" + str(row),                                      #J
                        "=SUBTOTAL(9, K" + str(firstRow) + ":K" + str(row - 1) + ")",           #K
                        "=D" + str(row) + "-J" + str(row) + "-K" + str(row),                    #L
                        "=(J" + str(row) + "+L" + str(row) + ")/J" + str(row),                  #M
                        "=H" + str(row) + "*M" + str(row),                                      #N
                        "=ROUND(I" + str(row) + "*M" + str(row) + ",2)+K" + str(row),           #O
                        "=ROUND(D$" + str(row) + "/(D$" + str(row) + "-O$" + str(row) + "),4)", #P
                        "=ROUND(N" + str(row) + "*P" + str(row) + ",2)",                        #Q
                        "=ROUND(Q" + str(row) + "/H" + str(row) + ",4)"]                        #R
        elif method == "B":
            # blankRow = ["" for i in range(12)]
            totalRow = ["Building Totals (Σ)",                                       #A
                        "=Sum(B" + str(firstRow) + ":B" + str(row - 1) + ")",        #B
                        "=SUBTOTAL(9,C" + str(firstRow) + ":C" + str(row - 1) + ")", #C
                        "=Sum(D" + str(firstRow) + ":D" + str(row - 1) + ")",        #D
                        "",                                                          #E
                        "=SUBTOTAL(9,F" + str(firstRow) + ":F" + str(row - 1) + ")", #F
                        "=SUBTOTAL(9,G" + str(firstRow) + ":G" + str(row - 1) + ")", #G
                        "=F" + str(row) + "+G" + str(row),                           #H
                        "=Sum(I" + str(firstRow) + ":I" + str(row - 1) + ")",        #I
                        "=D" + str(row) + "-H" + str(row) + "-I" + str(row),         #J
                        "=D$" + str(row) + "/H$" + str(row),                         #K
                        "=H" + str(row) + "*K" + str(row)]                           #L
        else:
            # totalRow = False
            blankRow = False
        return [totalRow]

# Collect all areas in the model
filter = AreaFilter()
areas = FilteredElementCollector(doc).WherePasses(filter).ToElements()
levels = FilteredElementCollector(doc).OfClass(Level).ToElements()
levels = sorted(levels, key = lambda x: x.Elevation)
levels = [level.Name.ToString() for level in levels]

##!! Create the rows for the excel export !!##
# loop through area schemes
for areaScheme, method in zip(areaSchemes, methods):
    schemeAreas = []
    # get excel header and setup the row numbering
    schemeRows = areaCalcArea.Header(method)
    row = 6
    firstRow = row

    # loop through the levels
    for level in levels:
        # start building a list of area objects that we can later turn
        # into rows
        levelAreas = []
        # build a level total object
        levelTotal = areaCalcArea(level, "Total", level)
        # add a high sort number to place it at the end of the list later
        levelTotal.Sort = 4
        levelBlank = (areaCalcArea("", "BLANK", ""))
        levelBlank.Sort = 5

        # loop through all the areas
        for area in areas:
            # make sure the level matches the area scheme and level name
            if (area.AreaScheme.Name.ToString() == areaScheme
                and area.Level.Name.ToString() == level):
                try:
                    # create an area object for the matching area
                    parsedArea = areaCalcArea()
                    parsedArea.ByRevitArea(method, area)
                    # add it to the area total for the level
                    levelTotal.AddAreas(parsedArea)
                    levelBlank.AddAreas(parsedArea)
                    # add the matched area to the list of areas
                    levelAreas.append(parsedArea)
                except Exception as e:
                    schemeAreas.append(e)

        # add all the areas from the level to the list
        levelAreas.append(levelTotal)
        levelAreas.append(levelBlank)
        # create a dictionary of area names so we can merge areas
        areaNames = set([area.Name for area in levelAreas])
        areaNames = list(areaNames)
        joinedAreas = dict.fromkeys(areaNames)
        # loop through the diction area and merge any areas that
        # have the same name
        for name in joinedAreas.keys():
            for area in levelAreas:
                if name == area.Name:
                    if joinedAreas[name] is None:
                        joinedAreas[name] = area
                    else:
                        (joinedAreas[name]).AddAreas(area)
        # sort all the joined areas to get them in the order BOMA expects
        joinedAreas = sorted(joinedAreas.values(), key = lambda x: x.Name)
        joinedAreas.sort(key = lambda x: x.Sort)
        sectionStartRow = row
        # remove areas that don't get listed out
        itemizedAreas = []
        for num, area in enumerate(joinedAreas):
            areaIn = area.ItemizeCheck()
            if area.ItemizeCheck():
                itemizedAreas.append(area)
        for num, area in enumerate(itemizedAreas):
            (itemizedAreas[num]).RowNumber = row
            sectionEndRow = row - 1
            row = row + 1
            if area.AreaType == "Total":
                (itemizedAreas[num]).SectionStartRow = sectionStartRow
                sectionStartRow = row
        for num, area in enumerate(itemizedAreas):
            (itemizedAreas[num]).SectionEndRow = sectionEndRow
        schemeAreas.extend(itemizedAreas)
        #% End Level Loop %#

    # Go through all the collected areas and build the rows for the excel doc
    for area in schemeAreas:
        schemeRows.append(area.MakeRow(method, row))

    # add the grand total loop
    schemeRows.extend(areaCalcArea.GrandTotal(method, firstRow, row))
    outList.append(schemeRows)
#% End Scheme Loop %#
OUT = outList
