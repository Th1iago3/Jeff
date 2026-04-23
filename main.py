import instl
instl.dep()

import os
import json
import asyncio
import threading
from typing import Optional, Dict, Any, List, Union
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import discord
from discord.ext import commands
from discord import app_commands
import httpx
from colorama import init as colorama_init, Fore, Style

colorama_init(autoreset=True)

if __name__ == "__main__":
    from loader import Loader
    try:
        bot_app = Loader()
        bot_app.run()
    except Exception as e:
        print(f"{Fore.RED}[CRITICO] Erro fatal: {e}{Style.RESET_ALL}")
        import sys
        sys.exit(1)
