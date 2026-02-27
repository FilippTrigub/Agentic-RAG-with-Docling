from __future__ import annotations

import os
from pathlib import Path

from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RAG MVP Web</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: #f5f5f5;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            position: relative;
        }
        
        .banner {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            text-align: center;
            font-size: 18px;
            font-weight: 600;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            z-index: 1000;
            animation: slideDown 0.5s ease-out;
        }
        
        @keyframes slideDown {
            from {
                transform: translateY(-100%);
            }
            to {
                transform: translateY(0);
            }
        }
        
        .circle-container {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 100%;
            height: 100vh;
        }
        
        .red-circle {
            width: 300px;
            height: 300px;
            background: linear-gradient(135deg, #ff0000 0%, #cc0000 100%);
            border-radius: 50%;
            box-shadow: 
                0 20px 60px rgba(255, 0, 0, 0.4),
                0 0 0 20px rgba(255, 0, 0, 0.1),
                0 0 0 40px rgba(255, 0, 0, 0.05);
            animation: pulse 3s ease-in-out infinite;
        }
        
        @keyframes pulse {
            0%, 100% {
                transform: scale(1);
            }
            50% {
                transform: scale(1.05);
            }
        }
        
        .info {
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: white;
            padding: 15px 30px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            font-size: 14px;
            color: #666;
        }
    </style>
</head>
<body>
    {% if show_banner %}
    <div class="banner">
        🎉 Environment variable detected: {{ env_var_name }} is set!
    </div>
    {% endif %}
    
    <div class="circle-container">
        <div class="red-circle"></div>
    </div>
    
    <div class="info">
        RAG MVP Web Interface | Big Red Circle Demo
    </div>
</body>
</html>
"""


@app.route('/')
def index():
    # Check for FOOBAR or NEXT_PUBLIC_FOOBAR environment variables
    foobar = os.environ.get('FOOBAR')
    next_public_foobar = os.environ.get('NEXT_PUBLIC_FOOBAR')
    
    show_banner = False
    env_var_name = None
    
    if foobar:
        show_banner = True
        env_var_name = 'FOOBAR'
    elif next_public_foobar:
        show_banner = True
        env_var_name = 'NEXT_PUBLIC_FOOBAR'
    
    return render_template_string(
        HTML_TEMPLATE,
        show_banner=show_banner,
        env_var_name=env_var_name
    )


def run_web_server(host: str = '0.0.0.0', port: int = 5000, debug: bool = False) -> None:
    """Run the Flask web server."""
    print(f"Starting web server at http://{host}:{port}")
    print("Press Ctrl+C to stop")
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    run_web_server(debug=True)
