################################## VEF. DEPEDENCIAS ################################## 
import sys
import subprocess
################################## INSTALAR DEP. NECESSARIAS ################################## 
def dep():
  dep = {
    "discord",
    "colorama",
    "httpx",
    "dotenv"    
  }
  dep_faltando = []
  for pacote in dep:
    try:
      __import__(pacote.replace("-", "_"))
    except ImportError:
      dep_faltando.append(pacote)

if dep_faltando:
  print(f"[INFO]: Instalando: {', '.join(dep_faltando)}")
  subprocess.check_call([sys.executable, "-m", "pip", "install"] + dep_faltando)
  print(f"[INFO]: Tudo pronto!")
  sys.exit(0)

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

################################## EXECUÇÃO VIA LOADER ################################## 
if __name__ == "__main__":
    from src.loader import Loader
    Loader().run()
