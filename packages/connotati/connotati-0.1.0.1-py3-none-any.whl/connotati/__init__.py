#!/bin/env python3

#    connotati
#
#    ----------------------------------------------------------------------
#    Copyright © 2018  Pellegrino Prevete
#
#    All rights reserved
#    ----------------------------------------------------------------------
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from argparse import ArgumentParser
from subprocess import Popen, PIPE
from subprocess import check_output as sh
from os import environ
from os.path import abspath, dirname
from time import sleep

name="connotati"

class Connotati:
    """Launch gtk app with dark theme variant.
    
    Works even on non-headerbar windows if xdotool and xprop are present; will apply to new
    application windows every given seconds
    
    Args:
        command (list): command to execute ("echo uzz" -> ['echo', 'uzz']);
        window_title_pattern: pattern that application windows name will share (usually name of the app);
        theme (str): theme to be used;
        variant (str): variant of the theme;
        refresh_time (int): seconds every which xdotool and xprop have to try to change titlebar style;
        verbose (bool): flag for verbose.
    """
    def __init__(self, command, window_title_pattern=[], theme="Adwaita", variant="dark", refresh_time=100, verbose=False):

        executable_path = dirname(abspath(__file__))
        xdotool_command = ['xdotool', 'search', '--name'] + window_title_pattern
        xprop_command = ['xprop', '-f', '_GTK_THEME_VARIANT', '8u', '-set', '_GTK_THEME_VARIANT', variant, "-id"]
        
        gtk_dark_environ = environ.copy()
        gtk_dark_environ["GTK_THEME"] = theme + ":" + variant
        
        output = Popen(command, encoding="UTF-8", stdout=PIPE, env=gtk_dark_environ)
      
        del gtk_dark_environ["GTK_THEME"] 

        if window_title_pattern != None: 
            while True:
                windows = []
                try:
                    windows = sh(xdotool_command, encoding="UTF-8").split("\n")
                except:
                    pass
                windows = [w for w in windows if w != ""]
                for w in windows:
                    try:
                        sh(xprop_command + [w], encoding="UTF-8")
                    except:
                        pass
                sleep(refresh_time)

def main():
    parser = ArgumentParser(description="start gtk app (even those with titlebars and multiple windows) with given theme and variant")
    parser.add_argument("command", nargs='+', help="command to execute")
    parser.add_argument("--window-title-pattern", nargs=1, action='store', default=[], help="pattern that application windows name will share (usually name of the app)")
    parser.add_argument("--theme", dest="theme", nargs=1, action='store', default=['Adwaita'], help="theme to be applied (default: Adwaita);")
    parser.add_argument("--variant", dest="variant", nargs=1, action='store', default=['dark'], help="variant of the theme to be used;")
    parser.add_argument("--refresh-time", dest="refresh_time", nargs=1, action="store", default=[100], help="if N, it will try change window titlebar satisfying pattern every N seconds;") 
    parser.add_argument("--verbose", dest="verbose", action="store_true", default=False, help="extended output")

    args = parser.parse_args()
    if args.verbose:
        print(args)
    app = Connotati(command=args.command, window_title_pattern=args.window_title_pattern, theme=args.theme[0], variant=args.variant[0], refresh_time=int(args.refresh_time[0]), verbose=args.verbose)

