import numpy


class CPU():
    def __init__(self):
        self.cycle: int = 0
        self.X: int = 1
        self.current_instruction: str = ''
        self.ready_for_next_instruction = True
        self.instruction_completed = True
        self.cycles_remaining: int = 0
        self.execution_finished: bool = False
        self.program: list[str] = []
        self.sum_of_signal_strengths: int = 0
        self.crt: CRT = CRT()

    def set_program(self, program: str) -> int:
        instructions = []
        cycles_neccessary = 0
        with open(program) as file:
            for line in file:
                instruction = line.strip()
                cycles_neccessary += self.get_cycles_per_instruction(instruction)
                instructions.append(instruction)
        self.program = instructions
        self.cycle = 0
        self.X = 1
        self.sum_of_signal_strengths = 0
        self.crt = CRT()
        print('program '+program+' loaded')
        return cycles_neccessary

    def get_cycles_per_instruction(self, instruction: str) -> int:
        if 'addx' in instruction:
            return 2
        elif 'noop' in instruction:
            return 1

    def get_sum_of_signal_strengths(self) -> int:
        return self.sum_of_signal_strengths

    def execute_cycle(self):
        if self.execution_finished:
            return

        self.cycle += 1
        # print('cycle: '+str(self.cycle))

        if self.ready_for_next_instruction:
            # start of the first cycle
            if len(self.program) > 0:
                self.current_instruction = self.program.pop(0)
                self.cycles_remaining = self.get_cycles_per_instruction(self.current_instruction)
            else:
                self.execution_finished = True
            self.ready_for_next_instruction = False

        self.cycles_remaining -= 1

        # print('\tinstruction: '+self.current_instruction)
        # print('\tX during cycle: '+str(self.X))
        self.crt.draw_pixel(self.X)
        self.crt.print_screen()
        print('---')

        if self.cycle in [*range(20, 220+1, 40)]:
            signal_strength = self.signal_strength()
            print(signal_strength)
            self.sum_of_signal_strengths += signal_strength

        if self.cycles_remaining == 0:
            # check for more likely branch first
            if 'addx' in self.current_instruction:
                if not self.ready_for_next_instruction:
                    self.X += int(self.current_instruction.split()[1])
                    self.ready_for_next_instruction = True
            elif 'noop' in self.current_instruction:
                self.ready_for_next_instruction = True

        # print('\tX after cycle: '+str(self.X))

    def signal_strength(self) -> int:
        return self.cycle*self.X


class CRT():
    def __init__(self):
        self.width: int = 40
        self.height: int = 6
        self.current_pixel: int = 0
        self.screen: numpy.ndarray = numpy.full((self.width, self.height), False)
        pass

    def draw_pixel(self, X_sprite: int):
        x = self.current_pixel % self.width

        if abs(x-X_sprite) < 2:
            y = int(self.current_pixel / self.width)
            self.screen[x, y] = True

        self.current_pixel += 1

    def print_screen(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.screen[x, y]:
                    pixel = '#'
                else:
                    pixel = '.'
                print(pixel, end=' ')
            print()


cpu = CPU()


for _ in range(cpu.set_program('day_10_input_example_1.txt')):
    cpu.execute_cycle()

print(cpu.get_sum_of_signal_strengths())

for _ in range(cpu.set_program('day_10_input_example_2.txt')):
    cpu.execute_cycle()

print(cpu.get_sum_of_signal_strengths())

for _ in range(cpu.set_program('day_10_input.txt')):
    cpu.execute_cycle()

print('solution to part 1: '+str(cpu.get_sum_of_signal_strengths()))
