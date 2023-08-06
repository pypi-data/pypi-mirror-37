"""Gridder is a program to generate an image containing a grid according to provided settings.
    Copyright (C) 2018  Federico Salerno <itashadd+gridder[at]gmail.com>

    Converter from various units to pixels.


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
from typing import Union


class Converter:
    """Converter class for unit to pixels conversion. Call Converter.to_px() to use."""
    __slots__ = []

    @staticmethod
    def to_px(raw_measure: str) -> int:
        """Detect the unit of the given measure and convert to pixels.

        :param raw_measure: the measure to convert, as a string ending with the symbol of the unit.

        :return: the measure in pixels as an integer.
        """

        # The dictionary of converters will update automatically as converter methods are added to Converter.
        converter = {re.split(r"_", k)[1]: v.__func__  # Select the unit symbol/name as key and the callable as value.
                     for k, v in Converter.__dict__.items()
                     if isinstance(v, staticmethod) and re.fullmatch(r"_[^_]+_to_px", k)}

        raw_measure = str(raw_measure)

        # Extract the amount to convert and the unit (if present) from the measure.
        # Empty string is appended in case no unit is specified.
        measure = list(re.split(r"(\D+)$", raw_measure, maxsplit=1)) + [""]

        if measure[0] == "":
            measure[0] = "0"
        # noinspection PyTypeChecker
        measure[0] = float(measure[0])

        # Use the unit to select the appropriate converter.
        # If no unit or the pixel unit are specified, just convert to int.
        return converter.setdefault(measure[1].strip(), int)(measure[0])

    @staticmethod
    def _cm_to_px(cm: Union[float, int]) -> int:
        """Convert an amount of centimetres to pixels at 300dpi resolution.

        :param cm: centimetres to convert from.
        :return: the converted measure in pixels as an integer
        """

        return round(118.11023622 * cm)

    @staticmethod
    def _mm_to_px(mm: Union[float, int]) -> int:
        """Convert an amount of millimetres to pixels at 300dpi resolution.

        :param mm: millimetres to convert from.
        :return: the converted measure in pixels as an integer
        """

        return round(11.811023622 * mm)

    @staticmethod
    def _in_to_px(inc: Union[float, int]) -> int:
        """Convert an amount of inches to pixels at 300dpi resolution.

        :param inc: inches to convert from.
        :return: the converted measure in pixels as an integer
        """

        return int(300 * inc)
