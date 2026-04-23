import json
from pathlib import Path
import discord
from discord import app_commands
from discord.ext import commands
from colorama import Fore, Style
# ==================================================================
# CONFIG
# ==================================================================
BASE = Path(__file__).resolve().parent.parent
CFG = BASE / "res" / "assets" / "config.json"

def ler_cfg():
    try:
        with open(CFG, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

dados = ler_cfg()
SID = dados.get("server_id")
LISTA_CMD = dados.get("comandos", ["ping"])
# ==================================================================
# CLASSE
# ==================================================================
class CmdBase(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        print(f"{Fore.GREEN}[CMD] Cog de comandos carregada.{Style.RESET_ALL}")

    @app_commands.command(name="ping", description="Teste de latência")
    async def cmd_ping(self, inter: discord.Interaction):
        if "ping" not in LISTA_CMD:
            await inter.response.send_message("Comando desativado.", ephemeral=True)
            return

        ms = round(self.bot.latency * 1000)
        await inter.response.send_message(f"🏓 Pong! `{ms}ms`", ephemeral=True)

async def setup(bot):
    await bot.add_cog(CmdBase(bot))
    print(f"{Fore.GREEN}[CMD] Cog de comandos carregada.{Style.RESET_ALL}")
