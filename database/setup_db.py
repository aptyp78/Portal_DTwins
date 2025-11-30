#!/usr/bin/env python3
"""
Скрипт инициализации базы данных Portal_DTwins
Создаёт БД, схему и загружает начальные данные
"""
import os
import sys
from pathlib import Path

# Добавляем корневую директорию проекта в PATH
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Загружаем .env файл
from dotenv import load_dotenv
load_dotenv(PROJECT_ROOT / ".env")

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from database.config import DatabaseConfig

# Перезагружаем конфигурацию после загрузки .env
db_config = DatabaseConfig.from_env()


def create_database():
    """Создание базы данных portal_dtwins"""
    print("🔧 Создание базы данных...")

    # Подключаемся к postgres для создания БД
    conn = psycopg2.connect(
        host=db_config.host,
        port=db_config.port,
        database="postgres",
        user=db_config.user,
        password=db_config.password,
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    with conn.cursor() as cur:
        # Проверяем существование БД
        cur.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (db_config.database,)
        )
        exists = cur.fetchone()

        if exists:
            print(f"   ℹ️  База данных '{db_config.database}' уже существует")
        else:
            cur.execute(f"CREATE DATABASE {db_config.database}")
            print(f"   ✅ База данных '{db_config.database}' создана")

    conn.close()


def run_schema():
    """Выполнение схемы базы данных"""
    print("📋 Применение схемы...")

    schema_file = PROJECT_ROOT / "database" / "schema" / "001_initial_schema.sql"

    if not schema_file.exists():
        print(f"   ❌ Файл схемы не найден: {schema_file}")
        return False

    conn = psycopg2.connect(
        host=db_config.host,
        port=db_config.port,
        database=db_config.database,
        user=db_config.user,
        password=db_config.password,
    )

    try:
        with conn.cursor() as cur:
            cur.execute(schema_file.read_text())
        conn.commit()
        print("   ✅ Схема применена успешно")
        return True
    except Exception as e:
        conn.rollback()
        print(f"   ❌ Ошибка при применении схемы: {e}")
        return False
    finally:
        conn.close()


def run_seeds():
    """Загрузка начальных данных"""
    print("🌱 Загрузка начальных данных...")

    seed_file = PROJECT_ROOT / "database" / "seeds" / "002_seed_materials.sql"

    if not seed_file.exists():
        print(f"   ❌ Файл seeds не найден: {seed_file}")
        return False

    conn = psycopg2.connect(
        host=db_config.host,
        port=db_config.port,
        database=db_config.database,
        user=db_config.user,
        password=db_config.password,
    )

    try:
        with conn.cursor() as cur:
            cur.execute(seed_file.read_text())
        conn.commit()
        print("   ✅ Данные загружены успешно")
        return True
    except Exception as e:
        conn.rollback()
        print(f"   ❌ Ошибка при загрузке данных: {e}")
        return False
    finally:
        conn.close()


def verify_data():
    """Проверка загруженных данных"""
    print("🔍 Проверка данных...")

    conn = psycopg2.connect(
        host=db_config.host,
        port=db_config.port,
        database=db_config.database,
        user=db_config.user,
        password=db_config.password,
    )

    with conn.cursor() as cur:
        # Материалы
        cur.execute("SELECT COUNT(*) FROM materials")
        materials_count = cur.fetchone()[0]

        # По категориям
        cur.execute("""
            SELECT category, COUNT(*) as count
            FROM materials
            GROUP BY category
            ORDER BY category
        """)
        by_category = {row[0]: row[1] for row in cur.fetchall()}

        # Аналитические узлы
        cur.execute("SELECT COUNT(*) FROM analytical_nodes")
        nodes_count = cur.fetchone()[0]

        # Source-Node маппинги
        cur.execute("SELECT COUNT(*) FROM source_node_mapping")
        mappings_count = cur.fetchone()[0]

    conn.close()

    print(f"\n📊 Статистика базы данных:")
    print(f"   • Всего материалов: {materials_count}")
    print(f"   • Аналитических узлов: {nodes_count}")
    print(f"   • Source-Node связей: {mappings_count}")
    print(f"\n📂 По категориям:")
    for cat, count in sorted(by_category.items()):
        print(f"   • {cat}: {count}")


def main():
    """Основная функция инициализации"""
    print("=" * 50)
    print("🚀 Portal_DTwins Database Setup")
    print("=" * 50)
    print(f"\n📌 Параметры подключения:")
    print(f"   • Host: {db_config.host}")
    print(f"   • Port: {db_config.port}")
    print(f"   • Database: {db_config.database}")
    print(f"   • User: {db_config.user}")
    print()

    try:
        create_database()
        if run_schema():
            run_seeds()
            verify_data()
            print("\n" + "=" * 50)
            print("✅ Инициализация завершена успешно!")
            print("=" * 50)
        else:
            print("\n❌ Инициализация прервана из-за ошибок")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
