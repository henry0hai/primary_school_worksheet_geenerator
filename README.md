# Primary School Worksheet Generator 🎓

A comprehensive Python package for generating educational worksheets for primary school students aged 4-10 years. Creates beautiful, age-appropriate PDF worksheets for Math, Logic, and Reading with visual elements and comprehensive assessments.

## Features ✨

- **🎯 Age-Appropriate Content**: Tailored for three age groups (4-5, 6-7, 8-10 years)
- **📚 Multiple Subjects**: Math, Logic, Reading, and Comprehensive Assessments
- **📄 Professional PDF Generation**: Beautiful worksheets with answer keys and visual patterns
- **🔄 Data-Driven**: All content loaded from JSON files for easy customization
- **🎨 Visual Elements**: Colored shapes, patterns, and symbols for engaging exercises
- **🏗️ Structured Distribution**: Age-based question type percentages for optimal learning
- **🔒 Uniqueness Guarantee**: No duplicate questions within worksheets
- **🧪 Comprehensive Testing**: Full test suite with master test runner
- **📦 Package Structure**: Proper Python package with organized modules

### Subject Coverage

- **📊 Math**: Addition, subtraction, multiplication, division, word problems
- **🧩 Logic**: Patterns, classification, reasoning, visual problem-solving
- **📖 Reading**: Vocabulary, sentence building, story comprehension
- **🎓 Comprehensive**: Mixed-subject assessments for complete evaluation

## What's New in v1.0.0 🆕

- ✅ **Comprehensive Assessment Mode**: Mixed-subject final exams
- ✅ **Visual Pattern Generation**: Actual colored shapes in PDFs
- ✅ **Structured Package Architecture**: Professional Python package structure
- ✅ **Master Test Suite**: Organized testing with categorized test runner
- ✅ **Enhanced PDF Generation**: Consistent visual patterns in worksheets and answer keys
- ✅ **Data-Driven Architecture**: All content externalized to JSON files
- ✅ **Improved CLI**: Support for comprehensive assessments and larger question counts
- ✅ **Symbol Consistency**: Proper emoji/symbol conversion throughout PDFs

## Educational Goals 🎯

### Mathematics
- Master basic arithmetic operations with age-appropriate number ranges
- Develop problem-solving skills through contextual word problems
- Build number sense and mathematical reasoning
- Prepare for advanced mathematical concepts

### Logic & Reasoning  
- Enhance pattern recognition and analytical thinking
- Develop classification and categorization skills
- Build deductive and inductive reasoning abilities
- Foster critical thinking through structured problem-solving

### Reading Comprehension
- Improve reading fluency and comprehension
- Build vocabulary through contextual exercises
- Develop inference and analytical reading skills
- Enhance sentence construction and language skills

## Quick Start 🚀

### Installation
```bash
# Clone the repository
git clone https://github.com/henry0hai/primary_school_worksheet_generator.git

cd primary_school_worksheet_generator

# Install dependencies
pip install -r requirements.txt
```

### Option 1: Command Line Interface
```bash
# Interactive CLI
python cli.py
```

### Option 2: Demo Mode (See all features)
```bash
python demo.py                    # Basic demo
```

## Testing 🧪

### Run All Tests
```bash
# Run complete test suite
python run_all_tests.py

# Run specific test categories
python run_all_tests.py --category core
python run_all_tests.py --category comprehensive

# Quick tests (skip slow tests)
python run_all_tests.py --quick

# Verbose output with error details
python run_all_tests.py --verbose
```

### Test Categories
- **Core**: Basic functionality, uniqueness, distribution
- **Comprehensive**: Comprehensive assessment features  
- **Visual**: Pattern generation and visual consistency
- **PDF Generation**: PDF formatting and symbol conversion
- **Integration**: Full end-to-end testing
- Build vocabulary
- Enhance analytical thinking through story-based questions

## Installation

1. **Clone or download this repository**
2. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate     # On Windows
   ```

3. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Simple CLI (Recommended)

Run the simple command-line interface:

```bash
python cli.py
```

Features:
- Interactive prompts for easy use
- Choose subject type (Math, Logic, Reading)
- Select age group (4-5, 6-7, 8-10)
- Automatic PDF generation with answer keys

### Demo Mode

See all features and generate sample worksheets:

```bash
python demo.py
```

Features:
- Generates 4 sample worksheets (different subjects and ages)
- Shows the full capability of the application
- Perfect for testing and demonstration

### Testing

Verify all components are working correctly:
```bash
python run_all_tests.py
```

This runs a comprehensive test suite that validates all generators and PDF creation.

### Quick Start - Sample Worksheets

To quickly see what the application can do, run:
```bash
python demo.py
```

This will create sample worksheets for all age groups in the `generated_worksheets/` folder.

## Question Types by Age Group

### Ages 4-6 (Early Learners)
- **Math**: Simple addition/subtraction (1-10), visual counting
- **Logic**: Basic patterns, color/shape sorting, simple matching
- **Reading**: Single sentence stories, character identification

### Ages 6-8 (Elementary)
- **Math**: Two-digit arithmetic, basic multiplication/division, simple word problems
- **Logic**: Sequence completion, classification, comparisons
- **Reading**: Short paragraphs, main idea questions, detail recall

### Ages 8-10 (Intermediate)
- **Math**: Multi-step problems, complex word problems, number patterns
- **Logic**: Deduction puzzles, riddles, logical reasoning
- **Reading**: Longer stories, theme identification, character analysis, predictions

## Customization

### Adding New Question Types

1. **Math Questions**: Add new methods to `MathGenerator` class in `generators/math_generator.py`
2. **Logic Questions**: Extend `LogicGenerator` class with new puzzle types in `generators/logic_generator.py`
3. **Reading Questions**: Create new story templates and question types in `generators/reading_generator.py`

### Modifying PDF Layout

Edit the `PDFGenerator` class in `pdf_generator_new.py` to:
- Change fonts, colors, and styling
- Modify page layout and spacing
- Add images or decorative elements
- Customize header and footer content

*Note: This project uses a simplified CLI interface. No GUI dependencies like tkinter are required.*

## Educational Benefits

This application helps children develop:

1. **Mathematical Skills**:
   - Number recognition and counting
   - Basic arithmetic operations
   - Problem-solving strategies
   - Pattern recognition

2. **Logical Thinking**:
   - Critical thinking skills
   - Deductive reasoning
   - Pattern analysis
   - Classification abilities

3. **Reading Comprehension**:
   - Vocabulary building
   - Story understanding
   - Detail retention
   - Analytical thinking

## Project Structure 📁

```
primary_school_worksheet_geenerator/
├── worksheet_generator/         # Main package
│   ├── __init__.py              # Package exports and convenience functions
│   ├── core/                    # Core functionality
│   │   ├── logic_generator.py   # Logic generators
│   │   ├── math_generator.py    # Math generators
│   │   ├── reading_generator.py # Reading generators
│   ├── output/                  # Output generation
|   |   └── data_loader.py       # Data loading utilities
│   ├── output/                  # Output generation
│   │   └── pdf_generator.py     # PDF generation with visual patterns
│   ├── utils/                   # Utilities and CLI
│   │   └── cli.py               # Command-line interface
│   └── data/                    # Data files
│       └── [JSON data files]
├── data_source/                 # External data sources
│   ├── math_source/             # Math problem templates
│   ├── logic_source/            # Logic problem templates
│   └── reading_source/          # Reading comprehension content
├── tests/                       # Test files (moved here for organization)
├── docs/                        # Documentation
│   ├── PROJECT_SUMMARY.md       # Detailed project summary
│   └── QUICK_START.md           # Quick start guide
├── cli.py                       # Main CLI entry point
├── run_all_tests.py             # Master test runner
├── demo.py                      # Basic demo
├── demo_comprehensive.py        # Comprehensive assessment demo
├── requirements.txt             # Python dependencies
└── README.md                    # This file

```

## Architecture Overview 🏗️

### Core Components
- **Generators**: Subject-specific problem generators with age-based distributions
- **Data Loader**: Centralized loading of content from JSON files
- **PDF Generator**: Professional PDF creation with visual pattern support
- **CLI Interface**: User-friendly command-line interaction

### Key Features
- **Data-Driven**: All content externalized to JSON for easy modification
- **Visual Elements**: Support for colored shapes and patterns in PDFs
- **Comprehensive Testing**: Organized test suite with master runner
- **Package Structure**: Professional Python package organization

## Tips for Educators and Parents

1. **Start with the demo mode** (`python demo.py`) to see all capabilities
2. **Use the simple CLI** (`python cli.py`) for interactive worksheet generation
3. **Focus on effort over correctness** to build confidence
4. **Create multiple versions** using the demo mode for repeated practice
5. **Encourage children to explain their thinking** process
6. **Take breaks** between different question types to maintain engagement

## Examples files

- SEE `generated_worksheets` folder for sample worksheets generated by the application.

## Future Enhancements

Potential improvements could include:
- Integration with AI services for dynamic content generation
- Image-based questions and visual puzzles
- Interactive online version
- Progress tracking and analytics
- Multilingual support
- Adaptive difficulty based on performance
- Enhanced GUI interface

## Contributing

Feel free to suggest improvements or report issues. Some areas for contribution:
- Additional question types
- New story templates for reading comprehension
- Enhanced PDF layouts
- Localization and translations

## License

This project is created for educational purposes. Feel free to use and modify for non-commercial educational activities.

---

**Happy Learning!** 📚✏️🎓
