import base64
import uuid
import os
from datetime import datetime
import requests
from flask import Blueprint, request, jsonify, current_app
from app import SessionLocal
from .models import Picture, Tag
from imagekitio import ImageKit
import json
from .credentials import load_credentials

# Leer credentials.json montado en /app

creds = load_credentials()

# -----------------------------
# BLUEPRINT ÚNICO
# -----------------------------
routes_bp = Blueprint("routes", __name__)

# -----------------------------
# ENDPOINT BÁSICO
# -----------------------------
@routes_bp.route("/ping")
def ping():
    return jsonify({"status": "ok"})


# -----------------------------
# CREDENCIALES
# -----------------------------
IMAGEKIT_PUBLIC = creds["imagekit_public_key"]
IMAGEKIT_PRIVATE = creds["imagekit_private_key"]
IMAGEKIT_URL = creds["imagekit_url_endpoint"]

IMAGGA_KEY = creds["imagga_api_key"]
IMAGGA_SECRET = creds["imagga_api_secret"]


# -----------------------------
# POST /image
# -----------------------------
@routes_bp.route("/image", methods=["POST"])
def upload_image():

    # 1. Leer body + base64
    body = request.get_json()
    if not body or "data" not in body:
        return jsonify({"error": "Missing 'data' base64 field"}), 400

    img_b64 = body["data"]

    try:
        img_bytes = base64.b64decode(img_b64)
    except Exception:
        return jsonify({"error": "Invalid base64"}), 400

    size_kb = round(len(img_bytes) / 1024, 2)

    # 2. Subir temporalmente a ImageKit
    imagekit = ImageKit(
        public_key=IMAGEKIT_PUBLIC,
        private_key=IMAGEKIT_PRIVATE,
        url_endpoint=IMAGEKIT_URL
    )

    upload_info = imagekit.upload(
        file=img_b64,
        file_name="temp_upload.jpg"
    )

    public_url = upload_info.url
    file_id = upload_info.file_id

    # 3. Obtener tags desde Imagga
    min_confidence = float(request.args.get("min_confidence", 80))

    response = requests.get(
        f"https://api.imagga.com/v2/tags?image_url={public_url}",
        auth=(IMAGGA_KEY, IMAGGA_SECRET)
    )

    data = response.json()

    imagga_tags = [
        {
            "tag": t["tag"]["en"],
            "confidence": t["confidence"]
        }
        for t in data["result"]["tags"]
        if t["confidence"] >= min_confidence
    ]

    # 4. Borrar imagen temporal
    imagekit.delete_file(file_id=file_id)

    # 5. Guardar imagen en local
    img_id = str(uuid.uuid4())
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    upload_dir = current_app.config.get("UPLOAD_FOLDER", "app/uploads")
    os.makedirs(upload_dir, exist_ok=True)

    local_path = os.path.join(upload_dir, f"{img_id}.jpg")

    with open(local_path, "wb") as f:
        f.write(img_bytes)

    # 6. Guardar en MySQL
    session = SessionLocal()

    try:
        picture = Picture(
            id=img_id,
            path=local_path,
            date=now
        )
        session.add(picture)

        for t in imagga_tags:
            tag = Tag(
                tag=t["tag"],
                picture_id=img_id,
                confidence=t["confidence"],
                date=now
            )
            session.add(tag)

        session.commit()

    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        session.close()

    # 7. Respuesta final
    return jsonify({
        "id": img_id,
        "size": size_kb,
        "date": now,
        "tags": imagga_tags,
        "data": img_b64
    }), 201
