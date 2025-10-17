import runpod
import torch
from diffusers import CogVideoXPipeline
from diffusers.utils import export_to_video
import base64
import subprocess
from pathlib import Path
import tempfile
import gc
import os

pipe = None

def download_model():
    """Download model on first run"""
    from huggingface_hub import snapshot_download
    model_dir = "/runpod-volume/cogvideox"
    
    if not os.path.exists(model_dir):
        print("Downloading CogVideoX model...")
        snapshot_download(
            repo_id="THUDM/CogVideoX-2b",
            local_dir=model_dir,
            local_dir_use_symlinks=False
        )
    return model_dir

def load_model():
    global pipe
    if pipe is None:
        print("Loading CogVideoX model...")
        model_dir = download_model()
        pipe = CogVideoXPipeline.from_pretrained(model_dir, torch_dtype=torch.float16)
        pipe = pipe.to("cuda")
        pipe.enable_model_cpu_offload()
        pipe.vae.enable_slicing()
        print("Model loaded!")
    return pipe

def upscale_video(input_path: str, output_path: str):
    try:
        cmd = ['ffmpeg', '-i', input_path, '-vf', 'scale=1280:720:flags=lanczos,fps=24',
               '-c:v', 'libx264', '-crf', '18', '-preset', 'slow', '-pix_fmt', 'yuv420p',
               '-y', output_path]
        subprocess.run(cmd, check=True, capture_output=True, stderr=subprocess.DEVNULL)
        return True
    except:
        return False

def generate_video(job):
    try:
        prompt = job.get("prompt", "A beautiful landscape")
        num_frames = job.get("num_frames", 25)
        num_inference_steps = job.get("num_inference_steps", 30)
        upscale = job.get("upscale", True)
        
        print(f"Generating: {prompt}")
        model = load_model()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_path = Path(tmpdir) / "temp.mp4"
            final_path = Path(tmpdir) / "final.mp4"
            
            video = model(
                prompt=prompt,
                num_videos_per_prompt=1,
                num_inference_steps=num_inference_steps,
                num_frames=num_frames,
                guidance_scale=6.0,
                generator=torch.Generator(device="cuda").manual_seed(42)
            ).frames[0]
            
            export_to_video(video, str(temp_path), fps=8)
            
            output_path = temp_path
            if upscale:
                if upscale_video(str(temp_path), str(final_path)):
                    output_path = final_path
            
            with open(output_path, 'rb') as f:
                video_bytes = f.read()
                video_base64 = base64.b64encode(video_bytes).decode('utf-8')
            
            torch.cuda.empty_cache()
            gc.collect()
            
            return {
                "video_base64": video_base64,
                "prompt": prompt,
                "size_mb": round(len(video_bytes) / 1024 / 1024, 2),
                "quality": "720p HD" if upscale else "480p",
                "success": True
            }
    except Exception as e:
        return {"error": str(e), "success": False}

runpod.serverless.start({"handler": generate_video})
