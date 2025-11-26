#!/usr/bin/env python3
"""
Embryo Grading System using Google Gemini API.
Grades embryo images based on the Gardner Scale for IVF embryos.
"""

import os
import sys
import json
import csv
from pathlib import Path
from datetime import datetime
import base64
import google.generativeai as genai


# Gardner Scale Grading Prompt
GARDNER_SCALE_PROMPT = """You are an expert embryologist specializing in IVF embryo assessment using the Gardner Scale.

GARDNER SCALE REFERENCE:

**Expansion Stage (1-6):**
- 1 = Early blastocyst (blastocoel < 50% of embryo volume)
- 2 = Blastocyst (blastocoel ≥ 50% of embryo volume)
- 3 = Full blastocyst (blastocoel fills entire embryo)
- 4 = Expanded blastocyst (blastocoel larger than embryo, zona pellucida thinning)
- 5 = Hatching blastocyst (trophectoderm herniating through zona)
- 6 = Hatched blastocyst (completely escaped from zona)

**Inner Cell Mass (ICM) Quality (A-C):**
- A = Tightly packed, many cells
- B = Loosely grouped, several cells
- C = Very few cells

**Trophectoderm (TE) Quality (A-C):**
- A = Many cells forming cohesive epithelium
- B = Few cells forming loose epithelium
- C = Very few large cells

**IMPORTANT NOTES:**
- Only blastocyst-stage embryos (expansion 1-6) can be graded with Gardner Scale
- Cleavage-stage embryos (2-cell, 4-cell, 8-cell, morula) should be marked as "N/A" or "Not Applicable"
- Day 3 embryos are typically cleavage-stage and NOT gradable by Gardner Scale
- Day 5+ embryos are typically blastocysts and can be graded

**YOUR TASK:**
Analyze the provided embryo image and provide:
1. Grade in format: XYZ (e.g., 4AA, 3BB, N/A)
2. Expansion stage (1-6 or N/A)
3. ICM quality (A, B, C, or N/A)
4. TE quality (A, B, C, or N/A)
5. Overall quality assessment (Good/Fair/Poor or "Not Applicable")
6. Brief explanation (2-3 sentences) of your grading rationale

**OUTPUT FORMAT (JSON):**
{
  "gardner_grade": "4AA",
  "expansion": "4",
  "icm_quality": "A",
  "te_quality": "A",
  "quality_score": "Good",
  "explanation": "The embryo is an expanded blastocyst with a tightly packed inner cell mass and cohesive trophectoderm."
}

If the embryo is NOT a blastocyst (cleavage stage, morula), respond with:
{
  "gardner_grade": "N/A",
  "expansion": "N/A",
  "icm_quality": "N/A",
  "te_quality": "N/A",
  "quality_score": "Not Applicable",
  "explanation": "This is a cleavage-stage embryo (Day 3, approximately X-cell stage). The Gardner Scale is only applicable to blastocyst-stage embryos."
}

Now analyze this embryo image:
"""


class EmbryoGrader:
    """Grades embryo images using Google Gemini API."""

    def __init__(self, api_key, model_name="gemini-2.0-flash-exp"):
        """
        Initialize the embryo grader.

        Args:
            api_key: Google AI Studio API key
            model_name: Gemini model to use (default: gemini-2.0-flash-exp)
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        self.results = []

    def load_image(self, image_path):
        """Load an image file and return it as bytes."""
        with open(image_path, 'rb') as f:
            return f.read()

    def grade_embryo(self, image_path):
        """
        Grade a single embryo image.

        Args:
            image_path: Path to the embryo image file

        Returns:
            dict: Grading results
        """
        print(f"\nGrading: {image_path}")

        try:
            # Load image
            image_data = self.load_image(image_path)

            # Prepare the image for Gemini
            image_parts = [
                {
                    "mime_type": "image/jpeg",
                    "data": image_data
                }
            ]

            # Generate content with the image and prompt
            response = self.model.generate_content(
                [GARDNER_SCALE_PROMPT, image_parts[0]],
                generation_config={
                    "temperature": 0.2,  # Low temperature for consistency
                    "top_p": 0.95,
                    "top_k": 40,
                    "max_output_tokens": 1024,
                }
            )

            # Parse the JSON response
            response_text = response.text.strip()

            # Extract JSON from response (handle markdown code blocks)
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()
            elif "```" in response_text:
                json_start = response_text.find("```") + 3
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()

            result = json.loads(response_text)

            # Add metadata
            result['image_name'] = Path(image_path).name
            result['image_path'] = str(image_path)
            result['timestamp'] = datetime.now().isoformat()
            result['full_response'] = response.text

            print(f"  Grade: {result.get('gardner_grade', 'N/A')}")
            print(f"  Quality: {result.get('quality_score', 'N/A')}")

            return result

        except Exception as e:
            print(f"  Error: {e}")
            return {
                'image_name': Path(image_path).name,
                'image_path': str(image_path),
                'gardner_grade': 'ERROR',
                'expansion': 'ERROR',
                'icm_quality': 'ERROR',
                'te_quality': 'ERROR',
                'quality_score': 'ERROR',
                'explanation': f'Error during grading: {str(e)}',
                'full_response': '',
                'timestamp': datetime.now().isoformat()
            }

    def grade_directory(self, image_dir):
        """
        Grade all embryo images in a directory.

        Args:
            image_dir: Directory containing embryo images

        Returns:
            list: List of grading results
        """
        image_path = Path(image_dir)
        image_files = sorted(image_path.glob("*.jpg")) + sorted(image_path.glob("*.jpeg"))

        if not image_files:
            print(f"No images found in {image_dir}")
            return []

        print(f"\nFound {len(image_files)} images to grade")
        print("=" * 60)

        self.results = []
        for img_file in image_files:
            result = self.grade_embryo(img_file)
            self.results.append(result)

        return self.results

    def save_results_csv(self, output_file):
        """Save results to CSV file."""
        if not self.results:
            print("No results to save")
            return

        fieldnames = [
            'image_name',
            'gardner_grade',
            'expansion',
            'icm_quality',
            'te_quality',
            'quality_score',
            'explanation',
            'timestamp',
            'image_path'
        ]

        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for result in self.results:
                row = {k: result.get(k, '') for k in fieldnames}
                writer.writerow(row)

        print(f"\nResults saved to: {output_file}")

    def save_results_json(self, output_file):
        """Save full results to JSON file."""
        if not self.results:
            print("No results to save")
            return

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2)

        print(f"Full results saved to: {output_file}")

    def generate_html_report(self, output_file):
        """Generate an HTML report with images and grades."""
        if not self.results:
            print("No results to generate report")
            return

        html_template = """<!DOCTYPE html>
<html>
<head>
    <title>Embryo Grading Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; background: #f5f5f5; }}
        h1 {{ text-align: center; color: #333; }}
        .summary {{ background: white; padding: 20px; margin-bottom: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .embryo-card {{ background: white; padding: 20px; margin-bottom: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); display: flex; gap: 20px; }}
        .image-container {{ flex: 0 0 300px; }}
        .image-container img {{ width: 100%; border-radius: 4px; border: 2px solid #ddd; }}
        .details {{ flex: 1; }}
        .grade-badge {{ display: inline-block; font-size: 24px; font-weight: bold; padding: 10px 20px; border-radius: 4px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }}
        .metric {{ margin: 10px 0; padding: 10px; background: #f8f9fa; border-radius: 4px; border-left: 4px solid #667eea; }}
        .quality-good {{ border-left-color: #28a745; }}
        .quality-fair {{ border-left-color: #ffc107; }}
        .quality-poor {{ border-left-color: #dc3545; }}
        .explanation {{ margin-top: 15px; padding: 15px; background: #f8f9fa; border-radius: 4px; color: #555; line-height: 1.6; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #f8f9fa; font-weight: bold; }}
    </style>
</head>
<body>
    <h1>🔬 Embryo Grading Report</h1>

    <div class="summary">
        <h2>Summary</h2>
        <table>
            <tr><th>Total Images</th><td>{total_images}</td></tr>
            <tr><th>Model</th><td>Google Gemini 2.0 Flash</td></tr>
            <tr><th>Grading Scale</th><td>Gardner Scale</td></tr>
            <tr><th>Generated</th><td>{timestamp}</td></tr>
        </table>
    </div>

    <h2>Individual Assessments</h2>
    {cards}
</body>
</html>"""

        card_template = """
    <div class="embryo-card">
        <div class="image-container">
            <img src="{image_path}" alt="{image_name}">
        </div>
        <div class="details">
            <h3>{image_name}</h3>
            <div class="grade-badge">{grade}</div>
            <div class="metric {quality_class}">
                <strong>Expansion:</strong> {expansion} |
                <strong>ICM:</strong> {icm} |
                <strong>TE:</strong> {te} |
                <strong>Quality:</strong> {quality}
            </div>
            <div class="explanation">
                <strong>Analysis:</strong> {explanation}
            </div>
        </div>
    </div>"""

        cards_html = []
        for result in self.results:
            quality = result.get('quality_score', 'N/A')
            quality_class = ''
            if 'good' in quality.lower():
                quality_class = 'quality-good'
            elif 'fair' in quality.lower():
                quality_class = 'quality-fair'
            elif 'poor' in quality.lower():
                quality_class = 'quality-poor'

            card = card_template.format(
                image_path=result.get('image_path', ''),
                image_name=result.get('image_name', ''),
                grade=result.get('gardner_grade', 'N/A'),
                expansion=result.get('expansion', 'N/A'),
                icm=result.get('icm_quality', 'N/A'),
                te=result.get('te_quality', 'N/A'),
                quality=quality,
                quality_class=quality_class,
                explanation=result.get('explanation', '')
            )
            cards_html.append(card)

        html_content = html_template.format(
            total_images=len(self.results),
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            cards=''.join(cards_html)
        )

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"HTML report saved to: {output_file}")


def main():
    """Main execution function."""
    print("=" * 60)
    print("Embryo Grading System - Gemini API")
    print("=" * 60)

    # Get API key from environment or user input
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        print("\nNo GEMINI_API_KEY found in environment.")
        api_key = input("Enter your Google AI Studio API key: ").strip()
        if not api_key:
            print("Error: API key is required")
            sys.exit(1)

    # Set paths
    image_dir = "extracted_images"
    output_dir = Path("grading_results")
    output_dir.mkdir(exist_ok=True)

    # Check if images exist
    if not Path(image_dir).exists():
        print(f"\nError: Image directory '{image_dir}' not found")
        print("Please run extract_images.py first to extract images from HTML")
        sys.exit(1)

    # Initialize grader
    print(f"\nInitializing Gemini model...")
    grader = EmbryoGrader(api_key)

    # Grade all embryos
    print(f"\nProcessing images from: {image_dir}")
    grader.grade_directory(image_dir)

    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    grader.save_results_csv(output_dir / f"grading_results_{timestamp}.csv")
    grader.save_results_json(output_dir / f"grading_results_{timestamp}.json")
    grader.generate_html_report(output_dir / f"grading_report_{timestamp}.html")

    print("\n" + "=" * 60)
    print("✅ Grading complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
