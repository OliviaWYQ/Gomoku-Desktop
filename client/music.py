#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 20:00:06 2018

@author: yiqianwang
music
"""
import sys, os
import pygame
from pygame.locals import *
from PyQt5.QtCore import QThread

class musicplayer(QThread):
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load('music/music1.ogg')
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)

    def mute(self):
        pygame.mixer.music.set_volume(0)

    def unmute(self):
        pygame.mixer.music.set_volume(0.2)
        
    def start(self):
        pause = False
        #keymap = {}
        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    #keymap[event.scancode] = event.unicode
                    if event.key == K_SPACE:  # push space
                        pause = not pause
                        print("music pause", pause)

            if pause:
                pygame.mixer.music.pause()  # pause
            else:
                pygame.mixer.music.unpause()  # unpause

    def stop(self):
        pygame.mixer.music.stop()
'''
def main():
    try:
        bgmusic = musicplayer()
        bgmusic.start()
    except KeyboardInterrupt:
        bgmusic.stop()

if __name__ == '__main__':
    main()
'''