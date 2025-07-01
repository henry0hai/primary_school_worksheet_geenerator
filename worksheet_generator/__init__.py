"""
Primary School Worksheet Generator

A comprehensive Python package for generating educational worksheets for primary school students.
Supports math, logic, and reading exercises with visual elements and PDF output.
"""

__version__ = "1.0.0"
__author__ = "henry0hai "
__email__ = "henry0hai@gmail.com"

# Import main classes for easy access
from .core import MathGenerator, LogicGenerator, ReadingGenerator
from .output.pdf_generator import PDFGenerator


# Package-level convenience functions
def create_math_worksheet(
    age_group: str,
    num_questions: int = 20,
    student_name: str = "",
    output_file: str = None,
):
    """Create a math worksheet quickly"""
    from .core import MathGenerator
    from .output.pdf_generator import PDFGenerator

    generator = MathGenerator()
    pdf_gen = PDFGenerator()

    problems = generator.generate_problems(age_group=age_group, count=num_questions)

    if output_file is None:
        from datetime import datetime

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"math_worksheet_{timestamp}.pdf"

    return pdf_gen.generate_worksheet(
        subject="math",
        age_group=age_group,
        problems=problems,
        output_filename=output_file,
        student_name=student_name,
    )


def create_comprehensive_assessment(
    age_group: str,
    num_questions: int = 30,
    student_name: str = "",
    output_file: str = None,
):
    """Create a comprehensive assessment quickly"""
    # Import the function from cli.py since that's where it actually exists
    import sys
    import os

    project_root = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, project_root)

    from cli import generate_comprehensive_problems
    from .output.pdf_generator import PDFGenerator

    pdf_gen = PDFGenerator()

    problems = generate_comprehensive_problems(age_group, num_questions)

    if output_file is None:
        from datetime import datetime

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"comprehensive_assessment_{timestamp}.pdf"

    return pdf_gen.generate_worksheet(
        subject="comprehensive",
        age_group=age_group,
        problems=problems,
        output_filename=output_file,
        student_name=student_name,
    )


# Export main classes and functions
__all__ = [
    "MathGenerator",
    "LogicGenerator",
    "ReadingGenerator",
    "PDFGenerator",
    "create_math_worksheet",
    "create_comprehensive_assessment",
]
