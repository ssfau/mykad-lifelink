#!/usr/bin/env python
"""Startup script for FastAPI server"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from backend.main import app
    print("✓ App imported successfully")
    
    import uvicorn
    print("✓ Uvicorn imported successfully")
    print("\nStarting server on http://127.0.0.1:8000")
    print("Press CTRL+C to stop\n")
    
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
except Exception as e:
    print(f"✗ Error: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc()
    sys.exit(1)

