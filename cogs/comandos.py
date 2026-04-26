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

dados = ler_cfg()
SID = int(dados.get("server_id", 0))
LISTA_CMD = dados.get("comandos", ["ping", "perfil"])
# ------------- CLASSE ------------- #
class ProfileView(discord.ui.View):
    # ------------- VIEW / COMPONENTS ------------- #
    def __init__(self, user: discord.Member):
        super().__init__(timeout=180)
        self.usr = user
        self.msg = None

    async def _build_embed(self, ctx_inter: discord.Interaction):
        u = self.usr
        av = u.avatar.url if u.avatar else u.default_avatar.url
        bn = u.banner.url if u.banner else None
        cr = int(u.created_at.timestamp())
        jd = int(u.joined_at.timestamp()) if u.joined_at else 0
        rls = [r.mention for r in u.roles[1:]]
        rls_str = ", ".join(rls[-5:]) if rls else "Nenhum"
        if len(rls) > 5: rls_str += f" e +{len(rls) - 5} outros"
        status = str(getattr(u, 'status', 'desconhecido')).title()
        act = "Nenhuma"
        if getattr(u, 'activity', None):
            a = u.activity
            act_name = getattr(a, 'name', None) or getattr(a, 'state', None) or getattr(a, 'details', None)
            act_type = a.type.name.title() if hasattr(a, 'type') else 'Atividade'
            act = f"{act_type}: {act_name}" if act_name else act_type

        flags = [f.replace('_', ' ').title() for f in u.public_flags.all()]

        emb = discord.Embed(
            title=f"{u.display_name}",
            description=u.global_name or u.name,
            color=u.color if u.color != discord.Color.default() else 0x2b2d31,
            timestamp=ctx_inter.created_at,
        )

        if bn:
            emb.set_thumbnail(url=bn)
        else:
            emb.set_thumbnail(url=av)
        emb.set_image(url=av)

        disc = getattr(u, 'discriminator', None)
        author_name = f"{u.name}#{disc}" if disc else f"{u.name}"
        emb.set_author(name=author_name, icon_url=av)

        emb.add_field(name="🆔 ID do Usuário", value=f"`{u.id}`", inline=False)
        emb.add_field(name="🎂 Conta Criada", value=f"<t:{cr}:D>\n<t:{cr}:R>", inline=True)
        if u.joined_at:
            emb.add_field(name="📥 Entrou no Servidor", value=f"<t:{jd}:D>\n<t:{jd}:R>", inline=True)
        emb.add_field(name="🤖 É Bot?", value="Sim" if u.bot else "Não", inline=True)
        if getattr(u, 'pronouns', None):
            emb.add_field(name="🏷️ Pronomes", value=getattr(u, 'pronouns'), inline=True)
        emb.add_field(name=f"🧾 Cargos ({len(rls)})", value=rls_str, inline=False)
        emb.add_field(name="🎖️ Badges", value=", ".join(flags) if flags else "Nenhuma", inline=True)
        emb.add_field(name="🔰 Status", value=status, inline=True)
        emb.add_field(name="🎮 Atividade", value=act, inline=True)
        top_role = u.top_role.name if getattr(u, 'top_role', None) else 'Nenhum'
        cor_hex = f"#{(u.color.value):06X}" if getattr(u, 'color', None) else '#2B2D31'
        emb.add_field(name="🎨 Cor / Top Role", value=f"{top_role} • {cor_hex}", inline=False)

        try:
            emb.set_footer(text=f"Solicitado por {ctx_inter.user}", icon_url=ctx_inter.user.display_avatar.url)
        except Exception:
            emb.set_footer(text=f"Solicitado por {ctx_inter.user}")

        return emb

    @discord.ui.button(emoji="🔄", style=discord.ButtonStyle.secondary)
    async def bt_refresh(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        emb = await self._build_embed(interaction)
        try:
            await interaction.message.edit(embed=emb, view=self)
        except Exception:
            await interaction.followup.send("Não foi possível atualizar a mensagem.", ephemeral=True)

    @discord.ui.button(emoji="🗑️", style=discord.ButtonStyle.danger)
    async def bt_clear(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.message.delete()
        except Exception:
            try:
                await interaction.response.send_message("Não foi possível deletar a mensagem.", ephemeral=True)
            except Exception:
                pass

    async def on_timeout(self):
        for it in self.children:
            try:
                it.disabled = True
            except Exception:
                pass
        if self.msg:
            try:
                await self.msg.edit(view=self)
            except Exception:
                pass

class CmdBase(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Teste de latencia")
    @app_commands.guilds(discord.Object(id=SID))
    async def cmd_ping(self, inter: discord.Interaction):
        if "ping" not in LISTA_CMD:
            await inter.response.send_message("Comando desativado.", ephemeral=True)
            return
        ms = round(self.bot.latency * 1000)
        await inter.response.send_message(f"Pong! `{ms}ms`", ephemeral=True)

    @app_commands.command(name="perfil", description="Veja o perfil completo de qualquer usuario.")
    @app_commands.guilds(discord.Object(id=SID))
    async def ver_perfil(self, inter: discord.Interaction, usuario: discord.Member = None):
        if "perfil" not in LISTA_CMD:
            await inter.response.send_message("Comando desativado.", ephemeral=True)
            return
        usuario = usuario or inter.user
        view = ProfileView(usuario)
        embed = await view._build_embed(inter)
        await inter.response.send_message(embed=embed, view=view)
        try:
            msg = await inter.original_response()
        except Exception:
            msg = None
        view.msg = msg

async def setup(bot):
    await bot.add_cog(CmdBase(bot))
    print(f"{Fore.GREEN}[CMD] Cog carregada.{Style.RESET_ALL}")
