
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import socket


class AppHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "healthy"}).encode())
            return

        response = {
            "message": "Welcome to the Industry Kubernetes Project!",
            "application": "kubernetes-demo",
            "hostname": socket.gethostname(),
            "environment": os.getenv("APP_ENV", "development")
        }

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response, indent=2).encode())

    def log_message(self, format, *args):
        print(f"{self.address_string()} - {format % args}")


server = HTTPServer(("0.0.0.0", 8080), AppHandler)
print("Application running on port 8080")
server.serve_forever()
