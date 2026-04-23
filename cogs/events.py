import os
import sys
import json
import datetime
from pathlib import Path
from dotenv import load_dotenv
import discord
from discord.ext import commands
from colorama import Fore, Style
# ------------------------------------------------------------------
# CONFIGS
# ------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "res" / "assets"
ENV_PATH = ASSETS_DIR / "infos_secrets.env"
CONFIG_PATH = ASSETS_DIR / "config.json"

load_dotenv(ENV_PATH)

def carregar_config():
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"{Fore.RED}[ERRO] Falha ao ler config.json: {e}{Style.RESET_ALL}")
        return {}

config = carregar_config()
SERVER_ID = config.get("server_id")
MODERADORES = config.get("moderadores", [])
CORES = config.get("cores_embed", {})

class SystemMonitor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        if SERVER_ID:
            try:
                guild_obj = discord.Object(id=SERVER_ID)
                self.bot.tree.clear_commands(guild=guild_obj)
                await self.bot.tree.sync(guild=guild_obj)
                print(f"{Fore.GREEN}[SYNC] Comandos sincronizados e limpos.{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}[SYNC] Erro: {e}{Style.RESET_ALL}")

        os.system('cls' if os.name == 'nt' else 'clear')
        
        try:
            app_info = await self.bot.application_info()
            client_id = app_info.id
            invite_url = f"https://discord.com/api/oauth2/authorize?client_id={client_id}&permissions=8&scope=bot%20applications.commands"
        except Exception:
            invite_url = "Indisponível"

        guild = self.bot.get_guild(SERVER_ID) if SERVER_ID else None

        print(f"{Fore.CYAN}{'='*50}")
        print(f"{Fore.CYAN}       SISTEMA ONLINE")
        print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}[+] Bot: {Fore.GREEN}{self.bot.user}")
        print(f"{Fore.WHITE}[+] ID: {Fore.YELLOW}{self.bot.user.id}")
        print(f"{Fore.WHITE}[+] Hora: {Fore.BLUE}{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"{Fore.WHITE}[+] Invite: {Fore.LIGHTBLUE_EX}{invite_url}")
        
        if guild:
            print(f"{Fore.WHITE}[+] Server: {Fore.MAGENTA}{guild.name} ({guild.id})")
            print(f"{Fore.WHITE}[+] Membros: {Fore.MAGENTA}{guild.member_count}")
            
            mods_online = []
            for m in guild.members:
                if m.id in MODERADORES and not m.bot:
                    mods_online.append(m.name)
                    
            print(f"{Fore.WHITE}[+] Mods Online: {Fore.GREEN}{', '.join(mods_online) if mods_online else 'Nenhum'}")
        else:
            if SERVER_ID:
                print(f"{Fore.RED}[!] Servidor ID: >>{SERVER_ID}<< não encontrado.{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}[!] server_id não configurado.{Style.RESET_ALL}")
                
        print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot: return
        if SERVER_ID and (not message.guild or message.guild.id != SERVER_ID): return
        
        ts = message.created_at.strftime("%H:%M:%S")
        conteudo = message.content[:80] + ("..." if len(message.content) > 80 else "")
        print(f"{Fore.WHITE}[{Fore.BLUE}{ts}{Fore.WHITE}] #{message.channel.name} | {Fore.GREEN}{message.author.name}{Fore.WHITE}: {conteudo}")

    @commands.Cog.listener()
    async def on_app_command_error(self, interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
        print(f"{Fore.RED}[ERRO CMD] /{interaction.command.name}: {error}{Style.RESET_ALL}")
        if not interaction.response.is_done():
            await interaction.response.send_message("Erro interno.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(SystemMonitor(bot))
