#!/usr/bin/env python3
"""
Agentic Loop - Direct Runtime Launcher
Запуск проекта БЕЗ Docker контейнеров
"""

import subprocess
import sys
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.resolve()

def print_banner():
    """Отобразить banner запуска"""
    banner = f"""
╔══════════════════════════════════════════════════════════╗
║     Agentic Loop - Direct Runtime Launcher v1.0          ║
║              Python + Node.js Hybrid Mode                ║
╚══════════════════════════════════════════════════════════╝

📍 Путь: {PROJECT_ROOT}
💻 Система: {'Windows' if os.name == 'nt' else 'Linux'}
"""
    print(banner)

def check_dependencies():
    """Проверить зависимости проекта"""
    checks = []
    
    # Python
    python_ok = sys.version_info >= (3, 9)
    checks.append(("Python ≥3.9", python_ok))
    
    # Node.js
    try:
        node_ver = subprocess.run(
            ["node", "--version"], 
            capture_output=True, text=True
        )
        checks.append(("Node.js installed", True))
    except FileNotFoundError:
        checks.append(("Node.js installed", False))
    
    return checks

def install_dependencies():
    """Установить зависимости проекта"""
    print("📦 Установка зависимостей...")
    
    # pip install
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "runtime/requirements.txt"], 
                   capture_output=True)
    
    # pnpm install (если есть package.json)
    pkg_json = PROJECT_ROOT / "package.json"
    if pkg_json.exists():
        subprocess.run(["pnpm", "install"], capture_output=True)
    
    print("✅ Зависимости установлены")

def start_api_server():
    """Запуск API сервера"""
    print("\n🚀 Запуск API сервера...")
    try:
        process = subprocess.Popen(
            [sys.executable, "api/main.py"],
            cwd=PROJECT_ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        return process
    except Exception as e:
        print(f"❌ Ошибка запуска API: {e}")

def start_agent_runtime():
    """Запуск runtime агента"""
    print("\n🤖 Запуск Agent Runtime...")
    try:
        process = subprocess.Popen(
            [sys.executable, "runtime/main.py"],
            cwd=PROJECT_ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        return process
    except Exception as e:
        print(f"❌ Ошибка запуска Runtime: {e}")

def start_cli():
    """Запуск CLI интерфейса"""
    print("\n📟 Запуск CLI...")
    subprocess.run([sys.executable, "-m", "cli"])

def main_menu():
    """Основное меню"""
    while True:
        print_banner()
        print("Выберите режим запуска:")
        print("  [1] API Server (порт 8000)")
        print("  [2] Agent Runtime")
        print("  [3] CLI Interface")
        print("  [4] Запустить всё вместе")
        print("  [5] Выход")
        
        choice = input("\nВаш выбор (1-5): ").strip()
        
        if choice == "1":
            start_api_server()
        elif choice == "2":
            start_agent_runtime()
        elif choice == "3":
            start_cli()
        elif choice == "4":
            print("\n🚀 Запуск всех компонентов...")
            processes = []
            try:
                p1 = subprocess.Popen(
                    [sys.executable, "api/main.py"],
                    cwd=PROJECT_ROOT,
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
                )
                processes.append(("API", p1))
                
                p2 = subprocess.Popen(
                    [sys.executable, "runtime/main.py"],
                    cwd=PROJECT_ROOT,
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
                )
                processes.append(("Runtime", p2))
            except Exception as e:
                print(f"Ошибка: {e}")
        elif choice == "5":
            break

if __name__ == "__main__":
    main_menu()