"""
Vercel serverless function entry point for FastAPI application
This file is used by Vercel to serve the FastAPI app as a serverless function

Vercel's @vercel/python runtime automatically detects and wraps ASGI applications
(like FastAPI), so we just need to import and expose the app.
"""
import sys
import os

# Add the project root to the Python path so imports work correctly
# This ensures backend.* imports work from the api/ directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Import the FastAPI app from the backend
from backend.main import app

# Vercel's @vercel/python runtime automatically wraps ASGI apps
# The app variable will be used by Vercel's runtime

