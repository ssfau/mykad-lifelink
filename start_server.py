#!/usr/bin/env python
"""Startup script for FastAPI server"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Main entry point for the server"""
    try:
        import uvicorn
        print("[OK] Uvicorn imported successfully")
        print("\nStarting server on http://127.0.0.1:8000")
        print("Press CTRL+C to stop\n")
        
        # Use import string format for reload to work properly
        # Required for Windows multiprocessing compatibility
        uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

