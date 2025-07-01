#!/usr/bin/env python3
"""
Master Test Suite for Primary School Worksheet Generator

This is the main test runner that executes all tests in the project.
It organizes tests by category and provides comprehensive reporting.

Usage:
    python run_all_tests.py              # Run all tests
    python run_all_tests.py --category core    # Run only core tests
    python run_all_tests.py --verbose          # Verbose output
    python run_all_tests.py --quick            # Skip slow tests
"""

import os
import sys
import time
import argparse
import subprocess
from datetime import datetime
from typing import Dict, List, Tuple
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))


class TestRunner:
    """Master test runner for the worksheet generator project"""

    def __init__(self):
        self.project_root = project_root
        self.test_results = {}
        self.start_time = None
        self.verbose = False

    def discover_tests(self) -> Dict[str, List[str]]:
        """Discover all test files and categorize them"""

        test_categories = {
            "core": [
                "test_structured_distribution.py",
                "test_enhanced_uniqueness.py",
                "test_uniqueness.py",
                "test_classification_fix.py",
            ],
            "comprehensive": [
                "test_comprehensive_assessment.py",
                "test_comprehensive_pdf_fix.py",
            ],
            "visual": [
                "test_visual_patterns.py",
                "test_visual_consistency.py",
                "test_animal_patterns.py",
            ],
            "pdf_generation": [
                "test_answer_key_fix.py",
                "test_explanation_fix.py",
            ],
            "integration": [
                "test_app.py",
            ],
        }

        # Verify files exist and remove missing ones
        existing_tests = {}
        tests_dir = self.project_root / "tests"

        for category, test_files in test_categories.items():
            existing_files = []
            for test_file in test_files:
                # Check both project root and tests/ directory
                test_path_root = self.project_root / test_file
                test_path_tests = tests_dir / test_file

                if test_path_tests.exists():
                    existing_files.append(f"tests/{test_file}")
                elif test_path_root.exists():
                    existing_files.append(test_file)
                elif self.verbose:
                    print(f"⚠️  Test file not found: {test_file}")

            if existing_files:
                existing_tests[category] = existing_files

        return existing_tests

    def run_test_file(self, test_file: str) -> Tuple[bool, str, float]:
        """Run a single test file and return (success, output, duration)"""
        test_path = self.project_root / test_file

        if not test_path.exists():
            return False, f"Test file not found: {test_file}", 0.0

        start_time = time.time()

        try:
            # Run the test file as a subprocess
            result = subprocess.run(
                [sys.executable, str(test_path)],
                cwd=str(self.project_root),
                capture_output=True,
                text=True,
                timeout=60,  # 1 minute timeout per test
            )

            duration = time.time() - start_time
            success = result.returncode == 0
            output = result.stdout + result.stderr

            return success, output, duration

        except subprocess.TimeoutExpired:
            duration = time.time() - start_time
            return False, f"Test timed out after 60 seconds", duration
        except Exception as e:
            duration = time.time() - start_time
            return False, f"Error running test: {str(e)}", duration

    def print_header(self):
        """Print test suite header"""
        print("=" * 80)
        print("🧪 PRIMARY SCHOOL WORKSHEET GENERATOR - MASTER TEST SUITE")
        print("=" * 80)
        print(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📁 Project root: {self.project_root}")
        print()

    def print_category_header(self, category: str, test_count: int):
        """Print category header"""
        print(f"\n🏷️  {category.upper()} TESTS ({test_count} tests)")
        print("-" * 50)

    def print_test_result(
        self, test_file: str, success: bool, duration: float, output: str = ""
    ):
        """Print individual test result"""
        status_icon = "✅" if success else "❌"
        duration_str = f"{duration:.2f}s"

        print(f"{status_icon} {test_file:<35} [{duration_str:>6}]")

        if not success and self.verbose:
            # Print error details in verbose mode
            print(f"   Error output:")
            for line in output.split("\n")[:10]:  # Limit to first 10 lines
                if line.strip():
                    print(f"   {line}")
            if len(output.split("\n")) > 10:
                print(f"   ... (output truncated)")
            print()

    def print_summary(self, all_results: Dict[str, List[Tuple]]):
        """Print final test summary"""
        print("\n" + "=" * 80)
        print("📊 TEST SUMMARY")
        print("=" * 80)

        total_tests = 0
        total_passed = 0
        total_duration = 0

        for category, results in all_results.items():
            category_passed = sum(1 for success, _, _ in results if success)
            category_total = len(results)
            category_duration = sum(duration for _, _, duration in results)

            total_tests += category_total
            total_passed += category_passed
            total_duration += category_duration

            status = "✅" if category_passed == category_total else "❌"
            print(
                f"{status} {category.upper():<15} {category_passed:>2}/{category_total} passed [{category_duration:>6.2f}s]"
            )

        print("-" * 50)
        overall_status = "✅" if total_passed == total_tests else "❌"
        print(
            f"{overall_status} OVERALL{'':<11} {total_passed:>2}/{total_tests} passed [{total_duration:>6.2f}s]"
        )

        if total_passed == total_tests:
            print(
                "\n🎉 All tests passed! The worksheet generator is working correctly."
            )
        else:
            failed_count = total_tests - total_passed
            print(
                f"\n⚠️  {failed_count} test(s) failed. Please review the output above."
            )

        print(f"\n⏱️  Total execution time: {total_duration:.2f} seconds")
        print(f"📅 Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    def run_tests(self, categories: List[str] = None, quick: bool = False):
        """Run tests for specified categories or all categories"""
        self.start_time = time.time()
        self.print_header()

        # Discover available tests
        available_tests = self.discover_tests()

        if not available_tests:
            print("❌ No test files found!")
            return False

        # Filter categories if specified
        if categories:
            filtered_tests = {}
            for category in categories:
                if category in available_tests:
                    filtered_tests[category] = available_tests[category]
                else:
                    print(
                        f"⚠️  Category '{category}' not found. Available: {list(available_tests.keys())}"
                    )
            available_tests = filtered_tests

        if not available_tests:
            print("❌ No tests to run after filtering!")
            return False

        # Skip slow tests in quick mode
        if quick:
            print("🚀 Quick mode: Skipping potentially slow tests")
            slow_tests = ["test_comprehensive_pdf_fix.py", "test_visual_patterns.py"]
            for category in available_tests:
                available_tests[category] = [
                    test for test in available_tests[category] if test not in slow_tests
                ]

        # Run tests by category
        all_results = {}

        for category, test_files in available_tests.items():
            if not test_files:
                continue

            self.print_category_header(category, len(test_files))
            category_results = []

            for test_file in test_files:
                success, output, duration = self.run_test_file(test_file)
                category_results.append((success, output, duration))
                self.print_test_result(test_file, success, duration, output)

            all_results[category] = category_results

        # Print final summary
        self.print_summary(all_results)

        # Return True if all tests passed
        return all(
            all(success for success, _, _ in results)
            for results in all_results.values()
        )


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Master test runner for Primary School Worksheet Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_all_tests.py                    # Run all tests
  python run_all_tests.py --category core    # Run core tests only
  python run_all_tests.py --verbose          # Verbose output with error details
  python run_all_tests.py --quick            # Skip slow tests
  python run_all_tests.py --category core --verbose  # Core tests with verbose output

Available categories:
  core          - Core functionality tests (uniqueness, distribution, classification)
  comprehensive - Comprehensive assessment tests
  visual        - Visual pattern and consistency tests (including animal patterns)
  pdf_generation - PDF generation and formatting tests
  integration   - Full integration tests
        """,
    )

    parser.add_argument(
        "--category",
        action="append",
        choices=["core", "comprehensive", "visual", "pdf_generation", "integration"],
        help="Run tests from specific category only (can be used multiple times)",
    )

    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Verbose output with error details"
    )

    parser.add_argument(
        "--quick", "-q", action="store_true", help="Quick mode: skip slow tests"
    )

    args = parser.parse_args()

    # Create and configure test runner
    runner = TestRunner()
    runner.verbose = args.verbose

    # Run tests
    success = runner.run_tests(categories=args.category, quick=args.quick)

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
