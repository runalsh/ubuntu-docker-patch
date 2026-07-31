# Ubuntu Docker Patch Images

Автоматизированная сборка Docker-образов с точной фиксированной патч-версией (point release) Ubuntu (**22.04.0** .. **22.04.5**, **24.04.0** .. **24.04.4**).

---

## ❓ Какую проблему решает проект

В официальном Docker Hub реестре (`library/ubuntu`) публикуются **только мажорные теги** (например, `ubuntu:22.04`, `ubuntu:24.04`, `jammy`, `noble`).

Официальных тегов вида `ubuntu:22.04.1`, `ubuntu:22.04.5` или `ubuntu:24.04.2` **не существует**, так как мейнтейнеры регулярно обновляют существующие теги до самых свежих пакетов.

### Проблемы:
1. **Тестирование на конкретных версиях дистрибутивов**: Нельзя запустить тесты или симулировать окружение, зафиксированное на конкретном минорном релизе (например, `22.04.1` или `24.04.2`).
2. **Воспроизводимость сборок**: Образ `ubuntu:22.04` со временем меняется из-за обновления пакетов в базовом образе Docker, что может маскировать или изменять поведение тестируемого ПО.
3. **Аудит безопасности и форензика**: Сложно воспроизвести окружение системы на момент выхода конкретного релиза.

---

## 🚀 Решение

Данный репозиторий решает эту проблему следующим образом:
- Использует официальные архивы корневой файловой системы (**rootfs tar.xz**) напрямую от Canonical (`cloud-images.ubuntu.com`).
- Формирует и валидирует чистые Docker-образы для каждой точной минорной версии Ubuntu LTS.
- Автоматически проверяет соответствие `/etc/os-release` запрашиваемому тегу перед публикацией.
- Автоматически публицирует готовые Docker-образы в Docker Hub: **`runalsh/ubuntu-docker-patch`**.

---

## 📦 Доступные образы и теги

### Ubuntu 22.04 LTS (Jammy Jellyfish)

| Тег | Версия в `/etc/os-release` | Базовый релиз Canonical |
|---|---|---|
| `runalsh/ubuntu-docker-patch:22.04.0` | `22.04 LTS` | `release-20220420` |
| `runalsh/ubuntu-docker-patch:22.04.1` | `22.04.1 LTS` | `release-20220810` |
| `runalsh/ubuntu-docker-patch:22.04.2` | `22.04.2 LTS` | `release-20230302` |
| `runalsh/ubuntu-docker-patch:22.04.3` | `22.04.3 LTS` | `release-20230814` |
| `runalsh/ubuntu-docker-patch:22.04.4` | `22.04.4 LTS` | `release-20240223` |
| `runalsh/ubuntu-docker-patch:22.04.5` | `22.04.5 LTS` | `release-20240912` |

### Ubuntu 24.04 LTS (Noble Numbat)

| Тег | Версия в `/etc/os-release` | Базовый релиз Canonical |
|---|---|---|
| `runalsh/ubuntu-docker-patch:24.04.0` | `24.04 LTS` | `release-20240423` |
| `runalsh/ubuntu-docker-patch:24.04.1` | `24.04.1 LTS` | `release-20240911` |
| `runalsh/ubuntu-docker-patch:24.04.2` | `24.04.2 LTS` | `release-20250221` |
| `runalsh/ubuntu-docker-patch:24.04.3` | `24.04.3 LTS` | `release-20250805` |
| `runalsh/ubuntu-docker-patch:24.04.4` | `24.04.4 LTS` | `release-20260225` |

---

## 🛠 Быстрый старт

### Использование готового образа из Docker Hub

```bash
docker run --rm -it runalsh/ubuntu-docker-patch:22.04.1 cat /etc/os-release
docker run --rm -it runalsh/ubuntu-docker-patch:24.04.2 cat /etc/os-release
```

### Локальная сборка

Файл `releases.txt` содержит список версий и их прямые ссылки на rootfs.

Для импорта всех версий локально:

```bash
chmod +x build.sh
TEST_VERSION=true PUSH_TO_DOCKERHUB=false ./build.sh
```

---

## ⚙️ Структура репозитория

```text
.
├── .github/workflows/
│   └── build-and-push.yml  # Автоматический CI pipeline для сборки, тестирования и push в Docker Hub
├── build.sh                 # Скрипт автоматического импорта и проверки версий
├── releases.txt             # Реестр URL с версиями rootfs
└── README.md                # Документация проекта
```

---

## 🔐 Секреты для GitHub Actions

Для работы CI workflow требуются секреты в GitHub Secrets:
- `DOCKERHUB_USERNAME`: Логин на Docker Hub (`runalsh`)
- `DOCKERHUB_TOKEN`: Personal Access Token Docker Hub
