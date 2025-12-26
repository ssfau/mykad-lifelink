# How to Start the Backend Server

## ⚠️ IMPORTANT: The server MUST be running for MyKad upload to work!

## Quick Start (Choose One Method):

### Method 1: Double-Click the Batch File (Easiest)
1. **Double-click** `START_SERVER.bat` in your project folder
2. A terminal window will open showing the server starting
3. **KEEP THIS WINDOW OPEN** while using the application
4. You should see: `INFO:     Uvicorn running on http://127.0.0.1:8000`

### Method 2: Use PowerShell Script
1. **Right-click** `START_SERVER.ps1`
2. Select **"Run with PowerShell"**
3. **KEEP THIS WINDOW OPEN** while using the application

### Method 3: Manual Start in Terminal
1. Open **Command Prompt** or **PowerShell**
2. Navigate to your project folder:
   ```
   cd "d:\Github\Hackathon\Godam2.0\Cursor\mykad-lifelink"
   ```
3. Run:
   ```
   python start_server.py
   ```
4. **KEEP THIS TERMINAL WINDOW OPEN**

## ✅ Success Indicators:
- You should see: `✓ App imported successfully`
- You should see: `✓ Uvicorn imported successfully`
- You should see: `Starting server on http://127.0.0.1:8000`
- You should see: `INFO:     Uvicorn running on http://127.0.0.1:8000`

## ❌ If You See Errors:
- **Import errors**: Install missing packages with `pip install -r backend/requirements.txt`
- **Tesseract OCR errors**: Tesseract OCR is required! See `INSTALL_TESSERACT.md` for installation instructions
- **Port already in use**: Another server might be running on port 8000
- **Python not found**: Make sure Python is installed and in your PATH

## 🛑 To Stop the Server:
- Press `CTRL+C` in the terminal window where the server is running
- Or simply close the terminal window

---

**Remember**: The server must be running whenever you want to upload a MyKad image!

