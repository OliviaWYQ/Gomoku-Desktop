#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 13:45:19 2018

@author: yiqianwang

Main function
"""

import showchessboard3

def main():
    app = QApplication(sys.argv)
    game = Gomoku()
    game.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()
