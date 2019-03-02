import sys

def readInfo(varFile, conFile):
    varFile = open(varFile, "r")
    conFile = open(conFile, "r")
    
    varDict = {}
    varLines = varFile.readLines()
    varFile.close()
    for line in varLines:
        vals = line.split()
        varDict[vals[0][0]] = vals[1:len(vals)]

    constraints = conFile.readLines()
    conFile.close()
    for i in range(len(constraints)):
        constraints[i] = constraints[i].split()

    return varDict, constraints

def solveConstraints(varDict, constraints, varAssignments, fc):
    
    varToAssign = getVariable(varAssignments, varDict, constraints)
    while len(varDict[varToAssign]) > 0:
        varAssignments[varToAssign], newVarDict = getValue(varAssignments, copy(varDict), varToAssign, constraints)

        solved = True

        if fc:
            varDict = newVarDict
            for key in newVarDict:
                if len(varDict[key]) == 0:
                    solved = False

        if solved:
            for constraint in constraints:
                var1 = constraint[0]
                op = constraint[1]
                var2 = constraint[2]
                if var1 in assignedVars and var2 in assignedVars:
                    if op == '<':
                        if varAssignments[var1] >= varAssignments[var2]:
                            solved = False
                            break
                    elif op == '=':
                        if varAssignments[var1] != varAssignments[var2]:
                            solved = False
                            break
                    elif op == '>':
                        if varAssignments[var1] <= varAssignments[var2]:
                            solved = False
                            break
                    else:
                        if varAssignments[var1] == varAssignments[var2]:
                            solved = False
                            break
                    
        if not solved:
            toPrint = str(path) + ". "
            for var in assignedVars:
                toPrint += var + "=" + varAssignment[var] + ", "
            toPrint = toPrint[:len(toPrint)-2] + "  failure"
            print toPrint
            varDict[var].remove(varAssignments[varToAssign])
            assignedVars.remove(varToAssign)
            del varAssignments[varToAssign]
            return varDict
        elif len(varAssignments) == len(varDict):
            toPrint = str(path) + ". "
            for var in assignedVars:
                toPrint += var + "=" + varAssignment[var] + ", "
            toPrint = toPrint[:len(toPrint)-2] + "  solution"
            print toPrint
            return True
        else:
            varDict = solveConstraints(copy(varDict), constraints, copy(varAssignments), fc)
            if varDict == True:
                return True

path = 1
params = sys.argv
varDict, constraints = readInfo(params[1], params[2])
solveConstraints(varDict, constraints, {}, params[3] == "fc")
