import re

class MIPS_to_hex_converter():
    def __init__(self, input_file):

        self.input_file = input_file

        '''
        TODO:   These instructions are yet to be implemented these instructions
        '''
        self.to_implement_instructions = [
        'li',
        'clo',
        'bgez',
        'madd',
        'msubu',
        'bgezal',
        'Label',
        'movn',
        'mul',
        'teq',
        'add.d',
        'add.s',
        'sub.d',
        'sub.s',
        'c.eq.d',
        'c.eq.s',
        'mul.d',
        'mul.s',
        'div.d'
        ]
        
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
        'lw': '100010',
        'sb': '101000',
        'sh': '101001',
        'slti': '001010',
        'sltiu': '001011',
        'sw': '101011',
        'ori': '001101',
        'xori': '001110',
        }
        self.J_type_instructions_op_codes  = {
        'j': '000010',
        'jal': '000011',
        }
        #most R type instructions have 000000 op codes by default
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
        'R_binary_zero': '00000',
        }

    def execute(self):
        with open(self.input_file, 'r') as f:
            file_text = f.read()
            data_area = self.__get_clean_data_list(file_text, 0)
            text_area = self.__get_clean_data_list(file_text, 1)
            self.__solve_data(data_area)
            self.__solve_text(text_area)
    
    def __solve_data(self, data):
        pass

    def __solve_text(self, data):
        for instruction in data:
            binary_answer = ""
            call = instruction.split()[0]
            values = re.sub(call, '', instruction)
            values = re.sub(r' ', '', values).split(',')
            if call in self.R_type_instructions_func_codes.keys():
                while len(values) != 3:
                    values.append('R_binary_zero')
                binary_answer += "000000"
                binary_answer += self.register_translations.get(values[1])
                binary_answer += self.register_translations.get(values[2])
                binary_answer += self.register_translations.get(values[0])
                ''' 
                TODO: implement shift amount the correct way.
                '''
                #shift amount
                binary_answer += "00000"

                binary_answer += self.R_type_instructions_func_codes.get(call)

                answer = self.__convert_binary_to_hex(binary_answer)
                import pdb; pdb.set_trace()
                
            elif call in self.I_type_instructions_op_codes.keys():
                pass
            elif call in self.J_type_instructions_op_codes.keys():
                pass
            elif call in self.to_implement_instructions:
                pass
            else:
                raise ValueError("Unknown instruction")

    @staticmethod
    def __get_clean_data_list(data, split):
        data_list = data.split('.text')[split].split('\n')
        return [string for string in data_list if (string != "" and string != '.data')]
    
    @staticmethod
    def __convert_binary_to_hex(string):
        decimal_representation = int(string, 2)
        hex_representation = hex(decimal_representation)[2:]
        if len(hex_representation) != 8:
            zero_amount = 8 - len(hex_representation)
            for _ in range(zero_amount):
                hex_representation = '0' + hex_representation
        return hex_representation


if __name__ == "__main__":
    input_file = "input/example_entrada.asm"
    converter = MIPS_to_hex_converter(input_file)
    converter.execute()
