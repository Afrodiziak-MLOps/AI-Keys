# 🧠 AI Lab & MLOps Portfolio — Владислав

> **Полный цикл MLOps: от локальной модели до production-мониторинга в Kubernetes.**

[![CI/CD Pipeline](https://github.com/Afrodiziak-MLOps/AI-Keys/actions/workflows/test_model.yml/badge.svg)](https://github.com/Afrodiziak-MLOps/AI-Keys/actions/workflows/test_model.yml)

---

## 🖥️ Система и стек

**Локально:**
- **ОС:** Windows 10 + WSL 2 (Ubuntu 24.04)
- **GPU:** AMD Radeon Graphics (ускорение через Vulkan)
- **Контейнеризация:** Docker, Docker Compose, Kubernetes (minikube)
- **ML-движок:** Ollama (`llama3.2:3b`, `tinyllama`)

**Облако:**
- **Платформа:** Amvera Cloud (24/7)
- **LLM API:** GigaChat (Сбер)
- **CI/CD:** GitHub Actions
- **Мониторинг:** Prometheus + Grafana (в Kubernetes)

---

## 📂 Проекты

### 🤖 Telegram AI Bot — @Afrod1z1ak_bot (живой продукт)

**Статус:** 🟢 Работает 24/7 в облаке Amvera и в Kubernetes.

Полноценный ИИ-ассистент с интеграцией **GigaChat API** и production-мониторингом.
- **История диалога** (до 10 сообщений) с изоляцией по пользователям.
- **Интерактивные кнопки:** 🔄 Перегенерировать, 🗑️ Удалить, 👍/👎 Оценить.
- **Отказоустойчивость:** автоматические повторы при сетевых ошибках (503).
- **Логирование:** все диалоги и оценки сохраняются в `/data/bot_log.txt`.
- **Безопасность:** токены и ключи API вынесены в секреты Kubernetes/Amvera.
- **Мониторинг:** Prometheus собирает метрики, Grafana визуализирует их в реальном времени.

**Ключевые метрики:**
- `bot_messages_received_total` — количество обработанных сообщений
- `bot_errors_total` — количество ошибок
- `bot_commands_total` — статистика по командам (`/start`, `/help`)

**Код:** [`main.py`](main.py) | [`bot-deployment.yaml`](bot-deployment.yaml)

---

### 📊 Мониторинг (Prometheus + Grafana)

**Статус:** 🟢 Развёрнут в Kubernetes.

Полноценный стек мониторинга для отслеживания состояния бота и инфраструктуры.
- **Prometheus** — сбор метрик с бота и подов (`:8000/metrics`).
- **Grafana** — дашборды с графиками в реальном времени.
- **Автоматическое обнаружение сервисов** через `telegram-bot-service`.

**Манифесты:** [`monitoring.yaml`](monitoring.yaml) | [`bot-service.yaml`](bot-service.yaml)

---

### 🐳 AI Infrastructure (Kubernetes + Docker)

**Статус:** Готов к локальному развертыванию.

- **Docker Compose:** `ollama` + `open-webui` для экспериментов с локальными LLM.
- **Kubernetes:** `Deployment`, `Service`, `Secret`, `ConfigMap` для оркестрации бота и мониторинга.
- **Запуск:** `docker compose up -d` или `kubectl apply -f .`

**Код:** [`ai-lab/`](ai-lab/) | [`bot-deployment.yaml`](bot-deployment.yaml) | [`monitoring.yaml`](monitoring.yaml)

---

### 🐍 AI Scripts (Python-автоматизация)

Коллекция скриптов для работы с LLM и автоматизации MLOps-задач.

| Файл | Описание |
| :--- | :--- |
| `model_deployer.py` | **CI/CD-скрипт.** Проверяет наличие модели, при необходимости скачивает и тестирует её. Интегрирован в GitHub Actions. |
| `rag_bot.py` | **RAG-пайплайн.** Ответы на вопросы по локальным документам (LangChain + ChromaDB + Ollama). |
| `ru_to_py.py` | **Переводчик.** Конвертирует задачи с русского языка в Python-код с помощью LLM. |
| `learn_01.py … learn_04.py` | **Учебные скрипты.** Переменные, циклы, условия, функции, работа с файлами. |

---

## 🛠️ Ключевые навыки

**Языки:** Python 3, Bash, PowerShell  
**Инфраструктура:** Docker, Docker Compose, Kubernetes (minikube), WSL2, Linux (Ubuntu), Git/GitHub  
**ML/LLM:** Ollama (Vulkan), GigaChat API, LangChain, ChromaDB, Prompt Engineering  
**CI/CD & Деплой:** GitHub Actions, Amvera Cloud, Kubernetes (Deployment, Service, Secret)  
**Мониторинг:** Prometheus, Grafana, экспорт метрик из Python (prometheus-client)  
**Сети и безопасность:** REST API, HTTP/HTTPS, работа с секретами и переменными окружения

---

## 🎯 Цель

Ищу позицию **Junior MLOps-инженера**, **Python-разработчика (AI)** или **AI Infrastructure Engineer**.  
Открыт к стажировкам, удалённой работе и интересным проектам.

📫 **Контакты:**  
- Telegram: [@Afrod1z1ak](https://t.me/Afrod1z1ak)  
- GitHub: [Afrodiziak-MLOps](https://github.com/Afrodiziak-MLOps)

---
*Это портфолио — результат интенсивной практики и осознанного перехода в IT из гуманитарной сферы.*
