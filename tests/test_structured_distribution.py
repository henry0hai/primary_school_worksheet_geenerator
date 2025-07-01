#!/usr/bin/env python3
"""
Test structured distribution functionality for all generators.
Verifies that all generators (math, logic, reading) use age-appropriate
question type distributions and produce balanced, unique worksheets.
"""

import sys
import os
from collections import Counter

# Add the project root to the path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from worksheet_generator.core import (
    MathGenerator,
    LogicGenerator,
    ReadingGenerator,
)


def test_math_distribution():
    """Test structured distribution in math generator"""
    print("🧮 Testing Math Generator Structured Distribution...")

    generator = MathGenerator()
    age_groups = ["4-5", "6-7", "8-10"]

    for age_group in age_groups:
        print(f"\n  Age Group: {age_group}")
        problems = generator.generate_problems(age_group, 20)

        # Count problem types
        type_counts = Counter([p["type"] for p in problems])
        print(f"    Generated {len(problems)} problems:")
        for problem_type, count in type_counts.items():
            percentage = (count / len(problems)) * 100
            print(f"      • {problem_type}: {count} ({percentage:.1f}%)")

        # Verify all problems are unique
        question_texts = [p["question"] for p in problems]
        unique_questions = set(question_texts)
        print(
            f"    Uniqueness: {len(unique_questions)}/{len(question_texts)} unique questions"
        )

        if len(unique_questions) != len(question_texts):
            print(
                f"    ⚠️  Found {len(question_texts) - len(unique_questions)} duplicate questions!"
            )
            return False

        # Verify age-appropriate distribution
        if age_group == "4-5":
            # Should be mostly addition with some subtraction
            if type_counts.get("addition", 0) < type_counts.get("multiplication", 0):
                print(f"    ❌ Age 4-5 should have more addition than multiplication")
                return False
        elif age_group == "8-10":
            # Should have good variety including multiplication/division
            if (
                type_counts.get("multiplication", 0) == 0
                and type_counts.get("division", 0) == 0
            ):
                print(f"    ❌ Age 8-10 should have multiplication or division")
                return False

    print("  ✅ Math generator distribution test passed!")
    return True


def test_logic_distribution():
    """Test structured distribution in logic generator"""
    print("\n🧩 Testing Logic Generator Structured Distribution...")

    generator = LogicGenerator()
    age_groups = ["4-5", "6-7", "8-10"]

    for age_group in age_groups:
        print(f"\n  Age Group: {age_group}")
        problems = generator.generate_problems(age_group, 20)

        # Count problem types
        type_counts = Counter([p["type"] for p in problems])
        print(f"    Generated {len(problems)} problems:")
        for problem_type, count in type_counts.items():
            percentage = (count / len(problems)) * 100
            print(f"      • {problem_type}: {count} ({percentage:.1f}%)")

        # Verify all problems are unique
        question_texts = [p["question"] for p in problems]
        unique_questions = set(question_texts)
        print(
            f"    Uniqueness: {len(unique_questions)}/{len(question_texts)} unique questions"
        )

        if len(unique_questions) != len(question_texts):
            print(
                f"    ⚠️  Found {len(question_texts) - len(unique_questions)} duplicate questions!"
            )
            return False

        # Verify age-appropriate distribution
        if age_group == "4-5":
            # Should be mostly patterns
            if type_counts.get("pattern", 0) < type_counts.get("logical_reasoning", 0):
                print(
                    f"    ❌ Age 4-5 should have more patterns than logical reasoning"
                )
                return False
        elif age_group == "8-10":
            # Should have good reasoning component
            if type_counts.get("logical_reasoning", 0) == 0:
                print(f"    ❌ Age 8-10 should have logical reasoning questions")
                return False

    print("  ✅ Logic generator distribution test passed!")
    return True


def test_reading_distribution():
    """Test structured distribution in reading generator"""
    print("\n📚 Testing Reading Generator Structured Distribution...")

    generator = ReadingGenerator()
    age_groups = ["4-5", "6-7", "8-10"]

    for age_group in age_groups:
        print(f"\n  Age Group: {age_group}")
        problems = generator.generate_problems(age_group, 20)

        # Count problem types
        type_counts = Counter([p["type"] for p in problems])
        print(f"    Generated {len(problems)} problems:")
        for problem_type, count in type_counts.items():
            percentage = (count / len(problems)) * 100
            print(f"      • {problem_type}: {count} ({percentage:.1f}%)")

        # Verify all problems are unique
        question_texts = [p["question"] for p in problems]
        unique_questions = set(question_texts)
        print(
            f"    Uniqueness: {len(unique_questions)}/{len(question_texts)} unique questions"
        )

        if len(unique_questions) != len(question_texts):
            print(
                f"    ⚠️  Found {len(question_texts) - len(unique_questions)} duplicate questions!"
            )
            return False

        # Verify age-appropriate distribution
        if age_group == "4-5":
            # Should be mostly vocabulary
            if type_counts.get("vocabulary", 0) < type_counts.get(
                "story_comprehension", 0
            ):
                print(
                    f"    ❌ Age 4-5 should have more vocabulary than story comprehension"
                )
                return False
        elif age_group == "8-10":
            # Should have good story comprehension component
            if type_counts.get("story_comprehension", 0) == 0:
                print(f"    ❌ Age 8-10 should have story comprehension questions")
                return False

    print("  ✅ Reading generator distribution test passed!")
    return True


def test_worksheet_variety():
    """Test that multiple worksheets for the same age group show variety"""
    print("\n🎲 Testing Worksheet Variety...")

    # Test math generator variety
    print("  Testing math worksheet variety...")
    math_gen = MathGenerator()

    worksheet1 = math_gen.generate_problems("6-7", 15)
    worksheet2 = math_gen.generate_problems("6-7", 15)

    # Check that worksheets are different
    questions1 = set([p["question"] for p in worksheet1])
    questions2 = set([p["question"] for p in worksheet2])

    overlap = questions1.intersection(questions2)
    overlap_percentage = (len(overlap) / len(questions1)) * 100

    print(
        f"    Math worksheets overlap: {len(overlap)}/{len(questions1)} questions ({overlap_percentage:.1f}%)"
    )

    if overlap_percentage > 50:  # Allow some overlap but not too much
        print(
            f"    ⚠️  Too much overlap between math worksheets: {overlap_percentage:.1f}%"
        )
        return False

    # Test logic generator variety
    print("  Testing logic worksheet variety...")
    logic_gen = LogicGenerator()

    worksheet1 = logic_gen.generate_problems("6-7", 15)
    worksheet2 = logic_gen.generate_problems("6-7", 15)

    questions1 = set([p["question"] for p in worksheet1])
    questions2 = set([p["question"] for p in worksheet2])

    overlap = questions1.intersection(questions2)
    overlap_percentage = (len(overlap) / len(questions1)) * 100

    print(
        f"    Logic worksheets overlap: {len(overlap)}/{len(questions1)} questions ({overlap_percentage:.1f}%)"
    )

    if overlap_percentage > 50:
        print(
            f"    ⚠️  Too much overlap between logic worksheets: {overlap_percentage:.1f}%"
        )
        return False

    # Test reading generator variety
    print("  Testing reading worksheet variety...")
    reading_gen = ReadingGenerator()

    worksheet1 = reading_gen.generate_problems("6-7", 15)
    worksheet2 = reading_gen.generate_problems("6-7", 15)

    questions1 = set([p["question"] for p in worksheet1])
    questions2 = set([p["question"] for p in worksheet2])

    overlap = questions1.intersection(questions2)
    overlap_percentage = (len(overlap) / len(questions1)) * 100

    print(
        f"    Reading worksheets overlap: {len(overlap)}/{len(questions1)} questions ({overlap_percentage:.1f}%)"
    )

    if overlap_percentage > 50:
        print(
            f"    ⚠️  Too much overlap between reading worksheets: {overlap_percentage:.1f}%"
        )
        return False

    print("  ✅ Worksheet variety test passed!")
    return True


def test_all_structured_distributions():
    """Run all structured distribution tests"""
    print("🎯 Testing Structured Distribution System")
    print("=" * 50)

    tests = [
        test_math_distribution,
        test_logic_distribution,
        test_reading_distribution,
        test_worksheet_variety,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        try:
            if test():
                passed += 1
            else:
                print(f"❌ {test.__name__} failed!")
        except Exception as e:
            print(f"❌ {test.__name__} failed with error: {e}")

    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All structured distribution tests passed!")
        print(
            "✨ The system now provides balanced, age-appropriate question distributions!"
        )
        return True
    else:
        print("❌ Some tests failed. Please check the implementation.")
        return False


if __name__ == "__main__":
    success = test_all_structured_distributions()
    sys.exit(0 if success else 1)
