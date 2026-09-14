"""
Vercel Serverless Entry Point for Lenny OS Backend.

This file re-exports the FastAPI application for Vercel's Python runtime.
"""
from backend.app.main import app

# Vercel expects an `app` variable or `handler` function
