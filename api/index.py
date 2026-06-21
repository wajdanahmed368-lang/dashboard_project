import os
import sys

# Add root folder to sys.path to resolve local imports correctly on Vercel
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
# This exposes the Flask app as 'app' to the Vercel serverless platform
