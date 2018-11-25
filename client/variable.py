#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 17:55:02 2018

@author: yiqianwang
variable
"""

class setvar:
    def __init__(self):
        global gdict
        gdict = {}
        self.cbtype = None
        self.fonttype = None
        self.OK = 0

    def setvalue(self, name, value):
        gdict[name] = value

    def getvalue(self, name, defValue=None):
        try:
            return gdict[name]
        except KeyError:
            return defValue

'''
self.cb14 = 'chessboard/cb14.png' # set background
self.cb8 = 'chessboard/cb8.png'
self.chessboard14 = 'chessboard/chessboard14.png' # set background
self.chessboard8 = 'chessboard/chessboard8.png'
self.ftype1 = "Roman times"
self.ftype2 = "Arial"
self.ftype3 = "Rockwell"
self.cbtype = self.chessboard14
self.fonttype = self.ftype1
self.OK = 0
'''