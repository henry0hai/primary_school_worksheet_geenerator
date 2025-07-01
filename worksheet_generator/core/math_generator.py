import random
from typing import List, Dict, Tuple, Set
from ..data.data_loader import data_loader


class MathGenerator:
    """Generates math problems suitable for primary school children (4-10 years old)"""

    def __init__(self):
        # Load age group configurations from data source
        self.data_source = data_loader
        # Track generated questions to ensure uniqueness
        self.generated_questions: Set[str] = set()

    def generate_addition(
        self, max_num: int, simple: bool = False, max_attempts: int = 10
    ) -> Dict:
        """Generate addition problems"""
        for attempt in range(max_attempts):
            if simple:
                # For younger kids: single digit + single digit <= 10
                a = random.randint(1, min(5, max_num))
                b = random.randint(1, min(10 - a, max_num))
            else:
                a = random.randint(1, max_num)
                b = random.randint(1, max_num)

            question_key = f"add_{a}_{b}"
            if question_key not in self.generated_questions:
                self.generated_questions.add(question_key)
                return {
                    "question": f"{a} + {b} = ____",
                    "answer": a + b,
                    "explanation": f"{a} + {b} = {a + b}",
                    "type": "addition",
                }

        # If we couldn't generate unique question, return a random one
        a = random.randint(1, max_num)
        b = random.randint(1, max_num)
        return {
            "question": f"{a} + {b} = ____",
            "answer": a + b,
            "explanation": f"{a} + {b} = {a + b}",
            "type": "addition",
        }

    def generate_subtraction(
        self, max_num: int, simple: bool = False, max_attempts: int = 10
    ) -> Dict:
        """Generate subtraction problems"""
        for attempt in range(max_attempts):
            if simple:
                # Ensure positive results for younger kids
                a = random.randint(5, min(10, max_num))
                b = random.randint(1, a)
            else:
                a = random.randint(10, max_num)
                b = random.randint(1, a)

            question_key = f"sub_{a}_{b}"
            if question_key not in self.generated_questions:
                self.generated_questions.add(question_key)
                return {
                    "question": f"{a} - {b} = ____",
                    "answer": a - b,
                    "explanation": f"{a} - {b} = {a - b}",
                    "type": "subtraction",
                }

        # Fallback if unique generation fails
        a = random.randint(10, max_num)
        b = random.randint(1, a)
        return {
            "question": f"{a} - {b} = ____",
            "answer": a - b,
            "explanation": f"{a} - {b} = {a - b}",
            "type": "subtraction",
        }

    def generate_multiplication(
        self, max_num: int, simple: bool = False, max_attempts: int = 10
    ) -> Dict:
        """Generate multiplication problems"""
        for attempt in range(max_attempts):
            if simple:
                # Tables of 2, 3, 5, 10 for beginners
                tables = [2, 3, 5, 10]
                a = random.choice(tables)
                b = random.randint(1, 10)
            else:
                a = random.randint(2, min(12, max_num))
                b = random.randint(2, min(12, max_num))

            question_key = f"mul_{a}_{b}"
            if question_key not in self.generated_questions:
                self.generated_questions.add(question_key)
                return {
                    "question": f"{a} × {b} = ____",
                    "answer": a * b,
                    "explanation": f"{a} × {b} = {a * b}",
                    "type": "multiplication",
                }

        # Fallback
        a = random.randint(2, min(12, max_num))
        b = random.randint(2, min(12, max_num))
        return {
            "question": f"{a} × {b} = ____",
            "answer": a * b,
            "explanation": f"{a} × {b} = {a * b}",
            "type": "multiplication",
        }

    def generate_division(
        self, max_num: int, simple: bool = False, max_attempts: int = 10
    ) -> Dict:
        """Generate division problems with whole number results"""
        for attempt in range(max_attempts):
            if simple:
                # Simple division with small numbers
                b = random.randint(2, 5)
                result = random.randint(2, 10)
                a = b * result
            else:
                b = random.randint(2, 12)
                result = random.randint(2, max_num // b)
                a = b * result

            question_key = f"div_{a}_{b}"
            if question_key not in self.generated_questions:
                self.generated_questions.add(question_key)
                return {
                    "question": f"{a} ÷ {b} = ____",
                    "answer": result,
                    "explanation": f"{a} ÷ {b} = {result}",
                    "type": "division",
                }

        # Fallback
        b = random.randint(2, 12)
        result = random.randint(2, max_num // b)
        a = b * result
        return {
            "question": f"{a} ÷ {b} = ____",
            "answer": result,
            "explanation": f"{a} ÷ {b} = {result}",
            "type": "division",
        }

    def generate_word_problem(self, age_group: str, max_attempts: int = 10) -> Dict:
        """Generate word problems appropriate for age group"""
        # Get operation settings combined with number ranges for this age group
        combined_settings = self.data_source.get_operation_settings_with_ranges(
            age_group
        )
        number_range = combined_settings.get("number_range", {"min": 1, "max": 20})
        max_num = number_range["max"]

        # Get all word problem templates for different operations
        all_templates = []
        for operation in ["addition", "subtraction", "multiplication", "division"]:
            templates = self.data_source.get_word_problems(operation, age_group)
            for template in templates:
                template["operation"] = operation
                all_templates.append(template)

        if not all_templates:
            # Fallback if no templates found
            return self._generate_fallback_word_problem(age_group, max_num)

        for attempt in range(max_attempts):
            template_data = random.choice(all_templates)

            # Generate numbers based on template constraints
            values = self._generate_numbers_for_template(template_data, max_num)

            # Create a unique key for this word problem
            if (
                template_data["operation"] == "division"
                and "total" in template_data["template"]
            ):
                question_key = (
                    f"word_{template_data['operation']}_{values['total']}_{values['b']}"
                )
            else:
                question_key = (
                    f"word_{template_data['operation']}_{values['a']}_{values['b']}"
                )

            if question_key not in self.generated_questions:
                self.generated_questions.add(question_key)

                # Calculate answer based on operation
                if (
                    template_data["operation"] == "division"
                    and "total" in template_data["template"]
                ):
                    answer = values["total"] // values["b"]
                else:
                    answer = self._calculate_answer(
                        template_data["operation"], values["a"], values["b"]
                    )

                # Format the question
                question = template_data["template"].format(**values)

                return {
                    "question": question,
                    "answer": answer,
                    "explanation": f"Answer: {answer}",
                    "type": "word_problem",
                }

        # Fallback if unique generation fails
        template_data = random.choice(all_templates)
        values = self._generate_numbers_for_template(template_data, max_num)

        if (
            template_data["operation"] == "division"
            and "total" in template_data["template"]
        ):
            answer = values["total"] // values["b"]
        else:
            answer = self._calculate_answer(
                template_data["operation"], values["a"], values["b"]
            )

        question = template_data["template"].format(**values)

        return {
            "question": question,
            "answer": answer,
            "explanation": f"Answer: {answer}",
            "type": "word_problem",
        }

    def _generate_numbers_for_template(
        self, template_data: Dict, max_num: int
    ) -> Dict[str, int]:
        """Generate appropriate numbers for a word problem template"""
        setup = template_data.get("setup", {})
        operation = template_data["operation"]

        # Handle division problems with {total} placeholder
        if operation == "division" and "total" in template_data["template"]:
            # For division problems: total = b * result, where result is the answer
            b_constraints = setup.get("b", {"min": 2, "max": 8})
            result_constraints = setup.get("result", {"min": 2, "max": 12})

            b = random.randint(b_constraints["min"], min(b_constraints["max"], max_num))
            result = random.randint(
                result_constraints["min"], min(result_constraints["max"], max_num)
            )
            total = b * result

            return {
                "total": total,
                "b": b,
                "result": result,
                "a": total,
            }  # a=total for compatibility

        # Handle regular problems with {a} and {b}
        else:
            a_constraints = setup.get("a", {"min": 1, "max": max_num})
            b_constraints = setup.get("b", {"min": 1, "max": max_num})

            a_min = a_constraints["min"]
            a_max = min(a_constraints["max"], max_num)
            b_min = b_constraints["min"]
            b_max = min(b_constraints["max"], max_num)

            # For subtraction, ensure a is large enough to accommodate b_min
            if operation == "subtraction":
                a_min = max(a_min, b_min)  # Ensure a is at least as large as b_min

            a = random.randint(a_min, a_max)

            # For subtraction, ensure b <= a for positive results
            if operation == "subtraction":
                b_max = min(b_max, a)

            b = random.randint(b_min, b_max)

            return {"a": a, "b": b}

    def _calculate_answer(self, operation: str, a: int, b: int) -> int:
        """Calculate the answer based on the operation"""
        if operation == "addition":
            return a + b
        elif operation == "subtraction":
            return a - b
        elif operation == "multiplication":
            return a * b
        elif operation == "division":
            return a // b
        else:
            return a + b  # default to addition

    def _generate_fallback_word_problem(self, age_group: str, max_num: int) -> Dict:
        """Generate a simple fallback word problem if templates are not available"""
        a = random.randint(1, max_num // 2)
        b = random.randint(1, max_num // 2)

        return {
            "question": f"Sarah has {a} apples. Her friend gives her {b} more apples. How many apples does Sarah have now?",
            "answer": a + b,
            "explanation": f"Answer: {a + b}",
            "type": "word_problem",
        }

    def reset_generated_questions(self):
        """Reset the tracking of generated questions for a new worksheet"""
        self.generated_questions.clear()

    def _get_structured_distribution(
        self, age_group: str, count: int
    ) -> Dict[str, int]:
        """Get structured distribution of problem types based on age group and count"""

        if age_group == "4-5":
            # Focus on basic addition and simple concepts
            base_distribution = {
                "addition": 0.50,  # 50% addition (most important)
                "subtraction": 0.25,  # 25% subtraction (simpler)
                "word": 0.25,  # 25% word problems (context)
            }
        elif age_group == "6-7":
            # Balanced introduction to operations
            base_distribution = {
                "addition": 0.30,  # 30% addition
                "subtraction": 0.25,  # 25% subtraction
                "multiplication": 0.15,  # 15% multiplication (introduction)
                "word": 0.30,  # 30% word problems (more context)
            }
        else:  # 8-10 years
            # Full spectrum of operations
            base_distribution = {
                "addition": 0.20,  # 20% addition
                "subtraction": 0.20,  # 20% subtraction
                "multiplication": 0.25,  # 25% multiplication (focus)
                "division": 0.15,  # 15% division
                "word": 0.20,  # 20% word problems
            }

        # Convert percentages to actual counts
        distribution = {}
        total_assigned = 0

        for problem_type, percentage in base_distribution.items():
            assigned_count = round(count * percentage)
            distribution[problem_type] = assigned_count
            total_assigned += assigned_count

        # Adjust for rounding differences
        diff = count - total_assigned
        if diff != 0:
            # Add/remove from the most appropriate type
            if age_group == "4-5":
                distribution["addition"] += diff
            elif age_group == "6-7":
                distribution["word"] += diff
            else:
                distribution["multiplication"] += diff

        return distribution

    def generate_problems(self, age_group: str, count: int) -> List[Dict]:
        """Generate a structured mix of math problems for the specified age group"""
        # Get operation settings combined with number ranges for this age group
        combined_settings = self.data_source.get_operation_settings_with_ranges(
            age_group
        )
        if not combined_settings:
            raise ValueError(f"Age group {age_group} not supported")

        # Reset questions tracking for each new worksheet
        self.reset_generated_questions()

        problems = []
        number_range = combined_settings.get("number_range", {"min": 1, "max": 20})
        max_num = number_range["max"]

        # Get structured distribution
        distribution = self._get_structured_distribution(age_group, count)

        print(f"📊 Math problem distribution for {count} questions (age {age_group}):")
        for problem_type, type_count in distribution.items():
            if type_count > 0:
                print(f"   • {problem_type.title()}: {type_count} problems")

        # Generate problems according to distribution
        for problem_type, type_count in distribution.items():
            for _ in range(type_count):
                if problem_type == "addition":
                    simple = age_group == "4-5"
                    problems.append(self.generate_addition(max_num, simple=simple))
                elif problem_type == "subtraction":
                    simple = age_group in ["4-5", "6-7"]
                    problems.append(self.generate_subtraction(max_num, simple=simple))
                elif problem_type == "multiplication":
                    simple = True  # Keep multiplication simple for all ages
                    problems.append(
                        self.generate_multiplication(max_num, simple=simple)
                    )
                elif problem_type == "division":
                    simple = True  # Keep division simple
                    problems.append(self.generate_division(max_num, simple=simple))
                elif problem_type == "word":
                    problems.append(self.generate_word_problem(age_group))

        # Shuffle to mix problem types throughout the worksheet
        random.shuffle(problems)

        return problems
