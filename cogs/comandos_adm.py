import os
import sys
import json
from pathlib import Path
import discord
from discord.ext import commands
# ------------- CONFIG ------------- #
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "res" / "assets" / "config.json"


def ler_config():
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

config = ler_config()
MODERADORES = {int(x) for x in config.get("moderadores", []) if str(x).isdigit()}
CORES = config.get("cores_embed", {})

# ------------- CLASSE ------------- #
class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        print("[CMD-ADM] Cog de comandos administrativos carregada.")

    def _is_moderador(self, usuario_id: int) -> bool:
        return usuario_id in MODERADORES

    @commands.command(name="restart")
    async def restart(self, ctx: commands.Context):
        if ctx.author.bot:
            return

        if not self._is_moderador(ctx.author.id):
            await ctx.reply("Você nao tem permissao para usar este comando.", mention_author=False)
            return

        embed = discord.Embed(
            title="🔄 Reiniciando...",
            description="O bot sera reiniciado em instantes.",
            color=int(CORES.get("aviso", "#FFA500").lstrip("#"), 16),
        )
        embed.set_footer(text=f"Solicitado por {ctx.author}")
        await ctx.send(embed=embed)

        os.environ["JEFF_RESTART_CHANNEL"] = str(ctx.channel.id)
        if ctx.guild:
            os.environ["JEFF_RESTART_GUILD"] = str(ctx.guild.id)

        await ctx.bot.close()
        os.execv(sys.executable, [sys.executable] + sys.argv)


async def setup(bot):
    await bot.add_cog(AdminCommands(bot))
