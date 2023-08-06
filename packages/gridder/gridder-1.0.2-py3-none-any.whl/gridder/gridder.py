"""Gridder is a program to generate an image containing a grid according to provided settings.
    Copyright (C) 2018  Federico Salerno <itashadd+gridder[at]gmail.com>

Usage:
    Run gridder.py with the following arguments in the given order:
        # width of the desired image in pixels;
        # height of the desired image in pixels;
        # size of the grid, i.e. the side of each square of the grid in pixels.
    For example `gridder.py 1920 1080 30` will yield a 1920x1080 image
    named "grid.png" with lines at every 30px interval.


    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <https://www.gnu.org/licenses/>
"""

import argparse

from PIL import Image

from .converter import Converter
from .drawer import Drawer

arg_parser = argparse.ArgumentParser(prog="Gridder", add_help=False,
                                     description="A program to generate an image containing a grid according to "
                                                 "provided settings.")
arg_parser.add_argument("--file", "-f", action="append",
                        help="path to an image file to use as background for the grid. Use either this "
                             "OR width and height")

# First check if a file was specified.
file_arg, next_args = arg_parser.parse_known_args()

file_path = None
file_used = False
if file_arg.file is not None:
    # Only pick up the first path given, if more than one was specified.
    file_path = file_arg.file[0]
    file_used = True
else:
    # Only require/allow width and height if no file was given.
    arg_parser.add_argument("width",
                            help="width of the base image. Use either this and height OR -f")
    arg_parser.add_argument("height",
                            help="height of the base image. Use either width and this OR -f")

arg_parser.add_argument("grid_size",
                        help="the side of the square of the grid")
arg_parser.add_argument("--linewidth", "-lw", dest="line_width", default="1",
                        help="line width of the grid. Default: 1")
arg_parser.add_argument("--gridtype", "-gt", dest="grid_type", default="square",
                        choices=["square", "vhex", "hhex", "vline", "hline"],
                        help="type of grid. Can be square, vhex (vertical hexagon), hhex (horizontal hexagon), vline "
                             "(vertical line), hline (horizontal line). Default: square")
arg_parser.add_argument("--gridcol", "-grc", dest="grid_colour",
                        help="colour of the grid, as a colour name or hex value like #FFFFFF")
arg_parser.add_argument("--padding", "-p", default="0",
                        help="padding around the grid. Default: 0")
arg_parser.add_argument("--paddingtop", "-pt", dest="padding_top",
                        help="padding to the top of the grid. Takes priority over generic padding")
arg_parser.add_argument("--paddingright", "-pr", dest="padding_right",
                        help="padding to the right of the grid. Takes priority over generic padding")
arg_parser.add_argument("--paddingbottom", "-pb", dest="padding_bottom",
                        help="padding to the bottom of the grid. Takes priority over generic padding")
arg_parser.add_argument("--paddingleft", "-pl", dest="padding_left",
                        help="padding to the left of the grid. Takes priority over generic padding")
arg_parser.add_argument("--destination", "-d", default="grid",
                        help="destination file name for the final image, not including extension")

if not file_used:
    # Only allow background colour if not using -f.
    arg_parser.add_argument("--bgcol", "-bgc", dest="background_colour", default="transparent",
                            help="colour of the background, as a colour name or hex value like #000000. "
                                 "Default: transparent. Not allowed with -f")


# Collect option values
args = vars(arg_parser.parse_args(next_args))


background_colour = None
if not file_used:
    # Default to transparent for background.
    background_colour = args["background_colour"] if args["background_colour"] != "transparent" else (0, 0, 0, 0)


if __name__ == '__main__':
    # Build the arguments needed for the Drawer class.
    if file_used:
        args["base"] = Image.open(file_path)

        args["im_width"], args["im_height"] = args["base"].size
    else:
        args["im_width"] = Converter.to_px(args["width"])
        args["im_height"] = Converter.to_px(args["height"])

        args["base"] = Image.new("RGBA", (args["im_width"], args["im_height"]), background_colour)

    # Call Drawer class.
    Drawer.draw(args["grid_type"], **args)

    args["base"].save(args["destination"] if args["destination"].endswith(".png") else args["destination"]+".png")
