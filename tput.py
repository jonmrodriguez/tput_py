#! /usr/bin/python


###
### tput
###
### main file
###
### created by "new_project"
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


tput_state = {
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
    return tput_state


# removes the effects of tput on color
def decolorize():
    os.system("tput sgr0") # TODO understand why sgr0

    # update the state mirror
    tput_state["fg"] = None
    tput_state["bg"] = None
    tput_state["bold"] = False

    return GetTputState()
# end decolorize


def colorize(fg="WHITE", bg="BLACK", bold=False):
    
    # first, convert color strings into ints
    # unsafe. I live on the edge, baby.
    if isinstance(fg, str):
        fg = color_LUT[fg]

    if isinstance(bg, str):
        bg = color_LUT[bg]

    # update the state mirror
    tput_state["fg"] = fg
    tput_state["bg"] = bg
    tput_state["bold"] = bold


    # reset previous fg, bg, and bold
    decolorize()

    # bold
    if bold:
        os.system("tput bold")

    # fg
    os.system("tput setaf " + str(fg))

    # bg
    os.system("tput setab " + str(bg))

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


