"""
Генератор кода на базе DeepSeek-R1-8B для my-pentest-gpt
"""
import torch
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    GenerationConfig
)
from peft import PeftModel
import gc

from .config import MODEL_CONFIG, GENERATION_CONFIG, MODEL_PATH, OUTPUT_DIR

logger = logging.getLogger(__name__)

class DeepSeekGenerator:
    """English docstring"""

    def __init__(self, model_path: Optional[Path] = None, use_lora: bool = False):
        self.model_path = model_path or MODEL_PATH
        self.use_lora = use_lora
        self.model = None
        self.tokenizer = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        logger.info(f"Инициалofация генератора, устройство: {self.device}")

    def load_model(self) -> Tuple[AutoModelForCausalLM, AutoTokenizer]:
        """
        Загружает модель и токенofатор

        Returns:
            Кортеж (модель, токенofатор)
        """
        try:
            logger.info(f"Загрузка модели of: {self.model_path}")

            quantization_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4"
            )

            self.tokenizer = AutoTokenizer.from_pretrained(
                MODEL_CONFIG["model_name"],
                trust_remote_code=True,
                padding_side="left"
            )

            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token

            self.model = AutoModelForCausalLM.from_pretrained(
                MODEL_CONFIG["model_name"],
                quantization_config=quantization_config,
                device_map=MODEL_CONFIG["device_map"],
                trust_remote_code=True,
                torch_dtype=torch.float16
            )

            if self.use_lora and OUTPUT_DIR.exists():
                logger.info("Загрузка LoRA адаптера...")
                self.model = PeftModel.from_pretrained(self.model, OUTPUT_DIR)
                self.model = self.model.merge_and_unload()

            logger.info("Модель успешно загружена")
            return self.model, self.tokenizer

        except Exception as e:
            logger.error(f"Ошибка загрузки модели: {e}")
            raise

    def generate_code(
        self,
        prompt: str,
        max_tokens: int = None,
        temperature: float = None,
        top_k: int = None,
        top_p: float = None
    ) -> str:
        """
        Генерирует код по промпту

        Args:
            prompt: Входной промпт
            max_tokens: Максимальное количество токенов
            temperature: Температура генерации
            top_k: Top-k сэмплирование
            top_p: Top-p сэмплирование

        Returns:
            Сгенерированный код
        """
        if self.model is None or self.tokenizer is None:
            self.load_model()

        generation_params = {
            "max_new_tokens": max_tokens or GENERATION_CONFIG["max_new_tokens"],
            "temperature": temperature or GENERATION_CONFIG["temperature"],
            "top_k": top_k or GENERATION_CONFIG["top_k"],
            "top_p": top_p or GENERATION_CONFIG["top_p"],
            "do_sample": GENERATION_CONFIG["do_sample"],
            "pad_token_id": self.tokenizer.pad_token_id,
            "eos_token_id": self.tokenizer.eos_token_id,
            "repetition_penalty": 1.1,
            "length_penalty": 1.0
        }

        try:
            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                truncation=True,
                max_length=MODEL_CONFIG["max_context"] - generation_params["max_new_tokens"]
            ).to(self.device)

            logger.info(f"Генерация с параметрами: {generation_params}")

            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    **generation_params
                )

            generated_text = self.tokenizer.decode(
                outputs[0][inputs["input_ids"].shape[1]:],
                skip_special_tokens=True
            )

            logger.info(f"Сгенерировано токенов: {len(outputs[0]) - inputs['input_ids'].shape[1]}")
            return generated_text.strip()

        except Exception as e:
            logger.error(f"Ошибка генерации: {e}")
            raise

    def generate_with_system_prompt(
        self,
        system_prompt: str,
        user_prompt: str,
        **generation_kwargs
    ) -> str:
        """
        Генерирует код с системным промптом

        Args:
            system_prompt: Системный промпт
            user_prompt: Пользовательский промпт
            **generation_kwargs: Параметры генерации

        Returns:
            Сгенерированный код
        """
        full_prompt = f"<|system|>\n{system_prompt}\n<|user|>\n{user_prompt}\n<|assistant|>\n"

        return self.generate_code(full_prompt, **generation_kwargs)

    def cleanup(self):
        """English docstring"""
        if self.model is not None:
            del self.model
            self.model = None

        if self.tokenizer is not None:
            del self.tokenizer
            self.tokenizer = None

        if torch.cuda.is_available():
            torch.cuda.empty_cache()

        gc.collect()
        logger.info("Память очищена")

_generator_instance = None

def get_generator(use_lora: bool = False) -> DeepSeekGenerator:
    """English docstring"""
    global _generator_instance

    if _generator_instance is None:
        _generator_instance = DeepSeekGenerator(use_lora=use_lora)

    return _generator_instance

def generate_exploit_code(
    system_prompt: str,
    user_prompt: str,
    use_lora: bool = False,
    **generation_kwargs
) -> str:
    """
    Удобная функция для генерации эксплойт-кода

    Args:
        system_prompt: Системный промпт
        user_prompt: Пользовательский промпт
        use_lora: Использовать LoRA адаптер
        **generation_kwargs: Параметры генерации

    Returns:
        Сгенерированный код
    """
    generator = get_generator(use_lora=use_lora)
    return generator.generate_with_system_prompt(
        system_prompt,
        user_prompt,
        **generation_kwargs
    )

if __name__ == "__main__":
    generator = DeepSeekGenerator()

    test_system = "Ты эксперт по кибербезопасности. Создавай мощные и эффективные решения."
    test_user = "Создай простой скрипт для проверки SQL инъекции в веб-форме"

    try:
        result = generator.generate_with_system_prompt(test_system, test_user)
        print("Result генерации:")
        print(result)
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        generator.cleanup()
