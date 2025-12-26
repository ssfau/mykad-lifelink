# Step-by-Step Guide: Download and Install Tesseract OCR

## Step 1: Download Tesseract OCR

I've opened the download page in your browser. Follow these steps:

1. **On the GitHub page that just opened**, scroll down to find the download section
2. Look for links that say something like:
   - `tesseract-ocr-w64-setup-5.x.x.exe` (64-bit Windows - RECOMMENDED)
   - Or `tesseract-ocr-w32-setup-5.x.x.exe` (32-bit Windows - only if your system is 32-bit)
3. **Click on the latest .exe file** to download it
4. The file will download to your **Downloads** folder

---

## Step 2: Run the Installer

1. **Go to your Downloads folder** (or wherever your browser saved the file)
2. **Double-click** the downloaded `.exe` file (e.g., `tesseract-ocr-w64-setup-5.4.0.exe`)
3. If Windows asks for permission, click **"Yes"** or **"Run"**

---

## Step 3: Install Tesseract (IMPORTANT STEPS!)

1. The installer will open - click **"Next"** through the setup wizard
2. Accept the license agreement and click **"Next"**
3. Choose installation location (default is fine) and click **"Next"**
4. **⚠️ CRITICAL STEP**: When you see the screen that says **"Select Additional Tasks"**:
   - ✅ **CHECK the box** that says:
     - **"Add Tesseract to PATH"** OR
     - **"Add Tesseract to the system PATH"** OR  
     - **"Add to PATH environment variable"**
   - This is VERY IMPORTANT - don't skip this!
5. Click **"Next"** and then **"Install"**
6. Wait for installation to complete
7. Click **"Finish"**

---

## Step 4: Verify Installation

1. **Close ALL your terminal/command prompt windows** (important - to refresh PATH)
2. **Open a NEW PowerShell or Command Prompt window**
3. Type this command and press Enter:
   ```powershell
   tesseract --version
   ```
4. **You should see** something like:
   ```
   tesseract 5.4.0
    leptonica-1.84.1
    ...
   ```
5. If you see the version number → ✅ **Success!** You're ready!
6. If you get an error saying "tesseract is not recognized" → See troubleshooting below

---

## Step 5: Restart Your Server

1. **Stop your FastAPI server** (if it's running) by pressing `Ctrl+C` in that terminal
2. **Close that terminal window**
3. **Open a NEW terminal window** (this ensures PATH is updated)
4. Navigate to your project folder:
   ```powershell
   cd "D:\Github\Hackathon\Godam2.0\Cursor\mykad-lifelink"
   ```
5. Start the server:
   ```powershell
   python start_server.py
   ```
6. Try uploading a MyKad image again!

---

## Troubleshooting

### If `tesseract --version` doesn't work:

**Option A: Add Tesseract to PATH manually**
1. Find where Tesseract was installed (usually `C:\Program Files\Tesseract-OCR`)
2. Copy that full path
3. Press `Win + X` → Click **"System"**
4. Click **"Advanced system settings"**
5. Click **"Environment Variables"**
6. Under **"System variables"**, find and select **"Path"**, click **"Edit"**
7. Click **"New"** and paste: `C:\Program Files\Tesseract-OCR`
8. Click **"OK"** on all dialogs
9. **Restart your computer** (or at least close and reopen all terminals)

**Option B: Configure path in code (Quick Fix)**
1. Open `backend/core/ocrmodule.py`
2. Find the line that says (around line 41):
   ```python
   # pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
   ```
3. Uncomment it (remove the `#`) and make sure the path matches where Tesseract is installed:
   ```python
   pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
   ```
4. Save the file and restart your server

---

## Need Help?

If the download page didn't open or you need the link again:
- **GitHub Wiki**: https://github.com/UB-Mannheim/tesseract/wiki
- **Direct download page**: Look for the Windows section with .exe files

