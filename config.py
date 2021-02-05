# pysplit
# A python-based speedrun splitter
# Evan Logue
# 2021-02-04

# MODULE IMPORTS
from configparser import ConfigParser
from os import path
import ast
from math import floor


# PARSER CLASS
class Parser:
    def __init__(self):
        ...

    # LOAD FROM SETTINGS FILE
    def load(self):
        # SET DIRECTORIES
        dir_local = path.dirname(__file__)
        settings = path.join(dir_local, "settings.ini")

        # LOAD SETTINGS FROM FILE
        config = ConfigParser()
        config.read(settings)

        # PARSE VARIABLES
        self.c_bg = ast.literal_eval(config.get('THEME', 'bg'))
        self.c_def = ast.literal_eval(config.get('THEME', 'def'))
        self.c_off = ast.literal_eval(config.get('THEME', 'off'))
        self.c_ahead = ast.literal_eval(config.get('THEME', 'ahead'))
        self.c_behind = ast.literal_eval(config.get('THEME', 'behind'))
        self.c_gold = ast.literal_eval(config.get('THEME', 'gold'))
        self.c_wr = ast.literal_eval(config.get('THEME', 'wr'))
        self.width = int(config.get('THEME', 'width'))
        self.height = int(config.get('THEME', 'height'))

        self.splitkey = config.get('KEYBINDS', 'splitkey')

        self.title = config.get('GAME', 'title')
        self.category = config.get('GAME', 'category')
        self.attempts = int(config.get('GAME', 'attempts'))

        self.wrtime = config.get('TIMES', 'wrtime')
        self.wrholder = config.get('TIMES', 'wrholder')
        self.wrdate = config.get('TIMES', 'wrdate')
        self.pbtime = config.get('TIMES', 'pbtime')

        # GET NUMBER OF SPLITS IN SETTINGS FILE
        self.splitcount = 0
        for section in config.sections():
            if "SPLIT" in section:
                self.splitcount += 1

        self.splittitles = []
        self.wrsplits = []
        self.wrtotals = []
        self.pbsplits = []
        self.pbtotals = []

        for split in range(self.splitcount):
            # PUT SPLIT INFORMATION INTO LISTS
            sec = "SPLIT" + str(split)
            self.splittitles.append(config.get(sec, 'title'))
            self.wrsplits.append(config.get(sec, 'wrsplit'))
            self.wrtotals.append(config.get(sec, 'wrtotal'))
            self.pbsplits.append(config.get(sec, 'pbsplit'))
            self.pbtotals.append(config.get(sec, 'pbtotal'))

        self.wrsplits_t = []
        self.wrtotals_t = []
        self.pbsplits_t = []
        self.pbtotals_t = []
        for split in range(self.splitcount):
            # PUT SPLIT INFORMATION INTO INTEGER LIST OF LISTS
            self.wrsplits_t.append(self.convert_to_ms(self.wrsplits[split]))
            self.wrtotals_t.append(self.convert_to_ms(self.wrtotals[split]))
            self.pbsplits_t.append(self.convert_to_ms(self.pbsplits[split]))
            self.pbtotals_t.append(self.convert_to_ms(self.pbtotals[split]))

    # CONVERT STRING TIME TO MILLISECOND TIME
    def convert_to_ms(self, target):
        # SPLIT HOURS, MINUTES, AND SECONDS AT :
        timelist = target.split(":")
        # SPLIT SECONDS AND MILLISECONDS AT .
        ms_split = timelist[2].split(".")
        # REPLACE SS.sss IN timelist WITH SS, sss
        timelist[2] = ms_split[0]
        timelist.append(ms_split[1])
        # EXTRACT STRINGS AND CONVERT TO INTEGERS
        hours = int(timelist[0])
        minutes = int(timelist[1])
        seconds = int(timelist[2])
        milliseconds = int(timelist[3])
        # CALCULATE ms FROM H, M, and S
        mstime = milliseconds + seconds * 1000 + minutes * 60000 + hours * 60000 * 3600
        return mstime

    # CONVERT MILLISECOND TIME TO STRING TIME
    def convert_to_str(self, target):
        # CALCULATE H, M, and S FROM ms
        hours = floor(target / 60000 / 3600)
        mstarget = target - hours * 60000 * 3600
        minutes = floor(mstarget / 60000)
        starget = mstarget - minutes * 60000
        seconds = floor(starget / 1000)
        ms = starget - seconds * 1000
        hours = str(hours).zfill(2)
        minutes = str(minutes).zfill(2)
        seconds = str(seconds).zfill(2)
        ms = str(ms).zfill(3)

        return hours + ":" + minutes + ":" + seconds + "." + ms
