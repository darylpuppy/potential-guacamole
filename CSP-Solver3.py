import sys
import copy

# find least constraining value
# the one that rules out the fewest values in the remaining variables
# varAssignment: dict type, variables and their assigned values
# varToAssign: this is the variable we are trying to find a value for it

def getValue(varAssignments, varDict, varToAssign, constraints, fc):

    # so... try each possible values to this variable
    
    # based on constraints, remove some of the values of varToAssign

    if fc:
        candidateValues = findCandidateValues(varAssignments, varDict, varToAssign, constraints)
    else:
        candidateValues = varDict[varToAssign]
  
    dictKeys = varDict.keys()
    assignedVars = varAssignments.keys()
    unassignedVars = list(set(dictKeys)-set(assignedVars) - set(varToAssign))


    # now choose which of these values?
    # actually assign it,

    mostVals = -1
    # after assigning a possible value to a variable
    # add all values still possible to the rest of the variables
    for val in candidateValues:
        thisDict = {}
        
        numberOfAllRemainingValues = 0
        varAssignments[varToAssign] = val # assign it

        for var in unassignedVars:
            thisDict[var] = findCandidateValues(varAssignments, varDict, var, constraints)
            numberOfAllRemainingValues += len(thisDict[var])
        if numberOfAllRemainingValues > mostVals:
            mostVals = numberOfAllRemainingValues
            bestDict = thisDict
            bestVal = val
        

    for var in assignedVars:
        bestDict[var] = varDict[var]
    bestDict[varToAssign] = varDict[var]
    return (bestVal, bestDict)

def findCandidateValues(varAssignments, varDict, varToAssign, constraints):
    assignedVars = varAssignments.keys()
    candidateValues = copy.copy(varDict[varToAssign])
    for constraint in constraints:
        if constraint[0] == varToAssign and constraint[2] in assignedVars:
                
                for val in varDict[varToAssign]:
                    
                    if val in candidateValues and not compare(val, constraint[1], varAssignments[constraint[2]]):
                        candidateValues.remove(val)

        elif constraint[2] == varToAssign and constraint[0] in assignedVars:
                
                for val in varDict[varToAssign]:
                    if val in candidateValues and not compare(varAssignments[constraint[0]], constraint[1], val):
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
    maxConstraints = -1
    for var in dictNumberOfConstraints:
        if dictNumberOfConstraints[var] > maxConstraints:
            maxConstraints = dictNumberOfConstraints[var]
            bestVar = var
        elif dictNumberOfConstraints[var] == maxConstraints:
            if var < bestVar:
                bestVar = var
    return bestVar
        
    #return max(dictNumberOfConstraints, key = dictNumberOfConstraints.get)
    
       

def findMostConstrainedVariables(varAssignments, varDict, constraints):
    leastVals = 9999999
    bestVars = []
    for var in varDict:
        if len(varDict[var]) < leastVals:
            if var not in varAssignments:
                leastVals = len(varDict[var])
                bestVars = [var]
        elif len(varDict[var]) == leastVals:
            if var not in varAssignments:
                bestVars.append(var)
    return bestVars
    """# variable with the fewest legal values
    
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

    return minLengthVariables"""
    

    

def compare(a, operator, b):
    if (operator == "="):
        if (a == b):
            return True

    elif (operator == '>'):
        if (a > b):
            return True

    elif (operator == "<"):
        if (a < b):
            return True
        
    elif (operator == "!"):
        if (a != b):
            return True

    return False
    
    

def readInfo(varFile, conFile):
    varFile = open(varFile, "r")    #Open up the files
    conFile = open(conFile, "r")
    
    varDict = {}
    varLines = varFile.readlines()
    varFile.close()
    for line in varLines:   #Split the lines into their components
        vals = line.split()
        varDict[vals[0][0]] = vals[1:len(vals)] #The variable is the first character of the first part of line

    constraints = conFile.readlines()
    conFile.close()
    for i in range(len(constraints)):
        constraints[i] = constraints[i].split()

    return varDict, constraints

def solveConstraints(varDict, constraints, varAssignments, varOrder, fc):
    global path
    varToAssign = getVariable(varAssignments, varDict.copy(), constraints)
    varOrder.append(varToAssign)    #Add the variable to the order so we print it out in order
    if len(varDict[varToAssign]) == 0:  #If there are no legal values, return
        return varDict
    while len(varDict[varToAssign]) > 0:    #Keep looking for a legal assignment until there are no legal values left
        varAssignments[varToAssign], newVarDict = getValue(varAssignments, varDict.copy(), varToAssign, constraints, fc)    #Get the best variable and resulting set of legal values for that value
        solved = True

        if fc:  #If we're forward checking, use the variable dictionary obtained above and check for variables without legal values
            varDict = newVarDict
            for key in newVarDict:
                if len(varDict[key]) == 0:
                    solved = False

        if solved:  #If there wasn't an issue with error checking, find out if there are any constraints we're violating
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

        if not solved:  #If there was some error above, print a failure and return
            toPrint = str(path) + ". "
            for var in varOrder:
                toPrint += var + "=" + varAssignments[var] + ", "
            toPrint = toPrint[:len(toPrint)-2] + "  failure"
            print toPrint
            path += 1
            print varAssignments
            print varDict
            varDict[varToAssign].remove(varAssignments[varToAssign])
            del varAssignments[varToAssign]
        elif len(varAssignments) == len(varDict):   #If there was no issue, print the solution and return
            toPrint = str(path) + ". "
            for var in varOrder:
                toPrint += var + "=" + varAssignments[var] + ", "
            toPrint = toPrint[:len(toPrint)-2] + "  solution"
            print toPrint
            return True
        else:   #If it neither failed nor succeeded, try the next variable
            success = solveConstraints(varDict.copy(), constraints, varAssignments.copy(), varOrder, fc)
            if success == True: #If that succeeded, stop searching
                return True
            else:
                varDict[varToAssign].remove(varAssignments[varToAssign])    #If it didn't, remove the current assignment and continue
                del varAssignments[varToAssign]
                
    varOrder.remove(varToAssign)
    return False

path = 1
params = sys.argv
varDict, constraints = readInfo(params[1], params[2])
solveConstraints(varDict, constraints, {}, [], params[3] == "fc")
