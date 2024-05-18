
import sys
# VARIABLES AND DATA DEFINE - INPUT
#file_string="input_assembler_new.txt"
#output_file="output_machine_code.txt"
output_file=""


operation_dict={
    'add': ['00000', 'A', 'Addition'], 
    'sub': ['00001', 'A', 'Subtraction'], 
    'mov': [['00011', 'C', 'Move'],['00010', 'B', 'Move']], 
    'ld': ['00100', 'D', 'Load'],  
    'st': ['00101', 'D', 'Store'], 
    'mul': ['00110', 'A', 'Multiply'], 
    'div': ['00111', 'C', 'Divide'], 
    'rs': ['01000', 'B', 'Right_Shift'], 
    'ls': ['01001', 'B', 'Left_Shift'], 
    'xor': ['01010', 'A', 'Exclusive_OR'], 
    'or': ['01011', 'A', 'Or'], 
    'and': ['01100', 'A', 'And'], 
    'not': ['01101', 'C', 'Invert'], 
    'cmp': ['01110', 'C', 'Compare'], 
    'jmp': ['01111', 'E', 'Uncondition_al_Jump'],
    # 
    '10101': ['ado', 'C', 'Add_one_to_Register'],
    '10110': ['adt', 'C', 'Add_two_to_Register'],
    '10111': ['hlf', 'C', 'Divide_Register_by_two'],
    '10011': ['sbo', 'C', 'Sub_one__from_Register'],
    '10100': ['mpt', 'C', 'Multiply_two_to_Register'], 
    #  
    'jlt': ['11100', 'E', 'Jump_If_Less_Than'], 
    'jgt': ['11101', 'E', 'Jump_If_Greater_Than'], 
    'je': ['11111', 'E', 'Jump_If_Equal'], 
    'addf': ['10000','A','Addition_F'],
    'subf': ['10001','A','Subtraction_F'],
    'movf': ['10010','I','Mov_f'],
    'hlt': ['11010', 'F', 'Halt']
    }




#A --> 3 Reg
#B --> 1 Reg , 1 immd
#C --> 2 Reg
#D --> 1 Reg , 1 MemAddr
#E --> 1 MemAddr
#F --> hlt 




#G --> label
#H --> var

operation_name_list=['add', 'sub', 'mov', 'ld', 'st', 'mul', 'div', 'rs', 'ls', 'xor', 'or', 'and', 'not', 'cmp', 'jmp', 'jlt', 'jgt', 'je','addf','subf','movf' ,'hlt']
operation_opcode_list=['00000', '00001', ['00010','00011'], '00100', '00101', '00110', '00111', '01000', '01001', '01010', '01011', '01100', '01101', '01110', '01111', '11100', '11101', '11111','10000','10001', '10010','11010']

register_dict={
    'R0':"000",
    'R1':"001",
    'R2':"010",
    'R3':"011",
    'R4':"100",
    'R5':"101",
    'R6':"110",
    'FLAGS':"111"
    }


# GLOBAL VARIABLE DEFINE


line_index=1                # to tell the line of input to print the error
memory_index=0              # to tell how much memory is allocated and next memory adress should be


label_dict={}               # dict which contains labels name and there memory location
variable_dict={}            # dict which contains var name and there memory location


label_check_dict={}



immediate_values={}         # to store values of immediate numbers



proc_code_dict={}
proc_code_index=0


hlt_index=-1
hlt_proc_index=-1
hlt_counter=0
hlt_up_bool=True


binary_dict={}


var_bool_end=True
continue_do=True


# FUNCTION DEFINE


    # these are general function except for mov part 

    




def int_to_bin_7(a):                            # function which takes int input and gives its 7 bit bianry representation in string format
    if(a>=0 and a<=127):
        ret_a=""
        while(a):
            ret_a=str(a%2)+ret_a
            a=a//2
        ret_a="0"*(7-len(ret_a))+ret_a
        return ret_a
    else:
        print("Error in Line "+str(line_index)+": memory address limit exceeded")
        continue_do=False
        #raise Exception("Error in Line "+str(line_index)+": memory address limit exceeded") 

def binary_val(s,n):
    i=s
    sk=""
    while i:
        r=i%2
        i=i//2
        sk=sk+str(r)
    sk=sk[::-1]
    ret="0"*(n-len(sk))
    ret=ret+sk
    return ret  
        
def make_list(s):
    z=[]
    k=[]
    z.clear()
    k.clear()
    k=s.split()
    for i in range(0,len(k)):
        k[i]=k[i].strip()
    for i in range(0,len(k)):
        if(k[i]!=""):
            z.append(k[i])
    k=z.copy()
    return k

def float_to_binary(decimal_float):
    binary = ''
    integer_part = int(decimal_float)
    fractional_part = decimal_float - integer_part

    # Convert the integer part to binary
    if integer_part == 0:
        binary += '0'
    else:
        binary += bin(integer_part)[2:]

    binary += '.'

    z=0
    # Convert the fractional part to binary
    while fractional_part != 0:
        if(z>5):
            break
        z=z+1
        fractional_part *= 2
        bit = int(fractional_part)
        binary += str(bit)
        fractional_part -= bit

    return binary




def check_H(s):                                          # function to check if its valid H type 
    global continue_do,var_bool_end
    if var_bool_end:
        k=make_list(s)
        if(len(k)!=2):
            print("Error in Line "+str(line_index)+":var must contain two parameter")
            continue_do=False
            #raise Exception("Error in Line "+str(line_index)+":var must contain two parameter")    
            return 0
        if(k[1] in variable_dict.keys()):
            print("Error in Line "+str(line_index)+":variable name '"+k[1]+"' already exists ")
            continue_do=False
            #raise Exception("Error in Line "+str(line_index)+":variable name '"+k[1]+"' already exists ")   
            return 0        
        else:
            variable_dict[k[1]]=""
        return 1
    else:
        print("Error in Line "+str(line_index)+": var defined after main code it should be initialzed in the begining")
        continue_do=False
        #raise Exception("Error in Line "+str(line_index)+": var defined after main code it should be initialzed in the begining") 

        
        
        
def check_E(s):                                     # function to check if its valid E type
    global continue_do
    k=make_list(s)    
    if(len(k)!=2):
        print("Error in Line "+str(line_index)+": "+k[0]+" must contain 1 parameter")
        continue_do=False
        #raise Exception("Error in Line "+str(line_index)+":"+k[0]+" must contain 1 parameter")    
        return 0
    return 1


    
    
def check_D(s):                                    # function to check if its valid D type
    global continue_do    
    k=make_list(s)
    if((len(k)!=3)):
        print("Error in Line "+str(line_index)+": "+k[0]+" must contain 2 parameter")
        continue_do=False
        #raise Exception("Error in Line "+str(line_index)+":"+k[0]+" must contain 2 parameter")    
        return 0
    if (k[1] not in register_dict.keys() or k[1]=="FLAGS"):
        print("Error in Line "+str(line_index)+":"+" register name '"+k[1]+"' not found")
        continue_do=False
        #raise Exception("Error in Line "+str(line_index)+":"+k[0]+" register name "+ k[1]+" not found")  
        return 0    
    if (k[2] not in variable_dict.keys()):
        print("Error in Line "+str(line_index)+":"+" variable name '"+k[2]+"' not found")
        continue_do=False
        #raise Exception("Error in Line "+str(line_index)+":"+k[0]+" variable name "+k[2]+" not found ")   
        return 0         
    return 1            
    
    
    
    
def check_C(s):                                  # function to check if its valid C type
    global continue_do    
    k=make_list(s)
    if(len(k)!=3):
        print("Error in Line "+str(line_index)+": "+k[0]+" must contain 2 parameter")
        continue_do=False
        #raise Exception("Error in Line "+str(line_index)+":"+k[0]+" must contain 2 parameter")    
        return 0
    if (k[1] not in register_dict.keys() or k[1]=="FLAGS"):
        print("Error in Line "+str(line_index)+":"+" register name '"+k[1]+"' not found")
        continue_do=False
        #raise Exception("Error in Line "+str(line_index)+":"+k[0]+" register name "+ k[1]+" not found")  
        return 0 
    if (k[2] not in register_dict.keys() or k[2]=="FLAGS"):
        print("Error in Line "+str(line_index)+":"+" register name '"+k[2]+"' not found")
        continue_do=False
        #raise Exception("Error in Line "+str(line_index)+":"+k[0]+" register name "+ k[2]+" not found")  
        return 0       
    return 1  




def check_B(s):                                   # function to check if its valid B type
    global continue_do    
    k=make_list(s)
    if((len(k)!=3) ):
        print("Error in Line "+str(line_index)+": "+k[0]+" must contain 2 parameter")
        continue_do=False
        #raise Exception("Error in Line "+str(line_index)+":"+k[0]+" must contain 2 parameter")    
        return 0
    if (k[1] not in register_dict.keys() or k[1]=="FLAGS"):
        print("Error in Line "+str(line_index)+":"+" register name '"+k[1]+"' not found")
        continue_do=False
        #raise Exception("Error in Line "+str(line_index)+":"+" register name '"+k[1]+"' not found") 
        return 0 
    if (k[2][0]!='$'):
        print("Error in Line "+str(line_index)+":"+" no immediate value found immediate value should start with '$'")
        continue_do=False
        #raise Exception("Error in Line "+str(line_index)+":"+" no immediate value found immediate value should start with '$'")
        return 0      
    try:
        z=int(k[2][1:])
        if(z>=0 and z<=127):
            immediate_values[proc_code_index]=[int_to_bin_7(z),z]
        else:
            print("Error in Line "+str(line_index)+": "+"'"+k[2]+"'"+"is not in range that is (0-127)")
            continue_do=False
            #raise Exception("Error in Line "+str(line_index)+": "+"'"+k[2]+"'"+"is not in range that is (0-127)")
            return 0                  
    except:
        print("Error in Line "+str(line_index)+": "+"'"+k[2]+"'"+"is not an integer")
        continue_do=False
        #raise Exception("Error in Line "+str(line_index)+": "+"'"+k[2]+"'"+"is not an integer")
        return 0          
    return 1




def check_A(s):                                     # function to check if its valid A type
    global continue_do    
    k=make_list(s)
    if(len(k)!=4):
        print("Error in Line "+str(line_index)+": "+k[0]+" must contain 3 parameter")
        continue_do=False
        #raise Exception("Error in Line "+str(line_index)+":"+k[0]+" must contain 3 parameter")    
        return 0
    if (k[1] not in register_dict.keys() or k[1]=="FLAGS"):
        print("Error in Line "+str(line_index)+":"+" register name '"+k[1]+"' not found")
        continue_do=False
        #raise Exception("Error in Line "+str(line_index)+": "+k[0]+" register name "+ k[1]+" not found")  
        return 0 
    if (k[2] not in register_dict.keys() or k[2]=="FLAGS"):
        print("Error in Line "+str(line_index)+":"+" register name '"+k[2]+"' not found")
        continue_do=False
        #raise Exception("Error in Line "+str(line_index)+":"+k[0]+" register name "+ k[2]+" not found")  
        return 0  
    if (k[3] not in register_dict.keys() or k[3]=="FLAGS"):
        print("Error in Line "+str(line_index)+":"+" register name '"+k[2]+"' not found")
        continue_do=False
        #raise Exception("Error in Line "+str(line_index)+": "+k[0]+" register name "+ k[3]+" not found")  
        return 0     
    return 1  


def check_I(s):                                   # function to check if its valid B type
    global continue_do    
    k=make_list(s)
    if((len(k)!=3) ):
        print("Error in Line "+str(line_index)+": "+k[0]+" must contain 2 parameter")
        continue_do=False
        #raise Exception("Error in Line "+str(line_index)+":"+k[0]+" must contain 2 parameter")    
        return 0
    if (k[1] not in register_dict.keys() or k[1]=="FLAGS"):
        print("Error in Line "+str(line_index)+":"+" register name '"+k[1]+"' not found")
        continue_do=False
        #raise Exception("Error in Line "+str(line_index)+":"+" register name '"+k[1]+"' not found") 
        return 0 
    if (k[2][0]!='$'):
        print("Error in Line "+str(line_index)+":"+" no immediate value found immediate value should start with '$'")
        continue_do=False
        #raise Exception("Error in Line "+str(line_index)+":"+" no immediate value found immediate value should start with '$'")
        return 0      
    try:
        z=float(k[2][1:])
        if(z>=0 and z<=31):
            k=float_to_binary(z)
            k=str(k)
            k=k+"0"*(6-len(k))
            m1=k.find(".")
            m2=m1-1
            h=k[:m1]+k[m1+1:]
            fghz=binary_val(m2)+h
            immediate_values[proc_code_index]=[fghz,z]
        else:
            print("Error in Line "+str(line_index)+": "+"'"+k[2]+"'"+"is not in range that is (0-31)")
            continue_do=False
            #raise Exception("Error in Line "+str(line_index)+": "+"'"+k[2]+"'"+"is not in range that is (0-127)")
            return 0                  
    except:
        print("Error in Line "+str(line_index)+": "+"'"+k[2]+"'"+"is not an integer")
        continue_do=False
        #raise Exception("Error in Line "+str(line_index)+": "+"'"+k[2]+"'"+"is not an integer")
        return 0          
    return 1



def check_move(s):
    global continue_do,proc_code_index
    k=make_list(s)
    if(len(k)!=3):
        print("Error in Line "+str(line_index)+":"+k[0]+" must contain 2 parameter")
        continue_do=False
        #raise Exception("Error in Line "+str(line_index)+": "+k[0]+" must contain 2 parameter")    
        return 0
    if (k[1] not in register_dict.keys() or k[1]=="FLAGS"):
        print("Error in Line "+str(line_index)+":"+" register name '"+k[1]+"' not found")
        continue_do=False
        #raise Exception("Error in Line "+str(line_index)+": "+k[0]+" register name "+ k[1]+" not found")  
        return 0 
    if(k[2][0]=='$'):
        try:
            z=int(k[2][1:])
            if(z>=0 and z<=127):
                immediate_values[proc_code_index]=[int_to_bin_7(z),z]
                proc_code_dict[proc_code_index].append("B")
            else:
                print("Error in Line "+str(line_index)+": "+"'"+k[2]+"'"+"is not in range that is (0-127)")
                continue_do=False
                #raise Exception("Error in Line "+str(line_index)+": "+"'"+k[2]+"'"+"is not in range that is (0-127)")
                return 0             
        except:
            print("Error in Line "+str(line_index)+": "+"'"+k[2]+"'"+"is not an integer")
            continue_do=False
            #raise Exception("Error in Line "+str(line_index)+": "+"'"+k[2]+"'"+"is not an integer")
            return 0  
    elif(k[2] not in register_dict.keys()):
        print("Error in Line "+str(line_index)+": "+" register name '"+k[2]+"' not found")
        continue_do=False
        #raise Exception("Error in Line "+str(line_index)+": "+k[0]+" register name "+ k[2]+" not found")   
    else:
        proc_code_dict[proc_code_index].append("C")           
    return 1




def read_get_file(list_temp):
    global continue_do,proc_code_index,line_index,hlt_counter,hlt_index,hlt_proc_index,var_bool_end,hlt_up_bool
    mn=list_temp.copy()
    mn_len=len(mn)
    v=0
    while(v<mn_len):
        #print(mn)
        #print("\n")
        line_index=v+1
        mn_str=mn[v]
        if(mn_str !=""):
            k=make_list(mn_str)
            if hlt_up_bool==False:
                hlt_up_bool=True
                print("Error in Line "+str(line_index)+":"+" Can't execute lines after hlt")
                #raise Exception("Error in Line "+str(line_index)+":"+" Can't execute lines after hlt")
                
            if(k[0].count(":")>1):
                var_bool_end=False
                print("Error in Line "+str(line_index)+":"+" no valid syntax or instruction")
                continue_do=False
                #raise Exception("Error in Line "+str(line_index)+":"+" no valid syntax or instruction")                 
            elif(k[0][len(k[0])-1]==':'):
                var_bool_end=False
                if(len(k)==1):
                    mn[v]=""
                    if(k[0][0:len(k[0])-1] not in label_dict.keys()):
                        label_dict[k[0][0:len(k[0])-1]]=int_to_bin_7(proc_code_index)
                    else:
                        continue_do=False
                        print("Error in Line "+str(line_index)+":"+" label name",k[0][0:len(k[0])-1] ,"already exists")
                        #raise Exception("Error in Line "+str(line_index)+":"+"label name",k[0][0:len(k[0])-1] ,"already exists")
                else:
                    if(k[0][0:len(k[0])-1] not in label_dict.keys()):
                        label_dict[k[0][0:len(k[0])-1]]=int_to_bin_7(proc_code_index)
                    else:
                        continue_do=False
                        print("Error in Line "+str(line_index)+":"+" label name",k[0][0:len(k[0])-1] ,"already exists")
                        #raise Exception("Error in Line "+str(line_index)+":"+"label name",k[0][0:len(k[0])-1] ,"already exists")
                    k.pop(0)
                    k=(" ").join(k)
                    mn[v]=k
                    k=k.split()
                    v=v-1
            elif(":"in k[0]):
                var_bool_end=False
                new_1=k[0].split(":")
                k[0]=new_1[1]
                label_dict[new_1[0]]=int_to_bin_7(proc_code_index)
                k=(" ").join(k)
                mn[v]=k
                k=k.split()
                v=v-1                

            elif(k[0]=="var"):
                check_H(mn_str)
            elif(k[0]=="mov"):
                var_bool_end=False
                proc_code_dict[proc_code_index]=[mn_str]
                check_move(mn_str)
                proc_code_index=proc_code_index+1
            elif(k[0] in operation_dict.keys()):
                var_bool_end=False
                tell_type=operation_dict[k[0]][1]
                proc_code_dict[proc_code_index]=[mn_str]
                if(tell_type=='A'):
                    check_A(mn_str)
                    proc_code_dict[proc_code_index].append("A")               
                elif(tell_type=='B'):
                    check_B(mn_str)
                    proc_code_dict[proc_code_index].append("B")
                elif(tell_type=='C'):
                    check_C(mn_str)
                    proc_code_dict[proc_code_index].append("C")
                elif(tell_type=='D'):
                    check_D(mn_str)
                    proc_code_dict[proc_code_index].append("D")          
                elif(tell_type=='E'):
                    label_check_dict[line_index]=k[1]
                    check_E(mn_str)
                    proc_code_dict[proc_code_index].append("E")  
                elif(tell_type=='H'):
                    check_H(mn_str)
                    proc_code_dict[proc_code_index].append("H") 
                elif(tell_type=='I'):
                    check_I(mn_str)
                    proc_code_dict[proc_code_index].append("I") 
                elif(tell_type=='F'):
                    proc_code_dict[proc_code_index].append("F") 
                    if(hlt_index==-1):
                        hlt_index=line_index
                    hlt_up_bool=False
                    hlt_counter=hlt_counter+1
                    hlt_proc_index=proc_code_index
                proc_code_index=proc_code_index+1
            else:
                print("Error in Line "+str(line_index)+":"+" no valid syntax or instruction ")
                continue_do=False
                #raise Exception("Error in Line "+str(line_index)+":"+" no valid syntax or instruction ")               
        v=v+1

    if(hlt_proc_index==-1):
        print("No Hlt Statement Or Instruction In The Code")
        continue_do=False
        #raise Exception("No Hlt Statement Or Instruction In The Code")
    elif(hlt_counter>1):
        print("Error in Line "+str(line_index)+":"+" hlt instruction appeared in the middle of the code")
        continue_do=False
        #raise Exception("Error in Line "+str(line_index)+":"+" hlt instruction appeared in the middle of the code")

    for i in label_check_dict.keys():
        if(label_check_dict[i] not in label_dict.keys()):
            print("Error in Line "+str(i)+":"+" label named '"+label_check_dict[i] +"' not found")
            continue_do=False
            #raise Exception("Error in Line "+str(i)+":"+"label named '"+label_check_dict[i] +"' not found")  

            
            

            
            
def assign_variable_address():
    z=0
    for i in variable_dict.keys():
        variable_dict[i]=int_to_bin_7(proc_code_index+z)
        z=z+1



        
def create_binary_dict():
    global output_file
    if continue_do:
        for i in proc_code_dict.keys():
            main_str=""
            k=make_list(proc_code_dict[i][0])
            type_str=proc_code_dict[i][1]
            if type_str=='A':
                main_str=main_str+operation_dict[k[0]][0]
                main_str=main_str+"0"*2
                main_str=main_str+register_dict[k[1]]
                main_str=main_str+register_dict[k[2]]
                main_str=main_str+register_dict[k[3]]
            elif type_str=='B':
                if k[0]=="mov":
                    main_str=main_str+operation_dict[k[0]][1][0]
                    main_str=main_str+"0"*1
                    main_str=main_str+register_dict[k[1]]
                    main_str=main_str+immediate_values[i][0]
                else:
                    main_str=main_str+operation_dict[k[0]][0]
                    main_str=main_str+"0"*1
                    main_str=main_str+register_dict[k[1]]
                    main_str=main_str+immediate_values[i][0]
            elif type_str=='C':
                if k[0]=="mov":
                    main_str=main_str+operation_dict[k[0]][0][0]
                    main_str=main_str+"0"*5
                    main_str=main_str+register_dict[k[1]]
                    main_str=main_str+register_dict[k[2]]
                else:
                    main_str=main_str+operation_dict[k[0]][0]
                    main_str=main_str+"0"*5
                    main_str=main_str+register_dict[k[1]]
                    main_str=main_str+register_dict[k[2]]
            elif type_str=='D':
                main_str=main_str+operation_dict[k[0]][0]
                main_str=main_str+"0"*1
                main_str=main_str+register_dict[k[1]]
                if(k[2] in label_dict.keys()):
                    main_str=main_str+label_dict[k[2]]
                elif(k[2] in variable_dict.keys()):
                    main_str=main_str+variable_dict[k[2]]   
            elif type_str=='E':
                main_str=main_str+operation_dict[k[0]][0]
                main_str=main_str+"0"*4
                if(k[1] in label_dict.keys()):
                    main_str=main_str+label_dict[k[1]]
                elif(k[1] in variable_dict.keys()):
                    main_str=main_str+variable_dict[k[1]] 
            elif type_str=='I':
                main_str=main_str+operation_dict[k[0]][0]    
                main_str=main_str+register_dict[k[1]]
                main_str=main_str+immediate_values[i][0]        
            elif type_str=='F':
                main_str=main_str+operation_dict[k[0]][0]
                main_str=main_str+"0"*11
            binary_dict[i]=main_str 
    else:
        write_binary_file(output_file)
        raise Exception("Code Terminated Due To Above Reason")




        
def write_binary_file(file_temp):
    #file_output=open(file_temp,"w+")
    if continue_do==True:
        for i in binary_dict.keys():
            #file_output.write(binary_dict[i]+"\n")
            print(binary_dict[i])
    #file_output.close()

    

    
# CODE RUN

 
code_list=[line.strip() for line in sys.stdin.readlines()]
read_get_file(code_list)

#print("\n",code_list,"\n")
#print("\n",label_dict,"\n")
#print("\n",variable_dict,"\n")


assign_variable_address()


#print("\n",variable_dict,"\n")
#print("\n",proc_code_dict,"\n")
#print("\n",binary_dict,"\n")


create_binary_dict()


#print("\n",binary_dict,"\n")


write_binary_file(output_file)


#print("\n")
