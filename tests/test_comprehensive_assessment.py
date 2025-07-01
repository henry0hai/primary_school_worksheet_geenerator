#!/usr/bin/env python3
"""
Test the comprehensive assessment functionality
"""

import sys
import os

# Add the project root to the path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from cli import generate_comprehensive_problems, get_comprehensive_distribution
from collections import Counter


def test_comprehensive_distribution():
    """Test the distribution calculation for comprehensive assessments"""
    print("🧪 Testing Comprehensive Assessment Distribution...")

    test_cases = [("4-5", 30), ("6-7", 40), ("8-10", 50)]

    for age_group, total_questions in test_cases:
        print(f"\n📊 Age Group {age_group} - {total_questions} questions:")
        distribution = get_comprehensive_distribution(age_group, total_questions)

        total_assigned = sum(distribution.values())
        print(f"  Total assigned: {total_assigned}/{total_questions}")

        for subject, count in distribution.items():
            percentage = (count / total_questions) * 100
            print(f"  • {subject.title()}: {count} questions ({percentage:.1f}%)")

        # Verify total matches
        assert (
            total_assigned == total_questions
        ), f"Distribution doesn't add up for {age_group}"
        print(f"  ✅ Distribution validated")

    print(f"\n✅ All distribution tests passed!")
    return True


def test_comprehensive_generation():
    """Test generating a comprehensive assessment"""
    print("\n🎯 Testing Comprehensive Assessment Generation...")

    age_group = "6-7"
    num_questions = 20  # Smaller number for testing

    print(
        f"\nGenerating comprehensive assessment for {age_group} with {num_questions} questions..."
    )

    try:
        problems = generate_comprehensive_problems(age_group, num_questions)

        print(f"\n📊 Generated {len(problems)} problems")

        # Check subject distribution
        subject_counts = Counter([p.get("subject", "unknown") for p in problems])
        print(f"\nActual distribution:")
        for subject, count in subject_counts.items():
            percentage = (count / len(problems)) * 100
            print(f"  • {subject.title()}: {count} questions ({percentage:.1f}%)")

        # Check problem types
        type_counts = Counter([p.get("type", "unknown") for p in problems])
        print(f"\nProblem types:")
        for prob_type, count in type_counts.items():
            print(f"  • {prob_type}: {count}")

        # Verify uniqueness
        question_texts = [p["question"] for p in problems]
        unique_questions = set(question_texts)
        print(
            f"\nUniqueness: {len(unique_questions)}/{len(question_texts)} unique questions"
        )

        if len(unique_questions) != len(question_texts):
            duplicates = len(question_texts) - len(unique_questions)
            print(f"⚠️  Found {duplicates} duplicate questions!")
            return False

        # Show sample problems
        print(f"\n📋 Sample problems:")
        for i, problem in enumerate(problems[:3], 1):
            subject = problem.get("subject", "unknown")
            prob_type = problem.get("type", "unknown")
            question = (
                problem["question"][:80] + "..."
                if len(problem["question"]) > 80
                else problem["question"]
            )
            print(f"  {i}. [{subject.upper()}:{prob_type}] {question}")

        print(f"\n✅ Comprehensive assessment generation successful!")
        return True

    except Exception as e:
        print(f"❌ Error generating comprehensive assessment: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Run all comprehensive assessment tests"""
    print("🎯 Testing Comprehensive Assessment System")
    print("=" * 50)

    tests = [
        test_comprehensive_distribution,
        test_comprehensive_generation,
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
        print("🎉 All comprehensive assessment tests passed!")
        print("✨ The system is ready for final exam generation!")
        return True
    else:
        print("❌ Some tests failed. Please check the implementation.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
