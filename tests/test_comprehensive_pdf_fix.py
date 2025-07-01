#!/usr/bin/env python3
"""
Test the comprehensive assessment PDF generation fix
"""

import sys
import os

# Add the project root to the path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from cli import generate_comprehensive_problems
from worksheet_generator.output import PDFGenerator
from datetime import datetime


def test_comprehensive_pdf_generation():
    """Test generating a comprehensive assessment PDF"""
    print("🧪 Testing Comprehensive Assessment PDF Generation...")

    # Generate a small comprehensive assessment
    age_group = "6-7"
    num_questions = 6

    print(f"Generating {num_questions} comprehensive questions for age {age_group}...")
    problems = generate_comprehensive_problems(age_group, num_questions)

    print(f"Generated {len(problems)} problems")

    # Create PDF generator
    pdf_gen = PDFGenerator()

    # Generate test files
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    worksheet_filename = f"test_comprehensive_worksheet_{timestamp}.pdf"
    answer_filename = f"test_comprehensive_answers_{timestamp}.pdf"

    # Test worksheet generation
    print("Generating worksheet PDF...")
    try:
        pdf_gen.generate_worksheet(
            subject="comprehensive",
            age_group=age_group,
            problems=problems,
            output_filename=worksheet_filename,
            student_name="Test Student",
        )
        print(f"✅ Worksheet PDF created: {worksheet_filename}")

        # Check file size (should be larger than just title)
        file_size = os.path.getsize(worksheet_filename)
        print(f"   File size: {file_size:,} bytes")

        if file_size < 2000:  # Very small files likely have no content
            print("⚠️  File seems too small - may not contain questions")
            return False

    except Exception as e:
        print(f"❌ Error generating worksheet: {e}")
        return False

    # Test answer key generation
    print("Generating answer key PDF...")
    try:
        pdf_gen.generate_answer_key(
            subject="comprehensive",
            age_group=age_group,
            problems=problems,
            output_filename=answer_filename,
        )
        print(f"✅ Answer key PDF created: {answer_filename}")

        # Check file size
        file_size = os.path.getsize(answer_filename)
        print(f"   File size: {file_size:,} bytes")

    except Exception as e:
        print(f"❌ Error generating answer key: {e}")
        return False

    print("\n📋 Sample problems included:")
    for i, problem in enumerate(problems[:3], 1):
        subject = problem.get("subject", "unknown")
        prob_type = problem.get("type", "unknown")
        question = (
            problem["question"][:60] + "..."
            if len(problem["question"]) > 60
            else problem["question"]
        )
        print(f"  {i}. [{subject.upper()}:{prob_type}] {question}")

    print(f"\n✅ Comprehensive PDF generation test completed successfully!")
    print(f"   Generated files: {worksheet_filename}, {answer_filename}")

    return True


def main():
    """Run the comprehensive PDF test"""
    print("🎯 Testing Comprehensive Assessment PDF Fix")
    print("=" * 50)

    try:
        success = test_comprehensive_pdf_generation()

        if success:
            print("\n🎉 PDF generation fix successful!")
            print("✨ Comprehensive assessments now generate proper worksheet PDFs!")
        else:
            print("\n❌ PDF generation test failed.")

        return success

    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
