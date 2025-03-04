# CSS Color Analyzer

A powerful Python tool for analyzing colors in your web development codebase. This tool helps you identify, categorize, and organize colors across CSS, SCSS, JavaScript, TypeScript, and React component files.

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

- 🎨 **Complete Color Detection**: Finds colors in hex, RGB, RGBA, HSL, HSLA, and named formats
- 🔄 **Normalization**: Automatically normalizes different representations of the same color
- 📊 **Usage Statistics**: Counts occurrences and variations of each color
- 📁 **Location Tracking**: Lists all files where each color appears
- 🏷️ **Categorization**: Organizes colors by type (red, blue, green, etc.)
- 👀 **Watch Mode**: Continuously monitors for changes in your files
- 🔍 **Variations Detection**: Identifies all syntax variations of the same color

## 📋 Installation

### Option 1: Install via pip (recommended)

```bash
# Clone the repository
git clone https://github.com/inaki/css-color-analyzer.git
cd css-color-analyzer

# Install the package
pip install .

# For development mode (if you want to modify the code)
pip install -e .
```

### Option 2: Manual installation

```bash
# Clone the repository
git clone https://github.com/inaki/css-color-analyzer.git
cd css-color-analyzer

# Make the script executable
chmod +x css_color_analyzer/analyzer.py

# Create a symlink (Linux/macOS)
ln -s $(pwd)/css_color_analyzer/analyzer.py /usr/local/bin/css-color-analyzer
# OR add to your user bin directory
ln -s $(pwd)/css_color_analyzer/analyzer.py ~/.local/bin/css-color-analyzer
```

## 🚀 Usage

### Basic Commands

```bash
# Analyze a single file
css-color-analyzer --input path/to/file.css

# Analyze a directory (recursively)
css-color-analyzer --dir src/styles

# Save analysis to a file
css-color-analyzer --dir src/styles --output colors.json

# Format the output to be more readable
css-color-analyzer --dir src/styles --pretty

# Watch for changes
css-color-analyzer --dir src/styles --watch
```

### Command-line Options

| Option | Shorthand | Description |
|--------|-----------|-------------|
| `--input FILE` | `-i FILE` | Input file to analyze |
| `--dir DIR` | `-d DIR` | Directory to analyze recursively |
| `--output FILE` | `-o FILE` | Save output to specified file |
| `--pretty` | | Format JSON output to be more readable |
| `--watch` | | Watch files for changes and update analysis |
| `--help` | | Show help message |

## 📊 Example Output

```json
{
  "blue": [
    {
      "name": "#0a40ff",
      "count": 5,
      "variations": [
        "#0A40FF", 
        "rgb(10, 64, 255)"
      ],
      "unique": false,
      "color_format": "hex",
      "category": "blue",
      "locations": [
        "src/theme.ts",
        "src/components/Button.tsx",
        "src/styles/colors.css"
      ]
    },
    {
      "name": "#4682b4",
      "count": 2,
      "variations": [
        "steelblue",
        "#4682B4"
      ],
      "unique": false,
      "color_format": "named",
      "category": "blue",
      "locations": [
        "src/components/Header.tsx",
        "src/styles/theme.css"
      ]
    }
  ],
  "red": [
    {
      "name": "#ca4141",
      "count": 2,
      "variations": [
        "#CA4141",
        "rgb(202, 65, 65)"
      ],
      "unique": false,
      "color_format": "hex",
      "category": "red",
      "locations": [
        "src/theme.ts",
        "src/components/Alert.tsx"
      ]
    }
  ]
}
```

## 🛠️ Supported File Types

- CSS: `.css`
- CSS Preprocessors: `.scss`, `.less`, `.styl`
- JavaScript/TypeScript: `.js`, `.ts`
- React Components: `.jsx`, `.tsx`

## 💻 Practical Use Cases

1. **Creating a Design System**: Identify all colors to build a cohesive color palette
2. **Code Refactoring**: Find duplicate or similar colors that should be consolidated
3. **Maintaining Consistency**: Ensure the same colors are used throughout your project
4. **Documentation**: Generate color documentation for your design system
5. **CSS Optimization**: Identify rarely used colors that could be removed

## 🧠 How It Works

1. The tool recursively scans your specified files
2. It extracts all color values using regular expressions
3. Colors are normalized to a standard format for accurate counting
4. Each color is categorized based on its hue, saturation, and lightness
5. File locations are tracked for each color occurrence
6. Results are organized by category and output as JSON

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📬 Contact

Iñaki - [@iaranzadi](https://twitter.com/iaranzadi) - 

Project Link: [https://github.com/inaki/css-color-analyzer](https://github.com/inaki/css-color-analyzer)