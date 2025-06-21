"""
Менеджер промптов для my-pentest-gpt
Загружает и валидирует шаблоны of JSON файлов
"""
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from pydantic import BaseModel, field_validator

from .config import PROMPTS_DIR

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PromptTemplate(BaseModel):
    """English docstring"""
    name: str
    description: str
    system_prompt: str
    user_template: str
    examples: Optional[list] = []

    @field_validator('system_prompt', 'user_template')
    @classmethod
    def validate_non_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Промпт не может быть пустым")
        return v.strip()

class PromptManager:
    """English docstring"""

    def __init__(self, prompts_dir: Path = PROMPTS_DIR):
        self.prompts_dir = prompts_dir
        self._templates_cache = {}
        self._load_all_templates()

    def _load_all_templates(self):
        """English docstring"""
        if not self.prompts_dir.exists():
            logger.warning(f"Директория промптов не найдена: {self.prompts_dir}")
            return

        for json_file in self.prompts_dir.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                if not isinstance(data, dict) or 'templates' not in data:
                    logger.error(f"Invalid file structure {json_file}")
                    continue

                for template_data in data['templates']:
                    try:
                        template = PromptTemplate(**template_data)
                        self._templates_cache[template.name] = template
                        logger.info(f"Template loaded: {template.name}")
                    except Exception as e:
                        logger.error(f"Error loading template {template_data.get('name', 'unknown')}: {e}")

            except Exception as e:
                logger.error(f"Error reading file {json_file}: {e}")

    def get_template(self, task_name: str, prompt_set: str = "default") -> Optional[PromptTemplate]:
        """
        Получает шаблон по имени задачи

        Args:
            task_name: Имя задачи
            prompt_set: Набор промптов (пока не используется)

        Returns:
            Объект PromptTemplate или None
        """
        return self._templates_cache.get(task_name)

    def load_template(self, task_name: str, prompt_set: str = "default") -> Dict[str, Any]:
        """
        Загружает шаблон по имени задачи

        Args:
            task_name: Имя задачи (generate_exploit, analyze_vulnerability, etc.)
            prompt_set: Набор промптов (default, custom)

        Returns:
            Словарь с данными шаблона
        """
        template_key = f"{prompt_set}_{task_name}"

        if template_key not in self._templates_cache:
            if task_name in self._templates_cache:
                template_key = task_name
            else:
                available = list(self._templates_cache.keys())
                raise ValueError(f"Шаблон '{template_key}' не найден. Доступные: {available}")

        template = self._templates_cache[template_key]
        return {
            "name": template.name,
            "description": template.description,
            "system_prompt": template.system_prompt,
            "user_template": template.user_template,
            "examples": template.examples
        }

    def list_templates(self) -> list:
        """English docstring"""
        return [
            {
                "name": template.name,
                "description": template.description
            }
            for template in self._templates_cache.values()
        ]

    def reload_templates(self):
        """English docstring"""
        self._templates_cache.clear()
        self._load_all_templates()
        logger.info("Шаблоны перезагружены")

prompt_manager = PromptManager()

def get_template(task_name: str, prompt_set: str = "default") -> Dict[str, Any]:
    """English docstring"""
    return prompt_manager.load_template(task_name, prompt_set)

if __name__ == "__main__":
    manager = PromptManager()
    templates = manager.list_templates()
    print(f"Загружено шаблонов: {len(templates)}")
    for template in templates:
        print(f"- {template['name']}: {template['description']}")
