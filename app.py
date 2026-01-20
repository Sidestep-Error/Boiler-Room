from flask import Flask, jsonify
import os
import time
import random
import logging

app = Flask(__name__)

# --- Config via env (12-factor) ---
APP_NAME = os.getenv("APP_NAME", "Sidestep Error Demo")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")
CHAOS_MODE = os.getenv("CHAOS_MODE", "false").lower() == "true"

# --- Logging (viktigt för SIEM / IR) ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sidestep-app")

@app.route("/")
def index():
    logger.info("Request to /")
    return jsonify(
        app=APP_NAME,
        version=APP_VERSION,
        environment=ENVIRONMENT
    )

@app.route("/health")
def health():
    return jsonify(status="healthy")

@app.route("/ready")
def readiness():
    # Simulerar extern dependency (DB/API)
    if random.random() < 0.1:
        logger.warning("Readiness check failed")
        return jsonify(status="not ready"), 503
    return jsonify(status="ready")

@app.route("/chaos")
def chaos():
    if CHAOS_MODE:
        logger.error("Chaos mode triggered – crashing!")
        raise RuntimeError("Simulated failure")
    return jsonify(message="Chaos mode disabled")

@app.route("/slow")
def slow():
    time.sleep(2)
    return jsonify(message="Slow response simulated")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)