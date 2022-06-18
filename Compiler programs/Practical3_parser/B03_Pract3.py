
# PROBLEM
    # Topic: Parser Construction
    # (A)	Write a program to find FIRST for any grammar. All the following rules of FIRST must be implemented.
    # (B)	Further, write a program to find Follow for the given grammar.
    # (C)	Construct the LL(1) parsing table using the FIRST and FOLLOW values computed above.


import re
import pandas as pd
#Input grammar
    # A -> SB | B
    # S -> a | Bc | @
    # B -> b | d

# list of standard values for all the capital and small letter
caps = [chr(x+65) for x in range(26)]
small = [chr(x+97) for x in range(26)]

# Taking input from file
file = open('grammar_inp.txt', 'r').read()
all = re.split(r'[->|\n]',file)

# storing all the non terminals and terminals
d={}
for i in file:
    # separate out all terminals and non terminals from the grammar
    i=i.strip()
    if(i in caps):
        if 'NT' not in d.keys():
            x=[]
            x.append(i)
            d['NT'] = x
        else:
            x = d['NT']
            x.append(i)
            d['NT']=x
        d['NT']= list(set(d['NT']))
   
    elif ( i in small):
        if('T' not in d.keys()):
            x=[]
            x.append(i)
            d['T'] = x
        else:
            x = d['T']
            x.append(i)
            d['T']=x
        d['T']= list(set(d['T']))
    

df = pd.Series(d)
# print(df)
#remove empty values and strip all
def clean(all):
    saveAll = []
    for i in range(len(all)):
        all[i]= all[i].strip()
        if(len(all[i])>0):
            saveAll.append(all[i])
    return saveAll
all = clean(all)
# print(saveAll)

grammar = file.split('\n')
# print(grammar)

#FOLLOW
def compute_follow(first, grammar):
    followSet= {}
    for i in d['NT']:
        followSet[i]=[]
    #Start Symbol
    onhold={}
    start_symbol = grammar[0][0]
    followSet[start_symbol].append("$")
    # print('start symbol',start_symbol)
    for i in grammar[::-1]:
        line = re.split(r'[->|\n]',i)
        line = clean(line)
        term = line[0]
        
        for g in range(len(line)):
            if(len(line[g])==1 and line[g]!= term and line[g] in d['NT']):
                onhold[line[g]]= term
                continue
            for x in range(len(line[g])):
                s = line[g]
                
                if(s[x] in d['NT'] and x+1<len(line[g]) and s[x+1] in d['T']):
                    followSet[s[x]].extend(s[x+1])
                    break
                if(s[x] in d['NT']):
                    y = x
                    f=0
                    while(y+1<len(s)):
                        if(s[y+1] in d['NT']):
                            followSet[s[x]].extend(first[s[y+1]])
                            
                            if("@" in first[s[y+1]]):
                                y+=1
                                continue
                            else:
                                f=1
                                break
                        y+=1
                    if(y+1<len(s) and f==0):
                        followSet[s[x]].extend(followSet[term])
                        onhold[s[x]]= term
                        break
                    
                        
    # print(onhold)
    for key in onhold:
        # print(str(onhold[key]))
        followSet[key].extend(followSet[str(onhold[key])])
    return followSet
    
# first information computation
def compute_first(grammar):
    firstpos = {}
    for i in d['NT']:
        firstpos[i]=[]
    
    #cal first of each Nterminal
    start_symbol = grammar[0][0]
    # print(start_symbol)
    for i in grammar[::-1]:
        line = re.split(r'[->|\n]',i) #Queue
        line = clean(line)
        
        term = line[0] #first non-terminl always
        for i in line[1:]:
            #rule one terminal at first position
            if i[0] in d['T'] or i=='@':
                if(i[0] not in firstpos[term]):

                    firstpos[term].append(i)
            else:
                
                if(i[0] in d['NT']):
                    temp = 0
                    while(True):
                        #All first non-terminal rule and epsilon in the first of non terminals
                        if( '@' in firstpos[i[temp]] and temp<len(i)-1):
                            # firstpos[term].remove('@')
                            
                            firstpos[term].extend(firstpos[i[temp]])
                            firstpos[term] = list(set(firstpos[term]))
                            #apply 3rd rule
                            if(temp>=len(i)):
                                break
                            firstpos[term].remove('@')
                            temp+=1 
                            
                            
                        else:
                            firstpos[term].extend(firstpos[i[temp]])
                            break
                        if(temp>=len(i)):
                            break
                    firstpos[term] = list(set(firstpos[term]))     
    return firstpos 

# table for first and follow information
def constructTable(first, follow, grammar):
    print()
    nt = {}
    for i in grammar[::-1]:
        line = re.split(r'[->|\n]',i) #Queue
        line = clean(line)
        pd1 = {}
        for ij in d['T']:
            pd1[ij]=[]
        pd1['$']=[]
        term = line[0]
        nt[line[0]]=[]
        for x in range(1, len(line)):
            if(line[x][0] in d['T']):
                s = term+' -> ' + line[x]
                pd1[line[x][0]].append(s)
            elif(line[x][0]=='@'):
                for ij in follow[term]:
                    s = term+' -> '+'@'
                    pd1[ij].append(s)
            elif(line[x][0] in d['NT']):
                temp = first[line[x][0]]
                
                for y in temp:
                    s = term+ ' -> '+line[x]
                    if(y=='@'):
                        for ij in follow[term]:
                            s = term+' -> '+'@'
                            pd1[ij].append(s)

                    else:
                        pd1[y].append(s)
        # print(term , pd)
        for i in pd1.keys():
            if len(pd1[i])==0:
                pd1[i].append('-')
        nt[term] = pd1
    return nt
                    


        

if __name__== '__main__':
    #FIRST            
    first  = compute_first(grammar)              
    print("\n----FIRST TABLE----")
    print(pd.Series(first))
    
    follow = compute_follow(first,grammar) 
    print("\n----FOLLOW TABLE----")
    print(pd.Series(follow))

    print("\n----LL(1) PARSING TABLE----")
    table = constructTable(first, follow,grammar)
    print("Table " ,table)
    print()
    print(" "*7,end="")
    print(*d['T'], "$", sep=" "*20)
    print()
    for i in table.keys():
        # print(i, end="\t")
        
        # for j in table[i].keys():
        #     print(*table[i][j], end=" \t")
        # print()
        print(i,end=" "*5)
        for j in table[i]:
            print(table[i][j], end=" "*(20-len(table[i][j])))
            # print("-", end=" "*20)
        print()
        # print(table[i])
        # print(pd.Series(table[i]))


# parsing of  a string to check if it belongs to a grammar or not

class Stack:
    def __init__(self):
        self.stack=[]
        self.top=-1
    def push(self,e):
        self.stack.append(e)
        self.top+=1
    def pop(self):
        if(len(self.stack)==0):
            print("operation not supported")
        else:
            self.stack.pop()
            self.top-=1
    def peek(self):
        return self.stack[self.top]


print('\n\n')
buff=input('Enter the string for parsing : ')
buffer=['$']
s=Stack()

for ch in buff[::-1]:
    buffer.append(ch)

start_symbol = all[0]
s.push('$')
s.push(start_symbol)
print(s.stack,buffer)
while(True):
    if(s.peek()==buffer[-1]=='$'):
        print("The string ",buff," is valid")
        break 
    if(s.peek()=='$' and buffer[-1]!='$'):
        print("String ",buff," not valid!")
        break
    if(s.stack[s.top] in d['NT']):
        x=table[s.stack[s.top]][buffer[-1]]
        if(x[0]=='-'):
            print("String ",buff," not valid!")
            break
        elem = x[0].split('->')[-1].strip()
        s.pop()
        for ch in elem[::-1]:
            s.push(ch)
        # print(s.stack)
    if(s.stack[s.top] in d['T']):
        if(s.stack[s.top] ==buffer[-1]):
            s.pop()
            buffer.pop()
        else:
            print("The String ",buff," not valid!")
            break
    # print(buffer,"---", s.stack)
    