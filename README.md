## Diffuser setup(Local Mac)
Diffuser documents : https://huggingface.co/docs/diffusers/index

brew install cmake protobuf rust python@3.9 git wget
brew install miniforge
python3 -m venv sd-env
source sd-env/bin/activate
pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cpu
pip install diffusers transformers scipy ftfy accelerate
pip install Pillow


python3 -m venv venv
source venv/bin/activate  # 가상 환경 활성화
pip install flask torch torchvision torchaudio diffusers transformers pillow
pip install huggingface_hub
pip install flask-socketio eventlet #socket
huggingface-cli login

model download
huggingface-cli download stabilityai/stable-diffusion-2-1 --local-dir ./models

## Image Generation
curl --location 'http://127.0.0.1:5000/generate_image' \
--header 'Content-Type: application/json' \
--data '{
    "prompt" : "pizza"
}'

## VRAM Status
curl --location 'http://127.0.0.1:5000/vram_status'

## DOCKER
# docker build -t mage81/flask_creation:latest .
# docker push mage81/flask_creation:latest
