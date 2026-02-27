import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

import cv2
import sqlite3
import pyttsx3
import threading
import time
import requests
import smtplib
from email.message import EmailMessage
from ultralytics import YOLO
from deepface import DeepFace
import pygame
import warnings

warnings.filterwarnings("ignore")

# --- CONFIGURATION ---
TOKEN = "8216407550:AAGWhHRxzRGpQb97FfhMGiSyCqhr57eZpd4"
CHAT_ID = "5497400422"
AUTH_DIR = "authorized_users"
BREACH_DIR = "breach_reports"
DB_FILE = "security_archive.db"
# Path to your dashboard's static folder for real-time web display
DASHBOARD_STATIC = os.path.join("static", "captures")

# --- EMAIL SETTINGS ---
SENDER_EMAIL = "poojithavela@gmail.com" 
SENDER_PASSWORD = "hmuq mhlm bkzh wroh"
RECEIVER_EMAIL = "poojithavela@gmail.com"

# --- 1. DATABASE FUNCTIONS ---
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS breaches 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  timestamp TEXT, object_name TEXT, status TEXT, image_path TEXT)''')
    conn.commit()
    conn.close()

def archive_breach(obj_name, status, path):
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("INSERT INTO breaches (timestamp, object_name, status, image_path) VALUES (?, ?, ?, ?)",
                  (time.strftime("%Y-%m-%d %H:%M:%S"), obj_name, status, path))
        last_id = c.lastrowid 
        conn.commit()
        conn.close()
        return last_id
    except Exception as e:
        print(f"❌ DATABASE ERROR: {e}")
        return None

# --- 2. PROFESSIONAL EMAIL ALERT ---
def send_email_report(image_path, label, status, obj_id):
    def task():
        try:
            current_time = time.strftime('%H:%M:%S')
            current_date = time.strftime('%Y-%m-%d')
            
            msg = EmailMessage()
            msg['Subject'] = f"🚨 SECURITY BREACH REPORT: {status}"
            msg['From'] = SENDER_EMAIL
            msg['To'] = RECEIVER_EMAIL
            
            content = f"""
            OMNI-SHIELD SECURITY INCIDENT REPORT
            ------------------------------------
            Status: {status}
            Object Detected: {label}
            System ID: {obj_id}
            Date: {current_date}
            Time: {current_time}
            Location: Primary Security Zone
            ------------------------------------
            Attached is the captured evidence image.
            Developed by: VELA POOJITHA
            """
            msg.set_content(content)

            with open(image_path, 'rb') as f:
                msg.add_attachment(f.read(), maintype='image', subtype='jpeg', filename=f"BREACH_{obj_id}.jpg")

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
                smtp.send_message(msg)
            print(f"✅ EMAIL SUCCESS: Security Report sent for ID:{obj_id}")
        except Exception as e:
            print(f"❌ EMAIL ERROR: Failed to send report - {e}")
    threading.Thread(target=task, daemon=True).start()

# --- 3. DETAILED TELEGRAM ALERT ---
def send_telegram_report(path, label, status, obj_id):
    def post():
        url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
        current_time = time.strftime('%H:%M:%S')
        current_date = time.strftime('%Y-%m-%d')
        
        caption = (f"🚨 OMNI-SHIELD SYSTEM ALERT\n"
                   f"━━━━━━━━━━━━━━━━━━\n"
                   f"📍 STATUS: {status}\n"
                   f"📦 OBJECT: {label}\n"
                   f"🆔 REF ID: {obj_id}\n"
                   f"📅 DATE: {current_date}\n"
                   f"🕒 TIME: {current_time}\n"
                   f"━━━━━━━━━━━━━━━━━━\n"
                   f"👤 OWNER: VELA POOJITHA")
        try:
            with open(path, "rb") as photo:
                requests.post(url, files={"photo": photo}, data={"chat_id": CHAT_ID, "caption": caption})
            print(f"✅ TELEGRAM SUCCESS: Alert sent for ID:{obj_id}")
        except:
            print(f"❌ TELEGRAM ERROR: Connection failed for ID:{obj_id}")
    threading.Thread(target=post, daemon=True).start()

# --- 4. SIREN & VOICE ---
def play_siren():
    def task():
        try:
            pygame.mixer.init()
            pygame.mixer.music.load("siren.mp3")
            pygame.mixer.music.play()
            time.sleep(4)
            pygame.mixer.music.stop()
        except: pass
    threading.Thread(target=task, daemon=True).start()

voice_lock = threading.Lock()
def speak_now(text):
    def run():
        with voice_lock:
            try:
                engine = pyttsx3.init()
                engine.say(text); engine.runAndWait()
            except: pass
    threading.Thread(target=run, daemon=True).start()

# --- 5. ENGINE INITIALIZATION ---
init_db() 
if not os.path.exists(BREACH_DIR): os.makedirs(BREACH_DIR)
if not os.path.exists(DASHBOARD_STATIC): os.makedirs(DASHBOARD_STATIC)
if not os.path.exists(AUTH_DIR): os.makedirs(AUTH_DIR)

model = YOLO('yolov8s.pt')
cap = cv2.VideoCapture(0)
cap.set(3, 1280); cap.set(4, 720)

zone_coords = []
def select_zone(event, x, y, flags, param):
    global zone_coords
    if event == cv2.EVENT_LBUTTONDOWN: zone_coords = [(x, y)]
    elif event == cv2.EVENT_LBUTTONUP: zone_coords.append((x, y))

# --- STEP 1: INTERACTIVE SETUP ---
print("\n" + "="*50)
print("🛡️  OMNI-SHIELD SYSTEM SETUP | VELA POOJITHA")
print("="*50)
print("👉 ACTION: Draw the Restricted Zone with your mouse.")
print("👉 ACTION: Press 'S' to Start Monitoring.")

cv2.namedWindow("SETUP")
cv2.setMouseCallback("SETUP", select_zone)

while True:
    ret, frame = cap.read()
    if not ret: break
    if len(zone_coords) == 2: cv2.rectangle(frame, zone_coords[0], zone_coords[1], (0,255,255), 2)
    cv2.imshow("SETUP", frame)
    if cv2.waitKey(1) & 0xFF == ord('s') and len(zone_coords) == 2:
        print("\n🚀 ZONE CONFIGURED. AI MONITORING STARTED...\n")
        break
cv2.destroyWindow("SETUP")

Z_START, Z_END = zone_coords[0], zone_coords[1]
seen_ids = {}

# --- STEP 2: RUNTIME ENGINE ---
while cap.isOpened():
    success, frame = cap.read()
    if not success: break
    results = model.track(frame, persist=True, verbose=False, conf=0.5)
    annotated_frame = results[0].plot()
    
    # Visual Zone Indicator
    cv2.rectangle(annotated_frame, Z_START, Z_END, (0,0,255), 2)
    cv2.putText(annotated_frame, "RESTRICTED ZONE", (Z_START[0], Z_START[1]-10), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)

    if results[0].boxes.id is not None:
        boxes = results[0].boxes.xyxy.cpu().numpy()
        ids = results[0].boxes.id.int().cpu().tolist()
        clss = results[0].boxes.cls.int().cpu().tolist()

        for box, obj_id, cls in zip(boxes, ids, clss):
            label = model.names[cls]
            cx, cy = int((box[0]+box[2])/2), int((box[1]+box[3])/2)

            # Check if object is inside the drawn zone
            if (Z_START[0] < cx < Z_END[0]) and (Z_START[1] < cy < Z_END[1]):
                now = time.time()
                # Cooldown of 12 seconds per specific object ID
                if obj_id not in seen_ids or (now - seen_ids[obj_id] > 12):
                    seen_ids[obj_id] = now
                    
                    is_authorized = False
                    if label == "person":
                        x1, y1, x2, y2 = map(int, box)
                        crop = frame[max(0,y1):y2, max(0,x1):x2]
                        try:
                            res = DeepFace.find(img_path=crop, db_path=AUTH_DIR, enforce_detection=False, silent=True)
                            if len(res) > 0 and not res[0].empty:
                                is_authorized = True
                        except: pass

                    # HANDLING AUTHORIZED ACCESS
                    if is_authorized:
                        speak_now("Authorized Access. Welcome Vela Poojitha")
                        path = os.path.join(BREACH_DIR, f"Auth_{obj_id}.jpg")
                        cv2.imwrite(path, annotated_frame)
                        
                        # Save to DB and then copy for Web
                        db_id = archive_breach("Vela Poojitha", "Authorized Entry", path)
                        web_snapshot_path = os.path.join(DASHBOARD_STATIC, f"alert_{db_id}.jpg")
                        cv2.imwrite(web_snapshot_path, annotated_frame)
                        
                        print(f"📝 VERIFIED: Vela Poojitha Identified (ID:{obj_id})")
                    
                    # HANDLING INTRUSIONS
                    else:
                        status = "CRITICAL INTRUDER" if label == "person" else f"Restricted {label}"
                        path = os.path.join(BREACH_DIR, f"Alert_{obj_id}.jpg")
                        cv2.imwrite(path, annotated_frame)
                        
                        # Archive to database
                        db_name = "Unknown Person" if label == "person" else label
                        db_id = archive_breach(db_name, status, path)
                        
                        # Sync with Dashboard
                        web_snapshot_path = os.path.join(DASHBOARD_STATIC, f"alert_{db_id}.jpg")
                        cv2.imwrite(web_snapshot_path, annotated_frame)
                        
                        if label == "person":
                            speak_now("Critical Alert! Unknown Intruder Detected!")
                            play_siren() 
                            send_telegram_report(path, "UNKNOWN PERSON", "CRITICAL INTRUDER", obj_id)
                            send_email_report(path, "UNKNOWN PERSON", "CRITICAL INTRUDER", obj_id)
                            print(f"🔥 ALARM: Unknown Intruder! (ID:{obj_id})")
                        else:
                            speak_now(f"Alert. Restricted {label} detected.")
                            send_telegram_report(path, label.upper(), "RESTRICTED OBJECT", obj_id)
                            print(f"⚠️  WARNING: Prohibited {label} detected (ID:{obj_id})")

    cv2.imshow("Omni-Shield Advance", annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        print("🛑 SYSTEM SHUTTING DOWN...")
        break

cap.release()
cv2.destroyAllWindows()