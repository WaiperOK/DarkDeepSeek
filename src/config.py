"""
Конфигурация проекта my-pentest-gpt
"""
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
MODEL_PATH = PROJECT_ROOT / "models" / "deepseek-r1-8b"
PROMPTS_DIR = PROJECT_ROOT / "prompts"
DATA_DIR = PROJECT_ROOT / "data" / "exploits"
OUTPUT_DIR = PROJECT_ROOT / "models" / "deepseek-r1-8b-lora"
TESTS_DIR = PROJECT_ROOT / "tests"

MODEL_CONFIG = {
    "model_name": "deepseek-ai/DeepSeek-R1-Distill-Qwen-8B",
    "max_context": 32768,
    "quantization": "4bit",
    "device_map": "auto"
}

GENERATION_CONFIG = {
    "temperature": 0.7,
    "top_k": 50,
    "top_p": 0.9,
    "max_new_tokens": 4096,
    "do_sample": True,
    "pad_token_id": 50256
}

LORA_CONFIG = {
    "r": 16,
    "lora_alpha": 32,
    "lora_dropout": 0.05,
    "target_modules": ["q_proj", "v_proj", "k_proj", "o_proj"]
}

TRAINING_CONFIG = {
    "epochs": 3,
    "batch_size": 8,
    "learning_rate": 3e-4,
    "seq_length": 1024,
    "fp16": True,
    "gradient_accumulation_steps": 4
}

OLLAMA_CONFIG = {
    "base_url": "http://localhost:11434",
    "default_model": "deepseek-r1",
    "timeout": 300,
    "stream": False
}

def ensure_directories():
    """Создает необходимые директории если они не существуют"""
    directories = [
        MODEL_PATH,
        PROMPTS_DIR,
        DATA_DIR,
        OUTPUT_DIR,
        TESTS_DIR
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    ensure_directories()
    print("Структура директорий создана успешно!")
