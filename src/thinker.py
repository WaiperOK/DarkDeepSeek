import re
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class ThinkingEngine:
    """English docstring"""

    THINKING_PATTERNS = {
        "analyze": [
            "Давайте проаналofируем эту задачу пошагово:",
            "1. Определим цель атаки",
            "2. Выявим потенциальные уязвимости",
            "3. Выберем подходящий метод эксплуатации",
            "4. Создадим payload"
        ],
        "exploit": [
            "Пошаговый план создания эксплойта:",
            "1. Аналof целевой системы",
            "2. Поиск векторов атаки",
            "3. Разработка payload'а",
            "4. Тестирование и валидация",
            "5. Добавление обхода защиты"
        ],
        "reverse": [
            "Методология реверс-инжиниринга:",
            "1. Статический аналof бинарника",
            "2. Поиск точек входа",
            "3. Аналof потока выполнения",
            "4. Выявление критических функций",
            "5. Создание proof-of-concept"
        ]
    }

    def __init__(self):
        self.thinking_enabled = False

    def apply_thinking(self, template: str, task_type: str = "exploit", think: bool = True) -> str:
        """
        Применяет Chain-of-Thought к шаблону промпта

        Args:
            template: Исходный шаблон промпта
            task_type: Type задачи (analyze, exploit, reverse)
            think: Включить ли режим рассуждения

        Returns:
            Модифицированный промпт с Chain-of-Thought
        """
        if not think:
            return template

        thinking_prompt = self._get_thinking_prompt(task_type)

        enhanced_template = f"{thinking_prompt}\n\n{template}"

        enhanced_template += "\n\nВыполните задачу пошагово, объясняя каждый шаг своих рассуждений."

        logger.info(f"Applied Chain-of-Thought for task type: {task_type}")
        return enhanced_template

    def _get_thinking_prompt(self, task_type: str) -> str:
        """English docstring"""
        patterns = self.THINKING_PATTERNS.get(task_type, self.THINKING_PATTERNS["exploit"])
        return "\n".join(patterns)

    def extract_reasoning(self, generated_text: str) -> Tuple[str, Optional[str]]:
        """
        Извлекает код и рассуждения of сгенерированного текста

        Args:
            generated_text: Сгенерированный текст с рассуждениями

        Returns:
            Кортеж (код, рассуждения)
        """
        code_patterns = [
            r'```python(.*?)```',
            r'```bash(.*?)```',
            r'```(?:javascript|js)(.*?)```',
            r'```(?:sql)(.*?)```',
            r'```(?:\w+)?(.*?)```'
        ]

        code_blocks = []
        reasoning_text = generated_text

        for pattern in code_patterns:
            matches = re.findall(pattern, generated_text, re.DOTALL)
            for match in matches:
                clean_code = match.strip()
                if clean_code:
                    code_blocks.append(clean_code)
            reasoning_text = re.sub(pattern, '', reasoning_text, flags=re.DOTALL)

        final_code = "\n\n".join(code_blocks) if code_blocks else ""

        reasoning = self._clean_reasoning(reasoning_text) if reasoning_text.strip() else None

        return final_code, reasoning

    def _clean_reasoning(self, text: str) -> str:
        """English docstring"""
        cleaned = re.sub(r'\n\s*\n', '\n\n', text.strip())

        cleaned = re.sub(r'^\s*[-*#]+\s*', '', cleaned, flags=re.MULTILINE)

        return cleaned

def apply_think(template: str, think: bool = True, task_type: str = "exploit") -> str:
    """
    Удобная функция для применения Chain-of-Thought

    Args:
        template: Шаблон промпта
        think: Включить ли рассуждения
        task_type: Type задачи

    Returns:
        Модифицированный промпт
    """
    engine = ThinkingEngine()
    return engine.apply_thinking(template, task_type, think)

if __name__ == "__main__":
    test_template = "Создай эксплойт для SQL инъекции в веб-приложении"

    result_no_think = apply_think(test_template, think=False)
    print("Без рассуждений:")
    print(result_no_think)
    print("\n" + "="*50 + "\n")

    result_with_think = apply_think(test_template, think=True, task_type="exploit")
    print("С рассуждениями:")
    print(result_with_think)
