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
import tempfile # tempfile.NamedTemporaryFile class
import copy


# lifted straight from the COLOR_* attributes of
# the module curses
color_LUT = {
 "BLACK": 0,
 "RED": 1,
 "GREEN": 2,
 "YELLOW": 3,
 "BLUE": 4,
 "MAGENTA": 5,
 "CYAN": 6,
 "WHITE": 7,

 # need xterm-256color beyond this point
 "DARK_GRAY": 8,
 # TODO more of the 256 colors
}


###
### Default color schemes
JRODAIR_BG = "BLACK"
CORN_MYTH_CONTROLMASTER_BG = "BLUE"
CORN_MYTH_PASSENGER_BG = "DARK_GRAY" # passenger means not controlmaster, aka just along for the ride



###
### Compute _tput_default_state
### based on (env=os.environ)

def create_default_state(env):

    os_type = env['OSTYPE']
    hostname = env['HOSTNAME']

    cluster = "cluster_not_recognized"
    #
    if os_type[0:6] == "darwin":
        cluster = "jrodair"
    elif hostname[0:4] == "corn":
        cluster = "corn"
    elif hostname[0:4] == "myth":
        cluster = "myth"

    ssh_tty = "local_tty"
    #
    if 'SSH_TTY' in env:
        ssh_tty = env['SSH_TTY']

    i_am_controlmaster = (ssh_tty == "/dev/pts/0") # the 0th pseudoterminal was the first session to connect =]

    # choose default fg
    fg = color_LUT['WHITE']

    # choose default bg
    #
    bg = "FAIL AND EXPLODE. UNANTICIPATED CLUSTER."
    #
    if cluster == "jrodair":
        bg = JRODAIR_BG
    elif cluster == "corn" or cluster == "myth":
        if i_am_controlmaster:
            bg = CORN_MYTH_CONTROLMASTER_BG
        else:
            bg = CORN_MYTH_PASSENGER_BG

    # choose deafult boldness
    bold = False

    # to return
    retval_default_state = {
        "fg": fg,
        "bg": bg,
        "bold": bold
    }

    return retval_default_state

# end def


_tput_default_state = create_default_state(env=os.environ)

_tput_state = copy.copy(_tput_default_state)



def GetTputState():
    return _tput_state


def colorize(fg=None, bg=None, bold=None):
    # color names are all caps, like "GREEN".
    # fg and bg take color name strings or ints. bold takes a bool
    # if any arg is none, don't change that property at all

    # reset previous fg, bg, and bold
    os.system("tput sgr0")

    # fg
    #
    if fg is None:
        fg = _tput_default_state['fg']
    #
    if isinstance(fg, str):
        fg = color_LUT[fg]
    #
    os.system("tput setaf " + str(fg))

    # bg
    #
    if bg is None:
        bg = _tput_default_state['bg']
    #
    if isinstance(bg, str):
        bg = color_LUT[bg]
    #
    os.system("tput setab " + str(bg))

    # bold
    #
    if bold is None:
        bold = _tput_default_state['bold']
    #
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


# restore to _tput_default_state
def decolorize():
    return colorize()


# fill the screen with the bg color, and
# tput cup 0 0
def clear():
    os.system("tput clear")


# set cursor y, x
def cup(y, x):
    os.system("tput cup " + str(y) + " " +  str(x))

    return (x,y) # non-standard order



###
###

# $PS1 triggers $(tput.py decolorize)
if __name__ == "__main__":
    
    if sys.argv[1] == "decolorize":
        decolorize()

    # possible TODO other commands. not urgent and YAGNI.


