"""Gridder is a program to generate an image containing a grid according to provided settings.
    Copyright (C) 2018  Federico Salerno <itashadd+gridder[at]gmail.com>

    Drawer class to draw grids on images.


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

import re

import numpy as np
from PIL import ImageDraw as Draw

from .converter import Converter


class Drawer:
    """Drawer class to draw grids on PIL Image objects. Call Drawer.draw() to use."""
    __slots__ = []

    @staticmethod
    def draw(shape: str, **kwargs) -> None:
        """Detect the shape to draw and draw it. Defaults to square on unknown shape.

        :param shape: the name of the shape to draw. Required. Options: square (default), vline, hline, vhex, hhex.
        :key base: the PIL.Image on which to draw. Required.
        :key im_width: width of the image to draw on. Required.
        :key im_height: height of the image to draw on. Required.
        :key grid_size: size of the elements of the grid; exact semantics depend on shape. Required.
        :key padding: padding around the edges of the image before the grid is drawn. Default: 0.
            Options for padding_top, _right, _bottom and _left also exist and take priority over generic padding.
        :key grid_colour: colour of the grid elements. Default: black.

        :raise ValueError: if the required arguments are not present or are unusable.
        """

        # The dictionary of draw methods will update automatically as methods are added to Drawer.
        drawer = {re.split(r"_draw_", k)[1]: v.__func__  # Select the shape name as key and the callable as value.
                  for k, v in Drawer.__dict__.items()
                  if isinstance(v, staticmethod) and re.fullmatch(r"_draw_[^_]+", k)}

        # Check validity of arguments
        for req_arg in ("base", "grid_size", "im_width", "im_height"):
            if req_arg not in kwargs.keys():
                raise ValueError(f"{req_arg} is required.")

            if kwargs[req_arg] == "":
                raise ValueError(f"{req_arg} cannot be empty.")

        # Set up the needed arguments.
        kwargs["grid"] = Draw.Draw(kwargs["base"])

        kwargs["im_width"] = max(Converter.to_px(kwargs["im_width"]), 1)
        kwargs["im_height"] = max(Converter.to_px(kwargs["im_height"]), 1)
        kwargs["grid_size"] = max(Converter.to_px(kwargs["grid_size"]), 1)

        kwargs.setdefault("line_width", 1)
        kwargs["line_width"] = max(Converter.to_px(kwargs["line_width"]), 1)

        kwargs.setdefault("grid_colour", "black")

        # Set padding options. Specific sides have priority over the generic setting.
        kwargs.setdefault("padding", 0)
        kwargs["padding"] = max(Converter.to_px(kwargs["padding"]), 0)
        for opt_arg in ("padding_top", "padding_right", "padding_bottom", "padding_left"):
            kwargs.setdefault(opt_arg, kwargs["padding"])
            kwargs[opt_arg] = Converter.to_px(kwargs[opt_arg])

        # Call the appropriate shape drawer. Default to square.
        try:
            drawer[shape](**kwargs)
        except IndexError:
            drawer["square"](**kwargs)

    @staticmethod
    def _draw_square(**kwargs):
        """Draw a square grid."""
        # Vertical lines.
        for x in range(0, kwargs["im_width"], kwargs["grid_size"]):
            kwargs["grid"].line([(min(max(x, kwargs["padding_left"]), kwargs["im_width"] - kwargs["padding_right"]),
                                  max(0, kwargs["padding_top"])),
                                 (min(max(x, kwargs["padding_left"]), kwargs["im_width"] - kwargs["padding_right"]),
                                  kwargs["im_height"] - kwargs["padding_bottom"])],
                                fill=kwargs["grid_colour"], width=kwargs["line_width"])

        # Horizontal lines.
        for y in range(0, kwargs["im_height"], kwargs["grid_size"]):
            kwargs["grid"].line([(max(0, kwargs["padding_left"]),
                                  min(max(y, kwargs["padding_top"]), kwargs["im_height"] - kwargs["padding_bottom"])),
                                 (kwargs["im_width"] - kwargs["padding_right"],
                                  min(max(y, kwargs["padding_top"]), kwargs["im_height"] - kwargs["padding_bottom"]))],
                                fill=kwargs["grid_colour"], width=kwargs["line_width"])

    @staticmethod
    def _draw_vline(**kwargs):
        """Draw a grid of vertical lines."""
        for x in range(0, kwargs["im_width"], kwargs["grid_size"]):
            kwargs["grid"].line([(min(max(x, kwargs["padding_left"]), kwargs["im_width"] - kwargs["padding_right"]),
                                  max(0, kwargs["padding_top"])),
                                (min(max(x, kwargs["padding_left"]), kwargs["im_width"] - kwargs["padding_right"]),
                                 kwargs["im_height"] - kwargs["padding_bottom"])],
                                fill=kwargs["grid_colour"], width=kwargs["line_width"])

    @staticmethod
    def _draw_hline(**kwargs):
        """Draw a grid of horizontal lines."""
        for y in range(0, kwargs["im_height"], kwargs["grid_size"]):
            kwargs["grid"].line([(max(0, kwargs["padding_left"]),
                                  min(max(y, kwargs["padding_top"]), kwargs["im_height"] - kwargs["padding_bottom"])),
                                 (kwargs["im_width"] - kwargs["padding_right"],
                                  min(max(y, kwargs["padding_top"]), kwargs["im_height"] - kwargs["padding_bottom"]))],
                                fill=kwargs["grid_colour"], width=kwargs["line_width"])

    @staticmethod
    def _draw_vhex(**kwargs):
        """Draw a grid of vertical hexagons."""
        # FIXME: hex edges are bolder when touching other hexes to their right.
        # grid_size is the height of the hex.
        # The apothem is the line from the centre of the hex to the centre of one of its sides.
        apothem = kwargs["grid_size"] / 2
        side = 2 * ((apothem * np.sqrt(3)) / 3)

        # Points are in clockwise order from top-left.
        hex_points = [(0, 0), (side, 0),
                      (side + apothem * 0.6, apothem), (side, 2 * apothem),
                      (0, 2 * apothem), (-(apothem * 0.6), apothem),
                      (0, 0)]  # The last point serves to join the last and first vertices together.

        for offs_y in np.arange(kwargs["padding_top"],
                                kwargs["im_height"] - kwargs["padding_bottom"],
                                apothem):
            for offs_x in np.arange(kwargs["padding_left"] + apothem * 0.6,
                                    kwargs["im_width"] - kwargs["padding_right"],
                                    3 * side):
                # offs_x is 3 times the side to give room for the hexes on the next row;
                # it starts from apothem*0.6 so that the leftmost vertex is at the edge of the image.

                # Add extra horizontal offset only on odd rows to leave room for the alternating rows.
                odd_row = side * 1.5 * ((offs_y / apothem) % 2)

                for p in range(len(hex_points)):
                    # Set the second point of the line to the next one.
                    # If we're at the last point set it to the first one to close the polygon.
                    next_p = p + 1 if p < len(hex_points)-1 else 0

                    x1 = hex_points[p][0] + offs_x + odd_row
                    y1 = hex_points[p][1] + offs_y

                    x2 = hex_points[next_p][0] + offs_x + odd_row
                    y2 = hex_points[next_p][1] + offs_y

                    # Don't draw the line if any of the two points lies outside the limits defined by the settings.
                    if all(x <= kwargs["im_width"] - kwargs["padding_right"] for x in (x1, x2))\
                            and all(y <= kwargs["im_height"] - kwargs["padding_bottom"] for y in (y1, y2)):
                        kwargs["grid"].line([x1, y1, x2, y2], fill=kwargs["grid_colour"], width=kwargs["line_width"])

    @staticmethod
    def _draw_hhex(**kwargs):
        """Draw a grid of horizontal hexagons."""
        # This is actually identical to the procedure for vertical hexes, but with x and y for points switched around.
        apothem = kwargs["grid_size"] / 2
        side = 2 * ((apothem * np.sqrt(3)) / 3)

        hex_points = [(0, 0), (side, 0),
                      (side + apothem * 0.6, apothem), (side, 2 * apothem),
                      (0, 2 * apothem), (-(apothem * 0.6), apothem),
                      (0, 0)]  # The last point serves to join the last and first vertices together.

        for offs_y in np.arange(kwargs["padding_top"],
                                kwargs["im_width"] - kwargs["padding_right"],
                                apothem):
            for offs_x in np.arange(kwargs["padding_left"] + apothem * 0.6,
                                    kwargs["im_height"] - kwargs["padding_bottom"],
                                    3 * side):

                odd_row = side * 1.5 * ((offs_y / apothem) % 2)

                for p in range(len(hex_points)):
                    # Set the second point of the line to the next one.
                    # If we're at the last point set it to the first one to close the polygon.
                    next_p = p + 1 if p < len(hex_points)-1 else 0

                    x1 = hex_points[p][1] + offs_y
                    y1 = hex_points[p][0] + offs_x + odd_row

                    x2 = hex_points[next_p][1] + offs_y
                    y2 = hex_points[next_p][0] + offs_x + odd_row

                    # Don't draw the line if any of the two points lies outside the limits defined by the settings.
                    if all(x <= kwargs["im_width"] - kwargs["padding_right"] for x in (x1, x2))\
                            and all(y <= kwargs["im_height"] - kwargs["padding_bottom"] for y in (y1, y2)):
                        kwargs["grid"].line([x1, y1, x2, y2], fill=kwargs["grid_colour"], width=kwargs["line_width"])
