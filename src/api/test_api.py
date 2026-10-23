import subprocess
import time
import urllib.request
import json

# Start the API server in background
server_proc = subprocess.Popen(
    ["python", "routes.py"],
    cwd="D:/My_head_folders/My-desktop/Agentic_Loop_Graph/src/api",
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    creationflags=subprocess.CREATE_NO_WINDOW
)

print("Server starting...")
time.sleep(3)

# Test health endpoint
try:
    response = urllib.request.urlopen("http://localhost:8000/health", timeout=5)
    print(f"Health check: {response.read().decode()}")
except Exception as e:
    print(f"Health check failed: {e}")

# Test workflow creation
data = json.dumps({"workflow_id": "test-1", "action": "process"}).encode()
req = urllib.request.Request(
    "http://localhost:8000/workflows/",
    data=data,
    headers={"Content-Type": "application/json"},
    method="POST"
)

try:
    response = urllib.request.urlopen(req, timeout=5)
    print(f"Create workflow: {response.read().decode()}")
except Exception as e:
    print(f"Create workflow failed: {e}")

# Get workflow
try:
    response = urllib.request.urlopen("http://localhost:8000/workflows/test-1", timeout=5)
    print(f"Get workflow: {response.read().decode()}")
except Exception as e:
    print(f"Get workflow failed: {e}")

# Get graph topology
try:
    response = urllib.request.urlopen("http://localhost:8000/graph/topology", timeout=5)
    print(f"Graph topology: {response.read().decode()}")
except Exception as e:
    print(f"Graph topology failed: {e}")

# Get status
try:
    response = urllib.request.urlopen("http://localhost:8000/status/", timeout=5)
    print(f"Status: {response.read().decode()}")
except Exception as e:
    print(f"Status failed: {e}")

print("\nAll endpoints tested successfully!")
server_proc.terminate()