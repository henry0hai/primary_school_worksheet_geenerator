"""
Utilities for the Primary School Worksheet Generator
Common helper functions and data
"""

import random
import string
from typing import List, Dict, Tuple


class EducationalUtils:
    """Utility class for educational content generation"""

    # Common sight words for different reading levels
    SIGHT_WORDS = {
        "basic": [
            "the",
            "and",
            "a",
            "to",
            "said",
            "in",
            "he",
            "I",
            "of",
            "it",
            "was",
            "you",
            "they",
            "she",
            "for",
            "on",
            "are",
            "as",
            "with",
            "his",
        ],
        "intermediate": [
            "there",
            "use",
            "an",
            "each",
            "which",
            "their",
            "time",
            "will",
            "about",
            "if",
            "up",
            "out",
            "many",
            "then",
            "them",
            "these",
            "so",
            "some",
            "her",
            "would",
        ],
        "advanced": [
            "make",
            "like",
            "into",
            "him",
            "has",
            "two",
            "more",
            "very",
            "what",
            "know",
            "just",
            "first",
            "get",
            "over",
            "think",
            "also",
            "your",
            "work",
            "life",
            "only",
        ],
    }

    # Simple stories for reading comprehension
    SIMPLE_STORIES = {
        "4-5": [
            "The cat sat on the mat. The cat was happy.",
            "Tom has a red ball. He likes to play with it.",
            "The dog runs in the park. The dog is fast.",
            "Mom made a cake. It smells good.",
            "The bird flies in the sky. It is blue.",
        ],
        "6-7": [
            "Emma found a lost puppy in the park. She took it home and gave it food and water. The puppy was very happy.",
            "Jack planted seeds in his garden. He watered them every day. Soon, beautiful flowers grew.",
            "The little mouse was hungry. It found some cheese in the kitchen. The mouse ate it all up.",
            "Sarah loves to read books. She goes to the library every week to find new stories.",
            "The butterfly landed on the flower. It was looking for sweet nectar to drink.",
        ],
        "8-10": [
            "Alex was nervous about his first day at a new school. When he arrived, a friendly boy named Sam showed him around. By lunch time, Alex had made three new friends and felt much better about his new school.",
            "The old oak tree in the schoolyard had been there for over 100 years. Students would sit under its shade and read books. One day, the principal decided to build a reading garden around it.",
            "Maya discovered that she had a talent for painting. She practiced every day after school. Her art teacher entered one of her paintings in a contest, and Maya won first prize.",
            "The hiking trail wound through the forest for three miles. As the children walked, they spotted rabbits, squirrels, and many different birds. Their nature guide taught them about the plants and animals they saw.",
        ],
    }

    # Logic patterns
    LOGIC_PATTERNS = {
        "shapes": ["circle", "square", "triangle", "rectangle", "star"],
        "colors": ["red", "blue", "green", "yellow", "purple", "orange"],
        "numbers": list(range(1, 21)),
        "letters": list(string.ascii_uppercase[:10]),
    }

    @staticmethod
    def generate_number_sequence(start: int, pattern: str, length: int) -> List[int]:
        """Generate a number sequence based on pattern"""
        sequence = [start]

        if pattern == "add":
            step = random.randint(2, 5)
            for i in range(1, length):
                sequence.append(sequence[-1] + step)
        elif pattern == "multiply":
            step = random.randint(2, 3)
            for i in range(1, length):
                sequence.append(sequence[-1] * step)
        elif pattern == "fibonacci":
            if length > 1:
                sequence.append(start + 1)
            for i in range(2, length):
                sequence.append(sequence[-1] + sequence[-2])

        return sequence

    @staticmethod
    def generate_pattern(pattern_type: str, length: int) -> List[str]:
        """Generate various types of patterns"""
        if pattern_type == "color":
            colors = ["red", "blue", "green"]
            pattern = []
            for i in range(length):
                pattern.append(colors[i % len(colors)])
            return pattern

        elif pattern_type == "shape":
            shapes = ["○", "□", "△"]
            pattern = []
            for i in range(length):
                pattern.append(shapes[i % len(shapes)])
            return pattern

        elif pattern_type == "size":
            sizes = ["small", "big", "small"]
            pattern = []
            for i in range(length):
                pattern.append(sizes[i % len(sizes)])
            return pattern

        return []

    @staticmethod
    def generate_word_problem_context() -> Dict[str, List[str]]:
        """Generate contexts for word problems"""
        return {
            "characters": [
                "Tom",
                "Sarah",
                "Mike",
                "Emma",
                "Jack",
                "Lily",
                "Sam",
                "Kate",
            ],
            "objects": [
                "apples",
                "toys",
                "books",
                "stickers",
                "marbles",
                "cookies",
                "pencils",
                "flowers",
            ],
            "actions": [
                "bought",
                "found",
                "collected",
                "gave away",
                "received",
                "lost",
                "counted",
            ],
            "places": [
                "store",
                "park",
                "school",
                "home",
                "library",
                "garden",
                "playground",
            ],
        }

    @staticmethod
    def create_comprehension_questions(story: str) -> List[Dict[str, str]]:
        """Create simple comprehension questions for a story"""
        # This is a simplified version - in a real implementation,
        # you might use NLP libraries or AI to generate better questions
        questions = []

        # Basic who/what/where questions
        if "cat" in story.lower():
            questions.append(
                {
                    "question": "What animal is in the story?",
                    "answer": "cat",
                    "type": "factual",
                }
            )

        if "happy" in story.lower():
            questions.append(
                {
                    "question": "How did the character feel?",
                    "answer": "happy",
                    "type": "emotional",
                }
            )

        # Add more sophisticated question generation here
        return questions

    @staticmethod
    def validate_age_appropriate_content(content: str, age_group: str) -> bool:
        """Validate that content is appropriate for age group"""
        max_lengths = {"4-5": 50, "6-7": 100, "8-10": 200}  # characters

        return len(content) <= max_lengths.get(age_group, 200)


class MathUtils:
    """Math-specific utility functions"""

    @staticmethod
    def generate_addition_problem(max_num: int) -> Tuple[int, int, int]:
        """Generate addition problem within range"""
        a = random.randint(1, max_num)
        b = (
            random.randint(1, max_num - a)
            if max_num > a
            else random.randint(1, max_num)
        )
        return a, b, a + b

    @staticmethod
    def generate_subtraction_problem(max_num: int) -> Tuple[int, int, int]:
        """Generate subtraction problem within range"""
        result = random.randint(0, max_num // 2)
        subtrahend = random.randint(1, max_num - result)
        minuend = result + subtrahend
        return minuend, subtrahend, result

    @staticmethod
    def generate_multiplication_problem(max_num: int) -> Tuple[int, int, int]:
        """Generate multiplication problem within range"""
        a = random.randint(2, min(10, max_num))
        b = random.randint(2, max_num // a) if max_num // a >= 2 else 2
        return a, b, a * b

    @staticmethod
    def generate_word_problem(operation: str, max_num: int) -> Dict[str, str]:
        """Generate a word problem"""
        context = EducationalUtils.generate_word_problem_context()
        character = random.choice(context["characters"])
        obj = random.choice(context["objects"])
        action = random.choice(context["actions"])

        if operation == "addition":
            a, b, answer = MathUtils.generate_addition_problem(max_num)
            problem = f"{character} has {a} {obj}. Then {character} {action} {b} more {obj}. How many {obj} does {character} have now?"
        elif operation == "subtraction":
            total, taken, answer = MathUtils.generate_subtraction_problem(max_num)
            problem = f"{character} had {total} {obj}. {character} {action} {taken} {obj}. How many {obj} are left?"
        elif operation == "multiplication":
            groups, per_group, answer = MathUtils.generate_multiplication_problem(
                max_num
            )
            problem = f"{character} has {groups} boxes of {obj}. Each box has {per_group} {obj}. How many {obj} does {character} have in total?"
        else:
            return {"problem": "Error generating problem", "answer": "0"}

        return {"problem": problem, "answer": str(answer)}


def format_time_estimate(num_questions: int, age_group: str) -> str:
    """Estimate completion time for worksheet"""
    base_time_per_question = {
        "4-5": 2,  # 2 minutes per question
        "6-7": 1.5,  # 1.5 minutes per question
        "8-10": 1,  # 1 minute per question
    }

    minutes = int(num_questions * base_time_per_question.get(age_group, 1.5))
    if minutes < 60:
        return f"~{minutes} minutes"
    else:
        hours = minutes // 60
        remaining_minutes = minutes % 60
        if remaining_minutes == 0:
            return f"~{hours} hour{'s' if hours > 1 else ''}"
        else:
            return f"~{hours}h {remaining_minutes}m"


def get_encouragement_message() -> str:
    """Get a random encouragement message for children"""
    messages = [
        "Great job! Keep learning and having fun! 🌟",
        "You're doing amazing! Every problem you solve makes you smarter! 🧠",
        "Fantastic work! Learning is an adventure! 🚀",
        "Excellent effort! You're becoming a problem-solving superhero! 🦸",
        "Wonderful! Your brain is growing stronger with each question! 💪",
        "Awesome job! You're on your way to becoming brilliant! ✨",
        "Super work! Keep asking questions and exploring! 🔍",
        "Marvelous! You're building amazing thinking skills! 🏗️",
    ]
    return random.choice(messages)
