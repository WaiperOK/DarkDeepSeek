"""
Генератор кода на базе Ollama для my-pentest-gpt
Поддержка локальных моделей DeepSeek через Ollama
"""
import requests
import json
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path

from .config import OLLAMA_CONFIG, GENERATION_CONFIG

logger = logging.getLogger(__name__)

class OllamaGenerator:
    """English docstring"""

    def __init__(self,
                 base_url: str = "http://localhost:11434",
                 model_name: str = "deepseek-r1"):
        self.base_url = base_url.rstrip('/')
        self.model_name = model_name
        self.session = requests.Session()

        logger.info(f"Ollama generator initialization: {self.base_url}")
        logger.info(f"Model: {self.model_name}")

    def check_connection(self) -> bool:
        """English docstring"""
        try:
            response = self.session.get(f"{self.base_url}/api/tags")
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Ollama connection error: {e}")
            return False

    def list_models(self) -> List[Dict[str, Any]]:
        """English docstring"""
        try:
            response = self.session.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                return response.json().get("models", [])
            return []
        except Exception as e:
            logger.error(f"Error getting models list: {e}")
            return []

    def pull_model(self, model_name: str = None) -> bool:
        """English docstring"""
        model = model_name or self.model_name

        try:
            logger.info(f"Загрузка модели {model}...")

            response = self.session.post(
                f"{self.base_url}/api/pull",
                json={"name": model},
                stream=True
            )

            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        data = json.loads(line)
                        if "status" in data:
                            logger.info(f"Статус: {data['status']}")
                        if data.get("status") == "success":
                            logger.info(f"Модель {model} успешно загружена")
                            return True

            return False

        except Exception as e:
            logger.error(f"Model loading error: {e}")
            return False

    def generate_code(self,
                     prompt: str,
                     system_prompt: Optional[str] = None,
                     temperature: float = None,
                     max_tokens: int = None,
                     stream: bool = False) -> str:
        """
        Генерирует код через Ollama API

        Args:
            prompt: Пользовательский промпт
            system_prompt: Системный промпт
            temperature: Температура генерации
            max_tokens: Максимальное количество токенов
            stream: Потоковая генерация

        Returns:
            Сгенерированный код
        """

        options = {
            "temperature": temperature or GENERATION_CONFIG["temperature"],
            "top_k": GENERATION_CONFIG["top_k"],
            "top_p": GENERATION_CONFIG["top_p"],
            "num_predict": max_tokens or GENERATION_CONFIG["max_new_tokens"]
        }

        request_data = {
            "model": self.model_name,
            "prompt": prompt,
            "options": options,
            "stream": stream
        }

        if system_prompt:
            request_data["system"] = system_prompt

        try:
            logger.info(f"Generation with parameters: {options}")

            response = self.session.post(
                f"{self.base_url}/api/generate",
                json=request_data,
                timeout=300
            )

            if response.status_code == 200:
                if stream:
                    return self._handle_stream_response(response)
                else:
                    result = response.json()
                    response_text = result.get("response", "")
                    return self._clean_thinking_blocks(response_text)
            else:
                logger.error(f"API error: {response.status_code} - {response.text}")
                return ""

        except Exception as e:
            logger.error(f"Ошибка генерации: {e}")
            return ""

    def _clean_thinking_blocks(self, text: str) -> str:
        """English docstring"""
        import re

        def shorten_think_block(match):
            think_content = match.group(1).strip()
            lines = think_content.split('\n')

            if len(lines) > 4:
                shortened = '\n'.join(lines[:3]) + '\n...'
            else:
                shortened = think_content

            return f"<think>\n{shortened}\n</think>"

        cleaned = re.sub(r'<think>(.*?)</think>', shorten_think_block, text, flags=re.DOTALL | re.IGNORECASE)

        cleaned = re.sub(r'\n\s*\n\s*\n', '\n\n', cleaned)

        return cleaned.strip()

    def _handle_stream_response(self, response) -> str:
        """English docstring"""
        full_response = ""

        try:
            for line in response.iter_lines():
                if line:
                    data = json.loads(line)
                    if "response" in data:
                        chunk = data["response"]
                        full_response += chunk
                        print(chunk, end="", flush=True)

                    if data.get("done", False):
                        break

            return self._clean_thinking_blocks(full_response)

        except Exception as e:
            logger.error(f"Stream processing error: {e}")
            return self._clean_thinking_blocks(full_response)

    def generate_with_system_prompt(self,
                                   system_prompt: str,
                                   user_prompt: str,
                                   **generation_kwargs) -> str:
        """
        Генерирует код с системным промптом

        Args:
            system_prompt: Системный промпт
            user_prompt: Пользовательский промпт
            **generation_kwargs: Параметры генерации

        Returns:
            Сгенерированный код
        """
        return self.generate_code(
            user_prompt,
            system_prompt=system_prompt,
            **generation_kwargs
        )

    def chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """
        Чат-интерфейс для генерации

        Args:
            messages: Список сообщений в формате [{"role": "user", "content": "..."}]
            **kwargs: Параметры генерации

        Returns:
            Ответ модели
        """

        system_messages = [msg["content"] for msg in messages if msg["role"] == "system"]
        user_messages = [msg["content"] for msg in messages if msg["role"] == "user"]

        system_prompt = "\n".join(system_messages) if system_messages else None
        user_prompt = "\n".join(user_messages)

        return self.generate_code(
            user_prompt,
            system_prompt=system_prompt,
            **kwargs
        )

_ollama_generator = None

def get_ollama_generator(model_name: str = None) -> OllamaGenerator:
    """English docstring"""
    global _ollama_generator

    if _ollama_generator is None:
        _ollama_generator = OllamaGenerator(model_name=model_name)

    return _ollama_generator

def setup_ollama_model(model_name: str = "deepseek-r1") -> bool:
    """
    Настраивает модель в Ollama

    Args:
        model_name: Имя модели для загрузки

    Returns:
        True если модель готова к использованию
    """
    generator = get_ollama_generator(model_name)

    if not generator.check_connection():
        logger.error("Ollama не запущена или недоступна")
        return False

    models = generator.list_models()
    model_names = [model["name"] for model in models]

    if model_name not in model_names and f"{model_name}:latest" not in model_names:
        logger.info(f"Модель {model_name} не найдена, загружаем...")
        if not generator.pull_model(model_name):
            logger.error(f"Не удалось загрузить модель {model_name}")
            return False

    logger.info(f"Модель {model_name} готова к использованию")
    return True

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Тест Ollama генератора")
    parser.add_argument("--model", default="deepseek-r1", help="Имя модели")
    parser.add_argument("--prompt", default="Создай простой Python скрипт", help="Тестовый промпт")
    parser.add_argument("--setup", action="store_true", help="Настроить модель")

    args = parser.parse_args()

    if args.setup:
        success = setup_ollama_model(args.model)
        if success:
            print(f"✅ Модель {args.model} настроена")
        else:
            print(f"❌ Ошибка настройки модели {args.model}")
    else:
        generator = get_ollama_generator(args.model)
        result = generator.generate_code(args.prompt)
        print("Result:")
        print(result)
