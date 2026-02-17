#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Terminal Launcher"""

import os
import sys
import json
import time
import threading
import subprocess
from pathlib import Path
import minecraft_launcher_lib as mll

# Константы
SCRIPT_DIR = Path(__file__).parent.absolute()
GAME_DIR = SCRIPT_DIR / ".minecraft"
CONFIG_FILE = SCRIPT_DIR / "config.json"
VERSION_FILE = SCRIPT_DIR / "version.txt"

# Текущая версия лаунчера
LAUNCHER_VERSION = "1.0"

# Языковые файлы
LANGUAGES = {
    'en': {
        'title': 'TERMINAL LAUNCHER',
        'menu_title': 'MAIN MENU',
        'game_folder': 'Game folder',
        'current_version': 'Current version',
        'launcher_version': 'Launcher version',
        
        # Menu
        'menu_play': 'Play Minecraft',
        'menu_settings': 'Settings',
        'menu_check_updates': 'Check for updates',
        'menu_language': 'Change language',
        'menu_exit': 'Exit',
        
        # Settings menu
        'settings_title': 'SETTINGS',
        'settings_version': 'Change Minecraft version',
        'settings_username': 'Change username',
        'settings_ram': 'Change RAM',
        'settings_loader': 'Change mod loader',
        'settings_back': 'Back to main menu',
        
        # Updates
        'checking_updates': 'Checking for updates',
        'current_launcher_version': 'Current launcher version',
        'latest_launcher_version': 'Latest version',
        'update_available': 'Update available',
        'no_updates': 'You have the latest version',
        'update_now': 'Update now',
        'update_complete': 'Update complete',
        'update_error': 'Update error',
        'downloading': 'Downloading',
        'creating_backup': 'Creating backup',
        
        # Other
        'choose_option': 'Choose option',
        'press_enter': 'Press Enter to continue',
        'goodbye': 'Goodbye',
        'yes': 'yes',
        'no': 'no',
        'y': 'y',
        'n': 'n',
    },
    
    'ru': {
        'title': 'TERMINAL LAUNCHER',
        'menu_title': 'ГЛАВНОЕ МЕНЮ',
        'game_folder': 'Папка игры',
        'current_version': 'Текущая версия',
        'launcher_version': 'Версия лаунчера',
        
        # Menu
        'menu_play': 'Играть в Minecraft',
        'menu_settings': 'Настройки',
        'menu_check_updates': 'Проверить обновления',
        'menu_language': 'Сменить язык',
        'menu_exit': 'Выход',
        
        # Settings menu
        'settings_title': 'НАСТРОЙКИ',
        'settings_version': 'Изменить версию Minecraft',
        'settings_username': 'Изменить никнейм',
        'settings_ram': 'Изменить RAM',
        'settings_loader': 'Изменить загрузчик модов',
        'settings_back': 'Вернуться в главное меню',
        
        # Updates
        'checking_updates': 'Проверка обновлений',
        'current_launcher_version': 'Текущая версия лаунчера',
        'latest_launcher_version': 'Последняя версия',
        'update_available': 'Доступно обновление',
        'no_updates': 'У вас актуальная версия',
        'update_now': 'Обновить сейчас',
        'update_complete': 'Обновление завершено',
        'update_error': 'Ошибка обновления',
        'downloading': 'Скачивание',
        'creating_backup': 'Создание бэкапа',
        
        # Other
        'choose_option': 'Выберите действие',
        'press_enter': 'Нажмите Enter для продолжения',
        'goodbye': 'До свидания',
        'yes': 'да',
        'no': 'нет',
        'y': 'д',
        'n': 'н',
    }
}

# Текущий язык
current_lang = 'ru'

def _(key, **kwargs):
    """Перевод строки"""
    text = LANGUAGES[current_lang].get(key, key)
    if kwargs:
        text = text.format(**kwargs)
    return text

def load_language():
    """Загружает язык из конфига"""
    global current_lang
    try:
        config = load_config()
        current_lang = config.get('language', 'ru')
    except:
        pass

def save_language(lang):
    """Сохраняет язык в конфиг"""
    global current_lang
    current_lang = lang
    config = load_config()
    config['language'] = lang
    save_config(config)

def load_config():
    """Загружает конфигурацию"""
    try:
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except:
        pass
    return {
        'version': '1.20.1',
        'username': 'Player',
        'ram': 2,
        'loader': None,
        'language': 'ru'
    }

def save_config(config):
    """Сохраняет конфигурацию"""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def clear_screen():
    """Очищает экран"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Заголовок"""
    clear_screen()
    print("=" * 60)
    print(f"     {_('title')} v{LAUNCHER_VERSION}")
    print("=" * 60)
    print(f"📁 {_('game_folder')}: {GAME_DIR}")
    print(f"🌍 Language: {'English' if current_lang == 'en' else 'Русский'}")
    print("=" * 60)
    print()

def print_config(config):
    """Показывает текущие настройки"""
    print(f"📋 {_('current_version')}: {config.get('version', '1.20.1')}")
    print(f"👤 {_('settings_username').replace('Изменить ', '')}: {config.get('username', 'Player')}")
    print(f"💾 RAM: {config.get('ram', 2)} GB")
    loader = config.get('loader')
    if loader:
        print(f"🔧 {_('settings_loader').replace('Изменить ', '')}: {loader.capitalize()}")
    else:
        print(f"🔧 {_('settings_loader').replace('Изменить ', '')}: Vanilla")
    print()

def get_yes_no(prompt_key, default='y'):
    """Получает ответ да/нет"""
    prompt = _(prompt_key)
    while True:
        if default == 'y':
            suffix = f" [{_('y')}/{_('n').upper()}]: "
        else:
            suffix = f" [{_('y').upper()}/{_('n')}]: "
        answer = input(prompt + suffix).lower().strip()
        if not answer:
            return default == 'y'
        if answer in ['y', 'yes', 'да', 'д']:
            return True
        if answer in ['n', 'no', 'нет', 'н']:
            return False

def main_menu():
    """Главное меню"""
    config = load_config()
    
    while True:
        print_header()
        print(f"📋 {_('menu_title')}")
        print("-" * 60)
        print_config(config)
        print()
        print(f"1. {_('menu_play')}")
        print(f"2. {_('menu_settings')}")
        print(f"3. {_('menu_check_updates')}")
        print(f"4. {_('menu_language')}")
        print(f"0. {_('menu_exit')}")
        print()
        
        choice = input(f"👉 {_('choose_option')}: ").strip()
        
        if choice == '1':
            play_game(config)
        elif choice == '2':
            settings_menu(config)
        elif choice == '3':
            check_updates()
        elif choice == '4':
            change_language()
        elif choice == '0':
            print(f"\n👋 {_('goodbye')}")
            break

def settings_menu(config):
    """Меню настроек"""
    while True:
        print_header()
        print(f"⚙️ {_('settings_title')}")
        print("-" * 60)
        print_config(config)
        print()
        print(f"1. {_('settings_version')}")
        print(f"2. {_('settings_username')}")
        print(f"3. {_('settings_ram')}")
        print(f"4. {_('settings_loader')}")
        print(f"0. {_('settings_back')}")
        print()
        
        choice = input(f"👉 {_('choose_option')}: ").strip()
        
        if choice == '1':
            new_version = input(f"📋 {_('settings_version')} [{config['version']}]: ").strip()
            if new_version:
                config['version'] = new_version
                save_config(config)
        elif choice == '2':
            new_username = input(f"👤 {_('settings_username')} [{config['username']}]: ").strip()
            if new_username:
                config['username'] = new_username
                save_config(config)
        elif choice == '3':
            try:
                new_ram = input(f"💾 {_('settings_ram')} (GB) [{config['ram']}]: ").strip()
                if new_ram:
                    config['ram'] = int(new_ram)
                    save_config(config)
            except:
                pass
        elif choice == '4':
            print(f"\n📦 {_('settings_loader')}:")
            print("1. Vanilla")
            print("2. Forge")
            print("3. Fabric")
            loader_choice = input(f"👉 {_('choose_option')} [1]: ").strip() or "1"
            
            if loader_choice == '1':
                config['loader'] = None
            elif loader_choice == '2':
                config['loader'] = 'forge'
            elif loader_choice == '3':
                config['loader'] = 'fabric'
            save_config(config)
        elif choice == '0':
            break
        
        input(f"\n{_('press_enter')}...")

def change_language():
    """Смена языка"""
    global current_lang
    print_header()
    print("🌍 Language / Язык")
    print("-" * 60)
    print("1. English")
    print("2. Русский")
    print()
    
    choice = input("👉 Choose / Выберите [1-2]: ").strip()
    
    if choice == '1':
        save_language('en')
    elif choice == '2':
        save_language('ru')
    
    input(f"\n{_('press_enter')}...")

def check_updates():
    """Проверка обновлений лаунчера"""
    print_header()
    print(f"🔄 {_('checking_updates')}")
    print("-" * 60)
    
    try:
        import requests
        response = requests.get(
            "https://api.github.com/repos/lixynhay/mc-terminal-launcher/releases/latest",
            headers={'User-Agent': 'Mozilla/5.0'},
            timeout=5
        )
        
        if response.status_code == 200:
            latest = response.json()
            latest_version = latest['tag_name'].lstrip('v')
            
            print(f"📌 {_('current_launcher_version')}: {LAUNCHER_VERSION}")
            print(f"📌 {_('latest_launcher_version')}: {latest_version}")
            print()
            
            if latest_version > LAUNCHER_VERSION:
                print(f"✨ {_('update_available')}!")
                print(f"📝 {latest.get('name', '')}")
                print()
                
                if get_yes_no('update_now'):
                    download_update(latest)
            else:
                print(f"✅ {_('no_updates')}")
        else:
            print(f"❌ {_('update_error')}: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ {_('update_error')}: {e}")
    
    print()
    input(f"{_('press_enter')}...")

def download_update(release_data):
    """Скачивает обновление"""
    print(f"\n📥 {_('downloading')}...")
    
    try:
        # Находим URL для скачивания
        download_url = None
        for asset in release_data.get('assets', []):
            if asset['name'] == 'launcher.py':
                download_url = asset['browser_download_url']
                break
        
        if not download_url:
            print(f"❌ {_('update_error')}: File not found")
            return
        
        # Создаем бэкап
        print(f"💾 {_('creating_backup')}...")
        current_file = Path(__file__).absolute()
        backup_file = current_file.with_suffix('.py.backup')
        import shutil
        shutil.copy2(current_file, backup_file)
        
        # Скачиваем
        import requests
        response = requests.get(download_url, timeout=30)
        
        if response.status_code == 200:
            # Сохраняем новый файл
            new_file = current_file.with_suffix('.py.new')
            with open(new_file, 'wb') as f:
                f.write(response.content)
            
            # Заменяем
            shutil.move(new_file, current_file)
            
            # Обновляем version.txt
            with open(VERSION_FILE, 'w') as f:
                f.write(release_data['tag_name'].lstrip('v'))
            
            print(f"✅ {_('update_complete')}")
            print(f"🔄 {_('press_enter')}...")
            input()
            
            # Перезапускаем
            os.execv(sys.executable, [sys.executable] + sys.argv)
        else:
            print(f"❌ {_('update_error')}: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ {_('update_error')}: {e}")

def play_game(config):
    """Запуск игры"""
    print_header()
    print(f"🚀 {_('menu_play')}")
    print("-" * 60)
    
    version = config['version']
    username = config['username']
    ram = config['ram']
    loader = config.get('loader')
    
    print(f"📋 {_('current_version')}: {version}")
    print(f"👤 {_('settings_username').replace('Изменить ', '')}: {username}")
    print(f"💾 RAM: {ram} GB")
    if loader:
        print(f"🔧 {_('settings_loader').replace('Изменить ', '')}: {loader.capitalize()}")
    print()
    
    if not get_yes_no('menu_play', default='y'):
        return
    
    # Создаем папку
    GAME_DIR.mkdir(exist_ok=True)
    
    # Устанавливаем Minecraft если нужно
    version_dir = GAME_DIR / 'versions' / version
    if not version_dir.exists():
        print(f"\n📥 {_('downloading')} Minecraft {version}...")
        try:
            mll.install.install_minecraft_version(version, str(GAME_DIR))
            print("✅ Minecraft installed")
        except Exception as e:
            print(f"❌ Error: {e}")
            input(f"\n{_('press_enter')}...")
            return
    
    # Устанавливаем загрузчик если нужно
    final_version = version
    if loader == 'forge':
        print(f"\n📦 Installing Forge...")
        try:
            for v in mll.forge.list_forge_versions():
                if version in v:
                    mll.forge.install_forge_version(v, str(GAME_DIR))
                    final_version = f"{version}-forge"
                    break
        except Exception as e:
            print(f"❌ Error: {e}")
    elif loader == 'fabric':
        print(f"\n📦 Installing Fabric...")
        try:
            mll.fabric.install_fabric(version, str(GAME_DIR))
            final_version = f"{version}-fabric"
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Запускаем
    print(f"\n🚀 Launching...")
    try:
        options = {
            "username": username,
            "jvmArguments": [f"-Xmx{ram}G", f"-Xms{ram}G", "-XX:+UseG1GC"],
            "gameDirectory": str(GAME_DIR),
        }
        
        command = mll.command.get_minecraft_command(final_version, str(GAME_DIR), options)
        subprocess.run(command)
        
        print(f"\n✅ Game finished")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    input(f"\n{_('press_enter')}...")

if __name__ == "__main__":
    try:
        load_language()
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n👋 {_('goodbye')}")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        input("\nPress Enter to exit...")