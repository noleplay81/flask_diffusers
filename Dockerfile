# Dockerfile for flask_diffusers RunPod deployment

FROM nvidia/cuda:12.1.1-base-ubuntu22.04

# System setup
RUN apt update && apt install -y \
    python3 \
    python3-pip \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /workspace/image_creation

# Copy all project files including requirements.txt
COPY . .

# Install Python dependencies from requirements.txt
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

# Expose port
EXPOSE 8000

# Default command
CMD ["python3", "app.py"]