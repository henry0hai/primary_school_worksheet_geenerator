from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Table,
    TableStyle,
    Image as ReportLabImage,
    Flowable,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import os
import tempfile
import re
from typing import List, Dict

try:
    from ..utils.visual_generator import visual_generator

    VISUAL_AVAILABLE = True
except ImportError:
    VISUAL_AVAILABLE = False


class VisualPatternFlowable(Flowable):
    """Custom flowable for displaying visual patterns with images"""

    def __init__(self, question_text: str, image_paths: List[str]):
        self.question_text = question_text
        self.image_paths = image_paths
        self.image_size = 30  # Size in points
        self.spacing = 10  # Spacing between images

    def draw(self):
        """Draw the visual pattern"""
        canvas = self.canv

        # Calculate total width needed
        total_width = (
            len(self.image_paths) * (self.image_size + self.spacing) - self.spacing
        )

        # Start position (centered)
        start_x = (self.width - total_width) / 2

        # Draw images in a row
        x = start_x
        y = 5  # Small offset from bottom

        for image_path in self.image_paths:
            if os.path.exists(image_path):
                try:
                    canvas.drawImage(
                        image_path,
                        x,
                        y,
                        width=self.image_size,
                        height=self.image_size,
                        preserveAspectRatio=True,
                    )
                except:
                    # If image fails, draw a placeholder circle
                    canvas.circle(x + self.image_size / 2, y + self.image_size / 2, 10)

            x += self.image_size + self.spacing

        # Add "- ____" at the end for the missing pattern item
        canvas.drawString(x, y + self.image_size / 2, "- ____")

    def wrap(self, availWidth, availHeight):
        """Return the space needed by this flowable"""
        self.width = availWidth
        return (availWidth, self.image_size + 20)  # Height includes padding


class PDFGenerator:
    """Generates beautiful PDF worksheets from exercise data"""

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Setup custom styles for the PDF"""
        # Title style
        self.title_style = ParagraphStyle(
            "CustomTitle",
            parent=self.styles["Heading1"],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue,
        )

        # Subtitle style
        self.subtitle_style = ParagraphStyle(
            "CustomSubtitle",
            parent=self.styles["Heading2"],
            fontSize=16,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=colors.darkgreen,
        )

        # Question style
        self.question_style = ParagraphStyle(
            "Question",
            parent=self.styles["Normal"],
            fontSize=12,
            spaceAfter=15,
            spaceBefore=10,
            leftIndent=20,
        )

        # Story style for reading comprehension
        self.story_style = ParagraphStyle(
            "Story",
            parent=self.styles["Normal"],
            fontSize=11,
            spaceAfter=15,
            spaceBefore=10,
            alignment=TA_JUSTIFY,
            leftIndent=20,
            rightIndent=20,
            borderWidth=1,
            borderColor=colors.lightgrey,
            borderPadding=10,
        )

        # Answer line style
        self.answer_style = ParagraphStyle(
            "Answer",
            parent=self.styles["Normal"],
            fontSize=12,
            spaceAfter=20,
            leftIndent=40,
        )

    def _create_header(self, subject: str, age_group: str, student_name: str = ""):
        """Create the worksheet header"""
        elements = []

        # Main title
        if subject == "comprehensive":
            title_text = "Comprehensive Assessment"
        else:
            title_text = f"{subject.title()} Practice Worksheet"
        elements.append(Paragraph(title_text, self.title_style))

        # Subtitle with age group
        subtitle_text = f"For Ages {age_group}"
        elements.append(Paragraph(subtitle_text, self.subtitle_style))

        # Student info section
        date_str = datetime.now().strftime("%B %d, %Y")
        info_data = [
            [
                "Student Name:",
                f"__{student_name}__" if student_name else "________________________",
            ],
            ["Date:", f"__{date_str}__"],
            ["Score:", "_____ / _____"],
        ]

        info_table = Table(info_data, colWidths=[2 * inch, 3 * inch])
        info_table.setStyle(
            TableStyle(
                [
                    ("FONTSIZE", (0, 0), (-1, -1), 12),
                    ("ALIGN", (0, 0), (0, -1), "RIGHT"),
                    ("ALIGN", (1, 0), (1, -1), "LEFT"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ]
            )
        )

        elements.append(Spacer(1, 20))
        elements.append(info_table)
        elements.append(Spacer(1, 30))

        return elements

    def _format_math_problems(self, problems: List[Dict]) -> List:
        """Format math problems for PDF"""
        elements = []

        for i, problem in enumerate(problems, 1):
            # Question number and text with emoji conversion
            question_text = f"{i}. {self._convert_emoji_to_text(problem['question'])}"
            elements.append(Paragraph(question_text, self.question_style))

            # Answer space
            if problem["type"] == "word_problem":
                # More space for word problems
                answer_space = "Answer: " + "_" * 50
                elements.append(Paragraph(answer_space, self.answer_style))
                elements.append(Spacer(1, 10))
            else:
                # Regular answer line
                elements.append(Spacer(1, 20))

        return elements

    def _format_logic_problems(self, problems: List[Dict]) -> List:
        """Format logic problems for PDF with visual elements"""
        elements = []

        for i, problem in enumerate(problems, 1):
            # Check if this is a visual pattern problem
            if (
                problem.get("type") == "pattern"
                and "Complete the pattern:" in problem["question"]
                and VISUAL_AVAILABLE
            ):

                # Try to create visual pattern
                try:
                    # Extract pattern items from the question text
                    pattern_items = self._extract_pattern_items_from_question(
                        problem["question"]
                    )

                    if pattern_items:
                        # Generate images for the pattern items
                        image_paths = visual_generator.create_pattern_images(
                            pattern_items
                        )

                        # Create question number
                        question_num = Paragraph(
                            f"{i}. Complete the pattern:", self.question_style
                        )
                        elements.append(question_num)

                        # Add visual pattern flowable
                        visual_pattern = VisualPatternFlowable(
                            problem["question"], image_paths
                        )
                        elements.append(visual_pattern)

                        # Answer space
                        answer_space = "Answer: " + "_" * 40
                        elements.append(Paragraph(answer_space, self.answer_style))
                        continue

                except Exception as e:
                    # Fall back to text conversion if visual fails
                    pass

            # Standard text-based formatting (with emoji conversion)
            question_text = f"{i}. {self._convert_emoji_to_text(problem['question'])}"
            elements.append(Paragraph(question_text, self.question_style))

            # Answer space
            answer_space = "Answer: " + "_" * 40
            elements.append(Paragraph(answer_space, self.answer_style))

        return elements

    def _extract_pattern_items_from_question(self, question: str) -> List[str]:
        """Extract pattern items from a question text"""
        # Pattern: "Complete the pattern: item1 - item2 - item3 - ____"
        if "Complete the pattern:" not in question:
            return []

        # Extract the pattern part after the colon
        pattern_part = question.split("Complete the pattern:")[1].strip()

        # Remove the "____" placeholder at the end
        pattern_part = pattern_part.replace(" - ____", "").strip()

        # Split by " - " to get individual items
        items = [item.strip() for item in pattern_part.split(" - ")]

        # Filter out empty items
        items = [item for item in items if item]

        return items

    def _format_reading_problems(self, problems: List[Dict]) -> List:
        """Format reading problems for PDF"""
        elements = []
        question_num = 1

        for problem in problems:
            if problem["type"] == "comprehension":
                # Story title and text
                story_title = f"<b>{problem['story_title']}</b>"
                elements.append(Paragraph(story_title, self.subtitle_style))
                elements.append(
                    Paragraph(
                        self._convert_emoji_to_text(problem["story_text"]),
                        self.story_style,
                    )
                )
                elements.append(Spacer(1, 15))

                # Question
                question_text = f"{question_num}. {self._convert_emoji_to_text(problem['question'])}"
                elements.append(Paragraph(question_text, self.question_style))

                # Answer space
                answer_space = "Answer: " + "_" * 50
                elements.append(Paragraph(answer_space, self.answer_style))
                question_num += 1

            else:
                # Regular question
                question_text = f"{question_num}. {self._convert_emoji_to_text(problem['question'])}"
                elements.append(Paragraph(question_text, self.question_style))

                # Answer space
                answer_space = "Answer: " + "_" * 40
                elements.append(Paragraph(answer_space, self.answer_style))
                question_num += 1

        return elements

    def _create_instructions(self, subject: str, age_group: str) -> List:
        """Create instructions section"""
        elements = []

        instructions_title = Paragraph("<b>Instructions:</b>", self.styles["Heading3"])
        elements.append(instructions_title)

        if subject == "math":
            if age_group == "4-5":
                instructions = "• Count carefully and write your answer in the blank space<br/>• Ask for help if you need it<br/>• Take your time with each problem"
            elif age_group == "6-7":
                instructions = "• Read each problem carefully<br/>• Show your work when possible<br/>• Check your answers when finished"
            else:
                instructions = "• Read word problems twice before solving<br/>• Show your work clearly<br/>• Check that your answers make sense"

        elif subject == "logic":
            instructions = "• Think carefully about each problem<br/>• Look for patterns and connections<br/>• Explain your thinking if possible"

        elif subject == "comprehensive":
            instructions = "• This assessment covers Math, Logic, and Reading<br/>• Read each question carefully and note the subject type<br/>• Show your work for math problems<br/>• Use complete sentences for reading questions<br/>• Take your time and check your work"

        else:  # reading
            instructions = "• Read all stories and passages carefully<br/>• Answer questions in complete sentences when possible<br/>• Use information from the text to support your answers"

        elements.append(Paragraph(instructions, self.styles["Normal"]))
        elements.append(Spacer(1, 20))

        return elements

    def generate_worksheet(
        self,
        subject: str,
        age_group: str,
        problems: List[Dict],
        output_filename: str,
        student_name: str = "",
    ) -> str:
        """Generate a complete worksheet PDF"""

        # Create the PDF document
        doc = SimpleDocTemplate(
            output_filename,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18,
        )

        # Build the content
        story = []

        # Header
        story.extend(self._create_header(subject, age_group, student_name))

        # Instructions
        story.extend(self._create_instructions(subject, age_group))

        # Problems
        if subject == "math":
            story.extend(self._format_math_problems(problems))
        elif subject == "logic":
            story.extend(self._format_logic_problems(problems))
        elif subject == "reading":
            story.extend(self._format_reading_problems(problems))
        elif subject == "comprehensive":
            story.extend(self._format_comprehensive_problems(problems))
        else:
            # Fallback for unknown subjects
            story.extend(self._format_generic_problems(problems))

        # Footer note
        story.append(Spacer(1, 30))
        footer_text = (
            "Great job! Remember to check your work and ask questions if you need help."
        )
        footer = Paragraph(footer_text, self.styles["Italic"])
        story.append(footer)

        # Build the PDF
        doc.build(story)

        return output_filename

    def generate_answer_key(
        self, subject: str, age_group: str, problems: List[Dict], output_filename: str
    ) -> str:
        """Generate an answer key PDF"""

        doc = SimpleDocTemplate(
            output_filename,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18,
        )

        story = []

        # Header
        if subject == "comprehensive":
            title_text = "Comprehensive Assessment - Answer Key"
        else:
            title_text = f"{subject.title()} Practice Worksheet - Answer Key"
        story.append(Paragraph(title_text, self.title_style))

        subtitle_text = f"For Ages {age_group}"
        story.append(Paragraph(subtitle_text, self.subtitle_style))
        story.append(Spacer(1, 30))

        # Answers
        for i, problem in enumerate(problems, 1):
            # Add subject indicator for comprehensive assessments
            if subject == "comprehensive":
                subject_type = problem.get("subject", "unknown")
                subject_indicator = f"[{subject_type.upper()}]"
                story.append(Paragraph(subject_indicator, self.styles["Italic"]))

            if (
                problem["type"] == "comprehension"
                or problem["type"] == "story_comprehension"
            ):
                # Show story title for context
                story_title = (
                    f"<b>Story: {problem.get('story_title', 'Reading Passage')}</b>"
                )
                story.append(Paragraph(story_title, self.styles["Heading4"]))

            # Check if this is a visual pattern problem (same logic as worksheet)
            if (
                problem.get("type") == "pattern"
                and "Complete the pattern:" in problem["question"]
                and VISUAL_AVAILABLE
            ):
                # Try to create visual pattern for answer key too
                try:
                    # Extract pattern items from the question text
                    pattern_items = self._extract_pattern_items_from_question(
                        problem["question"]
                    )

                    if pattern_items:
                        # Generate images for the pattern items
                        image_paths = visual_generator.create_pattern_images(
                            pattern_items
                        )

                        # Create question number with visual pattern
                        question_num = Paragraph(
                            f"{i}. Complete the pattern:", self.question_style
                        )
                        story.append(question_num)

                        # Add visual pattern flowable
                        visual_pattern = VisualPatternFlowable(
                            problem["question"], image_paths
                        )
                        story.append(visual_pattern)

                        # Show the answer with visual representation
                        answer_text = f"<b>Answer:</b> {self._convert_emoji_to_text(problem['answer'])}"
                        story.append(Paragraph(answer_text, self.answer_style))

                        if "explanation" in problem and problem["explanation"]:
                            explanation_text = f"<i>Explanation:</i> {self._convert_emoji_to_text(problem['explanation'])}"
                            story.append(
                                Paragraph(explanation_text, self.styles["Normal"])
                            )

                        story.append(Spacer(1, 15))
                        continue

                except Exception as e:
                    # Fall back to text conversion if visual fails
                    pass

            # Standard formatting for non-visual patterns
            question_text = f"{i}. {self._convert_emoji_to_text(problem['question'])}"
            story.append(Paragraph(question_text, self.question_style))

            answer_text = (
                f"<b>Answer:</b> {self._convert_emoji_to_text(problem['answer'])}"
            )
            story.append(Paragraph(answer_text, self.answer_style))

            if "explanation" in problem and problem["explanation"]:
                explanation_text = f"<i>Explanation:</i> {self._convert_emoji_to_text(problem['explanation'])}"
                story.append(Paragraph(explanation_text, self.styles["Normal"]))

            story.append(Spacer(1, 15))

        doc.build(story)
        return output_filename

    def _convert_emoji_to_text(self, text) -> str:
        """Convert emoji symbols to PDF-friendly text representations"""
        # Handle non-string inputs (like integers for math answers)
        if not isinstance(text, str):
            return str(text)

        emoji_map = {
            # Color circles
            "🔴": "[RED]",
            "🔵": "[BLUE]",
            "🟢": "[GREEN]",
            "🟡": "[YELLOW]",
            "🟣": "[PURPLE]",
            "🟠": "[ORANGE]",
            "🩷": "[PINK]",
            "🤎": "[BROWN]",
            # Shapes
            "⭕": "[CIRCLE]",
            "⬜": "[SQUARE]",
            "🔺": "[TRIANGLE]",
            "⭐": "[STAR]",
            "❤️": "[HEART]",
            "💎": "[DIAMOND]",
            "⬡": "[HEXAGON]",
            "🥚": "[OVAL]",
            "🟪": "[RECTANGLE]",
            # Animals
            "🐱": "[CAT]",
            "🐶": "[DOG]",
            "🐮": "[COW]",
            "🐷": "[PIG]",
            "🐑": "[SHEEP]",
            "🦆": "[DUCK]",
            # Alternative unicode symbols
            "●": "[CIRCLE]",
            "■": "[SQUARE]",
            "▲": "[TRIANGLE]",
            "★": "[STAR]",
            "♥": "[HEART]",
            "♦": "[DIAMOND]",
            "○": "[OVAL]",
            "▬": "[RECTANGLE]",
        }

        # Replace emojis with text representations
        converted_text = text
        for emoji, text_repr in emoji_map.items():
            converted_text = converted_text.replace(emoji, text_repr)

        return converted_text

    def _format_comprehensive_problems(self, problems: List[Dict]) -> List:
        """Format comprehensive assessment problems for PDF"""
        elements = []

        for i, problem in enumerate(problems, 1):
            # Get the subject from the problem
            subject = problem.get("subject", "unknown")
            problem_type = problem.get("type", "unknown")

            # Add subject indicator
            subject_indicator = f"[{subject.upper()}]"
            subject_para = Paragraph(subject_indicator, self.styles["Italic"])
            elements.append(subject_para)

            # Format based on problem type
            if problem_type == "story_comprehension":
                # Handle reading comprehension specially
                question_text = self._convert_emoji_to_text(problem["question"])

                # Check if it contains a story (has newlines indicating story + question format)
                if "\n\nQuestion:" in question_text:
                    story_part, question_part = question_text.split("\n\nQuestion:")

                    # Story text
                    elements.append(Paragraph(story_part, self.story_style))
                    elements.append(Spacer(1, 10))

                    # Question
                    full_question = f"{i}. {question_part.strip()}"
                    elements.append(Paragraph(full_question, self.question_style))
                else:
                    # Regular question format
                    full_question = f"{i}. {question_text}"
                    elements.append(Paragraph(full_question, self.question_style))

                # Answer space for reading
                answer_space = "Answer: " + "_" * 50
                elements.append(Paragraph(answer_space, self.answer_style))

            elif problem_type == "pattern" and VISUAL_AVAILABLE:
                # Handle visual patterns
                try:
                    # Extract pattern items from the question text
                    pattern_items = self._extract_pattern_items_from_question(
                        problem["question"]
                    )

                    if pattern_items:
                        # Generate images for the pattern items
                        image_paths = visual_generator.create_pattern_images(
                            pattern_items
                        )

                        # Create question number
                        question_num = Paragraph(
                            f"{i}. Complete the pattern:", self.question_style
                        )
                        elements.append(question_num)

                        # Add visual pattern flowable
                        visual_pattern = VisualPatternFlowable(
                            problem["question"], image_paths
                        )
                        elements.append(visual_pattern)

                        # Answer space
                        answer_space = "Answer: " + "_" * 40
                        elements.append(Paragraph(answer_space, self.answer_style))
                        continue

                except Exception as e:
                    # Fall back to text conversion if visual fails
                    pass

                # If visual pattern failed, fall through to regular formatting
                question_text = (
                    f"{i}. {self._convert_emoji_to_text(problem['question'])}"
                )
                elements.append(Paragraph(question_text, self.question_style))
                answer_space = "Answer: " + "_" * 40
                elements.append(Paragraph(answer_space, self.answer_style))

            else:
                # Handle all other types (math, logic, vocabulary, etc.)
                question_text = (
                    f"{i}. {self._convert_emoji_to_text(problem['question'])}"
                )
                elements.append(Paragraph(question_text, self.question_style))

                # Determine answer space based on problem type
                if problem_type == "word_problem":
                    answer_space = "Answer: " + "_" * 50
                else:
                    answer_space = "Answer: " + "_" * 40

                elements.append(Paragraph(answer_space, self.answer_style))

            elements.append(Spacer(1, 15))

        return elements

    def _format_generic_problems(self, problems: List[Dict]) -> List:
        """Format problems generically when subject type is unknown"""
        elements = []

        for i, problem in enumerate(problems, 1):
            # Basic question formatting
            question_text = f"{i}. {self._convert_emoji_to_text(problem['question'])}"
            elements.append(Paragraph(question_text, self.question_style))

            # Generic answer space
            answer_space = "Answer: " + "_" * 40
            elements.append(Paragraph(answer_space, self.answer_style))
            elements.append(Spacer(1, 15))

        return elements
