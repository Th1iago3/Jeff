import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import discord
from discord.ext import commands
from colorama import Fore, Style

class Loader:
    def __init__(self):
        self.intents = discord.Intents.default()
        self.intents.message_content = True
        self.intents.members = True
        self.bot = commands.Bot(command_prefix=None, intents=self.intents)
        self.src_path = Path(__file__).parent

    def load_cogs(self):
        for filename in os.listdir(self.src_path):
            if filename.endswith(".py") and not filename.startswith("__"):
                try:
                    self.bot.load_extension(f"src.{filename[:-3]}")
                    print(f"{Fore.GREEN}[LOADER] OK: {filename}{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.RED}[LOADER] ERRO: {filename} -> {e}{Style.RESET_ALL}")

    def run(self):
        load_dotenv(self.src_path.parent / "infos_secrets.env")
        token = os.getenv("TOKEN")
        
        if not token:
            print(f"{Fore.RED}[CRITICAL] Token missing in infos_secrets.env{Style.RESET_ALL}")
            sys.exit(1)
            
        self.load_cogs()
        print(f"{Fore.YELLOW}[LOADER] Iniciando runtime...{Style.RESET_ALL}")
        self.bot.run(token)
