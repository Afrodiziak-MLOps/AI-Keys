# 🧠 AI Lab & MLOps Portfolio — Владислав

> **Полный цикл MLOps: от локальной модели до production-мониторинга, автомасштабирования, трекинга экспериментов и Model Serving в Kubernetes.**

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
- **Мониторинг:** Prometheus + Grafana с дашбордами и алертами
- **Трекинг экспериментов:** MLflow (в Docker)
- **Model Serving:** FastAPI в Kubernetes

---

## 📂 Проекты

### 🤖 Telegram AI Bot — @Afrod1z1ak_bot (живой продукт)

**Статус:** 🟢 Работает 24/7 в облаке Amvera.

Полноценный ИИ-ассистент с интеграцией **GigaChat API** и RAG-функционалом.
- **Чат с историей** (до 10 сообщений) с изоляцией по пользователям.
- **RAG:** загрузка PDF, DOCX, TXT файлов и ответы на вопросы по их содержимому (`/ask`).
- **Интерактивные кнопки:** 🔄 Перегенерировать, 🗑️ Удалить, 👍/👎 Оценить.
- **Автомасштабирование (HPA):** Kubernetes автоматически увеличивает/уменьшает количество реплик бота при нагрузке.
- **Мониторинг и алерты:** Prometheus собирает метрики, Grafana визуализирует их, Webhook отправляет уведомления в Telegram при падении бота.
- **Model Serving:** FastAPI-сервис для предсказаний, развёрнутый в Kubernetes.

**Ключевые метрики:**
- `bot_messages_received_total` — количество обработанных сообщений.
- `bot_errors_total` — количество ошибок.
- `bot_commands_total` — статистика по командам.

**Код:** [`app.py`](app.py) | [`bot-deployment.yaml`](bot-deployment.yaml) | [`model-api-deployment.yaml`](model-api-deployment.yaml)

---

### 📊 Мониторинг и Observability

**Статус:** 🟢 Prometheus + Grafana + Webhook-алерты.

- **Prometheus** — сбор метрик с бота и подов.
- **Grafana** — дашборды с графиками в реальном времени.
- **Webhook-алерты** — уведомления в Telegram при падении бота.
- **HPA** — горизонтальное автомасштабирование подов бота по CPU.

**Манифесты:** [`monitoring.yaml`](monitoring.yaml) | [`bot-service.yaml`](bot-service.yaml) | [`webhook-deployment.yaml`](webhook-deployment.yaml)

---

### 🧪 Трекинг экспериментов (MLflow)

**Статус:** 🟢 Развёрнут в Docker.

- **Отслеживание гиперпараметров** и метрик при обучении моделей.
- **Визуализация** результатов экспериментов.
- **Интегрирован** с CI/CD пайплайном (GitHub Actions).

**Код:** [`docker-compose.yml`](docker-compose.yml) | [`train.py`](train.py)

---

### 🚀 Model Serving (FastAPI + Kubernetes)

**Статус:** 🟢 Развёрнут в Kubernetes.

- **FastAPI-сервис** для предсказаний (IrisClassifier).
- **Docker-образ** и **Kubernetes-манифесты** (Deployment + Service).
- **Готов к интеграции** с MLflow Model Registry.

**Код:** [`serve_model.py`](serve_model.py) | [`Dockerfile.api`](Dockerfile.api) | [`model-api-deployment.yaml`](model-api-deployment.yaml)

---

### 🐳 AI Infrastructure (Kubernetes + Docker)

**Статус:** Готов к локальному развертыванию.

- **Docker Compose:** `ollama` + `open-webui` + `mlflow` + `minio` для экспериментов.
- **Kubernetes:** `Deployment`, `Service`, `Secret`, `ConfigMap`, `HPA` для оркестрации бота, мониторинга и Model Serving.
- **Запуск:** `docker compose up -d` или `kubectl apply -f .`

**Код:** [`ai-lab/`](ai-lab/) | [`bot-deployment.yaml`](bot-deployment.yaml) | [`monitoring.yaml`](monitoring.yaml)

---

### 🐍 AI Scripts (Python-автоматизация)

| Файл | Описание |
| :--- | :--- |
| `model_deployer.py` | **CI/CD-скрипт.** Проверяет наличие модели, скачивает и тестирует её. |
| `rag_bot.py` | **RAG-пайплайн.** Ответы на вопросы по локальным документам (LangChain + ChromaDB + Ollama). |
| `ru_to_py.py` | **Переводчик.** Конвертирует задачи с русского языка в Python-код с помощью LLM. |
| `train.py` | **Трекинг экспериментов.** Регистрирует гиперпараметры и метрики в MLflow. |
| `serve_model.py` | **Model Serving.** FastAPI-сервис для предсказаний. |
| `learn_01.py … learn_04.py` | **Учебные скрипты.** Переменные, циклы, условия, функции, работа с файлами. |

---

## 🛠️ Ключевые навыки

**Языки:** Python 3, Bash, PowerShell  
**Инфраструктура:** Docker, Docker Compose, Kubernetes (minikube), WSL2, Linux (Ubuntu), Git/GitHub  
**ML/LLM:** Ollama (Vulkan), GigaChat API, LangChain, ChromaDB, Prompt Engineering  
**MLOps:** MLflow, CI/CD (GitHub Actions), HPA (автомасштабирование), IaC, Model Serving (FastAPI)  
**Мониторинг:** Prometheus, Grafana, Webhook-алерты, экспорт метрик из Python (prometheus-client)  
**Сети и безопасность:** REST API, HTTP/HTTPS, работа с секретами и переменными окружения

---

## 🎯 Цель

Ищу позицию **Junior MLOps-инженера**, **Python-разработчика (AI)** или **AI Infrastructure Engineer**.  
Открыт к стажировкам, удалённой работе и интересным проектам.

📫 **Контакты:**  
- Telegram: [@Afrod1z1ak](https://t.me/Afrod1z1ak)  
- GitHub: [Afrodiziak-MLOps](https://github.com/Afrodiziak-MLOps)

