# 🧠 AI Lab & MLOps Portfolio

> Локальная ИИ-лаборатория и проекты по автоматизации для позиции Junior MLOps / AI Infrastructure Engineer.

## 🖥️ Система
- **ОС**: Windows 11 + WSL 2 (Ubuntu 24.04)
- **CPU/GPU**: AMD Ryzen с интегрированной графикой Radeon Graphics (Vulkan)
- **ОЗУ**: 16 ГБ

---

## 📁 Проекты

### 1. 🐳 AI Infrastructure (Docker Compose)
**Папка:** [`ai-lab/`](ai-lab/)

Полноценная контейнеризованная среда для запуска LLM:
- `docker-compose.yml` — оркестрация Ollama + Open WebUI
- Запуск одной командой: `docker compose up -d`
- Поддержка GPU через Vulkan (локально)

### 2. 🐍 AI Scripts (Python)
**Папка:** [`ai-scripts/`](ai-scripts/)

| Файл | Описание |
|------|----------|
| `telegram_bot.py` | Telegram-бот с историей, сменой модели, inline-кнопками и логированием |
| `rag_bot.py` | RAG-пайплайн на LangChain + ChromaDB для ответов по локальным документам |
| `ru_to_py.py` | Интерактивный переводчик с русского языка на Python-код |
| `test_ollama.py` | Базовый пример запроса к Ollama API |
| `learn_01.py` … `learn_04.py` | Учебные скрипты по основам Python |
| `knowledge.txt` | Тестовая база знаний для RAG |
| `bot_log.txt` | Логи диалогов Telegram-бота |

---

## 🛠️ Технологический стек
- **LLM**: Ollama (llama3.2:3b, tinyllama) с ускорением Vulkan
- **Контейнеризация**: Docker, Docker Compose
- **RAG**: LangChain, ChromaDB, OllamaEmbeddings
- **Боты**: Telegram Bot API, python-telegram-bot
- **ОС и виртуализация**: Windows 11, WSL 2, Ubuntu 24.04

---

## 🔧 Полезные команды

| Действие | Команда |
|----------|---------|
| Запуск Docker-стека | `cd ai-lab && docker compose up -d` |
| Остановка Docker-стека | `cd ai-lab && docker compose down` |
| Запуск Telegram-бота | `cd ai-scripts && py telegram_bot.py` |
| Запуск локальной Ollama | `$env:OLLAMA_VULKAN=1; ollama serve` |

---

## 🎯 Цель
Получить позицию **Junior MLOps-инженера** или **AI Infrastructure Engineer**.  
Открыт к стажировкам и удалённой работе.

📫 **Контакты**: [Telegram](https://t.me/Afrod1z1ak) | [GitHub](https://github.com/Afrodiziak-MLOps)
