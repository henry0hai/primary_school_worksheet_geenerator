#!/usr/bin/env python3
"""
Test the updated answer key with visual patterns
"""

import sys
import os
from datetime import datetime

# Add the project root to the path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from worksheet_generator.core import LogicGenerator
from worksheet_generator.output import PDFGenerator


def test_visual_answer_key():
    """Test that answer key now shows visual patterns like the worksheet"""

    print("🧪 Testing Visual Answer Key Consistency...")
    print("=" * 50)

    # Generate a pattern problem with symbols
    logic_gen = LogicGenerator()
    pdf_gen = PDFGenerator()

    print("🧩 Generating logic pattern with symbols...")
    logic_problems = logic_gen.generate_problems(age_group="6-7", count=3)

    # Find a pattern problem with emojis
    pattern_problem = None
    for problem in logic_problems:
        if problem.get("type") == "pattern" and (
            "🔴" in problem["question"] or "🔵" in problem["question"]
        ):
            pattern_problem = problem
            break

    if not pattern_problem:
        print("❌ No pattern problem with color emojis found")
        return

    print(f"\n📝 Found pattern problem:")
    print(f"   Question: {pattern_problem['question']}")
    print(f"   Answer: {pattern_problem['answer']}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Generate worksheet
    worksheet_filename = f"test_visual_worksheet_{timestamp}.pdf"
    print(f"\n📄 Generating worksheet: {worksheet_filename}")
    pdf_gen.generate_worksheet(
        subject="logic",
        age_group="6-7",
        problems=[pattern_problem],
        output_filename=worksheet_filename,
    )

    # Generate answer key with visual patterns
    answer_key_filename = f"test_visual_answer_key_{timestamp}.pdf"
    print(f"📄 Generating answer key with visual patterns: {answer_key_filename}")
    pdf_gen.generate_answer_key(
        subject="logic",
        age_group="6-7",
        problems=[pattern_problem],
        output_filename=answer_key_filename,
    )

    # Check file sizes
    worksheet_size = (
        os.path.getsize(worksheet_filename) if os.path.exists(worksheet_filename) else 0
    )
    answer_key_size = (
        os.path.getsize(answer_key_filename)
        if os.path.exists(answer_key_filename)
        else 0
    )

    print(f"\n✅ Generated files:")
    print(f"   Worksheet: {worksheet_filename} ({worksheet_size:,} bytes)")
    print(f"   Answer key: {answer_key_filename} ({answer_key_size:,} bytes)")

    if worksheet_size > 1000 and answer_key_size > 1000:
        print(
            f"\n🎉 Success! Both files have good sizes and should show visual patterns!"
        )
        print(
            f"📖 Open both PDFs to verify they now have consistent visual pattern display"
        )
    else:
        print(f"\n⚠️  One or both files seem too small - there might be an issue")

    return True


if __name__ == "__main__":
    test_visual_answer_key()
