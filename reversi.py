import numpy as np
import sys


white = 1
black = -1
empty = 0
board_length = 8

class Reversi:
    def __init__(self):
        self.board = np.zeros((board_length,board_length))
        self.board = self.board.astype(int)
        self.board[3][3] = self.board[4][4] = 1
        self.board[3][4] = self.board[4][3] = -1
        self.current = black

    def change_turn(self):
        self.current *= -1

    def empty_remains(self):
        for y in self.board:
            for x in y:
                if x == empty:
                    return True
                continue
        return False

    def current_remains(self):
        for y in self.board:
            for x in y:
                if x == self.current:
                    return True
                continue
        return False

    def is_in_board(self,x,y):
        if x < 0 or x + 1 > board_length  or y < 0 or y + 1 > board_length:
            return False
        return True

    def can_place_stone(self,x,y): 
        if not self.is_in_board(x,y):
            print('The coordinate is out of board')
            return False
        if self.board[y][x] != empty:
            print('The coordinate is already filled')
            return False
        return self.find_reversible_stone(x,y)


    def reversible_stones_length_on_direction(self,x,y,dx,dy):
        if not self.is_in_board(x + dx, y + dy):
            return 0
        length = 0
        if self.board[y + dy][x + dx] == self.current:
            return 0 
        else:    
            while self.board[y + dy][x + dx] == -self.current: 
                x += dx
                y += dy
                length += 1
                if self.board[y+dy][x+dx] == self.current:
                    return length
                elif self.board[y+dy][x+dx] == -self.current:
                    continue
                else: 
                    return 0
            else: 
                return 0

    def find_reversible_stone(self,x,y):
        for dx in range(-1,2):
            for dy in range(-1,2):
                if self.reversible_stones_length_on_direction(x,y,dx,dy) == 0:
                    continue
                else:
                    return True
        return False
                    

    def reverse_stone(self,x,y): 
            for dx in (-1,0,1):
                for dy in (-1,0,1):
                    length = self.reversible_stones_length_on_direction(x,y,dx,dy)
                    if length == None: length = 0
                    if length > 0:
                        for l in range(length):
                            k = l+1
                            self.board[y + dy*k][x + dx*k] *= -1

    def display(self):
        print('==='*10)
        for y in range(board_length):
            for x in range(board_length):
                if self.board[y][x] == white:
                    print('●', end = '  ')
                elif self.board[y][x] == black:
                    print('◯', end = '  ')
                else:
                    print('･', end = '  ')
            print('\n', end = '')
        if self.current == black:
            print('current: ○')
        else:
            print('current: ●')

    def put_stone(self,x,y):
        self.board[y][x] = self.current
        self.reverse_stone(x,y)

    
    def input_point(self):
        print('Input number(1~8)')
        x = input('x>>')
        try:
            x = int(x)-1
        except:
            if x == 'skip':
                return 999, 999
            print('Invalid input. Try again.')
            self.input_point()
        y = input('y>>')
        try:
            y = int(y)-1
        except:
            print('Invalid input. Try again.')
            self.input_point()
        return x, y    

    def judge_result(self):
        self.display()
        black_count = 0
        for y in range(board_length):
            for x in range(board_length):
                if self.board[y][x] == black:
                    black_count += 1
        if black_count > 32:
            print('Winner: ●')
        elif black_count == 32:
            print('Draw')
        else:
            print('Winner: ◯')

    def computer_turn(self):
        for y in range(board_length):
            for x in range(board_length):
                if self.can_place_stone(x,y):
                    print('computer placed on (' + str(x + 1) + ', ' + str(y + 1) + ')')
                    self.put_stone(x,y)
                    return
                else:
                    continue
        print('computer skipped')
    
    def play_two_players_mode(self):
        while(self.empty_remains() and self.current_remains()):
            print(self.current_remains)
            self.display()
            (x,y) = self.input_point() 
            if x == 999:
                print('Skipped')
                self.change_turn()
                continue
            if self.can_place_stone(x,y):
                self.put_stone(x,y)
                self.change_turn()
            else:
                print('Invalid coordinate. Try again.')
                continue       
    
    
    def play_computer_mode(self):
        while(self.empty_remains() and self.current_remains()):
            self.display()
            # Player is always black.
            if self.current == black:
                (x,y) = self.input_point() 
                if x == 999:
                    print('Skipped')
                    self.display()
                    continue
                if self.can_place_stone(x,y):
                    self.put_stone(x,y)
                    self.change_turn()
                else:
                    print('Invalid coordinate. Try again.')
                    continue
            else:
                self.computer_turn()
                self.change_turn()
    
    
    def play_game(self):
        print('computer mode: 1\nmulti-player mode: 2')
        res = input('>>')
        if res == '1':
            self.play_computer_mode()
        elif res == '2':
            self.play_two_players_mode()
        else:
            print('Invalid input')
            return
        self.judge_result()

if __name__ == '__main__':
    reversi = Reversi()
    reversi.play_game()