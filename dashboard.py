from flask import Flask, render_template, jsonify, send_from_directory, redirect, url_for, request, session
import sqlite3
import os
import time

app = Flask(__name__)
# NEW: Secret key is required to keep you logged in securely
app.secret_key = "velapoojitha_omnishield_secure_key_2026"

# --- CONFIGURATION ---
DB_FILE = "security_archive.db"
IMAGE_PATH = os.path.join(os.getcwd(), 'static', 'captures')
# NEW: Global variable to store the PIN created during setup
ADMIN_PIN = None 

# Auto-create directory if missing to prevent errors
if not os.path.exists(IMAGE_PATH):
    os.makedirs(IMAGE_PATH)

# --- ROUTES ---

@app.route('/')
def gatekeeper():
    """Forces the user to see the Login page first. Checks if PIN is already set."""
    global ADMIN_PIN
    mode = "setup" if ADMIN_PIN is None else "login"
    return render_template('login.html', mode=mode)

@app.route('/verify', methods=['POST'])
def verify():
    """Real-time Admin Login Logic: Sets PIN for the first time, then validates."""
    global ADMIN_PIN
    op_id = request.form.get('operator_id')
    pin = request.form.get('pin')

    # Feature: First-time setup
    if ADMIN_PIN is None:
        ADMIN_PIN = pin
        session['logged_in'] = True
        session['operator_id'] = op_id
        return redirect(url_for('index'))

    # Feature: Standard Login
    if pin == ADMIN_PIN:
        session['logged_in'] = True
        session['operator_id'] = op_id
        return redirect(url_for('index'))
    else:
        return "<h1>ACCESS DENIED: INVALID SECURITY PIN</h1><a href='/'>Try Again</a>"

@app.route('/home')
def index():
    """Renders the colorful and redesigned OmniShield Welcome UI."""
    if not session.get('logged_in'): return redirect(url_for('gatekeeper'))
    return render_template('index.html', op_id=session.get('operator_id'))

@app.route('/login')
def login_page():
    """Explicit route for the login page."""
    return redirect(url_for('gatekeeper'))

@app.route('/audit-center')
def audit_center():
    """Renders the high-security audit stream page."""
    if not session.get('logged_in'): return redirect(url_for('gatekeeper'))
    return render_template('audit.html', op_id=session.get('operator_id'))

# --- API ENDPOINTS ---

@app.route('/api/logs/all')
def get_logs():
    """Fetches incident logs and ensures the status labels match color requirements."""
    if not session.get('logged_in'): return jsonify([])
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("SELECT id, timestamp, object_name, status FROM breaches ORDER BY id DESC LIMIT 50")
        rows = cur.fetchall()
        
        log_data = []
        for r in rows:
            log_data.append({
                "id": r[0], 
                "time": r[1], 
                "name": r[2], 
                "status": r[3], 
                "image": f"/static/captures/alert_{r[0]}.jpg"
            })
        return jsonify(log_data)
    except Exception as e:
        print(f"Log Error: {e}")
        return jsonify([])
    finally:
        if conn:
            conn.close()

@app.route('/api/stats')
def get_stats():
    """Calculates live metrics for the vibrant dashboard header."""
    if not session.get('logged_in'): return jsonify({})
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        
        cur.execute("SELECT COUNT(*) FROM breaches")
        total = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM breaches WHERE status LIKE '%CRITICAL%' OR status LIKE '%Unknown%'")
        threats = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(DISTINCT object_name) FROM breaches WHERE status LIKE '%Authorized%'")
        identified = cur.fetchone()[0]
        
        return jsonify({
            "total_scans": total,
            "threats": threats,
            "identified": identified,
            "uptime": "99.9%",
            "system_name": "OMNISHIELD AI"
        })
    except Exception as e:
        print(f"Stats Error: {e}")
        return jsonify({"total_scans": 0, "threats": 0, "identified": 0, "uptime": "OFFLINE"})
    finally:
        if conn:
            conn.close()

@app.route('/static/captures/<path:filename>')
def serve_capture(filename):
    """Directly serves images to the Evidence Feed."""
    return send_from_directory(IMAGE_PATH, filename)

@app.route('/api/export')
def export_data():
    """Placeholder for the Export Feature."""
    return jsonify({"message": "Generating CSV Report... Download started."})

@app.route('/logout')
def logout():
    """Redirects back to login gatekeeper and clears session."""
    session.clear()
    return redirect(url_for('gatekeeper'))

# --- MAIN EXECUTION ---

if __name__ == '__main__':
    print("---" * 10)
    print("✨ VELA POOJITHA'S OMNISHIELD DASHBOARD STARTING...")
    print(f"📂 DATABASE: {DB_FILE}")
    print(f"📷 IMAGE STORAGE: {IMAGE_PATH}")
    print("---" * 10)
    app.run(debug=True, port=5000)