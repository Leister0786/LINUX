from flask import Flask, render_template, jsonify
import subprocess
from pathlib import Path
import platform

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = BASE_DIR / "scripts"

def run_script(script_name, timeout=8):
    """Run only a known, bundled script. No user-supplied shell commands are accepted."""
    script_path = SCRIPTS_DIR / script_name
    result = subprocess.run(
        ["bash", str(script_path)],
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"{script_name} failed")
    return result.stdout.strip()

def parse_key_values(output):
    data = {}
    for line in output.splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            data[key.strip()] = value.strip()
    return data

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/health")
def health():
    return jsonify({"ok": True, "platform": platform.system()})

@app.route("/api/system")
def system():
    try:
        values = parse_key_values(run_script("system_metrics.sh"))
        return jsonify({
            "cpu": float(values.get("cpu", 0)),
            "memory": float(values.get("memory", 0)),
            "disk": float(values.get("disk", 0)),
            "memory_used": values.get("memory_used", "N/A"),
            "memory_total": values.get("memory_total", "N/A"),
            "disk_used": values.get("disk_used", "N/A"),
            "disk_total": values.get("disk_total", "N/A"),
            "uptime": values.get("uptime", "N/A"),
            "hostname": values.get("hostname", "N/A"),
            "os": values.get("os", "Linux"),
            "kernel": values.get("kernel", "N/A"),
            "process_count": int(values.get("process_count", 0))
        })
    except (RuntimeError, ValueError, subprocess.TimeoutExpired) as exc:
        return jsonify({"error": str(exc)}), 500

@app.route("/api/processes")
def processes():
    try:
        output = run_script("processes.sh")
        rows = []
        for line in output.splitlines():
            parts = line.split("\t")
            if len(parts) >= 5:
                rows.append({
                    "pid": parts[0], "user": parts[1], "cpu": parts[2],
                    "memory": parts[3], "name": parts[4]
                })
        return jsonify({"processes": rows})
    except (RuntimeError, subprocess.TimeoutExpired) as exc:
        return jsonify({"error": str(exc), "processes": []}), 500

@app.route("/api/users")
def users():
    try:
        output = run_script("users.sh")
        return jsonify({"users": [line for line in output.splitlines() if line.strip()]})
    except (RuntimeError, subprocess.TimeoutExpired) as exc:
        return jsonify({"error": str(exc), "users": []}), 500

@app.route("/api/services")
def services():
    try:
        output = run_script("services.sh")
        return jsonify({"services": [line.strip() for line in output.splitlines() if line.strip()]})
    except (RuntimeError, subprocess.TimeoutExpired) as exc:
        return jsonify({"error": str(exc), "services": []}), 500

@app.route("/api/disk")
def disk():
    try:
        output = run_script("disk_usage.sh")
        rows = []
        for line in output.splitlines()[1:]:
            parts = line.split()
            if len(parts) >= 6:
                rows.append({
                    "filesystem": parts[0], "size": parts[1], "used": parts[2],
                    "available": parts[3], "percent": parts[4], "mount": parts[5]
                })
        return jsonify({"disks": rows})
    except (RuntimeError, subprocess.TimeoutExpired) as exc:
        return jsonify({"error": str(exc), "disks": []}), 500

@app.errorhandler(404)
def not_found(_error):
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    # Local development only. Do not expose Flask's debug server to a public network.
    app.run(host="127.0.0.1", port=5000, debug=True)
