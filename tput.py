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
 "bold": None}


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

    # tactic: use bash_fn to call tput

    # reset previous fg, bg, and bold
    bash_fn.bf_s_aa(["tput", "sgr0"])

    if bold:
        bash_fn.bf_s_aa(["tput", "bold"])

    # fg
    bash_fn.bf_s_aa(["tput", "setaf", str(fg)])

    # bg
    bash_fn.bf_s_aa(["tput", "setab", str(bg)])

    return GetTputState()

# end colorize


# fill the screen with the bg color, and
# tput cup 0 0
def clear():
    bash_fn.bf_s_aa(["tput", "clear"])


# set cursor y, x
def cup(y, x):
    bash_fn.bf_s_aa(["tput", "cup", str(y), str(x)])


