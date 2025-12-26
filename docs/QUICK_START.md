# 🚀 QUICK START - Start the Backend Server

## ⚠️ CRITICAL: The server MUST be running for MyKad upload to work!

## Easiest Method:

### 1. Double-Click `START_SERVER.bat`
   - Find `START_SERVER.bat` in your project folder
   - **Double-click it**
   - A black terminal window will open
   - **DO NOT CLOSE THIS WINDOW**

### 2. Wait for this message:
   ```
   ✓ App imported successfully
   ✓ Uvicorn imported successfully
   
   Starting server on http://127.0.0.1:8000
   INFO:     Uvicorn running on http://127.0.0.1:8000
   ```

### 3. Once you see "Uvicorn running", the server is ready!
   - Go back to your browser
   - Try uploading your MyKad image again
   - The error should be gone!

---

## Alternative: Manual Start

Open PowerShell or Command Prompt and run:
```powershell
cd "d:\Github\Hackathon\Godam2.0\Cursor\mykad-lifelink"
python start_server.py
```

**Keep the terminal window open while using the app!**

---

## ✅ How to Know It's Working:

- You see: `INFO:     Uvicorn running on http://127.0.0.1:8000`
- No error messages in the terminal
- The MyKad upload works in your browser

## ❌ If You See Errors:

- **Import errors**: Run `pip install fastapi uvicorn sqlalchemy pytesseract Pillow python-multipart`
- **Port in use**: Another server might be running - close it first
- **Python not found**: Make sure Python is installed and in your PATH

---

**Remember**: The server must stay running! Don't close the terminal window.

