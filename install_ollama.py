"""
Скрипт автоматической установки Ollama и DeepSeek-R1-8B
Быстрый запуск my-pentest-gpt с локальными моделями
"""
import os
import sys
import subprocess
import platform
import requests
from pathlib import Path

def print_step(message: str):
    """English docstring"""
    print(f"\n🔧 {message}")
    print("=" * 50)

def run_command(command: str, check: bool = True) -> bool:
    """English docstring"""
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка выполнения команды: {e}")
        if e.stderr:
            print(f"Stderr: {e.stderr}")
        return False

def check_ollama_installed() -> bool:
    """English docstring"""
    try:
        result = subprocess.run(["ollama", "--version"], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def install_ollama():
    """English docstring"""
    system = platform.system().lower()

    if system == "linux":
        print("Установка Ollama для Linux...")
        return run_command("curl -fsSL https://ollama.ai/install.sh | sh")

    elif system == "darwin":
        print("Установка Ollama для macOS...")
        print("Загружаем Ollama.app...")
        if run_command("which brew", check=False):
            return run_command("brew install ollama")
        else:
            print("❌ Homebrew не найден. Установите Ollama вручную:")
            print("https://ollama.ai/download/mac")
            return False

    elif system == "windows":
        print("Для Windows скачайте Ollama с официального сайта:")
        print("https://ollama.ai/download/windows")
        print("После установки перезапустите этот скрипт.")
        return False

    else:
        print(f"❌ Неподдерживаемая ОС: {system}")
        return False

def start_ollama_service():
    """English docstring"""
    print("Запуск сервиса Ollama...")

    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama уже запущена")
            return True
    except:
        pass

    system = platform.system().lower()

    if system in ["linux", "darwin"]:
        subprocess.Popen(["ollama", "serve"],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)

        import time
        for i in range(30):
            try:
                response = requests.get("http://localhost:11434/api/tags", timeout=2)
                if response.status_code == 200:
                    print("✅ Ollama сервис запущен")
                    return True
            except:
                pass
            time.sleep(1)
            print(f"Ожидание запуска... {i+1}/30")

        print("❌ Не удалось запустить Ollama сервис")
        return False

    else:
        print("Запустите Ollama вручную: ollama serve")
        return True

def pull_deepseek_model():
    """English docstring"""
    print("Загрузка DeepSeek-R1-8B модели...")
    print("⚠️ Это может занять несколько минут (модель ~5GB)")

    models_to_try = [
        "deepseek-r1:8b-distill-q4_K_M",
        "deepseek-r1:8b",
        "deepseek-r1",
        "deepseek-coder:6.7b-instruct-q4_K_M"
    ]

    for model in models_to_try:
        print(f"Попытка загрузки: {model}")
        if run_command(f"ollama pull {model}", check=False):
            print(f"✅ Модель {model} успешно загружена!")
            return model
        else:
            print(f"❌ Не удалось загрузить {model}")

    print("❌ Не удалось загрузить ни одну модель DeepSeek")
    print("Попробуйте вручную:")
    print("ollama pull deepseek-coder:6.7b-instruct-q4_K_M")
    return None

def test_installation():
    """English docstring"""
    print("Тестирование установки...")

    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=10)
        if response.status_code != 200:
            print("❌ Ollama API недоступно")
            return False

        models = response.json().get("models", [])
        if not models:
            print("❌ Модели не найдены")
            return False

        print("✅ Найдены модели:")
        for model in models:
            print(f"  • {model.get('name', 'Unknown')}")

        print("\nТестирование генерации...")
        test_data = {
            "model": models[0]["name"],
            "prompt": "Напиши простую функцию Hello World на Python:",
            "options": {"num_predict": 100}
        }

        response = requests.post(
            "http://localhost:11434/api/generate",
            json=test_data,
            timeout=60
        )

        if response.status_code == 200:
            result = response.json()
            generated_text = result.get("response", "")
            if generated_text:
                print("✅ Тест генерации прошел успешно!")
                print("Пример генерации:")
                print("-" * 30)
                print(generated_text[:200] + "..." if len(generated_text) > 200 else generated_text)
                print("-" * 30)
                return True

        print("❌ Тест генерации не прошел")
        return False

    except Exception as e:
        print(f"❌ Ошибка тестирования: {e}")
        return False

def setup_my_pentest_gpt():
    """English docstring"""
    print("Настройка my-pentest-gpt...")

    if not Path("src").exists():
        print("❌ Запустите скрипт of корневой директории проекта")
        return False

    print("Установка Python зависимостей...")
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt"):
        print("❌ Ошибка установки зависимостей")
        return False

    print("Создание структуры директорий...")
    if not run_command(f"{sys.executable} src/config.py"):
        print("❌ Ошибка создания директорий")
        return False

    print("✅ my-pentest-gpt настроен!")
    return True

def main():
    """English docstring"""
    print("🛡️ Установка my-pentest-gpt с Ollama + DeepSeek-R1-8B")
    print("=" * 60)

    print_step("Проверка Ollama")
    if not check_ollama_installed():
        print("Ollama не найдена, устанавливаем...")
        if not install_ollama():
            print("❌ Не удалось установить Ollama")
            sys.exit(1)
    else:
        print("✅ Ollama уже установлена")

    print_step("Запуск Ollama сервиса")
    if not start_ollama_service():
        print("❌ Не удалось запустить Ollama")
        print("Попробуйте вручную: ollama serve")
        sys.exit(1)

    print_step("Загрузка DeepSeek модели")
    model_name = pull_deepseek_model()
    if not model_name:
        print("❌ Не удалось загрузить модель")
        sys.exit(1)

    print_step("Настройка my-pentest-gpt")
    if not setup_my_pentest_gpt():
        print("❌ Ошибка настройки проекта")
        sys.exit(1)

    print_step("Тестирование установки")
    if not test_installation():
        print("❌ Тесты не прошли")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("🎉 УСТАНОВКА ЗАВЕРШЕНА УСПЕШНО!")
    print("=" * 60)

    print(f"\n✅ Установленная модель: {model_name}")
    print("✅ Ollama сервис запущен")
    print("✅ my-pentest-gpt готов к использованию")

    print("\n🚀 ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ:")
    print("-" * 30)
    examples = [
        "python -m src.cli_ollama generate generate_exploit --target 'SQL injection в форме входа'",
        "python -m src.cli_ollama generate analyze_vulnerability --target 'XSS в комментариях'",
        "python -m src.cli_ollama chat",
        "python -m src.cli_ollama list-templates",
        "python -m src.cli_ollama list-models",
    ]
    for cmd in examples:
        print(cmd)

    print("\n📚 ДОКУМЕНТАЦИЯ:")
    print("README.md - полная документация")
    print("src/cli_ollama.py - CLI с Ollama")

    print("\n⚠️ ЭТИЧЕСКОЕ ИСПОЛЬЗОВАНИЕ:")
    print("Используйте только для образовательных целей")
    print("и этичного тестирования безопасности!")

if __name__ == "__main__":
    main()
