"""
🖥️ RETRO START - Максимальный ретро-эффект запуска
Полная имитация компьютера 90-х годов
"""
import os
import sys
import time
import subprocess
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

try:
    from rich.console import Console
    from retro_effects import RetroEffects
except ImportError:
    print("❌ Missing dependencies. Install: pip install -r requirements.txt")
    sys.exit(1)

def retro_startup():
    """English docstring"""
    console = Console(width=80, color_system="256")
    effects = RetroEffects(console)

    os.system('cls' if os.name == 'nt' else 'clear')

    print("🖥️  Initializing CRT display...")
    effects.crt_flicker(1.0)

    print("💾 Starting BIOS sequence...")
    effects.old_computer_startup()

    print("🔍 Checking file system...")
    effects.boot_disk_check()

    print("🌐 Establishing network connection...")
    effects.modem_connection()

    print("🎨 Loading interface...")
    effects.cyber_banner()

    print("👤 Authenticating user...")
    effects.ascii_art_hacker()

    effects.loading_bar_retro("Loading DarkDeepSeek Terminal", 2.0)

    console.print("\n🎉 RETRO STARTUP COMPLETE!", style="bright_green")
    console.print("🚀 Launching main terminal...", style="bright_yellow")
    time.sleep(2)

    try:
        subprocess.run([sys.executable, "run.py"], check=True)
    except KeyboardInterrupt:
        console.print("\n👋 Retro session terminated!", style="bright_cyan")
    except Exception as e:
        console.print(f"\n❌ Error: {e}", style="bright_red")

if __name__ == "__main__":
    retro_startup()
