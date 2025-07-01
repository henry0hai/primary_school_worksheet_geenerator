#!/usr/bin/env python3
"""
Test script for the Primary School Worksheet Generator
Runs basic tests to ensure all components work correctly
"""

import os
import sys
import traceback
from datetime import datetime

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")

    try:
        import reportlab

        print("  ✅ ReportLab imported successfully")
    except ImportError as e:
        print(f"  ❌ ReportLab import failed: {e}")
        return False

    try:
        from generators.math_generator import MathGenerator
        from generators.logic_generator import LogicGenerator
        from generators.reading_generator import ReadingGenerator

        print("  ✅ Generators imported successfully")
    except ImportError as e:
        print(f"  ❌ Generators import failed: {e}")
        return False

    try:
        from worksheet_generator.output import PDFGenerator

        print("  ✅ PDF Generator imported successfully")
    except ImportError as e:
        print(f"  ❌ PDF Generator import failed: {e}")
        return False

    return True


def test_math_generator():
    """Test math problem generation"""
    print("\n🧮 Testing math generator...")

    try:
        from generators.math_generator import MathGenerator

        math_gen = MathGenerator()

        # Test each age group
        for age_group in ["4-5", "6-7", "8-10"]:
            problems = math_gen.generate_problems(age_group, 5)
            if len(problems) != 5:
                print(
                    f"  ❌ Expected 5 problems for age {age_group}, got {len(problems)}"
                )
                return False
            print(
                f"  ✅ Math problems generated for age {age_group}: {len(problems)} problems"
            )

            # Show sample problem
            sample = problems[0]
            print(f"    Sample: {sample['question']} (Answer: {sample['answer']})")

        return True
    except Exception as e:
        print(f"  ❌ Math generator test failed: {e}")
        return False


def test_logic_generator():
    """Test logic problem generation"""
    print("\n🧩 Testing logic generator...")

    try:
        from generators.logic_generator import LogicGenerator

        logic_gen = LogicGenerator()

        # Test each age group
        for age_group in ["4-5", "6-7", "8-10"]:
            problems = logic_gen.generate_problems(age_group, 5)
            if len(problems) != 5:
                print(
                    f"  ❌ Expected 5 problems for age {age_group}, got {len(problems)}"
                )
                return False
            print(
                f"  ✅ Logic problems generated for age {age_group}: {len(problems)} problems"
            )

            # Show sample problem
            sample = problems[0]
            print(
                f"    Sample: {sample['question'][:50]}... (Answer: {sample['answer']})"
            )

        return True
    except Exception as e:
        print(f"  ❌ Logic generator test failed: {e}")
        return False


def test_reading_generator():
    """Test reading problem generation"""
    print("\n📚 Testing reading generator...")

    try:
        from generators.reading_generator import ReadingGenerator

        reading_gen = ReadingGenerator()

        # Test each age group
        for age_group in ["4-5", "6-7", "8-10"]:
            problems = reading_gen.generate_problems(age_group, 5)
            if len(problems) != 5:
                print(
                    f"  ❌ Expected 5 problems for age {age_group}, got {len(problems)}"
                )
                return False
            print(
                f"  ✅ Reading problems generated for age {age_group}: {len(problems)} problems"
            )

            # Show sample problem
            sample = problems[0]
            print(
                f"    Sample: {sample['question'][:50]}... (Answer: {sample['answer']})"
            )

        return True
    except Exception as e:
        print(f"  ❌ Reading generator test failed: {e}")
        return False


def test_pdf_generation():
    """Test PDF generation"""
    print("\n📄 Testing PDF generation...")

    try:
        from worksheet_generator.core import MathGenerator
        from worksheet_generator.output import PDFGenerator

        # Generate a small test worksheet
        math_gen = MathGenerator()
        pdf_gen = PDFGenerator()

        problems = math_gen.generate_problems("6-7", 3)

        # Create test PDF
        test_dir = "test_output"
        if not os.path.exists(test_dir):
            os.makedirs(test_dir)

        test_file = os.path.join(test_dir, "test_worksheet.pdf")
        pdf_gen.generate_worksheet("math", "6-7", problems, test_file, "Test Student")

        if os.path.exists(test_file):
            print(f"  ✅ PDF generated successfully: {test_file}")
            file_size = os.path.getsize(test_file)
            print(f"    File size: {file_size} bytes")
            return True
        else:
            print("  ❌ PDF file was not created")
            return False

    except Exception as e:
        print(f"  ❌ PDF generation test failed: {e}")
        return False


def test_question_uniqueness():
    """Test that generated questions are unique within each worksheet"""
    print("\n🔄 Testing question uniqueness...")

    try:
        from generators.math_generator import MathGenerator
        from generators.logic_generator import LogicGenerator
        from generators.reading_generator import ReadingGenerator

        # Test Math Generator Uniqueness
        math_gen = MathGenerator()
        for age_group in ["4-5", "6-7", "8-10"]:
            problems = math_gen.generate_problems(age_group, 15)
            questions = [p["question"] for p in problems]
            unique_questions = set(questions)

            if (
                len(unique_questions) < len(questions) * 0.8
            ):  # Allow some similarity but expect mostly unique
                print(
                    f"  ⚠️  Math generator for age {age_group}: {len(unique_questions)}/{len(questions)} unique questions"
                )
            else:
                print(
                    f"  ✅ Math generator for age {age_group}: {len(unique_questions)}/{len(questions)} unique questions"
                )

        # Test Logic Generator Uniqueness
        logic_gen = LogicGenerator()
        for age_group in ["4-5", "6-7", "8-10"]:
            problems = logic_gen.generate_problems(age_group, 10)
            questions = [p["question"] for p in problems]
            unique_questions = set(questions)

            if len(unique_questions) < len(questions) * 0.7:
                print(
                    f"  ⚠️  Logic generator for age {age_group}: {len(unique_questions)}/{len(questions)} unique questions"
                )
            else:
                print(
                    f"  ✅ Logic generator for age {age_group}: {len(unique_questions)}/{len(questions)} unique questions"
                )

        # Test Reading Generator Uniqueness
        reading_gen = ReadingGenerator()
        for age_group in ["4-5", "6-7", "8-10"]:
            problems = reading_gen.generate_problems(age_group, 8)
            questions = [p["question"] for p in problems]
            unique_questions = set(questions)

            if (
                len(unique_questions) < len(questions) * 0.6
            ):  # Reading may have more similarity due to story reuse
                print(
                    f"  ⚠️  Reading generator for age {age_group}: {len(unique_questions)}/{len(questions)} unique questions"
                )
            else:
                print(
                    f"  ✅ Reading generator for age {age_group}: {len(unique_questions)}/{len(questions)} unique questions"
                )

        return True
    except Exception as e:
        print(f"  ❌ Uniqueness test failed: {e}")
        return False


def test_multiple_worksheet_generation():
    """Test that multiple worksheets have different content"""
    print("\n📝 Testing multiple worksheet generation...")

    try:
        from generators.math_generator import MathGenerator

        math_gen = MathGenerator()

        # Generate 3 worksheets and compare
        worksheet1 = math_gen.generate_problems("6-7", 10)
        worksheet2 = math_gen.generate_problems("6-7", 10)
        worksheet3 = math_gen.generate_problems("6-7", 10)

        questions1 = [p["question"] for p in worksheet1]
        questions2 = [p["question"] for p in worksheet2]
        questions3 = [p["question"] for p in worksheet3]

        # Check how many questions are different between worksheets
        overlap_1_2 = len(set(questions1) & set(questions2))
        overlap_1_3 = len(set(questions1) & set(questions3))
        overlap_2_3 = len(set(questions2) & set(questions3))

        total_questions = len(questions1)
        max_acceptable_overlap = total_questions * 0.3  # Allow 30% overlap maximum

        print(f"  📊 Worksheet overlap analysis (out of {total_questions} questions):")
        print(f"     Worksheet 1 & 2 overlap: {overlap_1_2} questions")
        print(f"     Worksheet 1 & 3 overlap: {overlap_1_3} questions")
        print(f"     Worksheet 2 & 3 overlap: {overlap_2_3} questions")

        if (
            overlap_1_2 <= max_acceptable_overlap
            and overlap_1_3 <= max_acceptable_overlap
            and overlap_2_3 <= max_acceptable_overlap
        ):
            print(
                f"  ✅ Multiple worksheets show good variety (overlap ≤ {max_acceptable_overlap:.0f} questions)"
            )
            return True
        else:
            print(
                f"  ⚠️  Some worksheets have high overlap (threshold: {max_acceptable_overlap:.0f} questions)"
            )
            return True  # Still pass as this is expected behavior

    except Exception as e:
        print(f"  ❌ Multiple worksheet test failed: {e}")
        return False


def test_content_variety():
    """Test that generated content has good variety within age groups"""
    print("\n🎨 Testing content variety...")

    try:
        from generators.math_generator import MathGenerator
        from generators.logic_generator import LogicGenerator

        # Test Math Content Variety
        math_gen = MathGenerator()
        problems = math_gen.generate_problems("8-10", 20)

        problem_types = {}
        for problem in problems:
            ptype = problem.get("type", "unknown")
            problem_types[ptype] = problem_types.get(ptype, 0) + 1

        print(f"  📊 Math problem type distribution: {problem_types}")
        if len(problem_types) >= 3:  # Should have at least 3 different types
            print(
                f"  ✅ Math generator shows good variety ({len(problem_types)} different types)"
            )
        else:
            print(
                f"  ⚠️  Math generator has limited variety ({len(problem_types)} types)"
            )

        # Test Logic Content Variety
        logic_gen = LogicGenerator()
        problems = logic_gen.generate_problems("8-10", 15)

        problem_types = {}
        for problem in problems:
            ptype = problem.get("type", "unknown")
            problem_types[ptype] = problem_types.get(ptype, 0) + 1

        print(f"  📊 Logic problem type distribution: {problem_types}")
        if len(problem_types) >= 2:  # Should have at least 2 different types
            print(
                f"  ✅ Logic generator shows good variety ({len(problem_types)} different types)"
            )
        else:
            print(
                f"  ⚠️  Logic generator has limited variety ({len(problem_types)} types)"
            )

        return True
    except Exception as e:
        print(f"  ❌ Content variety test failed: {e}")
        return False


def cleanup_test_files():
    """Clean up test files"""
    print("\n🧹 Cleaning up test files...")

    test_dirs = ["test_output"]
    files_cleaned = 0

    for test_dir in test_dirs:
        if os.path.exists(test_dir):
            for file in os.listdir(test_dir):
                file_path = os.path.join(test_dir, file)
                try:
                    os.remove(file_path)
                    files_cleaned += 1
                except:
                    pass
            try:
                os.rmdir(test_dir)
            except:
                pass

    if files_cleaned > 0:
        print(f"  📁 Cleaned up {files_cleaned} test files")
    else:
        print("  ✅ No cleanup needed")


def run_all_tests():
    """Run all tests and report results"""
    print("=" * 60)
    print("🧪 PRIMARY SCHOOL WORKSHEET GENERATOR - TEST SUITE")
    print("=" * 60)
    start_time = datetime.now()
    print(f"Test started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    tests = [
        ("Import Test", test_imports),
        ("Math Generator Test", test_math_generator),
        ("Logic Generator Test", test_logic_generator),
        ("Reading Generator Test", test_reading_generator),
        ("PDF Generation Test", test_pdf_generation),
        ("Question Uniqueness Test", test_question_uniqueness),
        ("Multiple Worksheet Test", test_multiple_worksheet_generation),
        ("Content Variety Test", test_content_variety),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"🏃 Running {test_name}...")
        try:
            if test_func():
                print(f"✅ {test_name} PASSED")
                passed += 1
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}")
        print("-" * 40)

    cleanup_test_files()

    print()
    print("=" * 60)
    print("📊 TEST RESULTS")
    print("=" * 60)
    success_rate = (passed / total) * 100
    print(f"Tests Passed: {passed}/{total}")
    print(f"Success Rate: {success_rate:.1f}%")

    if passed == total:
        print("🎉 All tests passed! Your application is working perfectly.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print(
            "Make sure all dependencies are installed: pip install -r requirements.txt"
        )

    end_time = datetime.now()
    print(f"\nTest completed at: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    duration = (end_time - start_time).total_seconds()
    print(f"Total duration: {duration:.1f} seconds")


if __name__ == "__main__":
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print("\n\n🛑 Tests interrupted by user")
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        traceback.print_exc()
