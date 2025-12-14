# 🚀 Quick Setup Guide

## Running Locally (Recommended for Hackathon Demo)

### Step 1: Get Your API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Get API Key" or "Create API Key"
4. Copy your API key (keep it secure!)

### Step 2: Run the Application

**Option A: Simple (No Server)**
```bash
# Just open the file in your browser
open app.html
# or double-click app.html in Finder
```

**Option B: Local Server (Recommended)**
```bash
cd /Users/kritishukla/google-hackathon/embryograding

# Using Python 3
python3 -m http.server 8000

# Then open: http://localhost:8000/app.html
```

### Step 3: Enter Your API Key
1. When the app loads, you'll see an "API Configuration" section at the top
2. Enter your Gemini API key in the password field
3. The key will be masked (like a password) for security
4. Click the 👁️ button if you need to see it temporarily
5. You'll see a ✅ when the format looks good

### Step 4: Use the App
1. Upload an embryo image (drag & drop or click to browse)
2. Click "🔬 Analyze Embryo"
3. Wait 2-5 seconds for AI grading
4. View results with detailed explanation!

## 🔐 Security Features

✅ **API Key Never Stored**
- Your API key is only kept in memory during your browser session
- It's NOT saved to localStorage, cookies, or any file
- When you close the tab, it's gone

✅ **Password-Masked Input**
- API key appears as dots (•••) when typing
- Optional show/hide toggle for verification
- Prevents shoulder surfing

✅ **No Backend Required**
- Runs entirely in your browser
- Direct API calls to Google Gemini
- No server storing your data

## 📊 GitHub Pages

The app is also live at:
**https://yogitas1.github.io/embryograding/app.html**

Note: On GitHub Pages, you'll need to enter your API key each time you visit.

## 🎓 For Hackathon Presentation

**Demo Flow:**
1. Show the pain points slide (no standardization, time-consuming)
2. Open the app
3. Enter your API key (you can prepare it in advance)
4. Upload a sample embryo image
5. Show the instant grading (<10 seconds vs 5-10 minutes)
6. Highlight the detailed Gardner Scale breakdown
7. Emphasize consistency and standardization

**Sample Images:**
You can find sample embryo images in:
- `verification_results/verification_report.html` (embedded images)
- Or use any embryo image from public datasets

## 🐛 Troubleshooting

**"API key seems too short"**
- Make sure you copied the complete API key
- It should be 39+ characters long

**"API request failed"**
- Check your internet connection
- Verify the API key is correct
- Make sure your Google Cloud project has Gemini API enabled

**"Error analyzing image"**
- Ensure the image is a valid format (JPG, PNG)
- File should be under 10MB
- Try a different embryo image

**CORS errors (if any)**
- This shouldn't happen with Google's API
- If it does, use the local server method (Option B)

## 📝 Notes

- The API key input is cleared when you refresh the page (by design for security)
- Each image analysis costs a small amount of API credits (~$0.001)
- You can analyze unlimited embryos with your API key

## 🎯 Next Steps

After the hackathon, you might want to:
1. Add user authentication for saved results
2. Implement batch processing for multiple embryos
3. Add export to PDF/CSV functionality
4. Create a mobile app version
5. Integrate with lab management systems

---

**Ready to go!** 🚀

Just run `python3 -m http.server 8000` and open http://localhost:8000/app.html

