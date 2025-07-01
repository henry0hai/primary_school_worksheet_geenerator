#!/usr/bin/env python3
"""
Test script to verify the fixed classification logic
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(project_root))

from worksheet_generator.core.logic_generator import LogicGenerator


def test_classification():
    """Test classification problem generation"""
    print("Testing classification problem generation...")

    # Create logic generator
    lg = LogicGenerator()

    # Test classification for different age groups
    age_groups = ["4-5", "6-7", "8-10"]

    total_tests = 0
    successful_tests = 0

    for age_group in age_groups:
        print(f"\n🧩 Testing classification for age group {age_group}:")

        # Generate several classification problems to see the variety
        for i in range(3):
            total_tests += 1
            try:
                problem = lg.generate_classification(age_group)
                print(f"  Question {i+1}: {problem['question']}")
                print(f"  Answer: {problem['answer']}")
                print(f"  Explanation: {problem['explanation']}")

                # Validate the question format
                if "doesn't belong with" in problem["question"] and problem["answer"]:
                    successful_tests += 1
                    print(f"  ✅ Valid classification question")
                else:
                    print(f"  ❌ Invalid question format")
                    return False

                print()
            except Exception as e:
                print(f"  ❌ Error generating problem {i+1}: {e}")
                return False

    print(
        f"✅ All tests passed! Successfully generated {successful_tests}/{total_tests} classification problems"
    )
    return True


if __name__ == "__main__":
    success = test_classification()
    sys.exit(0 if success else 1)
