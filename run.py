import subprocess
import time
import webbrowser

# Start FastAPI backend
backend = subprocess.Popen(["py", "app.py"])

# Give backend time to start
time.sleep(5)

# Start Streamlit frontend
frontend = subprocess.Popen(["py", "-m", "streamlit", "run", "streamlit_app.py"])

# Give Streamlit time to launch
time.sleep(5)

# # Open browser
# webbrowser.open("http://localhost:8501")

# Keep processes alive
backend.wait()
frontend.wait()