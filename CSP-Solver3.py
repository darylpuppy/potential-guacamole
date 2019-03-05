import sys


# find least constraining value
# the one that rules out the fewest values in the remaining variables
# varAssignment: dict type, variables and their assigned values
# varToAssign: this is the variable we are trying to find a value for it

def getValue(varAssignments, varDict, varToAssign, constraints):

    # so... try each possible values to this variable
    
    # based on constraints, remove some of the values of varToAssign

    candidateValues = findCandidateValues(varAssignments, varDict, varToAssign, constraints)
    
    dictKeys = varDict.keys()
    assignedVars = varAssignments.keys()
    unassignedVars = list(set(dictKeys)-set(assignedVars))


    # now choose which of these values?
    # actually assign it,

    newVarAssignments = varAssignments
    
    dictNumberOfAllRemainingValues = {}
    # after assigning a possible value to a variable
    # add all values still possible to the rest of the variables

    for val in candidateValues:
        
        dictNumberOfAllRemainingValues[val] = 0
        newVarAssignments[varToAssign] = val # assign it

        for var in unassignedVars:
            dictNumberOfAllRemainingValues[val] += len(findCandidateValues(newVarAssignments, varDict, var, constraints))

        newVarAssignments = varAssignments # clear the assignment

    
    return max(dictNumberOfAllRemainingValues, key = dictNumberOfAllRemainingValues.get)
        
        
        
        


def findCandidateValues(varAssignments, varDict, varToAssign, constraints):
    assignedVars = varAssignments.keys()
    candidateValues = varDict[varToAssign]
    for constraint in constraints:
        if constraint[0] == varToAssign and constraint[2] in assignedVars:
                
                for val in candidateValues:
                    
                    if not compare(val, constraint[1], varAssignments[constraint[2]]):
                        candidateValues.remove(val)

        elif constraint[2] == varToAssign and constraint[0] in assignedVars:
                
                for val in candidateValues:
                    
                    if not compare(varAssignments[constraint[0]], constraint[1], val):
                        candidateValues.remove(val)

    return candidateValues
    


# returns the variable to assign a value to, based on the heuristics
# varAssignments was passed by solveConstraint(), dict type
# presumably the variables and their values up to this point 

def getVariable (varAssignments, varDict, constraints):

    candidateVariables = findMostConstrainedVariables(varAssignments, varDict, constraints)
    # this function returns a list of "most constrained variables"
    # it is a list because there may be a tie, or there may be just one variable

    if len(candidateVariables) == 1:
        return candidateVariables[0]

    else:
        # break ties by choosing the most constraining variable on the rest of the variables.
        # how to find the most constraining variable??????
        return findMostConstrainingVariable(candidateVariables, varAssignments, varDict, constraints)
    
    
    
        
def findMostConstrainingVariable(candidateVariables, varAssignments, varDict, constraints):
    # count how many time does this variable appear in the constraints?????

    # candidateVariables
    assignedVars = varAssignments.keys()

    dictNumberOfConstraints = {}
    # initiate dict, key: 0

    for var in candidateVariables:
        dictNumberOfConstraints[var] = 0
    

    for var in candidateVariables:
        for constraint in constraints:
            if constraint[0] == var or constraint[2] == var:
                if not constraint[0] in assignedVars and not constraint[2] in assignedVars:
                    dictNumberOfConstraints[var] += 1
                    
        

    # return the variable with the max value in dictNumberOfConstraints
    # and it should be the first one, so it is breaking ties by alphabetical order 
    return max(dictNumberOfConstraints, key = dictNumberofConstraints.get)
    
       

def findMostConstrainedVariables(varAssignments, varDict, constraints):
    # variable with the fewest legal values
    
    # get unassigned variables

    dictKeys = varDict.keys()
    assignedVars = varAssignments.keys()
    unassignedVars = list(set(dictKeys)-set(assignedVars))

    
    # create a dict of unassigned variables, and their possible domains
    newDict = {}
    for var in unassignedVars:
        newDict[var] = varDict[var] # just copy some of the varDict


    # based on constraints, remove some of the values in newDict
    for var in newDict:
        domains = newDict[var]
        for constraint in constraints:
            if constraint[0] == var and constraint[2] in assignedVars:
                
                    for domain in domains:
                        # if not (this domain, operator, value that's already assigned),
                        # remove this domain (it is not applicable) 
                        if not compare(domains[domain], constraint[1], varAssignments[constraint[2]]):
                            domains.remove(domain)

            elif constraint[2] == var and constraint[0] in assignedVars:
                
                    for domain in domains:
                        # if not (this domain, operator, value that's already assigned),
                        # remove this domain (it is not applicable) 
                        if not compare(varAssignments[constraint[2]], constraint[1], domains[domain]):
                            domains.remove(domain)

    # return the list of variable in newDict that has the least values
    # because they may tie

    listOfLength = []
    for var in newDict:
        listOfLength.append((var, len(newDict[var])))

    minLength = min(listOfLength)
    minLengthVariables = [val[0] for index, val in enumerate(listOfLength) if val == minLength]

    return minLengthVariables
    

    

def compare(a, operator, b):
    if (operator == "="):
        if (a == b):
            return True

    elif (operator == ">"):
        if (a > b):
            return True

    elif (operator == "<"):
        if (a < b):
            return Trye

    return False
    
    

def readInfo(varFile, conFile):
    varFile = open(varFile, "r")
    conFile = open(conFile, "r")
    
    varDict = {}
    varLines = varFile.readlines()
    varFile.close()
    for line in varLines:
        vals = line.split()
        varDict[vals[0][0]] = vals[1:len(vals)]

    constraints = conFile.readlines()
    conFile.close()
    for i in range(len(constraints)):
        constraints[i] = constraints[i].split()

    return varDict, constraints

def solveConstraints(varDict, constraints, varAssignments, fc):
    
    varToAssign = getVariable(varAssignments, varDict, constraints)
    if len(varDict[varToAssign]) == 0:
        return varDict
    while len(varDict[varToAssign]) > 0:
        varAssignments[varToAssign] = getValue(varAssignments, varDict.copy(), varToAssign, constraints)
        print "solveConstraints"
        solved = True

        if fc:
            for key in newVarDict:
                if len(varDict[key]) == 0:
                    solved = False

        if solved:
            for constraint in constraints:
                var1 = constraint[0]
                op = constraint[1]
                var2 = constraint[2]
                if var1 in varAssignments and var2 in varAssignments:
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
            for var in varAssignments:
                toPrint += var + "=" + varAssignments[var] + ", "
            toPrint = toPrint[:len(toPrint)-2] + "  failure"
            print toPrint
            varDict[varToAssign].remove(varAssignments[varToAssign])
            assignedVars.remove(varToAssign)
            del varAssignments[varToAssign]
            return varDict
        elif len(varAssignments) == len(varDict):
            toPrint = str(path) + ". "
            for var in varAssignments:
                toPrint += var + "=" + varAssignments[var] + ", "
            toPrint = toPrint[:len(toPrint)-2] + "  solution"
            print toPrint
            return True
        else:
            varDict = solveConstraints(varDict.copy(), constraints, varAssignments.copy(), fc)
            if varDict == True:
                return True
    toPrint = str(path) + ". "
    for var in varAssignments:
        toPrint += var + "=" + varAssignments[var] + ", "
    toPrint = toPrint[:len(toPrint)-2] + "  failure"
    print toPrint
    print varDict
    varDict[varToAssign].remove(varAssignments[varToAssign])
    assignedVars.remove(varToAssign)
    del varAssignments[varToAssign]
    return varDict

path = 1
params = sys.argv
print params
varDict, constraints = readInfo(params[1], params[2])
solveConstraints(varDict, constraints, {}, params[3] == "fc")
