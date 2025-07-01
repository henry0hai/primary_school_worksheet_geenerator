#!/usr/bin/env python3
"""
Data Source Loader for Primary School Worksheet Generator
Loads content templates and configurations from JSON files
"""

import json
import os
import glob
from typing import Dict, List, Any
import random


class DataSourceLoader:
    """Utility class to load and manage content from data_source folder"""

    def __init__(self, data_source_path: str = "data_source"):
        """Initialize the data loader

        Args:
            data_source_path: Path to the data_source directory
        """
        self.data_source_path = data_source_path
        self._cache = {}
        self._load_all_sources()

    def _load_all_sources(self):
        """Load all JSON files from the data_source directory"""
        print("📁 Loading data sources...")

        # Load math sources
        math_path = os.path.join(self.data_source_path, "math_source")
        self._cache["math"] = self._load_source_directory(math_path)

        # Load logic sources
        logic_path = os.path.join(self.data_source_path, "logic_source")
        self._cache["logic"] = self._load_source_directory(logic_path)

        # Load reading sources
        reading_path = os.path.join(self.data_source_path, "reading_source")
        self._cache["reading"] = self._load_source_directory(reading_path)

        print(f"✅ Loaded data sources: {list(self._cache.keys())}")

    def _load_source_directory(self, directory_path: str) -> Dict[str, Any]:
        """Load all JSON files from a directory

        Args:
            directory_path: Path to the source directory

        Returns:
            Dict containing all loaded JSON data
        """
        sources = {}

        if not os.path.exists(directory_path):
            print(f"⚠️  Directory not found: {directory_path}")
            return sources

        json_files = glob.glob(os.path.join(directory_path, "*.json"))

        for json_file in json_files:
            filename = os.path.basename(json_file).replace(".json", "")
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    sources[filename] = data
                    print(f"  📄 Loaded {filename}.json")
            except Exception as e:
                print(f"  ❌ Failed to load {json_file}: {e}")

        return sources

    def get_math_source(self, source_name: str = None) -> Dict[str, Any]:
        """Get math source data

        Args:
            source_name: Specific source file name (without .json), or None for all

        Returns:
            Math source data
        """
        if source_name:
            return self._cache.get("math", {}).get(source_name, {})
        return self._cache.get("math", {})

    def get_logic_source(self, source_name: str = None) -> Dict[str, Any]:
        """Get logic source data

        Args:
            source_name: Specific source file name (without .json), or None for all

        Returns:
            Logic source data
        """
        if source_name:
            return self._cache.get("logic", {}).get(source_name, {})
        return self._cache.get("logic", {})

    def get_reading_source(self, source_name: str = None) -> Dict[str, Any]:
        """Get reading source data

        Args:
            source_name: Specific source file name (without .json), or None for all

        Returns:
            Reading source data
        """
        if source_name:
            return self._cache.get("reading", {}).get(source_name, {})
        return self._cache.get("reading", {})

    def get_word_problems(self, operation: str, age_group: str) -> List[Dict[str, Any]]:
        """Get word problems for a specific operation and age group

        Args:
            operation: Math operation (addition, subtraction, multiplication, division)
            age_group: Target age group (4-5, 6-7, 8-10)

        Returns:
            List of matching word problem templates
        """
        word_problems = self.get_math_source("word_problems")
        problems = word_problems.get("word_problems", {}).get(operation, [])

        # Filter by age group
        filtered_problems = []
        for problem in problems:
            if age_group in problem.get("age_groups", []):
                filtered_problems.append(problem)

        return filtered_problems

    def get_operation_settings(self, age_group: str) -> Dict[str, Any]:
        """Get operation settings for an age group

        Args:
            age_group: Target age group (4-5, 6-7, 8-10)

        Returns:
            Operation settings for the age group
        """
        settings = self.get_math_source("operation_settings")
        return settings.get("operation_settings", {}).get(age_group, {})

    def get_operation_settings_with_ranges(self, age_group: str) -> Dict[str, Any]:
        """Get operation settings combined with number ranges for an age group

        Args:
            age_group: Target age group (4-5, 6-7, 8-10)

        Returns:
            Operation settings with number ranges included
        """
        settings_data = self.get_math_source("operation_settings")
        operation_settings = settings_data.get("operation_settings", {}).get(
            age_group, {}
        )
        number_ranges = settings_data.get("number_ranges", {}).get(
            age_group, {"min": 1, "max": 20}
        )

        # Combine settings with number ranges
        combined_settings = operation_settings.copy()
        combined_settings["number_range"] = number_ranges

        return combined_settings

    def get_stories(
        self, age_group: str, story_type: str = None
    ) -> List[Dict[str, Any]]:
        """Get stories for a specific age group

        Args:
            age_group: Target age group (4-5, 6-7, 8-10)
            story_type: Type of stories (simple, intermediate, advanced) or None for auto-detect

        Returns:
            List of stories suitable for the age group
        """
        # Auto-detect story type based on age group
        if story_type is None:
            if age_group == "4-5":
                story_type = "simple"
            elif age_group == "6-7":
                story_type = "intermediate"
            else:  # 8-10
                story_type = "advanced"

        story_source_name = f"{story_type}_stories"
        stories_data = self.get_reading_source(story_source_name)

        # Handle different JSON structures
        if story_type + "_stories" in stories_data:
            return stories_data[story_type + "_stories"]
        elif "stories" in stories_data:
            return stories_data["stories"]
        else:
            return list(stories_data.values())[0] if stories_data else []

    def get_vocabulary_exercises(self, age_group: str) -> List[Dict[str, Any]]:
        """Get vocabulary exercises for an age group

        Args:
            age_group: Target age group (4-5, 6-7, 8-10)

        Returns:
            List of vocabulary exercises
        """
        vocab_data = self.get_reading_source("vocabulary_exercises")
        return vocab_data.get("vocabulary_exercises", {}).get(age_group, [])

    def get_sentence_building_exercises(self, age_group: str) -> List[Dict[str, Any]]:
        """Get sentence building exercises for an age group

        Args:
            age_group: Target age group (4-5, 6-7, 8-10)

        Returns:
            List of sentence building exercises
        """
        vocab_data = self.get_reading_source("vocabulary_exercises")
        return vocab_data.get("sentence_building", {}).get(age_group, [])

    def get_pattern_templates(self, age_group: str) -> List[Dict[str, Any]]:
        """Get pattern templates for an age group

        Args:
            age_group: Target age group (4-5, 6-7, 8-10)

        Returns:
            List of pattern templates
        """
        patterns_data = self.get_logic_source("patterns")
        pattern_templates = patterns_data.get("pattern_templates", {})

        if age_group == "4-5":
            return pattern_templates.get("4-5", {}).get("simple_patterns", [])
        elif age_group == "6-7":
            return pattern_templates.get("6-7", {}).get("intermediate_patterns", [])
        else:  # 8-10
            return pattern_templates.get("8-10", {}).get("advanced_patterns", [])

    def get_classification_problems(self, age_group: str) -> List[Dict[str, Any]]:
        """Get classification problems for an age group

        Args:
            age_group: Target age group (4-5, 6-7, 8-10)

        Returns:
            List of classification problems
        """
        classification_data = self.get_logic_source("classification")
        problems = classification_data.get("classification_problems", {})

        if age_group == "4-5":
            return problems.get("4-5", {}).get("simple_categories", [])
        elif age_group == "6-7":
            return problems.get("6-7", {}).get("intermediate_categories", [])
        else:  # 8-10
            return problems.get("8-10", {}).get("advanced_categories", [])

    def get_reasoning_problems(self, age_group: str) -> List[Dict[str, Any]]:
        """Get reasoning problems for an age group

        Args:
            age_group: Target age group (4-5, 6-7, 8-10)

        Returns:
            List of reasoning problems
        """
        reasoning_data = self.get_logic_source("reasoning")
        problems = reasoning_data.get("reasoning_problems", {})

        if age_group == "4-5":
            return problems.get("4-5", {}).get("simple_logic", [])
        elif age_group == "6-7":
            return problems.get("6-7", {}).get("simple_deduction", [])
        else:  # 8-10
            return problems.get("8-10", {}).get("complex_reasoning", [])

    def reload_sources(self):
        """Reload all data sources from files"""
        self._cache.clear()
        self._load_all_sources()

    def get_random_item(self, items: List[Any]) -> Any:
        """Get a random item from a list

        Args:
            items: List of items to choose from

        Returns:
            Random item from the list
        """
        return random.choice(items) if items else None

    def get_cache_info(self) -> Dict[str, Any]:
        """Get information about loaded cache

        Returns:
            Dictionary with cache statistics
        """
        info = {}
        for subject, sources in self._cache.items():
            info[subject] = {
                "source_files": list(sources.keys()),
                "total_files": len(sources),
            }
        return info


# Global instance for easy access
data_loader = DataSourceLoader()
