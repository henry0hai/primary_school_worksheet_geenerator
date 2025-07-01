import random
from typing import List, Dict, Set
from ..data.data_loader import data_loader


class LogicGenerator:
    """Generates logic and reasoning problems for primary school children"""

    def __init__(self):
        # Load data from data source
        self.data_source = data_loader
        # Track generated questions to ensure uniqueness
        self.generated_questions: Set[str] = set()

    def reset_generated_questions(self):
        """Reset the tracking of generated questions for a new worksheet"""
        self.generated_questions.clear()

    def generate_pattern_sequence(self, age_group: str, max_attempts: int = 20) -> Dict:
        """Generate pattern completion problems"""
        # Get pattern templates from data source
        pattern_templates = self.data_source.get_pattern_templates(age_group)

        if not pattern_templates:
            return self._generate_fallback_pattern(age_group)

        for attempt in range(max_attempts):
            template = random.choice(pattern_templates)

            # Generate the pattern based on the template
            pattern_result = self._generate_pattern_from_template(template)

            if pattern_result:
                # Create unique key using the actual question text for absolute uniqueness
                question_text = pattern_result["question"]
                question_key = f"pattern_{hash(question_text)}_{age_group}"

                if question_key not in self.generated_questions:
                    self.generated_questions.add(question_key)
                    return {
                        "question": pattern_result["question"],
                        "answer": pattern_result["answer"],
                        "explanation": pattern_result["explanation"],
                        "type": "pattern",
                    }

        # Fallback if unique generation fails
        return self._generate_fallback_pattern(age_group)

    def _generate_pattern_from_template(self, template: Dict) -> Dict:
        """Generate a pattern based on a template"""
        pattern_type = template.get("type", "AB_color")

        if pattern_type.startswith("AB_"):
            return self._generate_ab_pattern(template)
        elif pattern_type.startswith("ABC_"):
            return self._generate_abc_pattern(template)
        elif pattern_type.startswith("ABCD_") or pattern_type == "ABCD_pattern":
            return self._generate_abcd_pattern(template)
        elif pattern_type == "number_sequence":
            return self._generate_number_sequence_pattern(template)
        elif pattern_type == "skip_counting" or pattern_type == "large_skip_counting":
            return self._generate_skip_counting_pattern(template)
        elif pattern_type == "growing_pattern" or pattern_type == "growing_sequence":
            return self._generate_growing_pattern(template)
        elif pattern_type == "fibonacci_like":
            return self._generate_fibonacci_pattern(template)
        elif (
            pattern_type == "complex_visual_pattern" or pattern_type == "complex_visual"
        ):
            return self._generate_complex_visual_pattern(template)
        else:
            return self._generate_ab_pattern(template)
            return self._generate_ab_pattern(template)

    def _generate_ab_pattern(self, template: Dict) -> Dict:
        """Generate a simple AB repeating pattern"""
        pattern_type = template.get("type", "AB_color")

        if pattern_type == "AB_color":
            colors = template.get("colors", [])
            if colors and len(colors) >= 2 and isinstance(colors[0], dict):
                # New visual format with symbols
                selected_colors = random.sample(colors, 2)
                items = [
                    color.get("symbol", color.get("name", "🔴"))
                    for color in selected_colors
                ]
                names = [color.get("name", "color") for color in selected_colors]
            else:
                # Fallback for old format
                items = random.sample(
                    colors or ["red", "blue"], min(2, len(colors) if colors else 2)
                )
                names = items
        elif pattern_type == "AB_shape":
            shapes = template.get("shapes", [])
            if shapes and len(shapes) >= 2 and isinstance(shapes[0], dict):
                # New visual format with symbols
                selected_shapes = random.sample(shapes, 2)
                items = [
                    shape.get("symbol", shape.get("unicode", shape.get("name", "●")))
                    for shape in selected_shapes
                ]
                names = [shape.get("name", "shape") for shape in selected_shapes]
            else:
                # Fallback for old format
                items = random.sample(
                    shapes or ["circle", "square"], min(2, len(shapes) if shapes else 2)
                )
                names = items
        elif pattern_type == "AB_animal":
            animals = template.get("animals", [])
            if animals and len(animals) >= 2 and isinstance(animals[0], dict):
                # Animal patterns with emojis
                selected_animals = random.sample(animals, 2)
                items = [
                    animal.get("symbol", animal.get("name", "🐱"))
                    for animal in selected_animals
                ]
                names = [animal.get("name", "animal") for animal in selected_animals]
            else:
                # Fallback
                items = ["🐱", "🐶"]
                names = ["cat", "dog"]
        elif pattern_type == "AB_number":
            num_range = template.get("number_range", {"min": 1, "max": 5})
            start = random.randint(num_range["min"], num_range["max"])
            items = [str(start), str(start + 1)]
            names = items
        else:
            items = ["🔴", "🔵"]  # fallback with visual symbols
            names = ["red", "blue"]

        pattern_length = template.get("pattern_length", 6)
        repeats = pattern_length // 2

        # Create the full sequence
        sequence = (items * repeats)[:pattern_length]

        # Remove the last item to create the question
        question_sequence = sequence[:-1]
        answer = sequence[-1]

        question = f"Complete the pattern: {' - '.join(question_sequence)} - ____"
        explanation = (
            f"The pattern repeats {' - '.join(items)}, so the next item is: {answer}"
        )

        # Create a more unique sequence key that includes pattern order, length, and actual sequence
        sorted_names = sorted(names)  # Sort to ensure consistent ordering
        sequence_hash = hash(
            "_".join(question_sequence)
        )  # Add sequence hash for uniqueness
        sequence_key = f"{pattern_type}_{'-'.join(sorted_names)}_{pattern_length}_{answer}_{sequence_hash}"

        return {
            "question": question,
            "answer": answer,
            "explanation": explanation,
            "sequence_key": sequence_key,
            "visual_items": items,
            "item_names": names,
        }

    def _generate_abc_pattern(self, template: Dict) -> Dict:
        """Generate an ABC repeating pattern"""
        items_data = template.get("items", {})

        # Randomly choose between colors and shapes
        if "colors" in items_data and random.choice([True, False]):
            colors = items_data["colors"]
            if colors and len(colors) >= 3 and isinstance(colors[0], dict):
                # New visual format
                selected_colors = random.sample(colors, 3)
                items = [
                    color.get("symbol", color.get("name", "🔴"))
                    for color in selected_colors
                ]
                names = [color.get("name", "color") for color in selected_colors]
            else:
                # Fallback for old format
                items = random.sample(
                    colors or ["red", "blue", "green"],
                    min(3, len(colors) if colors else 3),
                )
                names = items
        elif "shapes" in items_data:
            shapes = items_data["shapes"]
            if shapes and len(shapes) >= 3 and isinstance(shapes[0], dict):
                # New visual format
                selected_shapes = random.sample(shapes, 3)
                items = [
                    shape.get("symbol", shape.get("unicode", shape.get("name", "●")))
                    for shape in selected_shapes
                ]
                names = [shape.get("name", "shape") for shape in selected_shapes]
            else:
                # Fallback for old format
                items = random.sample(
                    shapes or ["circle", "square", "triangle"],
                    min(3, len(shapes) if shapes else 3),
                )
                names = items
        else:
            items = ["🔴", "🔵", "🟢"]  # fallback with visual symbols
            names = ["red", "blue", "green"]

        pattern_length = template.get("pattern_length", 9)
        repeats = pattern_length // 3

        # Create the full sequence
        sequence = (items * repeats)[:pattern_length]

        # Remove the last item to create the question
        question_sequence = sequence[:-1]
        answer = sequence[-1]

        question = f"Complete the pattern: {' - '.join(question_sequence)} - ____"
        explanation = (
            f"The pattern repeats {' - '.join(items)}, so the next item is: {answer}"
        )

        # Create a more unique sequence key that includes pattern order, length, and actual sequence
        sorted_names = sorted(names)  # Sort to ensure consistent ordering
        sequence_hash = hash(
            "_".join(question_sequence)
        )  # Add sequence hash for uniqueness
        sequence_key = (
            f"ABC_{'-'.join(sorted_names)}_{pattern_length}_{answer}_{sequence_hash}"
        )

        return {
            "question": question,
            "answer": answer,
            "explanation": explanation,
            "sequence_key": sequence_key,
            "visual_items": items,
            "item_names": names,
        }

    def _generate_abcd_pattern(self, template: Dict) -> Dict:
        """Generate an ABCD repeating pattern (for advanced children)"""
        items_data = template.get("items", {})

        if "shapes" in items_data:
            shapes = items_data["shapes"]
            if shapes and len(shapes) >= 4 and isinstance(shapes[0], dict):
                # New visual format
                selected_shapes = random.sample(shapes, 4)
                items = [
                    shape.get("symbol", shape.get("unicode", shape.get("name", "●")))
                    for shape in selected_shapes
                ]
                names = [shape.get("name", "shape") for shape in selected_shapes]
            else:
                # Fallback for old format
                items = random.sample(
                    shapes or ["circle", "square", "triangle", "star"],
                    min(4, len(shapes) if shapes else 4),
                )
                names = items
        else:
            items = ["🔴", "🔵", "🟢", "🟡"]  # fallback with visual symbols
            names = ["red", "blue", "green", "yellow"]

        pattern_length = template.get("pattern_length", 8)
        repeats = pattern_length // 4

        # Create the full sequence
        sequence = (items * repeats)[:pattern_length]

        # Remove the last item to create the question
        question_sequence = sequence[:-1]
        answer = sequence[-1]

        question = f"Complete the pattern: {' - '.join(question_sequence)} - ____"
        explanation = (
            f"The pattern repeats {' - '.join(items)}, so the next item is: {answer}"
        )

        # Create a more unique sequence key
        sorted_names = sorted(names)
        sequence_hash = hash("_".join(question_sequence))
        sequence_key = (
            f"ABCD_{'-'.join(sorted_names)}_{pattern_length}_{answer}_{sequence_hash}"
        )

        return {
            "question": question,
            "answer": answer,
            "explanation": explanation,
            "sequence_key": sequence_key,
            "visual_items": items,
            "item_names": names,
        }

    def _generate_complex_visual_pattern(self, template: Dict) -> Dict:
        """Generate complex visual patterns combining multiple elements"""
        visual_elements = template.get("visual_elements", {})

        # Get available colors and shapes
        colors = visual_elements.get("colors", [])
        shapes = visual_elements.get("shapes", [])
        sizes = visual_elements.get("sizes", ["small", "medium", "large"])

        if colors and shapes and len(colors) >= 2 and len(shapes) >= 2:
            # Create a pattern combining color and shape
            selected_colors = random.sample(colors, 2)
            selected_shapes = random.sample(shapes, 2)

            # Create combined items (color + shape)
            items = []
            names = []
            for i in range(2):
                color = selected_colors[i % len(selected_colors)]
                shape = selected_shapes[i % len(selected_shapes)]

                # Use shape symbol as base, could be enhanced with color info
                items.append(shape.get("symbol", shape.get("unicode", "●")))
                names.append(
                    f"{color.get('name', 'color')} {shape.get('name', 'shape')}"
                )

            pattern_length = template.get("pattern_length", 6)
            sequence = (items * (pattern_length // 2 + 1))[:pattern_length]

            question_sequence = sequence[:-1]
            answer = sequence[-1]

            question = f"Complete the pattern: {' - '.join(question_sequence)} - ____"
            explanation = f"The pattern alternates between {names[0]} and {names[1]}, so the next item is: {answer}"

            return {
                "question": question,
                "answer": answer,
                "explanation": explanation,
                "sequence_key": f"complex_visual_{hash('_'.join(question_sequence))}",
                "visual_items": items,
                "item_names": names,
            }
        else:
            # Fallback to simple pattern
            return self._generate_ab_pattern(template)

    def _generate_fibonacci_pattern(self, template: Dict) -> Dict:
        """Generate a Fibonacci-like pattern"""
        start_range = template.get("start_range", {"min": 1, "max": 3})
        a = random.randint(start_range["min"], start_range["max"])
        b = random.randint(start_range["min"] + 1, start_range["max"] + 2)

        sequence = [a, b, a + b, a + 2 * b]
        question_sequence = sequence[:-1]
        answer = str(sequence[-1])

        question = (
            f"Complete the pattern: {' - '.join(map(str, question_sequence))} - ____"
        )
        explanation = f"Each number is the sum of the previous numbers, so the next number is: {answer}"

        return {
            "question": question,
            "answer": answer,
            "explanation": explanation,
            "sequence_key": f"fib_{a}_{b}",
        }

    def _generate_number_sequence_pattern(self, template: Dict) -> Dict:
        """Generate a number sequence pattern"""
        start_range = template.get("start_range", {"min": 1, "max": 10})
        step_range = template.get("step_range", {"min": 1, "max": 5})

        start = random.randint(start_range["min"], start_range["max"])
        step = random.randint(step_range["min"], step_range["max"])
        length = template.get("sequence_length", 5)

        sequence = [start + i * step for i in range(length)]
        question_sequence = sequence[:-1]
        answer = str(sequence[-1])

        question = (
            f"Complete the pattern: {' - '.join(map(str, question_sequence))} - ____"
        )
        explanation = (
            f"The pattern increases by {step}, so the next number is: {answer}"
        )

        return {
            "question": question,
            "answer": answer,
            "explanation": explanation,
            "sequence_key": f"{start}_{step}",
        }

    def _generate_skip_counting_pattern(self, template: Dict) -> Dict:
        """Generate a skip counting pattern"""
        start_range = template.get("start_range", {"min": 1, "max": 8})
        skip_range = template.get("skip_range", {"min": 2, "max": 5})

        start = random.randint(start_range["min"], start_range["max"])
        skip = random.randint(skip_range["min"], skip_range["max"])
        length = template.get("sequence_length", 4)

        sequence = [start + i * skip for i in range(length)]
        question_sequence = sequence[:-1]
        answer = str(sequence[-1])

        question = (
            f"Complete the pattern: {' - '.join(map(str, question_sequence))} - ____"
        )
        explanation = f"The pattern skips by {skip}, so the next number is: {answer}"

        return {
            "question": question,
            "answer": answer,
            "explanation": explanation,
            "sequence_key": f"skip_{start}_{skip}",
        }

    def _generate_growing_pattern(self, template: Dict) -> Dict:
        """Generate a growing pattern (multiplication or power)"""
        start_range = template.get("start_range", {"min": 2, "max": 5})
        mult_range = template.get("multiplier_range", {"min": 2, "max": 3})

        start = random.randint(start_range["min"], start_range["max"])
        multiplier = random.randint(mult_range["min"], mult_range["max"])
        length = template.get("sequence_length", 4)

        sequence = [start * (multiplier**i) for i in range(length)]
        question_sequence = sequence[:-1]
        answer = str(sequence[-1])

        question = (
            f"Complete the pattern: {' - '.join(map(str, question_sequence))} - ____"
        )
        explanation = (
            f"The pattern multiplies by {multiplier}, so the next number is: {answer}"
        )

        return {
            "question": question,
            "answer": answer,
            "explanation": explanation,
            "sequence_key": f"grow_{start}_{multiplier}",
        }

    def _generate_fallback_pattern(self, age_group: str) -> Dict:
        """Generate a simple fallback pattern if templates are not available"""
        # Create variety based on how many pattern questions have been generated
        pattern_count = len([q for q in self.generated_questions if "pattern" in q])

        # Define different fallback patterns with more variety
        fallback_patterns = [
            # Color patterns
            (["🔴", "🔵"], "red and blue circles"),
            (["🟢", "🟡"], "green and yellow circles"),
            (["🟣", "🟠"], "purple and orange circles"),
            (["🔴", "🟢"], "red and green circles"),
            (["🔵", "🟡"], "blue and yellow circles"),
            (["🟠", "🩷"], "orange and pink circles"),
            # Shape patterns
            (["⬜", "🔺"], "square and triangle"),
            (["⭕", "⬜"], "circle and square"),
            (["🔺", "⭐"], "triangle and star"),
            (["❤️", "⭐"], "heart and star"),
            (["⬜", "❤️"], "square and heart"),
            (["⭕", "🔺"], "circle and triangle"),
            # Animal patterns
            (["🐱", "🐶"], "cat and dog"),
            (["🐮", "🐷"], "cow and pig"),
            (["🦆", "🐑"], "duck and sheep"),
            (["🐸", "🐰"], "frog and bunny"),
            # Mixed patterns
            (["🌟", "🌙"], "star and moon"),
            (["🌞", "⭐"], "sun and star"),
            (["🍎", "🍌"], "apple and banana"),
            (["🚗", "🚲"], "car and bike"),
            # Number patterns
            (["1", "2"], "numbers 1 and 2"),
            (["3", "4"], "numbers 3 and 4"),
            (["5", "6"], "numbers 5 and 6"),
            # Letter patterns
            (["A", "B"], "letters A and B"),
            (["X", "Y"], "letters X and Y"),
            (["M", "N"], "letters M and N"),
        ]

        # Select pattern based on count to ensure variety
        pattern_items, description = fallback_patterns[
            pattern_count % len(fallback_patterns)
        ]
        sequence = pattern_items * 3  # AB AB AB
        question = f"Complete the pattern: {' - '.join(sequence[:-1])} - ____"
        answer = sequence[-1]

        # Create unique tracking key
        question_key = f"pattern_fallback_{pattern_count}_{hash(question)}_{age_group}"
        self.generated_questions.add(question_key)

        return {
            "question": question,
            "answer": answer,
            "explanation": f"The pattern repeats {description}, so the next item is: {answer}",
            "type": "pattern",
        }

    def generate_classification(self, age_group: str, max_attempts: int = 10) -> Dict:
        """Generate classification and sorting problems"""
        # Get classification problems from data source
        classification_problems = self.data_source.get_classification_problems(
            age_group
        )

        if not classification_problems:
            return self._generate_fallback_classification(age_group)

        for attempt in range(max_attempts):
            problem_template = random.choice(classification_problems)

            # Generate the problem based on the template
            correct_items = random.sample(
                problem_template.get("correct_items", ["cat", "dog", "bird"]),
                min(
                    3,
                    len(problem_template.get("correct_items", ["cat", "dog", "bird"])),
                ),
            )
            wrong_item = random.choice(problem_template.get("wrong_items", ["apple"]))

            # Create unique key for this classification question
            category_name = problem_template.get("category", "animals")
            question_key = f"classification_{category_name}_{wrong_item}_{'-'.join(sorted(correct_items))}"

            if question_key not in self.generated_questions:
                self.generated_questions.add(question_key)

                items = correct_items + [wrong_item]
                random.shuffle(items)

                question = (
                    f"Which one doesn't belong with {category_name}? {', '.join(items)}"
                )
                answer = wrong_item
                explanation = problem_template.get(
                    "explanation_template",
                    f"{wrong_item} doesn't belong with {category_name}",
                ).format(item=wrong_item, category=category_name)

                return {
                    "question": question,
                    "answer": answer,
                    "explanation": explanation,
                    "type": "classification",
                }

        # Fallback if unique generation fails
        return self._generate_fallback_classification(age_group)

    def _generate_fallback_classification(self, age_group: str) -> Dict:
        """Generate a simple fallback classification if templates are not available"""
        animals = ["cat", "dog", "bird"]
        wrong_item = "apple"
        items = animals + [wrong_item]
        random.shuffle(items)

        question = f"Which one doesn't belong? {', '.join(items)}"
        answer = wrong_item
        explanation = f"{wrong_item} is not an animal"

        return {
            "question": question,
            "answer": answer,
            "explanation": explanation,
            "type": "classification",
        }

    def generate_logical_reasoning(
        self, age_group: str, max_attempts: int = 10
    ) -> Dict:
        """Generate logical reasoning problems"""
        # Get reasoning problems from data source
        reasoning_problems = self.data_source.get_reasoning_problems(age_group)

        if not reasoning_problems:
            return self._generate_fallback_reasoning(age_group)

        for attempt in range(max_attempts):
            problem = random.choice(reasoning_problems)

            # Handle different problem formats
            if "scenarios" in problem:
                # Multiple choice scenarios
                scenario = random.choice(problem["scenarios"])
                question = scenario["question"]
                answer = scenario["answer"]
                explanation = scenario.get("explanation", f"Answer: {answer}")
                # Create more unique key using hash of full question
                question_key = (
                    f"reasoning_scenario_{hash(question + answer)}_{age_group}"
                )
            else:
                # Single problem format
                question = problem["question"]
                answer = problem["answer"]
                explanation = problem.get("explanation", f"Answer: {answer}")
                # Create more unique key using hash of full question
                question_key = f"reasoning_{hash(question + answer)}_{age_group}"

            if question_key not in self.generated_questions:
                self.generated_questions.add(question_key)

                return {
                    "question": question,
                    "answer": answer,
                    "explanation": explanation,
                    "type": "logical_reasoning",
                }

        # Fallback if unique generation fails
        return self._generate_fallback_reasoning(age_group)

    def _generate_fallback_reasoning(self, age_group: str) -> Dict:
        """Generate a simple fallback reasoning problem if templates are not available"""
        # Create a unique fallback question based on current generated questions count
        question_count = len([q for q in self.generated_questions if "reasoning" in q])

        if age_group == "4-5":
            fallback_questions = [
                ("If it's raining, we use an ____", "umbrella"),
                ("What comes after Monday?", "Tuesday"),
                ("Birds can ____", "fly"),
                ("We sleep in a ____", "bed"),
                ("The sun shines during the ____", "day"),
                ("Ice is ____", "cold"),
                ("Fire is ____", "hot"),
                ("Fish live in ____", "water"),
                ("Cars drive on the ____", "road"),
                ("We eat with a ____", "fork"),
                ("Books have ____", "pages"),
                ("At night it is ____", "dark"),
                ("Snow is ____", "white"),
                ("Grass is ____", "green"),
                ("The moon comes out at ____", "night"),
            ]
        elif age_group == "6-7":
            fallback_questions = [
                (
                    "Tom is taller than Sarah. Sarah is taller than Mike. Who is the shortest?",
                    "Mike",
                ),
                (
                    "Anna finished before Ben, but after Carol. Who finished first?",
                    "Carol",
                ),
                (
                    "If all roses are flowers, and this is a rose, what is it?",
                    "a flower",
                ),
                ("There are 3 cats and 2 dogs. How many animals in total?", "5"),
                ("What day comes 2 days after Monday?", "Wednesday"),
                ("What day comes before Sunday?", "Saturday"),
                ("If you have 5 cookies and eat 2, how many are left?", "3"),
                ("What season comes after winter?", "spring"),
                ("Which is bigger: a mouse or an elephant?", "elephant"),
                ("What do we use to cut paper?", "scissors"),
                ("Where do fish swim?", "in water"),
                ("What do plants need to grow?", "water and sunlight"),
                ("How many legs does a spider have?", "8"),
                ("What color do you get when you mix red and yellow?", "orange"),
                ("Which animal says 'moo'?", "cow"),
            ]
        else:  # 8-10 years
            fallback_questions = [
                ("If today is Wednesday, what day was it 3 days ago?", "Sunday"),
                (
                    "If all birds can fly, and penguins are birds, what about penguins?",
                    "they should be able to fly (but actually can't)",
                ),
                (
                    "There are twice as many apples as oranges. If there are 4 oranges, how many apples?",
                    "8",
                ),
                ("If the pattern is A=1, B=2, C=3, what number is F?", "6"),
                (
                    "A train leaves at 2:00 PM and arrives at 5:00 PM. How long was the journey?",
                    "3 hours",
                ),
                ("If yesterday was Thursday, what day is tomorrow?", "Saturday"),
                ("What is 25% of 100?", "25"),
                ("If a dozen eggs costs $3, how much does one egg cost?", "25 cents"),
                ("What is the next prime number after 7?", "11"),
                ("How many minutes are in 2 hours?", "120"),
                ("If a rectangle has length 6 and width 4, what is its area?", "24"),
                ("What is half of half of 20?", "5"),
                (
                    "If you save $2 per week, how much will you have after 6 weeks?",
                    "$12",
                ),
                ("What is 8 × 7?", "56"),
                (
                    "If a movie starts at 7:30 PM and lasts 2 hours, when does it end?",
                    "9:30 PM",
                ),
            ]

        # Check if we've used up all available questions to avoid repeats
        if question_count >= len(fallback_questions):
            # Generate dynamic questions to avoid repetition
            question_variation = question_count % 5  # Increase variation
            if question_variation == 0:
                question = f"If it's sunny, we might need ____"
                answer = "sunglasses"
            elif question_variation == 1:
                question = f"What do we use to write?"
                answer = "a pen or pencil"
            elif question_variation == 2:
                question = f"Where do we go to learn?"
                answer = "school"
            elif question_variation == 3:
                question = f"What season has falling leaves?"
                answer = "autumn"
            else:
                question = f"What do we drink when thirsty?"
                answer = "water"

            # Add timestamp to make it even more unique
            question_key = (
                f"fallback_reasoning_{question_count}_{hash(question)}_{age_group}"
            )
        else:
            # Select from predefined questions
            question, answer = fallback_questions[
                question_count % len(fallback_questions)
            ]
            question_key = f"fallback_reasoning_{question_count}_{hash(question + answer)}_{age_group}"

        # Ensure this question hasn't been used
        if question_key in self.generated_questions:
            # Create an even more unique variant
            question = f"{question} (version {question_count})"
            question_key = f"fallback_reasoning_variant_{question_count}_{hash(question)}_{age_group}"

        self.generated_questions.add(question_key)

        return {
            "question": question,
            "answer": answer,
            "explanation": f"Answer: {answer}",
            "type": "logical_reasoning",
        }

    def _get_structured_distribution(
        self, age_group: str, count: int
    ) -> Dict[str, int]:
        """Get structured distribution of logic problem types based on age group"""
        # Define age-based percentages for different logic problem types
        distributions = {
            "4-5": {
                "pattern": 60,  # Focus on simple patterns (visual/color)
                "classification": 30,  # Simple sorting and grouping
                "reasoning": 10,  # Very basic logical thinking
            },
            "6-7": {
                "pattern": 45,  # Continue patterns but add complexity
                "classification": 35,  # More sophisticated grouping
                "reasoning": 20,  # Increased logical reasoning
            },
            "8-10": {
                "pattern": 35,  # Advanced patterns (sequences, math)
                "classification": 25,  # Complex categorization
                "reasoning": 40,  # Strong focus on logical thinking
            },
        }

        # Get the distribution for this age group (fallback to 6-7 if not found)
        age_distribution = distributions.get(age_group, distributions["6-7"])

        # Calculate actual numbers based on percentages
        distribution = {}
        total_assigned = 0

        for problem_type, percentage in age_distribution.items():
            type_count = round((percentage / 100) * count)
            distribution[problem_type] = type_count
            total_assigned += type_count

        # Adjust for rounding differences
        diff = count - total_assigned
        if diff != 0:
            # Add/remove from the most appropriate type based on age
            if age_group == "4-5":
                distribution["pattern"] += diff
            elif age_group == "6-7":
                distribution["classification"] += diff
            else:
                distribution["reasoning"] += diff

        return distribution

    def generate_problems(self, age_group: str, count: int) -> List[Dict]:
        """Generate a structured mix of logic problems for the specified age group"""
        # Reset questions tracking for each new worksheet
        self.reset_generated_questions()

        problems = []

        # Get structured distribution
        distribution = self._get_structured_distribution(age_group, count)

        print(f"🧩 Logic problem distribution for {count} questions (age {age_group}):")
        for problem_type, type_count in distribution.items():
            if type_count > 0:
                print(f"   • {problem_type.title()}: {type_count} problems")

        # Generate problems according to distribution
        for problem_type, type_count in distribution.items():
            for _ in range(type_count):
                if problem_type == "pattern":
                    problems.append(self.generate_pattern_sequence(age_group))
                elif problem_type == "classification":
                    problems.append(self.generate_classification(age_group))
                elif problem_type == "reasoning":
                    problems.append(self.generate_logical_reasoning(age_group))

        # Shuffle to mix problem types throughout the worksheet
        random.shuffle(problems)

        return problems
