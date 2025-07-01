#!/usr/bin/env python3
"""
Test script to generate a PDF with visual patterns to verify shape rendering
"""

import sys
import os

# Add the project root to the path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from worksheet_generator.core import LogicGenerator
from worksheet_generator.output import PDFGenerator


def test_visual_pattern_generation():
    """Generate a worksheet with visual patterns to test shape rendering"""

    print("🧪 Testing Visual Pattern Generation")
    print("=" * 50)

    # Create generators
    logic_generator = LogicGenerator()
    pdf_generator = PDFGenerator()

    # Generate multiple logic problems to get variety
    problems = []
    max_attempts = 20
    attempt = 0

    while len(problems) < 15 and attempt < max_attempts:
        logic_generator.reset_generated_questions()
        problem = logic_generator.generate_pattern_sequence("4-5")

        # Add problem if it's a pattern type
        if problem.get("type") == "pattern":
            problems.append(problem)
            print(f"✅ Pattern {len(problems)}: {problem['question']}")
            print(f"   Answer: {problem['answer']}")
            print("---")

        attempt += 1

    # Ensure we have enough problems
    while len(problems) < 15:
        # Add some fallback problems
        fallback = {
            "question": f"Complete the pattern: ⭐ - ❤️ - ⭐ - ❤️ - ⭐ - ____",
            "answer": "❤️",
            "type": "pattern",
            "explanation": "The pattern alternates star and heart",
        }
        problems.append(fallback)

    # Take only first 15 problems
    problems = problems[:15]

    # Generate PDF
    output_file = "test_visual_patterns_detailed.pdf"
    try:
        pdf_generator.generate_worksheet(
            subject="logic",
            age_group="4-5",
            problems=problems,
            output_filename=output_file,
            student_name="Test Student",
        )
        print(f"\n✅ PDF generated successfully: {output_file}")

        # Check file size
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"📄 File size: {file_size} bytes")

        return True

    except Exception as e:
        print(f"❌ Error generating PDF: {e}")
        return False


if __name__ == "__main__":
    success = test_visual_pattern_generation()
    if success:
        print("\n🎉 Visual pattern test completed successfully!")
    else:
        print("\n💥 Visual pattern test failed!")
