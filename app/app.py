from flask import Flask, jsonify, render_template_string
import os
import socket
import datetime

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>CI/CD Portfolio App</title>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Syne:wght@400;800&display=swap" rel="stylesheet"/>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
      --bg: #0a0a0f;
      --surface: #111118;
      --border: #1e1e2e;
      --accent: #00ff99;
      --accent2: #7c3aed;
      --text: #e2e2f0;
      --muted: #555570;
      --mono: 'JetBrains Mono', monospace;
      --sans: 'Syne', sans-serif;
    }

    body {
      background: var(--bg);
      color: var(--text);
      font-family: var(--mono);
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 2rem;
      overflow-x: hidden;
    }

    body::before {
      content: '';
      position: fixed;
      inset: 0;
      background:
        radial-gradient(ellipse 80% 60% at 20% 10%, rgba(124,58,237,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 60% 50% at 80% 90%, rgba(0,255,153,0.08) 0%, transparent 60%);
      pointer-events: none;
      z-index: 0;
    }

    .container {
      position: relative;
      z-index: 1;
      max-width: 820px;
      width: 100%;
    }

    .badge {
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      background: rgba(0,255,153,0.08);
      border: 1px solid rgba(0,255,153,0.25);
      border-radius: 999px;
      padding: 0.25rem 0.85rem;
      font-size: 0.72rem;
      color: var(--accent);
      letter-spacing: 0.12em;
      text-transform: uppercase;
      margin-bottom: 1.5rem;
    }

    .dot {
      width: 7px; height: 7px;
      border-radius: 50%;
      background: var(--accent);
      animation: pulse 2s ease-in-out infinite;
    }

    @keyframes pulse {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.4; transform: scale(0.75); }
    }

    h1 {
      font-family: var(--sans);
      font-size: clamp(2rem, 6vw, 3.8rem);
      font-weight: 800;
      line-height: 1.08;
      letter-spacing: -0.03em;
      margin-bottom: 0.75rem;
    }

    h1 span { color: var(--accent); }

    .subtitle {
      color: var(--muted);
      font-size: 0.9rem;
      margin-bottom: 2.5rem;
      line-height: 1.6;
    }

    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 1px;
      background: var(--border);
      border: 1px solid var(--border);
      border-radius: 12px;
      overflow: hidden;
      margin-bottom: 1.5rem;
    }

    .card {
      background: var(--surface);
      padding: 1.4rem 1.5rem;
      transition: background 0.2s;
    }

    .card:hover { background: #16161f; }

    .card-label {
      font-size: 0.68rem;
      text-transform: uppercase;
      letter-spacing: 0.14em;
      color: var(--muted);
      margin-bottom: 0.45rem;
    }

    .card-value {
      font-size: 0.95rem;
      color: var(--text);
      word-break: break-all;
    }

    .card-value.highlight { color: var(--accent); }

    .stack {
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      margin-bottom: 2rem;
    }

    .tag {
      font-size: 0.72rem;
      padding: 0.3rem 0.75rem;
      border-radius: 6px;
      border: 1px solid var(--border);
      color: var(--muted);
      letter-spacing: 0.08em;
      transition: all 0.2s;
    }

    .tag:hover {
      border-color: var(--accent2);
      color: var(--text);
    }

    .tag.active {
      border-color: var(--accent);
      color: var(--accent);
      background: rgba(0,255,153,0.06);
    }

    .footer {
      font-size: 0.72rem;
      color: var(--muted);
      border-top: 1px solid var(--border);
      padding-top: 1.2rem;
      display: flex;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 0.5rem;
    }

    .footer a {
      color: var(--accent2);
      text-decoration: none;
    }
    .footer a:hover { text-decoration: underline; }
  </style>
</head>
<body>
  <div class="container">
    <div class="badge"><span class="dot"></span> Live &amp; Deployed</div>

    <h1>CI/CD<br/><span>Pipeline</span><br/>Demo</h1>
    <p class="subtitle">
      A portfolio project showcasing end-to-end DevOps:<br/>
      Flask → Docker → Kubernetes → Jenkins → GitHub Actions
    </p>

    <div class="grid">
      <div class="card">
        <div class="card-label">Hostname (Pod)</div>
        <div class="card-value highlight">{{ hostname }}</div>
      </div>
      <div class="card">
        <div class="card-label">Environment</div>
        <div class="card-value">{{ env }}</div>
      </div>
      <div class="card">
        <div class="card-label">App Version</div>
        <div class="card-value highlight">{{ version }}</div>
      </div>
      <div class="card">
        <div class="card-label">Server Time</div>
        <div class="card-value">{{ time }}</div>
      </div>
    </div>

    <div class="stack">
      <span class="tag active">Python 3.11</span>
      <span class="tag active">Flask</span>
      <span class="tag active">Docker</span>
      <span class="tag active">Kubernetes</span>
      <span class="tag active">Jenkins</span>
      <span class="tag active">GitHub Actions</span>
      <span class="tag active">AWS EC2 (Free Tier)</span>
    </div>

    <div class="footer">
      <span>GET /health → returns JSON status</span>
      <a href="/health">View /health endpoint →</a>
    </div>
  </div>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML,
        hostname=socket.gethostname(),
        env=os.environ.get("APP_ENV", "production"),
        version=os.environ.get("APP_VERSION", "1.0.0"),
        time=datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    )

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "hostname": socket.gethostname(),
        "version": os.environ.get("APP_VERSION", "1.0.0"),
        "timestamp": datetime.datetime.utcnow().isoformat()
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
