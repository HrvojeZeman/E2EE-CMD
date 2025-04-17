import subprocess

NgrokProcess = subprocess.Popen(
    ['ngrok', 'start', 'myapp', '--config=C:\\Users\\Hrvoje\\.ngrok2\\ngrok.yml'],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

UvicornProcess = subprocess.Popen(
    ['uvicorn', 'server:app', '--host 0.0.0.0', '--port 50'],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)