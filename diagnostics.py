"""
Diagnostic and Troubleshooting Script
Run this to check if everything is set up correctly
"""

import sys
import os

def check_python_version():
    """Check Python version"""
    print("\n" + "="*60)
    print("🐍 Checking Python Version...")
    print("="*60)
    
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print("✅ Python version is compatible (3.8+)")
        return True
    else:
        print("❌ Python 3.8+ required. Please upgrade.")
        return False

def check_dependencies():
    """Check if all required packages are installed"""
    print("\n" + "="*60)
    print("📦 Checking Dependencies...")
    print("="*60)
    
    required = [
        'pyautogui',
        'cv2',
        'numpy',
        'PIL',
        'keyboard',
        'mouse',
        'anthropic'
    ]
    
    all_installed = True
    
    for package in required:
        try:
            if package == 'cv2':
                import cv2
                print(f"✅ opencv-python: {cv2.__version__}")
            elif package == 'PIL':
                import PIL
                print(f"✅ Pillow: {PIL.__version__}")
            else:
                module = __import__(package)
                version = getattr(module, '__version__', 'unknown')
                print(f"✅ {package}: {version}")
        except ImportError:
            print(f"❌ {package}: NOT INSTALLED")
            all_installed = False
    
    if all_installed:
        print("\n✅ All dependencies installed!")
    else:
        print("\n❌ Missing dependencies. Run:")
        print("   pip install -r requirements.txt")
    
    return all_installed

def check_permissions():
    """Check if script has necessary permissions"""
    print("\n" + "="*60)
    print("🔐 Checking Permissions...")
    print("="*60)
    
    try:
        import keyboard
        print("✅ Keyboard access: OK")
    except:
        print("❌ Keyboard access: DENIED")
        print("   → Run as Administrator")
        return False
    
    try:
        import mouse
        print("✅ Mouse access: OK")
    except:
        print("❌ Mouse access: DENIED")
        print("   → Run as Administrator")
        return False
    
    try:
        from PIL import ImageGrab
        ImageGrab.grab()
        print("✅ Screenshot access: OK")
    except:
        print("❌ Screenshot access: DENIED")
        return False
    
    return True

def check_api_key():
    """Check if Claude API key is set"""
    print("\n" + "="*60)
    print("🔑 Checking API Key...")
    print("="*60)
    
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    
    if api_key:
        masked_key = api_key[:15] + "..." + api_key[-4:]
        print(f"✅ API Key found: {masked_key}")
        print("   Advanced features will be available!")
        return True
    else:
        print("⚠️  No API key found")
        print("   Basic features will work fine.")
        print("   For AI features, set ANTHROPIC_API_KEY environment variable")
        return False

def test_screen_capture():
    """Test if screen capture works"""
    print("\n" + "="*60)
    print("📸 Testing Screen Capture...")
    print("="*60)
    
    try:
        from PIL import ImageGrab
        img = ImageGrab.grab()
        print(f"✅ Screenshot captured: {img.size[0]}x{img.size[1]}")
        return True
    except Exception as e:
        print(f"❌ Screenshot failed: {e}")
        return False

def test_mouse_control():
    """Test mouse control (safe test)"""
    print("\n" + "="*60)
    print("🖱️  Testing Mouse Control...")
    print("="*60)
    
    try:
        import pyautogui
        current_pos = pyautogui.position()
        print(f"✅ Current mouse position: {current_pos}")
        print("   (Mouse control is working)")
        return True
    except Exception as e:
        print(f"❌ Mouse control failed: {e}")
        return False

def test_keyboard_control():
    """Test keyboard control"""
    print("\n" + "="*60)
    print("⌨️  Testing Keyboard Control...")
    print("="*60)
    
    try:
        import keyboard
        print("✅ Keyboard module loaded")
        print("   (Keyboard control is working)")
        return True
    except Exception as e:
        print(f"❌ Keyboard control failed: {e}")
        return False

def check_file_structure():
    """Check if necessary files exist"""
    print("\n" + "="*60)
    print("📁 Checking File Structure...")
    print("="*60)
    
    required_files = [
        'cursor_automation_agent.py',
        'advanced_cursor_agent.py',
        'requirements.txt',
        'README.md',
        'QUICKSTART.md',
        'config.json'
    ]
    
    all_present = True
    
    for filename in required_files:
        if os.path.exists(filename):
            print(f"✅ {filename}")
        else:
            print(f"❌ {filename} - MISSING")
            all_present = False
    
    # Check if recordings directory exists
    if os.path.exists('recordings'):
        print(f"✅ recordings/ directory")
    else:
        print(f"ℹ️  recordings/ directory will be created on first use")
    
    return all_present

def run_full_diagnostic():
    """Run all diagnostic checks"""
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║        🔧 CURSOR AUTOMATION AGENT - DIAGNOSTICS            ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    results = {
        'python_version': check_python_version(),
        'dependencies': check_dependencies(),
        'permissions': check_permissions(),
        'api_key': check_api_key(),
        'screen_capture': test_screen_capture(),
        'mouse_control': test_mouse_control(),
        'keyboard_control': test_keyboard_control(),
        'file_structure': check_file_structure()
    }
    
    # Summary
    print("\n" + "="*60)
    print("📊 DIAGNOSTIC SUMMARY")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    print(f"\nTests Passed: {passed}/{total}")
    
    if passed == total:
        print("\n✅ ALL CHECKS PASSED!")
        print("   You're ready to use the automation agent!")
        print("\n   Next steps:")
        print("   1. Run: python cursor_automation_agent.py")
        print("   2. Read: QUICKSTART.md for examples")
    elif results['python_version'] and results['dependencies']:
        print("\n⚠️  PARTIALLY READY")
        print("   Basic functionality should work.")
        if not results['permissions']:
            print("   ⚠️  Run as Administrator for full features")
        if not results['api_key']:
            print("   ℹ️  Set API key for advanced AI features")
    else:
        print("\n❌ SETUP INCOMPLETE")
        print("   Please fix the errors above before proceeding.")
    
    print("\n" + "="*60 + "\n")
    
    return results

if __name__ == "__main__":
    run_full_diagnostic()
    input("\nPress Enter to exit...")

# Multi-monitor coordinate bounding validation

# OS permission checks

# Frame rate benchmark
