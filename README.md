# Portal_DTwins

**Аналитический корпус стратегического партнёрства ПСБ × СПбПУ**

Структурированная база знаний по цифровым двойникам в контексте финтех-брокерской модели диффузии суверенных технологий.

---

## 🎯 Назначение

Репозиторий содержит:
- **Первоисточники** — оригинальные документы партнёрства (docx, pdf, xlsx)
- **Аналитический корпус** — 13 семантически связанных JSON-узлов
- **Knowledge Graph** — граф связей v14 (83 ребра, 13 узлов)
- **Архив** — история развития корпуса (v2-v13, до нормализации)

### Тематика

- Архитектура партнёрства ПСБ и СПбПУ
- Методология СЦИ (Системной Цифровой Инженерии)
- Платформа CML-Bench и её позиционирование
- Программа МКЦП ЦД 2026-2035 (15 трлн руб.)
- Регуляторная рамка и рыночный контекст

---

## 📁 Структура репозитория

```
Portal_DTwins/                           60 файлов, 12 MB
│
├── README.md                            ← Этот файл
├── .gitignore
│
├── data/                                ← АКТУАЛЬНЫЕ ДАННЫЕ
│   ├── graph/
│   │   └── psb_knowledge_graph_integration_v14.json    (197 KB)
│   ├── nodes/                           ← 13 нормализованных узлов (1.1 MB)
│   │   ├── psb_spbpu_context_analysis.json
│   │   ├── psb_shareholder_logic_analysis.json
│   │   ├── psb_financial_architecture_analysis.json
│   │   ├── psb_ecosystem_infrastructure_analysis.json
│   │   ├── psb_technological_foundation_6tu_analysis.json
│   │   ├── psb_global_trend_platform_analysis.json
│   │   ├── psb_regulatory_framework_analysis.json
│   │   ├── psb_strategic_sovereignty_role_analysis.json
│   │   ├── psb_sci_architecture_analysis.json
│   │   ├── psb_dt_platforms_market_analysis.json
│   │   ├── psb_cmlbench_technology_context_analysis.json
│   │   ├── psb_state_agenda_dt_timeline_analysis.json
│   │   └── psb_mkcp_program_analysis.json
│   ├── schema/
│   │   ├── psb_analytical_json_schema.json             (5 KB)
│   │   └── id_convention.json                          (2 KB)
│   └── index/
│       ├── incoming_edges_index.json                   (85 KB)
│       ├── validation_report.json                      (2 KB)
│       └── project_inventory.json                      (17 KB)
│
├── SOURCE_DOCUMENTS/                    ← ПЕРВОИСТОЧНИКИ (8.9 MB)
│   ├── 1_2025_11_Док_1_*.docx           Структура ПСБ, логика акционера
│   ├── 2_2025_11_Док_2_*.docx           Финансовая архитектура
│   ├── 3_2025_11_Док_3_*.docx           Экосистема инфраструктуры
│   ├── 4_2025_11_Док_4_*.docx           Контекст ПСБ×СПбПУ
│   ├── 4_2025_11_Док_4_Приложение_1_*.pdf   Схема нац.документов
│   ├── 4_2025_11_Док_4_Приложение_2_*.pdf   Видение роли ПСБ
│   ├── 4_2025_11_Док_4_Приложение_3_*.pdf   Структурная схема СЦИ
│   ├── 4_2025_11_Док_4_Приложение_4_*.xlsx  Сравнительный анализ платформ
│   ├── 4_2025_11_Док_4_Приложение_5_*.pdf   CML-Bench в контексте
│   ├── 5_2025_11_Док_5_*.docx           Глобальный уровень
│   ├── 5_2025_11_Док_5_Приложение_1_*.pdf   Принципы новой тех.основы
│   ├── 2025_Хронология_*.docx           Хронология инициатив
│   └── МКЦП_редакция_после_МО.pdf       Программа МКЦП ЦД (7.4 MB)
│
├── docs/
│   └── architecture.md                  ← Архитектура графа
│
└── archive/                             ← ИСТОРИЯ РАЗВИТИЯ
    ├── legacy_graphs/                   ← 12 версий графа (v2-v13)
    │   ├── psb_knowledge_graph_integration_v2.json
    │   ├── psb_knowledge_graph_integration_v3.json
    │   ├── ...
    │   └── psb_knowledge_graph_integration_v13.json
    └── json_pre_normalization/          ← 13 узлов до нормализации
        ├── psb_spbpu_context_analysis.json
        ├── ...
        └── psb_mkcp_program_analysis.json
```

---

## 🗂 Узлы графа (v14)

| node_id | Layer | Файл | Описание |
|---------|-------|------|----------|
| NODE-CONTEXT | L1-Strategic | psb_spbpu_context_analysis | Базовый контекст партнёрства |
| NODE-SHAREHOLDER | L1-Strategic | psb_shareholder_logic_analysis | Логика миссионного акционера |
| NODE-FINANCE | L2-Operational | psb_financial_architecture_analysis | Финансовая архитектура ПСБ |
| NODE-ECOSYSTEM | L2-Operational | psb_ecosystem_infrastructure_analysis | Экосистема инфраструктуры |
| NODE-TECHBASE | L3-Technical | psb_technological_foundation_6tu_analysis | 6ТУ Framework |
| NODE-PLATFORM | L1-Strategic | psb_global_trend_platform_analysis | Глобальные тренды платформ |
| NODE-REGULATORY | L2-Operational | psb_regulatory_framework_analysis | Регуляторная рамка |
| NODE-SOVEREIGNTY | L1-Strategic | psb_strategic_sovereignty_role_analysis | Роль в тех.суверенитете |
| NODE-SCI | L3-Technical | psb_sci_architecture_analysis | Архитектура СЦИ |
| NODE-MARKET | L2-Operational | psb_dt_platforms_market_analysis | Рынок платформ ЦД |
| NODE-CMLBENCH | L3-Technical | psb_cmlbench_technology_context_analysis | Платформа CML-Bench |
| NODE-TIMELINE | L2-Operational | psb_state_agenda_dt_timeline_analysis | Хронология госагенды |
| NODE-MKCP | L1-Strategic | psb_mkcp_program_analysis | Программа МКЦП ЦД |

### Распределение по слоям

```
L1-Strategic (5 узлов)     Миссия, цели, глобальный контекст
    NODE-CONTEXT, NODE-SHAREHOLDER, NODE-PLATFORM, NODE-SOVEREIGNTY, NODE-MKCP

L2-Operational (5 узлов)   Процессы, ограничения, динамика
    NODE-FINANCE, NODE-ECOSYSTEM, NODE-REGULATORY, NODE-MARKET, NODE-TIMELINE

L3-Technical (3 узла)      Методология, платформы, инструменты
    NODE-TECHBASE, NODE-SCI, NODE-CMLBENCH
```

---

## 📊 Статистика

### Knowledge Graph v14

| Метрика | Значение |
|---------|----------|
| Узлов | 13 |
| Связей | 83 |
| Обратных ссылок | 313 |
| Типов связей | 12 |
| Narrative summaries | 13 (ср. 128 слов) |

### Репозиторий

| Категория | Файлов | Размер |
|-----------|--------|--------|
| SOURCE_DOCUMENTS/ | 13 | 8.9 MB |
| data/nodes/ | 13 | 1.1 MB |
| data/graph/ | 1 | 197 KB |
| data/schema/ | 2 | 7 KB |
| data/index/ | 3 | 104 KB |
| archive/legacy_graphs/ | 12 | 523 KB |
| archive/json_pre_normalization/ | 13 | 943 KB |
| docs/ | 1 | 4 KB |
| **Итого** | **60** | **~12 MB** |

---

## 🚀 Быстрый старт

### Загрузка графа

```python
import json

# Загрузка Knowledge Graph v14
with open('data/graph/psb_knowledge_graph_integration_v14.json', 'r') as f:
    graph = json.load(f)

# Все узлы
nodes = graph['nodes']
print(f"Узлов: {len(nodes)}")

# Все связи
edges = graph['edges']
print(f"Связей: {len(edges)}")

# Онтология связей
ontology = graph['meta']['edge_ontology']
print(f"Типов связей: {len(ontology['by_type'])}")
```

### Навигация по связям

```python
def get_node_edges(node_id):
    """Получить все связи узла"""
    outgoing = [e for e in edges if e['source'] == node_id]
    incoming = [e for e in edges if e['target'] == node_id]
    return {'outgoing': outgoing, 'incoming': incoming}

# Пример: связи NODE-CMLBENCH
cmlbench = get_node_edges('NODE-CMLBENCH')
print(f"Исходящих: {len(cmlbench['outgoing'])}")
print(f"Входящих: {len(cmlbench['incoming'])}")
```

### Загрузка узла

```python
# Загрузка отдельного узла
with open('data/nodes/psb_cmlbench_technology_context_analysis.json', 'r') as f:
    node = json.load(f)

print(f"node_id: {node['node_id']}")
print(f"layer: {node['layer']}")
print(f"backlinks: {len(node['referenced_by'])}")
print(f"narrative: {node['narrative_summary'][:200]}...")
```

---

## 🔗 Типы связей

| Тип | Описание | Пример |
|-----|----------|--------|
| `enables` | Технологическое обеспечение | TECHBASE → CMLBENCH |
| `requires` | Зависимость | CMLBENCH → REGULATORY |
| `influences` | Стратегическое влияние | SHAREHOLDER → FINANCE |
| `informs` | Информационная связь | MARKET → CMLBENCH |
| `implements` | Реализация концепции | MKCP → TIMELINE |
| `validates` | Верификация | SCI → CMLBENCH |
| `constrains` | Ограничение | REGULATORY → ECOSYSTEM |
| `supports` | Поддержка | ECOSYSTEM → CMLBENCH |
| `funds` | Финансирование | MKCP → FINANCE |
| `positions` | Позиционирование | SOVEREIGNTY → CONTEXT |
| `complies_with` | Соответствие | CMLBENCH → REGULATORY |
| `integrates` | Интеграция | PLATFORM → ECOSYSTEM |

---

## 📜 Маппинг первоисточников → узлы

| Первоисточник | Производные узлы |
|---------------|------------------|
| Док 1 | NODE-SHAREHOLDER |
| Док 2 | NODE-FINANCE |
| Док 3 | NODE-ECOSYSTEM |
| Док 4 + Приложения | NODE-CONTEXT, NODE-TECHBASE, NODE-SCI, NODE-CMLBENCH, NODE-MARKET |
| Док 5 + Приложение | NODE-PLATFORM, NODE-SOVEREIGNTY |
| Хронология | NODE-TIMELINE, NODE-REGULATORY |
| МКЦП | NODE-MKCP |

---

## 📅 История версий

| Версия | Дата | Ключевые изменения |
|--------|------|-------------------|
| **v14** | 2025-11-29 | **PRODUCTION**: 83 связи, edge ontology, narratives |
| v13 | 2025-11-29 | Фаза 2: JSON Schema, edge ontology |
| v12 | 2025-11-29 | Фаза 1: node_id, layer, 313 backlinks |
| v11 | 2025-11-28 | NODE-MKCP добавлен |
| v10 | 2025-11-28 | NODE-TIMELINE добавлен |
| v9 | 2025-11-27 | NODE-CMLBENCH, 54 связи |
| v8 | 2025-11-27 | NODE-MARKET добавлен |
| v7 | 2025-11-26 | NODE-SCI добавлен |
| v6 | 2025-11-26 | Реструктуризация |
| v5 | 2025-11-25 | NODE-SOVEREIGNTY добавлен |
| v4 | 2025-11-25 | NODE-REGULATORY добавлен |
| v3 | 2025-11-24 | NODE-PLATFORM добавлен |
| v2 | 2025-11-24 | Начальная версия, 5 узлов |

---

## 🔧 Нормализация (Фазы 1-3)

Аналитические JSON-файлы прошли три фазы нормализации:

### Фаза 1: Идентификация
- Добавлен `node_id` (NODE-CONTEXT, NODE-SHAREHOLDER, ...)
- Добавлен `layer` (L1-Strategic, L2-Operational, L3-Technical)
- Добавлен `referenced_by` — 313 обратных ссылок

### Фаза 2: Связность
- 83 связи в графе (было 54)
- Edge ontology (by_source, by_target, by_type)
- JSON Schema v1.0

### Фаза 3: Нарративы
- `executive_summary` для 2 узлов
- `narrative_summary` для всех 13 узлов (ср. 128 слов)
- ID Convention документ

**Сравнение до/после:**
- Прирост размера: +131.9 KB (+12.7%)
- Причина: метаданные, backlinks, narratives

---

## 👥 Контекст проекта

**Партнёрство:** ПСБ × СПбПУ  
**Домен:** Цифровые двойники, финтех-брокер, технологический суверенитет  
**Программа:** МКЦП ЦД 2026-2035 (15 трлн руб., 10 лет)  
**Ключевая платформа:** CML-Bench (А.И. Боровков, СПбПУ)

### Ключевые концепции

- **ПСБ** — финтех-брокер для диффузии суверенных технологий
- **СЦИ** — Системная Цифровая Инженерия (методология)
- **6ТУ** — Шестой технологический уклад
- **МКЦП ЦД** — Межведомственная комплексная целевая программа по цифровым двойникам

---

## 📚 Дополнительная документация

- [docs/architecture.md](docs/architecture.md) — Архитектура Knowledge Graph
- [data/schema/id_convention.json](data/schema/id_convention.json) — Конвенция именования ID
- [data/schema/psb_analytical_json_schema.json](data/schema/psb_analytical_json_schema.json) — JSON Schema

---

*Сгенерировано: 2025-11-29 | Knowledge Graph v14 | 60 файлов*
