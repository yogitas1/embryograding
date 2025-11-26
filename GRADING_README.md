# Embryo Grading System using Gemini API

This system uses Google's Gemini AI to automatically grade IVF embryo images based on the **Gardner Scale**.

## 📁 Project Structure

```
embryograding/
├── extract_images.py          # Extract images from HTML report
├── grade_embryos.py           # Main grading script using Gemini API
├── requirements.txt           # Python dependencies
├── extracted_images/          # Extracted embryo images (15 JPGs)
├── grading_results/           # Output directory for grading results
└── verification_results/      # Original verification data
```

## 🚀 Quick Start

### Option 1: Run Locally

#### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 2: Set Up API Key
Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

**Option A - Environment Variable (Recommended):**
```bash
export GEMINI_API_KEY="your-api-key-here"
```

**Option B - Enter When Prompted:**
The script will ask for your API key if not found in environment.

#### Step 3: Extract Images (Already Done)
```bash
python3 extract_images.py
```
✅ This extracts 15 embryo images from the HTML report to `extracted_images/`

#### Step 4: Grade Embryos
```bash
python3 grade_embryos.py
```

### Option 2: Run in This Environment

If Claude is running this for you:
1. Provide your Gemini API key when prompted
2. Claude will execute the scripts and show results
3. All outputs will be committed and pushed to GitHub

## 📊 Output Files

After running `grade_embryos.py`, you'll get:

```
grading_results/
├── grading_results_YYYYMMDD_HHMMSS.csv    # CSV with all grades
├── grading_results_YYYYMMDD_HHMMSS.json   # Full JSON results
└── grading_report_YYYYMMDD_HHMMSS.html    # Visual HTML report
```

### CSV Format
```csv
image_name,gardner_grade,expansion,icm_quality,te_quality,quality_score,explanation,timestamp,image_path
D5_368.jpg,4AA,4,A,A,Good,"Expanded blastocyst with excellent ICM and TE",2025-11-26T...,extracted_images/D5_368.jpg
```

### JSON Format
Complete results including full AI responses for analysis.

### HTML Report
Visual report with images, grades, and explanations - open in browser.

## 🔬 Gardner Scale Reference

### Expansion Stage (1-6)
- **1** = Early blastocyst (< 50% volume)
- **2** = Blastocyst (≥ 50% volume)
- **3** = Full blastocyst (fills entire volume)
- **4** = Expanded blastocyst (zona thinning)
- **5** = Hatching blastocyst
- **6** = Hatched blastocyst

### Inner Cell Mass (ICM) Quality
- **A** = Tightly packed, many cells
- **B** = Loosely grouped, several cells
- **C** = Very few cells

### Trophectoderm (TE) Quality
- **A** = Many cells, cohesive epithelium
- **B** = Few cells, loose epithelium
- **C** = Very few large cells

### Example Grades
- **4AA** = Expanded, excellent ICM & TE (highest quality)
- **3BB** = Full blastocyst, good ICM & TE
- **N/A** = Not a blastocyst (cleavage stage)

## 🔄 Workflow for Feedback & Improvement

### Step 1: Initial Grading
Run `grade_embryos.py` to get baseline AI grades.

### Step 2: Expert Review
Have an embryologist review the results and provide feedback:
- Correct grades for each embryo
- Agreement level (Yes/No/Partial)
- Specific critiques

### Step 3: Improvement Script
After receiving feedback, use the improvement script (to be created) to:
- Analyze discrepancies
- Refine the AI prompt
- Re-grade with improved approach
- Generate comparison report

### Step 4: Comparison Report
See before/after results with accuracy metrics.

## 🛠️ Customization

### Adjust Model Parameters
Edit `grade_embryos.py` around line 140:
```python
generation_config={
    "temperature": 0.2,      # Lower = more consistent (0.0-1.0)
    "top_p": 0.95,           # Nucleus sampling
    "top_k": 40,             # Top-k sampling
    "max_output_tokens": 1024,
}
```

### Change Gemini Model
Edit `grade_embryos.py` line 107:
```python
def __init__(self, api_key, model_name="gemini-2.0-flash-exp"):
```

Available models:
- `gemini-2.0-flash-exp` (default - fast, accurate)
- `gemini-1.5-pro` (more capable, slower)
- `gemini-1.5-flash` (faster, less capable)

### Modify Grading Prompt
Edit the `GARDNER_SCALE_PROMPT` variable in `grade_embryos.py` to:
- Add specific criteria
- Include few-shot examples
- Emphasize certain features

## 📝 Notes

- **Day 3 embryos** are typically cleavage-stage (4-8 cell) and not gradable by Gardner Scale
- **Day 5+ embryos** are typically blastocysts and can be graded
- The AI will return "N/A" for non-blastocyst embryos
- Low temperature (0.2) ensures consistent grading

## 🆘 Troubleshooting

### "No module named 'google.generativeai'"
```bash
pip install google-generativeai
```

### "API key not found"
Make sure to set the environment variable or enter when prompted.

### "No images found"
Run `extract_images.py` first to extract images from HTML.

### API Rate Limits
If you hit rate limits, add delays between requests in the script.

## 📧 Support

For issues or questions, refer to:
- [Google Gemini API Documentation](https://ai.google.dev/docs)
- [Gardner Scale Reference](https://en.wikipedia.org/wiki/Blastocyst_grading)

---

**Next Steps:** Run the grading, collect expert feedback, and iterate to improve accuracy! 🚀
