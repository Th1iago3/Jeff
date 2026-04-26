import json
from pathlib import Path
import discord
from discord import app_commands
from discord.ext import commands
from colorama import Fore, Style
# ------------- CONFIG ------------- #
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
LISTA_CMD = dados.get("comandos", ["ping", "vermissoes", "perfil"])
# ------------- CLASSE ------------- #
class CmdBase(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

class ProfileView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=180)

    @discord.ui.button(label="Atualizar", style=discord.ButtonStyle.secondary, emoji="🔄")
    async def refresh(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await self.message.edit(view=self)
        
    async def cog_load(self):
        print(f"{Fore.GREEN}[CMD] Cog de comandos carregada.{Style.RESET_ALL}")

    @app_commands.command(name="ping", description="Teste de latência")
    @app_commands.guilds(discord.Object(id=SID))
    async def cmd_ping(self, inter: discord.Interaction):
        if "ping" not in LISTA_CMD:
            await inter.response.send_message("Comando desativado.", ephemeral=True)
            return

        ms = round(self.bot.latency * 1000)
        await inter.response.send_message(f"🏓 Pong! `{ms}ms`", ephemeral=True)


        
    @app_commands.command(name="perfil", description="Veja o perfil completo de qualquer usuário.")
    @app_commands.guilds(discord.Object(id=SID))
    async def ver_perfil(self, inter: discord.Interaction, usuario: discord.Member = None):
        if usuario is None:
            usuario = inter.user
    
        avatar_url = usuario.avatar.url if usuario.avatar else usuario.default_avatar.url
        banner_url = usuario.banner.url if usuario.banner else None
        
        created_at = int(usuario.created_at.timestamp())
        joined_at = int(usuario.joined_at.timestamp()) if usuario.joined_at else 0
        
        roles = [role.mention for role in usuario.roles[1:]]
        roles_str = ", ".join(roles[-5:]) if roles else "Nenhum"
        if len(roles) > 5:
            roles_str += f" e +{len(roles) - 5} outros"
    
        embed = discord.Embed(
            title=f"{usuario.display_name}",
            description=usuario.global_name or usuario.name,
            color=usuario.color if usuario.color != discord.Color.default() else 0x2b2d31,
            timestamp=inter.created_at
        )
        
        embed.set_thumbnail(url=avatar_url)
        if banner_url:
            embed.set_image(url=banner_url)
            
        embed.add_field(name="🆔 ID do Usuário", value=f"`{usuario.id}`", inline=False)
        embed.add_field(name="📅 Conta Criada", value=f"<t:{created_at}:D>\n<t:{created_at}:R>", inline=True)
        if usuario.joined_at:
            embed.add_field(name="📥 Entrou no Servidor", value=f"<t:{joined_at}:D>\n<t:{joined_at}:R>", inline=True)
        
        pronouns = getattr(usuario, 'pronouns', None)
        if pronouns:
            embed.add_field(name="🏳️‍⚧️ Pronomes", value=pronouns, inline=True)
            
        embed.add_field(name="🎭 Apelido", value=usuario.nick or "Não possui", inline=True)
        embed.add_field(name="🛡️ Cargos ({})".format(len(roles)), value=roles_str, inline=False)
        
        flags = [flag.name.replace('_', ' ').title() for flag in usuario.public_flags if flag.value]
        embed.add_field(name="🚩 Badges", value=", ".join(flags) if flags else "Nenhuma", inline=True)
        
        view = ProfileView()
        message = await inter.response.send_message(embed=embed, view=view)
        view.message = message
                
                
            
async def setup(bot):
    await bot.add_cog(CmdBase(bot))
    print(f"{Fore.GREEN}[CMD] Cog de comandos carregada.{Style.RESET_ALL}")
