#!/usr/bin/env python3
"""
Запуск Knowledge Gate Agent CLI
"""
import sys
from pathlib import Path

# Настройка путей
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# Загружаем .env
from dotenv import load_dotenv
load_dotenv(PROJECT_ROOT / ".env")

# Запуск CLI
from agent.cli import main

if __name__ == "__main__":
    main()
