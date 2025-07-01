import random
from typing import List, Dict, Set
from ..data.data_loader import data_loader


class ReadingGenerator:
    """Generates reading comprehension exercises for primary school children"""

    def __init__(self):
        # Load data from data source
        self.data_source = data_loader
        # Track generated questions to ensure uniqueness
        self.generated_questions: Set[str] = set()

    def reset_generated_questions(self):
        """Reset the tracking of generated questions for a new worksheet"""
        self.generated_questions.clear()

    def generate_vocabulary_exercise(
        self, age_group: str, max_attempts: int = 10
    ) -> Dict:
        """Generate vocabulary exercises"""
        # Get vocabulary exercises from data source
        vocab_exercises = self.data_source.get_vocabulary_exercises(age_group)

        if not vocab_exercises:
            return self._generate_fallback_vocabulary(age_group)

        for attempt in range(max_attempts):
            exercise = random.choice(vocab_exercises)
            word = exercise["word"]
            correct_answer = exercise.get(
                "correct_answer", exercise["choices"][0]
            )  # Use provided correct answer or first choice

            # Create unique key using sorted choices to avoid choice order issues
            choices_sorted = sorted(exercise["choices"])
            question_key = f"vocab_{word}_{correct_answer}_{hash(''.join(choices_sorted))}_{age_group}"

            if question_key not in self.generated_questions:
                self.generated_questions.add(question_key)

                choices = exercise[
                    "choices"
                ].copy()  # Make a copy to avoid modifying original
                random.shuffle(choices)

                return {
                    "question": f"Which word means the same as '{word}'? Choose from: {', '.join(choices)}",
                    "answer": correct_answer,
                    "explanation": f"'{word}' means the same as '{correct_answer}'",
                    "type": "vocabulary",
                }

        # Fallback if unique generation fails
        return self._generate_fallback_vocabulary(age_group)

    def _generate_fallback_vocabulary(self, age_group: str) -> Dict:
        """Generate a simple fallback vocabulary exercise if templates are not available"""
        # Create variety based on how many vocab questions have been generated
        vocab_count = len([q for q in self.generated_questions if "vocab" in q])

        if age_group == "4-5":
            fallback_exercises = [
                ("big", ["large", "tiny", "small"], "large"),
                ("happy", ["glad", "sad", "angry"], "glad"),
                ("fast", ["quick", "slow", "heavy"], "quick"),
                ("cold", ["freezing", "hot", "warm"], "freezing"),
                ("little", ["small", "huge", "big"], "small"),
                ("nice", ["kind", "mean", "rude"], "kind"),
                ("loud", ["noisy", "quiet", "silent"], "noisy"),
                ("soft", ["gentle", "hard", "rough"], "gentle"),
                ("dark", ["black", "bright", "light"], "black"),
                ("wet", ["damp", "dry", "warm"], "damp"),
                ("tall", ["high", "short", "low"], "high"),
                ("new", ["fresh", "old", "used"], "fresh"),
                ("clean", ["neat", "dirty", "messy"], "neat"),
                ("fun", ["enjoyable", "boring", "dull"], "enjoyable"),
                ("scary", ["frightening", "safe", "calm"], "frightening"),
            ]
        elif age_group == "6-7":
            fallback_exercises = [
                ("brave", ["courageous", "scared", "afraid"], "courageous"),
                ("smart", ["clever", "silly", "dumb"], "clever"),
                ("pretty", ["beautiful", "ugly", "plain"], "beautiful"),
                ("angry", ["mad", "happy", "calm"], "mad"),
                ("tired", ["sleepy", "awake", "energetic"], "sleepy"),
                ("funny", ["amusing", "serious", "sad"], "amusing"),
                ("difficult", ["hard", "easy", "simple"], "hard"),
                ("quiet", ["silent", "loud", "noisy"], "silent"),
                ("strange", ["weird", "normal", "usual"], "weird"),
                ("empty", ["vacant", "full", "packed"], "vacant"),
                ("strong", ["powerful", "weak", "fragile"], "powerful"),
                ("gentle", ["soft", "rough", "harsh"], "soft"),
                ("ancient", ["very old", "new", "modern"], "very old"),
                ("perfect", ["flawless", "broken", "damaged"], "flawless"),
                ("honest", ["truthful", "lying", "false"], "truthful"),
            ]
        else:  # 8-10 years
            fallback_exercises = [
                ("enormous", ["huge", "tiny", "average"], "huge"),
                ("magnificent", ["wonderful", "terrible", "ordinary"], "wonderful"),
                ("ancient", ["old", "new", "modern"], "old"),
                ("furious", ["angry", "peaceful", "calm"], "angry"),
                ("brilliant", ["smart", "stupid", "average"], "smart"),
                ("mysterious", ["puzzling", "obvious", "clear"], "puzzling"),
                ("tremendous", ["massive", "small", "medium"], "massive"),
                ("delicate", ["fragile", "strong", "tough"], "fragile"),
                ("remarkable", ["amazing", "ordinary", "boring"], "amazing"),
                ("exhausted", ["very tired", "energetic", "rested"], "very tired"),
                ("spectacular", ["impressive", "dull", "plain"], "impressive"),
                ("fortunate", ["lucky", "unlucky", "cursed"], "lucky"),
                ("essential", ["necessary", "optional", "useless"], "necessary"),
                ("abundant", ["plentiful", "scarce", "few"], "plentiful"),
                ("genuine", ["real", "fake", "artificial"], "real"),
            ]

        # Try to find an unused exercise first
        max_attempts = len(fallback_exercises) * 2  # Give it more attempts
        for attempt in range(max_attempts):
            # Select based on count but with some randomization to avoid predictable patterns
            if vocab_count < len(fallback_exercises):
                word, choices, correct_answer = fallback_exercises[
                    vocab_count % len(fallback_exercises)
                ]
            else:
                # If we've used all exercises, pick randomly but try to avoid recent ones
                word, choices, correct_answer = fallback_exercises[
                    attempt % len(fallback_exercises)
                ]

            # Create unique tracking key using sorted choices to avoid order issues
            choices_sorted = sorted(choices)
            question_key = f"vocab_fallback_{word}_{correct_answer}_{hash(''.join(choices_sorted))}_{age_group}"

            # Check if this word/answer combination has already been used
            if question_key not in self.generated_questions:
                self.generated_questions.add(question_key)

                choices_copy = choices.copy()
                random.shuffle(choices_copy)

                return {
                    "question": f"Which word means the same as '{word}'? Choose from: {', '.join(choices_copy)}",
                    "answer": correct_answer,
                    "explanation": f"'{word}' means the same as '{correct_answer}'",
                    "type": "vocabulary",
                }

        # If all attempts failed, generate a truly unique dynamic question
        # Use a timestamp-based approach to ensure uniqueness
        fallback_count = len(
            [q for q in self.generated_questions if "vocab_fallback" in q]
        )
        question_variation = fallback_count % 4
        if question_variation == 0:
            word, choices, correct_answer = (
                "good",
                ["great", "bad", "terrible"],
                "great",
            )
        elif question_variation == 1:
            word, choices, correct_answer = (
                "small",
                ["tiny", "huge", "giant"],
                "tiny",
            )
        elif question_variation == 2:
            word, choices, correct_answer = (
                "warm",
                ["hot", "cold", "freezing"],
                "hot",
            )
        else:
            word, choices, correct_answer = (
                "quick",
                ["fast", "slow", "lazy"],
                "fast",
            )

        # Create unique tracking key using sorted choices and fallback count
        choices_sorted = sorted(choices)
        question_key = f"vocab_dynamic_{word}_{correct_answer}_{fallback_count}_{hash(''.join(choices_sorted))}_{age_group}"
        self.generated_questions.add(question_key)

        choices_copy = choices.copy()
        random.shuffle(choices_copy)

        return {
            "question": f"Which word means the same as '{word}'? Choose from: {', '.join(choices_copy)}",
            "answer": correct_answer,
            "explanation": f"'{word}' means the same as '{correct_answer}'",
            "type": "vocabulary",
        }

    def generate_story_comprehension(
        self, age_group: str, max_attempts: int = 10
    ) -> Dict:
        """Generate story-based comprehension questions"""
        # Get stories from data source
        stories = self.data_source.get_stories(age_group)

        if not stories:
            return self._generate_fallback_story_comprehension(age_group)

        for attempt in range(max_attempts):
            story_data = random.choice(stories)

            # Ensure the story has questions
            if "questions" not in story_data or not story_data["questions"]:
                continue

            question_data = random.choice(story_data["questions"])

            # Handle different question formats
            if isinstance(question_data, dict):
                question_text = question_data["question"]
                answer = question_data["answer"]
            else:
                # Legacy tuple format
                question_text, answer = question_data

            # Create unique key for this question
            story_title = story_data.get("title", "Story")
            question_key = f"story_{story_title}_{question_text[:20]}"

            if question_key not in self.generated_questions:
                self.generated_questions.add(question_key)

                story_text = story_data.get("text", story_data.get("story", ""))
                full_question = f"{story_text}\n\nQuestion: {question_text}"

                return {
                    "question": full_question,
                    "answer": answer,
                    "explanation": f"The answer can be found in the story: {answer}",
                    "type": "story_comprehension",
                }

        # Fallback if unique generation fails
        return self._generate_fallback_story_comprehension(age_group)

    def _generate_fallback_story_comprehension(self, age_group: str) -> Dict:
        """Generate a simple fallback story comprehension if templates are not available"""
        story_text = "Mimi is a small black cat. She likes to play with a red ball. Every morning, Mimi drinks milk and eats fish."
        question_text = "What color is Mimi?"
        answer = "black"

        full_question = f"{story_text}\n\nQuestion: {question_text}"

        return {
            "question": full_question,
            "answer": answer,
            "explanation": f"The answer can be found in the story: {answer}",
            "type": "story_comprehension",
        }

    def generate_sentence_building(
        self, age_group: str, max_attempts: int = 10
    ) -> Dict:
        """Generate sentence building exercises"""
        # Get sentence building exercises from data source
        sentence_exercises = self.data_source.get_sentence_building_exercises(age_group)

        if not sentence_exercises:
            return self._generate_fallback_sentence_building(age_group)

        for attempt in range(max_attempts):
            exercise = random.choice(sentence_exercises)
            sentence = exercise["sentence"]

            # Create unique key using hash to handle choice order variations
            choices_sorted = sorted(
                exercise["choices"]
            )  # Sort to ensure consistent ordering
            correct_answer = exercise.get(
                "correct_answer", exercise["choices"][0]
            )  # Use provided correct answer or first option
            question_key = f"sentence_{hash(sentence + correct_answer + ''.join(choices_sorted))}_{age_group}"

            if question_key not in self.generated_questions:
                self.generated_questions.add(question_key)

                options = exercise[
                    "choices"
                ].copy()  # Make a copy to avoid modifying original
                random.shuffle(options)

                return {
                    "question": f"Complete the sentence: {sentence} Choose from: {', '.join(options)}",
                    "answer": correct_answer,
                    "explanation": f"The correct answer is '{correct_answer}'",
                    "type": "sentence_building",
                }

        # Fallback if unique generation fails
        return self._generate_fallback_sentence_building(age_group)

    def _generate_fallback_sentence_building(self, age_group: str) -> Dict:
        """Generate a simple fallback sentence building exercise if templates are not available"""
        # Create variety based on how many sentence questions have been generated
        sentence_count = len([q for q in self.generated_questions if "sentence" in q])

        if age_group == "4-5":
            fallback_exercises = [
                ("The cat is ____.", ["sleeping", "running", "eating"], "sleeping"),
                ("Birds can ____.", ["fly", "swim", "run"], "fly"),
                ("The sun is ____.", ["bright", "dark", "cold"], "bright"),
                ("Fish live in ____.", ["water", "trees", "houses"], "water"),
                ("At night, we ____.", ["sleep", "work", "play"], "sleep"),
                ("Dogs like to ____.", ["bark", "meow", "chirp"], "bark"),
                ("Flowers need ____.", ["water", "snow", "rocks"], "water"),
                ("We use our ____ to see.", ["eyes", "ears", "nose"], "eyes"),
                ("Ice is very ____.", ["cold", "hot", "warm"], "cold"),
                ("The sky is ____.", ["blue", "green", "red"], "blue"),
                ("We ____ with our feet.", ["walk", "eat", "think"], "walk"),
                ("Milk comes from a ____.", ["cow", "tree", "rock"], "cow"),
                ("We ____ our teeth.", ["brush", "wash", "comb"], "brush"),
                ("Bears like to eat ____.", ["honey", "grass", "metal"], "honey"),
                ("We wear ____ on our feet.", ["shoes", "hats", "gloves"], "shoes"),
            ]
        elif age_group == "6-7":
            fallback_exercises = [
                ("Yesterday, we ____ to the zoo.", ["went", "walked", "drove"], "went"),
                ("The book is ____ the table.", ["on", "under", "beside"], "on"),
                (
                    "She ____ her homework.",
                    ["finished", "started", "forgot"],
                    "finished",
                ),
                ("The dog ____ loudly.", ["barked", "meowed", "chirped"], "barked"),
                ("We ____ pizza for dinner.", ["ate", "cooked", "bought"], "ate"),
                (
                    "The teacher ____ the lesson.",
                    ["explained", "listened", "wrote"],
                    "explained",
                ),
                (
                    "Children ____ in the playground.",
                    ["played", "worked", "studied"],
                    "played",
                ),
                ("The car ____ down the street.", ["drove", "flew", "swam"], "drove"),
                ("We ____ our hands before eating.", ["wash", "paint", "hide"], "wash"),
                ("The bird ____ in the tree.", ["sat", "ran", "swam"], "sat"),
                ("Mom ____ dinner for us.", ["cooked", "ate", "drank"], "cooked"),
                (
                    "The student ____ the question.",
                    ["answered", "forgot", "ignored"],
                    "answered",
                ),
                (
                    "We ____ our coats when it's cold.",
                    ["wear", "remove", "wash"],
                    "wear",
                ),
                ("The baby ____ when hungry.", ["cries", "laughs", "sleeps"], "cries"),
                ("Flowers ____ in the garden.", ["grow", "swim", "fly"], "grow"),
            ]
        else:  # 8-10 years
            fallback_exercises = [
                (
                    "The scientist ____ an important discovery.",
                    ["made", "found", "achieved"],
                    "made",
                ),
                (
                    "The athlete ____ the world record.",
                    ["broke", "set", "reached"],
                    "broke",
                ),
                (
                    "The teacher ____ the lesson clearly.",
                    ["explained", "taught", "demonstrated"],
                    "explained",
                ),
                (
                    "The artist ____ a beautiful painting.",
                    ["created", "painted", "drew"],
                    "created",
                ),
                (
                    "The student ____ the difficult problem.",
                    ["solved", "answered", "completed"],
                    "solved",
                ),
                (
                    "The chef ____ a delicious meal.",
                    ["prepared", "cooked", "served"],
                    "prepared",
                ),
                (
                    "The musician ____ a wonderful concert.",
                    ["performed", "played", "gave"],
                    "performed",
                ),
                (
                    "The engineer ____ the bridge carefully.",
                    ["designed", "built", "planned"],
                    "designed",
                ),
                (
                    "The doctor ____ the patient's illness.",
                    ["diagnosed", "treated", "cured"],
                    "diagnosed",
                ),
                (
                    "The writer ____ an exciting story.",
                    ["wrote", "told", "created"],
                    "wrote",
                ),
                (
                    "The pilot ____ the airplane safely.",
                    ["landed", "flew", "controlled"],
                    "landed",
                ),
                (
                    "The gardener ____ beautiful flowers.",
                    ["grew", "planted", "watered"],
                    "grew",
                ),
                (
                    "The detective ____ the mystery.",
                    ["solved", "investigated", "discovered"],
                    "solved",
                ),
                (
                    "The architect ____ the building plans.",
                    ["drew", "designed", "created"],
                    "drew",
                ),
                (
                    "The photographer ____ amazing pictures.",
                    ["took", "captured", "shot"],
                    "took",
                ),
            ]

        # Check if we've exhausted all fallback questions
        if sentence_count >= len(fallback_exercises):
            # Generate simple dynamic questions to avoid repeats
            question_variation = sentence_count % 4
            if question_variation == 0:
                sentence, options, correct_answer = (
                    "The weather is ____.",
                    ["nice", "bad", "terrible"],
                    "nice",
                )
            elif question_variation == 1:
                sentence, options, correct_answer = (
                    "We ____ to school.",
                    ["go", "fly", "swim"],
                    "go",
                )
            elif question_variation == 2:
                sentence, options, correct_answer = (
                    "The food tastes ____.",
                    ["good", "bad", "strange"],
                    "good",
                )
            else:
                sentence, options, correct_answer = (
                    "Children like to ____.",
                    ["play", "work", "study"],
                    "play",
                )
        else:
            # Select based on count to ensure variety
            sentence, options, correct_answer = fallback_exercises[
                sentence_count % len(fallback_exercises)
            ]

        # Create unique tracking key
        question_key = f"sentence_fallback_{sentence_count}_{hash(sentence + correct_answer)}_{age_group}"
        self.generated_questions.add(question_key)

        options_copy = options.copy()
        random.shuffle(options_copy)

        return {
            "question": f"Complete the sentence: {sentence} Choose from: {', '.join(options_copy)}",
            "answer": correct_answer,
            "explanation": f"The correct answer is '{correct_answer}'",
            "type": "sentence_building",
        }

    def _get_structured_distribution(
        self, age_group: str, count: int
    ) -> Dict[str, int]:
        """Get structured distribution of reading problem types based on age group"""
        # Define age-based percentages for different reading problem types
        distributions = {
            "4-5": {
                "vocabulary": 50,  # Focus on word recognition and simple meanings
                "sentence": 35,  # Basic sentence completion
                "story": 15,  # Very short, simple stories
            },
            "6-7": {
                "vocabulary": 35,  # Continue vocabulary building
                "sentence": 30,  # More complex sentence structures
                "story": 35,  # Increased story comprehension
            },
            "8-10": {
                "vocabulary": 25,  # Advanced vocabulary
                "sentence": 25,  # Complex sentence building
                "story": 50,  # Strong focus on reading comprehension
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
                distribution["vocabulary"] += diff
            elif age_group == "6-7":
                distribution["story"] += diff
            else:
                distribution["story"] += diff  # Favor comprehension for older kids

        return distribution

    def generate_problems(self, age_group: str, count: int) -> List[Dict]:
        """Generate a structured mix of reading problems for the specified age group"""
        # Reset questions tracking for each new worksheet
        self.reset_generated_questions()

        problems = []

        # Get structured distribution
        distribution = self._get_structured_distribution(age_group, count)

        print(
            f"📚 Reading problem distribution for {count} questions (age {age_group}):"
        )
        for problem_type, type_count in distribution.items():
            if type_count > 0:
                print(f"   • {problem_type.title()}: {type_count} problems")

        # Generate problems according to distribution
        for problem_type, type_count in distribution.items():
            for _ in range(type_count):
                if problem_type == "story":
                    problems.append(self.generate_story_comprehension(age_group))
                elif problem_type == "vocabulary":
                    problems.append(self.generate_vocabulary_exercise(age_group))
                elif problem_type == "sentence":
                    problems.append(self.generate_sentence_building(age_group))

        # Shuffle to mix problem types throughout the worksheet
        random.shuffle(problems)

        return problems
