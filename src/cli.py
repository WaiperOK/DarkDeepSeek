"""
CLI интерфейс для my-pentest-gpt
Главная точка входа в приложение
"""
import typer
from typing import Optional
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax
import logging

from .config import ensure_directories
from .prompt_manager import get_template
from .thinker import apply_think, ThinkingEngine
from .generator import get_generator
from .formatter import format_markdown
from .lora_trainer import train_lora

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = typer.Typer(
    name="my-pentest-gpt",
    help="🛡️ AI-инструмент для кибербезопасности на базе DeepSeek-R1-8B",
    epilog="Создано экспертом по кибербезопасности для образовательных целей."
)

console = Console()

@app.command()
def generate(
    task: str = typer.Argument(..., help="Тип задачи (generate_exploit, analyze_vulnerability, etc.)"),
    prompt_set: str = typer.Option("default", "--prompt-set", "-p", help="Набор промптов"),
    model: str = typer.Option("deepseek-r1-8b", "--model", "-m", help="Модель для использования"),
    think: bool = typer.Option(True, "--think/--no-think", help="Включить Chain-of-Thought рассуждения"),
    use_lora: bool = typer.Option(False, "--lora/--no-lora", help="Использовать LoRA адаптер"),
    temperature: float = typer.Option(0.7, "--temp", "-t", help="Температура генерации"),
    max_tokens: int = typer.Option(4096, "--max-tokens", help="Максимальное количество токенов"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Файл для сохранения результата"),
    target: Optional[str] = typer.Option(None, "--target", help="Цель атаки/анализа"),
    custom_prompt: Optional[str] = typer.Option(None, "--custom", help="Пользовательский промпт")
):
    """
    🚀 Генерирует код для задач кибербезопасности
    """
    console.print(Panel.fit(
        "[bold blue]my-pentest-gpt[/] - AI Генератор для Кибербезопасности",
        border_style="blue"
    ))

    try:
        ensure_directories()

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:

            progress.add_task("Загрузка шаблона промпта...", total=None)

            try:
                template_data = get_template(task, prompt_set)
                user_prompt = custom_prompt or template_data["user_template"]

                if target:
                    user_prompt += f"\n\nЦель: {target}"

            except ValueError as e:
                console.print(f"[red]Ошибка загрузки шаблона: {e}[/red]")
                raise typer.Exit(1)

            progress.add_task("Применение Chain-of-Thought...", total=None)

            task_type = _detect_task_type(task)
            enhanced_prompt = apply_think(user_prompt, think, task_type)

            progress.add_task("Загрузка модели...", total=None)

            generator = get_generator(use_lora=use_lora)

            progress.add_task("Генерация кода...", total=None)

            generated_text = generator.generate_with_system_prompt(
                template_data["system_prompt"],
                enhanced_prompt,
                temperature=temperature,
                max_tokens=max_tokens
            )

            progress.add_task("Обработка результата...", total=None)

            thinking_engine = ThinkingEngine()
            code, reasoning = thinking_engine.extract_reasoning(generated_text)

            if not code:
                code = generated_text

        metadata = {
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "lora_enabled": use_lora,
            "thinking_enabled": think
        }

        task_info = {
            "task_name": task,
            "description": template_data.get("description", ""),
            "target": target or "Не указана"
        }

        formatted_result = format_markdown(code, reasoning, task_info, metadata)

        console.print("\n" + "="*60)
        console.print(formatted_result)
        console.print("="*60 + "\n")

        if output:
            output.parent.mkdir(parents=True, exist_ok=True)
            with open(output, 'w', encoding='utf-8') as f:
                f.write(formatted_result)

            console.print(f"[green]✅ Результат сохранен в: {output}[/green]")

        if code:
            console.print("\n[bold]Сгенерированный код:[/bold]")
            syntax = Syntax(code, "python", theme="monokai", line_numbers=True)
            console.print(syntax)

    except Exception as e:
        console.print(f"[red]❌ Ошибка генерации: {e}[/red]")
        logger.error(f"Ошибка генерации: {e}", exc_info=True)
        raise typer.Exit(1)

@app.command()
def train(
    data_path: Optional[Path] = typer.Option(None, "--data", "-d", help="Путь к файлу данных (JSONL)"),
    epochs: int = typer.Option(3, "--epochs", "-e", help="Количество эпох"),
    batch_size: int = typer.Option(8, "--batch-size", "-b", help="Размер батча"),
    learning_rate: float = typer.Option(3e-4, "--lr", help="Скорость обучения")
):
    """
    🎯 Обучает LoRA адаптер на пользовательских данных
    """
    console.print(Panel.fit(
        "[bold green]LoRA Обучение[/] - Специализация модели",
        border_style="green"
    ))

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:

            progress.add_task("Запуск LoRA обучения...", total=None)

            train_lora(
                data_path=data_path,
                epochs=epochs,
                batch_size=batch_size,
                learning_rate=learning_rate
            )

        console.print("[green]✅ LoRA обучение успешно завершено![/green]")

    except Exception as e:
        console.print(f"[red]❌ Ошибка обучения: {e}[/red]")
        logger.error(f"Ошибка обучения: {e}", exc_info=True)
        raise typer.Exit(1)

@app.command()
def list_templates():
    """
    📋 Показывает список доступных шаблонов
    """
    from .prompt_manager import prompt_manager

    templates = prompt_manager.list_templates()

    if not templates:
        console.print("[yellow]⚠️ Шаблоны не найдены[/yellow]")
        return

    console.print("[bold]Доступные шаблоны:[/bold]\n")

    for template in templates:
        console.print(f"• [blue]{template['name']}[/blue]: {template['description']}")

@app.command()
def setup():
    """
    ⚙️ Настраивает рабочую среду и создает структуру директорий
    """
    console.print(Panel.fit(
        "[bold cyan]Настройка my-pentest-gpt[/]",
        border_style="cyan"
    ))

    try:
        ensure_directories()

        _create_default_prompts()

        console.print("[green]✅ Настройка завершена успешно![/green]")
        console.print("\n[bold]Следующие шаги:[/bold]")
        console.print("1. Убедитесь что модель DeepSeek-R1-8B загружена")
        console.print("2. Запустите: [cyan]my-pentest-gpt generate generate_exploit[/cyan]")

    except Exception as e:
        console.print(f"[red]❌ Ошибка настройки: {e}[/red]")
        raise typer.Exit(1)

def _detect_task_type(task: str) -> str:
    """Определяет тип задачи для Chain-of-Thought"""
    if "analyze" in task.lower():
        return "analyze"
    elif "reverse" in task.lower():
        return "reverse"
    else:
        return "exploit"

def _create_default_prompts():
    """Создает файлы промптов по умолчанию"""
    from .config import PROMPTS_DIR
    import json

    default_prompts = {
        "templates": [
            {
                "name": "generate_exploit",
                "description": "Генерация эксплойта для уязвимости",
                "system_prompt": "Ты эксперт по кибербезопасности с 15-летним опытом. Создавай только образовательные PoC-эксплойты. Всегда добавляй предупреждения о безопасности и используй код только для обучения.",
                "user_template": "Создай эксплойт для {vulnerability_type}. Включи:\n1. Описание уязвимости\n2. Proof-of-Concept код\n3. Меры защиты\n4. Рекомендации по исправлению",
                "examples": []
            },
            {
                "name": "analyze_vulnerability",
                "description": "Анализ уязвимости в коде",
                "system_prompt": "Ты эксперт по анализу кода и поиску уязвимостей. Проводи детальный анализ безопасности кода.",
                "user_template": "Проанализируй следующий код на предмет уязвимостей:\n\n{code}\n\nВключи:\n1. Найденные уязвимости\n2. Уровень критичности\n3. Способы эксплуатации\n4. Рекомендации по исправлению",
                "examples": []
            },
            {
                "name": "reverse_engineering",
                "description": "Помощь в реверс-инжиниринге",
                "system_prompt": "Ты эксперт по реверс-инжинирингу и анализу malware. Помогай в легальном анализе программ для образовательных целей.",
                "user_template": "Помоги с реверс-инжинирингом:\n{target_description}\n\nВключи:\n1. Подход к анализу\n2. Инструменты\n3. Методологию\n4. Пример кода для анализа",
                "examples": []
            }
        ]
    }

    default_path = PROMPTS_DIR / "default_prompts.json"
    with open(default_path, 'w', encoding='utf-8') as f:
        json.dump(default_prompts, f, ensure_ascii=False, indent=2)

    console.print(f"[green]✅ Созданы промпты по умолчанию: {default_path}[/green]")

if __name__ == "__main__":
    app()
