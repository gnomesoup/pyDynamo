import clr

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument

phases = IN[0]
if not isinstance(phases, list):
    phases = [phases]
phases = UnwrapElement(phases)
outList = []

for phase in phases:
    phaseId = phase.Id
    collector = FilteredElementCollector(doc)
    provider = ParameterValueProvider(ElementId(BuiltInParameter.PHASE_CREATED))
    evaluator = FilterNumericEquals()
    rule = FilterElementIdRule(provider, evaluator, phaseId)
    parameterFilter = ElementParameterFilter(rule)
    elements = collector.WherePasses(parameterFilter)
    elementList = []
    for element in elements:
        try:
            elementList.append(element.ToDSType())
        except:
            elementList.append(element)
    outList.append(elementList)

OUT = outList
