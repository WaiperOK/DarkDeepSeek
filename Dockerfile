# Используем официальный Python образ с CUDA поддержкой
FROM nvidia/cuda:11.8-devel-ubuntu22.04

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    git \
    wget \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip3 install --upgrade pip
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
RUN pip3 install -r requirements.txt

# Копируем исходный код
COPY src/ ./src/
COPY prompts/ ./prompts/
COPY tests/ ./tests/
COPY data/ ./data/

# Создаем директории для моделей
RUN mkdir -p models/deepseek-r1-8b models/deepseek-r1-8b-lora

# Устанавливаем переменные окружения
ENV PYTHONPATH=/app
ENV CUDA_VISIBLE_DEVICES=0

# Создаем пользователя для безопасности
RUN useradd -m -u 1000 pentester
RUN chown -R pentester:pentester /app
USER pentester

# Устанавливаем точку входа
ENTRYPOINT ["python3", "-m", "src.cli"]

# Метаданные
LABEL maintainer="my-pentest-gpt"
LABEL description="AI-инструмент для кибербезопасности на базе DeepSeek-R1-8B"
LABEL version="1.0.0" 