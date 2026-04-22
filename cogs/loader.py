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
        self.cogs_path = Path(__file__).parent

    def load_cogs(self):
        print(f"{Fore.YELLOW}[LOADER] Varrendo cogs...{Style.RESET_ALL}")
        for filename in os.listdir(self.cogs_path):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = f"cogs.{filename[:-3]}"
                try:
                    self.bot.load_extension(module_name)
                    print(f"{Fore.GREEN}[LOADER] OK: {filename}{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.RED}[LOADER] ERRO: {filename} -> {e}{Style.RESET_ALL}")

    def run(self):
        assets_dir = self.cogs_path.parent / "src" / "assets"
        env_path = assets_dir / "infos_secrets.env"
        
        load_dotenv(env_path)
        token = os.getenv("TOKEN")
        
        if not token:
            print(f"{Fore.RED}[CRITICAL] Token não encontrado em src/assets/infos_secrets.env{Style.RESET_ALL}")
            sys.exit(1)
            
        self.load_cogs()
        print(f"{Fore.YELLOW}[LOADER] Conectando...{Style.RESET_ALL}")
        try:
            self.bot.run(token)
        except Exception as e:
            if e == "Improper token has been passed.":
                print(f"{Fore.RED}[CRITICAL] Token inválido. Verifique src/assets/infos_secrets.env{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[CRITICAL] Erro ao iniciar o bot: {e}{Style.RESET_ALL}")
            sys.exit(1)

if __name__ == "__main__":
    loader = Loader()
    loader.run()
