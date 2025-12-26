#!/usr/bin/env python
"""
Railway startup script - Installs Tesseract and starts the FastAPI server
This script runs when Railway deploys your application
"""
import sys
import os
import subprocess

def check_tesseract():
    """Check if Tesseract OCR is available (should be installed via nixpacks.toml)"""
    print("[INFO] Checking for Tesseract OCR...")
    try:
        # Check if tesseract is available
        result = subprocess.run(
            ["tesseract", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version = result.stdout.split()[1] if len(result.stdout.split()) > 1 else "unknown"
            print(f"[OK] Tesseract is available: version {version}")
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception) as e:
        print(f"[WARNING] Tesseract not found in PATH: {e}")
        print("[INFO] Tesseract should be installed via nixpacks.toml during build")
        print("[WARNING] OCR features may not work if Tesseract is not installed")
        return False
    
    return False

def main():
    """Main entry point for Railway"""
    # Add project root to Python path
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_root)
    
    # Check Tesseract (should be installed via nixpacks.toml during build)
    if sys.platform.startswith('linux'):
        check_tesseract()
    else:
        print("[INFO] Not on Linux, using system Tesseract installation if available")
    
    # Get port from Railway environment variable (Railway provides PORT)
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0")
    
    print(f"[INFO] Starting server on {host}:{port}")
    print(f"[INFO] Railway environment detected: PORT={port}")
    
    try:
        import uvicorn
        # Use import string format for proper module resolution
        # Railway will serve both frontend and backend from the same port
        uvicorn.run(
            "backend.main:app",
            host=host,
            port=port,
            log_level="info"
        )
    except Exception as e:
        print(f"[ERROR] Failed to start server: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

