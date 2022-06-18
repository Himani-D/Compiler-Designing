
# Himani Dighorikar
# B03
# AIM : Write a code to implement Local optimization techniques until no further optimization is 
# possible for the given three address code.
data = open("C:/Users/HP/Desktop/Semester6/Compiler design/Lab/Pract8/code.txt").read()
instructions=[]
import re
for i in data.split("\n"):
    instructions.append(i)
print('------------ CODE ----------------')
for i in instructions:
    print(i)

print('---------------------------------')
print("Step 1: Algebric Simplification")
print('---------------------------------')
simp={'^':'+'}
for i in range(len(instructions)):
    if('^' in instructions[i]):
        num = re.findall(r'[0-9]+', instructions[i])
        instructions[i]=''.join(list(instructions[i])[:list(instructions[i]).index('^')-1])+" "+' '.join(list(instructions[i][instructions[i].index('^')-1])+list(('*'+instructions[i][instructions[i].index('^')-1])*(int(num[0])-1)))

for i in instructions:
    print(i)
print('---------------------------------')
print("Step 2: Constant and Copy Propagation with constant folding")
print('---------------------------------')
def propagration(instructions):
    code  = ' '.join(instructions)
    assign = {}
    for i in range(len(instructions)):
        inst = ''.join(instructions[i].split())
        ind = inst.split("=")
        if(len(ind[1].split("+"))==1 and len(ind[1].split("-"))==1 and len(ind[1].split("*"))==1):
            assign[ind[0]]=ind[1]
        else:
            if(len(assign.keys())>0):
                for k in assign.keys():
                    while(k in instructions[i]):
                        id = instructions[i].index(k)
                        temp = list(instructions[i])
                        temp[id]=assign[k]
                        temp = ''.join(temp)
                        compute = temp.split()[1:]
                        
                        for numb in compute:
                            if(numb in [chr(x+97) for x in range(26)]):
                                instructions[i] = temp
                                break
                        else:
                            su=0
                            for numb in compute:
                                if(numb.isdigit()==True):
                                    
                                    if("+" in compute):
                                        su+=int(numb)
                                    if("*" in compute):
                                        su*=int(numb)
                            
                            instructions[i] = temp.split()[0] +" = "+str(su)
                
    return instructions
instructions = propagration(instructions)
for i in instructions:
    print(i)
print('---------------------------------')
print("Step 3 : Sub expression Elimination")
print('---------------------------------')
def subExpressionElimination(instructions):
    compute={}
    replaced={}
    for i in range(len(instructions)):
        val = instructions[i].split("=")
        if(val[1].strip() not in compute.values()):
            compute[val[0].strip()]=val[1].strip()
        else:
            key=-1
            for k in compute.keys():
                if(compute[k]==val[1].strip()):
                    replaced[k]=val[0].strip()
                    key=k
            instructions[i] = val[0]+" = "+key
    return (instructions, replaced)
instructions, replaced=subExpressionElimination(instructions)
instructions=propagration(instructions)
for i in instructions:
    print(i)
print('---------------------------------')
print("Step 4 : Constant Folding")
print('---------------------------------')
for key in replaced:
    count=0
    for i in range(len(instructions)):
        if(replaced[key] in ''.join(instructions[i].split("=")[1:]).split()):
            temp=list(instructions[i])
            ind = temp.index(replaced[key])
            temp[ind]=key
            instructions[i] = ''.join(temp)
              
for i in instructions:
    print(i)
print('---------------------------------')
print("Step 5: Dead COde Elimination")
print('---------------------------------')
final_inst=[]
variables=[]
for i in range(len(instructions)):
    flag=0
    var = instructions[i].split("=")[0].strip()
    rgt = instructions[i].split("=")[1].strip()
    if(len(rgt)>1):
        final_inst.append(instructions[i])

    # for j in range(i, len(instructions)):
    #     exp = instructions[j].split("=")[1].strip()
    #     if(var in exp):
    #         for v in variables:
    #             if(v in exp):
    #                 break
    #         else:
    #             flag=1
    #             break
    # if(flag==1):
        # final_inst.append(instructions[i])
        # variables.append(var)
for i in final_inst:
    print(i)
        
        
        


