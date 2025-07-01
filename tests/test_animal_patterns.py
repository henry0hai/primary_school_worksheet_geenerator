#!/usr/bin/env python3
"""
Test script to verify the enhanced visual generator with animal patterns
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(project_root))

from worksheet_generator.utils.visual_generator import VisualGenerator


def test_animal_patterns():
    """Test animal pattern generation"""
    print("Testing enhanced visual generator with animal patterns...")

    # Create visual generator
    vg = VisualGenerator()

    # Test animal emojis
    animal_emojis = ["🐱", "🐶", "🐮", "🐷", "🐑", "🦆"]

    print("\nTesting animal emoji patterns:")
    success_count = 0
    for emoji in animal_emojis:
        try:
            image_path = vg.create_pattern_images([emoji])[0]
            print(f"✅ {emoji}: {image_path}")
            success_count += 1
        except Exception as e:
            print(f"❌ {emoji}: {e}")
            return False

    # Test mixed pattern (animal + color)
    print("\nTesting mixed pattern (cat, red circle, dog, blue circle):")
    try:
        mixed_pattern = ["🐱", "🔴", "🐶", "🔵"]
        image_paths = vg.create_pattern_images(mixed_pattern)
        for i, path in enumerate(image_paths):
            print(f"  {mixed_pattern[i]}: {path}")
        print("✅ Mixed pattern generated successfully")
    except Exception as e:
        print(f"❌ Mixed pattern failed: {e}")
        return False

    # Test number patterns
    print("\nTesting number patterns:")
    try:
        number_pattern = ["1", "2", "3"]
        image_paths = vg.create_pattern_images(number_pattern)
        for i, path in enumerate(image_paths):
            print(f"  {number_pattern[i]}: {path}")
        print("✅ Number pattern generated successfully")
    except Exception as e:
        print(f"❌ Number pattern failed: {e}")
        return False

    print(
        f"\n✅ All tests passed! Successfully generated {success_count}/{len(animal_emojis)} animal patterns"
    )
    return True


if __name__ == "__main__":
    success = test_animal_patterns()
    sys.exit(0 if success else 1)
