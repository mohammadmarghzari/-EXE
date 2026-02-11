"""
Build script for Portfolio360 Windows Executable
"""
import PyInstaller.__main__
import os
import shutil
import sys

def clean_build():
    """پاک کردن فایل‌های قبلی"""
    dirs_to_remove = ['build', 'dist', '__pycache__']
    for d in dirs_to_remove:
        if os.path.exists(d):
            print(f"Removing {d}...")
            shutil.rmtree(d)
    
    files_to_remove = [f for f in os.listdir('.') if f.endswith('.spec')]
    for f in files_to_remove:
        print(f"Removing {f}...")
        os.remove(f)

def build():
    """ساخت فایل اجرایی"""
    
    # پاکسازی
    clean_build()
    
    # تنظیمات PyInstaller
    args = [
        'main.py',                          # فایل اصلی
        '--name=Portfolio360-Ultimate-Pro', # نام خروجی
        '--onefile',                        # یک فایل exe
        '--windowed',                       # بدون کنسول
        '--clean',                          # پاکسازی کش
        '--noconfirm',                      # بدون تایید
        
        # اضافه کردن فایل‌ها
        '--add-data=app.py;.',              # کد اصلی استریم‌لیت
        
        # مخفی کردن importها
        '--hidden-import=sklearn.utils._typedefs',
        '--hidden-import=sklearn.neighbors._partition_nodes',
        '--hidden-import=scipy.special.cython_special',
        '--hidden-import=scipy.sparse.csgraph._validation',
        '--hidden-import=plotly.validators',
        '--hidden-import=pandas._libs.tslibs.timedeltas',
        '--hidden-import=pandas._libs.tslibs.nattype',
        '--hidden-import=pandas._libs.tslibs.np_datetime',
        '--hidden-import=pandas._libs.skiplist',
        
        # آیکون (اگر داری)
        # '--icon=icon.ico',
        
        # بهینه‌سازی
        '--strip',                          # حذف symbolها
    ]
    
    # اضافه کردن آیکون اگر وجود داشت
    if os.path.exists('icon.ico'):
        args.append('--icon=icon.ico')
    
    print("Building executable...")
    print(f"Command: pyinstaller {' '.join(args)}")
    
    PyInstaller.__main__.run(args)
    
    print("\n" + "="*50)
    print("Build completed!")
    print(f"Output: dist/Portfolio360-Ultimate-Pro.exe")
    print("="*50)

def create_installer():
    """ساخت installer با NSIS (اختیاری)"""
    nsis_script = """
    !define PRODUCT_NAME "Portfolio360 Ultimate Pro"
    !define PRODUCT_VERSION "1.0.0"
    !define PRODUCT_PUBLISHER "Your Company"
    
    Name "${PRODUCT_NAME}"
    OutFile "Portfolio360-Setup.exe"
    InstallDir "$PROGRAMFILES64\\Portfolio360"
    
    Section "MainSection" SEC01
        SetOutPath "$INSTDIR"
        File "dist\\Portfolio360-Ultimate-Pro.exe"
        CreateShortcut "$DESKTOP\\Portfolio360.lnk" "$INSTDIR\\Portfolio360-Ultimate-Pro.exe"
    SectionEnd
    """
    
    with open('installer.nsi', 'w') as f:
        f.write(nsis_script)
    
    print("NSIS script created: installer.nsi")
    print("Install NSIS and run: makensis installer.nsi")

if __name__ == "__main__":
    build()
    
    # اگر آرگومان --installer داده شد
    if '--installer' in sys.argv:
        create_installer()
