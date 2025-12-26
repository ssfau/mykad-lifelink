# Download Tesseract OCR - Quick Guide

## Direct Download Links

### Latest Windows 64-bit Installer:
**Direct Download:** https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.4.0.20241005.exe

### Alternative (GitHub Releases):
1. Go to: https://github.com/UB-Mannheim/tesseract/releases
2. Download the latest `.exe` file (e.g., `tesseract-ocr-w64-setup-5.x.x.exe`)

### Official Wiki (with multiple versions):
https://github.com/UB-Mannheim/tesseract/wiki

---

## Quick Installation Steps:

1. **Download** one of the installers above
2. **Run** the downloaded `.exe` file
3. **Important**: During installation, check the box that says:
   - ✅ "Add Tesseract to PATH" or
   - ✅ "Add to PATH environment variable"
4. **Complete** the installation
5. **Restart** your terminal/command prompt (or restart your computer)
6. **Verify** by running in a new terminal:
   ```powershell
   tesseract --version
   ```
7. **Restart** your FastAPI server

---

## If the download link doesn't work:

1. Visit the official GitHub wiki: https://github.com/UB-Mannheim/tesseract/wiki
2. Look for the "Windows" section
3. Click on the latest installer link
4. The file will be named something like: `tesseract-ocr-w64-setup-5.x.x.exe`

---

**Note**: Make sure to select the 64-bit version (w64) unless you're on a 32-bit system.

