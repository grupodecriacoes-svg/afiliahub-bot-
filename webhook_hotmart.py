"""
AfiliaHub — Webhook Hotmart
Recebe notificações do Hotmart via Make e atualiza cargos no Discord.

Endpoints:
  POST /hotmart/compra    — Atribui cargo baseado no produto comprado
  POST /hotmart/reembolso — Remove cargo ao reembolsar

Use junto com o bot.py (pode ser o mesmo processo ou separado).
Integre com o Make: HTTP → Webhook → POST para este servidor.
"""

import os
import json
import hmac
import hashlib
import logging
from aiohttp import web
from dotenv import load_dotenv
import discord

load_dotenv()
log = logging.getLogger("Webhook")

# Mapeamento Produto Hotmart → Cargo Discord
# Configure os IDs/nomes exatos dos produtos na Hotmart
PRODUTOS_CARGOS = {
    # "nome_produto_hotmart": "Nome do Cargo Discord"
    "AfiliaHub Starter": "⚡ Starter",
    "AfiliaHub Pro": "🚀 Pro",
    "AfiliaHub Elite": "👑 Elite",
    # Adicione mais produtos conforme necessário
}

HOTMART_SECRET = os.environ.get("HOTMART_WEBHOOK_SECRET", "")


def verificar_assinatura(body: bytes, signature: str) -> bool:
    """Verifica a assinatura HMAC do webhook Hotmart."""
    if not HOTMART_SECRET:
        log.warning("HOTMART_WEBHOOK_SECRET não configurado — pulando verificação")
        return True
    expected = hmac.new(
        HOTMART_SECRET.encode(), body, hashlib.sha1
    ).hexdigest()
    return hmac.compare_digest(expected, signature or "")


class HotmartWebhook:
    def __init__(self, bot: discord.Client):
        self.bot = bot
        self.app = web.Application()
        self.app.router.add_post("/hotmart/compra", self.handle_compra)
        self.app.router.add_post("/hotmart/reembolso", self.handle_reembolso)
        self.app.router.add_get("/health", self.health_check)

    async def health_check(self, request: web.Request) -> web.Response:
        return web.json_response({"status": "ok", "bot": str(self.bot.user)})

    async def handle_compra(self, request: web.Request) -> web.Response:
        """
        Payload esperado do Make (após processar o webhook Hotmart):
        {
            "discord_user_id": "123456789",
            "produto": "AfiliaHub Pro",
            "email": "usuario@email.com",
            "transaction": "HP-XXXX"
        }
        """
        body = await request.read()
        sig = request.headers.get("X-Hotmart-Signature", "")

        if not verificar_assinatura(body, sig):
            log.warning("Assinatura inválida no webhook de compra")
            return web.json_response({"error": "Assinatura inválida"}, status=401)

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            return web.json_response({"error": "JSON inválido"}, status=400)

        discord_id = data.get("discord_user_id")
        produto = data.get("produto")
        transaction = data.get("transaction", "N/A")

        if not discord_id or not produto:
            return web.json_response({"error": "discord_user_id e produto são obrigatórios"}, status=400)

        cargo_nome = PRODUTOS_CARGOS.get(produto)
        if not cargo_nome:
            log.warning(f"Produto não mapeado: {produto}")
            return web.json_response({"error": f"Produto '{produto}' não mapeado"}, status=400)

        guild_id = int(os.environ.get("GUILD_ID", "0"))
        guild = self.bot.get_guild(guild_id)
        if not guild:
            return web.json_response({"error": "Servidor não encontrado"}, status=500)

        try:
            member = await guild.fetch_member(int(discord_id))
        except discord.NotFound:
            return web.json_response({"error": f"Membro {discord_id} não encontrado no servidor"}, status=404)

        cargo = discord.utils.get(guild.roles, name=cargo_nome)
        if not cargo:
            return web.json_response({"error": f"Cargo '{cargo_nome}' não encontrado"}, status=500)

        # Remove cargos de plano anteriores antes de adicionar o novo
        cargos_plano = ["👤 Membro", "⚡ Starter", "🚀 Pro", "👑 Elite"]
        for nome_cargo in cargos_plano:
            c = discord.utils.get(guild.roles, name=nome_cargo)
            if c and c in member.roles:
                await member.remove_roles(c, reason=f"Upgrade para {cargo_nome}")

        await member.add_roles(cargo, reason=f"Compra Hotmart: {produto} ({transaction})")

        # Notifica no canal de log
        canal_log_id = int(os.environ.get("CANAL_LOG_MEMBROS_ID", "0"))
        if canal_log_id:
            canal = self.bot.get_channel(canal_log_id)
            if canal:
                embed = discord.Embed(
                    title="🎉 Novo Upgrade de Plano!",
                    color=0x2ECC71,
                )
                embed.add_field(name="Membro", value=member.mention, inline=True)
                embed.add_field(name="Produto", value=produto, inline=True)
                embed.add_field(name="Cargo", value=cargo_nome, inline=True)
                embed.add_field(name="Transação", value=transaction, inline=True)
                await canal.send(embed=embed)

        log.info(f"Cargo {cargo_nome} atribuído a {member} | Produto: {produto} | TX: {transaction}")
        return web.json_response({"success": True, "cargo": cargo_nome, "membro": str(member)})

    async def handle_reembolso(self, request: web.Request) -> web.Response:
        """
        Payload esperado:
        {
            "discord_user_id": "123456789",
            "produto": "AfiliaHub Pro",
            "transaction": "HP-XXXX"
        }
        """
        body = await request.read()

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            return web.json_response({"error": "JSON inválido"}, status=400)

        discord_id = data.get("discord_user_id")
        produto = data.get("produto")
        transaction = data.get("transaction", "N/A")

        cargo_nome = PRODUTOS_CARGOS.get(produto, "")
        guild_id = int(os.environ.get("GUILD_ID", "0"))
        guild = self.bot.get_guild(guild_id)

        if not guild or not discord_id:
            return web.json_response({"error": "Parâmetros inválidos"}, status=400)

        try:
            member = await guild.fetch_member(int(discord_id))
        except discord.NotFound:
            return web.json_response({"error": "Membro não encontrado"}, status=404)

        if cargo_nome:
            cargo = discord.utils.get(guild.roles, name=cargo_nome)
            if cargo and cargo in member.roles:
                await member.remove_roles(cargo, reason=f"Reembolso: {produto} ({transaction})")

        # Atribui cargo Membro básico
        cargo_membro = discord.utils.get(guild.roles, name="👤 Membro")
        if cargo_membro and cargo_membro not in member.roles:
            await member.add_roles(cargo_membro, reason="Reembolso — downgrade para Membro")

        # Log do reembolso
        canal_log_id = int(os.environ.get("CANAL_LOG_MEMBROS_ID", "0"))
        if canal_log_id:
            canal = self.bot.get_channel(canal_log_id)
            if canal:
                embed = discord.Embed(
                    title="⚠️ Reembolso Processado",
                    color=0xE74C3C,
                )
                embed.add_field(name="Membro", value=member.mention, inline=True)
                embed.add_field(name="Produto", value=produto or "N/A", inline=True)
                embed.add_field(name="Transação", value=transaction, inline=True)
                await canal.send(embed=embed)

        log.info(f"Reembolso processado: {member} | Produto: {produto} | TX: {transaction}")
        return web.json_response({"success": True})


async def iniciar_webhook(bot: discord.Client):
    """Inicia o servidor webhook junto com o bot Discord."""
    porta = int(os.environ.get("WEBHOOK_PORT", "8080"))
    handler = HotmartWebhook(bot)
    runner = web.AppRunner(handler.app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", porta)
    await site.start()
    log.info(f"🌐 Webhook Hotmart rodando na porta {porta}")
    return runner
