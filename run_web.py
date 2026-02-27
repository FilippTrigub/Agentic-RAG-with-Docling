#!/usr/bin/env python3
"""Standalone web server runner that doesn't require RAG dependencies."""

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import and run the web server
from rag_mvp.web import run_web_server

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description="RAG MVP Web Server")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=5000, help="Port to bind to")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    
    args = parser.parse_args()
    
    run_web_server(host=args.host, port=args.port, debug=args.debug)
