## Diffuser setup (Local Mac)
Docs: https://huggingface.co/docs/diffusers/index

brew install cmake protobuf rust python@3.9 git wget
brew install miniforge
python3 -m venv sd-env
source sd-env/bin/activate
pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cpu
pip install diffusers transformers scipy ftfy accelerate
pip install Pillow

python3 -m venv venv
source venv/bin/activate
pip install flask torch torchvision torchaudio diffusers transformers pillow
pip install huggingface_hub
pip install flask-socketio eventlet
huggingface-cli login

Model download
huggingface-cli download stabilityai/stable-diffusion-2-1 --local-dir ./models

## Run the server
python app.py
- Backend opens HTTP + Socket.IO on 0.0.0.0:8000 and waits for frontend requests.

## How the frontend talks to the backend
1) Socket.IO connect: connect with `io("http://localhost:8000")`. After `connect`, read `socket.id`. This `sid` must be sent with the image generation request.

```js
import { io } from "socket.io-client";
const socket = io("http://localhost:8000");

socket.on("connect", () => {
  console.log("sid", socket.id);
});
```

2) Image generation HTTP request: `POST http://127.0.0.1:8000/generate_image` with JSON body including `prompt` and the `sid` you just received.

```bash
curl --location 'http://127.0.0.1:8000/generate_image' \
--header 'Content-Type: application/json' \
--data '{
    "prompt" : "pizza",
    "sid": "<socket-id>"
}'
```

Or via fetch/axios:

```js
await fetch("http://127.0.0.1:8000/generate_image", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ prompt: "pizza", sid: socket.id })
});
```

3) Listen for server events over Socket.IO during generation:

```js
socket.on("progress_update", ({ step, total_steps, percentage }) => {
  // update progress UI
});

socket.on("generation_complete", ({ image_data }) => {
  const img = `data:image/png;base64,${image_data}`;
  // show the generated image
});

socket.on("generation_error", ({ message }) => {
  console.error(message);
});
```

## Endpoints and events
- POST /generate_image: JSON `{ prompt: string, sid: string }`. `sid` must match an active Socket.IO connection. Returns `{ "status": "started" }` while generation runs in the background.
- progress_update (socket event): carries `step`, `total_steps`, `percentage` for progress UI.
- generation_complete (socket event): carries `image_data` with base64-encoded PNG.
- generation_error (socket event): carries `message` describing the failure.

## Docker
# docker build -t mage81/flask_diffusers:latest .
# docker push mage81/flask_diffusers:latest
