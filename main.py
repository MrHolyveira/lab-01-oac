import re


class MipsToHexConverter:
    def __init__(self, input_file, output_data_file, output_text_file):

        self.input_file = input_file
        self.output_data_file = output_data_file
        self.output_text_file = output_text_file

        self.branch_instructions_list = ['beq', 'bne', 'blez', 'bgtz']

        self.counter = 0

        self.to_implement_instructions = [
            'c.eq.d',
            'c.eq.s',
        ]

        self.pseudo_instructions = ['li']

        self.R_type_instructions_op_codes = {
            'clo': '011100',
            'mul': '011100',
            'add.d': '010001',
            'add.s': '010001',
            'sub.d': '010001',
            'sub.s': '010001',
            'mult.d': '010001',
            'mult.s': '010001',
            'div.d': '010001',
        }

        self.I_type_instructions_op_codes = {
            'addi': '001000',
            'addiu': '001001',
            'andi': '001100',
            'beq': '000100',
            'bne': '000101',
            'bgtz': '000111',
            'blez': '000110',
            'lb': '100000',
            'lbu': '100100',
            'lui': '001111',
            'lw': '100011',
            'sb': '101000',
            'sh': '101001',
            'slti': '001010',
            'sltiu': '001011',
            'sw': '101011',
            'ori': '001101',
            'xori': '001110',
            'teq': '000000',
            'madd': '011100',
            'msubu': '011100'
        }

        self.J_type_instructions_op_codes = {
            'j': '000010',
            'jal': '000011',
        }

        # most R type instructions have 000000 op codes by default
        self.R_type_instructions_func_codes = {
            'add': '100000',
            'addu': '100001',
            'and': '100100',
            'div': '011010',
            'divu': '011011',
            'jalr': '001001',
            'jr': '001000',
            'mfhi': '010000',
            'mthi': '010001',
            'mflo': '010010',
            'mtlo': '010011',
            'mult': '011000',
            'multu': '011001',
            'nor': '100111',
            'xor': '100110',
            'or': '100101',
            'slt': '101010',
            'sltu': '101011',
            'sll': '000000',
            'srl': '000010',
            'sra': '000011',
            'sllv': '000100',
            'srav': '000111',
            'srlv': '000110',
            'sub': '100010',
            'subu': '100011',
            'clo': '100001',
            'movn': '001011',
            'mul': '000010',
            'add.d': '000000',
            'add.s': '000000',
            'sub.d': '000001',
            'sub.s': '000001',
            'mult.d': '000010',
            'mult.s': '000010',
            'div.d': '000011',
        }

        self.special_R_type_cases = {
            'add.d': '10001',
            'add.s': '10000',
            'sub.d': '10001',
            'sub.s': '10000',
            'mult.d': '10001',
            'mult.s': '10000',
            'div.d': '10001',
        }

        self.special_I_type_cases = {
            'teq': '0000000000110100',
            'madd': '0000000000000000',
            'msubu': '0000000000000101'
        }

        self.register_translations = {
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
            '$ra': '11111',
            '$f0': '00000',
            '$f1': '00001',
            '$f2': '00010',
            '$f3': '00011',
            '$f4': '00100',
            '$f5': '00101',
            '$f6': '00110',
            '$f7': '00111',
            '$f8': '01000',
            '$f9': '01001',
            '$f10': '01010',
            '$f11': '01011',
            '$f12': '01100',
            '$f13': '01101',
            '$f14': '01110',
            '$f15': '01111',
            '$f16': '10000',
            '$f17': '10001',
            '$f18': '10010',
            '$f19': '10011',
            '$f20': '10100',
            '$f21': '10101',
            '$f22': '10110',
            '$f23': '10111',
            '$f24': '11000',
            '$f25': '11001',
            '$f26': '11010',
            '$f27': '11011',
            '$f28': '11100',
            '$f29': '11101',
            '$f30': '11110',
            '$f31': '11111',
        }

    def execute(self):
        with open(self.input_file, 'r') as f:
            file_text = f.read()
            data_area = self.__get_clean_data_list(file_text, 0)
            text_area = self.__get_clean_data_list(file_text, 1)
            hex_data = self.solve_data(data_area)
            hex_text = self.solve_text(text_area)
            f.close()
        with open(self.output_data_file, 'w') as f:
            f.write(hex_data)
            f.close()
        with open(self.output_text_file, 'w') as f:
            f.write(hex_text)
            f.close()

    def solve_data(self, data):
        answer = 'DEPTH = 16384;\nWIDTH = 32;\nADDRESS_RADIX = HEX;\nDATA_RADIX = HEX;\nCONTENT\nBEGIN\n\n'
        instruction = 0

        for line in data:
            variables = line.split('.word')[1].split(',')

            for variable in variables:
                variable = int(variable)
                answer += self.__handle_integer_to_hex(instruction) + ' : '
                answer += self.__handle_integer_to_hex(variable) + ';\n'
                instruction += 1

        answer += '\nEND;'
        return answer

    def solve_text(self, data):
        answer = 'DEPTH = 4096;\nWIDTH = 32;\nADDRESS_RADIX = HEX;\nDATA_RADIX = HEX;\nCONTENT\nBEGIN\n\n'
        for instruction in data:
            answer += hex(self.counter)[2:].zfill(8) + ' : ' + self.solve_instruction(instruction)
            self.counter += 1

        answer += '\nEND;'
        return answer

    def solve_instruction(self, instruction):
        call = self.__check_if_label(instruction)
        values = re.search(re.escape(call) + r'(.*)', instruction).group(1)
        values = re.sub(r' ', '', values).split(',')

        if call in self.R_type_instructions_func_codes.keys():
            answer = self.__solve_R_type_instructions(values, call, instruction)

        elif call in self.I_type_instructions_op_codes.keys():
            answer = self.__solve_I_type_instructions(values, call, instruction)

        elif call in self.J_type_instructions_op_codes.keys():
            answer = self.__solve_J_type_instructions(values, call, instruction)

        elif call in self.pseudo_instructions:
            answer = self.__solve_pseudo_instructions(values, call, instruction)

        else:
            msg = "Unknown instruction: " + instruction
            raise ValueError(msg)
        return answer

    def __solve_pseudo_instructions(self, values, call, instruction):
        answer = ''
        if call == 'li':
            register_values = self.__get_register_values(values)
            immediate = values[-1][2:].zfill(8)
            instruction_1 = 'lui $at, ' + self.__convert_hex_to_integer(immediate[:4])
            instruction_2 = 'ori ' + register_values[0] + ', $at, ' + self.__convert_hex_to_integer(immediate[4:])
            answer += self.solve_instruction(instruction_1).replace('; % ' + instruction_1 + ' %\n',
                                                                    '') + '; % ' + instruction + ' %\n'
            self.counter += 1
            answer += hex(self.counter)[2:].zfill(8) + ' : ' + self.solve_instruction(instruction_2).replace(
                ' % ' + instruction_2 + ' %', '')
        return answer

    def __solve_J_type_instructions(self, values, call, instruction):
        binary_answer = ''
        immediate = self.__get_immediate_value(values, 26)

        binary_answer += self.J_type_instructions_op_codes.get(call)

        binary_answer += immediate

        return self.__convert_binary_to_hex(binary_answer) + '; % ' + instruction + ' %\n'

    def __solve_I_type_instructions(self, values, call, instruction):
        binary_answer = ''
        register_values = self.__get_register_values(values)
        binary_answer += self.__check_special_I_type_cases(call, register_values)
        if binary_answer:
            return self.__convert_binary_to_hex(binary_answer) + '; % ' + instruction + ' %\n'
        immediate = self.__get_immediate_value(values, 16)

        binary_answer += self.I_type_instructions_op_codes.get(call)

        if call in self.branch_instructions_list:
            if call == "beq" or call == "bne":
                binary_answer += self.register_translations.get(register_values[0])
                binary_answer += self.register_translations.get(register_values[1])
            else:
                binary_answer += self.register_translations.get(register_values[0])
                if call == "bgez":
                    binary_answer += '00001'
                elif call == "bgezeal":
                    binary_answer += '10001'
                else:
                    binary_answer += '00000'
        else:
            while len(register_values) < 2:
                register_values.append('$zero')
            binary_answer += self.register_translations.get(register_values[1])
            binary_answer += self.register_translations.get(register_values[0])

        binary_answer += immediate

        return self.__convert_binary_to_hex(binary_answer) + '; % ' + instruction + ' %\n'

    def __solve_R_type_instructions(self, values, call, instruction):
        binary_answer = ''

        register_values = self.__get_register_values(values)
        while len(register_values) < 3:
            register_values.append('$zero')

        opcode_value = "000000" if not self.R_type_instructions_op_codes.get(
            call) else self.R_type_instructions_op_codes.get(call)
        binary_answer += self.__check_special_R_type_cases(call, register_values, opcode_value)
        if binary_answer:
            return self.__convert_binary_to_hex(binary_answer) + '; % ' + instruction + ' %\n'
        binary_answer += opcode_value

        binary_answer += self.register_translations.get(register_values[1])
        binary_answer += self.register_translations.get(register_values[2])
        binary_answer += self.register_translations.get(register_values[0])

        binary_answer += self.__get_shift_amount(values)

        binary_answer += self.R_type_instructions_func_codes.get(call)

        return self.__convert_binary_to_hex(binary_answer) + '; % ' + instruction + ' %\n'

    def __check_special_R_type_cases(self, call, register_values, opcode_value):
        binary_answer = ''
        if call in self.special_R_type_cases:
            binary_answer += opcode_value
            binary_answer += self.special_R_type_cases.get(call)
            binary_answer += self.register_translations.get(register_values[2])
            binary_answer += self.register_translations.get(register_values[1])
            binary_answer += self.register_translations.get(register_values[0])
            binary_answer += self.R_type_instructions_func_codes.get(call)
        return binary_answer

    def __check_special_I_type_cases(self, call, register_values):
        binary_answer = ''
        if call in self.special_I_type_cases:
            binary_answer += self.I_type_instructions_op_codes.get(call)
            binary_answer += self.register_translations.get(register_values[0])
            binary_answer += self.register_translations.get(register_values[1])
            binary_answer += self.special_I_type_cases.get(call)
        return binary_answer

    @staticmethod
    def __check_if_label(instruction):
        call = instruction.split()[0]
        if call[-1] == ':':
            return re.search(r': (\S*) ', instruction).group(1)
        else:
            return call

    @staticmethod
    def __handle_integer_to_hex(number):
        return str(hex(number)[2:].zfill(8))

    @staticmethod
    def __get_immediate_value(values, binary_length):
        for value in values:
            if value[0] != '$':
                if '(' in value:
                    string_value = re.search(r'(\S+)\(\S+\)', value).group(1)
                else:
                    string_value = value
                binary_string = bin(int(string_value))[2:]
                if len(binary_string) != binary_length:
                    zero_amount = binary_length - len(binary_string)
                    for _ in range(zero_amount):
                        binary_string = '0' + binary_string
        return binary_string

    @staticmethod
    def __get_shift_amount(values):
        shift_list = [value for value in values if value[0] != '$']
        return shift_list[0] if shift_list else '00000'

    @staticmethod
    def __get_register_values(values):
        register_list = []
        for value in values:
            if value[0] != '$' and '(' in value:
                register_list.append(re.search(r'(\$\S{2})', value).group(1))
            elif value[0] == '$':
                register_list.append(value)
        return register_list

    @staticmethod
    def __get_clean_data_list(data, split):
        data_list = data.split('.text')[split].split('\n')
        return [string for string in data_list if (string != "" and string != '.data')]

    @staticmethod
    def __convert_binary_to_hex(string):
        decimal_representation = int(string, 2)
        hex_representation = hex(decimal_representation)[2:].zfill(8)
        return hex_representation

    @staticmethod
    def __convert_hex_to_integer(string):
        return str(int(string, base=16))


if __name__ == "__main__":
    input_file = "input/example_entrada.asm"
    output_data_file = "output/example_saida_data_nosso.mif"
    output_text_file = "output/example_saida_text_nosso.mif"
    converter = MipsToHexConverter(input_file, output_data_file, output_text_file)
    converter.execute()
