# pysplit
# A python-based speedrun splitter
# Evan Logue
# 2021-02-04

# MODULE IMPORTS
import pygame as pg


class Timer:
    def __init__(self):
        self.elapsed = 0
        self.split_time = 0
        self.start_time = pg.time.get_ticks()
        self.running = True
        self.splittimes = []

    def stop(self):
        if not self.running:
            return
        self.running = False
        self.elapsed += pg.time.get_ticks() - self.start_time
        return self.elapsed

    def start(self):
        if self.running:
            self.split()
            return
        self.running = True
        self.start_time = pg.time.get_ticks()

    def get(self):
        if self.running:
            return self.elapsed + pg.time.get_ticks() - self.start_time
        else:
            return self.elapsed

    def split(self):
        self.splittimes.append(self.get())

