'''
    Tyler Scott
    CS222 Assignment 1: Instruction Processing
'''

# Opcodes
NOOP = 0
ADD = 1
ADDI = 2
BEQ = 3
JAL = 4
LW = 5
SW = 6
RETURN = 7


def main():
    testCaseOne()
    print("\n")
    testCaseTwo()


def testCaseOne():
    print("Test 1")

    i0 = (NOOP << 28)
    i1 = (ADDI << 28) + (1 << 24) + (0 << 20) + 1
    i2 = (ADDI << 28) + (2 << 24) + (0 << 20) + 2
    i3 = (ADD << 28) + (3 << 24) + (1 << 20) + (1 << 16)
    i4 = (ADD << 28) + (4 << 24) + (2 << 20) + (2 << 16)
    i5 = (BEQ << 28) + (3 << 20) + (4 << 16) + 3
    i6 = (ADDI << 28) + (8 << 24) + (0 << 20) + 10
    i7 = (JAL << 28) + (0 << 24) + 2
    i8 = (ADDI << 28) + (8 << 24) + (0 << 20) + 1000
    i9 = (SW << 28) + (2 << 20) + (8 << 16) + 10
    i10 = (LW << 28) + (5 << 24) + (8 << 20) + 10
    i11 = (RETURN << 28)

    cpu = CPU()
    cpu.memory[100] = i0
    cpu.memory[101] = i1
    cpu.memory[102] = i2
    cpu.memory[103] = i3
    cpu.memory[104] = i4
    cpu.memory[105] = i5
    cpu.memory[106] = i6
    cpu.memory[107] = i7
    cpu.memory[108] = i8
    cpu.memory[109] = i9
    cpu.memory[110] = i10
    cpu.memory[111] = i11
    cpu.pc = 100

    running = True
    while running:
        terminate = cpu.EX()  # IF() and ID() used as helper functions in CPU class
        if terminate:
            running = False

    print("All values currently in registers: ")
    print(cpu.regs)
    print("Value at memory[20]: ")
    print(cpu.memory[20])


def testCaseTwo():
    print("Test 2")
    i0 = (ADDI << 28) + (1 << 24) + (0 << 20) + 1
    i1 = (ADDI << 28) + (2 << 24) + (0 << 20) + 2
    i2 = (ADD << 28) + (3 << 24) + (2 << 20) + (1 << 16)
    i3 = (ADD << 28) + (4 << 24) + (1 << 20) + (2 << 16)
    i4 = (BEQ << 28) + (3 << 20) + (4 << 16) + 3
    i5 = (ADDI << 28) + (8 << 24) + (0 << 20) + 10
    i6 = (JAL << 28) + (0 << 24) + 2
    i7 = (ADDI << 28) + (8 << 24) + (0 << 20) + 1000
    i8 = (SW << 28) + (2 << 20) + (8 << 16) + 10
    i9 = (LW << 28) + (5 << 24) + (8 << 20) + 10
    i10 = (RETURN << 28)

    cpu = CPU()
    cpu.memory[100] = i0
    cpu.memory[101] = i1
    cpu.memory[102] = i2
    cpu.memory[103] = i3
    cpu.memory[104] = i4
    cpu.memory[105] = i5
    cpu.memory[106] = i6
    cpu.memory[107] = i7
    cpu.memory[108] = i8
    cpu.memory[109] = i9
    cpu.memory[110] = i10
    cpu.pc = 100

    running = True
    while running:
        terminate = cpu.EX()
        if terminate:
            running = False

    print("All values currently in registers: ")
    print(cpu.regs)
    print("Value at memory[1010]: ")
    print(cpu.memory[1010])


class CPU:
    MEM_SIZE = 65536
    NUM_REGISTERS = 16

    def __init__(self):
        self.pc = 0
        self.next_pc = 0
        self.memory = []
        self.regs = []
        for num in range(self.MEM_SIZE):
            self.memory.append(0)
        for num in range(self.NUM_REGISTERS):
            self.regs.append(0)

    def IF(self):
        instruction = self.memory[self.pc]  # Copy instruction from memory
        self.next_pc = self.pc + 1  # Iterate next position
        return instruction

    def ID(self):
        currentInstruction = self.IF()  # Get instruction

        # Decode all values from current instruction
        decodedInstruction = Instruction()
        decodedInstruction.opcode = (currentInstruction >> 28) & 15  # 4-digit bit
        decodedInstruction.Rd = (currentInstruction >> 24) & 15
        decodedInstruction.Rs1 = (currentInstruction >> 20) & 15
        decodedInstruction.Rs2 = (currentInstruction >> 16) & 15
        decodedInstruction.immediate = currentInstruction & 65535  # 16-digit bit
        return decodedInstruction

    def EX(self):
        instruction = self.ID()  # To get decoded instruction

        # Perform instruction operations
        if instruction.opcode == NOOP:
            pass

        elif instruction.opcode == ADD:
            alu_result = instruction.Rs1 + instruction.Rs2
            self.regs[instruction.Rd] = alu_result

        elif instruction.opcode == ADDI:
            alu_result = instruction.Rs1 + instruction.immediate
            self.regs[instruction.Rd] = alu_result

        elif instruction.opcode == BEQ:
            if self.regs[instruction.Rs1] == self.regs[instruction.Rs2]:
                self.next_pc = self.pc + instruction.immediate

        elif instruction.opcode == JAL:
            alu_result = self.pc + 1
            self.next_pc = self.pc + instruction.immediate
            self.regs[instruction.Rd] = alu_result

        elif instruction.opcode == LW:
            eff_address = self.memory[instruction.immediate + self.regs[instruction.Rs1]]
            self.regs[instruction.Rd] = eff_address

        elif instruction.opcode == SW:
            eff_address = instruction.immediate + self.regs[instruction.Rs2]
            self.memory[eff_address] = instruction.Rs1

        elif instruction.opcode == RETURN:
            return True

        else:
            print("Something went very wrong!")
            return True

        self.pc = self.next_pc  # Set new pc value for next iteration


class Instruction:
    def __init__(self):
        self.opcode = 0
        self.Rd = 0
        self.Rs1 = 0
        self.Rs2 = 0
        self.immediate = 0


if __name__ == "__main__":
    main()
