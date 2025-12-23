from ultralytics import YOLO
import psycopg2
import psycopg2.extras
from datetime import datetime

# Koneksi Database PostgreSQL
DB = {
    "host": "localhost",
    "port": 5432,
    "user": "postgres",        # ganti sesuai user PostgreSQL kamu
    "password": "gajahbengkak",  # isi password PostgreSQL
    "dbname": "ujicobamodelai"    # nama DB hasil migrasi
}

# Buka koneksi
db = psycopg2.connect(**DB)
cursor = db.cursor()

# Load YOLO
model = YOLO("models/best.pt")

# Fungsi Simpan ke DB
def simpan_ke_db(label, confidence, bbox):
    sql = """INSERT INTO deteksi_objek
            (nama_objek, confidence, timestamp, bbox_x_min, bbox_y_min, bbox_x_max, bbox_y_max)
            VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    data = (
        label,
        float(confidence),
        datetime.now(),
        int(bbox[0]),
        int(bbox[1]),
        int(bbox[2]),
        int(bbox[3])
    )
    cursor.execute(sql, data)
    db.commit()
    print(f"✅ Simpan ke DB: {label}, conf={confidence:.2f}")

# Kamera Stream
results = model(source=1, stream=True, conf=0.4, show=True)

for r in results:
    boxes = r.boxes
    if boxes:
        for box in boxes:
            conf = box.conf.item()
            if conf > 0.4:
                cls_id = int(box.cls.item())
                label = model.names[cls_id]
                bbox = box.xyxy[0].tolist()
                simpan_ke_db(label, conf, bbox)
