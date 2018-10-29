#! /usr/bin/python
import sys

class chessboard(object):

        #initialize
        def __init__ (self) :
                self.size = 15
                self.board = [ [ 0 for i in range(self.size)] for j in range(self.size)] #build a size * size chessboard
                self.steplist = [];
        #reset
        def reset (self):
                #reset value for each point = 0; empty: 0; black: 1; white: 2;
                self.steplist[:] = []
                for i in range(self.size):
                        for j in range(self.size):
                                self.board[i][j] = 0
                return 0
        #get the value (empty: 0; black: 1; white: 2;invalid:-1)
        def getvalue(self,row,col):
                if (row < 0) or (row >= self.size) or (col < 0)or(col >= self.size):#invalid position
                        return -1
                else:
                        return self.board[row][col]
        #put the value of point after each round (fail:0;success:1)
        def changevalue(self,row,col,val):
                if (self.getvalue(row, col) == 0): #position emoty
                        self.steplist.append((row,col))
                        self.board[row][col] = val
                        return 1
                else:
                        return 0
        #check five continuous piece
        def five_in_line(self,val,row,col,n_dir):
                x = row
                y = col
                #if next four pieces can be in a line
                for n in range(4):
                        x = x + n_dir[0]
                        y = y + n_dir[0]
                        if self.getvalue(x,y) != val:
                                return False
                return True
        #check if there is a winner (0:unfinished; 1:black win; 2:white win; 3:draw)
        def checkwinner(self):
                t_board = self.board
                #test the first piece and check if the next piece exists for each direction
                dir = ((0,1),(1,-1),(1,0),(1,1))
                Full = True
                #check each point
                for i in range(self.size):
                        for j in range(self.size):
                                #if the point is empty
                                if (self.getvalue(i,j) == 0):
                                        Full = False
                                #if note empty, check the next piece
                                else:
                                        p_value =  self.getvalue(i,j)
                                        # check five in lines
                                        for d in dir:
                                                if (self.five_in_line(p_value,i,j,d)):
                                                        return p_value
                #no one wins
                if (Full == True):
                        return 3
                else:
                        return 0
        #return each step in a list
        def sendsteps(self):
            return self.steplist
        #return size
        def getsize(self):
            return self.size
