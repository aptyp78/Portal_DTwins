# Архитектура Knowledge Graph

## Обзор

Knowledge Graph проекта ПСБ×СПбПУ представляет собой семантическую сеть из 13 узлов, связанных 83 направленными рёбрами. Граф моделирует знания о стратегическом партнёрстве в области цифровых двойников.

## Слои (Layers)

Узлы организованы в три слоя:

```
L1-Strategic    ← Стратегический уровень (целеполагание)
L2-Operational  ← Операционный уровень (реализация)
L3-Technical    ← Технический уровень (инструменты)
```

### Распределение по слоям

| Слой | Узлы | Назначение |
|------|------|------------|
| L1-Strategic | NODE-CONTEXT, NODE-SHAREHOLDER, NODE-PLATFORM, NODE-SOVEREIGNTY, NODE-MKCP | Миссия, цели, глобальный контекст |
| L2-Operational | NODE-FINANCE, NODE-ECOSYSTEM, NODE-REGULATORY, NODE-MARKET, NODE-TIMELINE | Процессы, ограничения, динамика |
| L3-Technical | NODE-TECHBASE, NODE-SCI, NODE-CMLBENCH | Методология, платформы, инструменты |

## Типология связей

### Структурные связи
- **enables** — технологическое обеспечение
- **requires** — зависимость
- **implements** — реализация

### Информационные связи
- **informs** — передача информации
- **validates** — верификация

### Управляющие связи
- **influences** — стратегическое влияние
- **constrains** — ограничение
- **funds** — финансирование

### Интеграционные связи
- **integrates** — объединение компонентов
- **supports** — поддержка
- **positions** — позиционирование
- **complies_with** — соответствие

## Ключевые паттерны

### 1. Вертикальная интеграция

```
NODE-SHAREHOLDER (L1)
    │ influences
    ▼
NODE-FINANCE (L2)
    │ enables
    ▼
NODE-ECOSYSTEM (L2)
    │ enables
    ▼
NODE-CMLBENCH (L3)
```

### 2. Методологический каскад

```
NODE-TECHBASE (L3) ─── enables ──→ NODE-SCI (L3)
       │                              │
       │ requires                     │ enables
       ▼                              ▼
NODE-REGULATORY (L2)           NODE-CMLBENCH (L3)
```

### 3. Финансовый контур

```
NODE-MKCP (L1) ─── funds ──→ NODE-FINANCE (L2)
       │                          │
       │ implements               │ enables
       ▼                          ▼
NODE-TIMELINE (L2)         NODE-ECOSYSTEM (L2)
```

## Метрики узлов

### Входящие связи (in-degree)

Узлы с наибольшим числом входящих связей являются "интеграторами":

| Узел | In-degree | Роль |
|------|-----------|------|
| NODE-CMLBENCH | 9 | Технологический интегратор |
| NODE-ECOSYSTEM | 8 | Операционный интегратор |
| NODE-FINANCE | 7 | Финансовый интегратор |

### Исходящие связи (out-degree)

Узлы с наибольшим числом исходящих связей являются "драйверами":

| Узел | Out-degree | Роль |
|------|------------|------|
| NODE-SHAREHOLDER | 8 | Стратегический драйвер |
| NODE-MKCP | 7 | Программный драйвер |
| NODE-REGULATORY | 6 | Нормативный драйвер |

## Навигация по графу

### Python-примеры

```python
import json

# Загрузка
with open('../data/graph/psb_knowledge_graph_integration_v14.json') as f:
    g = json.load(f)

# Получить все связи определённого типа
def edges_by_type(edge_type):
    return [e for e in g['edges'] if e['type'] == edge_type]

# Пример: все связи финансирования
funding = edges_by_type('funds')

# Путь между узлами (BFS)
from collections import deque

def find_path(source, target):
    visited = {source}
    queue = deque([(source, [source])])
    
    while queue:
        node, path = queue.popleft()
        for edge in g['edges']:
            if edge['source'] == node and edge['target'] not in visited:
                new_path = path + [edge['target']]
                if edge['target'] == target:
                    return new_path
                visited.add(edge['target'])
                queue.append((edge['target'], new_path))
    return None

# Пример: путь от SHAREHOLDER до CMLBENCH
path = find_path('NODE-SHAREHOLDER', 'NODE-CMLBENCH')
```

## Расширение графа

### Добавление нового узла

1. Создать JSON-файл в `data/nodes/` по схеме
2. Добавить узел в `nodes` массив графа
3. Определить связи с существующими узлами
4. Обновить `incoming_edges_index.json`
5. Инкрементировать версию графа

### Конвенция именования

```
NODE-{CONCEPT}
└── CONCEPT: 3-12 символов, UPPER_CASE
    Примеры: CMLBENCH, ECOSYSTEM, REGULATORY
```

---

*Версия документа: 1.0 | 2025-11-29*
