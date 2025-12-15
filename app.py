# backend/app.py

# import eventlet
# eventlet.monkey_patch()

from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from threading import Thread
from PIL import Image
from io import BytesIO
import base64
import torch
from diffusers import StableDiffusionPipeline

app = Flask(__name__)
#socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

# 연결된 클라이언트 추적
connected_sockets = set()

# 모델 로딩
print("[MODEL] Loading model...")
pipe = StableDiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-2-1")
pipe = pipe.to("cpu")  # CPU 환경
print("[MODEL] Loaded.")

# 클라이언트 접속 처리
@socketio.on("connect")
def handle_connect():
    connected_sockets.add(request.sid)
    print(f"[CONNECT] {request.sid}")

@socketio.on("disconnect")
def handle_disconnect():
    connected_sockets.discard(request.sid)
    print(f"[DISCONNECT] {request.sid}")

@app.route("/generate_image", methods=["POST"])
def generate():
    data = request.get_json()
    prompt = data.get("prompt")
    sid = data.get("sid")
    if not prompt or not sid:
        return jsonify({"error": "Missing prompt or sid"}), 400

    Thread(target=generate_image, args=(prompt, sid), daemon=True).start()
    return jsonify({"status": "started"})

def generate_image(prompt, sid):
    def callback(pipe, step, timestep, kwargs):
        if sid in connected_sockets:
            socketio.emit("progress_update", {
                "step": step,
                "total_steps": 50,
                "percentage": (step / 50.0) * 100
            }, to=sid)
            return {}

    try:
        result = pipe(prompt, num_inference_steps=50, callback_on_step_end=callback)
        image: Image.Image = result.images[0]
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

        if sid in connected_sockets:
            socketio.emit("generation_complete", {"image_data": img_str}, to=sid)
    except Exception as e:
        print(f"[ERROR] {e}")
        if sid in connected_sockets:
            socketio.emit("generation_error", {"message": str(e)}, to=sid)

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=8000)
