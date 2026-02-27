"""Minimal web server that shows a big red circle and an optional env-var banner."""

from __future__ import annotations

import os
from html import escape
from http.server import HTTPServer, BaseHTTPRequestHandler

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not installed; rely on real env vars

FOOBAR_VALUE = os.environ.get("FOOBAR") or os.environ.get("NEXT_PUBLIC_FOOBAR") or ""


def _build_page() -> str:
    show_banner = bool(FOOBAR_VALUE)
    banner_html = ""
    if show_banner:
        safe_value = escape(FOOBAR_VALUE)
        banner_html = (
            f'<div class="banner">'
            f"FOOBAR is set: <strong>{safe_value}</strong>"
            f"</div>"
        )

    return f"""\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Red Circle</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  html, body {{ height: 100%; }}
  body {{
    display: flex;
    align-items: center;
    justify-content: center;
    background: #111;
    font-family: sans-serif;
  }}
  .banner {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    padding: 14px 20px;
    background: #ffcc00;
    color: #222;
    font-size: 18px;
    text-align: center;
    z-index: 10;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
  }}
  .circle {{
    width: 300px;
    height: 300px;
    border-radius: 50%;
    background: red;
  }}
</style>
</head>
<body>
{banner_html}
<div class="circle"></div>
</body>
</html>
"""


PAGE_HTML = _build_page()


class _Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(PAGE_HTML.encode())

    def log_message(self, format: str, *args: object) -> None:  # noqa: A002
        # keep stdout clean; override to silence per-request logs
        pass


def main(host: str = "0.0.0.0", port: int = 8000) -> None:
    server = HTTPServer((host, port), _Handler)
    print(f"Serving on http://{host}:{port}")
    if FOOBAR_VALUE:
        print(f"Banner enabled (FOOBAR / NEXT_PUBLIC_FOOBAR = {FOOBAR_VALUE!r})")
    else:
        print("Banner hidden (FOOBAR / NEXT_PUBLIC_FOOBAR not set)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
        server.server_close()


if __name__ == "__main__":
    main()
