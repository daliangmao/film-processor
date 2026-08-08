import runpod

def handler(event):
    job_input = event.get("input", {})
    return {"message": "Hello from Film API on A6000!", "received": job_input}

runpod.serverless.start({"handler": handler})
