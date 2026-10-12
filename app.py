from flask import Flask, jsonify
import os
import socket

app = Flask(__name__)

@app.get("/")
def home():
    return """
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Jenkins + Docker Demo</title>
        <style>
          body { font-family: Arial, sans-serif; margin: 0; background: #f3f6fb; color: #172033; }
          main { max-width: 760px; margin: 8vh auto; padding: 32px; background: white; border-radius: 16px; box-shadow: 0 8px 28px #17203318; }
          h1 { color: #1769aa; margin-top: 0; }
          .status { display: inline-block; padding: 8px 12px; border-radius: 999px; background: #e2f8e9; color: #176b35; font-weight: bold; }
          code { background: #f0f3f8; padding: 3px 6px; border-radius: 5px; }
        </style>
      </head>
      <body>
        <main>
          <span class="status">Application is running</span>
          <h1>Jenkins Freestyle + Docker Demo</h1>
          <p>This Flask application was built into a Docker image and deployed by a Jenkins Freestyle job.</p>
          <p><strong>Container host:</strong> <code>{{ hostname }}</code></p>
          <p><strong>Build version:</strong> <code>{{ build_version }}</code></p>
          <p>Health endpoint: <a href="/health">/health</a></p>
        </main>
      </body>
    </html>
    """.replace("{{ hostname }}", socket.gethostname()).replace(
        "{{ build_version }}", os.environ.get("APP_VERSION", "local")
    )

@app.get("/health")
def health():
    return jsonify(status="ok", app="jenkins-flask-app",
                   version=os.environ.get("APP_VERSION", "local")), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
