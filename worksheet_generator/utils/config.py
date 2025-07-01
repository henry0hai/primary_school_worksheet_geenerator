# Configuration file for the Primary School Worksheet Generator

# Difficulty levels for different age groups
DIFFICULTY_LEVELS = {
    "4-5": {
        "math": {
            "max_number": 10,
            "operations": ["addition", "subtraction"],
            "word_problems": True,
            "simple_shapes": True,
        },
        "logic": {"pattern_length": 3, "simple_sequences": True, "basic_sorting": True},
        "reading": {
            "word_length": 4,
            "sentence_length": 8,
            "vocabulary_level": "basic",
        },
    },
    "6-7": {
        "math": {
            "max_number": 20,
            "operations": ["addition", "subtraction", "simple_multiplication"],
            "word_problems": True,
            "geometry": True,
        },
        "logic": {
            "pattern_length": 4,
            "sequences": True,
            "categorization": True,
            "simple_puzzles": True,
        },
        "reading": {
            "word_length": 6,
            "sentence_length": 12,
            "vocabulary_level": "intermediate",
            "comprehension": True,
        },
    },
    "8-10": {
        "math": {
            "max_number": 100,
            "operations": ["addition", "subtraction", "multiplication", "division"],
            "word_problems": True,
            "geometry": True,
            "fractions": True,
        },
        "logic": {
            "pattern_length": 5,
            "complex_sequences": True,
            "problem_solving": True,
            "reasoning": True,
        },
        "reading": {
            "word_length": 8,
            "sentence_length": 20,
            "vocabulary_level": "advanced",
            "comprehension": True,
            "inference": True,
        },
    },
}

# Subject distribution for comprehensive assessments
COMPREHENSIVE_DISTRIBUTION = {
    "4-5": {"math": 0.4, "logic": 0.3, "reading": 0.3},
    "6-7": {"math": 0.35, "logic": 0.35, "reading": 0.3},
    "8-10": {"math": 0.4, "logic": 0.3, "reading": 0.3},
}

# Visual settings
VISUAL_SETTINGS = {
    "colors": ["red", "blue", "green", "yellow", "purple", "orange"],
    "shapes": ["circle", "square", "triangle", "star", "heart"],
    "image_size": (100, 100),  # pixels
    "pattern_spacing": 10,
}

# PDF settings
PDF_SETTINGS = {
    "page_size": "A4",
    "margins": {"top": 72, "bottom": 72, "left": 72, "right": 72},
    "font_sizes": {"title": 24, "subtitle": 16, "question": 12, "answer": 12},
    "colors": {"title": "darkblue", "subtitle": "darkgreen"},
}
