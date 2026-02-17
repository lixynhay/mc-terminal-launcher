# 🚀 Minecraft Terminal Launcher

A lightweight, terminal-based Minecraft launcher with auto-updates and mod loader support. No GUI, just pure functionality!

![Version](https://img.shields.io/badge/version-2.0-blue)
![Python](https://img.shields.io/badge/python-3.7%2B-green)
![License](https://img.shields.io/badge/license-MIT-orange)
![Windows](https://img.shields.io/badge/platform-Windows-lightgrey)

## 📋 Features

- ⚡ **Lightweight** - No GUI, runs in terminal, minimal resource usage
- 🔄 **Auto-updates** - Automatically updates via `.bat` launcher
- 💾 **Automatic RAM detection** - Optimizes memory usage
- 📦 **Multiple versions support** - Any Minecraft version
- 🔧 **Mod loaders** - Forge, Fabric support
- 💿 **Settings persistence** - Remembers your preferences
- 📊 **Progress indicators** - Know what's happening
- 🎮 **Offline mode** - Play with any username

## 🚀 Quick Start (Recommended)

### ⭐ **RECOMMENDED: Use the Batch File**

The `.bat` launcher provides auto-updates and dependency management:

1. **Download both files** to the same folder:
   - `launcher.py` - The main launcher
   - `launcher_updater.bat` - The updater/launcher

2. **Double-click** `launcher_updater.bat`

That's it! The batch file will:
- ✅ Check for updates automatically
- ✅ Install Python libraries if needed
- ✅ Verify Java installation
- ✅ Launch the game
- ✅ Create backups before updating

### Manual Installation

If you prefer to run manually:

```bash
# Install required libraries
pip install minecraft-launcher-lib psutil requests

# Run the launcher
python launcher.py
