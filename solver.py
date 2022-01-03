class Solver:

    def __init__(self, board):
        self.board = board

    def backtrack(self):
        for i in range(0, 81):
            r = i//9
            c = i%9
            if self.board[r][c] == 0:
                dc = c%3 # Column offset for square range
                dr = r%3 # Row offset for square range
                # Check for all rows, columns and squares for each number in NUMBERLIST
                for n in self.NUMBER_LIST:
                    if not n in self.board[r,:]: # Current number not in row
                        if not n in self.board[:,c]: # Current number not in column
                            if not n in self.board[r-dr:r+3-dr, c-dc:c+3-dc]:
                                self.board[r][c] == n    
                            if self.checkBoard():
                                return True
                            else:
                                self.recursion_counter += 1
                                print(f'Recursion counter = {self.recursion_counter}')
                                if self.backtrack():
                                    return True
            break

    def checkBoard(self):
        for r in range(0, 9):
            for c in range(0, 9):
                if self.board[r][c] == 0:
                    return False

        return True



