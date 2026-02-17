#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Minecraft Launcher - User Edition (Multilingual)"""

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
LANG_FILE = SCRIPT_DIR / "language.json"

# Языковые файлы
LANGUAGES = {
    'en': {
        # Header
        'title': 'MINECRAFT LAUNCHER',
        'game_folder': 'Game folder',
        
        # Java check
        'checking_java': 'Checking Java',
        'java_found': 'Java found',
        'java_not_found': 'Java not found',
        'download_java': 'Download Java from: https://www.java.com/',
        'continue_without_java': 'Continue without Java',
        
        # Settings
        'use_saved_settings': 'Use saved settings',
        'saved_settings': 'SAVED SETTINGS',
        'version': 'Version',
        'username': 'Username',
        'ram': 'RAM',
        'loader': 'Loader',
        'vanilla': 'Vanilla',
        
        # New settings
        'new_settings': 'NEW SETTINGS',
        'popular_versions': 'Popular versions',
        'stable': 'stable',
        'popular': 'popular',
        'old_mods': 'for old mods',
        'latest': 'latest',
        'enter_version': 'Version',
        'latest_version': 'Latest version',
        'enter_username': 'Username',
        'player': 'Player',
        
        # RAM
        'total_ram': 'Total RAM',
        'recommended_ram': 'Recommended',
        'ram_gb': 'RAM (GB)',
        'enter_number': 'Please enter a number',
        'enter_1_to': 'Enter from 1 to',
        
        # Loader
        'mod_loaders': 'MOD LOADERS',
        'vanilla_option': 'Vanilla (no mods)',
        'forge_option': 'Forge',
        'fabric_option': 'Fabric',
        'choose_loader': 'Choose',
        'selected': 'Selected',
        
        # Summary
        'summary': 'SUMMARY',
        'start_installation': 'Start installation and launch',
        'change_settings': 'Change settings',
        
        # Installation
        'installing_minecraft': 'INSTALLING MINECRAFT',
        'downloading_files': 'Downloading files... (this may take a few minutes)',
        'downloading': 'Downloading',
        'success_installed': 'Minecraft successfully installed',
        'client_size': 'Client size',
        'install_error': 'Installation error',
        'try_again': 'Try again',
        
        # Loader installation
        'installing_loader': 'INSTALLING {0}',
        'forge_installed': 'Forge {0} installed',
        'forge_not_found': 'Forge not found for version {0}',
        'fabric_installed': 'Fabric installed',
        'loader_error': 'Error installing {0}',
        
        # Launch
        'launching': 'LAUNCHING MINECRAFT',
        'preparing': 'Preparing',
        'game_launching': 'Minecraft is launching...',
        'close_game_to_return': 'Close the game to return to launcher',
        'game_finished': 'Game finished',
        'launch_error': 'Launch error',
        
        # Other
        'goodbye': 'Goodbye',
        'thanks_for_using': 'Thanks for using',
        'another_version': 'Launch another version',
        'yes': 'yes',
        'no': 'no',
        'y': 'y',
        'n': 'n',
        
        # Updates
        'checking_updates': 'Checking for updates',
        'update_available': 'Update available',
        'current_version': 'Current version',
        'new_version': 'New version',
        'whats_new': "What's new",
        'update_now': 'Update now',
        'skip_update': 'Skip update',
        'update_complete': 'Update complete',
        'update_error': 'Update error',
    },
    
    'ru': {
        # Header
        'title': 'MINECRAFT ЛАУНЧЕР',
        'game_folder': 'Папка игры',
        
        # Java check
        'checking_java': 'Проверка Java',
        'java_found': 'Java найдена',
        'java_not_found': 'Java не найдена',
        'download_java': 'Скачайте Java с: https://www.java.com/',
        'continue_without_java': 'Продолжить без Java',
        
        # Settings
        'use_saved_settings': 'Использовать сохраненные настройки',
        'saved_settings': 'СОХРАНЕННЫЕ НАСТРОЙКИ',
        'version': 'Версия',
        'username': 'Никнейм',
        'ram': 'RAM',
        'loader': 'Загрузчик',
        'vanilla': 'Vanilla',
        
        # New settings
        'new_settings': 'НОВЫЕ НАСТРОЙКИ',
        'popular_versions': 'Популярные версии',
        'stable': 'стабильная',
        'popular': 'популярная',
        'old_mods': 'для старых модов',
        'latest': 'последняя',
        'enter_version': 'Версия',
        'latest_version': 'Последняя версия',
        'enter_username': 'Никнейм',
        'player': 'Игрок',
        
        # RAM
        'total_ram': 'Всего RAM',
        'recommended_ram': 'Рекомендуется',
        'ram_gb': 'RAM (GB)',
        'enter_number': 'Пожалуйста, введите число',
        'enter_1_to': 'Введите от 1 до',
        
        # Loader
        'mod_loaders': 'ЗАГРУЗЧИКИ МОДОВ',
        'vanilla_option': 'Vanilla (без модов)',
        'forge_option': 'Forge',
        'fabric_option': 'Fabric',
        'choose_loader': 'Выберите',
        'selected': 'Выбран',
        
        # Summary
        'summary': 'СВОДКА',
        'start_installation': 'Начать установку и запуск',
        'change_settings': 'Изменить настройки',
        
        # Installation
        'installing_minecraft': 'УСТАНОВКА MINECRAFT',
        'downloading_files': 'Идет загрузка файлов... (это может занять несколько минут)',
        'downloading': 'Загрузка',
        'success_installed': 'Minecraft успешно установлен',
        'client_size': 'Размер клиента',
        'install_error': 'Ошибка установки',
        'try_again': 'Попробовать снова',
        
        # Loader installation
        'installing_loader': 'УСТАНОВКА {0}',
        'forge_installed': 'Forge {0} установлен',
        'forge_not_found': 'Forge не найден для версии {0}',
        'fabric_installed': 'Fabric установлен',
        'loader_error': 'Ошибка установки {0}',
        
        # Launch
        'launching': 'ЗАПУСК MINECRAFT',
        'preparing': 'Подготовка',
        'game_launching': 'Minecraft запускается...',
        'close_game_to_return': 'Закройте игру, чтобы вернуться в лаунчер',
        'game_finished': 'Игра завершена',
        'launch_error': 'Ошибка запуска',
        
        # Other
        'goodbye': 'До свидания',
        'thanks_for_using': 'Спасибо за использование',
        'another_version': 'Запустить другую версию',
        'yes': 'да',
        'no': 'нет',
        'y': 'д',
        'n': 'н',
        
        # Updates
        'checking_updates': 'Проверка обновлений',
        'update_available': 'Доступно обновление',
        'current_version': 'Текущая версия',
        'new_version': 'Новая версия',
        'whats_new': 'Что нового',
        'update_now': 'Обновить сейчас',
        'skip_update': 'Пропустить',
        'update_complete': 'Обновление завершено',
        'update_error': 'Ошибка обновления',
    }
}

# Текущий язык
current_lang = 'ru'  # По умолчанию русский

def _(key, **kwargs):
    """Перевод строки"""
    text = LANGUAGES[current_lang].get(key, key)
    if kwargs:
        text = text.format(**kwargs)
    return text

def load_language():
    """Загружает язык из файла"""
    global current_lang
    try:
        if LANG_FILE.exists():
            with open(LANG_FILE, 'r', encoding='utf-8') as f:
                lang_data = json.load(f)
                current_lang = lang_data.get('language', 'ru')
    except:
        pass

def save_language(lang):
    """Сохраняет язык в файл"""
    global current_lang
    current_lang = lang
    with open(LANG_FILE, 'w', encoding='utf-8') as f:
        json.dump({'language': lang}, f)

# Анимация загрузки
class Spinner:
    """Класс для анимации спиннера"""
    def __init__(self, message):
        self.message = message
        self.spinner = ['|', '/', '-', '\\']
        self.running = False
        self.thread = None
        
    def spin(self):
        self.running = True
        self.thread = threading.Thread(target=self._animate)
        self.thread.daemon = True
        self.thread.start()
    
    def _animate(self):
        i = 0
        while self.running:
            sys.stdout.write(f"\r{self.message} {self.spinner[i % 4]}")
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1
    
    def stop(self, success=True):
        self.running = False
        if self.thread:
            self.thread.join()
        if success:
            sys.stdout.write(f"\r{self.message} ✅\n")
        else:
            sys.stdout.write(f"\r{self.message} ❌\n")
        sys.stdout.flush()

# Функции лаунчера
def load_config():
    """Загружает конфигурацию"""
    try:
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except:
        pass
    return {}

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
    print(f"     {_('title')} v2.0")
    print("=" * 60)
    print(f"📁 {_('game_folder')}: {GAME_DIR}")
    print(f"🌍 Language: {'English' if current_lang == 'en' else 'Русский'}")
    print("=" * 60)

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
        print(_('yes') + '/' + _('no'))

def get_ram():
    """Получает количество RAM"""
    try:
        import psutil
        total = psutil.virtual_memory().total / (1024**3)
        recommended = min(int(total * 0.7), 8)
        
        print(f"\n💻 {_('total_ram')}: {total:.1f} GB")
        print(f"📊 {_('recommended_ram')}: {recommended} GB")
        
        while True:
            try:
                ram_input = input(f"👉 {_('ram_gb')} [{recommended}]: ").strip()
                if not ram_input:
                    return recommended
                ram = int(ram_input)
                if 1 <= ram <= total:
                    return ram
                print(f"{_('enter_1_to')} {int(total)}")
            except ValueError:
                print(_('enter_number'))
    except ImportError:
        print("\n⚠️ psutil not installed, using 2 GB")
        return 2
    except Exception as e:
        print(f"\n⚠️ Error: {e}, using 2 GB")
        return 2

def check_java():
    """Проверяет наличие Java"""
    spinner = Spinner(f"🔍 {_('checking_java')}")
    spinner.spin()
    
    try:
        result = subprocess.run(['java', '-version'], 
                              capture_output=True, text=True)
        spinner.stop(True)
        java_version = result.stderr.split('\n')[0]
        print(f"✅ {_('java_found')}: {java_version}")
        return True
    except:
        spinner.stop(False)
        print(f"❌ {_('java_not_found')}")
        print(f"📥 {_('download_java')}")
        return False

def install_minecraft(version, game_dir):
    """Устанавливает Minecraft с индикацией"""
    print(f"\n📥 {_('installing_minecraft')} {version}")
    print("=" * 60)
    print(f"⏳ {_('downloading_files')}")
    
    spinner = Spinner(f"🔄 {_('downloading')}")
    spinner.spin()
    
    try:
        game_dir.mkdir(exist_ok=True)
        mll.install.install_minecraft_version(version, str(game_dir))
        spinner.stop(True)
        print(f"✅ {_('success_installed')}")
        
        version_dir = game_dir / 'versions' / version
        if version_dir.exists():
            jar_file = version_dir / f'{version}.jar'
            if jar_file.exists():
                size = jar_file.stat().st_size / (1024**2)
                print(f"📦 {_('client_size')}: {size:.1f} MB")
        
        return True
    except Exception as e:
        spinner.stop(False)
        print(f"❌ {_('install_error')}: {e}")
        return False

def install_loader(version, loader_type, game_dir):
    """Устанавливает загрузчик модов"""
    print(f"\n📦 {_('installing_loader', loader=loader_type.upper())}")
    print("=" * 60)
    
    spinner = Spinner(f"🔄 {_('installing_loader', loader=loader_type)}")
    spinner.spin()
    
    try:
        if loader_type == "forge":
            forge_versions = mll.forge.list_forge_versions()
            forge_version = None
            for v in forge_versions:
                if version in v:
                    forge_version = v
                    break
            
            if forge_version:
                mll.forge.install_forge_version(forge_version, str(game_dir))
                spinner.stop(True)
                print(f"✅ {_('forge_installed', forge_version)}")
                return f"{version}-forge"
            else:
                spinner.stop(False)
                print(f"❌ {_('forge_not_found', version)}")
                return version
                
        elif loader_type == "fabric":
            mll.fabric.install_fabric(version, str(game_dir))
            spinner.stop(True)
            print(f"✅ {_('fabric_installed')}")
            return f"{version}-fabric"
        
        return version
    except Exception as e:
        spinner.stop(False)
        print(f"❌ {_('loader_error', loader_type)}: {e}")
        return version

def launch_game(final_version, username, ram, game_dir):
    """Запускает игру"""
    print(f"\n🚀 {_('launching')}")
    print("=" * 60)
    print(f"📋 {_('version')}: {final_version}")
    print(f"👤 {_('username')}: {username}")
    print(f"💾 {_('ram')}: {ram} GB")
    print(f"📁 {_('game_folder')}: {game_dir}")
    
    spinner = Spinner(f"🔄 {_('preparing')}")
    spinner.spin()
    
    try:
        options = {
            "username": username,
            "jvmArguments": [f"-Xmx{ram}G", f"-Xms{ram}G", "-XX:+UseG1GC"],
            "gameDirectory": str(game_dir),
            "launcherName": "TerminalLauncher"
        }
        
        command = mll.command.get_minecraft_command(final_version, str(game_dir), options)
        spinner.stop(True)
        
        print(f"\n✅ {_('game_launching')}")
        print(f"ℹ️  {_('close_game_to_return')}")
        print("-" * 60)
        
        if os.name == 'nt':
            cmd_str = ' '.join(f'"{arg}"' if ' ' in arg else arg for arg in command)
            os.system(cmd_str)
        else:
            os.system(' '.join(command))
        
        print(f"\n✅ {_('game_finished')}")
        return True
        
    except Exception as e:
        spinner.stop(False)
        print(f"❌ {_('launch_error')}: {e}")
        return False

def main():
    """Главная функция"""
    global current_lang
    load_language()
    config = load_config()
    
    while True:
        print_header()
        
        # Проверяем Java
        if not check_java():
            if not get_yes_no('continue_without_java', default='n'):
                print(f"\n👋 {_('goodbye')}")
                break
            print()
        
        # Быстрый запуск если есть конфиг
        if config and get_yes_no('use_saved_settings', default='y'):
            version = config.get('version', '1.20.1')
            username = config.get('username', 'Player')
            ram = config.get('ram', 2)
            loader = config.get('loader')
            
            print(f"\n📋 {_('saved_settings')}:")
            print(f"   {_('version')}: {version}")
            print(f"   {_('username')}: {username}")
            print(f"   {_('ram')}: {ram} GB")
            print(f"   {_('loader')}: {loader if loader else _('vanilla')}")
            print()
        else:
            # Новые настройки
            print(f"\n📥 {_('new_settings')}")
            print("-" * 60)
            
            # Версия
            print(f"\n📋 {_('popular_versions')}:")
            print(f"   • 1.20.1 ({_('stable')})")
            print(f"   • 1.19.2 ({_('popular')})")
            print(f"   • 1.16.5 ({_('old_mods')})")
            print(f"   • latest ({_('latest')})")
            version = input(f"👉 {_('enter_version')} [1.20.1]: ").strip() or "1.20.1"
            
            if version.lower() == "latest":
                try:
                    version = mll.utils.get_latest_version()['release']
                    print(f"   ✅ {_('latest_version')}: {version}")
                except:
                    version = "1.20.1"
                    print(f"   ⚠️ Error, using {version}")
            
            # Никнейм
            username = input(f"👤 {_('enter_username')} [{_('player')}]: ").strip() or _('player')
            
            # RAM
            ram = get_ram()
            
            # Загрузчик
            print(f"\n📦 {_('mod_loaders')}:")
            print(f"   1. {_('vanilla_option')}")
            print(f"   2. {_('forge_option')}")
            print(f"   3. {_('fabric_option')}")
            loader_choice = input(f"👉 {_('choose_loader')} [1]: ").strip() or "1"
            
            loader = None
            if loader_choice == "2":
                loader = "forge"
                print(f"   ✅ {_('selected')}: Forge")
            elif loader_choice == "3":
                loader = "fabric"
                print(f"   ✅ {_('selected')}: Fabric")
            
            # Сохраняем конфиг
            config = {
                'version': version,
                'username': username,
                'ram': ram,
                'loader': loader
            }
            save_config(config)
            print("\n💾 Settings saved")
        
        # Показываем сводку
        print("\n" + "=" * 60)
        print(f"📋 {_('summary')}:")
        print(f"   {_('version')}: {version}")
        print(f"   {_('username')}: {username}")
        print(f"   {_('ram')}: {ram} GB")
        print(f"   {_('loader')}: {loader if loader else _('vanilla')}")
        print("=" * 60)
        
        if not get_yes_no('start_installation', default='y'):
            if get_yes_no('change_settings', default='y'):
                continue
            else:
                print(f"\n👋 {_('goodbye')}")
                break
        
        # УСТАНОВКА MINECRAFT
        success = install_minecraft(version, GAME_DIR)
        
        if not success:
            if not get_yes_no('try_again', default='y'):
                break
            continue
        
        # УСТАНОВКА ЗАГРУЗЧИКА
        final_version = version
        if loader:
            final_version = install_loader(version, loader, GAME_DIR)
        
        # ЗАПУСК
        launch_game(final_version, username, ram, GAME_DIR)
        
        # Спрашиваем про следующий запуск
        print()
        if not get_yes_no('another_version', default='n'):
            print(f"\n👋 {_('thanks_for_using')}")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n👋 {_('goodbye')}")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        input("\nPress Enter to exit...")