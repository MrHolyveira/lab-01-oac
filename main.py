class MIPS_to_hex_converter():
    def __init__(self, input_file):

        self.input_file = input_file
        self.opCodeDict = {
        'add': '100000',
        'addu': '100001',
        'addi': '001000',
        'addiu': '001001',
        'and': '100100',
        'andi': '001100',
        'div': '011010',
        'divu': '011011',
        'mult': '011000',
        'multu': '011001',
        'nor': '100111',
        'or': '100101',
        'ori': '001101',
        'sll': '000000',
        'sllv': '000100',
        'sra': '000011',
        'srav': '000111',
        'srl': '000010',
        'srlv': '000110',
        'sub': '100010',
        'subu': '100011',
        'xor': '100110',
        'xori': '001110',
        'lhi': '011001',
        'llo': '011000',
        'slt': '101010',
        'sltu': '101001',
        'slti': '001010',
        'sltiu': '001001',
        'beq': '000100',
        'bgtz': '000111',
        'blez': '000110',
        'bne': '000101',
        'j': '000010',
        'jal': '000011',
        'jalr': '001001',
        'jr': '001000',
        'lb': '100000',
        'lbu': '100100',
        'lh': '100001',
        'lhu': '100101',
        'lw': '100011',
        'sb': '101000',
        'sh': '101001',
        'sw': '101011',
        'mfhi': '010000',
        'mflo': '010010',
        'mthi': '010001',
        'mtlo': '010011',
        'trap': '011010',

        'li':'0',
        'clo':'0',
        'Label:':'0',
        'movn':'0',
        'mul':'0',
        'teq':'0',
        }

    def execute(self):
        with open(self.input_file, 'r') as f:
            file_text = f.read()
            data_area = self.get_clean_data_list(file_text, 0)
            text_area = self.get_clean_data_list(file_text, 1)
    
    def solve_data(self):
        pass

    def solve_text(self):
        pass

    def get_clean_data_list(self, data, split):
        data_list = data.split('.text')[split].split('\n')
        return [string for string in data_list if (string != "" and string != '.data')]

# for instruction in textArea:
#     print(instruction)

#     if instruction != '':
#         print(opCodeDict[instruction.split(' ')[0]])
    

if __name__ == "__main__":
    input_file = "input/example_entrada.asm"
    converter = MIPS_to_hex_converter(input_file)
    converter.execute()
