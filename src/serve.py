from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Mapping
from urllib.parse import unquote

from .utils import traverse_keys

CONTENT_TYPES = {
    ".css": "text/css; charset=utf-8",
    ".csv": "text/csv; charset=utf-8",
    ".gif": "image/gif",
    ".html": "text/html; charset=utf-8",
    ".ico": "image/x-icon",
    ".jpeg": "image/jpeg",
    ".jpg": "image/jpeg",
    ".js": "application/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".png": "image/png",
    ".svg": "image/svg+xml",
    ".txt": "text/plain; charset=utf-8",
    ".xml": "application/xml",
}

def content_type(data: bytes, path: str) -> str:
    """Return a best-effort guess of the content type of the given bytes and path."""
    # First try file extension
    extension = Path(path).suffix.lower()
    if extension in CONTENT_TYPES:
        return CONTENT_TYPES[extension]

    # Fallback to content sniffing
    if data.startswith(b"<!DOCTYPE html") or b"<html" in data[:100]:
        return "text/html; charset=utf-8"
    elif data.startswith(b"<?xml") or data.startswith(b"<svg"):
        return "image/svg+xml"
    elif data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    elif data.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    elif data.startswith(b"GIF87a") or data.startswith(b"GIF89a"):
        return "image/gif"
    elif all(32 <= b < 127 or b in (9, 10, 13) for b in data[:100]):
        return "text/plain; charset=utf-8"
    else:
        return "application/octet-stream"

def handle_dict(mapping: Mapping):
    """Return a request handler class that serves the given mapping."""
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            path = unquote(self.path)   # decode %xx
            keys = path_to_keys(path)
            if path.endswith("/"):
                keys.append("index.html")
            resource = traverse_keys(mapping, *keys)

            if isinstance(resource, bytes):
                body = resource
            elif isinstance(resource, str):
                body = resource.encode("utf-8")
            elif isinstance(resource, Mapping) and not path.endswith("/"):
                # Redirect to path with trailing slash
                self.send_response(307)
                self.send_header("Location", path + "/")
                self.end_headers()
                return
            else:
                message = "Not found"
                self.send_response(404)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.send_header("Content-Length", str(len(message)))
                self.end_headers()
                self.wfile.write(message.encode("utf-8"))
                return

            self.send_response(200)
            self.send_header("Content-Type", content_type(body, path))
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    return Handler

def path_to_keys(path: str) -> list[str]:
    """Convert a URL path like /a/b/c to a list of keys ['a', 'b', 'c']."""
    parts = path.lstrip("/").split("/")
    return [part for part in parts if part]

def serve(mapping: Mapping):
    """Serve the site represented by the given mapping."""
    port = 8000
    with HTTPServer(("", port), handle_dict(mapping)) as httpd:
        print(f"Serving on http://localhost:{port}")
        httpd.serve_forever()
