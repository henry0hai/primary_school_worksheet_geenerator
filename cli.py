#!/usr/bin/env python3
"""
Full-featured command-line interface for the Primary School Worksheet Generator
Enhanced with student name input, customizable question count, and improved UX
"""

import os
import sys
import re
from datetime import datetime

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from worksheet_generator.core import MathGenerator, LogicGenerator, ReadingGenerator
from worksheet_generator.output import PDFGenerator


def get_student_name():
    """Get and validate student name input"""
    print("\n👤 Student Information:")
    while True:
        name = input("Enter student name (or press Enter to skip): ").strip()
        
        if not name:
            return ""
        
        # Basic validation: only letters, spaces, hyphens, and apostrophes
        if re.match(r"^[a-zA-Z\s\-']+$", name) and len(name) <= 50:
            return name.title()  # Capitalize first letters
        else:
            print("❌ Please enter a valid name (letters, spaces, hyphens, and apostrophes only, max 50 characters)")


def get_question_count():
    """Get and validate question count input"""
    print("\n📊 Question Count:")
    print("Choose number of questions:")
    print("• 10 questions - Quick practice (5-10 minutes)")
    print("• 15 questions - Standard worksheet (10-15 minutes)")
    print("• 20 questions - Extended practice (15-20 minutes)")
    print("• 25 questions - Comprehensive review (20-25 minutes)")
    print("• 30 questions - Full assessment (25-30 minutes)")
    print("• 40 questions - Major assessment (35-40 minutes)")
    print("• 50 questions - Final exam format (45-50 minutes)")
    
    while True:
        try:
            count = input("Enter number of questions (10-50) [default: 15]: ").strip()
            
            if not count:
                return 15  # Default value
            
            count = int(count)
            if 10 <= count <= 50:
                return count
            else:
                print("❌ Please enter a number between 10 and 50")
        except ValueError:
            print("❌ Please enter a valid number")


def get_subject_choice():
    """Get and validate subject choice"""
    print("\n📚 Subject Options:")
    print("1. 🧮 Math - Arithmetic, word problems, and number concepts")
    print("2. 🧩 Logic - Patterns, reasoning, and critical thinking")
    print("3. 📖 Reading - Comprehension, vocabulary, and sentence building")
    print("4. 🎯 Comprehensive Assessment - Mixed questions from all subjects")
    
    while True:
        choice = input("Choose subject (1-4): ").strip()
        subjects = {"1": "math", "2": "logic", "3": "reading", "4": "comprehensive"}
        
        if choice in subjects:
            return subjects[choice]
        else:
            print("❌ Please enter 1, 2, 3, or 4")


def get_age_group():
    """Get and validate age group choice"""
    print("\n👶 Age Groups:")
    print("1. 👶 Ages 4-5 (Pre-K/Kindergarten)")
    print("   • Basic counting, simple patterns, picture books")
    print("2. 🧒 Ages 6-7 (1st-2nd Grade)")
    print("   • Addition/subtraction, easy logic, short stories")
    print("3. 👦 Ages 8-10 (3rd-4th Grade)")
    print("   • Multiplication/division, complex patterns, longer passages")
    
    while True:
        choice = input("Choose age group (1-3): ").strip()
        age_groups = {"1": "4-5", "2": "6-7", "3": "8-10"}
        
        if choice in age_groups:
            return age_groups[choice]
        else:
            print("❌ Please enter 1, 2, or 3")


def get_output_options():
    """Get output preferences"""
    print("\n📄 Output Options:")
    print("1. Both worksheet and answer key (recommended)")
    print("2. Worksheet only")
    print("3. Answer key only")
    
    while True:
        choice = input("Choose output (1-3) [default: 1]: ").strip()
        
        if not choice:
            return "both"  # Default
        
        options = {"1": "both", "2": "worksheet", "3": "answers"}
        if choice in options:
            return options[choice]
        else:
            print("❌ Please enter 1, 2, or 3")


def confirm_generation(subject, age_group, num_questions, student_name, output_type):
    """Show summary and confirm generation"""
    print("\n" + "=" * 60)
    print("📋 WORKSHEET SUMMARY")
    print("=" * 60)
    
    if subject == "comprehensive":
        print(f"Subject: Comprehensive Assessment (Math + Logic + Reading)")
        
        # Show expected distribution
        from collections import defaultdict
        temp_distribution = get_comprehensive_distribution(age_group, num_questions)
        print(f"Expected Distribution:")
        for subj, count in temp_distribution.items():
            percentage = (count / num_questions) * 100
            print(f"  • {subj.title()}: {count} questions ({percentage:.1f}%)")
    else:
        print(f"Subject: {subject.title()}")
    
    print(f"Age Group: {age_group} years old")
    print(f"Number of Questions: {num_questions}")
    print(f"Student Name: {student_name if student_name else 'Not specified'}")
    print(f"Output: {output_type.replace('_', ' ').title()}")
    
    if subject == "comprehensive":
        print(f"\n⏱️  Estimated Time: {num_questions * 1.5:.0f}-{num_questions * 2:.0f} minutes")
        print("📚 Assessment Type: Final exam / Comprehensive evaluation")
    
    print("\n" + "-" * 60)
    confirm = input("Generate worksheet? (y/n) [default: y]: ").strip().lower()
    
    return confirm in ['', 'y', 'yes']


def create_output_directory():
    """Create and return output directory path"""
    output_dir = "generated_worksheets"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"📁 Created output directory: {output_dir}")
    return output_dir


def get_comprehensive_distribution(age_group, total_questions):
    """Get balanced distribution for comprehensive assessment across all subjects"""
    # Define age-based distribution percentages for comprehensive assessments
    distributions = {
        "4-5": {
            "math": 45,     # Focus on basic math concepts
            "reading": 35,  # Strong reading foundation
            "logic": 20     # Simple logic and patterns
        },
        "6-7": {
            "math": 40,     # Balanced math skills
            "reading": 35,  # Continued reading development
            "logic": 25     # Increased logical thinking
        },
        "8-10": {
            "math": 35,     # Advanced math concepts
            "reading": 30,  # Complex reading comprehension
            "logic": 35     # Strong emphasis on logical reasoning
        }
    }
    
    # Get the distribution for this age group (fallback to 6-7 if not found)
    age_distribution = distributions.get(age_group, distributions["6-7"])
    
    # Calculate actual numbers based on percentages
    distribution = {}
    total_assigned = 0
    
    for subject, percentage in age_distribution.items():
        subject_count = round((percentage / 100) * total_questions)
        distribution[subject] = subject_count
        total_assigned += subject_count
    
    # Adjust for rounding differences
    diff = total_questions - total_assigned
    if diff != 0:
        # Add/remove from the most appropriate subject based on age
        if age_group == "4-5":
            distribution["math"] += diff
        elif age_group == "6-7":
            distribution["reading"] += diff
        else:
            distribution["logic"] += diff
    
    return distribution


def generate_comprehensive_problems(age_group, total_questions):
    """Generate a comprehensive assessment with problems from all subjects"""
    print(f"\n🎯 Generating comprehensive assessment with {total_questions} questions for ages {age_group}...")
    
    # Get distribution across subjects
    distribution = get_comprehensive_distribution(age_group, total_questions)
    
    print(f"📊 Comprehensive assessment distribution:")
    for subject, count in distribution.items():
        if count > 0:
            percentage = (count / total_questions) * 100
            print(f"   • {subject.title()}: {count} questions ({percentage:.1f}%)")
    
    all_problems = []
    
    # Generate math problems
    if distribution["math"] > 0:
        print(f"\n🧮 Generating {distribution['math']} math problems...")
        math_gen = MathGenerator()
        math_problems = math_gen.generate_problems(age_group, distribution["math"])
        # Add subject identifier to each problem
        for problem in math_problems:
            problem["subject"] = "math"
        all_problems.extend(math_problems)
    
    # Generate logic problems
    if distribution["logic"] > 0:
        print(f"\n🧩 Generating {distribution['logic']} logic problems...")
        logic_gen = LogicGenerator()
        logic_problems = logic_gen.generate_problems(age_group, distribution["logic"])
        # Add subject identifier to each problem
        for problem in logic_problems:
            problem["subject"] = "logic"
        all_problems.extend(logic_problems)
    
    # Generate reading problems
    if distribution["reading"] > 0:
        print(f"\n📚 Generating {distribution['reading']} reading problems...")
        reading_gen = ReadingGenerator()
        reading_problems = reading_gen.generate_problems(age_group, distribution["reading"])
        # Add subject identifier to each problem
        for problem in reading_problems:
            problem["subject"] = "reading"
        all_problems.extend(reading_problems)
    
    # Shuffle all problems to mix subjects throughout the assessment
    import random
    random.shuffle(all_problems)
    
    print(f"\n✅ Generated {len(all_problems)} total problems across all subjects")
    return all_problems


def generate_problems(subject, age_group, num_questions):
    """Generate problems based on subject"""
    if subject == "comprehensive":
        return generate_comprehensive_problems(age_group, num_questions)
    
    print(f"\n🔄 Generating {num_questions} {subject} problems for ages {age_group}...")
    
    if subject == "math":
        generator = MathGenerator()
        problems = generator.generate_problems(age_group, num_questions)
    elif subject == "logic":
        generator = LogicGenerator()
        problems = generator.generate_problems(age_group, num_questions)
    else:  # reading
        generator = ReadingGenerator()
        problems = generator.generate_problems(age_group, num_questions)
    
    print(f"✅ Generated {len(problems)} unique problems")
    return problems


def create_filenames(output_dir, subject, age_group, student_name):
    """Create output filenames with timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Base filename
    base_name = f"{subject}_{age_group.replace('-', '_')}"
    if student_name:
        # Clean student name for filename
        clean_name = re.sub(r'[^a-zA-Z0-9\-_]', '_', student_name.replace(' ', '_'))
        base_name = f"{base_name}_{clean_name}"
    
    base_name = f"{base_name}_{timestamp}"
    
    worksheet_filename = os.path.join(output_dir, f"{base_name}_worksheet.pdf")
    answer_key_filename = os.path.join(output_dir, f"{base_name}_answers.pdf")
    
    return worksheet_filename, answer_key_filename


def show_sample_problems(problems, subject):
    """Display sample problems to the user"""
    if subject == "comprehensive":
        print(f"\n📋 Sample problems from comprehensive assessment:")
        print("-" * 60)
        
        # Group sample problems by subject
        sample_by_subject = {}
        for problem in problems:
            prob_subject = problem.get("subject", "unknown")
            if prob_subject not in sample_by_subject:
                sample_by_subject[prob_subject] = []
            sample_by_subject[prob_subject].append(problem)
        
        # Show one sample from each subject
        sample_count = 1
        for subj in ["math", "logic", "reading"]:
            if subj in sample_by_subject and sample_by_subject[subj]:
                problem = sample_by_subject[subj][0]
                print(f"{sample_count}. [{subj.upper()}] {problem['question']}")
                
                # Special formatting for different problem types
                if problem.get("type") == "story_comprehension":
                    print(f"   📖 Type: Reading Comprehension")
                elif problem.get("type") == "word_problem":
                    print(f"   🧮 Type: Math Word Problem")
                elif problem.get("type") == "pattern":
                    print(f"   🧩 Type: Logic Pattern")
                elif problem.get("type") == "vocabulary":
                    print(f"   📚 Type: Vocabulary")
                elif problem.get("type") == "logical_reasoning":
                    print(f"   🤔 Type: Logical Reasoning")
                elif problem.get("type") == "classification":
                    print(f"   � Type: Classification")
                
                print(f"   ✅ Answer: {problem['answer']}")
                print()
                sample_count += 1
        
        # Show distribution summary
        from collections import Counter
        subject_counts = Counter([p.get("subject", "unknown") for p in problems])
        print(f"📊 Assessment breakdown:")
        for subj, count in subject_counts.items():
            percentage = (count / len(problems)) * 100
            print(f"   • {subj.title()}: {count} questions ({percentage:.1f}%)")
        
    else:
        print(f"\n📋 Sample {subject} problems generated:")
        print("-" * 50)
        
        for i, problem in enumerate(problems[:3], 1):
            print(f"{i}. {problem['question']}")
            
            # Special formatting for different problem types
            if problem.get("type") == "story_comprehension":
                print(f"   📖 Type: Reading Comprehension")
            elif problem.get("type") == "word_problem":
                print(f"   🧮 Type: Word Problem")
            elif problem.get("type") == "pattern":
                print(f"   🧩 Type: Pattern Recognition")
            elif problem.get("type") == "vocabulary":
                print(f"   📚 Type: Vocabulary")
            
            print(f"   ✅ Answer: {problem['answer']}")
            print()


def generate_pdfs(pdf_gen, subject, age_group, problems, student_name, output_type, worksheet_filename, answer_key_filename):
    """Generate PDF files based on output type"""
    generated_files = []
    
    if output_type in ["both", "worksheet"]:
        print("📄 Creating worksheet PDF...")
        pdf_gen.generate_worksheet(subject, age_group, problems, worksheet_filename, student_name)
        print(f"✅ Worksheet saved: {worksheet_filename}")
        generated_files.append(worksheet_filename)
    
    if output_type in ["both", "answers"]:
        print("📄 Creating answer key PDF...")
        pdf_gen.generate_answer_key(subject, age_group, problems, answer_key_filename)
        print(f"✅ Answer key saved: {answer_key_filename}")
        generated_files.append(answer_key_filename)
    
    return generated_files


def show_completion_summary(generated_files, output_dir, num_questions, subject):
    """Show completion summary and statistics"""
    print("\n" + "=" * 60)
    print("🎉 GENERATION COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    
    print(f"📊 Statistics:")
    if subject == "comprehensive":
        print(f"• Generated {num_questions} comprehensive assessment questions")
        print(f"• Mixed problems from Math, Logic, and Reading subjects")
    else:
        print(f"• Generated {num_questions} unique {subject} problems")
    print(f"• Created {len(generated_files)} PDF file(s)")
    print(f"• Output location: {os.path.abspath(output_dir)}")
    
    print(f"\n📁 Generated Files:")
    for i, file_path in enumerate(generated_files, 1):
        file_size = os.path.getsize(file_path)
        print(f"{i}. {os.path.basename(file_path)} ({file_size:,} bytes)")
    
    print(f"\n💡 Tips:")
    print("• Print the worksheet in black and white to save ink")
    print("• Use the answer key to check student work")
    if subject == "comprehensive":
        print("• This comprehensive assessment covers all major learning areas")
        print("• Perfect for final exams, progress assessments, or skill evaluations")
        print("• Consider timing: 1-2 minutes per question for younger children")
    else:
        print("• Generate multiple worksheets for extra practice")
        print("• Try the comprehensive assessment for mixed subject practice")


def main():
    """Enhanced command line interface for the worksheet generator"""
    
    print("=" * 60)
    print("🎓 PRIMARY SCHOOL WORKSHEET GENERATOR 🎓")
    print("=" * 60)
    print("Generate customized practice worksheets for children aged 4-10 years")
    print("Enhanced with student names, variable question counts, and visual patterns!")
    print()
    
    try:
        # Create output directory
        output_dir = create_output_directory()
        
        # Get user inputs
        student_name = get_student_name()
        subject = get_subject_choice()
        age_group = get_age_group()
        num_questions = get_question_count()
        output_type = get_output_options()
        
        # Confirm generation
        if not confirm_generation(subject, age_group, num_questions, student_name, output_type):
            print("\n👋 Generation cancelled. Goodbye!")
            return
        
        # Generate problems
        problems = generate_problems(subject, age_group, num_questions)
        
        # Create filenames
        worksheet_filename, answer_key_filename = create_filenames(
            output_dir, subject, age_group, student_name
        )
        
        # Generate PDFs
        pdf_gen = PDFGenerator()
        generated_files = generate_pdfs(
            pdf_gen, subject, age_group, problems, student_name, 
            output_type, worksheet_filename, answer_key_filename
        )
        
        # Show sample problems
        show_sample_problems(problems, subject)
        
        # Show completion summary
        show_completion_summary(generated_files, output_dir, num_questions, subject)
        
    except KeyboardInterrupt:
        print("\n\n👋 Generation cancelled by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n🔧 Troubleshooting:")
        print("• Make sure all required packages are installed")
        print("• Run: pip install -r requirements.txt")
        print("• Check that all generator files are present")
        print("• Ensure you have write permissions in the current directory")


if __name__ == "__main__":
    main()
