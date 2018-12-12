#! /usr/bin/python
#import sys
from chessboard import chessboard
# inherit chessboard
# add e_value
class ai(chessboard):
    def __init__ (self, s, difficulty_1, val) :
        chessboard.__init__(self,s)
        self.e_value = [ [ 0 for i in range(self.size)] for j in range(self.size)]
        self.difficulty = difficulty_1
        self.h_val = val #human's value
        if val == 1:
            self.ai_val = 2
        else:
            self.ai_val = 1
        self.e_value_max = 0
        self.ai_row = 0
        self.ai_col = 0
    def reset_e_value(self):
        self.e_value = [ [ 0 for i in range(self.size)] for j in range(self.size)]

    def evluate_five(self,row,col,n_dir,val):
        x = row
        y = col
        #if next four pieces can be in a line
        for n in range(4):
            x = x + n_dir[0]
            y = y + n_dir[1]
            if self.getvalue(x,y) != val:
                self.e_value[row][col] = self.e_value[row][col] + n **2
                print ("update:",row,col,n,self.e_value[row][col])
                if self.e_value[row][col] > self.e_value_max:
                    self.e_value_max = self.e_value[row][col]
                    self.ai_row = row
                    self.ai_col = col
                return
        self.e_value[row][col] = self.e_value[row][col] + 30
        if self.e_value[row][col] > self.e_value_max:
            print ("update:",row,col,self.e_value[row][col])
            self.e_value_max = self.e_value[row][col]
            self.ai_row = row
            self.ai_col = col
        return




    #input is the human step and val
    def decision(self,row,col):
        self.reset_e_value()
        self.e_value_max = 0
        self.ai_row = 0
        self.ai_col = 0
        if(self.difficulty == 1):
            #find the closet position
            minimum = 10000
            ai_row = 0
            ai_col = 0
            for i in range(self.size):
                for j in range(self.size):
                    if (self.getvalue(i,j) == 0):
                        temp = (row - i)**2 + (col - j)**2
                        if (temp < minimum):
                            minimum = temp
                            ai_row = i
                            ai_col = j
            valid = self.changevalue(ai_row,ai_col,self.ai_val)
            if valid == 1:
                return (ai_row,ai_col)
            else:
                return None
        else:
            dir = ((0,1),(0,-1),(1,-1),(-1,1),(1,0),(-1,0),(1,1),(-1,-1))
            #check each point
            for i in range(self.size):
                for j in range(self.size):
                    #if the point is empty
                    if (self.getvalue(i,j) == 0):
                        for d in dir:
                            self.evluate_five(i,j,d,self.h_val)
                            if (self.difficulty == 3):
                                self.evluate_five(i,j,d,self.ai_val)
            valid = self.changevalue(self.ai_row,self.ai_col,self.ai_val)

            return (self.ai_row,self.ai_col)
            # get the maximum
