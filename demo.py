#!/usr/bin/env python3
"""
Demo script for the Primary School Worksheet Generator
Generates sample worksheets to showcase capabilities
"""

import os
import sys
from datetime import datetime

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from worksheet_generator.core.math_generator import MathGenerator
from worksheet_generator.core.logic_generator import LogicGenerator
from worksheet_generator.core.reading_generator import ReadingGenerator
from worksheet_generator.output.pdf_generator import PDFGenerator


def run_demo():
    """Run a demonstration of the worksheet generator"""
    print("🎪 DEMO: Primary School Worksheet Generator")
    print("=" * 50)
    print("This demo will generate sample worksheets for each subject and age group")
    print()

    # Create output directory
    output_dir = "demo_worksheets"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"📁 Created demo directory: {output_dir}")

    # Initialize generators
    math_gen = MathGenerator()
    logic_gen = LogicGenerator()
    reading_gen = ReadingGenerator()
    pdf_gen = PDFGenerator()

    # Demo scenarios
    demos = [
        {
            "subject": "math",
            "age": "4-5",
            "questions": 10,
            "description": "Basic Math for Preschoolers",
        },
        {
            "subject": "logic",
            "age": "6-7",
            "questions": 15,
            "description": "Logic Puzzles for Early Elementary",
        },
        {
            "subject": "reading",
            "age": "8-10",
            "questions": 12,
            "description": "Reading Comprehension for Upper Elementary",
        },
        {
            "subject": "math",
            "age": "8-10",
            "questions": 20,
            "description": "Advanced Math with Word Problems",
        },
    ]

    print("🚀 Generating demo worksheets...")
    print("-" * 30)

    for i, demo in enumerate(demos, 1):
        print(f"📝 Demo {i}/4: {demo['description']}")
        print(
            f"   Subject: {demo['subject'].title()}, Age: {demo['age']}, Questions: {demo['questions']}"
        )

        try:
            # Generate problems based on subject
            if demo["subject"] == "math":
                problems = math_gen.generate_problems(demo["age"], demo["questions"])
            elif demo["subject"] == "logic":
                problems = logic_gen.generate_problems(demo["age"], demo["questions"])
            else:  # reading
                problems = reading_gen.generate_problems(demo["age"], demo["questions"])

            # Create filenames
            timestamp = datetime.now().strftime("%H%M%S")
            worksheet_filename = os.path.join(
                output_dir,
                f"demo_{i}_{demo['subject']}_{demo['age'].replace('-', '_')}_worksheet_{timestamp}.pdf",
            )
            answer_filename = os.path.join(
                output_dir,
                f"demo_{i}_{demo['subject']}_{demo['age'].replace('-', '_')}_answers_{timestamp}.pdf",
            )

            # Generate PDFs
            pdf_gen.generate_worksheet(
                demo["subject"],
                demo["age"],
                problems,
                worksheet_filename,
                f"Demo Student #{i}",
            )
            pdf_gen.generate_answer_key(
                demo["subject"], demo["age"], problems, answer_filename
            )

            print(f"   ✅ Worksheet: {os.path.basename(worksheet_filename)}")
            print(f"   ✅ Answer Key: {os.path.basename(answer_filename)}")

            # Show sample problems
            print(f"   📋 Sample problems:")
            for j, problem in enumerate(problems[:2], 1):
                question_text = problem["question"][:60] + (
                    "..." if len(problem["question"]) > 60 else ""
                )
                print(f"      {j}. {question_text}")

        except Exception as e:
            print(f"   ❌ Error: {str(e)}")

        print()

    print("🎉 Demo complete!")
    print(f"📁 Check the '{output_dir}' folder for generated worksheets")
    print()
    print("🎯 Application Features Demonstrated:")
    print("   • Math worksheets with varying difficulty levels")
    print("   • Logic puzzles and pattern recognition")
    print("   • Reading comprehension with age-appropriate content")
    print("   • Professional PDF formatting")
    print("   • Answer keys for easy checking")
    print()
    print("🚀 Ready to create your own worksheets!")
    print("   Run: python simple_cli.py (for basic interface)")
    print("   Run: python enhanced_cli.py (for advanced features)")
    print("   Run: python main.py (for GUI interface)")


if __name__ == "__main__":
    try:
        run_demo()
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
        print("Make sure all dependencies are installed and try again.")
