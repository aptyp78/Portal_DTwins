# Portal_DTwins Database Setup Guide

## Архитектура

```
PostgreSQL 15+
    └── pgvector extension (v0.5+)
        └── portal_dtwins database
            ├── materials (основная таблица)
            ├── analytical_nodes (13 узлов)
            ├── source_documents (13 первоисточников)
            ├── knowledge_graphs (версии графа)
            ├── material_edges (83 связи)
            ├── source_node_mapping (трассировка)
            ├── backlinks (313 входящих ссылок)
            └── agent_operations (лог агента)
```

## Требования

- PostgreSQL 15+
- pgvector extension 0.5+
- Python 3.10+

## Установка PostgreSQL (macOS)

```bash
# Через Homebrew
brew install postgresql@15
brew services start postgresql@15

# Установка pgvector
brew install pgvector

# Или через psql
CREATE EXTENSION vector;
```

## Быстрый старт

### 1. Клонирование и настройка

```bash
cd Portal_DTwins

# Создание виртуального окружения
python3 -m venv .venv
source .venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt

# Копирование конфигурации
cp .env.example .env
# Отредактируйте .env, укажите пароль PostgreSQL
```

### 2. Инициализация базы данных

```bash
# Запуск скрипта инициализации
python database/setup_db.py
```

Скрипт автоматически:
- Создаст базу данных `portal_dtwins`
- Применит схему (таблицы, индексы, views)
- Загрузит начальные данные (31 материал)

### 3. Проверка

```bash
# Подключение к БД
psql -d portal_dtwins

# Проверка данных
SELECT * FROM v_category_stats;
SELECT * FROM v_materials_overview LIMIT 10;
```

## Структура таблиц

### materials (основная)
| Поле | Тип | Описание |
|------|-----|----------|
| id | UUID | Primary key |
| material_id | VARCHAR(50) | Уникальный ID (NODE-*, SRC-*) |
| filename | VARCHAR(255) | Имя файла |
| title | VARCHAR(500) | Заголовок |
| category | ENUM | RAW_SOURCES, ANALYTICAL_NODES, etc. |
| status | ENUM | production, immutable, archived |
| layer | ENUM | L1-Strategic, L2-Operational, L3-Technical |
| embedding | vector(1536) | Векторное представление |
| metadata | JSONB | Дополнительные метаданные |
| tags | VARCHAR[] | Теги для поиска |

### analytical_nodes (расширение)
| Поле | Тип | Описание |
|------|-----|----------|
| node_id | VARCHAR(50) | NODE-CONTEXT, NODE-SHAREHOLDER, etc. |
| layer | ENUM | Слой графа знаний |
| backlinks_count | INTEGER | Количество входящих ссылок |
| source_ids | VARCHAR[] | ID первоисточников |
| importance_score | DECIMAL | Важность (0-1) |
| centrality_score | DECIMAL | Центральность в графе |

### material_edges (связи)
| Поле | Тип | Описание |
|------|-----|----------|
| source_material_id | UUID | Исходный узел |
| target_material_id | UUID | Целевой узел |
| edge_type | ENUM | derives_from, references, depends_on, etc. |
| weight | DECIMAL | Вес связи (0-1) |

## Views

### v_materials_overview
Обзор материалов с метриками backlinks и outgoing edges.

### v_knowledge_graph
Граф связей для визуализации.

### v_category_stats
Статистика по категориям.

## Индексы

- **GIN** на `tags`, `metadata` — для поиска по массивам и JSON
- **IVFFlat** на `embedding` — для векторного поиска (cosine similarity)
- **GIN** на `content_tsvector` — для полнотекстового поиска

## Python API

```python
from database import db_manager, MaterialCategory

# Получение материала
material = db_manager.get_material("NODE-CONTEXT")

# Список материалов
nodes = db_manager.list_materials(category=MaterialCategory.ANALYTICAL_NODES)

# Поиск
results = db_manager.search_materials("CML-Bench")

# Трассировка source -> nodes
chain = db_manager.get_source_chain("SRC-DOC-001")

# Связи узла
edges = db_manager.get_node_edges("NODE-CONTEXT")

# Статистика
stats = db_manager.get_statistics()
```

## Семантический поиск

Для семантического поиска требуется:
1. OpenAI API key в `.env`
2. Генерация embeddings для материалов

```python
# Поиск по embedding
embedding = generate_embedding("технологический суверенитет")
results = db_manager.semantic_search(embedding, limit=5)
```

## Миграции

Новые миграции добавляются в `database/schema/`:
- `001_initial_schema.sql` — базовая схема
- `002_seed_materials.sql` — начальные данные

## Резервное копирование

```bash
# Backup
pg_dump -d portal_dtwins > backup_$(date +%Y%m%d).sql

# Restore
psql -d portal_dtwins < backup_20251130.sql
```

## Статистика (после инициализации)

| Категория | Количество |
|-----------|------------|
| RAW_SOURCES | 13 |
| ANALYTICAL_NODES | 13 |
| KNOWLEDGE_GRAPH | 1 |
| SCHEMAS | 2 |
| GOLD | 3 |
| **Всего** | **32** |

## Поддержка

При проблемах проверьте:
1. PostgreSQL запущен: `brew services list`
2. pgvector установлен: `SELECT * FROM pg_extension WHERE extname = 'vector';`
3. Права доступа: `\du` в psql
