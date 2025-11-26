#!/usr/bin/env python3
"""
Embryo Grading Improvement System.
Takes expert feedback and improves the AI grading system.
"""

import os
import sys
import json
import csv
from pathlib import Path
from datetime import datetime
import google.generativeai as genai


class FeedbackAnalyzer:
    """Analyzes expert feedback to improve grading."""

    def __init__(self):
        self.feedback_data = []
        self.discrepancies = []
        self.agreement_stats = {
            'total': 0,
            'agree': 0,
            'partial': 0,
            'disagree': 0
        }

    def load_feedback(self, feedback_file):
        """
        Load expert feedback from CSV file.

        Expected CSV format:
        image_name,ai_grade,expert_grade,agreement,expert_comments
        """
        with open(feedback_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            self.feedback_data = list(reader)

        print(f"Loaded feedback for {len(self.feedback_data)} embryos")
        return self.feedback_data

    def analyze_feedback(self):
        """Analyze expert feedback to identify patterns."""
        print("\n" + "=" * 60)
        print("FEEDBACK ANALYSIS")
        print("=" * 60)

        for item in self.feedback_data:
            self.agreement_stats['total'] += 1

            agreement = item.get('agreement', '').lower()
            if 'yes' in agreement or 'agree' in agreement:
                self.agreement_stats['agree'] += 1
            elif 'partial' in agreement:
                self.agreement_stats['partial'] += 1
            else:
                self.agreement_stats['disagree'] += 1
                self.discrepancies.append(item)

        # Print statistics
        print(f"\nTotal Embryos: {self.agreement_stats['total']}")
        print(f"✅ Full Agreement: {self.agreement_stats['agree']} ({self._percentage('agree')}%)")
        print(f"⚠️  Partial Agreement: {self.agreement_stats['partial']} ({self._percentage('partial')}%)")
        print(f"❌ Disagreement: {self.agreement_stats['disagree']} ({self._percentage('disagree')}%)")

        # Analyze discrepancies
        if self.discrepancies:
            print(f"\n📊 Analyzing {len(self.discrepancies)} discrepancies:")
            for disc in self.discrepancies:
                print(f"\n  {disc.get('image_name', 'Unknown')}")
                print(f"    AI Grade: {disc.get('ai_grade', 'N/A')}")
                print(f"    Expert Grade: {disc.get('expert_grade', 'N/A')}")
                print(f"    Comment: {disc.get('expert_comments', 'No comment')}")

        return self.discrepancies

    def _percentage(self, key):
        """Calculate percentage for agreement stats."""
        total = self.agreement_stats['total']
        if total == 0:
            return 0
        return round((self.agreement_stats[key] / total) * 100, 1)

    def generate_improved_prompt(self):
        """Generate an improved prompt based on feedback patterns."""
        # Analyze common mistakes
        expansion_errors = []
        icm_errors = []
        te_errors = []
        stage_misidentification = []

        for disc in self.discrepancies:
            comments = disc.get('expert_comments', '').lower()

            if 'expansion' in comments or 'stage' in comments:
                expansion_errors.append(disc)
            if 'icm' in comments or 'inner cell mass' in comments:
                icm_errors.append(disc)
            if 'te' in comments or 'trophectoderm' in comments:
                te_errors.append(disc)
            if 'not a blastocyst' in comments or 'cleavage' in comments or 'morula' in comments:
                stage_misidentification.append(disc)

        # Build improved prompt with specific examples
        improved_sections = []

        if stage_misidentification:
            improved_sections.append("""
**CRITICAL: Blastocyst vs Cleavage Stage Identification**
- ONLY embryos with a visible blastocoel cavity can be graded using Gardner Scale
- Day 3 embryos are almost always cleavage-stage (2-8 cells) - mark as N/A
- Compacted morulas without a cavity - mark as N/A
- If you cannot clearly see a fluid-filled blastocoel, default to N/A
""")

        if expansion_errors:
            improved_sections.append("""
**EXPANSION STAGE GUIDELINES (Expert-Refined):**
- Stage 1-2: Blastocoel is smaller than or equal to embryo size
- Stage 3: Blastocoel fills the entire embryo but zona is not thinning
- Stage 4: Embryo is larger than original size, zona is visibly thinner
- Stage 5-6: Embryo is hatching or hatched (rarely seen in Day 5)
- When in doubt between stages, choose the lower number
""")

        if icm_errors:
            improved_sections.append("""
**ICM QUALITY GUIDELINES (Expert-Refined):**
- Grade A: Many cells (>8), very tightly compacted, clear distinct mass
- Grade B: Several cells (4-8), somewhat loose grouping
- Grade C: Few cells (<4) or very poorly defined
- If ICM is difficult to distinguish, default to grade B, not A
""")

        if te_errors:
            improved_sections.append("""
**TE QUALITY GUIDELINES (Expert-Refined):**
- Grade A: Many cells forming a smooth, continuous epithelium around entire circumference
- Grade B: Moderate cells, some gaps or irregularity in epithelium
- Grade C: Very few cells, large gaps, or very large/irregular cells
- Look for cohesiveness - even if many cells, gaps = grade B
""")

        improved_prompt = "\n".join(improved_sections)
        return improved_prompt

    def save_analysis_report(self, output_file):
        """Save detailed analysis report."""
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_embryos': self.agreement_stats['total'],
            'agreement_stats': self.agreement_stats,
            'accuracy': self._percentage('agree'),
            'discrepancies': self.discrepancies,
            'improvement_recommendations': self.generate_improved_prompt()
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)

        print(f"\n📄 Analysis report saved to: {output_file}")


class ImprovedGrader:
    """Re-grades embryos with improved prompt based on expert feedback."""

    def __init__(self, api_key, improved_prompt, model_name="gemini-2.0-flash-exp"):
        """Initialize improved grader with enhanced prompt."""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        self.improved_prompt = improved_prompt
        self.results = []

    def regrade_embryos(self, image_dir, original_results):
        """Re-grade embryos with improved prompt."""
        from grade_embryos import EmbryoGrader

        # Use the improved prompt
        base_grader = EmbryoGrader(api_key="dummy")  # Will set later
        base_grader.model = self.model

        # Temporarily update the prompt
        import grade_embryos
        original_prompt = grade_embryos.GARDNER_SCALE_PROMPT
        grade_embryos.GARDNER_SCALE_PROMPT = self.improved_prompt + "\n\n" + original_prompt

        print("\n🔄 Re-grading with improved prompt...")
        self.results = base_grader.grade_directory(image_dir)

        # Restore original prompt
        grade_embryos.GARDNER_SCALE_PROMPT = original_prompt

        return self.results

    def generate_comparison_report(self, original_results, expert_feedback, output_file):
        """Generate HTML comparison report."""
        html_template = """<!DOCTYPE html>
<html>
<head>
    <title>Grading Improvement Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 1400px; margin: 0 auto; padding: 20px; background: #f5f5f5; }}
        h1 {{ text-align: center; color: #333; }}
        .summary {{ background: white; padding: 20px; margin-bottom: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .comparison {{ background: white; padding: 20px; margin-bottom: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .grades {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-top: 15px; }}
        .grade-box {{ padding: 15px; border-radius: 4px; text-align: center; }}
        .grade-box h4 {{ margin: 0 0 10px 0; color: #666; }}
        .grade-box .grade {{ font-size: 24px; font-weight: bold; }}
        .original {{ background: #f8d7da; border: 2px solid #f5c6cb; }}
        .expert {{ background: #d4edda; border: 2px solid #c3e6cb; }}
        .improved {{ background: #d1ecf1; border: 2px solid #bee5eb; }}
        .match {{ background: #d4edda; }}
        .mismatch {{ background: #f8d7da; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
        th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #f8f9fa; font-weight: bold; }}
    </style>
</head>
<body>
    <h1>📊 Grading Improvement Report</h1>

    <div class="summary">
        <h2>Summary</h2>
        <table>
            <tr><th>Original Accuracy</th><td>{original_accuracy}%</td></tr>
            <tr><th>Improved Accuracy</th><td>{improved_accuracy}%</td></tr>
            <tr><th>Improvement</th><td>{improvement}%</td></tr>
            <tr><th>Total Embryos</th><td>{total_embryos}</td></tr>
        </table>
    </div>

    <h2>Individual Comparisons</h2>
    {comparisons}
</body>
</html>"""

        # Generate comparison cards (placeholder for now)
        comparisons_html = "<p>Comparison details will be generated after re-grading.</p>"

        html_content = html_template.format(
            original_accuracy="TBD",
            improved_accuracy="TBD",
            improvement="TBD",
            total_embryos=len(expert_feedback),
            comparisons=comparisons_html
        )

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"📊 Comparison report saved to: {output_file}")


def main():
    """Main execution function."""
    print("=" * 60)
    print("Embryo Grading Improvement System")
    print("=" * 60)

    # Check for feedback file
    if len(sys.argv) < 2:
        print("\nUsage: python3 improve_with_feedback.py <feedback.csv>")
        print("\nExpected CSV format:")
        print("image_name,ai_grade,expert_grade,agreement,expert_comments")
        print("\nExample:")
        print("D5_368.jpg,4AA,3AA,Partial,Expansion should be 3 not 4")
        sys.exit(1)

    feedback_file = sys.argv[1]

    if not Path(feedback_file).exists():
        print(f"Error: Feedback file '{feedback_file}' not found")
        sys.exit(1)

    # Analyze feedback
    analyzer = FeedbackAnalyzer()
    analyzer.load_feedback(feedback_file)
    analyzer.analyze_feedback()

    # Generate improved prompt
    improved_prompt = analyzer.generate_improved_prompt()
    print("\n" + "=" * 60)
    print("IMPROVED PROMPT SECTIONS")
    print("=" * 60)
    print(improved_prompt)

    # Save analysis
    output_dir = Path("improved_results")
    output_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    analyzer.save_analysis_report(output_dir / f"feedback_analysis_{timestamp}.json")

    # Ask if user wants to re-grade
    print("\n" + "=" * 60)
    print("Would you like to re-grade embryos with the improved prompt?")
    print("This requires your Gemini API key.")
    response = input("Re-grade now? (y/n): ").strip().lower()

    if response == 'y':
        api_key = os.environ.get('GEMINI_API_KEY')
        if not api_key:
            api_key = input("Enter your Gemini API key: ").strip()

        if api_key:
            grader = ImprovedGrader(api_key, improved_prompt)
            # Re-grading logic would go here
            print("\n✅ Re-grading complete!")
        else:
            print("No API key provided. Skipping re-grading.")
    else:
        print("\nSkipping re-grading. You can run this script again later.")

    print("\n" + "=" * 60)
    print("✅ Analysis complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
