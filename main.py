with open("in.txt","rt") as textFile:
    progArr = [line.split() for line in textFile] # read the programm in an array
with open("instructions.txt","rt") as textFile:
    instructions = [line.split() for line in textFile] #read instructions
symbols=[]
pcArr=[]
lttArr=[]
pass2=[]


# checks if it's format 1, 2, or 3/4 or 5/6
def checkformat(stringaya):
    if stringaya == 'BYTE' or stringaya == 'WORD' or stringaya == 'RESB' or stringaya == 'RESW' or stringaya == 'BASE' or stringaya == 'LTORG' or stringaya == '*' :
        return stringaya
    for i in range(len(instructions)):
        if instructions[i][0] == stringaya or instructions[i][0] == stringaya[1:]:
            # print(instructions[i][0])
            # print(instructions[i][1])
            if instructions[i][1]=='34':
                if stringaya[0]=='+' or stringaya[0]=='$': # format 4 and 6
                    return '4'
                else:  # format 3 and 5
                    return '3'
            else:
                return instructions[i][1] # format 2 and 1
    return ''


def getinstruction(arr):
    if checkformat(arr[0]) != '' :
        return checkformat(arr[0])
    return checkformat(arr[1])



def arr_of_ltorg(progArr):
    temparr=[]
    i=0
    j=0
    c=0
    k=0
    newarr=[]
    for i in range(len(progArr)):
        newarr.append(progArr[i])
        if len(progArr[i]) == 3:
            if progArr[i][2][0]== '=':
                temparr.append(progArr[i][2])
        elif progArr[i][0] == 'LTORG' or progArr[i][0] == 'END':
            for c in range(0,len(temparr),1):
               newarr.append(['*',temparr[c]])
            temparr=[]
    progArr=newarr
    return progArr




def objectcode(progArr,symbols,instructions):
    opcode = ''
    opcodebin=0
    xbit=''
    bp='01'
    e='0'
    f4=''
    f5=''
    f6=''
    xvalue=0
    # pass2[0]=''
    for i in range(1, len(progArr), 1):
        x=0
        ni= '11'
        if checkformat(progArr[i][0])=='':
            x=1
        # print(progArr[i])
        # print(progArr[i][x])
        for j in range(len(instructions)):
            # print(instructions[i][0])
            if instructions[j][0] ==progArr[i][x] or (instructions[j][0] == progArr[i][x][1:] and (progArr[i][x][0]=='+' or progArr[i][x][0]=='$' )):
                if getinstruction(progArr[i]) == '1' or getinstruction(progArr[i]) == '2':
                    opcodebin = hex(int(instructions[j][2], 16)).split('x')[-1].upper()
                    opcode = str(opcodebin)
                else:
                    opcodebin = bin(int(instructions[j][2],16)).split('b')[-1].upper()
                    opcode = str(opcodebin).zfill(8)



            # for j in range(len(symbols)):
            #     if progArr[i][x+1]== symbols[j][0]:
            #         opcode=opcode + symbols[j][1]

        if getinstruction(progArr[i]) == '2':
            lt=progArr[i][x+1]
            if len(lt) == 3:
                # opcode= opcode + convert(letters(lt[0]),4) + convert(letters(lt[2]),4)
                opcode = opcode + hex(int(convert(letters(lt[0]),4), 2)).split('x')[-1].upper()+hex(int(convert(letters(lt[2]),4), 2)).split('x')[-1].upper()
            else:
                opcode= opcode + hex(int(convert(letters(lt[0]),4), 2)).split('x')[-1].upper() + '0'

        if getinstruction(progArr[i]) == '3':
            opcode = opcode[0:6]
            if len(progArr[i]) != 1:
                if progArr[i][x+1][0] == '#':  # we sit the n-i if it has immediate
                    ni = '01'
                    bp='00'
                elif progArr[i][x+1][0] == '@':  # same if it has indirect
                    ni = '10'
                else:  # the default case
                    ni = '11'
                if ',X' in progArr[i][x+1]:
                    xbit = '1'
                else:
                    xbit = '0'
                if(xbit == '1'):
                    displacement = (getadd(progArr[i][x + 1]) - pcArr[i]) + xvalue

                else:
                    displacement = getadd(progArr[i][x+1])-pcArr[i]
                    # print(displacement)

                if(displacement<=2048 and displacement>=-2047):
                    bp='01'
                else:
                    bp='10'
                if (displacement > 2048 or displacement < -2047):
                    displacement = getadd(progArr[i][x+1])-int(getBase(),16)
                    if (xbit == '1'):
                        displacement = displacement + xvalue


                opcode = hex(int(opcode + ni + xbit + bp + e , 2)).split('x')[-1].upper().zfill(3) + str(hex(displacement).split('x')[-1].upper()).zfill(3)
                # opcode =hex(displacement).split('x')[-1].upper().zfill(3)
                # if '+' in progArr[i][x+1]:  # if it's a format 4, e=1
                #     e = '1'
                # else:  # format 3
                #     e = '0'

        if getinstruction(progArr[i]) == '4' and progArr[i][x][0] =='$' :  # format 6
             opcode = opcode[0:6]
             if len(progArr[i]) != 1:
                 if progArr[i][x + 1][0] == '#':  # we sit the n-i if it has immediate
                     ni = '01'

                 elif progArr[i][x + 1][0] == '@':  # same if it has indirect
                     ni = '10'
                 else:  # the default case
                     ni = '11'
                 if ',X' in progArr[i][x + 1]:
                     xbit = '1'
                 else:
                     xbit = '0'
                 if (xbit == '1'):
                     address = (getadd(progArr[i][x + 1]) ) + xvalue

                 else:
                     address = getadd(progArr[i][x + 1])
                     # print(displacement)

                 if(address % 2 == 0):
                     f4='0'
                 else:
                     f4='1'
                 if (address  == 0):
                     f5 = '0'
                 else:
                     f5 = '1'
                 if (address  == getBase()):
                     f6 = '0'
                 else:
                     f6 = '1'

                 opcode = hex(int(opcode + ni + xbit + f4 + f5 + f6, 2)).split('x')[-1].upper().zfill(3) + str(hex(address).split('x')[-1].upper().zfill(5))

        if getinstruction(progArr[i]) == 'BYTE':
            if progArr[i][x + 1][0] == 'X':
                opcode = progArr[i][x + 1][2:len(progArr[i][x + 1])-1]
            elif progArr[i][x + 1][0] == 'C':
                opcode = getascii(progArr[i][x + 1][2:len(progArr[i][x + 1])-1])

        if getinstruction(progArr[i]) == 'WORD':
            wvalue = int(progArr[i][2])
            opcode = str(hex(wvalue).split('x')[-1].upper().zfill(6))

        if progArr[i][0] == 'RSUB' :
            opcode = '4C0000'


        pass2.append(opcode)
        # print(opcode)
        opcode= ''

def convert(x,y):
    result = str(bin(x)).split('b')[-1].upper().zfill(y)
    return result

def letters(c):
    n=0
    if c == 'A':
        n=0
    elif c == 'X':
        n = 1
    elif c == 'L':
        n = 2
    elif c == 'B':
        n = 3
    elif c == 'S':
        n = 4
    elif c == 'T':
        n = 5
    elif c == 'F':
        n = 6
    return n

def getBase():
    for i in range(len(progArr)):
        if(progArr[i][0]=='BASE'):
            baseVar = progArr[i][1]
            c = getadd(baseVar)
            c = hex(int(c)).split('x')[-1].upper()
            return c




def getltt():
        for i in range(len(progArr)):
            if(progArr[i][0]=='*'):
                lttArr.append([progArr[i][1],pcArr[i-1]])
        # print(lttArr)


def getadd(smb):
    if ',X' in smb:
        smb = smb[0:len(smb)-2]
    if '@' in smb:
        smb = smb[1:len(smb)]
    for i in range(0, len(symbols), 1):
        if symbols[i][0] == smb:
            return symbols[i][1]
    for i in range(0, len(lttArr), 1):
        if lttArr[i][0] == smb:
            return lttArr[i][1]

def getascii(chars):
    ascii=''
    for i in range(len(chars)):
        if chars[i]=='E':
            ascii=ascii + '45'
        elif chars[i]=='O':
            ascii=ascii + '4F'
        elif chars[i]=='F':
            ascii=ascii + '46'
    return ascii


def HTME_rec():
    Hrec = 'H.' + progArr[0][0].zfill(6) + '.' + progArr[0][2].zfill(6) + '.' + str(hex(pcArr[len(pcArr)-1]+1-int(progArr[0][2],16)).split('x')[-1].upper()).zfill(6)
    Erec = 'E.' + progArr[0][2].zfill(6)
    Trec = []
    j=0
    sf=0
    current_length=0
    current_T = []
    arr_of_pc=[]
    Tstring=''

    for i in range(1,len(progArr),1):


        if sf == 0 :
            if pass2[i-1] != '':
                current_T.append(pass2[i-1].zfill(6))

            if i == 1 :
                arr_of_pc.append(int(progArr[0][2],16))
            else:
                arr_of_pc.append(pcArr[i - 1])

            if len(arr_of_pc) >= 2 :
                current_length=arr_of_pc[len(arr_of_pc)-1]-arr_of_pc[0]


        if current_length > 30 :
            i = i-1
            arr_of_pc= arr_of_pc[0:len(arr_of_pc)-1]
            current_T =  current_T[0:len(current_T)-1]
            current_length = arr_of_pc[len(arr_of_pc) - 1] - arr_of_pc[0]
            sf = 1
            j = j + 1

        if sf == 1 or i == len(progArr)-1 :
            # print(current_length)
            # print(arr_of_pc)
            # print(current_T)
            Tstring = 'T.' + str(hex(current_length).split('x')[-1].upper())
            for c in range(len(current_T)):
                Tstring = Tstring + '.' + current_T[c].zfill(6)
            Trec.append(Tstring)
            current_length = 0
            current_T = []
            arr_of_pc=[]
            sf = 0


    fout = open("HTE.txt", "wt")
    fout.write(Hrec)
    fout.write('\n')
    for i in range(len(Trec)):
        fout.write(Trec[i])
        fout.write('\n')
    fout.write(Erec)
    fout.write('\n')


def getPass1():
    global pcArr
    pcArr=[0 for _ in range(len(progArr))]
    temp = int(progArr[0][2], 16)
    temp = int(progArr[0][2], 16)
    fout = open("out.txt", "wt")
    fout1 = open("symbol.txt", "wt")
    fout.write('\t' + progArr[0][0] + '\t' + progArr[0][1] + '\t' + progArr[0][2] + '\t' + 'Object Code')
    fout.write('\n')
    for i in range(1, len(progArr), 1):
        counter = hex(int(temp)).split('x')[-1].upper()
        if progArr[i][0] != 'BASE' and progArr[i][0] != 'LTORG' :
            if len(progArr[i]) == 1:
                fout.write(str(counter).zfill(4) + '\t' + '\t' + progArr[i][0])
                fout.write('\n')
            elif progArr[i][0] == '*':
                fout.write(str(counter).zfill(4) + '\t' + progArr[i][0] + '\t' + progArr[i][1])
                fout.write('\n')
            elif len(progArr[i]) == 2:
                fout.write(str(counter).zfill(4) + '\t' + '\t' + progArr[i][0] + '\t' + progArr[i][1])
                fout.write('\n')
            elif len(progArr[i]) == 3:
                fout.write(str(counter).zfill(4) + '\t' + progArr[i][0] + '\t' + progArr[i][1] + '\t' + progArr[i][2])
                fout.write('\n')
        else:
            if len(progArr[i]) == 1:
                fout.write('\t' + '\t' + progArr[i][0])
                fout.write('\n')
            elif len(progArr[i]) == 2:
                fout.write('\t' + '\t' + progArr[i][0] + '\t' + progArr[i][1])
                fout.write('\n')

        if checkformat(progArr[i][0])=='' and progArr[i][0]!='END':
            symbols.append([progArr[i][0],temp])
            fout1.write(progArr[i][0]+' '+counter + '\n')

        if getinstruction(progArr[i]) == '1':
            temp = temp + 1
        elif getinstruction(progArr[i]) == '2':
            temp = temp + 2
        elif getinstruction(progArr[i]) == '3':
            temp = temp + 3
        elif getinstruction(progArr[i]) == '4':
            temp = temp + 4
        elif 'BYTE' in getinstruction(progArr[i]):
            if progArr[i][2][0] == 'X' :
                temp = temp + (len(progArr[i][2])-3)//2
            elif progArr[i][2][0] == 'C' :
                temp = temp + (len(progArr[i][2])-3)
        elif '*' in getinstruction(progArr[i]):
            if progArr[i][1][1] == 'X' :
                temp = temp + (len(progArr[i][1])-4)//2
            elif progArr[i][1][1] == 'C' :
                temp = temp + (len(progArr[i][1])-4)
        elif 'WORD' in getinstruction(progArr[i]):
            temp = temp + 3
        elif 'RESB' in getinstruction(progArr[i]):
            temp = temp + int(progArr[i][2])
        elif 'RESW' in getinstruction(progArr[i]):
            temp = temp + int(progArr[i][2]) * 3
        else:
            temp = temp + 0
        pcArr[i]=temp
        # print(pcArr)


progArr=arr_of_ltorg(progArr)
getPass1()
getltt()
objectcode(progArr,symbols,instructions)
HTME_rec()


line_code=''

fout = open("out.txt", "wt")
fout.write('\t' + progArr[0][0] + '\t' + progArr[0][1] + '\t' + progArr[0][2] + '\t' + '\t' + 'Object Code')
fout.write('\n')
for i in range(1, len(progArr), 1):
    if i == 1:
        line_code = progArr[i][0] + '\t' + progArr[i][1] + '\t' + progArr[i][2]
        fout.write(progArr[0][2] + '\t' + line_code + '\t' + '\t' + pass2[i - 1])
        fout.write('\n')
    else:
        if progArr[i][0] != 'BASE' and progArr[i][0] != 'LTORG':
            if len(progArr[i]) == 1:
                line_code= '\t' + progArr[i][0] + '\t'
            elif progArr[i][0] == '*':
                line_code= progArr[i][0] + '\t' + progArr[i][1] + '\t'
            elif len(progArr[i]) == 2:
                line_code= '\t' + progArr[i][0] + '\t' + progArr[i][1]
            elif len(progArr[i]) == 3:
                line_code= progArr[i][0] + '\t' + progArr[i][1] + '\t' + progArr[i][2]
        else:
            if len(progArr[i]) == 1:
                line_code= '\t' + progArr[i][0]
            elif len(progArr[i]) == 2:
                line_code= '\t' + progArr[i][0] + '\t' + progArr[i][1]
        fout.write(str(hex(pcArr[i-1]).split('x')[-1].upper()) + '\t' + line_code + '\t' + '\t' + pass2[i-1] )
        fout.write('\n')

