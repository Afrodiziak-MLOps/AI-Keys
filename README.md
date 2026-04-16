# 🧠 AI Lab — Локальная ИИ-лаборатория MLOps-инженера

> Проект создан в рамках самообучения профессии MLOps-инженера с нуля.

## 🖥️ Система
- **ОС**: Windows 10 + WSL 2 (Ubuntu 24.04)
- **CPU/GPU**: AMD Ryzen с интегрированной графикой Radeon Graphics (Vulkan)
- **ОЗУ**: 16 ГБ

## ✅ Реализовано

### 1. Локальный запуск LLM через Ollama + Vulkan
- Установлен и настроен Vulkan SDK для использования AMD GPU.
- Ollama запускается с флагом `OLLAMA_VULKAN=1`.
- Модели: `llama3.2:3b` (основная), `tinyllama`.

### 2. Автоматизация на Python
- Скрипт `test_ollama.py` — отправка запросов к Ollama API.
- Скрипт `ru_to_py.py` — переводчик с русского языка на Python-код (интерактивный).
- Скрипт `rag_bot.py` — простой RAG-пайплайн с ChromaDB, отвечает на вопросы по локальному файлу `knowledge.txt`.

### 3. Контейнеризация (Docker Compose)
- `docker-compose.yml` поднимает связку:
  - `ollama` (контейнеризованный движок)
  - `open-webui` (веб-интерфейс а-ля ChatGPT)
- Стек запускается одной командой: `docker compose up -d`

### 4. Десктопные интерфейсы
- **AnythingLLM** — подключен к локальной Ollama, работает с GPU.
- **Open WebUI** — развёрнут в Docker, доступен на `http://localhost:3000`.

## 📂 Структура проектов

### `ai-scripts/` — Python-автоматизация
- `test_ollama.py` — базовый запрос к Ollama
- `ru_to_py.py` — интерактивный переводчик русский → Python
- `rag_bot.py` — RAG на ChromaDB
- `learn_01.py` … `learn_04.py` — учебные скрипты по Python

### `ai-lab/` — Docker-инфраструктура
- `docker-compose.yml` — оркестрация Ollama + Open WebUI

## 🔧 Полезные команды

| Действие | Команда |
|----------|---------|
| Запуск Docker-стека | `cd ai-lab && docker compose up -d` |
| Остановка Docker-стека | `cd ai-lab && docker compose down` |
| Скачать модель в контейнер | `docker exec -it ollama ollama pull <model>` |
| Запуск локальной Ollama | `$env:OLLAMA_VULKAN=1; ollama serve` |
| Вход в WSL | `wsl -d Ubuntu-24.04` |

## 🎯 Цель
Получить позицию **Junior MLOps-инженера** или **AI Infrastructure Engineer**.  
Открыт к стажировкам и удалённой работе.
