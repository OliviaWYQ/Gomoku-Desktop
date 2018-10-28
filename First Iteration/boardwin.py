#! /usr/bin/python
import sys




class chessboard(object):
  
        size = 9 #  size of chessboard
    
    
        #initialize
        def __init__ (self) :
                #build a size * size chessboard
                self.board = [ [ 0 for i in range(size)] for j in range(size)]
        #reset
        def reset (self):
                #reset value for each point = 0; empty: 0; black: 1; white: 2;
                for i in range(size):
                        for j in range(size):
                                self.board[i][j] = 0
                return 0


        #get the value of point if we have row and col
        def getvalue(self,row,col):
                #check if row and col are out of range
                if (row < 0) or (row >= size) or (col < 0)or(col >= size):
                        return -1
                else:
                        return self.board[row][col]

        #put the value of point after each round
        def changevalue(self,row,col,val):
                if (row < 0)or(row >= size)or(col < 0)or(col >= size):
                        return
                else:
                        self.board[i][j] = val
                        return




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
                for i in range(size):
                        for j in range(size):
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
                return 0
