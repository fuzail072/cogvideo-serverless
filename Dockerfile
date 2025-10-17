FROM runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel-ubuntu22.04

WORKDIR /app

RUN apt-get update && apt-get install -y ffmpeg git && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    runpod \
    diffusers==0.24.0 \
    transformers \
    accelerate \
    safetensors \
    imageio \
    imageio-ffmpeg \
    sentencepiece \
    protobuf \
    huggingface_hub

COPY handler.py /app/handler.py

ENV PYTHONUNBUFFERED=1

CMD ["python", "-u", "handler.py"]
```

---

### **3. requirements.txt**
```
runpod
diffusers==0.24.0
transformers
accelerate
safetensors
imageio
imageio-ffmpeg
sentencepiece
protobuf
huggingface_hub
