#!/usr/bin/env python3
"""
Test script to verify question uniqueness across all generators
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
    """Test that generators produce unique questions within each worksheet"""

    print("🧪 TESTING QUESTION UNIQUENESS")
    print("=" * 60)

    # Test parameters
    age_groups = ["4-5", "6-7", "8-10"]
    questions_per_worksheet = 15

    all_tests_passed = True

    for age_group in age_groups:
        print(f"\n📝 Testing Age Group: {age_group}")
        print("-" * 40)

        # Test Math Generator
        math_generator = MathGenerator()
        math_problems = math_generator.generate_problems(
            age_group, questions_per_worksheet
        )
        math_questions = [p["question"] for p in math_problems]
        math_unique = len(set(math_questions))
        math_total = len(math_questions)

        print(f"🧮 Math: {math_unique}/{math_total} unique questions", end="")
        if math_unique == math_total:
            print(" ✅")
        else:
            print(" ❌")
            all_tests_passed = False
            # Show duplicates
            seen = set()
            duplicates = []
            for q in math_questions:
                if q in seen:
                    duplicates.append(q)
                seen.add(q)
            if duplicates:
                print(f"   Duplicates: {duplicates[:2]}...")  # Show first 2 duplicates

        # Test Logic Generator
        logic_generator = LogicGenerator()
        logic_problems = logic_generator.generate_problems(
            age_group, questions_per_worksheet
        )
        logic_questions = [p["question"] for p in logic_problems]
        logic_unique = len(set(logic_questions))
        logic_total = len(logic_questions)

        print(f"🧩 Logic: {logic_unique}/{logic_total} unique questions", end="")
        if logic_unique == logic_total:
            print(" ✅")
        else:
            print(" ❌")
            all_tests_passed = False
            # Show duplicates
            seen = set()
            duplicates = []
            for q in logic_questions:
                if q in seen:
                    duplicates.append(q)
                seen.add(q)
            if duplicates:
                print(f"   Duplicates: {duplicates[:2]}...")

        # Test Reading Generator
        reading_generator = ReadingGenerator()
        reading_problems = reading_generator.generate_problems(
            age_group, questions_per_worksheet
        )
        reading_questions = [p["question"] for p in reading_problems]
        reading_unique = len(set(reading_questions))
        reading_total = len(reading_questions)

        print(f"📚 Reading: {reading_unique}/{reading_total} unique questions", end="")
        if reading_unique == reading_total:
            print(" ✅")
        else:
            print(" ❌")
            all_tests_passed = False
            # Show duplicates
            seen = set()
            duplicates = []
            for q in reading_questions:
                if q in seen:
                    duplicates.append(q)
                seen.add(q)
            if duplicates:
                print(f"   Duplicates: {duplicates[:2]}...")

    print("\n" + "=" * 60)

    if all_tests_passed:
        print("🎉 ALL UNIQUENESS TESTS PASSED!")
        print("✅ No duplicate questions found in any worksheet")
    else:
        print("⚠️  SOME TESTS FAILED")
        print("❌ Duplicate questions detected")

    return all_tests_passed


def test_multiple_worksheets_variety():
    """Test that multiple worksheets for the same age group have variety"""

    print("\n🔄 TESTING MULTIPLE WORKSHEET VARIETY")
    print("=" * 60)

    age_group = "6-7"  # Test with one age group
    num_worksheets = 3
    questions_per_worksheet = 10

    # Generate multiple worksheets for each generator
    for generator_name, generator_class in [
        ("Math", MathGenerator),
        ("Logic", LogicGenerator),
        ("Reading", ReadingGenerator),
    ]:
        print(f"\n📊 {generator_name} Generator - Multiple Worksheets:")

        worksheets = []
        for i in range(num_worksheets):
            generator = generator_class()
            problems = generator.generate_problems(age_group, questions_per_worksheet)
            questions = [p["question"] for p in problems]
            worksheets.append(questions)

        # Calculate overlap between worksheets
        total_overlap = 0
        comparisons = 0

        for i in range(num_worksheets):
            for j in range(i + 1, num_worksheets):
                overlap = len(set(worksheets[i]) & set(worksheets[j]))
                total_overlap += overlap
                comparisons += 1
                print(
                    f"   Worksheet {i+1} & {j+1} overlap: {overlap}/{questions_per_worksheet} questions"
                )

        avg_overlap = total_overlap / comparisons if comparisons > 0 else 0
        print(f"   Average overlap: {avg_overlap:.1f} questions")

        if avg_overlap <= 2:  # Allow some overlap, but not too much
            print("   ✅ Good variety between worksheets")
        else:
            print("   ⚠️  High overlap between worksheets")


if __name__ == "__main__":
    uniqueness_passed = test_question_uniqueness()
    test_multiple_worksheets_variety()

    if uniqueness_passed:
        print("\n🎯 SUMMARY: Question uniqueness is working correctly!")
    else:
        print("\n⚠️  SUMMARY: Some issues with question uniqueness detected.")
