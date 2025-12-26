# Quick Download Guide for Tesseract OCR

## Method 1: Use the Download Script (Easiest)

1. Open PowerShell in this directory
2. Run:
   ```powershell
   .\download_tesseract.ps1
   ```
3. Follow the prompts

**Note**: If you get a script execution error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## Method 2: Direct Download Link

**Click this link or copy to browser:**
https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.4.0.20241005.exe

**Or visit the official page:**
https://github.com/UB-Mannheim/tesseract/wiki

---

## Method 3: Manual Download Steps

1. **Open your browser** and go to:
   https://github.com/UB-Mannheim/tesseract/wiki

2. **Find the latest Windows installer** (look for a file named like `tesseract-ocr-w64-setup-5.x.x.exe`)

3. **Click to download** the installer

4. **Save it** to your Downloads folder or desktop

5. **Run the installer** and follow these steps:
   - Click "Next" through the setup wizard
   - **IMPORTANT**: When you see the "Select Additional Tasks" screen, make sure to check:
     - ✅ **"Add Tesseract to PATH"** or **"Add to PATH environment variable"**
   - Complete the installation

6. **Verify installation**:
   - Open a NEW PowerShell/Command Prompt window
   - Run: `tesseract --version`
   - You should see a version number

7. **Restart your FastAPI server** and try the MyKad scan again!

---

## Troubleshooting

- **If download link doesn't work**: The version number might have changed. Visit https://github.com/UB-Mannheim/tesseract/wiki and download the latest version manually.

- **If installation fails**: Make sure you have administrator privileges

- **If tesseract command not found after installation**: You need to add Tesseract to PATH manually or restart your computer

