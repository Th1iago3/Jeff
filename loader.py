import os
import sys
import asyncio
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
        self.bot = commands.Bot(command_prefix="!", intents=self.intents)
        self.cogs_path = Path(__file__).parent / "cogs"

    async def _load_cogs_async(self):
        print(f"{Fore.YELLOW}[LOADER] Varrendo cogs...{Style.RESET_ALL}")
        if not self.cogs_path.exists():
            print(f"{Fore.RED}[LOADER] Pasta cogs não encontrada!{Style.RESET_ALL}")
            return

        for filename in os.listdir(self.cogs_path):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = f"cogs.{filename[:-3]}"
                try:
                    await self.bot.load_extension(module_name)
                    print(f"{Fore.GREEN}[LOADER] OK: {filename}{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.RED}[LOADER] ERRO: {filename} -> {e}{Style.RESET_ALL}")

    def run(self):
        assets_dir = Path(__file__).parent / "src" / "assets"
        env_path = assets_dir / "infos_secrets.env"
        
        if not env_path.exists():
            print(f"{Fore.RED}[CRITICAL] Token não encontrado em src/assets/infos_secrets.env{Style.RESET_ALL}")
            sys.exit(1)
            
        load_dotenv(env_path)
        token = os.getenv("TOKEN")
        
        if not token:
            print(f"{Fore.RED}[CRITICAL] Variável TOKEN vazia no .env{Style.RESET_ALL}")
            sys.exit(1)
            
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            loop.run_until_complete(self._load_cogs_async())
            print(f"{Fore.YELLOW}[LOADER] Conectando...{Style.RESET_ALL}")
            self.bot.run(token)
        except discord.LoginFailure:
            print(f"{Fore.RED}[AUTH] Token inválido. Verifique o infos_secrets.env{Style.RESET_ALL}")
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[SISTEMA] Desligamento manual.{Style.RESET_ALL}")
        finally:
            loop.close()
