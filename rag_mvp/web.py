from __future__ import annotations

import os
from pathlib import Path

from flask import Flask, render_template


def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(
        __name__,
        template_folder=str(Path(__file__).parent.parent / "templates"),
    )

    @app.route("/")
    def index():
        # Check if FOOBAR or NEXT_PUBLIC_FOOBAR environment variables are set
        foobar = os.environ.get("FOOBAR")
        next_public_foobar = os.environ.get("NEXT_PUBLIC_FOOBAR")
        
        show_banner = bool(foobar or next_public_foobar)
        banner_message = f"Environment variable detected: FOOBAR={foobar}" if foobar else f"Environment variable detected: NEXT_PUBLIC_FOOBAR={next_public_foobar}"
        
        return render_template(
            "index.html",
            show_banner=show_banner,
            banner_message=banner_message if show_banner else "",
        )

    return app


def run_web_server(host: str = "0.0.0.0", port: int = 5000, debug: bool = False) -> None:
    """Run the Flask web server."""
    app = create_app()
    print(f"Starting web server at http://{host}:{port}")
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    run_web_server(debug=True)
