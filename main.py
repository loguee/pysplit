# pysplit
# A python-based speedrun splitter
# Evan Logue
# 2021-02-04

# MODULE IMPORTS
import pygame as pg
from os import path
import sys
import os
from configparser import ConfigParser

# CLASS IMPORTS
from config import *
from timer import *


# MAIN CLASS
class Main:
    def __init__(self):
        # FORCE OPEN IN UPPER-LEFT CORNER
        x = 1
        y = 1
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)

        pg.init()
        self.timer = Timer()
        self.parser = Parser()
        self.parser.load()
        self.screen = pg.display.set_mode((self.parser.width, self.parser.height))
        pg.display.set_caption("pysplit")

        self.timing = False
        self.current_split = 1
        pg.key.set_repeat(1000, 1000)

    # RUN METHOD
    def run(self):
        self.running = True
        while self.running:
            self.events()
            self.draw()

    # EVENT METHOD
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if pg.key.name(event.key) == self.parser.splitkey:
                    self.timer.start()
                    self.current_split += 1

    # DRAW TEXT
    def draw_text(self, surf, text, size, x, y, alignment, color):
        self.font = pg.font.Font(pg.font.match_font('arial'), size)
        self.text_surface = self.font.render(text, True, color)
        self.text_rect = self.text_surface.get_rect()
        if alignment == "c":
            self.text_rect.center = (x, y)
        if alignment == "l":
            self.text_rect = (x, y)
        surf.blit(self.text_surface, self.text_rect)

    # DRAW METHOD
    def draw(self):
        self.screen.fill(self.parser.c_bg)

        # DRAW GAME TITLE AND RUN CATEGORY
        self.draw_text(self.screen, self.parser.title + " " + self.parser.category, 20, self.parser.width / 2, 10, "c",
                       self.parser.c_def)
        pg.draw.line(self.screen, self.parser.c_def, (0, 25), (self.parser.width, 25))

        # DRAW CURRENT WR INFO
        self.draw_text(self.screen, "Current WR", 18, self.parser.width / 2, 35, "c", self.parser.c_def)
        self.draw_text(self.screen, self.parser.wrtime, 15, self.parser.width / 2, 50, "c", self.parser.c_off)
        self.draw_text(self.screen, "By " + self.parser.wrholder + " on " + self.parser.wrdate, 15,
                       self.parser.width / 2, 65, "c", self.parser.c_off)
        pg.draw.line(self.screen, self.parser.c_def, (0, 75), (self.parser.width, 75))

        # DRAW ATTEMPT COUNTER
        self.draw_text(self.screen, "Attempts", 18, self.parser.width / 2, 85, "c", self.parser.c_def)
        self.draw_text(self.screen, str(self.parser.attempts), 15, self.parser.width / 2, 100, "c", self.parser.c_off)
        pg.draw.line(self.screen, self.parser.c_def, (0, 110), (self.parser.width, 110))

        # DRAW SPLIT HEADINGS
        self.col = [0, 130, 230, 330]
        self.draw_text(self.screen, "Name", 15, self.col[0], 115, "l", self.parser.c_def)
        self.draw_text(self.screen, "WR Time", 15, self.col[1], 115, "l", self.parser.c_def)
        self.draw_text(self.screen, "Elapsed", 15, self.col[2], 115, "l", self.parser.c_def)
        self.draw_text(self.screen, "Split", 15, self.col[3], 115, "l", self.parser.c_def)
        pg.draw.line(self.screen, self.parser.c_def, (0, 340), (self.parser.width, 340))

        # GET LISTS FROM CONFIG
        for split in range(self.parser.splitcount):
            title = self.parser.splittitles[split]
            wrsplit = self.parser.wrsplits[split]
            wrtotal = self.parser.wrtotals[split]
            pbsplit = self.parser.pbsplits[split]
            pbtotal = self.parser.pbtotals[split]

            # SET VERTICAL INCREMENT
            gap = 140 + split * 20

            # DRAW SPLIT TITLES
            self.draw_text(self.screen, title, 15, self.col[0], gap, "l", self.parser.c_off)
            # DRAW WR TOTAL TIMES
            self.draw_text(self.screen, wrtotal, 15, self.col[1], gap, "l", self.parser.c_off)
            # IF SPLIT OCCURS, DRAW LAST TOTAL TIME
            if 0 <= split < len(self.timer.splittimes):
                self.draw_text(self.screen, str(self.parser.convert_to_str(self.timer.splittimes[split])), 15,
                               self.col[2], gap, "l", self.parser.c_off)
                # COMPARE ELAPSED TIME TO WR AND PB ELAPSED TIMES
                pbcompare = self.timer.splittimes[split] - self.parser.pbtotals_t[split]
                abspbcompare = abs(pbcompare)
                wrcompare = self.timer.splittimes[split] - self.parser.wrtotals_t[split]
                abswrcompare = abs(wrcompare)
                # COLOR SPLIT TIME BASED ON WR AND PB COMPARISON
                if pbcompare <= 0:
                    self.draw_text(self.screen, str(self.parser.convert_to_str(abswrcompare)), 15, self.col[3], gap,
                                   "l", self.parser.c_gold)
                elif wrcompare <= 0:
                    self.draw_text(self.screen, str(self.parser.convert_to_str(abswrcompare)), 15, self.col[3], gap,
                                   "l", self.parser.c_ahead)
                elif wrcompare > 0:
                    self.draw_text(self.screen, str(self.parser.convert_to_str(abswrcompare)), 15, self.col[3], gap,
                                   "l", self.parser.c_behind)

        # DRAW CURRENT TOTAL TIME IN ACTIVE SPLIT ROW UNTIL END OF SPLITS IS REACHED
        if self.current_split <= self.parser.splitcount:
            gap = 140 + (self.current_split - 1) * 20
            self.draw_text(self.screen, str(self.parser.convert_to_str(self.timer.get())), 15, self.col[2], gap, "l",
                           self.parser.c_def)
            self.draw_text(self.screen, str(self.parser.convert_to_str(self.timer.get())), 30, self.parser.width / 2,
                           360, "c", self.parser.c_def)
        else:
            self.timer.stop()
            # DRAW FINAL TIME, COLORED BASED ON RESULT
            if wrcompare <= 0:
                self.finalcolor = self.parser.c_wr
            elif pbcompare <= 0:
                self.finalcolor = self.parser.c_gold
            elif wrcompare > 0:
                self.finalcolor = self.parser.c_behind
            self.draw_text(self.screen, str(self.parser.convert_to_str(self.timer.get())), 30, self.parser.width / 2,
                           360, "c", self.finalcolor)

        pg.display.update()

    # QUIT METHOD
    def quit(self):
        pg.quit()
        sys.exit()

    # WRITE NEW CONFIG
    def write(self):
        ...


# CALL CLASS INSTANCE
m = Main()

while True:
    m.run()
