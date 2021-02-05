Title:  pysplit
Desc:   A python-based speedrun timer
Auth:   Evan Logue
Date:   2021-02-04

Files included in this repository:
readme.txt      Provides a summary of pysplit and its use
settings.ini    Configuration file for pysplit
main.py         Contains Main class
config.py       Contains ConfigParser class
timer.py        Contains Timer class

Module dependencies:
pygame

Description:
I have taken a recent interest in speedrunning, but speedrunning utilities for Linux users are few and far between. I
decided to use my (admittedly basic) python skills to whip up something for my own use; hopefully it is useful for
others as well.

Features:
    *   .ini based configuration for configuring the pysplit window
    *   Customizable hotkey for splitting
    *   Should be able to handle any number of splits (that will fit on the height defined in settings.ini)
    *   Provides comparisons between current elapsed time, WR elapsed time, and PB elapsed time
    *   Color codes splits and final time based on elapsed time comparisons

To-Do:
    *   Allow overwriting settings.ini after each run to overwrite PBs and WRs as applicable
    *   Create text based or GUI-based configuration wizard to make it easier to fill out splits and other info
    *   Eliminate some hard-coded features that I don't yet know how best to implement
    *   Implement resizable window with automatic text wrapping
    *   Implement split autoscroll to prevent splits from running off the edge of the set canvas size

Please feel free to adapt this code to your own needs or provide any feedback you may have. I'm trying to learn as much
as I can so I can create more useful software for myself and others in the future!

Enjoy!