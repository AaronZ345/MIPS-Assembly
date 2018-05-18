import re


class Assembler():
    def __init__(self):
        # 建立R型和I型指令对应编码字典
        self.operation_r = {
            'add': '100000',
            'addu': '100001',
            'sub': '100010',
            'subu': '100011',
            'and': '100100',
            'or': '100101',
            'nor': '100111',
            'xor': '100110',
            'sll': '000000',
            'srl': '000010',
            'slt': '101010',
            'jr': '001000'
        }
        self.operation_i = {
            'addi': '001000',
            'lw': '100011',
            'sw': '101011',
            'ori': '001101',
            'beq': '000100',
            'bne': '000101',
            'bgtz': '000111',
            'blez': '000110',
            'bltz': '000001',
            'bgez': '000001',
            'slti': '001010',
            'j': '000010',
            'jal': '000011'
            }

        # 建立寄存器对应编号
        self.register = {
            '$zero': '00000',
            '$at': '00001',
            '$v0': '00010',
            '$v1': '00011',
            '$a0': '00100',
            '$a1': '00101',
            '$a2': '00110',
            '$a3': '00111',
            '$t0': '01000',
            '$t1': '01001',
            '$t2': '01010',
            '$t3': '01011',
            '$t4': '01100',
            '$t5': '01101',
            '$t6': '01110',
            '$t7': '01111',
            '$s0': '10000',
            '$s1': '10001',
            '$s2': '10010',
            '$s3': '10011',
            '$s4': '10100',
            '$s5': '10101',
            '$s6': '10110',
            '$s7': '10111',
            '$t8': '11000',
            '$t9': '11001',
            '$k0': '11010',
            '$k1': '11011',
            '$gp': '11100',
            '$sp': '11101',
            '$fp': '11110',
            '$ra': '11111'
        }

        # 为反汇编反转字典
        self.dis_operation_r = {v: k for k, v in self.operation_r.items()}
        self.dis_operation_i = {v: k for k, v in self.operation_i.items()}
        self.dis_register = {v: k for k, v in self.register.items()}

        # 保存寄存器中存储的值
        self.registers = {
            '$zero': '00000000',
            '$at': '00000000',
            '$v0': '00000000',
            '$v1': '00000000',
            '$a0': '00000000',
            '$a1': '00000000',
            '$a2': '00000000',
            '$a3': '00000000',
            '$t0': '00000000',
            '$t1': '00000000',
            '$t2': '00000000',
            '$t3': '00000000',
            '$t4': '00000000',
            '$t5': '00000000',
            '$t6': '00000000',
            '$t7': '00000000',
            '$s0': '00000000',
            '$s1': '00000000',
            '$s2': '00000000',
            '$s3': '00000000',
            '$s4': '00000000',
            '$s5': '00000000',
            '$s6': '00000000',
            '$s7': '00000000',
            '$t8': '00000000',
            '$t9': '00000000',
            '$k0': '00000000',
            '$k1': '00000000',
            '$gp': '00000000',
            '$sp': '00000000',
            '$fp': '00000000',
            '$ra': '00000000'
        }

        self.memory = {}  # 初始内存为零

        self.step = 0  # 初始调试步数为零

    def assembly(self, path):
        address = 0  # 初始化地址
        labelAddr = {}  # 初始化标签字典
        opt_str = ''  # 初始化返回字符串

        file_asm = open(path, 'r')  # 打开传入文件
        for line in file_asm:
            line = line.strip('\n')

            # 记录基地址
            if '#baseAddr' in line:
                address = int(line.lstrip().split(' ')[1], 16)
            # 将注释排除
            if '#' in line:
                line = line.lstrip().split('#')[0].rstrip()
            if '//' in line:
                line = line.lstrip().split('//')[0].rstrip()

            # 记录标签
            if ':' in line:
                newLabel = line.lstrip().rstrip().split(':')[0]
                labelAddr[newLabel] = str(address)
                line = line.strip().split(':')[1].strip()

            line = line.strip(';')
            # 跳过处理之后的空行
            if line == '':
                continue
            address += 4
        file_asm.close()

        address = 0
        file_asm = open(path, 'r')  # 打开传入文件
        file_coe = open(path.replace('asm', 'coe'), 'w+')  # 打开写入文件
        # 以行为单位进行汇编操作
        for line in file_asm:
            line = line.strip('\n')

            # 记录基地址
            if '#baseAddr' in line:
                address = int(line.lstrip().split(' ')[1], 16)
            # 将注释排除
            if '#' in line:
                line = line.lstrip().split('#')[0].rstrip()
            if '//' in line:
                line = line.lstrip().split('//')[0].rstrip()

            # 记录标签
            if ':' in line:
                line = line.strip().split(':')[1].strip()

            line = line.strip(';')
            # 跳过处理之后的空行
            if line == '':
                continue

            opt = ''  # 初始化输出操作字符串
            opt2 = ''  # 初始化第二个输出操作字符串
            line = line.lower()  # 将指令转为小写字母
            line = re.split(r'[, ]', line)  # 将指令按处理方便划分

            # R型指令处理
            if line[0] in self.operation_r:
                opt += '000000'
                if line[0] == 'jr':
                    opt += self.register[line[1]] + '000000000000000'
                elif line[0] == 'sll' or line[0] == 'srl':
                    opt += '00000' + self.register[line[2]] + self.register[line[1]] + str(bin(int(line[3])))[2:].zfill(5)
                else:
                    opt += self.register[line[2]] + self.register[line[3]] + self.register[line[1]] + '00000'
                opt += self.operation_r[line[0]]

            # I型指令处理
            elif line[0] in self.operation_i:
                opt += self.operation_i[line[0]]
                if line[0] == 'j' or line[0] == 'jal':
                    if line[1] in labelAddr:
                        opt += str(bin(int(int(labelAddr[line[1]]) / 4)))[2:].zfill(26)
                    else:
                        opt += str(bin(int(line[1])))[2:].zfill(26)
                elif line[0] == 'bgtz' or line[0] == 'blez' or line[0] == 'bltz':
                    opt += self.register[line[1]] + '00000'
                    if line[2] in labelAddr:
                        opt += str(bin(int((int(labelAddr[line[2]]) - (address + 4)) / 4) & 0b1111111111111111))[2:].zfill(16)
                    else:
                        opt += str(bin(int(line[2])))[2:].zfill(16)

                elif line[0] == 'bgez':
                    opt += self.register[line[1]] + '00001'
                    if line[2] in labelAddr:
                        opt += str(bin(int((int(labelAddr[line[2]]) - (address + 4)) / 4) & 0b1111111111111111))[2:].zfill(16)
                    else:
                        opt += str(bin(int(line[2])))[2:].zfill(16)

                elif line[0] == 'lw' or line[0] == 'sw':
                    addr = line[2].strip(')').split('(')
                    opt += self.register[addr[1]] + self.register[line[1]] + str(bin(int(addr[0])))[2:].zfill(16)
                elif line[0] == 'beq' or line[0] == 'bne':
                    opt += self.register[line[1]] + self.register[line[2]]
                    if line[3] in labelAddr:
                        opt += str(bin(int((int(labelAddr[line[3]]) - (address + 4)) / 4) & 0b1111111111111111))[2:].zfill(16) 
                    else:
                        opt += str(bin(int(line[3])))[2:].zfill(16)
                else:
                    opt += self.register[line[2]] + self.register[line[1]] + str(bin(int(line[3])))[2:].zfill(16)

            # 伪码处理
            elif line[0] == 'move':
                opt += '000000' + self.register['$zero'] + self.register[line[2]] + self.register[line[1]] + '00000' + self.operation_r['add']

            elif line[0] == 'bgt':
                opt += '000000' + self.register[line[1]] + self.register[line[2]] + self.register['$at'] + '00000' + self.operation_r['subu']
                opt2 += self.operation_i['bgtz'] + self.register['$at'] + '00000'
                if line[3] in labelAddr:
                    opt2 += str(bin(int((int(labelAddr[line[3]]) - (address + 4)) / 4) & 0b1111111111111111))[2:].zfill(16)
                else:
                    opt2 += str(bin(int(line[3])))[2:].zfill(16)

            elif line[0] == 'bge':
                opt += '000000' + self.register[line[1]] + self.register[line[2]] + self.register['$at'] + '00000' + self.operation_r['subu']
                opt2 += self.operation_i['bgez'] + self.register['$at'] + '00001'
                if line[3] in labelAddr:
                    opt2 += str(bin(int((int(labelAddr[line[3]]) - (address + 4)) / 4) & 0b1111111111111111))[2:].zfill(16)
                else:
                    opt2 += str(bin(int(line[3])))[2:].zfill(16)

            elif line[0] == 'blt':
                opt += '000000' + self.register[line[1]] + self.register[line[2]] + self.register['$at'] + '00000' + self.operation_r['subu']
                opt2 += self.operation_i['bltz'] + self.register['$at'] + '00000'
                if line[3] in labelAddr:
                    opt2 += str(bin(int((int(labelAddr[line[3]]) - (address + 4)) / 4) & 0b1111111111111111))[2:].zfill(16)
                else:
                    opt2 += str(bin(int(line[3])))[2:].zfill(16)

            elif line[0] == 'ble':
                opt += '000000' + self.register[line[1]] + self.register[line[2]] + self.register['$at'] + '00000' + self.operation_r['subu']
                opt2 += self.operation_i['blez'] + self.register['$at'] + '00000'
                if line[3] in labelAddr:
                    opt2 += str(bin(int((int(labelAddr[line[3]]) - (address + 4)) / 4) & 0b1111111111111111))[2:].zfill(16)
                else:
                    opt2 += str(bin(int(line[3])))[2:].zfill(16)

            file_coe.write(str(hex(int(opt, 2)))[2:].zfill(8))
            opt_str += str(hex(int(address)))[2:].zfill(8) + '\t' + str(hex(int(opt, 2)))[2:].zfill(8) + '\n'
            address += 4

            if opt2 != '':
                file_coe.write(str(hex(int(opt2, 2)))[2:].zfill(8))
                opt_str += str(hex(int(address)))[2:].zfill(8) + '\t' + str(hex(int(opt2, 2)))[2:].zfill(8) + '\n'
                address += 4

        file_asm.close()
        file_coe.close()
        return opt_str

    def disassembly(self, path):
        address = 0
        opt_str = ''

        # 支持两种二进制文件格式
        file_coe = open(path, 'r')
        if 'coe' in path:
            file_asm = open(path.replace('coe', 'asm'), 'w+')
            hex_code = re.findall(r'.{8}', file_coe.read())  # 将16进制指令转为2进制
            bin_code = [(str(bin(int(hc, 16)))[2:].zfill(32)) for hc in hex_code]
        elif 'bin' in path:
            file_asm = open(path.replace('bin', 'asm'), 'w+')
            bin_code = re.findall(r'.{32}', file_coe.read())

        # 以32位为单位处理二进制指令文件
        for line in bin_code:
            opt = ''

            # 处理R型指令
            if line[0:6] == '000000':
                opt += self.dis_operation_r[line[26:]] + ' '
                if opt == 'jr ':
                    opt += self.dis_register[line[6:11]]
                elif opt == 'sll ' or opt == 'srl ':
                    opt += self.dis_register[line[16:21]] + ',' + self.dis_register[line[11:16]] + ',' + str(int(line[21:26], 2))
                else:
                    opt += self.dis_register[line[16:21]] + ',' + self.dis_register[line[6:11]]+',' + self.dis_register[line[11:16]]

            # 处理I型指令
            else:
                opt += self.dis_operation_i[line[0:6]] + ' '
                if opt == 'j ' or opt == 'jal ':
                    opt += (str(int(line[6:32], 2)))
                elif opt == 'lw ' or opt == 'sw ':
                    opt += self.dis_register[line[11:16]] + ',' + str(int(line[16:32], 2)) + '(' + self.dis_register[line[6:11]] + ')'
                elif opt == 'beq ' or opt == 'bne ':
                    opt += self.dis_register[line[6:11]] + ',' + self.dis_register[line[11:16]] + ','
                    if line[16] == '0':
                        opt += str(int(int(line[17:32], 2)))
                    else:
                        opt += str(int(int(line[17:32], 2) - pow(2, 15)))
                elif opt == 'bgtz ' or opt == 'blez ' or opt == 'bgez ' or opt == 'bltz ':
                    opt += self.dis_register[line[6:11]] + ','
                    if line[16] == '0':
                        opt += str(int(int(line[17:32], 2)))
                    else:
                        opt += str(int(int(line[17:32], 2) - pow(2, 15)))
                else:
                    opt += self.dis_register[line[11:16]] + ',' + self.dis_register[line[6:11]] + ',' + str(int(line[16:32], 2))

            file_asm.write(opt + '; //' + str(hex(int(address)))[2:].zfill(8) + '\n')
            opt_str += str(int(int(address) / 4)) + '\t' + opt + '\n'
            address += 4

        file_asm.close()
        file_coe.close()
        return opt_str

    def debug(self, path):
        address = 0
        labelAddr = {}
        labelLine = {}
        addrToLine = {}
        opt_str = ''
        stepFun = 0  # 函数内运行步数初始化
        flagJ = 0 # 判断是否进入跳转类指令

        file_asm = open(path, 'r')  # 打开传入文件
        for line in file_asm:
            line = line.strip('\n')

            # 记录基地址
            if '#baseAddr' in line:
                address = int(line.lstrip().split(' ')[1], 16)
            # 将注释排除
            if '#' in line:
                line = line.lstrip().split('#')[0].rstrip()
            if '//' in line:
                line = line.lstrip().split('//')[0].rstrip()

            # 记录标签
            if ':' in line:
                newLabel = line.lstrip().rstrip().split(':')[0]
                labelAddr[newLabel] = str(address)
                labelLine[newLabel] = stepFun
                line = line.strip().split(':')[1].strip()

            line = line.strip(';')
            # 跳过处理之后的空行
            if line == '':
                continue

            stepFun += 1
            address += 4
        file_asm.close()

        address = 0
        stepFun = 0
        file_asm = open(path, 'r')
        for line in file_asm:
            line = line.strip(';').strip('\n')
            addrToLine[address] = stepFun

            # 记录基地址
            if '#baseAddr' in line:
                address = int(line.lstrip().split(' ')[1], 16)
            if '#' in line:
                line = line.lstrip().split('#')[0].rstrip()
            if '//' in line:
                line = line.lstrip().split('//')[0].rstrip()
            if ':' in line:
                line = line.strip().split(':')[1].strip()

            line = line.strip(';')
            # 处理后空行则跳过模拟
            if line == '':
                continue

            # 进行至当前步骤则开始执行
            if stepFun < self.step:
                stepFun += 1
                address += 4
                continue

            opt = ''
            line = line.lower()
            line = re.split(r'[, ]', line)

            if line[0] in self.operation_r:
                opt += '000000'
                if line[0] == 'jr':
                    opt += self.register[line[1]] + '000000000000000'
                elif line[0] == 'sll' or line[0] == 'srl':
                    opt += '00000' + self.register[line[2]] + self.register[line[1]] + str(bin(int(line[3])))[2:].zfill(5)
                else:
                    opt += self.register[line[2]] + self.register[line[3]] + self.register[line[1]] + '00000'
                opt += self.operation_r[line[0]]

            elif line[0] in self.operation_i:
                opt += self.operation_i[line[0]]
                if line[0] == 'j' or line[0] == 'jal':
                    if line[1] in labelAddr:
                        opt += str(bin(int(int(labelAddr[line[1]]) / 4)))[2:].zfill(26)
                    else:
                        opt += str(bin(int(line[1])))[2:].zfill(26)
                elif line[0] == 'bgtz' or line[0] == 'blez' or line[0] == 'bltz':
                    opt += self.register[line[1]] + '00000'
                    if line[2] in labelAddr:
                        opt += str(bin(int((int(labelAddr[line[2]]) - (address + 4)) / 4) & 0b1111111111111111))[2:].zfill(16)
                    else:
                        opt += str(bin(int(line[2])))[2:].zfill(16)

                elif line[0] == 'bgez':
                    opt += self.register[line[1]] + '00001'
                    if line[2] in labelAddr:
                        opt += str(bin(int((int(labelAddr[line[2]]) - (address + 4)) / 4) & 0b1111111111111111))[2:].zfill(16)
                    else:
                        opt += str(bin(int(line[2])))[2:].zfill(16)

                elif line[0] == 'lw' or line[0] == 'sw':
                    addr = line[2].strip(')').split('(')
                    opt += self.register[addr[1]] + self.register[line[1]] + str(bin(int(addr[0])))[2:].zfill(16)
                elif line[0] == 'beq' or line[0] == 'bne':
                    opt += self.register[line[1]] + self.register[line[2]]
                    if line[3] in labelAddr:
                        opt += str(bin(int((int(labelAddr[line[3]]) - (address + 4)) / 4) & 0b1111111111111111))[2:].zfill(16)
                    else:
                        opt += str(bin(int(line[3])))[2:].zfill(16)
                else:
                    opt += self.register[line[2]] + self.register[line[1]] + str(bin(int(line[3])))[2:].zfill(16)

            elif line[0] == 'move':
                opt += '000000' + self.register['$zero'] + self.register[line[2]] + self.register[line[1]] + '00000' + self.operation_r['add']

            opt_str += str(hex(int(address)))[2:].zfill(8) + '\t' + str(hex(int(opt, 2)))[2:].zfill(8) + '\n'
            self.memory[str(hex(int(address)))[2:].zfill(8)] = str(hex(int(opt, 2)))[2:].zfill(8)

            # 对部分指令进行模拟操作
            if line[0] == 'add':
                self.registers[line[1]] = str(hex(int(self.registers[line[2]], 16) + int(self.registers[line[3]], 16)))[2:].zfill(8)
            elif line[0] == 'sub':
                self.registers[line[1]] = str(hex(int(self.registers[line[2]], 16) - int(self.registers[line[3]], 16)))[2:].zfill(8)
            elif line[0] == 'addi':
                self.registers[line[1]] = str(hex(int(self.registers[line[2]], 16) + int(line[3])))[2:].zfill(8)
            elif line[0] == 'move':
                self.registers[line[1]] = str(hex(int(self.registers[line[2]], 16) + int(self.registers['$zero'], 16)))[2:].zfill(8)
            elif line[0] == 'and':
                self.registers[line[1]] = str(hex(int(self.registers[line[2]], 16) & int(self.registers['$zero'], 16)))[2:].zfill(8)
            elif line[0] == 'or':
                self.registers[line[1]] = str(hex(int(self.registers[line[2]], 16) | int(self.registers['$zero'], 16)))[2:].zfill(8)
            elif line[0] == 'xor':
                self.registers[line[1]] = str(hex(int(self.registers[line[2]], 16) ^ int(self.registers['$zero'], 16)))[2:].zfill(8)
            elif line[0] == 'sll':
                self.registers[line[1]] = str(hex(int(self.registers[line[2]], 16) << int(line[3])))[2:].zfill(8)
            elif line[0] == 'srl':
                self.registers[line[1]] = str(hex(int(self.registers[line[2]], 16) >> int(line[3])))[2:].zfill(8)
            elif line[0] == 'slt':
                if int(self.registers[line[2]], 16) < int(self.registers[line[3]], 16):
                    self.registers[line[1]] = '00000001'
                else:
                    self.registers[line[1]] = '00000000'
            elif line[0] == 'lw':
                addr = line[2].strip(')').split('(')
                try:
                    self.registers[line[1]] = self.memory[str(hex(int(self.registers[addr[1]], 16) + int(addr[0])))[2:].zfill(8)]
                except:
                    self.registers[line[1]] = '00000000'
            elif line[0] == 'sw':
                addr = line[2].strip(')').split('(')
                self.memory[str(hex(int(self.registers[addr[1]], 16) + int(addr[0])))[2:].zfill(8)] = self.registers[line[1]]
            elif line[0] == 'j':
                flagJ = 1
                if line[1] in labelLine:
                    self.step = labelLine[line[1]]
                else:
                    self.step = addrToLine[int(line[1])]
            elif line[0] == 'jal':
                flagJ = 1
                self.registers['$ra'] = str(hex(int(address)))[2:].zfill(8)
                print(address)
                try:
                    if line[1] in labelLine:
                        self.step = labelLine[line[1]]
                    else:
                        self.step = addrToLine[int(line[1])]
                except:
                    raise Exception('end')
            elif line[0] == 'jr':
                flagJ = 1
                self.step = addrToLine[4 * int(self.registers[line[1]])]
            elif line[0] == 'beq' and self.registers[line[1]] == self.registers[line[2]]:
                flagJ = 1
                if line[3] in labelLine:
                    self.step = labelLine[line[3]]
                else:
                    self.step = addrToLine[address + 1 + 4 * int(line[3])]
            elif line[0] == 'bne' and self.registers[line[1]] != self.registers[line[2]]:
                flagJ = 1
                if line[3] in labelLine:
                    self.step = labelLine[line[3]]
                    #print(stepFun,self.step,labelLine[line[3]])
                else:
                    self.step = addrToLine[address + 1 + 4 * int(line[3])]
            break

        if self.step == stepFun + 1:
            raise Exception('end')  # 若结束则掷出一个异常
        if not flagJ:
            self.step = stepFun + 1
        # print(self.step)

        file_asm.close()

        return opt_str
