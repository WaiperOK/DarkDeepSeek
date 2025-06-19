
import subprocess
import sys
from pathlib import Path

def main():
    script_path = Path(__file__).parent / "run.py"

    try:
        subprocess.run([sys.executable, str(script_path)], check=True)
    except KeyboardInterrupt:
        print("\n👋 До свидания!")
    except Exception as e:
        print(f"❌ Ошибка запуска: {e}")

if __name__ == "__main__":
    main()
