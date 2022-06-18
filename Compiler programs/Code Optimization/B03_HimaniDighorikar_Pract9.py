# Himan Dighorikar
# B03
# Practical 9 : Write a program to perform loop detection by finding leader, basic blocks and
# program flow graph's natural loop.
data = open("C:/Users/HP/Desktop/Semester6/Compiler design/Lab/Pract9/code.txt").read()
print(data)
instructions=[]
for i in data.split("\n"):
    instructions.append(i)
print(instructions)
import re
print('----------------------')
print("Leaders statements ")
print('----------------------')
def leaderstatements(code):
    statements=[]
    cond=False
    for i in range(len(code)):
        # first statement
        if(cond):
            cond=False
            statements.append((i+1,code[i]))
        else:
            if(i==0):
                statements.append((i+1,code[i]))
            if('if' in code[i].lower() and (i+1,code[i]) not in statements):
                statements.append((i+1,code[i]))
                num = int(re.findall(r'[0-9+]',code[i])[-1])
                statements.append((num,code[num-1]))
                cond=True
            if(code[i][:4].lower()=='goto'):
                num = int(re.findall(r'[0-9+]',code[i])[-1])
                if((num,code[num-1]) not in statements):
                    statements.append((num,code[num-1]))

    return statements

leaders = leaderstatements(instructions)
for i in sorted(leaders):
    print(str(i[0])+'. ',i[1])


print('----------------------')
print('2. The basic blocks')
print('----------------------')

def blocks(code):
    ind=0
    bcontainer=[]
    while(ind<len(code)):
        temp=[]
        while(ind<len(code) and 'if' not in code[ind].lower()):
            temp.append((ind+1,code[ind]))
            if('goto' in code[ind].lower()):
                ind+=1
                break
            ind+=1
        if(len(temp)>0):
            bcontainer.append(temp)
        if(ind<len(code) and 'if' in code[ind].lower()):
            bcontainer.append([(ind+1,code[ind])])
            ind+=1

        

    return bcontainer

totblocks = blocks(instructions)
for b in range(len(totblocks)):
    print('Block {}'.format(b+1))
    print(totblocks[b])
    print()

print()

print('----------------------')
print('3. Program flow graph indicating the successor and  predecessor.')
print('----------------------')

def checkForTransfer(block):
    for i in block:
        if('if' in i[1].lower()):
            return True 
        if('goto' in i[1].lower()):
            return True
    return False
d={}
for i in range(len(totblocks)):
    d[i+1]=[]
    for j in totblocks[i]:
        d[i+1].append(j[0])
print(d)

# initialize the predecessor or successor
def allocateBlocks(blocks):
    b={}
    for i in range(len(blocks)):
        b[i+1]=[]
    return b

blocks_pred= allocateBlocks(totblocks)
blocks_succ=allocateBlocks(totblocks)

def checkBlock(totBlocks, num):
    for block in range(totBlocks):
        for i in totBlocks[block]:
            if(i[0]==num):
                return block
    return -1

for block in range(len(totblocks)):
    if(checkForTransfer(totblocks[block])==False):
        if('end' not in totblocks[block][0][1].lower()):
            blocks_succ[block+1].append(block+2)
            blocks_pred[block+2].append(block+1)
    else:
        f=0
        for i in totblocks[block]:
            
            if('if' in i[1].lower()):
                num = int(re.findall(r'[0-9+]',i[1])[-1])
                for k in d.keys():
                    if(num in d[k]):
                        blocks_succ[block+1].append(k)
                        blocks_pred[k].append(block+1)
                        f=1
                        break
                blocks_succ[block+1].append(block+2)
                blocks_pred[block+2].append(block+1)
                
            if(f==1):
                f=0
                break
            if('goto' in i[1].lower() and 'if' not in i[1].lower()):
                
                num = int(re.findall(r'[0-9+]',i[1])[-1])
                for k in d.keys():
                    
                    if(num in d[k]):
                        
                        blocks_succ[block+1].append(k)
                        blocks_pred[k].append(block+1)
                        break

print(blocks_pred,blocks_succ)
for i in blocks_succ.keys():
    if(len(blocks_succ[i])>0):
        print(i,' -> ',blocks_succ[i])
print('----------------------')
print("Dominators of all the basic blocks ")
print('----------------------')

dominators=allocateBlocks(totblocks)
paths={1:[]}
curr=1
num=1
import copy
queue = []
path = [curr]
e=1
while(curr!=len(totblocks)):
    c=1
    while(c<=len(blocks_succ[curr])):  
        t =copy.deepcopy(path)   
        t.append(blocks_succ[curr][c-1])
        paths[c] = t
        # curr = blocks_succ[curr]
        c=c+1
    path = paths[curr]
    queue.extend(blocks_succ[curr])
    curr = queue[0]
    queue.pop(0)
    
# check if the paths are endding at the last block
for i in paths.keys():
    while(paths[i][-1]!=len(totblocks)):
        if(blocks_succ[paths[i][-1]][0] in paths[i]):
            paths[i].append(blocks_succ[paths[i][-1]][0])
            break
        paths[i].append(blocks_succ[paths[i][-1]])
print(paths)

print('----------------------')
print('3. Natural Loop Detction.')
print('----------------------')

for i in paths.keys():
    if(paths[i][-1] in paths[i][:-1]):
        print('Loop detected!')
        print("Backward edge in : ", paths[i][-2],' -> ', paths[i][-1])
