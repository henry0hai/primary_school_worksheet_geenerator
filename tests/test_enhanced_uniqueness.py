#!/usr/bin/env python3
"""
Enhanced uniqueness test to verify that all generators produce unique questions
"""

import sys
import os

# Add the project root to the path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from worksheet_generator.core import (
    MathGenerator,
    LogicGenerator,
    ReadingGenerator,
)


def test_question_uniqueness():
    """Test that each generator produces unique questions within a worksheet"""
    print("🧪 ENHANCED QUESTION UNIQUENESS TEST")
    print("=" * 60)

    # Test all age groups
    age_groups = ["4-5", "6-7", "8-10"]
    all_passed = True

    for age_group in age_groups:
        print(f"\n📝 Testing Age Group: {age_group}")
        print("-" * 40)

        # Test Math Generator
        math_gen = MathGenerator()
        math_problems = math_gen.generate_problems(
            age_group, 20
        )  # Generate more problems
        math_questions = [p["question"] for p in math_problems]
        math_unique = len(set(math_questions))
        math_total = len(math_questions)

        if math_unique == math_total:
            print(f"🧮 Math: {math_unique}/{math_total} unique questions ✅")
        else:
            print(f"🧮 Math: {math_unique}/{math_total} unique questions ❌")
            duplicates = [q for q in math_questions if math_questions.count(q) > 1]
            print(f"   Duplicates: {list(set(duplicates))[:3]}...")
            all_passed = False

        # Test Logic Generator
        logic_gen = LogicGenerator()
        logic_problems = logic_gen.generate_problems(
            age_group, 20
        )  # Generate more problems
        logic_questions = [p["question"] for p in logic_problems]
        logic_unique = len(set(logic_questions))
        logic_total = len(logic_questions)

        if logic_unique == logic_total:
            print(f"🧩 Logic: {logic_unique}/{logic_total} unique questions ✅")
        else:
            print(f"🧩 Logic: {logic_unique}/{logic_total} unique questions ❌")
            duplicates = [q for q in logic_questions if logic_questions.count(q) > 1]
            print(f"   Duplicates: {list(set(duplicates))[:3]}...")
            all_passed = False

        # Test Reading Generator
        reading_gen = ReadingGenerator()
        reading_problems = reading_gen.generate_problems(
            age_group, 20
        )  # Generate more problems
        reading_questions = [p["question"] for p in reading_problems]
        reading_unique = len(set(reading_questions))
        reading_total = len(reading_questions)

        if reading_unique == reading_total:
            print(f"📚 Reading: {reading_unique}/{reading_total} unique questions ✅")
        else:
            print(f"📚 Reading: {reading_unique}/{reading_total} unique questions ❌")
            duplicates = [
                q for q in reading_questions if reading_questions.count(q) > 1
            ]
            print(f"   Duplicates: {list(set(duplicates))[:3]}...")
            all_passed = False

    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ALL UNIQUENESS TESTS PASSED!")
        print("✅ No duplicate questions detected in any generator")
    else:
        print("⚠️  SOME TESTS FAILED")
        print("❌ Duplicate questions detected")

    return all_passed


def test_worksheet_variety():
    """Test that multiple worksheets have good variety between them"""
    print("\n🔄 TESTING WORKSHEET VARIETY")
    print("=" * 60)

    age_group = "6-7"  # Test with middle age group

    # Generate 3 worksheets for each type
    generators = {
        "Math": MathGenerator(),
        "Logic": LogicGenerator(),
        "Reading": ReadingGenerator(),
    }

    for gen_name, generator in generators.items():
        print(f"\n📊 {gen_name} Generator - Multiple Worksheets:")

        # Generate 3 worksheets
        worksheets = []
        for i in range(3):
            if hasattr(generator, "reset_generated_questions"):
                generator.reset_generated_questions()
            problems = generator.generate_problems(age_group, 10)
            questions = [p["question"] for p in problems]
            worksheets.append(set(questions))

        # Calculate overlaps
        overlaps = []
        total_overlap = 0

        for i in range(len(worksheets)):
            for j in range(i + 1, len(worksheets)):
                overlap = len(worksheets[i].intersection(worksheets[j]))
                overlaps.append(overlap)
                total_overlap += overlap
                print(f"   Worksheet {i+1} & {j+1} overlap: {overlap}/10 questions")

        avg_overlap = total_overlap / len(overlaps) if overlaps else 0
        print(f"   Average overlap: {avg_overlap:.1f} questions")

        if avg_overlap <= 5:
            print(f"   ✅ Good variety between worksheets")
        else:
            print(f"   ⚠️  High overlap between worksheets")


if __name__ == "__main__":
    uniqueness_passed = test_question_uniqueness()
    test_worksheet_variety()

    print(f"\n{'=' * 60}")
    if uniqueness_passed:
        print("🎯 SUMMARY: All uniqueness improvements successful!")
    else:
        print("⚠️  SUMMARY: Some issues still need attention.")
