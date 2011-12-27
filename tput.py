#! /usr/bin/python


###
### tput
###
### module
###


### Wrapper fns:
###
### tput.colorize(fg, bg, bold)
### tput.cup
### tput.clear_with_bg_color(bg)
###


import sys # sys.argv
import optparse # optparse.OptionParser class
import os # os.system
import bash_fn # bash_fn.bf_s_aa
import tempfile # tempfile.NamedTemporaryFile class


_tput_state = {
 "fg": None,
 "bg": None,
 "bold": None}  # TODO I should find out the value of bold at the initialization time of tput, and set the state mirror to that.


# lifted straight from the COLOR_* attributes of
# the module curses
color_LUT = {
 "BLACK": 0,
 "BLUE": 4,
 "CYAN": 6,
 "GREEN": 2,
 "MAGENTA": 5,
 "RED": 1,
 "WHITE": 7,
 "YELLOW": 3}


def GetTputState():
    return _tput_state


# removes the effects of tput on color
def decolorize():
    os.system("tput sgr0") # TODO understand why sgr0

    # update the state mirror
    _tput_state["fg"] = None
    _tput_state["bg"] = None
    _tput_state["bold"] = False

    return GetTputState()
# end decolorize


def colorize(fg=None, bg=None, bold=None):
    # color names are all caps, like "GREEN".
    # fg and bg take color name strings or ints. bold takes a bool
    # if any arg is none, don't change that property at all

    # reset previous fg, bg, and bold
    decolorize()

    # fg
    if fg is not None:
        if isinstance(fg, str):
            fg = color_LUT[fg]
        
        os.system("tput setaf " + str(fg))

    # bg
    if bg is not None:
        if isinstance(bg, str):
            bg = color_LUT[bg]
    
        os.system("tput setab " + str(bg))

    # bold
    if bold is not None:
        if bold:
            os.system("tput bold")
    
    # update the state mirror
    _tput_state["fg"] = fg
    _tput_state["bg"] = bg
    _tput_state["bold"] = bold

    # return the new state
    # (in the user-presentable format returned by this method)
    return GetTputState()

# end colorize


# fill the screen with the bg color, and
# tput cup 0 0
def clear():
    os.system("tput clear")


# set cursor y, x
def cup(y, x):
    os.system("tput cup " + str(y) + " " +  str(x))

    return (x,y) # non-standard order


