# Topic : Parsing
# Write a program to validate a natural language sentence. Design a natural language grammar, compute and input the LL(1) table. Validate if the given sentence is valid based on the grammar or not.

import pandas as pd
# Himani Dighorikar

#Initializing parsing tables
nonTerminal = ['S','NP','VP','N','V','P','PN','D']
terminal  = ['championship','ball','toss','is','want','won','played','me','I','you','India','Australia','Steve','John','the','a','an','$']
parsingTable=[ ['','','','','','','','S->NP VP','S->NP VP','S->NP VP','S->NP VP','S->NP VP','S->NP VP','S->NP VP','S->NP VP','S->NP VP','S->NP VP',''],
 ['','','','','','','','NP->P','NP->P','NP->P','NP->PN','NP->PN','NP->PN','NP->PN','NP->D N','NP->D N','NP->D N',''],
 ['','','','VP->V NP','VP->V NP','VP->V NP','VP->V NP','','','','','','','','','','',''],
 ['N->championship','N->ball','N->toss','','','','','','','','','','','','','','',''],
 ['','','','V->is','V->want','V->won','V->played','','','','','','','','','','',''],
 ['','','','','','','','P->me','P->I','P->you','','','','','','','',''],['','','','','','','','','','','PN->India','PN->Australia','PN->Steve','PN->John','','','',''],
 ['','','','','','','','','','','','','','','D->the','D->a','D->an','']
]
table = pd.DataFrame( parsingTable, index= nonTerminal,columns = terminal )
# String Validation
def parse(user_input,start_symbol,table):
    stack=[]
    initial = user_input
    stack.append("$")
    stack.append("S")
    user_input=user_input.split(" ")
    user_input.append("$")
  
    print("Stack:",stack,"\n","Input:",user_input,"\n")
    while True:
    # input is empty but stack is not empty
        if bool(stack)==True and bool(user_input)==False:
            print("{} is an invalid String".format(initial))
            break
        #stack and input both are empty
        elif bool(stack)==False and bool(user_input)==False:
            print("{} is a valid String".format(initial))
            break
        #for same symbol
        elif user_input[0] == stack[len(stack)-1]:
            stack.pop()
            user_input.pop(0)
            print("Stack:",stack,"\n","Input:",user_input,"\n")
        else:
            term=user_input[0]
            indexNonTerminal = nonTerminal.index(stack[len(stack)-1])
            str2=table[term][indexNonTerminal]
            stack.pop()
            str2 = str2.split(">")
            str2 = str2[1].split(" ")
            str2 = str2[::-1]
            for s in str2:
                stack.append(s)
parse('India won the championship','S',table)
