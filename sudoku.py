import sys
import numpy as np
from pprint import PrettyPrinter as PP
from matplotlib import pyplot as plt
import random


class Sudoku:
    NUMBER_LIST = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def __init__(self, board = np.empty((9,9), dtype=int)):
        self.board = board
        self.recursion_counter = 0
        pass

 
    def refreshBoard(self):
        num_list = [_ for _ in range(1, 10)]
        random.shuffle(num_list)
        for r in range(9):
            row = self.offsetRow(num_list, 3*(r%3) + r//3)
            self.board[r] = row
   

    def generateBoard(self):
        self.refreshBoard()
        self.shuffleBoard()


    def offsetRow(self, row, n):
        '''
        Offsets a list to the left.
        Pluggs first numnbers at the end
        
        offsetRow([1, 2, 3, 4, 5], 2) = [3, 4, 5, 1, 2] 
        '''
        
        rr = row[n:]
        rr += row[:n]
        return rr 


    def shuffleBoard(self, count=100):
        for c in range(count):
            action = random.randint(0, 75)
            if action <= 5:
                self.board = np.rot90(self.board)
            elif action <= 15:
                self.swap2(axis=0)
            elif action <= 25:
                self.swap2(axis=1)
            elif action >= 35:
                self.swap2(axis=0, dim=1)
            elif action >= 45:
                self.swap2(axis=1, dim=1)
            elif action >= 60:
                n1 = random.randint(1, 10)
                n2 = random.randint(1, 10)
                self.substituteNumbers(n1, n2)
 

    def swap2(self, axis=0, dim=0):
        '''
        Exchanges 2 rows or cols from the same slice (3 wide)
        Axis = 0: Exchanges rows
        Axis = 1: Exachanges cols

        dim = 0: Exchanges single row/col
        dim = 1: exchanges blocks of 3 rows/cols
        '''
        r1 = random.randint(0, 2)
        r2 = (r1 + random.randint(1, 2)) % 3
        band = 3* random.randint(0, 2)
        if dim == 0:
            if axis == 0:
                mem = self.board[r1+band,:].copy()
                self.board[r1+band,:] = self.board[r2+band,:].copy()
                self.board[r2+band,:] = mem.copy()
            else:
                mem = self.board[:,r1+band].copy()
                self.board[:,r1+band] = self.board[:,r2+band].copy()
                self.board[:,r2+band] = mem.copy()
        else:
            if axis == 0:
                mem = self.board[(r1 - r1%3):(r1 + 3 - r1%3),:].copy()
                self.board[(r1 - r1%3):(r1 + 3 - r1%3),:] = self.board[(r2 - r2%3):(r2 + 3 - r2%3),:].copy()
                self.board[(r2 - r2%3):(r2 + 3 - r2%3),:] = mem.copy()
            else:
                mem = self.board[:,(r1 - r1%3):(r1 + 3 - r1%3)].copy()
                self.board[:,(r1 - r1%3):(r1 + 3 - r1%3)] = self.board[:,(r2 - r2%3):(r2 + 3 - r2%3)].copy()
 
                self.board[:,(r2-r2%3):(r2+3-r2%3)] = mem.copy()


    def substituteNumbers(self, n1, n2):
        self.board[self.board==n1] = 0
        self.board[self.board==n2] = n1
        self.board[self.board==0] = n2


    def removeNumbers(self, n_left=40):
        n = 81
        while n > n_left:
            r = random.randint(0, 8)
            c = random.randint(0, 8)
            if not self.board[r,c] == 0:
                self.board[r, c] = 0
                n -= 1


if __name__ == "__main__":
    printer = PP()
#    board = np.zeros((9, 9), dtype=int)
#    board = np.ones((9, 9), dtype=int)
    my_sudoku = Sudoku(np.empty((9, 9), dtype=int))
    my_sudoku.generateBoard()
    my_sudoku.removeNumbers()
    printer.pprint(my_sudoku.board)
