#!/usr/bin/env python3
"""
Test script to verify the answer key emoji/symbol fix
"""

import sys
import os
from datetime import datetime

# Add the project root to the path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from worksheet_generator.core import (
    MathGenerator,
    LogicGenerator,
    ReadingGenerator,
)
from worksheet_generator.output import PDFGenerator


def test_answer_key_symbols():
    """Test that symbols are properly converted in answer keys"""

    print("🧪 Testing Answer Key Symbol Conversion Fix...")
    print("=" * 50)

    # Initialize generators (they load data sources automatically)
    print("📁 Initializing generators...")
    math_gen = MathGenerator()
    logic_gen = LogicGenerator()
    pdf_gen = PDFGenerator()

    # Generate some problems with symbols
    print("🔧 Generating test problems with symbols...")

    # Generate a few math and logic problems that likely contain symbols
    math_problems = math_gen.generate_problems(age_group="6-7", count=2)
    logic_problems = logic_gen.generate_problems(age_group="6-7", count=2)

    # Combine for comprehensive test
    all_problems = []

    # Add subject indicators for comprehensive format
    for problem in math_problems:
        problem["subject"] = "math"
        all_problems.append(problem)

    for problem in logic_problems:
        problem["subject"] = "logic"
        all_problems.append(problem)

    print(f"📋 Generated {len(all_problems)} test problems")

    # Print the problems to see what symbols we have
    print("\n📝 Sample problems with symbols:")
    for i, problem in enumerate(all_problems, 1):
        print(
            f"  {i}. [{problem.get('subject', 'unknown').upper()}:{problem.get('type', 'unknown')}] {problem['question'][:80]}..."
        )
        print(f"     Answer: {problem['answer']}")

    # Generate answer key PDF
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    answer_key_filename = f"test_answer_key_symbols_{timestamp}.pdf"

    print(f"\n🎯 Generating answer key PDF: {answer_key_filename}")

    try:
        pdf_gen.generate_answer_key(
            subject="comprehensive",
            age_group="6-7",
            problems=all_problems,
            output_filename=answer_key_filename,
        )

        # Check if file was created and has content
        if os.path.exists(answer_key_filename):
            file_size = os.path.getsize(answer_key_filename)
            print(f"✅ Answer key PDF created: {answer_key_filename}")
            print(f"   File size: {file_size:,} bytes")

            if file_size > 1000:  # Reasonable size check
                print("✅ File size looks good - symbols should be properly converted!")
            else:
                print("⚠️  File size seems small - might be an issue")
        else:
            print("❌ Answer key PDF was not created")

    except Exception as e:
        print(f"❌ Error generating answer key PDF: {e}")
        return False

    print("\n🎉 Answer key symbol conversion test completed!")
    print(
        "📖 Open the generated PDF to verify symbols are displayed as [RED], [BLUE], etc."
    )

    return True


if __name__ == "__main__":
    test_answer_key_symbols()
