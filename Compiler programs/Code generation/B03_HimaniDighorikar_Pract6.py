# Himani Dighorikar
# B03
# Aim : Three Address COde Generation - For loop with If-Else Condition
import re
code = open('C:/Users/HP/Desktop/Semester6/Compiler design/Lab/Practical_6/Input_Pract7.txt', 'r').read()
print("Input : for-loop with If-else condition.")
print(code)
count_loop = code.count('for')
print("Output : Three Address Code!")
# fetch information fron the for loops
address_count=100
d={}
incr=""
count_for=0
for_cond=[]
for line in code.split('\n'):
    if('for' in line):
        parts = re.split(r';', line)
        incr = parts[2]
        val = []
        val.append((int(re.findall('\d+',parts[0])[0]), parts[0][parts[0].index('=')-1]))
        val.append((int(re.findall('\d+',parts[1])[0]), parts[1]))
        for_cond.append(val)
        d[address_count]='{} = {}'.format(for_cond[-1][0][1],for_cond[-1][0][0])
        address_count+=1
        d[address_count] = 'if {} goto {}'.format(for_cond[-1][1][1], address_count+2)
        addr = address_count
        address_count+=1
        d[address_count] = 'goto {}'.format(address_count)
        address_count+=1

    if('if' in line):
        x=line.split('{')
        
        d[address_count] = x[0].strip()+' goto {}'.format(address_count)
        address_count+=1
        temp =code.split('\n')
        
        for i in range(temp.index(line),len(temp)):
            if('else' in temp[i]):
                j=i+1
                
                while(temp[j].strip()!='}'):
                    if(("+=" in temp[j]) or ("-=" in temp[j]) or ("*=" in temp[j]) or ("/=" in temp[j] ) or (("+" or "-" or "*" or "/") and  ("=")) in temp[j]):
                        d[address_count] = "T = " + str(*(re.findall(r'[a-zA-Z_]+', temp[j])))+ str(*(re.findall(r'[*+/-]+', temp[j])))+ str(int(*(re.findall(r'[0-9]+', temp[j]))))
                        address_count+=1
                        d[address_count] =str(*(re.findall(r'[a-zA-Z_]+', temp[j]))) + " = T"
                        address_count+=1
                        j+=1

                    else:

                        d[address_count] = temp[j].strip()
                        address_count+=1
                        j+=1 
                break
        d[address_count] = 'goto {}'.format(address_count)
        address_count+=1
        i=temp.index(line)+1
        while(temp[i].strip()!='}'):
            if(("+=" in temp[i]) or ("-=" in temp[i]) or ("*=" in temp[i]) or ("/=" in temp[i] ) or (("+" or "-" or "*" or "/") and  ("=")) in temp[i]):
           
                d[address_count] = "T = " + str(*(re.findall(r'[a-zA-Z_]+', temp[i])))+ str(*(re.findall(r'[*+/-]+', temp[i])))+ str(int(*(re.findall(r'[0-9]+', temp[i]))))
                address_count+=1
                d[address_count] =str(*(re.findall(r'[a-zA-Z_]+', temp[i]))) + " = T"
                address_count+=1
            else:
                d[address_count] = temp[i].strip()
                address_count+=1

            i+=1

# operator for updation of iteration value
if("++" in incr):
    op="+1"
elif("--" in incr):
    op="-1"
elif("+=" in incr):
    op="+"+re.findall("\d+",incr)[0]
elif("-=" in incr):
    op="-"+re.findall("\d+",incr)[0]

store_incr= address_count
d[address_count] = "t1 = "+d[100][0]+op
address_count+=1
d[address_count] =d[100][0]+" = t1"
address_count+=1    
d[address_count] ='goto {}'.format(addr)
address_count+=1   
d[address_count]="exit"
for i in range(len(d.keys())-1):
    if("goto" in d[list(d.keys())[i]][:4]):
        
        d[list(d.keys())[i]]="goto " +str(100+len(d.keys())-1)
        break
# for i in d:
#     print(i, d[i])
trav=0
for i in range(len(d.keys())-1):
    # print('===',list(d.keys())[i],d[list(d.keys())[i]])
    if("goto" in d[list(d.keys())[i]]):
        if(str(d[list(d.keys())[i]][-3:]) ==str(list(d.keys())[i])):
            ind=-1
            if (trav%2==0):
                for j in range(i+1,len(d)):
                  
                    if("goto" in d[list(d.keys())[j]] and str(d[list(d.keys())[j]][-3:])==str(list(d.keys())[j])):
                        ind=j
                        break
                        
                if(ind!=-1 and j<len(list(d.keys()))-1):
                    
                    y = d[list(d.keys())[i]][:-3]+str(list(d.keys())[j+1])
                    d[list(d.keys())[i]]=y
                
            else:
                
                y = "goto "+str(store_incr)
                d[list(d.keys())[i]]=y
        
            trav+=1
     

for i in d:
    print(i, d[i])