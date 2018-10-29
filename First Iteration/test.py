import io
import os
import random
import chessboard # imports chessboard.py

def test_chessboard():
        chessboard.reset()
        #position out of range check
        t1 = chessboard.changevalue(-1,-1,1)
        assert (t1,0)
        #input value out of range check
        t2 = chessboard.changevalue(-1,-1,5)
        assert (t2,0)
        #occupy conflict
        t3 = chessboard.changevalue(2,3,2)
        assert (t3,1)
        t4 = chessboard.changevalue(2,3,1)
        assert (t4,0)

        #black win
        for n in range(5):
                b_valid = chessboard.changevalue(0,n,1) # put black at first row in order
                assert (b_valid,1)
                w_valid = chessboard.changevalue(random.randint(1,15),2*n,2) # put black at first row in order
                assert (w_valid,1)
        chessboard.checkwinner()



        
