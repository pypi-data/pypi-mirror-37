# Gridder
Gridder can generate grids in image form according to the specified settings, either as
brand-new images or drawing on existing ones. Grids can have various shapes, such as square
or hexagonal, and are highly configurable.

Suggestions and appreciation are welcome! Feel free to email me or open an issue on Gitlab.

## Usage
Gridder can draw either on an empty background or on an existing image.

To use an **empty background**, run `gridder.py <width> <height> <grid size>`, where:
- `<width>` is the width of the image in pixels.
- `<height>` is the height of the image in pixels.
- `<grid size>` is the interval, in pixels, at which each line of the 
grid will be generated. This effectively corresponds to the side of each
square of the grid.

To draw on an **existing image**, run `gridder.py --file <file path> <grid size>`, where:
- `<file path>` is the path to the image on which Gridder will paint a grid.
- `<grid size>` is as described above.

Note that the `--file` (or `-f`) option **must be the first argument** if specified.

The result of the above will be a file named `grid.png` in the same
directory. If used, the existing image will not be modified.

### Options
The following optional arguments (or their aliases) can be provided:
- `--gridtype`, alias: `-gt` specifies the shape of the grid. Possible options:
    - `square` squares (default),
    - `vhex` vertical hexes (flat side on top and bottom),
    - `hhex` horizontal hexes (flat side on left and right),
    - `vline` vertical lines,
    - `hline` horizontal lines.
- `--linewidth`, alias: `-lw` specifies the line width of the elements of the grid. Default: 1.
- `--gridcol <colour>`, alias: `-grc` specifies a <colour> for the grid, as the name of
a colour or a string format recognised by Pillow, such as hex values like `#000000`.
- `--bgcol <colour>`, alias: `-bgc` specifies a <colour> for the background, as the name of
a colour or a string format recognised by Pillow, such as hex values like `#000000`.
For a transparent background, omit this argument or specify `transparent`.
**NOTE:** This cannot be used when drawing on an existing image using `-f`.
- `--padding <size>`, alias `-p` specifies a padding of <size> pixels around the grid, 
i.e. a padding between the borders of the image and the actual grid.
- `--paddingtop <size>`, ..`right`, ..`bottom`, ..`left`, alias: `-pt`, `-pr`, `-pb`, `-pl` specify each 
a padding of <size> specific to the indicated side. Each can be used separately, and they will take
priority over the generic `--padding` option above.
- `--destination`, alias `-d` specifies the file name of the finished image. Do not include
extension, as it will always be .png automatically. The default file name is `grid.png`.

### Units
By default, all size arguments, `<width>`, `<height>`, `<grid size>` and all applicable
optional parameters use **pixels**, but other units are also allowed, namely:
- `cm`,
- `mm`,
- `in`.

These units all assume a resolution on `300dpi` as customary for printing.

For example, a grid created by running `gridder.py 12cm 12cm 1in` will be
1417x1417 pixels and have 300-pixels wide squares.

## Known issues
- Due to rounding errors, hex grids may have some unwanted bold edges.
