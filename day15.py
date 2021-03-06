from collections import deque
import time
from copy import deepcopy


class Computer:

    def __init__(self, prog=None):
        self.prog = prog
        self.ip = 0
        self.base = 0
    
    def __deepcopy__(self, memo):
        c = Computer()
        c.prog = deepcopy(self.prog)
        c.ip = self.ip
        c.base = self.base
        return c

    def parse_instruction(self, i):
        i = str(i)
        opcode = int(i[-1])
        mode1 = int(i[-3]) if len(i) > 2 else 0
        mode2 = int(i[-4]) if len(i) > 3 else 0
        mode3 = int(i[-5]) if len(i) > 4 else 0

        return opcode, mode1, mode2, mode3

    def read_value(self, op, mode):
        if mode == 0:
            return self.prog[op]
        elif mode == 1:
            return op
        elif mode == 2:
            return self.prog[self.base + op]
    
    def read_write_address(self, op, mode):
        if mode == 2:
            return op + self.base
        else:
            return op

    def is_halt(self):
        return self.prog[self.ip] == 99

    def run_step(self, inp):
        while self.prog[self.ip] != 99:
            opcode, mode1, mode2, mode3 = self.parse_instruction(self.prog[self.ip])
            
            if opcode == 1:
                op1, op2, op3 = self.prog[self.ip+1], self.prog[self.ip+2], self.prog[self.ip+3]
                self.prog[self.read_write_address(op3, mode3)] = self.read_value(op1, mode1) + self.read_value(op2, mode2)
                self.ip += 4

            elif opcode == 2:
                op1, op2, op3 = self.prog[self.ip+1], self.prog[self.ip+2], self.prog[self.ip+3]
                self.prog[self.read_write_address(op3, mode3)] = self.read_value(op1, mode1) * self.read_value(op2, mode2)
                self.ip += 4
            
            elif opcode == 3:
                op1 = self.prog[self.ip+1]
                self.prog[self.read_write_address(op1, mode1)] = inp

                self.ip += 2

            elif opcode == 4:
                op1 = self.read_value(self.prog[self.ip+1], mode1)
                self.ip += 2
                return op1
            
            elif opcode == 5:
                op1, op2 = self.prog[self.ip+1], self.prog[self.ip+2]
                if self.read_value(op1, mode1) != 0:
                    self.ip = self.read_value(op2, mode2)
                else:
                    self.ip += 3
            
            elif opcode == 6:
                op1, op2 = self.prog[self.ip+1], self.prog[self.ip+2]
                if self.read_value(op1, mode1) == 0:
                    self.ip = self.read_value(op2, mode2)
                else:
                    self.ip += 3
            
            elif opcode == 7:
                op1, op2, op3 = self.prog[self.ip+1], self.prog[self.ip+2], self.prog[self.ip+3]
                if self.read_value(op1, mode1) < self.read_value(op2, mode2):
                    self.prog[self.read_write_address(op3, mode3)] = 1
                else:
                    self.prog[self.read_write_address(op3, mode3)] = 0
                self.ip += 4

            elif opcode == 8:
                op1, op2, op3 = self.prog[self.ip+1], self.prog[self.ip+2], self.prog[self.ip+3]
                if self.read_value(op1, mode1) == self.read_value(op2, mode2):
                    self.prog[self.read_write_address(op3, mode3)] = 1
                else:
                    self.prog[self.read_write_address(op3, mode3)] = 0
                self.ip += 4
            
            elif opcode == 9:
                op1 = self.read_value(self.prog[self.ip+1], mode1)
                self.base += op1
                self.ip += 2

def bfs1(queue, grid):
    d = {1: (0,1), 2: (0,-1), 3: (-1,0), 4: (1,0)}
    while len(queue) > 0:
        x, y, computer, dist = queue.pop(0)
        grid[(x,y)] = '.'
        print(x,y)

        for i in [1,2,3,4]:
            newx = x + d[i][0]
            newy = y + d[i][1]
            if (newx, newy) in grid:
                continue
            c = deepcopy(computer)
            output = c.run_step(i)
            if output == 0:
                grid[(newx, newy)] = '#'
            elif output == 1:
                queue.append((newx, newy, c, dist+1))
            elif output == 2:
                grid[(newx, newy)] = 'O'
                ox_x = newx
                ox_y = newy
                dist_to_oxygen = dist + 1
    
    return dist_to_oxygen, ox_x, ox_y

def bfs2(queue, grid):
    d = {1: (0,1), 2: (0,-1), 3: (-1,0), 4: (1,0)}
    max_dist = 0
    while len(queue) > 0:
        x, y, dist = queue.pop(0)
        max_dist = max(max_dist, dist)
        grid[(x,y)] = 'O'

        for i in [1,2,3,4]:
            newx = x + d[i][0]
            newy = y + d[i][1]
            if (newx, newy) not in grid:
                continue
            if grid[(newx, newy)] == '#' or grid[(newx, newy)] == 'O':
                continue
            else:
                queue.append((newx, newy, dist+1))
    
    return max_dist

def print_grid(grid):
    maze = [[' ' for i in range(50)] for j in range(50)]
    for x, y in grid.keys():
        maze[y+25][x+25] = grid[(x,y)]
    for i in range(50):
        print(''.join(maze[i]))

if __name__ == '__main__':

    with open('day15.txt') as f:
        prog_input = [int(x) for x in f.read().split(',')] + [0 for i in range(100000)]
    
    computer = Computer(prog_input)
    grid = dict()
    dist, ox_x, ox_y = bfs1([(0, 0, computer, 0)], grid)
    print('Distance:', dist)

    print_grid(grid)

    dist = bfs2([(ox_x, ox_y, 0)], grid)
    print('Distance:', dist)

    print_grid(grid)
