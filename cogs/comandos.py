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
CFG = BASE / "src" / "assets" / "config.json"

def ler_cfg():
    with open(CFG, "r", encoding="utf-8") as f:
        return json.load(f)
          
dados = ler_cfg()
SID = dados.get("server_id")
LISTA_CMD = dados.get("comandos", [])
# ==================================================================
# CLASSE
# ==================================================================
class CmdBase(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tree = bot.tree
        self.alvo = discord.Object(id=SID)
    # ==================================================================
    # INIT E SYNC
    # ==================================================================
    async def cog_load(self):
        await self.limpar_velhos()
        await self.sincronizar()

    async def limpar_velhos(self):
        self.tree.clear_commands(guild=self.alvo)
        print(f"{Fore.YELLOW}[CMD] Limpeza feita{Style.RESET_ALL}")

    async def sincronizar(self):
        await self.tree.sync(guild=self.alvo)
        print(f"{Fore.GREEN}[CMD] Sync completo{Style.RESET_ALL}")
    # ==================================================================
    # COMANDOS
    # ==================================================================
    @app_commands.command(name="ping", description="teste rapido")
    async def cmd_ping(self, inter: discord.Interaction):
        if "ping" not in LISTA_CMD:
            await inter.response.send_message("cmd off no config", ephemeral=True)
            return

        ms = round(self.bot.latency * 1000)
        await inter.response.send_message(f"pong! {ms}ms", ephemeral=True)

async def setup(bot):
    await bot.add_cog(CmdBase(bot))
