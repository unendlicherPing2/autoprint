import FreeCAD
import Part
import sys

# Open the FreeCAD document
doc = FreeCAD.openDocument("./internal/Biotop.FCStd")

# Access the VariableSet (assuming it's named "Variables")
varset = doc.getObject("VarSet")

# Change a variable in the VariableSet
varset.setExpression("Global_Diameter", sys.argv[2])  # Change "VariableName" and 50 to your desired variable and value

# Recompute the document
doc.recompute()

# Get the part to export (assuming it's named "Part")
floor = doc.getObject("Body")
body = doc.getObject("Body001")

# Export the part as STEP
Part.export([floor], "./static/temp/floor.step")
Part.export([body], "./static/temp/body.step")
