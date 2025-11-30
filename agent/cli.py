#!/usr/bin/env python3
"""
Knowledge Gate Agent CLI
Интерактивный интерфейс для работы с агентом
"""
import sys
import json
from pathlib import Path
from datetime import datetime

# Добавляем корневую директорию в PATH
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Загружаем .env
from dotenv import load_dotenv
load_dotenv(PROJECT_ROOT / ".env")

from agent.knowledge_gate import KnowledgeGateAgent


class AgentCLI:
    """CLI интерфейс для Knowledge Gate Agent"""

    COMMANDS = {
        "help": "Показать справку",
        "info": "Информация об агенте",
        "overview": "Обзор базы знаний",
        "stats": "Статистика",
        "list": "Список материалов (list nodes, list sources, list l1)",
        "get": "Получить материал (get NODE-CONTEXT)",
        "search": "Поиск (search CML-Bench)",
        "trace": "Трассировка (trace SRC-DOC-001)",
        "keyword": "Поиск по ключевому слову (keyword ПСБ)",
        "edges": "Связи узла (edges NODE-CONTEXT)",
        "layer": "Узлы слоя (layer L1-Strategic)",
        "session": "Информация о сессии",
        "exit": "Выход",
    }

    def __init__(self):
        print("=" * 60)
        print("🚀 Knowledge Gate Agent CLI")
        print("=" * 60)
        print("Инициализация агента...")

        self.agent = KnowledgeGateAgent()
        agent_info = self.agent.get_agent_info()

        print(f"✅ Агент: {agent_info['name']} v{agent_info['version']}")
        print(f"📍 Сессия: {agent_info['session_id'][:8]}...")
        print(f"📚 Gold Index: {'загружен' if agent_info['gold_index_loaded'] else 'не найден'}")
        print()
        print("Введите 'help' для списка команд")
        print("-" * 60)

    def run(self):
        """Запуск интерактивного режима"""
        while True:
            try:
                user_input = input("\n🤖 > ").strip()

                if not user_input:
                    continue

                if user_input.lower() in ("exit", "quit", "q"):
                    print("\n👋 До свидания!")
                    break

                self.process_command(user_input)

            except KeyboardInterrupt:
                print("\n\n👋 Прервано пользователем")
                break
            except EOFError:
                break
            except Exception as e:
                print(f"❌ Ошибка: {e}")

    def process_command(self, user_input: str):
        """Обработка команды"""
        parts = user_input.split(maxsplit=1)
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        # Специальные команды
        if command == "help":
            self.show_help()
        elif command == "info":
            self.show_agent_info()
        elif command == "overview":
            self.show_overview()
        elif command == "stats":
            self.show_stats()
        elif command == "session":
            self.show_session()
        elif command == "list":
            self.handle_list(args)
        elif command == "get":
            self.handle_get(args)
        elif command == "search":
            self.handle_search(args)
        elif command == "trace":
            self.handle_trace(args)
        elif command == "keyword":
            self.handle_keyword(args)
        elif command == "edges":
            self.handle_edges(args)
        elif command == "layer":
            self.handle_layer(args)
        else:
            # Передаём как свободный запрос
            result = self.agent.process_query(user_input)
            self.print_result(result)

    def show_help(self):
        """Показать справку"""
        print("\n📖 Доступные команды:")
        print("-" * 40)
        for cmd, desc in self.COMMANDS.items():
            print(f"  {cmd:12} - {desc}")
        print("\nИли введите свободный запрос на естественном языке")

    def show_agent_info(self):
        """Информация об агенте"""
        info = self.agent.get_agent_info()
        print(f"\n🤖 {info['name']}")
        print(f"   ID: {info['agent_id']}")
        print(f"   Версия: {info['version']}")
        print(f"   Состояние: {info['state']}")
        print(f"\n📌 Возможности:")
        for cap in info['capabilities']:
            print(f"   • {cap}")
        print(f"\n🔗 Downstream агенты:")
        for agent in info['downstream_agents']:
            print(f"   • {agent}")

    def show_overview(self):
        """Обзор базы знаний"""
        result = self.agent.get_overview()
        if result['status'] == 'success':
            data = result['data']

            # База данных
            db = data.get('database', {})
            print(f"\n📊 Статистика базы данных:")
            print(f"   Всего материалов: {db.get('total_materials', 'N/A')}")

            by_cat = db.get('by_category', {})
            if by_cat:
                print(f"\n📂 По категориям:")
                for cat, stats in by_cat.items():
                    print(f"   • {cat}: {stats.get('total_count', 0)}")

            # Граф
            graph = data.get('graph', {})
            print(f"\n🕸️ Knowledge Graph:")
            print(f"   Узлов: {graph.get('nodes_count', 'N/A')}")
            print(f"   Связей: {graph.get('edges_count', 'N/A')}")
            print(f"   Backlinks: {graph.get('total_backlinks', 'N/A')}")

            # Critical path
            cp = data.get('critical_path', {})
            if cp:
                print(f"\n🛤️ Критический путь:")
                print(f"   {cp.get('interpretation', 'N/A')}")

            # Top nodes
            ranking = data.get('backlinks_ranking', [])
            if ranking:
                print(f"\n🔝 Топ узлов по backlinks:")
                for item in ranking[:5]:
                    print(f"   • {item['node']}: {item['backlinks']}")

    def show_stats(self):
        """Статистика"""
        result = self.agent.get_statistics()
        self.print_result(result)

    def show_session(self):
        """Информация о сессии"""
        ctx = self.agent.get_session_context()
        print(f"\n📍 Сессия: {ctx['session_id'][:8]}...")
        print(f"   Начало: {ctx['started_at']}")
        print(f"   Операций: {ctx['operations_count']}")
        print(f"   Запросов: {ctx['queries_count']}")
        print(f"   Материалов открыто: {len(ctx['materials_accessed'])}")
        if ctx['current_focus']:
            print(f"   Текущий фокус: {ctx['current_focus']}")

    def handle_list(self, args: str):
        """Обработка команды list"""
        args_lower = args.lower()

        if "node" in args_lower or "узл" in args_lower:
            result = self.agent.list_materials(category="ANALYTICAL_NODES")
        elif "source" in args_lower or "источник" in args_lower:
            result = self.agent.list_materials(category="RAW_SOURCES")
        elif "l1" in args_lower or "strategic" in args_lower:
            result = self.agent.list_materials(layer="L1-Strategic")
        elif "l2" in args_lower or "operational" in args_lower:
            result = self.agent.list_materials(layer="L2-Operational")
        elif "l3" in args_lower or "technical" in args_lower:
            result = self.agent.list_materials(layer="L3-Technical")
        elif "gold" in args_lower:
            result = self.agent.list_materials(category="GOLD")
        else:
            result = self.agent.list_materials(limit=20)

        self.print_materials_list(result)

    def handle_get(self, args: str):
        """Обработка команды get"""
        if not args:
            print("❓ Укажите ID материала (например: get NODE-CONTEXT)")
            return

        material_id = args.upper().strip()
        result = self.agent.get_material(material_id)
        self.print_material(result)

    def handle_search(self, args: str):
        """Обработка команды search"""
        if not args:
            print("❓ Укажите поисковый запрос (например: search CML-Bench)")
            return

        result = self.agent.search(args)
        self.print_search_results(result)

    def handle_trace(self, args: str):
        """Обработка команды trace"""
        if not args:
            print("❓ Укажите ID материала (например: trace SRC-DOC-001)")
            return

        material_id = args.upper().strip()
        if material_id.startswith("SRC"):
            result = self.agent.get_source_chain(material_id)
        else:
            result = self.agent.get_node_sources(material_id)
        self.print_result(result)

    def handle_keyword(self, args: str):
        """Обработка команды keyword"""
        if not args:
            print("❓ Укажите ключевое слово (например: keyword ПСБ)")
            return

        result = self.agent.search_by_keyword(args)
        self.print_result(result)

    def handle_edges(self, args: str):
        """Обработка команды edges"""
        if not args:
            print("❓ Укажите ID узла (например: edges NODE-CONTEXT)")
            return

        node_id = args.upper().strip()
        result = self.agent.get_node_edges(node_id)
        self.print_edges(result)

    def handle_layer(self, args: str):
        """Обработка команды layer"""
        if not args:
            print("❓ Укажите слой (L1-Strategic, L2-Operational, L3-Technical)")
            return

        layer = args.strip()
        if not layer.startswith("L"):
            layer = f"L{layer}"
        if "-" not in layer:
            layer_map = {"L1": "L1-Strategic", "L2": "L2-Operational", "L3": "L3-Technical"}
            layer = layer_map.get(layer, layer)

        result = self.agent.get_layer_nodes(layer)
        self.print_result(result)

    # ==========================================
    # ФОРМАТИРОВАНИЕ ВЫВОДА
    # ==========================================

    def print_result(self, result: dict):
        """Печать результата операции"""
        status = result.get('status', 'unknown')

        if status == 'success':
            print(f"\n✅ {result.get('operation', 'Операция')}")
            data = result.get('data', {})
            print(json.dumps(data, ensure_ascii=False, indent=2, default=str))
        elif status == 'error':
            print(f"\n❌ Ошибка: {result.get('error', 'Неизвестная ошибка')}")
        elif status == 'routed':
            print(f"\n🔀 Маршрутизация к: {result.get('target_agent')}")
            print(f"   {result.get('message', '')}")
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2, default=str))

    def print_materials_list(self, result: dict):
        """Печать списка материалов"""
        if result.get('status') != 'success':
            self.print_result(result)
            return

        data = result.get('data', {})
        materials = data.get('materials', [])
        count = data.get('count', len(materials))

        print(f"\n📋 Найдено материалов: {count}")
        print("-" * 60)

        for m in materials:
            layer = f"[{m.get('layer', '')}]" if m.get('layer') else ""
            print(f"  {m['material_id']:18} {layer:15} {m.get('title', '')[:40]}")

    def print_material(self, result: dict):
        """Печать информации о материале"""
        if result.get('status') != 'success':
            self.print_result(result)
            return

        m = result.get('data', {})
        print(f"\n📄 {m.get('material_id', 'N/A')}")
        print("=" * 50)
        print(f"   Название: {m.get('title', 'N/A')}")
        print(f"   Файл: {m.get('filename', 'N/A')}")
        print(f"   Категория: {m.get('category', 'N/A')}")
        print(f"   Статус: {m.get('status', 'N/A')}")
        if m.get('layer'):
            print(f"   Слой: {m.get('layer')}")
        if m.get('file_size_bytes'):
            size_kb = m['file_size_bytes'] / 1024
            print(f"   Размер: {size_kb:.1f} KB")
        if m.get('backlinks_count'):
            print(f"   Backlinks: {m.get('backlinks_count')}")
        if m.get('source_ids'):
            print(f"   Источники: {', '.join(m.get('source_ids', []))}")

    def print_search_results(self, result: dict):
        """Печать результатов поиска"""
        if result.get('status') != 'success':
            self.print_result(result)
            return

        data = result.get('data', {})
        results = data.get('results', [])
        query = data.get('query', '')

        print(f"\n🔍 Поиск: '{query}'")
        print(f"   Найдено: {len(results)}")
        print("-" * 50)

        for r in results:
            rank = f"[{r.get('rank', 0):.2f}]" if 'rank' in r else ""
            print(f"  {r.get('material_id', ''):18} {rank:8} {r.get('title', '')[:35]}")

    def print_edges(self, result: dict):
        """Печать связей узла"""
        if result.get('status') != 'success':
            self.print_result(result)
            return

        data = result.get('data', {})
        node_id = data.get('node_id', '')
        edges = data.get('edges', {})

        print(f"\n🔗 Связи узла: {node_id}")
        print("=" * 50)

        outgoing = edges.get('outgoing', [])
        if outgoing:
            print(f"\n📤 Исходящие ({len(outgoing)}):")
            for e in outgoing:
                print(f"   → {e.get('target_id', '')} ({e.get('edge_type', '')})")

        incoming = edges.get('incoming', [])
        if incoming:
            print(f"\n📥 Входящие ({len(incoming)}):")
            for e in incoming:
                print(f"   ← {e.get('source_id', '')} ({e.get('edge_type', '')})")


def main():
    """Точка входа CLI"""
    cli = AgentCLI()
    cli.run()


if __name__ == "__main__":
    main()
