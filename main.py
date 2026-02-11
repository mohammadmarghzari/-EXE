"""
Portfolio360 Ultimate Pro - Windows Native Launcher
Using PyWebview for native desktop experience
"""
import webview
import threading
import time
import sys
import os
import socket
from contextlib import closing

# تنظیمات
STREAMLIT_PORT = 8501
MAX_RETRIES = 30
RETRY_DELAY = 0.5

def find_free_port():
    """پیدا کردن پورت آزاد"""
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

def is_port_open(port):
    """چک کردن باز بودن پورت"""
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        return s.connect_ex(('localhost', port)) == 0

def wait_for_server(port, timeout=30):
    """منتظر بالا اومدن سرور"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        if is_port_open(port):
            return True
        time.sleep(0.5)
    return False

def run_streamlit(port):
    """اجرای Streamlit در ترد جداگانه"""
    import streamlit.web.cli as stcli
    
    app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.py")
    
    # اگر فایل توی exe پک شده باشه
    if not os.path.exists(app_path):
        # استخراج از temp
        if hasattr(sys, '_MEIPASS'):
            app_path = os.path.join(sys._MEIPASS, "app.py")
    
    sys.argv = [
        "streamlit", 
        "run", 
        app_path,
        "--server.headless=true",
        f"--server.port={port}",
        "--server.address=localhost",
        "--browser.gatherUsageStats=false",
        "--logger.level=error",
        "--client.toolbarMode=viewer",  # مخفی کردن toolbar استریم‌لیت
        "--theme.base=dark"
    ]
    
    try:
        stcli.main()
    except Exception as e:
        print(f"Streamlit error: {e}")

def create_loading_html():
    """HTML برای صفحه لودینگ"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {
                margin: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                color: white;
            }
            .container {
                text-align: center;
            }
            .spinner {
                width: 60px;
                height: 60px;
                border: 4px solid rgba(255,255,255,0.3);
                border-top: 4px solid white;
                border-radius: 50%;
                animation: spin 1s linear infinite;
                margin: 0 auto 20px;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            h2 { margin: 0; font-weight: 300; }
            p { opacity: 0.8; margin-top: 10px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="spinner"></div>
            <h2>Portfolio360 Ultimate Pro</h2>
            <p>در حال راه‌اندازی...</p>
        </div>
    </body>
    </html>
    """

class Api:
    """API برای ارتباط بین Python و JavaScript"""
    def __init__(self):
        self.window = None
    
    def minimize(self):
        if self.window:
            self.window.minimize()
    
    def maximize(self):
        if self.window:
            self.window.maximize()
    
    def close(self):
        if self.window:
            self.window.destroy()

def main():
    """تابع اصلی"""
    # پیدا کردن پورت آزاد
    port = find_free_port()
    print(f"Using port: {port}")
    
    # اجرای Streamlit در ترد پس‌زمینه
    streamlit_thread = threading.Thread(target=run_streamlit, args=(port,), daemon=True)
    streamlit_thread.start()
    
    # نمایش پنجره لودینگ
    loading_window = webview.create_window(
        'Portfolio360 - Loading',
        html=create_loading_html(),
        width=400,
        height=300,
        frameless=True,
        on_top=True
    )
    
    # چک کردن سرور در ترد دیگه
    server_ready = threading.Event()
    
    def check_server():
        if wait_for_server(port, timeout=30):
            server_ready.set()
    
    checker_thread = threading.Thread(target=check_server, daemon=True)
    checker_thread.start()
    
    # استارت webview با لودینگ
    def start_main_window():
        server_ready.wait()
        loading_window.destroy()
        
        # ساخت پنجره اصلی
        api = Api()
        main_window = webview.create_window(
            'Portfolio360 Ultimate Pro',
            f'http://localhost:{port}',
            width=1400,
            height=900,
            min_size=(1000, 600),
            text_select=True,
            confirm_close=True
        )
        api.window = main_window
        
        # تزریق CSS برای مخفی کردن المان‌های استریم‌لیت
        main_window.events.loaded += lambda: inject_custom_css(main_window)
        
        return main_window
    
    # اجرای webview
    webview.start(
        func=start_main_window,
        debug=False,
        http_server=True,
        gui='edgechromium'  # استفاده از Edge Chromium روی ویندوز
    )

def inject_custom_css(window):
    """مخفی کردن header و footer استریم‌لیت برای ظاهر native"""
    css = """
    // مخفی کردن deploy button و منوی همبرگری
    const style = document.createElement('style');
    style.textContent = `
        #MainMenu {visibility: hidden !important;}
        footer {visibility: hidden !important;}
        header {visibility: hidden !important;}
        .stDeployButton {display: none !important;}
        [data-testid="stToolbar"] {display: none !important;}
    `;
    document.head.appendChild(style);
    """
    window.evaluate_js(css)

if __name__ == "__main__":
    # جلوگیری از اجرای چندباره (PyInstaller multiprocessing)
    if sys.platform.startswith('win'):
        import multiprocessing
        multiprocessing.freeze_support()
    
    main()
