import sys
from copy import deepcopy
import re


assign_true = set()
assign_false = set()
n_props, n_splits = 0, 0


def print_cnf(cnf):
    s = ''
    for i in cnf:
        print(i)
        if len(i) > 0:
            s += '(' + i.replace(' ', '+') + ')'
            #it means: put the literals , and replace the space with + so if one item is !A B -> (!A+B)
    if s == '': #so the cnf was empty
        s = '()'
    print(s)


def solve(cnf, literals):
    print('\nCNF = ', end='')
    print_cnf(cnf)
    new_true = []
    new_false = []
    global assign_true, assign_false, n_props, n_splits
    assign_true = set(assign_true)
    assign_false = set(assign_false)
    n_splits += 1
    cnf = list(set(cnf))
    units = [i for i in cnf if len(i)<3] #we just want clauses with one literal
    units = list(set(units))


    if len(units): #if there is any unit
        '''The Unit literal Rule'''
        '''Start'''
        for unit in units:
            n_props += 1 #we have to do the unit propagation for each unit
            if '!' in unit: #example: !A
                assign_false.add(unit[-1]) # The literal unit[-1] is assigned to false
                new_false.append(unit[-1]) #unit[-1] means the literal not the negative(!)
                i = 0
                while True:  
                    if unit in cnf[i]: #delete all clauses containing that Literal (unit)
                        cnf.remove(cnf[i])
                        i -= 1
                    elif unit[-1] in cnf[i]: #delete all occurances of complement of that Literal (!unit) from all other clauses
                        cnf[i] = cnf[i].replace(unit[-1], '').strip()
                    i += 1
                    if i >= len(cnf):
                        break
            else: #example: A
                assign_true.add(unit) # The literal unit is assigned to true
                new_true.append(unit)
                i = 0
                while True:
                    if '!'+unit in cnf[i]: #delete all occurances of complement of that Literal (!unit) from all other clauses
                        cnf[i] = cnf[i].replace('!'+unit, '').strip()
                        if '  ' in cnf[i]:
                            cnf[i] = cnf[i].replace('  ', ' ')
                    elif unit in cnf[i]: #delete all clauses containing that Literal (unit)
                        cnf.remove(cnf[i])
                        i -= 1 #BCZ the previous literal was deleted so the index is one ahead that what it should be
                    i += 1
                    if i >= len(cnf):
                        break
        '''The Unit literal Rule'''
        '''End'''
        
    print('Units =', units)
    print('CNF after unit propogation = ', end = '')
    print_cnf(cnf)

    if len(cnf) == 0:# if by doing the unit propagation, there is no more any cluses in the cnf 
        return True #so the cnf was SAT
    '''Backtracking after doing the previous assignments'''
    if sum(len(clause)==0 for clause in cnf): #check if there is at least 1 clause which is null
        
        print("before doing the back tracking")
        for i in assign_true:
            print('\t\t'+i, '= True')
        for i in assign_false:
            print('\t\t'+i, '= False')
        print("-------------------------------------------")
        for i in new_true:
            assign_true.remove(i)
        for i in new_false:
            assign_false.remove(i)
        print('Null clause found, backtracking...')
        return False
    literals = [k for k in list(set(''.join(cnf))) if k.isalpha()] #finding all the literals of our cnf

    x = literals[0]
    if solve(deepcopy(cnf)+[x], deepcopy(literals)):
        return True
    elif solve(deepcopy(cnf)+['!'+x], deepcopy(literals)):
        return True
    else:
        for i in new_true:
            assign_true.remove(i)
        for i in new_false:
            assign_false.remove(i)
        return False


def dpll():
    global assign_true, assign_false, n_props, n_splits
    input_cnf = open(sys.argv[1], 'r').read() #reading the file
    literals = [i for i in list(set(input_cnf)) if i.isalpha()]
    cnf = input_cnf.splitlines()
    if solve(cnf, literals):
        # print('\nNumber of Splits =', n_splits)
        # print('Unit Propogations =', n_props)
        print('\nResult: SATISFIABLE')
        print('Solution:')
        for i in assign_true:
            print('\t\t'+i, '= True')
        for i in assign_false:
            print('\t\t'+i, '= False')
    else:
        # print('\nReached starting node!')
        # print('Number of Splitss =', n_splits)
        # print('Unit Propogations =', n_props)
        print('\nResult: UNSATISFIABLE')
    print()


# def solve_dp(cnf , true_literals):
#     print("in dp_solve function")
#     cnf = list(set(cnf))
#     units = [i for i in cnf if len(i)<3] #we just want clauses with one literal
#     units = list(set(units)) #i think it removes duplicated units if exists
#     print("The cnf is :")
#     print(cnf)
#     print("the units are:\n" , units)
#     print("The literals are \n" , true_literals)

#     unit_flag = 0
#     if len(units): #if there is any unit
#         '''The Unit literal Rule'''
#         '''Start'''
#         for unit in units:
#             print("we are in unit propagation and the unit is")
#             print(unit)
#             if '!' in unit: #example: !A
#                 i = 0
#                 while True:  
#                     if unit in cnf[i]: #delete all clauses containing that Literal (unit)
#                         cnf.remove(cnf[i])
#                         unit_flag=1
#                         i -= 1
#                     elif unit[-1] in cnf[i]: #delete all occurances of complement of that Literal (!unit) from all other clauses
#                         cnf[i] = cnf[i].replace(unit[-1], '').strip()
#                         unit_flag=1
#                     i += 1
#                     if i >= len(cnf):
#                         break
#             else: #example: A
#                 i = 0
#                 while True:
#                     if '!'+unit in cnf[i]: #delete all occurances of complement of that Literal (!unit) from all other clauses
#                         cnf[i] = cnf[i].replace('!'+unit, '').strip()
#                         unit_flag=1
#                         if '  ' in cnf[i]:
#                             cnf[i] = cnf[i].replace('  ', ' ')
#                     elif unit in cnf[i]: #delete all clauses containing that Literal (unit)
#                         cnf.remove(cnf[i])
#                         unit_flag=1
#                         i -= 1 #BCZ the previous literal was deleted so the index is one ahead that what it should be
#                     i += 1
#                     if i >= len(cnf):
#                         break
#         '''The Unit literal Rule'''
#         '''End'''

#     '''Pure literal Rule'''
#     '''Start'''
#     pure_flag = 0
#     print("before for")
#     for l in true_literals:
#         if '!' in l:
#             x = l[1]
#             print(x)
#             if x not in true_literals:
#                 for clause in cnf:
#                     if l in clause:
#                         print(clause)
#                         cnf.remove(clause)
#                         print(cnf)
#                         pure_flag = 1
#         else:
#             x = '!'+l
#             if x not in true_literals:
#                 for clause in cnf:
#                     if l in clause:
#                         cnf.remove(clause)
#                         pure_flag = 1
#     '''Pure Literal Rule'''
#     '''End'''

#     '''Resolution Rule '''
#     '''Start'''
#     resolution_flag = 0
#     all_resolvents = []
#     for l in true_literals:
#         resolvents = []
#         # if '!' in l :
#         #     l_complement = l[1]
#         # else:
#         #     l_complement = '!'+l

#         for clause in cnf:
#             if l in clause:
#                 print("before error clause:")
#                 print(clause)
#                 print(cnf)
#                 clause_copy = clause
#                 for another_clause in cnf:
#                     if '!' in l :
#                         if l[1] in another_clause and l not in another_clause : 
#                             # another_clause_copy = another_clause
#                             c2 = re.sub(l[1] , '' , another_clause).strip()
#                             c1 = re.sub(l , '' , clause).strip()
#                             # c2 = another_clause_copy.replace(l[1] , '').strip()
#                             # c1 = clause_copy.replace(l,'').strip()
#                             print("here is the error clause:")
#                             print(clause)
#                             print(cnf)
#                             cnf.remove(clause)  
#                             cnf.remove(another_clause)
#                             new_clause = c1+" "+c2
#                             cnf.append(new_clause)
#                             resolvents.append(new_clause)
#                             all_resolvents.append(resolvents)
#                     else:
#                         if '!'+l in another_clause and l not in another_clause : 
#                             # another_clause_copy = another_clause
#                             c2 = re.sub(l[1] , '' , another_clause).strip()
#                             c1 = re.sub(l , '' , clause).strip()
#                             # c2 = another_clause_copy.replace(l[1] , '').strip()
#                             # c1 = clause_copy.replace(l,'').strip()
#                             print("here is the error clause:")
#                             print(clause)
#                             print(cnf)
#                             cnf.remove(clause)  
#                             cnf.remove(another_clause)
#                             new_clause = c1+" "+c2
#                             cnf.append(new_clause)
#                             resolvents.append(new_clause)
#                             all_resolvents.append(resolvents)

#                     # if '  ' in clause or '  ' in another_clause:
#                     #             # clause = clause.replace('  ' , ' ')
#                     #             # another_clause = another_clause.replace('  ' , ' ')
#                     #             clause = re.sub('  ' , ' ' , clause)
#                     #             another_clause = re.sub('  ' , ' ' , another_clause)
#         # for resolvent in resolvents:
#         #     cnf.append(resolvent)

#     if len(all_resolvents):
#         resolution_flag = 1
    
#     for clause in cnf:
#         if '  ' in clause:
#             clause.replace('  ' , '')


#     '''Resolution Rule'''
#     '''End'''

#     '''Terminate rules'''
#     for clause in cnf: #checking if there is any empty clause
#         if clause == '':
#             print("the cnf is unsat and the cnf is:\n" , cnf)
#             return False
    
#     # If no more rule is applicable
#     if cnf == []:
#         return True
#     if pure_flag == 0 and unit_flag == 0 and resolution_flag == 0 :
#         return True
    
#     else:
#         solve_dp(cnf ,true_literals)




# def dp():
#     input_cnf = open(sys.argv[1], 'r').read() #reading the file
#     literals = [i for i in list(set(input_cnf)) if i.isalpha()]
#     cnf = input_cnf.splitlines()
#     true_literals = [i for i in set(input_cnf.split())]# i will use it for pure literal rule
#     if solve_dp(cnf , true_literals):
#         print('SATISFIABLE')
#     else:
#         print("NotSATISFIABLE")

if __name__=='__main__':
    dpll()
    # dp()