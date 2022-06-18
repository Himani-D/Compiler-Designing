
# Himani Dighorikar
# B03
# Aim : Construct the SLR parser for the given grammar

import re
raw_grammar = open('C:/Users/HP/Desktop/Semester6/Compiler design/Lab/Pract5/Input5.txt', 'r').read()
grammar = re.split(r'\n', raw_grammar)
# all = re.split(r'[->|\n]',raw_grammar)
# print(len(grammar))
start_symbol = grammar[0][0]
print("Start Symbol : ", start_symbol)
add = "S' -> "+start_symbol
grammar=[add]+grammar

#Augumented grammar
for g in range(len(grammar)):
    x=grammar[g].split()
    x[-1]='.'+x[-1]
    grammar[g]=''.join(x)
print("First Step : Augumentation")
for i in grammar:
    print(i)
# Grammar exploration - no. of terminals and non terminals
caps = [chr(x+65) for x in range(26)]
small = [chr(x+97) for x in range(26)]
d={}
for i in raw_grammar:
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

# Closure function
i0 = [grammar[0]]
print("\nSecond Step - Closure :- ", grammar[0])
print(*grammar, sep="\n")

gotos_dictionary={'i0':grammar,'i1':i0}
# Gotos
def goto(gram):
    l=[]
    g = list(gram)
    f=0
    ind = g.index('.')
    if(ind!=len(g)-1):
        ele = g[ind+1]
    else:
        f=1
        return l
    if f==0:
        g.remove('.')
        g.insert(ind+1,'.')
        l.append(''.join(g))
        u=[g]
        while(len(u)!=0):
            curr = u[0]
            if(curr.index('.')==len(g)-1 or curr[curr.index('.')+1] in d['T']):
                break
            else:
                nt = curr[curr.index('.')+1]
                for i in grammar:
                    if(i[0]==nt):
                        u.append(i)
                        l.append(''.join(i))
            u.pop(0)
        # print('Goto on {} : {}'.format(ele,l))
        return l
        
queue= [grammar]
count=0
all_prev_states =[]
while(len(queue)>0):
    grm = queue[0]
    all_prev_states.append(grm)
    queue.pop(0)
    l=[]
    print('...........................................')
    print('Grammar Rule: ',grm)
    print()
    for i in grm:
        if(i.index('.')==len(i)-1) or '@' in i :
            continue
        temp=goto(i)
        print('States : ',grm)
        print('Processing on grammar rule : ',i)
        print('on Goto operations: ', i[i.index('.')+1])
        print(temp)
        if(temp not in all_prev_states):
            queue.append(temp)
        all_prev_states.append(temp)
        print()
    print()