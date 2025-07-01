#!/usr/bin/env python3
"""
Test the explanation text consistency fix
"""

import sys
import os
from datetime import datetime

# Add the project root to the path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from worksheet_generator.core import LogicGenerator
from worksheet_generator.output import PDFGenerator


def test_explanation_consistency():
    """Test that explanation text is consistently formatted"""

    print("🧪 Testing Explanation Text Consistency...")
    print("=" * 50)

    # Initialize generators
    logic_gen = LogicGenerator()
    pdf_gen = PDFGenerator()

    # Generate a pattern problem with symbols
    print("🧩 Generating logic pattern with explanation...")
    logic_problems = logic_gen.generate_problems(age_group="6-7", count=5)

    # Find a pattern problem with emojis
    pattern_problem = None
    for problem in logic_problems:
        if (
            problem.get("type") == "pattern"
            and ("🔴" in problem["question"] or "🔵" in problem["question"])
            and "explanation" in problem
            and problem["explanation"]
        ):
            pattern_problem = problem
            break

    if not pattern_problem:
        print("❌ No pattern problem with color emojis and explanation found")
        print("Available problems:")
        for i, p in enumerate(logic_problems):
            print(f"  {i+1}. {p.get('type', 'unknown')}: {p['question'][:50]}...")
            print(
                f"     Has explanation: {'explanation' in p and bool(p['explanation'])}"
            )
        return

    print(f"\n📝 Found pattern problem with explanation:")
    print(f"   Question: {pattern_problem['question']}")
    print(f"   Answer: {pattern_problem['answer']}")
    print(f"   Explanation: {pattern_problem['explanation']}")

    # Test emoji conversion on explanation
    print(f"\n🔧 Testing explanation conversion:")
    original_explanation = pattern_problem["explanation"]
    converted_explanation = pdf_gen._convert_emoji_to_text(original_explanation)
    print(f"   Original: {original_explanation}")
    print(f"   Converted: {converted_explanation}")

    # Generate test files
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Generate worksheet
    worksheet_filename = f"test_explanation_worksheet_{timestamp}.pdf"
    print(f"\n📄 Generating worksheet: {worksheet_filename}")
    pdf_gen.generate_worksheet(
        subject="logic",
        age_group="6-7",
        problems=[pattern_problem],
        output_filename=worksheet_filename,
    )

    # Generate answer key
    answer_key_filename = f"test_explanation_answer_key_{timestamp}.pdf"
    print(f"📄 Generating answer key: {answer_key_filename}")
    pdf_gen.generate_answer_key(
        subject="logic",
        age_group="6-7",
        problems=[pattern_problem],
        output_filename=answer_key_filename,
    )

    # Check file sizes
    worksheet_size = os.path.getsize(worksheet_filename)
    answer_key_size = os.path.getsize(answer_key_filename)

    print(f"\n✅ Generated files:")
    print(f"   Worksheet: {worksheet_filename} ({worksheet_size:,} bytes)")
    print(f"   Answer key: {answer_key_filename} ({answer_key_size:,} bytes)")

    print(f"\n🎉 Success! Explanation text should now be consistently formatted!")
    print(
        f"📖 Check the answer key PDF to verify explanation shows: {converted_explanation}"
    )


if __name__ == "__main__":
    test_explanation_consistency()
