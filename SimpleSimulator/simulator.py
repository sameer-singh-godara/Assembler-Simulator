import sys
input_file="input_simulator"
output_file="output_simulator"

operation_dict={
    '00000': ['add', 'A', 'Addition'], 
    '00001': ['sub', 'A', 'Subtraction'], 
    '00011': ['mov', 'C', 'Move'], 
    '00010': ['mov', 'B', 'Move'], 
    '00100': ['ld', 'D', 'Load'], 
    '00101': ['st', 'D', 'Store'], 
    '00110': ['mul', 'A', 'Multiply'], 
    '00111': ['div', 'C', 'Divide'], 
    '01000': ['rs', 'B', 'Right_Shift'], 
    '01001': ['ls', 'B', 'Left_Shift'], 
    '01010': ['xor', 'A', 'Exclusive_OR'], 
    '01011': ['or', 'A', 'Or'], 
    '01100': ['and', 'A', 'And'], 
    '01101': ['not', 'C', 'Invert'], 
    '01110': ['cmp', 'C', 'Compare'], 
    '01111': ['jmp', 'E', 'Uncondition_al_Jump'],
    # 
    '10101': ['ado', 'C', 'Add_one_to_Register'],
    '10110': ['adt', 'C', 'Add_two_to_Register'],
    '10111': ['hlf', 'C', 'Divide_Register_by_two'],
    '10011': ['sbo', 'C', 'Sub_one__from_Register'],
    '10100': ['mpt', 'C', 'Multiply_two_to_Register'], 
    #  
    '11100': ['jlt', 'E', 'Jump_If_Less_Than'], 
    '11101': ['jgt', 'E', 'Jump_If_Greater_Than'], 
    '11111': ['je', 'E', 'Jump_If_Equal'], 
    '10000': ['addf','A','Addition_F'],
    '10001': ['subf','A','Subtraction_F'],
    '10010': ['movf','I','Mov_f'],    
    '11010': ['hlt', 'F', 'Halt']
    }

#A --> 3 Reg                    00000 00            000 000 000
#B --> 1 Reg , 1 immd           00000 0             000 0000000
#C --> 2 Reg                    00000 00000         000 000
#D --> 1 Reg , 1 MemAddr        00000 0             000 0000000
#E --> 1 MemAddr                00000 0000          0000000
#F --> hlt                      00000 00000000000

#G --> label
#H --> var

register_arr={"000":0, "001":0, "010":0, "011":0, "100":0, "101":0, "110":0, "111":0}
register_fract={"000":1.0, "001":1.0, "010":1.0, "011":1.0, "100":1.0, "101":1.0, "110":1.0, "111":1.0}
register_dict={ "000":[0,"R0"], "001":[0,"R1"], "010":[0,"R2"], "011":[0, "R3"],"100":[0,"R4"], "101":[0,"R5"], "110":[0,"R6"], "111":[0,"FLAGS"]}

label_dict={}
var_dict={}

#file_input=open(input_file,'r')
#file_output=open(output_file,'w')


list_input=[line.strip() for line in sys.stdin.readlines()]

        
halt=False
program_counter=0
pc_binary=""
flag="0000000000000000"


def bin_to_int(s):
    ret=0
    s=s[::-1]
    for i in range(0,len(s)):
        ret=ret+(2**i)*(int(s[i]))
    return ret




for i in list_input:
    if i[0:5] in operation_dict.keys():
        if operation_dict[i[0:5]][1]=='D':
            var_dict[i[len(i)-7:len(i)]]=0
        elif operation_dict[i[0:5]][1]=='E':
            label_dict[i[len(i)-7:len(i)]]=bin_to_int(i[len(i)-7:len(i)])


def make_list(l):
    temp_dict={}
    o_type=''
    m=0
    for i in l:
        o_type=operation_dict[i[0:5]][1]
        if(o_type=='A'):
            temp_dict[m]=[i[0:5],i[7:10],i[10:13],i[13:]]
        elif(o_type=='B'):
            temp_dict[m]=[i[0:5],i[6:9],i[9:]]
        elif(o_type=='C'):
            temp_dict[m]=[i[0:5],i[10:13],i[13:]]
        elif(o_type=='D'):
            temp_dict[m]=[i[0:5],i[6:9],i[9:]]
        elif(o_type=='E'):
            temp_dict[m]=[i[0:5],i[9:]]
        elif(o_type=='I'):
            temp_dict[m]=[i[0:5],i[5:8],i[8:]]
        elif(o_type=='F'):
            temp_dict[m]=[i[0:5]]
        m=m+1
    return temp_dict
        
code_dict=make_list(list_input).copy()


def register_file(s):
    return register_dict[s][0]

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


def bin_to_frac(s):
    e=s[:3]
    m=s[3:]
    e1=int(e,2)
    k1=m[:e1]+"."+m[e1:]
    k1="1"+k1

    l=k1.split(".")
    real=l[0]
    dec=l[1]
    print(l)
    val=0.0
    for i in range (0,len(dec)):
        val=val+float(dec[i])*(2**(-(i+1)))
    bin1=int(real,2)
    bin1=float(bin1)
    ret=bin1+val
    return ret

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

    # Convert the fractional part to binary
    while fractional_part != 0:
        fractional_part *= 2
        bit = int(fractional_part)
        binary += str(bit)
        fractional_part -= bit

    return binary




def execute(pc):
    global flag,program_counter,halt
    opt=operation_dict[code_dict[pc][0]][0]
    if(opt=='add'):
        temp_rd=code_dict[pc][1]
        temp_rs1=register_file(code_dict[pc][2])
        temp_rs2=register_file(code_dict[pc][3])
        program_counter=program_counter+1
        if(temp_rs1+temp_rs2<=127 and temp_rs1+temp_rs2>=0):
            register_dict[temp_rd][0]=temp_rs1+temp_rs2
            flag="0000000000000000"
            register_dict["111"][0]=0
        else:
            register_dict[temp_rd][0]=0;
            register_dict["111"][0]=8;
            flag="0000000000001000"
    elif(opt=='sub'):
        temp_rd=code_dict[pc][1]
        temp_rs1=register_file(code_dict[pc][2])
        temp_rs2=register_file(code_dict[pc][3])
        program_counter=program_counter+1
        if(temp_rs1-temp_rs2<=127 and temp_rs1-temp_rs2>=0 and temp_rs1>=temp_rs2):
            register_dict[temp_rd][0]=temp_rs1+temp_rs2
            flag="0000000000000000"
            register_dict["111"][0]=0
        else:
            register_dict[temp_rd][0]=0;
            register_dict["111"][0]=8;
            flag="0000000000001000"        
    elif(opt=='mov' and operation_dict[code_dict[pc][0]][1]=='C'):
        temp_rd=code_dict[pc][1]
        temp_rs1=register_file(code_dict[pc][2])
        register_dict[temp_rd][0]=temp_rs1
        flag="0000000000000000"
        register_dict["111"][0]=0
        program_counter=program_counter+1
    elif(opt=='mov' and operation_dict[code_dict[pc][0]][1]=='B'):
        temp_rd=code_dict[pc][1]
        temp_imm=bin_to_int(code_dict[pc][2])
        register_dict[temp_rd][0]=temp_imm
        flag="0000000000000000"
        register_dict["111"][0]=0
        program_counter=program_counter+1
    elif(opt=='ld' and operation_dict[code_dict[pc][0]][1]=='D'):
        temp_rd=code_dict[pc][1]
        temp_mem=var_dict[code_dict[pc][2]]
        register_dict[temp_rd][0]=temp_mem
        flag="0000000000000000"
        register_dict["111"][0]=0
        program_counter=program_counter+1     
    elif(opt=='st' and operation_dict[code_dict[pc][0]][1]=='D'):
        temp_rd=register_file(code_dict[pc][1])
        var_dict[code_dict[pc][2]]=temp_rd 
        flag="0000000000000000"
        register_dict["111"][0]=0
        program_counter=program_counter+1
    elif(opt=='mul'):
        temp_rd=code_dict[pc][1]
        temp_rs1=register_file(code_dict[pc][2])
        temp_rs2=register_file(code_dict[pc][3])
        program_counter=program_counter+1
        if(temp_rs1*temp_rs2<=127 and temp_rs1*temp_rs2>=0 ):
            register_dict[temp_rd][0]=temp_rs1*temp_rs2
            flag="0000000000000000"
            register_dict["111"][0]=0
        else:
            register_dict[temp_rd][0]=0;
            register_dict["111"][0]=8;
            flag="0000000000001000"   
    elif(opt=='div'):
        temp_rs1=register_file(code_dict[pc][1])
        temp_rs2=register_file(code_dict[pc][2])
        program_counter=program_counter+1
        if temp_rs2>0:
            register_dict["000"][0]=temp_rs1//temp_rs2
            register_dict["000"][1]=temp_rs1%temp_rs2  
            flag="0000000000000000"
            register_dict["111"][0]=0          
        else:
            register_dict["000"][0]=0
            register_dict["000"][1]=0
            register_dict["111"][0]=8;
            flag="0000000000001000"            
    elif(opt=='xor'):
        temp_rd=code_dict[pc][1]
        temp_rs1=register_file(code_dict[pc][2])
        temp_rs2=register_file(code_dict[pc][3])
        program_counter=program_counter+1
        flag="0000000000000000"
        register_dict["111"][0]=0
        register_dict[temp_rd][0]=temp_rs1^temp_rs2
    elif(opt=='or'):
        temp_rd=code_dict[pc][1]
        temp_rs1=register_file(code_dict[pc][2])
        temp_rs2=register_file(code_dict[pc][3])
        flag="0000000000000000"
        register_dict["111"][0]=0
        program_counter=program_counter+1
        register_dict[temp_rd][0]=temp_rs1 | temp_rs2
    elif(opt=='and'):
        temp_rd=code_dict[pc][1111]
        temp_rs1=register_file(code_dict[pc][2])
        temp_rs2=register_file(code_dict[pc][3])
        flag="0000000000000000"
        register_dict["111"][0]=0
        program_counter=program_counter+1
        register_dict[temp_rd][0]=temp_rs1 & temp_rs2
    elif(opt=='not'):
        temp_rd=code_dict[pc][1]
        temp_rs1=register_file(code_dict[pc][2])
        program_counter=program_counter+1
        flag="0000000000000000"
        register_dict["111"][0]=0
        register_dict[temp_rd][0]=~temp_rs1 
    elif(opt=='cmp'):
        temp_rd=register_file(code_dict[pc][1])
        temp_rs1=register_file(code_dict[pc][2])
        program_counter=program_counter+1
        if(temp_rd==temp_rs1):
            flag="0000000000000001"
            register_dict["111"][0]=1;
        elif(temp_rd<temp_rs1):
            flag="0000000000000100"
            register_dict["111"][0]=4;
        elif(temp_rd>temp_rs1):
            flag="0000000000000010"      
            register_dict["111"][0]=2;  
    elif(opt=='jmp'):
        temp_label=code_dict[pc][1]
        flag="0000000000000000"
        register_dict["111"][0]=0
        program_counter=label_dict[temp_label]
    elif(opt=='jlt'):
        temp_label=code_dict[pc][1]
        if(flag[13]=="1"):
            program_counter=label_dict[temp_label]
            flag="0000000000000000"
            register_dict["111"][0]=0
        else:
            program_counter=program_counter+1
            flag="0000000000000000"
            register_dict["111"][0]=0
    elif(opt=='jgt'):
        temp_label=code_dict[pc][1]
        if(flag[14]=="1"):        
            program_counter=label_dict[temp_label]
            flag="0000000000000000"
            register_dict["111"][0]=0            
        else:
            flag="0000000000000000"
            register_dict["111"][0]=0
            program_counter=program_counter+1
    elif(opt=='je'):
        temp_label=code_dict[pc][1]
        if(flag[15]=="1"):  
            flag="0000000000000000"
            register_dict["111"][0]=0 
            program_counter=label_dict[temp_label]
        else:
            flag="0000000000000000"
            register_dict["111"][0]=0
            program_counter=program_counter+1
    elif(opt=="addf"):
        temp_rd=code_dict[pc][1]
        temp_rs1=register_file(code_dict[pc][2])
        temp_rs2=register_file(code_dict[pc][3])
        mb1=binary_val(temp_rs1,7)  
        mb2=binary_val(temp_rs2,7)
        mb1=str(register_arr[temp_rs1])+mb1
        mb2=str(register_arr[temp_rs2])+mb2
        fb1=bin_to_frac(mb1)
        fb2=bin_to_frac(mb2)
        fbr=fb1+fb2
        k=float_to_binary(fbr)

        k=str(k)
        k=k+"0"*(6-len(k))
        m1=k.find(".")
        m2=m1-1
        h=k[:m1]+k[m1+1:]
        bin_m2=binary_val(m2,3)
        final=bin_m2[1:]+h
        program_counter=program_counter+1
        if(fbr<=31 and fbr>=1):
            register_arr[temp_rd]=bin_m2[0]
            register_dict[temp_rd][0]=bin_to_int(final)
            flag="0000000000000000"
            register_dict["111"][0]=0
        else:
            register_dict[temp_rd][0]=0
            register_arr[temp_rd]=0          
            register_dict["111"][0]=8
            flag="0000000000001000"        
    elif(opt=="subf"):
        temp_rd=code_dict[pc][1]
        temp_rs1=register_file(code_dict[pc][2])
        temp_rs2=register_file(code_dict[pc][3])
        mb1=binary_val(temp_rs1,7)  
        mb2=binary_val(temp_rs2,7)
        mb1=str(register_arr[temp_rs1])+mb1
        mb2=str(register_arr[temp_rs2])+mb2
        fb1=bin_to_frac(mb1)
        fb2=bin_to_frac(mb2)
        fbr=fb1-fb2
        k=float_to_binary(fbr)

        k=str(k)
        k=k+"0"*(6-len(k))
        m1=k.find(".")
        m2=m1-1
        h=k[:m1]+k[m1+1:]
        bin_m2=binary_val(m2,3)
        final=bin_m2[1:]+h
        program_counter=program_counter+1
        if(fbr<=31 and fbr>=1):
            register_arr[temp_rd]=bin_m2[0]
            register_dict[temp_rd][0]=bin_to_int(final)
            flag="0000000000000000"
            register_dict["111"][0]=0
        else:
            register_dict[temp_rd][0]=0
            register_arr[temp_rd]=0          
            register_dict["111"][0]=8
            flag="0000000000001000"
    elif(opt=="movf"):
        temp_rd=code_dict[pc][1]  
        imm_val=code_dict[pc][2]     
        register_arr[temp_rd]=imm_val[0]
        register_dict[temp_rd][0]=bin_to_int(imm_val[1:])
        flag="0000000000000000"
        register_dict["111"][0]=0
        program_counter=program_counter+1

    elif(opt=='ado'):
        temp_rd=code_dict[pc][1]
        temp_rs1=register_file(code_dict[pc][2])
        program_counter=program_counter+1
        if(temp_rs1+1<=127 and temp_rs1+1>=0):
            register_dict[temp_rd][0]=temp_rs1+1
            flag="0000000000000000"
            register_dict["111"][0]=0
        else:
            register_dict[temp_rd][0]=0;
            register_dict["111"][0]=8;
            flag="0000000000001000"
    elif(opt=='adt'):
        temp_rd=code_dict[pc][1]
        temp_rs1=register_file(code_dict[pc][2])
        program_counter=program_counter+1
        if(temp_rs1+1<=127 and temp_rs1+1>=0):
            register_dict[temp_rd][0]=temp_rs1+1
            flag="0000000000000000"
            register_dict["111"][0]=0
        else:
            register_dict[temp_rd][0]=0;
            register_dict["111"][0]=8;
            flag="0000000000001000"
    elif(opt=='mpt'):
        temp_rd=code_dict[pc][1]
        temp_rs1=register_file(code_dict[pc][2])
        program_counter=program_counter+1
        if(temp_rs1*2<=127 and temp_rs1*2>=0 ):
            register_dict[temp_rd][0]=temp_rs1*2
            flag="0000000000000000"
            register_dict["111"][0]=0
        else:
            register_dict[temp_rd][0]=0;
            register_dict["111"][0]=8;
            flag="0000000000001000"
    elif(opt=='hlf'):
        temp_rs1=register_file(code_dict[pc][1])
        temp_rs2=2
        program_counter=program_counter+1
        if temp_rs2>0:
            register_dict["000"][0]=temp_rs1//temp_rs2
            register_dict["000"][1]=temp_rs1%temp_rs2  
            flag="0000000000000000"
            register_dict["111"][0]=0          
        else:
            register_dict["000"][0]=0
            register_dict["000"][1]=0
            register_dict["111"][0]=8;
            flag="0000000000001000"
    elif(opt=='sbo'):
        temp_rd=code_dict[pc][1]
        temp_rs1=register_file(code_dict[pc][2])
        temp_rs2=1
        program_counter=program_counter+1
        if(temp_rs1-temp_rs2<=127 and temp_rs1-temp_rs2>=0 and temp_rs1>=temp_rs2):
            register_dict[temp_rd][0]=temp_rs1+temp_rs2
            flag="0000000000000000"
            register_dict["111"][0]=0
        else:
            register_dict[temp_rd][0]=0;
            register_dict["111"][0]=8;
            flag="0000000000001000"
    
    elif(opt=='hlt'):
        halt=True

new_progm=0

while not halt:
    #file_output.write(binary_val(new_progm,7)+"        ")
    execute(program_counter)
    print(binary_val(new_progm,7),end="        ")
    for i in register_dict.keys():
        if(i!="111"):
            a_register=binary_val(register_dict[i][0],16)
            am_register=a_register[:8]
            am_register=am_register+str(register_arr[i])
            am_register=am_register+a_register[9:]
            #file_output.write(am_register+" ")
            print(binary_val(register_dict[i][0],16),end=" ")
    #file_output.write(flag+"\n")
    print(flag)
    new_progm=program_counter
    


count_z1=0
for i in list_input:
    print(i)
    count_z1=count_z1+1
for i in var_dict:
    print(binary_val(var_dict[i],16))
    count_z1=count_z1+1
for i in range(1,128-count_z1):
    print("0000000000000000")
print("0000000000000000",end="")    


"""
count_z1=0
for i in list_input:
    file_output.write(i+"\n")
    count_z1=count_z1+1

for i in var_dict:
    file_output.write(binary_val(var_dict[i],16)+"\n")
    count_z1=count_z1+1

for i in range(1,128-count_z1):
    file_output.write("0000000000000000"+"\n")

file_output.write("0000000000000000") 
file_output.close()
  
"""
#print(code_dict)
#print()
#print(label_dict)
#print() 
#print(var_dict)
#print()
#print(bin_to_int("101010"))
