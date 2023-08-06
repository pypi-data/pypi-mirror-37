# 1.0.3
- Converter now accepts values that are already in numeric form.
- Converter now accepts values that would result in an empty string, defaulting
to 0.
- Drawer now accepts calls with missing arguments, provided these are optional.
- Drawer now defaults to a 1x1 image when provided with malformed arguments.

# 1.0.2
- Bug fixes.

# 1.0.1
- Added support for --linewidth.
- Major bug fixes pertaining hex grids.

# 1.0.0
- Added support for individual padding sides settings.

# 0.3.1
- Major code refactoring.

# 0.3.0
- Added support for custom destination file name.
- Removed --version command.

# 0.2.4
- Added support for alternative units (cm, mm, in).

# 0.2.3
- Added support for padding around the grid, --padding (-p).

# 0.2.2
- Added support for vertical and horizontal hexagons.
- Added support for vertical and horizontal lines.
- Added --gridtype (-gt) option.

# 0.2.1
- Explicitly entering "transparent" as background colour is now allowed.

# 0.2.0
- Added support for painting on an existing image.
- Width, height and background colour selection are now only allowed if not using an existing file.
- --help is now unavailable due to inconsistencies. Will maybe fix in the future by manually rewriting it.

# 0.1.0
- Added support for selecting grid and background colour.
- Restructured code.
