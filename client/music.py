#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 20:00:06 2018

@author: yiqianwang
music
"""
import sys, os
import pygame
from pygame.locals import KEYDOWN, K_SPACE
from PyQt5.QtCore import QThread
import os.path

class musicplayer(QThread):
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        #pygame.mixer.music.load('music/music1.ogg')
        pygame.mixer.music.set_volume(0.2)
        #pygame.mixer.music.play(-1)
        #current_path = sys.path[0] + '/'
        #self.musicpath = current_path + 'music/'
        self.get_music()

    def resource_path(self, relative_path):
        # related path
        if hasattr(sys, "_MEIPASS"):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def get_music(self):
        self.musicpath = self.resource_path('music/')
        folder = os.listdir(self.musicpath)
        self.music_files = []
        for filename in folder:
            if filename.lower().endswith('.ogg'):
                self.music_files.append(self.musicpath + filename)
        print(self.music_files)
        # init
        self.current = 0
        self.total = len(self.music_files)
        pygame.mixer.music.load(self.music_files[self.current])
        pygame.mixer.music.play()
        print('Now playing:', self.music_files[self.current])

    def mute(self):
        pygame.mixer.music.pause()

    def unmute(self):
        pygame.mixer.music.unpause()

    def nextsong(self):
        self.current = (self.current + 1) % self.total
        pygame.mixer.music.load(self.music_files[self.current])
        pygame.mixer.music.play()
        print('Now playing:', self.music_files[self.current])
        
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

    def test(self):
        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.nextsong()

    def stop(self):
        pygame.mixer.music.stop()

def main():
    try:
        bgmusic = musicplayer()
        bgmusic.start()
    except KeyboardInterrupt:
        bgmusic.stop()

if __name__ == '__main__':
    main()
