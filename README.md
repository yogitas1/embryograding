# Embryo AI Grading - Verification Report

This is a static site showing AI-graded IVF embryo images for expert verification.

## 📊 Contents

- **Landing page**: `index.html`
- **Verification report**: `verification_results/verification_report.html` (15 embryo images with AI grades)

## 🚀 Deploy to GitHub Pages

### Step 1: Create a new GitHub repository

1. Go to https://github.com/new
2. Repository name: `embryo-ai-grading` (or any name you like)
3. Set to **Public**
4. ⚠️ **Do NOT check** "Add a README file"
5. Click "Create repository"

### Step 2: Upload files

**Option A: Using Git (Command Line)**

```bash
cd embryo-grading-pages
git init
git add .
git commit -m "Initial commit: Embryo verification report"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/embryo-ai-grading.git
git push -u origin main
```

**Option B: Using GitHub Web Interface (Easier!)**

1. In your new repository, click "uploading an existing file"
2. Drag and drop the entire `embryo-grading-pages` folder contents
   - `index.html`
   - `verification_results/` folder
3. Scroll down and click "Commit changes"

### Step 3: Enable GitHub Pages

1. Go to your repository **Settings** → **Pages** (left sidebar)
2. Under "Source", select:
   - **Branch**: `main`
   - **Folder**: `/ (root)`
3. Click **Save**
4. Wait 1-2 minutes for deployment

### Step 4: Share the URL

Your site will be live at:
```
https://YOUR_USERNAME.github.io/embryo-ai-grading/
```

Share this URL with your IVF expert friend! They can:
- View the landing page
- Click to see the full verification report with all 15 embryos
- Add their expert grades and comments
- Save as PDF to send back

## 📁 What's Included

- **15 embryo images** (embedded in HTML, no separate image files needed)
- **AI grades** for each embryo using Gardner Scale
- **Interactive form** for expert verification
- **Detailed explanations** for each grade

## 🔒 Privacy Note

These are de-identified research images from a public Kaggle dataset. No patient information is included.

## 📧 Sharing with Experts

Simply send them the GitHub Pages URL:
```
https://YOUR_USERNAME.github.io/embryo-ai-grading/verification_results/verification_report.html
```

They can review directly in their browser, no downloads needed!

