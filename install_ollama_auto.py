"""
🔧 Автоматический установщик Ollama
Для Windows, Linux и macOS
"""
import os
import sys
import platform
import subprocess
import urllib.request
import tempfile
from pathlib import Path

def get_system_info():
    """English docstring"""
    system = platform.system().lower()
    arch = platform.machine().lower()

    if arch in ['x86_64', 'amd64']:
        arch = 'amd64'
    elif arch in ['aarch64', 'arm64']:
        arch = 'arm64'
    else:
        arch = 'unknown'

    return system, arch

def check_ollama_installed():
    """English docstring"""
    try:
        result = subprocess.run(['ollama', '--version'],
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            return True, result.stdout.strip()
    except:
        pass
    return False, None

def install_ollama_windows():
    """English docstring"""
    print("🔧 Установка Ollama для Windows...")

    url = "https://ollama.ai/download/windows"

    try:
        print("📥 Загрузка установщика...")
        with tempfile.NamedTemporaryFile(suffix='.exe', delete=False) as tmp_file:
            urllib.request.urlretrieve(url, tmp_file.name)
            installer_path = tmp_file.name

        print("🚀 Запуск установщика...")
        print("⚠️  Следуйте инструкциям установщика")

        subprocess.run([installer_path], check=True)

        os.unlink(installer_path)

        print("✅ Установка завершена!")
        return True

    except Exception as e:
        print(f"❌ Ошибка установки: {e}")
        return False

def install_ollama_linux():
    """English docstring"""
    print("🔧 Установка Ollama для Linux...")

    try:
        print("📥 Загрузка и запуск установочного скрипта...")

        cmd = "curl -fsSL https://ollama.ai/install.sh | sh"
        result = subprocess.run(cmd, shell=True, check=True)

        print("✅ Установка завершена!")
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка установки: {e}")
        print("💡 Попробуйте установить вручную:")
        print("   curl -fsSL https://ollama.ai/install.sh | sh")
        return False

def install_ollama_macos():
    """English docstring"""
    print("🔧 Установка Ollama для macOS...")

    try:
        subprocess.run(['brew', '--version'],
                      capture_output=True, check=True)
        homebrew_available = True
    except:
        homebrew_available = False

    if homebrew_available:
        try:
            print("🍺 Установка через Homebrew...")
            subprocess.run(['brew', 'install', 'ollama'], check=True)
            print("✅ Установка завершена!")
            return True
        except subprocess.CalledProcessError:
            print("⚠️  Ошибка установки через Homebrew, пробуем альтернативный способ...")

    try:
        print("📥 Загрузка и запуск установочного скрипта...")
        cmd = "curl -fsSL https://ollama.ai/install.sh | sh"
        subprocess.run(cmd, shell=True, check=True)
        print("✅ Установка завершена!")
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка установки: {e}")
        print("💡 Попробуйте установить вручную:")
        print("   Скачайте с https://ollama.ai/download/mac")
        return False

def start_ollama_service():
    """English docstring"""
    print("🚀 Запуск Ollama...")

    system = platform.system().lower()

    try:
        if system == "windows":
            subprocess.Popen(['ollama', 'serve'],
                           creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            subprocess.Popen(['ollama', 'serve'],
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)

        print("✅ Ollama запущена!")
        return True

    except Exception as e:
        print(f"⚠️  Ошибка запуска: {e}")
        return False

def pull_deepseek_model():
    """English docstring"""
    print("📦 Загрузка модели deepseek-r1:8b...")
    print("⏳ Это может занять несколько минут (~5GB)...")

    try:
        process = subprocess.Popen(
            ['ollama', 'pull', 'deepseek-r1:8b'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )

        for line in process.stdout:
            if line.strip():
                print(f"📥 {line.strip()}")

        process.wait()

        if process.returncode == 0:
            print("✅ Модель deepseek-r1:8b загружена!")
            return True
        else:
            print("❌ Ошибка загрузки модели")
            return False

    except Exception as e:
        print(f"❌ Ошибка загрузки модели: {e}")
        return False

def main():
    """English docstring"""
    print("🖥️  DarkDeepSeek - Автоустановщик Ollama")
    print("=" * 50)

    system, arch = get_system_info()
    print(f"🔍 Система: {system.title()} {arch}")

    is_installed, version = check_ollama_installed()

    if is_installed:
        print(f"✅ Ollama уже установлена: {version}")
    else:
        print("📦 Ollama не найдена, начинаем установку...")

        if system == "windows":
            success = install_ollama_windows()
        elif system == "linux":
            success = install_ollama_linux()
        elif system == "darwin":
            success = install_ollama_macos()
        else:
            print(f"❌ Неподдерживаемая система: {system}")
            return False

        if not success:
            print("❌ Установка Ollama не удалась")
            return False

        print("🔍 Проверка установки...")
        time.sleep(2)
        is_installed, version = check_ollama_installed()

        if not is_installed:
            print("❌ Ollama не была установлена корректно")
            return False

        print(f"✅ Ollama установлена: {version}")

    if not start_ollama_service():
        print("⚠️  Не удалось запустить Ollama автоматически")
        print("💡 Запустите вручную: ollama serve")

    print("⏳ Ожидание запуска сервиса...")
    time.sleep(5)

    if not pull_deepseek_model():
        print("⚠️  Не удалось загрузить модель автоматически")
        print("💡 Загрузите вручную: ollama pull deepseek-r1:8b")
        return False

    print("\n🎉 Установка завершена успешно!")
    print("🚀 Теперь можете запустить: python start.py")
    print("   или: ./start.bat (Windows) / ./start.sh (Linux/macOS)")

    return True

if __name__ == "__main__":
    import time
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ Установка прервана пользователем")
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")

    input("\nНажмите Enter для выхода...")
