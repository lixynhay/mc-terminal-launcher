🚀 Minecraft Terminal Launcher
A lightweight, terminal-based Minecraft launcher with auto-updates and mod loader support. No GUI, just pure functionality!

https://img.shields.io/badge/version-2.0-blue
https://img.shields.io/badge/python-3.7%252B-green
https://img.shields.io/badge/license-MIT-orange
https://img.shields.io/badge/platform-Windows-lightgrey

📋 Features
⚡ Lightweight - No GUI, runs in terminal, minimal resource usage

🔄 Auto-updates - Automatically updates via .bat launcher

💾 Automatic RAM detection - Optimizes memory usage

📦 Multiple versions support - Any Minecraft version

🔧 Mod loaders - Forge, Fabric support

💿 Settings persistence - Remembers your preferences

📊 Progress indicators - Know what's happening

🎮 Offline mode - Play with any username

🚀 Quick Start (Recommended)
⭐ RECOMMENDED: Use the Batch File
The .bat launcher provides auto-updates and dependency management:

Download both files to the same folder:

launcher.py - The main launcher

launcher_updater.bat - The updater/launcher

Double-click launcher_updater.bat

That's it! The batch file will:

✅ Check for updates automatically

✅ Install Python libraries if needed

✅ Verify Java installation

✅ Launch the game

✅ Create backups before updating

Manual Installation
If you prefer to run manually:

bash
# Install required libraries
pip install minecraft-launcher-lib psutil requests

# Run the launcher
python launcher.py
📖 How to Use
With the Updater (Recommended)
text
====================================================
         MINECRAFT LAUNCHER UPDATER
====================================================
📌 Текущая версия: 2.0

[1] Проверить обновления
[2] Запустить лаунчер
[3] Установить библиотеки
[4] Очистить кэш и бэкапы
[0] Выход
Just press 2 and you're good to go!

First Launch
The launcher will guide you through:

Java Check - Verifies Java is installed

Version Selection - Choose Minecraft version

1.20.1 (stable)

1.19.2 (popular)

1.16.5 (old mods)

latest (latest release)

RAM Configuration - Auto or manual

Mod Loader - Vanilla, Forge, or Fabric

Download & Launch - Automatic installation

⚙️ Configuration
Settings are saved in config.json:

json
{
  "version": "1.20.1",
  "username": "Player",
  "ram": 4,
  "loader": "forge"
}
📁 Project Structure
text
mc-terminal-launcher/
├── launcher.py              # Main launcher (required)
├── launcher_updater.bat     ⭐ Windows updater (recommended)
├── README.md                # This file
├── .minecraft/              # Game files (created automatically)
├── backups/                 # Backup copies (created before updates)
└── config.json              # Your settings (created automatically)
🎯 Why Use the Batch File?
The launcher_updater.bat is the recommended way to run the launcher because:

Feature	Manual Run	With .bat
Auto-updates	❌ No	✅ Yes
Backup before update	❌ No	✅ Yes
Library installation	❌ Manual	✅ Automatic
Java check	❌ Manual	✅ Automatic
Clean cache	❌ Manual	✅ One-click
Update notifications	❌ No	✅ Yes
🔧 Troubleshooting
Common Issues & Solutions
"Python not found"

Download from python.org

✅ Batch file will warn you

"Java not found"

Download from java.com

✅ Batch file checks this

"Library missing"

✅ Batch file installs automatically

"Update failed"

✅ Batch file creates backups so you can rollback

📦 Requirements
Windows 7/8/10/11 (for .bat launcher)

Python 3.7 or higher

Java 8 or higher

Internet connection (for downloads/updates)

🚀 Quick Installation
One-liner (Copy & Paste in CMD)
batch
curl -L https://github.com/yourusername/mc-terminal-launcher/releases/latest/download/launcher.py -o launcher.py && curl -L https://github.com/yourusername/mc-terminal-launcher/releases/latest/download/launcher_updater.bat -o launcher_updater.bat && launcher_updater.bat
🔒 Security
✅ No telemetry or data collection

✅ All downloads from official Mojang servers

✅ Open source - fully auditable

✅ No admin privileges required

✅ Backup system prevents data loss

📝 License
MIT License - Free to use and modify!

🙏 Credits
minecraft-launcher-lib - Python library

Mojang - For Minecraft

All contributors

⭐ Quick Start Summary
Download launcher.py and launcher_updater.bat

Put them in the same folder

Double-click launcher_updater.bat

Press 2 to launch

Enjoy! 🎮

The batch file handles everything else automatically!

Made with ❤️ for Minecraft players who love the terminal and hate complicated setups
