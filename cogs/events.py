import os
import sys
import json
import datetime
import asyncio
from pathlib import Path
from dotenv import load_dotenv
import discord
from discord import ActivityType, Activity, CustomActivity, Streaming, Status
from typing import Optional
from discord.ext import commands
from colorama import Fore, Style
# ----------------- CONFIG ----------------- #
BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "res" / "assets"
ENV_PATH = ASSETS_DIR / "infos_secrets.env"
CONFIG_PATH = ASSETS_DIR / "config.json"
load_dotenv(ENV_PATH)
STATUS_ATUAL = None
# ----------------- FUNCOES ----------------- #
def carregar_config():
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            raw = json.load(f)
        cleaned = {}
        for k, v in raw.items():
            ck = k.strip()
            if isinstance(v, str): cleaned[ck] = v.strip()
            elif isinstance(v, list): cleaned[ck] = [str(x).strip() for x in v]
            elif isinstance(v, dict): cleaned[ck] = {sk.strip(): sv.strip() if isinstance(sv, str) else sv for sk, sv in v.items()}
            else: cleaned[ck] = v
        return cleaned
    except Exception:
        return {}

def clear():
    os.system("cls" if os.name == "nt" else "clear")

async def status_atividade(bot, tipo, titulo, description=None, imagem=None, url=None, emoji=None, status_bot="online", duracao=None):
    try:
        tipo_lower = tipo.lower().strip()
        mapa_tipos = {
            "playing": ActivityType.playing,
            "streaming": ActivityType.streaming,
            "listening": ActivityType.listening,
            "watching": ActivityType.watching,
            "competing": ActivityType.competing,
            "custom": None
        }
        
        if tipo_lower not in mapa_tipos:
            print(f"{Fore.YELLOW}[STATUS] Tipo invalido: {tipo}. Tipos suportados: {list(mapa_tipos.keys())}{Style.RESET_ALL}")
            return False
        
        if url and tipo_lower != "streaming":
            url = None
            
        target_emoji = emoji or imagem
        valid_statuses = {"online": Status.online, "idle": Status.idle, "dnd": Status.dnd, "offline": Status.offline, "invisible": Status.invisible}
        bot_status = valid_statuses.get(status_bot.lower(), Status.online)
        
        if tipo_lower == "custom":
            activity = CustomActivity(name=titulo, emoji=target_emoji)
        elif tipo_lower == "streaming":
            if not url:
                print(f"{Fore.RED}[STATUS] Tipo 'streaming' requer uma URL valida (Twitch/YouTube).{Style.RESET_ALL}")
                return False
            activity = Streaming(name=titulo, url=url, details=description)
        else:
            kwargs = {"type": mapa_tipos[tipo_lower], "name": titulo}
            if description:
                kwargs["details"] = description
            activity = Activity(**kwargs)
            
        await bot.change_presence(activity=activity, status=bot_status)
        
        atividade_str = f"{tipo.title()}: {titulo}"
        if description and tipo_lower != "custom":
            atividade_str += f" - {description}"
        if url:
            atividade_str += f" | {url}"
        if target_emoji:
            atividade_str += f" | {target_emoji}"
            
        global STATUS_ATUAL
        STATUS_ATUAL = atividade_str
        
        if duracao and duracao > 0:
            async def auto_clear():
                global STATUS_ATUAL
                await asyncio.sleep(duracao)
                try:
                    await bot.change_presence(activity=None, status=bot_status)
                    STATUS_ATUAL = "Nenhuma"
                except Exception:
                    pass
            asyncio.create_task(auto_clear())
            
        return True
    except Exception as e:
        print(f"{Fore.RED}[STATUS] Erro ao definir atividade: {e}{Style.RESET_ALL}")
        return False


# ----------------- COGS ----------------- #
config = carregar_config()
SERVER_ID = int(config.get("server_id", 0))
MODERADORES = {int(x) for x in config.get("moderadores", []) if str(x).isdigit()}
CORES = config.get("cores_embed", {})
class SystemMonitor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await asyncio.sleep(2)
        if SERVER_ID > 0:
            try:
                guild_obj = discord.Object(id=SERVER_ID)
                await asyncio.sleep(0.5)
                sync_result = await self.bot.tree.sync(guild=guild_obj)
                if sync_result is None:
                    print(f"{Fore.YELLOW}[SYNC] Nenhum comando sincronizado.{Style.RESET_ALL}")
                else:
                    print(f"{Fore.GREEN}[SYNC] {len(sync_result)} comandos sincronizados:{Style.RESET_ALL}")
                    for cmd in sync_result:
                        print(f"{Fore.GREEN}  /{cmd.name}{Style.RESET_ALL}")
            except Exception as e:
                import traceback
                print(f"{Fore.RED}[SYNC] Erro ao sincronizar comandos:{Style.RESET_ALL}")
                traceback.print_exc()

        await asyncio.sleep(1)
        clear()
        try:
            app_info = await self.bot.application_info()
            invite_url = f"https://discord.com/api/oauth2/authorize?client_id={app_info.id}&permissions=8&scope=bot%20applications.commands"
        except Exception:
            invite_url = "Indisponivel"

        guild = self.bot.get_guild(SERVER_ID) if SERVER_ID else None
        await status_atividade(self.bot, "streaming", "a TV", "Jeff esta assistindo a TV", imagem=None, url="https://www.youtube.com/watch?v=NlPoPjPeyL0")
        print(f"{Fore.CYAN}{'='*50}")
        print(f"{Fore.CYAN}       SISTEMA ONLINE ")
        print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}[+] Bot: {Fore.GREEN}{self.bot.user}")
        print(f"{Fore.WHITE}[+] ID: {Fore.YELLOW}{self.bot.user.id}")
        print(f"{Fore.WHITE}[+] Hora: {Fore.BLUE}{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"{Fore.WHITE}[+] Invite: {Fore.LIGHTBLUE_EX}{invite_url}")
        if guild:
            print(f"{Fore.WHITE}[+] Server: {Fore.MAGENTA}{guild.name} ({guild.id})")
            print(f"{Fore.WHITE}[+] Membros: {Fore.MAGENTA}{guild.member_count}")
            mods_online = [m.name for m in guild.members if not m.bot and m.id in MODERADORES]
            print(f"{Fore.WHITE}[+] Mods Online: {Fore.GREEN}{', '.join(mods_online) if mods_online else 'Nenhum'}")
            print(f"{Fore.WHITE}[+] Status de Atividade: {Fore.BLUE}{STATUS_ATUAL}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[!] Servidor nao encontrado.{Style.RESET_ALL}")
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
