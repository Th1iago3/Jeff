################################## VEF. DEPEDENCIAS ################################## 
import sys
import subprocess
import importlib.util
################################## INSTALAR DEP. NECESSARIAS ################################## 
def dep():
  dep_map = {
    "discord": "discord.py",
    "colorama": "colorama",
    "httpx": "httpx",
    "dotenv": "python-dotenv"    
  }
  dep_faltando = []
  for modulo, pacote in dep_map.items():
    if importlib.util.find_spec(modulo) is None:
      dep_faltando.append(pacote)
  
  if dep_faltando:
    print(f"[INFO]: Instalando dependências: {', '.join(dep_faltando)}")
    subprocess.check_call([sys.executable, "-m", "pip", "install"] + dep_faltando)
    print(f"[INFO]: Instalação concluída. Reiniciando...")
    os.execv(sys.executable, [sys.executable] + sys.argv)

dep()
################################## BIBLIOTECAS ################################## 
import os
import sys
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
################################## INICIAR COLORAMA ################################## 
colorama_init(autoreset=True) 
################################## EXEC. VIA LOADER ################################## 
if __name__ == "__main__":
    from loader import Loader
    try:
        bot_app = Loader()
        bot_app.run()
    except Exception as e:
        print(f"{Fore.RED}[CRÍTICO] Erro fatal: {e}{Style.RESET_ALL}")
        sys.exit(1)
