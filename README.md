# MyKad LifeLink

A healthcare management system for managing patient records using MyKad (Malaysian ID card) scanning.

## Prerequisites

1. **Python 3.8+** - Make sure Python is installed and in your PATH
2. **Tesseract OCR** - Required for MyKad image processing
   - Download from: https://github.com/UB-Mannheim/tesseract/wiki
   - During installation, check "Add to PATH"
   - See `docs/INSTALL_TESSERACT.md` for detailed instructions

## Installation

1. Install Python dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```

2. Install Tesseract OCR (see `docs/INSTALL_TESSERACT.md`)

## Running the Application

### Start the Backend Server

**Easiest method**: Double-click `START_SERVER.bat`

**Or run manually**:
```bash
python start_server.py
```

⚠️ **Keep the server window open** while using the app. Server runs on http://127.0.0.1:8000

### Access the Frontend

For best results, serve the frontend files using a local web server:
```bash
cd frontend
python -m http.server 8080
```

Then open: http://127.0.0.1:8080/index.html

## Troubleshooting

- **CORS errors**: Serve HTML files through a web server (not file:// protocol)
- **Tesseract errors**: Make sure Tesseract OCR is installed (the code will auto-detect it)
- **Server connection errors**: Ensure the backend server is running on port 8000
- **Import errors**: Run `pip install -r backend/requirements.txt`
- **Port already in use**: Another server might be running on port 8000

## Additional Documentation

See the `docs/` folder for detailed guides:
- `INSTALL_TESSERACT.md` - Detailed Tesseract installation guide
