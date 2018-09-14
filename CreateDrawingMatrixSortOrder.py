
defaultDisciplines = ["GENERAL",
                      "CIVIL",
                      "LANDSCAPE",
                      "ARCHITECTURE",
                      "STRUCTURE",
                      "MECHANICAL",
                      "ELECTRICAL",
                      "PLUMBING",
                      "FIRE PROTECTION",
                      "LOW VOLTAGE",
                      "TELECOMMUNICATIONS",
                      "SECURITY",
                      "KITCHEN",
                      "AUDIO/VISUAL"]

disciplines = IN[0]

if disciplines is None:
    disciplines = defaultDisciplines

if not isinstance(disciplines, list):
    disciplines = [disciplines]

formula = ""
formulaClose = ""
for i, discipline in enumerate(disciplines):
    formula = (formula +
               "if(and(not(Sort Order < " +
               str(i) +
               "), Sort Order < " +
               str(i+1) +
               "), \"" +
               discipline +
               "\", ")
    formulaClose = formulaClose + ")"
formula = formula + "\"!!Adjust formula for additional disciplines!!\"" + formulaClose

OUT = formula
print(formula)
