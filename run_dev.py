"""
Development runner - بدون ساخت EXE
"""
import subprocess
import sys

def run():
    """اجرای مستقیم"""
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", 
        "app.py",
        "--server.port=8501",
        "--browser.gatherUsageStats=false"
    ])

if __name__ == "__main__":
    run()
