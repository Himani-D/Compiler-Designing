# AIM :  Write a program to generate the code using simple code generation algorithm.
# Name : Himani Dighorikar
# Roll no : 03
import re
operations = {'+' : 'ADD', '-': 'SUB','*': 'MUL'}
code = open('C:/Users/HP/Desktop/Semester6/Compiler design/Lab/Pract10/code', 'r').read()
print(code)
code = code.split('\n')
stored={}
dag=[]
count=0

# iterate through all the instructions
for i in range(len(code)):
    inst = code[i]
    lhs = inst.split('=')[0].strip()
    rhs = inst.split('=')[1].strip() 
    # find an operator and separate variables from rhs
    var= re.findall(r"[a-z]",rhs)
    op = re.findall(r"[+-/*]",rhs)[0]
    
    if(var[1] not in stored.keys() and var[0] not in stored.keys()):
        instruction = 'MOV {}, R{}'.format(var[-1],count)
        dag.append(instruction)
        for val in var[:-1]:
            instruction = operations[op]+ ' {}, R{}'.format(val,count)
            dag.append(instruction)
        stored[lhs] = 'R{}'.format(count)
        count+=1
    else:
        dag.append('MOV {}, memo'.format(stored[var[-1]]))   
        # instruction = operations[op]+ ' {}, R{}'.format(val,count)
        # dag.append(instruction)
        if(var[0] in stored.keys()):
            instruction = operations[op]+ ' {}, {}'.format(stored[var[0]],stored[var[-1]])
        else:
            instruction = operations[op]+ ' {}, {}'.format(var[0],stored[var[-1]])
        
        dag.append(instruction)
        stored[lhs] = stored[var[-1]]
print('-------------------------------------------')  
print('The simple code generation for above code : ')   
print('-------------------------------------------')  
for i in dag:
    print(i)

