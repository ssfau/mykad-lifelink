# Installing Tesseract OCR for Windows

Tesseract OCR is required for MyKad image processing. Follow these steps to install it:

## Step 1: Download Tesseract OCR

1. Go to: https://github.com/UB-Mannheim/tesseract/wiki
2. Download the latest Windows installer (e.g., `tesseract-ocr-w64-setup-5.x.x.exe`)
3. Or use direct link: https://digi.bib.uni-mannheim.de/tesseract/

## Step 2: Install Tesseract OCR

1. Run the downloaded installer
2. **IMPORTANT**: During installation, make sure to check the option **"Add Tesseract to PATH"** or **"Add to PATH environment variable"**
3. Note the installation directory (usually `C:\Program Files\Tesseract-OCR`)
4. Complete the installation

## Step 3: Verify Installation

Open a new PowerShell or Command Prompt window and run:
```powershell
tesseract --version
```

You should see the Tesseract version number. If you get an error, Tesseract is not in your PATH.

## Step 4: If Tesseract is Not in PATH

If the `tesseract --version` command doesn't work, you need to add Tesseract to your system PATH:

1. Find your Tesseract installation directory (usually `C:\Program Files\Tesseract-OCR`)
2. Copy the full path
3. Add it to your system PATH:
   - Press `Win + X` and select "System"
   - Click "Advanced system settings"
   - Click "Environment Variables"
   - Under "System variables", find and select "Path", then click "Edit"
   - Click "New" and paste the Tesseract installation path
   - Click "OK" on all dialogs
   - **Restart your terminal/command prompt** (or restart your computer)

## Step 5: Verify Python Can Find Tesseract

After adding to PATH, restart your terminal and verify:

```powershell
python -c "import pytesseract; print(pytesseract.get_tesseract_version())"
```

This should print the Tesseract version number.

## Step 6: Restart Your Server

After installing Tesseract, restart your FastAPI server:
1. Stop the current server (Ctrl+C)
2. Run `python start_server.py` again
3. Try uploading a MyKad image again

---

**Troubleshooting:**

- If you still get errors, try specifying the Tesseract path in your code (see backend/core/ocrmodule.py)
- Make sure you've restarted your terminal after adding Tesseract to PATH
- On Windows, you may need to restart your computer for PATH changes to take effect

