#! /usr/bin/python
import sys

# inherit chessboard
# add e_value
class ai(chessboard):
    def __init__ (self, s , difficulty_1, val) :
        chessboard.__init__(self,s)
        self.e_value = [ [ 0 for i in range(self.size)] for j in range(self.size)]
        self.difficulty = difficulty_1
        self.h_val = val #human's value
        if val == 1:
            self.ai_val = 2
        else:
            self.ai_val = 1

    def evluate_five(self,row,col,n_dir):
        x = row
        y = col
        #if next four pieces can be in a line
        for n in range(4):
            x = x + n_dir[0]
            y = y + n_dir[1]
            if self.getvalue(x,y) != self.h_val:
                self.e_value[row][col] = self.e_value[row][col] + n
                return
        self.e_value[row][col] = self.e_value[row][col] + 4
        return

    def maximum_loc(self):
        max = 0        
        for i in range(self.size):
            for j in range(self.size):
                if (self.getvalue(i,j) == 0):
                    if (self.e_value[i][j] > max):
                        max = self.e_value[i][j]
                        ai_row = i
                        ai_row = j
        valid = self.changevalue(ai_row,ai_col,self.ai_val)
        if valid == 1:
            return (ai_row,ai_col)
        else:
            return None

    #user is always black
    #input is the human step and val
    def decision(self,row,col):
        if(self.difficulty == 1):
            #find the closet position
            min = 100
            for i in range(self.size):
                for j in range(self.size):
                    if (self.getvalue(i,j) == 0):
                        temp = min(abs(row - i), abs(col - j))
                        if (temp < min):
                            min = temp
                            ai_row = i
                            ai_col = j
            valid = self.changevalue(ai_row,ai_col,self.ai_val)
            if valid == 1:
                return (ai_row,ai_col)
            else:
                return None
        else:
            if (self.difficulty == 2):
                dir = ((0,1),(1,-1),(1,0),(1,1))
            else :
                dir = ((0,1),(0,-1),(1,-1),(-1,1),(1,0),(-1,0),(1,1),(-1,-1))
            #check each point
            for i in range(self.size):
                for j in range(self.size):
                    #if the point is empty
                    if (self.getvalue(i,j) == 0):
                        for d in dir:
                            self.evluate_five(i,j,d,self.h_val)
            return self.maximum_loc()
            # get the maximum
