#!/usr/bin/env python3
"""
CSS Color Analyzer

A tool to analyze colors in CSS and TSX files, tracking their usage,
variations, file locations, and organizing them by category.
"""

import os
import sys
import json
import re
import argparse
import time
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Set, Any, Optional
import colorsys

# Regular expressions for different color formats
HEX_COLOR_REGEX = r'#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b'
RGB_COLOR_REGEX = r'rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)'
RGBA_COLOR_REGEX = r'rgba\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(0?\.\d+|1(\.0)?|0)\s*\)'
HSL_COLOR_REGEX = r'hsl\(\s*(\d+)\s*,\s*(\d+)%\s*,\s*(\d+)%\s*\)'
HSLA_COLOR_REGEX = r'hsla\(\s*(\d+)\s*,\s*(\d+)%\s*,\s*(\d+)%\s*,\s*(0?\.\d+|1(\.0)?|0)\s*\)'

# CSS named colors with their hex equivalents
NAMED_COLORS = {
    'aliceblue': '#f0f8ff', 'antiquewhite': '#faebd7', 'aqua': '#00ffff', 'aquamarine': '#7fffd4',
    'azure': '#f0ffff', 'beige': '#f5f5dc', 'bisque': '#ffe4c4', 'black': '#000000',
    'blanchedalmond': '#ffebcd', 'blue': '#0000ff', 'blueviolet': '#8a2be2', 'brown': '#a52a2a',
    'burlywood': '#deb887', 'cadetblue': '#5f9ea0', 'chartreuse': '#7fff00', 'chocolate': '#d2691e',
    'coral': '#ff7f50', 'cornflowerblue': '#6495ed', 'cornsilk': '#fff8dc', 'crimson': '#dc143c',
    'cyan': '#00ffff', 'darkblue': '#00008b', 'darkcyan': '#008b8b', 'darkgoldenrod': '#b8860b',
    'darkgray': '#a9a9a9', 'darkgreen': '#006400', 'darkgrey': '#a9a9a9', 'darkkhaki': '#bdb76b',
    'darkmagenta': '#8b008b', 'darkolivegreen': '#556b2f', 'darkorange': '#ff8c00',
    'darkorchid': '#9932cc', 'darkred': '#8b0000', 'darksalmon': '#e9967a', 'darkseagreen': '#8fbc8f',
    'darkslateblue': '#483d8b', 'darkslategray': '#2f4f4f', 'darkslategrey': '#2f4f4f',
    'darkturquoise': '#00ced1', 'darkviolet': '#9400d3', 'deeppink': '#ff1493',
    'deepskyblue': '#00bfff', 'dimgray': '#696969', 'dimgrey': '#696969', 'dodgerblue': '#1e90ff',
    'firebrick': '#b22222', 'floralwhite': '#fffaf0', 'forestgreen': '#228b22', 'fuchsia': '#ff00ff',
    'gainsboro': '#dcdcdc', 'ghostwhite': '#f8f8ff', 'gold': '#ffd700', 'goldenrod': '#daa520',
    'gray': '#808080', 'green': '#008000', 'greenyellow': '#adff2f', 'grey': '#808080',
    'honeydew': '#f0fff0', 'hotpink': '#ff69b4', 'indianred': '#cd5c5c', 'indigo': '#4b0082',
    'ivory': '#fffff0', 'khaki': '#f0e68c', 'lavender': '#e6e6fa', 'lavenderblush': '#fff0f5',
    'lawngreen': '#7cfc00', 'lemonchiffon': '#fffacd', 'lightblue': '#add8e6', 'lightcoral': '#f08080',
    'lightcyan': '#e0ffff', 'lightgoldenrodyellow': '#fafad2', 'lightgray': '#d3d3d3',
    'lightgreen': '#90ee90', 'lightgrey': '#d3d3d3', 'lightpink': '#ffb6c1', 'lightsalmon': '#ffa07a',
    'lightseagreen': '#20b2aa', 'lightskyblue': '#87cefa', 'lightslategray': '#778899',
    'lightslategrey': '#778899', 'lightsteelblue': '#b0c4de', 'lightyellow': '#ffffe0',
    'lime': '#00ff00', 'limegreen': '#32cd32', 'linen': '#faf0e6', 'magenta': '#ff00ff',
    'maroon': '#800000', 'mediumaquamarine': '#66cdaa', 'mediumblue': '#0000cd',
    'mediumorchid': '#ba55d3', 'mediumpurple': '#9370db', 'mediumseagreen': '#3cb371',
    'mediumslateblue': '#7b68ee', 'mediumspringgreen': '#00fa9a', 'mediumturquoise': '#48d1cc',
    'mediumvioletred': '#c71585', 'midnightblue': '#191970', 'mintcream': '#f5fffa',
    'mistyrose': '#ffe4e1', 'moccasin': '#ffe4b5', 'navajowhite': '#ffdead', 'navy': '#000080',
    'oldlace': '#fdf5e6', 'olive': '#808000', 'olivedrab': '#6b8e23', 'orange': '#ffa500',
    'orangered': '#ff4500', 'orchid': '#da70d6', 'palegoldenrod': '#eee8aa', 'palegreen': '#98fb98',
    'paleturquoise': '#afeeee', 'palevioletred': '#db7093', 'papayawhip': '#ffefd5',
    'peachpuff': '#ffdab9', 'peru': '#cd853f', 'pink': '#ffc0cb', 'plum': '#dda0dd',
    'powderblue': '#b0e0e6', 'purple': '#800080', 'rebeccapurple': '#663399', 'red': '#ff0000',
    'rosybrown': '#bc8f8f', 'royalblue': '#4169e1', 'saddlebrown': '#8b4513', 'salmon': '#fa8072',
    'sandybrown': '#f4a460', 'seagreen': '#2e8b57', 'seashell': '#fff5ee', 'sienna': '#a0522d',
    'silver': '#c0c0c0', 'skyblue': '#87ceeb', 'slateblue': '#6a5acd', 'slategray': '#708090',
    'slategrey': '#708090', 'snow': '#fffafa', 'springgreen': '#00ff7f', 'steelblue': '#4682b4',
    'tan': '#d2b48c', 'teal': '#008080', 'thistle': '#d8bfd8', 'tomato': '#ff6347',
    'turquoise': '#40e0d0', 'violet': '#ee82ee', 'wheat': '#f5deb3', 'white': '#ffffff',
    'whitesmoke': '#f5f5f5', 'yellow': '#ffff00', 'yellowgreen': '#9acd32'
}

NAMED_COLOR_REGEX = '|'.join(r'\b' + color + r'\b' for color in NAMED_COLORS.keys())


def normalize_hex_color(hex_color: str) -> str:
    """
    Normalize hex color to lowercase 6 digit format.

    Examples:
    - #fff -> #ffffff
    - #CCC -> #cccccc
    - #AbC -> #aabbcc
    """
    hex_color = hex_color.lower()
    if len(hex_color) == 4:  # Convert 3-digit hex to 6-digit
        return '#' + ''.join(c + c for c in hex_color[1:])
    return hex_color


def hex_to_rgb(hex_color: str) -> tuple:
    """Convert hex color to RGB tuple."""
    hex_color = normalize_hex_color(hex_color)[1:]  # Remove the #
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hsl(r: int, g: int, b: int) -> tuple:
    """Convert RGB to HSL."""
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return (int(h * 360), int(s * 100), int(l * 100))


def determine_color_category(hex_color: str) -> str:
    """
    Determine the color category based on the hex color.
    Categories: red, orange, yellow, green, teal, blue, purple, pink, gray, brown, black, white
    """
    rgb = hex_to_rgb(hex_color)
    hsl = rgb_to_hsl(*rgb)

    h, s, l = hsl

    # Handle grayscale colors
    if s < 10:
        if l < 10:
            return "black"
        elif l > 90:
            return "white"
        else:
            return "gray"

    # Determine hue-based category
    if h < 15 or h >= 345:
        return "red"
    elif h < 45:
        return "orange"
    elif h < 75:
        return "yellow"
    elif h < 165:
        return "green"
    elif h < 195:
        return "teal"
    elif h < 255:
        return "blue"
    elif h < 315:
        return "purple"
    else:
        return "pink"


def format_of_color(color: str) -> str:
    """Determine the format of a color string."""
    if color.startswith('#'):
        return 'hex'
    elif color.startswith('rgb('):
        return 'rgb'
    elif color.startswith('rgba('):
        return 'rgba'
    elif color.startswith('hsl('):
        return 'hsl'
    elif color.startswith('hsla('):
        return 'hsla'
    else:
        return 'named'


def extract_colors_from_content(content: str) -> Dict[str, List[str]]:
    """Extract all colors from content and return them organized by normalized value."""
    color_matches = {}

    # Extract hex colors
    for match in re.finditer(HEX_COLOR_REGEX, content):
        color = match.group(0).lower()
        normalized = normalize_hex_color(color)

        if normalized not in color_matches:
            color_matches[normalized] = []

        if color not in color_matches[normalized]:
            color_matches[normalized].append(color)

    # Extract RGB colors
    for match in re.finditer(RGB_COLOR_REGEX, content):
        color = match.group(0)
        r, g, b = map(int, match.groups())
        hex_value = f'#{r:02x}{g:02x}{b:02x}'

        if hex_value not in color_matches:
            color_matches[hex_value] = []

        if color not in color_matches[hex_value]:
            color_matches[hex_value].append(color)

    # Extract RGBA colors
    for match in re.finditer(RGBA_COLOR_REGEX, content):
        color = match.group(0)
        r, g, b, a = match.groups()
        hex_value = f'#{int(r):02x}{int(g):02x}{int(b):02x}'

        if hex_value not in color_matches:
            color_matches[hex_value] = []

        if color not in color_matches[hex_value]:
            color_matches[hex_value].append(color)

    # Extract HSL colors
    for match in re.finditer(HSL_COLOR_REGEX, content):
        color = match.group(0)
        h, s, l = map(int, match.groups())
        h = h / 360.0
        s = s / 100.0
        l = l / 100.0

        r, g, b = colorsys.hls_to_rgb(h, l, s)
        r, g, b = int(r * 255), int(g * 255), int(b * 255)
        hex_value = f'#{r:02x}{g:02x}{b:02x}'

        if hex_value not in color_matches:
            color_matches[hex_value] = []

        if color not in color_matches[hex_value]:
            color_matches[hex_value].append(color)

    # Extract HSLA colors
    for match in re.finditer(HSLA_COLOR_REGEX, content):
        color = match.group(0)
        h, s, l, a = match.groups()
        h = int(h) / 360.0
        s = int(s) / 100.0
        l = int(l) / 100.0

        r, g, b = colorsys.hls_to_rgb(h, l, s)
        r, g, b = int(r * 255), int(g * 255), int(b * 255)
        hex_value = f'#{r:02x}{g:02x}{b:02x}'

        if hex_value not in color_matches:
            color_matches[hex_value] = []

        if color not in color_matches[hex_value]:
            color_matches[hex_value].append(color)

    # Extract named colors
    for match in re.finditer(NAMED_COLOR_REGEX, content, re.IGNORECASE):
        color = match.group(0).lower()
        hex_value = NAMED_COLORS.get(color)

        if hex_value not in color_matches:
            color_matches[hex_value] = []

        if color not in color_matches[hex_value]:
            color_matches[hex_value].append(color)

    return color_matches


def analyze_file(file_path: Path) -> Dict[str, List[str]]:
    """Analyze a single file and extract colors."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return extract_colors_from_content(content)
    except Exception as e:
        print(f"Error analyzing {file_path}: {e}", file=sys.stderr)
        return {}


def find_files(path: Path, extensions: Set[str]) -> List[Path]:
    """Find all files with given extensions in a directory tree."""
    if path.is_file():
        return [path] if path.suffix.lower() in extensions else []

    files = []
    for root, _, filenames in os.walk(path):
        for filename in filenames:
            file_path = Path(root) / filename
            if file_path.suffix.lower() in extensions:
                files.append(file_path)
    return files


def process_files(files: List[Path]) -> Dict[str, Any]:
    """Process a list of files and aggregate color data."""
    color_data = {}

    for file_path in files:
        file_colors = analyze_file(file_path)
        file_str = str(file_path)

        for normalized_value, variations in file_colors.items():
            if normalized_value not in color_data:
                color_format = format_of_color(variations[0])
                category = determine_color_category(normalized_value)

                color_data[normalized_value] = {
                    'name': normalized_value,
                    'count': 1,
                    'variations': variations,
                    'unique': True,
                    'color_format': color_format,
                    'category': category,
                    'locations': [file_str]
                }
            else:
                color_data[normalized_value]['count'] += 1
                for variation in variations:
                    if variation not in color_data[normalized_value]['variations']:
                        color_data[normalized_value]['variations'].append(variation)
                if file_str not in color_data[normalized_value]['locations']:
                    color_data[normalized_value]['locations'].append(file_str)
                color_data[normalized_value]['unique'] = False

    # Organize colors by category
    organized_data = {}
    for color_hex, color_info in color_data.items():
        category = color_info['category']
        if category not in organized_data:
            organized_data[category] = []
        organized_data[category].append(color_info)

    return organized_data


def generate_color_report(color_data: Dict[str, Any], pretty: bool = False) -> str:
    """Generate a JSON report of color data."""
    indent = 2 if pretty else None
    return json.dumps(color_data, indent=indent)


def watch_files(files: List[Path], output_path: Optional[str], pretty: bool = False):
    """Watch files for changes and update the analysis."""
    last_modification_times = {}

    for file_path in files:
        try:
            last_modification_times[file_path] = os.path.getmtime(file_path)
        except Exception:
            last_modification_times[file_path] = 0

    while True:
        files_changed = False

        for file_path in files:
            try:
                mtime = os.path.getmtime(file_path)
                if mtime > last_modification_times.get(file_path, 0):
                    files_changed = True
                    last_modification_times[file_path] = mtime
            except Exception:
                pass

        if files_changed:
            color_data = process_files(files)
            report = generate_color_report(color_data, pretty)

            if output_path:
                with open(output_path, 'w', encoding='utf-8') as out_file:
                    out_file.write(report)
                print(f"Updated color analysis to {output_path}")
            else:
                print(report)

        time.sleep(1)


def main():
    """Main function to run the tool."""
    parser = argparse.ArgumentParser(
        description='CSS Color Analyzer - Extract and analyze colors from CSS and TSX files.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  Analyze a single file:
    python color_analyzer.py -i style.css

  Analyze a directory:
    python color_analyzer.py -d src/styles

  Watch a directory for changes:
    python color_analyzer.py -d src/styles --watch

  Save the analysis to a file:
    python color_analyzer.py -d src/styles -o colors.json

  Format the output in a readable way:
    python color_analyzer.py -d src/styles --pretty

  Generate a report with file locations:
    python color_analyzer.py -d src/styles --pretty (file locations are included by default)
        '''
    )

    parser.add_argument('-i', '--input', type=str, help='Input file to analyze')
    parser.add_argument('-d', '--dir', type=str, help='Directory to analyze recursively')
    parser.add_argument('-o', '--output', type=str, help='Output file to save the analysis (default: stdout)')
    parser.add_argument('--pretty', action='store_true', help='Format the JSON output to be more readable')
    parser.add_argument('--watch', action='store_true', help='Watch files for changes and update analysis')

    args = parser.parse_args()

    if not args.input and not args.dir:
        parser.print_help()
        sys.exit(1)

    file_extensions = {'.css', '.scss', '.less', '.styl', '.tsx', '.jsx', '.js', '.ts'}
    files = []

    if args.input:
        input_path = Path(args.input)
        if input_path.is_file():
            files = [input_path]
        else:
            print(f"Error: {args.input} is not a file", file=sys.stderr)
            sys.exit(1)

    if args.dir:
        dir_path = Path(args.dir)
        if dir_path.is_dir():
            files.extend(find_files(dir_path, file_extensions))
        else:
            print(f"Error: {args.dir} is not a directory", file=sys.stderr)
            sys.exit(1)

    if not files:
        print("No files found to analyze", file=sys.stderr)
        sys.exit(1)

    if args.watch:
        print(f"Watching {len(files)} files for changes...")
        watch_files(files, args.output, args.pretty)
    else:
        color_data = process_files(files)
        report = generate_color_report(color_data, args.pretty)

        if args.output:
            with open(args.output, 'w', encoding='utf-8') as out_file:
                out_file.write(report)
            print(f"Color analysis saved to {args.output}")
        else:
            print(report)


if __name__ == '__main__':
    main()
