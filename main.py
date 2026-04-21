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
