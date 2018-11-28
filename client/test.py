import io
import os
import random
from chessboard import *# imports chessboard.py

def test_chessboard():
		obj = chessboard(15)
		obj.reset()
		#position out of range check
		t1 = obj.changevalue(-1,-1,1)
		assert t1==0
		#input value out of range check
		t2 = obj.changevalue(-1,-1,5)
		assert t2==0
		#occupy conflict
		t3 = obj.changevalue(2,3,2)
		assert t3==1
		t4 = obj.changevalue(2,3,1)
		assert t4==0
		obj.reset()
		#black win 1 (five in a row)
		for n in range(5):
				b_valid1 = obj.changevalue(0,n,1)
				assert b_valid1==1
				w_valid1 = obj.changevalue(2,2*n,2)
				assert w_valid1==1
		winner1 = obj.checkwinner()
		assert winner1==1
		obj.reset()
		#black win 2 (five in a column)
		for n in range(5):
				b_valid2 = obj.changevalue(n,0,1)
				assert b_valid2==1
				w_valid2 = obj.changevalue(2*n,3,2)
				assert w_valid2==1
		winner2 = obj.checkwinner()
		assert winner2==1
		obj.reset()
		#black win 3 (five in a polyline)
		for n in range(5):
				b_valid3 = obj.changevalue(n,n,1)
				assert b_valid3==1
				w_valid3 = obj.changevalue(5,2*n,2)
				assert w_valid3==1
		winner3 = obj.checkwinner()
		assert winner3==1
		obj.reset()
		#white win 1
		for n in range(5):
				b_valid4 = obj.changevalue(5,2*n,1)
				assert b_valid4==1
				w_valid4 = obj.changevalue(3,n,2)
				assert w_valid4==1
		winner4 = obj.checkwinner()
		assert winner4 == 2
		obj.reset()
		#test the loop
		#test inside loop first 
		# black five in a polyline
		for n in range(5):
				b_valid5 = obj.changevalue(n,n,1)
				assert b_valid5==1
				w_valid5 = obj.changevalue(5,2*n,2)
				assert w_valid5==1
		b_valid5 = obj.changevalue(0,1,1)
		assert b_valid5==1
		b_valid5 = obj.changevalue(0,2,1)
		assert b_valid5==1
		b_valid5 = obj.changevalue(0,3,1)
		assert b_valid5==1
		b_valid5 = obj.changevalue(1,0,1)
		assert b_valid5==1
		b_valid5 = obj.changevalue(2,0,1)
		assert b_valid5==1
		looptest = obj.five_in_line(2,0,0,(1,1))
		assert looptest== False
		looptest = obj.five_in_line(1,0,0,(0,1))
		assert looptest== False
		looptest = obj.five_in_line(1,0,0,(1,0))
		assert looptest== False
		looptest = obj.five_in_line(1,0,0,(1,1))
		assert looptest== True
		
		winnertest = obj.checkwinner
		assert winnertest == 1

test_chessboard()
