# CogVideoX Serverless Video Generator

AI-powered video generation API using CogVideoX. Generate 720p HD videos from text prompts.

## Features

- 🎥 Text-to-Video generation
- 📺 720p HD output (upscaled from 480p)
- ⚡ Serverless - pay only for what you use
- 🚀 Fast generation (~2-3 minutes)
- 💰 Cost-effective (~$0.13 per video)

## Deploy to RunPod

1. Build Docker image: `docker build -t your-username/cogvideo-serverless .`
2. Push to Docker Hub: `docker push your-username/cogvideo-serverless`
3. Deploy on RunPod Serverless with this image

## API Usage
```python
import runpod

runpod.api_key = "YOUR_API_KEY"
endpoint = runpod.Endpoint("YOUR_ENDPOINT_ID")

job = endpoint.run({
    "prompt": "A cat playing with yarn",
    "num_frames": 25,
    "num_inference_steps": 30,
    "upscale": True
})

result = job.output()
```

## Parameters

- `prompt` (required): Text description of video
- `num_frames`: Number of frames (default: 25, max: 81)
- `num_inference_steps`: Quality steps (default: 30, max: 100)
- `upscale`: Enable 720p upscaling (default: true)

## Cost

~$0.13 per video (2-3 min generation on A40 GPU)

## License

MIT
