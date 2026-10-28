from http.server import BaseHTTPRequestHandler, HTTPServer
from html import escape
import json
import os
import socket
from datetime import datetime, timezone


class AppHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/health":
            self.send_json(200, {"status": "healthy"})
            return

        if self.path == "/api/status":
            self.send_json(200, {
                "status": "healthy",
                "application": "kubernetes-demo",
                "version": os.getenv("APP_VERSION", "v2"),
                "environment": os.getenv("APP_ENV", "development"),
                "hostname": socket.gethostname(),
                "port": 8080
            })
            return

        if self.path not in ("/", "/index.html"):
            self.send_json(404, {"error": "Not found"})
            return

        environment = escape(os.getenv("APP_ENV", "development"))
        version = escape(os.getenv("APP_VERSION", "v2"))
        hostname = escape(socket.gethostname())

        page = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#0b1530">
<meta name="description" content="Industry Kubernetes Project — a cloud-native DevOps portfolio application.">
<title>Industry Kubernetes | Cloud Native Platform</title>
<style>
:root {
  color-scheme: dark;
  --bg: #081226;
  --panel: #101e38;
  --panel2: #132744;
  --border: #263b5d;
  --text: #edf4ff;
  --muted: #9db0ce;
  --blue: #55a7ff;
  --cyan: #51e0ed;
  --green: #35d5a0;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--text);
  font-family: Inter, ui-sans-serif, system-ui, -apple-system,
    BlinkMacSystemFont, "Segoe UI", sans-serif;
  line-height: 1.6;
}
a { color: inherit; text-decoration: none; }
.container { width: min(1160px, 90%); margin: auto; }
header {
  border-bottom: 1px solid var(--border);
  background: #0b1730;
}
nav {
  min-height: 76px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
}
.brand { display: flex; align-items: center; gap: 12px; font-weight: 750; }
.logo {
  width: 43px; height: 43px; display: grid; place-items: center;
  border-radius: 13px; color: white; font-size: 25px;
  background: linear-gradient(140deg, #398cff, #625cf6);
  box-shadow: 0 5px 25px #276cff40;
}
.navlinks { display: flex; gap: 25px; color: var(--muted); font-size: 14px; }
.navlinks a:hover { color: white; }
.live { color: var(--green); font-size: 13px; white-space: nowrap; }
.hero {
  position: relative; overflow: hidden;
  background:
    radial-gradient(ellipse at 80% 20%, #234b8870, transparent 42%),
    linear-gradient(125deg, #10284b, #0a1630 65%, #132c50);
  border-bottom: 1px solid var(--border);
}
.hero-grid {
  min-height: 390px; padding: 70px 0;
  display: grid; grid-template-columns: 1.3fr .7fr;
  align-items: center; gap: 35px;
}
.eyebrow {
  color: var(--cyan); font-size: 12px; font-weight: 800;
  letter-spacing: 2.5px; text-transform: uppercase;
}
h1 { font-size: clamp(38px, 5vw, 62px); line-height: 1.08; margin: 18px 0; letter-spacing: -2px; }
.gradient {
  background: linear-gradient(90deg, #64b5ff, #6ce5e9);
  -webkit-background-clip: text; background-clip: text; color: transparent;
}
.intro { max-width: 600px; color: #b7c8e2; font-size: 17px; }
.actions { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 28px; }
.btn {
  display: inline-flex; justify-content: center; align-items: center;
  padding: 12px 20px; border-radius: 10px; font-weight: 700; font-size: 14px;
  border: 1px solid var(--border); transition: transform .2s, opacity .2s;
}
.btn:hover { transform: translateY(-2px); opacity: .9; }
.primary { background: linear-gradient(120deg, #368cff, #625cf6); border: 0; }
.secondary { background: #ffffff08; }
.orbit {
  width: 230px; height: 230px; margin: auto; position: relative;
  display: grid; place-items: center;
  border-radius: 50%; border: 1px solid #5a9dff40;
  background: radial-gradient(circle, #326ecb40, #172d5000 68%);
}
.orbit:before, .orbit:after {
  content: ""; position: absolute; border-radius: 50%;
  border: 1px dashed #58c6ff66; inset: 20px;
}
.orbit:after { inset: 43px; border-style: solid; border-color: #7c8aff45; }
.orbit-icon {
  z-index: 1; width: 115px; height: 115px; border-radius: 28px;
  display: grid; place-items: center; font-size: 61px;
  background: linear-gradient(145deg, #358bff, #5145d7);
  box-shadow: 0 15px 55px #347eff70;
}
.orbit-label {
  position: absolute; padding: 6px 11px; border-radius: 8px;
  background: #142849; border: 1px solid #37577d; color: #d4e7ff;
  font-size: 12px; font-weight: 700;
}
.label-a { top: 7px; left: -18px; }
.label-b { top: 30px; right: -35px; }
.label-c { bottom: 24px; left: -30px; }
.label-d { bottom: 6px; right: -13px; }
section { padding: 60px 0; }
.section-heading { margin-bottom: 25px; }
.section-heading h2 { margin: 0 0 6px; font-size: 26px; }
.section-heading p { color: var(--muted); margin: 0; font-size: 14px; }
.cards { display: grid; grid-template-columns: repeat(4, 1fr); gap: 17px; }
.card {
  padding: 23px; border: 1px solid var(--border); border-radius: 15px;
  background: linear-gradient(145deg, #142541, #0e1a30);
  min-width: 0;
}
.card-icon {
  width: 43px; height: 43px; display: grid; place-items: center;
  border-radius: 12px; margin-bottom: 19px; font-size: 21px;
  background: #378dff20; border: 1px solid #4b9dff45;
}
.card h3 { margin: 0 0 6px; font-size: 16px; }
.card p { margin: 0; color: var(--muted); font-size: 13px; }
.pill {
  display: inline-flex; align-items: center; gap: 7px;
  border: 1px solid #2a5e55; background: #123b383b;
  color: var(--green); padding: 5px 9px; border-radius: 30px;
  font-size: 11px; font-weight: 750;
}
.dot { width: 7px; height: 7px; border-radius: 50%; background: currentColor; }
.details {
  display: grid; grid-template-columns: 1fr 1fr; gap: 18px; margin-top: 22px;
}
.panel { padding: 25px; border-radius: 15px; border: 1px solid var(--border); background: var(--panel); }
.panel h3 { margin: 0 0 18px; font-size: 17px; }
.row {
  display: flex; justify-content: space-between; align-items: center;
  gap: 12px; padding: 11px 0; border-bottom: 1px solid #263751;
  font-size: 13px;
}
.row:last-child { border: 0; }
.row span:first-child { color: var(--muted); }
.row strong { text-align: right; overflow-wrap: anywhere; }
.tech { display: flex; flex-wrap: wrap; gap: 9px; }
.tech span {
  padding: 8px 12px; border: 1px solid #2b4162; border-radius: 9px;
  background: #182b48; color: #c9ddfa; font-size: 12px;
}
.banner {
  margin-top: 22px; padding: 22px 25px; border-radius: 13px;
  border: 1px solid #285c58; background: linear-gradient(100deg, #12332f, #10233b);
  display: flex; justify-content: space-between; align-items: center; gap: 20px;
}
.banner h3 { margin: 0 0 4px; font-size: 16px; }
.banner p { margin: 0; color: var(--muted); font-size: 13px; }
footer { border-top: 1px solid var(--border); padding: 27px 0; color: var(--muted); font-size: 12px; }
.footer-inner { display: flex; justify-content: space-between; gap: 15px; flex-wrap: wrap; }
@media (max-width: 850px) {
  .navlinks { display: none; }
  .hero-grid { grid-template-columns: 1fr; padding: 55px 0; }
  .orbit { width: 200px; height: 200px; }
  .cards { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 520px) {
  .live { display: none; }
  h1 { letter-spacing: -1px; }
  .cards, .details { grid-template-columns: 1fr; }
  section { padding: 42px 0; }
  .banner { align-items: flex-start; flex-direction: column; }
}
</style>
</head>
<body>
<header>
  <nav class="container">
    <a class="brand" href="/">
      <span class="logo">⎈</span>
      <span>Industry Kubernetes</span>
    </a>
    <div class="navlinks">
      <a href="#overview">Overview</a>
      <a href="#platform">Platform</a>
      <a href="#environment">Environment</a>
      <a href="#stack">Tech stack</a>
    </div>
    <span class="live">● Application online</span>
  </nav>
</header>

<main>
<section class="hero" id="overview">
  <div class="container hero-grid">
    <div>
      <div class="eyebrow">Cloud native · Kubernetes · DevOps</div>
      <h1>Build. Deploy.<br><span class="gradient">Scale with confidence.</span></h1>
      <p class="intro">
        A cloud-native application demonstrating modern containerization,
        Kubernetes orchestration, Helm deployments, and reliable health checks.
      </p>
      <div class="actions">
        <a class="btn primary" href="#platform">Explore the platform ↗</a>
        <a class="btn secondary" href="/api/status">View live status →</a>
      </div>
    </div>
    <div class="orbit" aria-label="Cloud native technology illustration">
      <span class="orbit-label label-a">Docker</span>
      <span class="orbit-label label-b">Helm</span>
      <span class="orbit-label label-c">Kustomize</span>
      <span class="orbit-label label-d">DevOps</span>
      <div class="orbit-icon">⎈</div>
    </div>
  </div>
</section>

<section id="platform">
  <div class="container">
    <div class="section-heading">
      <h2>Platform capabilities</h2>
      <p>A practical demonstration of cloud-native engineering fundamentals.</p>
    </div>
    <div class="cards">
      <article class="card">
        <div class="card-icon">▣</div>
        <h3>Containerized app</h3>
        <p>Packaged with Docker for consistent and repeatable deployments.</p>
      </article>
      <article class="card">
        <div class="card-icon">⎈</div>
        <h3>Kubernetes</h3>
        <p>Orchestrated workloads with replicas, probes, and rolling updates.</p>
      </article>
      <article class="card">
        <div class="card-icon">⌘</div>
        <h3>Helm releases</h3>
        <p>Templated manifests and configurable environments for deployments.</p>
      </article>
      <article class="card">
        <div class="card-icon">↗</div>
        <h3>Health monitoring</h3>
        <p>Dedicated health checks help Kubernetes detect application readiness.</p>
      </article>
    </div>

    <div class="details" id="environment">
      <article class="panel">
        <h3>Application information</h3>
        <div class="row"><span>Application</span><strong>kubernetes-demo</strong></div>
        <div class="row"><span>Version</span><strong>VERSION_PLACEHOLDER</strong></div>
        <div class="row"><span>Environment</span><strong>ENVIRONMENT_PLACEHOLDER</strong></div>
        <div class="row"><span>HTTP port</span><strong>8080</strong></div>
        <div class="row"><span>Health endpoint</span><strong>/health</strong></div>
      </article>
      <article class="panel" id="stack">
        <h3>Technology stack</h3>
        <p style="color:var(--muted);font-size:13px;margin-top:-8px;margin-bottom:18px">
          Tools powering this learning project
        </p>
        <div class="tech">
          <span>Python</span><span>Docker</span><span>Kubernetes</span>
          <span>Helm</span><span>Kustomize</span><span>Linux</span>
          <span>Git</span><span>GitHub</span>
        </div>
        <div style="margin-top:22px">
          <span class="pill"><span class="dot"></span> HTTP service running</span>
        </div>
      </article>
    </div>

    <div class="banner">
      <div>
        <h3>✓ Application started successfully</h3>
        <p>Designed for cloud-native learning, deployment practice, and continuous improvement.</p>
      </div>
      <span class="pill"><span class="dot"></span> Operational</span>
    </div>
  </div>
</section>
</main>

<footer>
  <div class="container footer-inner">
    <span>© <span id="year"></span> Industry Kubernetes Project</span>
    <span>Built with Python · Docker · Kubernetes · Helm</span>
  </div>
</footer>
<script>
document.getElementById("year").textContent = new Date().getFullYear();
</script>
</body>
</html>"""

        page = page.replace("ENVIRONMENT_PLACEHOLDER", environment)
        page = page.replace("VERSION_PLACEHOLDER", version)

        body = page.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def send_json(self, status, payload):
        body = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        print(f"{self.address_string()} - {format % args}")



if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    server = HTTPServer(("0.0.0.0", port), AppHandler)
    print(f"Industry Kubernetes website running on port {port}")
    server.serve_forever()
