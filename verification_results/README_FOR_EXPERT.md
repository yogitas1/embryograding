# Embryo Grading Verification - Expert Review

## Overview

This folder contains AI-generated embryo grades for **15 IVF embryo images** using the **Gardner Scale**. We need your expert review to validate the AI's accuracy.

## What's Inside

- **📊 verification_report.html** - Main report with embedded images (open in browser)
- **📋 verification_results.csv** - Data in spreadsheet format
- **🖼️ images/** - Original embryo images (15 total)

## How to Review

### Option 1: HTML Report (Recommended)

1. **Open `verification_report.html` in your web browser**
2. Each embryo card shows:
   - Original embryo image
   - AI-assigned Gardner grade (e.g., 4AA, 3BB)
   - Breakdown: Expansion (1-6), ICM quality (A-C), TE quality (A-C)
   - AI's explanation
   - **Input fields for your expert assessment**

3. **For each embryo, please provide:**
   - Your expert Gardner grade
   - Whether you agree with the AI (Yes/No/Partially)
   - Any comments or corrections

4. **To save your notes:**
   - After filling in, use browser's Print function → "Save as PDF"
   - This preserves your input for sharing back

### Option 2: CSV Spreadsheet

- Open `verification_results.csv` in Excel or Google Sheets
- Add columns for:
  - `expert_grade`
  - `agreement` (Yes/No/Partial)
  - `expert_comments`
- Email back the updated CSV

## Gardner Scale Reference

### Expansion Stage (1-6):
- **1** = Early blastocyst (< 50% volume)
- **2** = Blastocyst (> 50% volume)
- **3** = Full blastocyst (fills entire volume)
- **4** = Expanded blastocyst
- **5** = Hatching blastocyst
- **6** = Hatched blastocyst

### Inner Cell Mass (ICM) Quality:
- **A** = Tightly packed, many cells
- **B** = Loosely grouped, several cells
- **C** = Very few cells

### Trophectoderm (TE) Quality:
- **A** = Many cells forming cohesive epithelium
- **B** = Few cells forming loose epithelium
- **C** = Very few large cells

## Example Grades

- **4AA** = Expanded blastocyst, excellent ICM, excellent TE (highest quality)
- **3BB** = Full blastocyst, good ICM, good TE (moderate quality)
- **2CC** = Early blastocyst, poor ICM, poor TE (low quality)
- **N/A** = Not at blastocyst stage (morula, cleavage stage)

## Questions to Consider

When reviewing each image, please assess:

1. ✅ Is the AI's expansion stage accurate?
2. ✅ Is the ICM quality grading correct?
3. ✅ Is the TE quality grading correct?
4. ✅ Is the overall grade appropriate?
5. ✅ Did the AI correctly identify non-blastocyst embryos?

## Sample Sizes

This validation set includes:
- **15 embryos** randomly selected from the dataset
- Mix of different stages and quality levels
- Day 3 and Day 5 embryos

## Notes

- The AI was trained on **Google Gemini 2.5 Flash** model
- Images are from the Kaggle "Embryo Prediction" dataset
- This is an initial proof-of-concept for AI-assisted grading
- Your expert feedback will help us assess the AI's viability

## Thank You!

Your expertise is invaluable for validating this AI system. Please feel free to add any additional observations or suggestions for improvement.

---

**Questions?** Contact the project team for any clarifications.

