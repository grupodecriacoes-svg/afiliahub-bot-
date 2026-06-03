"""
AfiliaHub Discord Bot
Comandos: /radar, /copy, /nicho, /meu-plano, /prompt
Post diário automático às 9h BRT (12h UTC)
"""

import os
import asyncio
import aiohttp
import json
import logging
import random
from datetime import datetime, time
import pytz

import discord
from discord import app_commands
from discord.ext import commands, tasks
from anthropic import Anthropic
from biblioteca_prompts import (
    TUTORIAL_COMO_USAR,
    PROMPTS_EXEMPLOS,
    PROMPTS_BANCO,
    CATEGORIAS_INFO,
)

# ─── Configuração de logging ───────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("bot.log", encoding="utf-8"),
    ],
)
log = logging.getLogger("AfiliaHub")

# ─── Constantes ────────────────────────────────────────────────────────────
BRT = pytz.timezone("America/Sao_Paulo")
DAILY_POST_TIME = time(hour=9, minute=0, tzinfo=BRT)

PLANOS = {
    "gratuito": {
        "nome": "🆓 Gratuito",
        "cor": 0x95A5A6,
        "limite_comandos": 3,
        "descricao": "Acesso básico à plataforma",
    },
    "trial": {
        "nome": "⚡ Trial 7 dias",
        "cor": 0xE67E22,
        "limite_comandos": 10,
        "descricao": "Experimente a plataforma por 7 dias",
    },
    "pro_mensal": {
        "nome": "🚀 Pro Mensal",
        "cor": 0x3498DB,
        "limite_comandos": 999,
        "descricao": "Acesso completo + suporte prioritário",
    },
    "pro_anual": {
        "nome": "👑 Pro Anual",
        "cor": 0xF39C12,
        "limite_comandos": 999,
        "descricao": "Melhor custo-benefício — economize 58%",
    },
}

# Mapeamento cargo Discord → plano
CARGO_PLANO = {
    "👑 Pro Anual": "pro_anual",
    "🚀 Pro Mensal": "pro_mensal",
    "⚡ Trial": "trial",
    "👤 Membro": "gratuito",
}

# Próximos planos e preços
PROXIMOS_PLANOS = {
    "gratuito": ("trial", "R$ 19,90", "7 dias de acesso"),
    "trial": ("pro_mensal", "R$ 69,90/mês", "acesso completo"),
    "pro_mensal": ("pro_anual", "R$ 350,00/ano", "economize R$ 488,80"),
    "pro_anual": None,
}

BENEFICIOS_PLANOS = {
    "gratuito": [
        "✅ Biblioteca de +633 prompts gratuitos",
        "✅ Conteúdo diário às 9h",
        "✅ Canal de dúvidas",
        "✅ Comunidade e networking",
        "❌ Comandos IA (/copy, /radar, /nicho)",
        "❌ Canais exclusivos Pro",
    ],
    "trial": [
        "✅ Tudo do Gratuito",
        "✅ Comandos IA limitados (10/dia)",
        "✅ Canais Starter desbloqueados",
        "✅ 7 dias para conhecer a plataforma",
        "❌ Canais VIP Pro",
        "❌ Suporte prioritário",
    ],
    "pro_mensal": [
        "✅ Todos os comandos IA ilimitados",
        "✅ /radar • /copy • /nicho • /prompt",
        "✅ Canais VIP Pro desbloqueados",
        "✅ Suporte prioritário",
        "✅ Aulas e treinamentos",
        "✅ Sala de estratégia exclusiva",
    ],
    "pro_anual": [
        "✅ Tudo do Pro Mensal",
        "✅ Badge exclusivo 👑 Pro Anual",
        "✅ Canal exclusivo anualistas",
        "✅ Acesso antecipado a novidades",
        "✅ Economia de R$ 488,80/ano",
        "✅ Melhor custo-benefício da plataforma",
    ],
}


# ─── Helpers de IA ─────────────────────────────────────────────────────────
def get_claude_client() -> Anthropic:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY não configurada!")
    return Anthropic(api_key=api_key)


async def ask_claude(prompt: str, system: str = "", max_tokens: int = 1000) -> str:
    """Chama a API da Claude de forma assíncrona via thread pool."""
    loop = asyncio.get_event_loop()

    def _call():
        client = get_claude_client()
        kwargs = {
            "model": "claude-opus-4-5",
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system:
            kwargs["system"] = system
        msg = client.messages.create(**kwargs)
        return msg.content[0].text

    return await loop.run_in_executor(None, _call)


# ─── Bot setup ─────────────────────────────────────────────────────────────
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


def get_plano_usuario(member: discord.Member) -> str:
    """Detecta o plano do usuário pelos cargos do Discord."""
    role_names = [r.name for r in member.roles]
    for cargo, plano in CARGO_PLANO.items():
        if cargo in role_names:
            return plano
    return "gratuito"


def embed_erro_plano(plano_atual: str, plano_necessario: str) -> discord.Embed:
    embed = discord.Embed(
        title="🔒 Recurso Bloqueado",
        description=(
            f"Este comando requer o plano **{PLANOS[plano_necessario]['nome']}** ou superior.\n\n"
            f"Seu plano atual: **{PLANOS[plano_atual]['nome']}**\n\n"
            "👉 [Fazer upgrade agora](https://afiliahub.com.br/planos)"
        ),
        color=0xE74C3C,
    )
    embed.set_footer(text="AfiliaHub • Plataforma de Afiliados")
    return embed


# ─── Comando /radar ─────────────────────────────────────────────────────────
@bot.tree.command(
    name="radar",
    description="🎯 Descubra produtos em alta para promover agora mesmo",
)
@app_commands.describe(
    nicho="Nicho de mercado (ex: emagrecimento, finanças, relacionamento)",
    plataforma="Plataforma de afiliados (padrão: Hotmart)",
)
async def radar(
    interaction: discord.Interaction,
    nicho: str,
    plataforma: str = "Hotmart",
):
    await interaction.response.defer(thinking=True)

    plano = get_plano_usuario(interaction.user)

    system = (
        "Você é um especialista em marketing de afiliados no Brasil. "
        "Analise tendências de mercado e indique produtos com alto potencial de conversão. "
        "Seja direto, prático e use dados reais do mercado brasileiro. "
        "Sempre inclua: comissão estimada, temperatura do nicho, e dica de ângulo de venda."
    )

    prompt = (
        f"Faça uma análise de RADAR DE PRODUTOS para o nicho '{nicho}' na plataforma {plataforma}.\n\n"
        "Inclua:\n"
        "1. 🔥 Top 3 produtos em alta agora (com estimativa de comissão)\n"
        "2. 📈 Tendência do nicho (subindo/estável/caindo) com justificativa\n"
        "3. 🎯 Melhor ângulo de venda para iniciantes\n"
        "4. ⚠️ Principais concorrências e como se diferenciar\n"
        "5. 💡 Dica de ouro para converter mais\n\n"
        "Formato: use emojis, seja conciso e acionável. Máximo 400 palavras."
    )

    try:
        resposta = await ask_claude(prompt, system=system, max_tokens=800)

        embed = discord.Embed(
            title=f"🎯 Radar de Produtos — {nicho.title()}",
            description=resposta,
            color=0x2ECC71,
            timestamp=datetime.now(BRT),
        )
        embed.add_field(name="📦 Plataforma", value=plataforma, inline=True)
        embed.add_field(name="👤 Solicitado por", value=interaction.user.mention, inline=True)
        embed.set_footer(
            text="AfiliaHub Radar • Dados baseados em tendências de mercado",
            icon_url="https://i.imgur.com/YOUR_LOGO.png",
        )
        await interaction.followup.send(embed=embed)
        log.info(f"/radar | {interaction.user} | nicho={nicho}")

    except Exception as e:
        log.error(f"/radar erro: {e}")
        await interaction.followup.send(
            "❌ Erro ao consultar o Radar. Tente novamente em instantes.", ephemeral=True
        )


# ─── Comando /copy ──────────────────────────────────────────────────────────
@bot.tree.command(
    name="copy",
    description="✍️ Gere copies prontas para vender como afiliado",
)
@app_commands.describe(
    produto="Nome ou descrição do produto",
    formato="Formato da copy (story, post, email, whatsapp, anuncio)",
    publico="Público-alvo (ex: mulheres 30-45 anos, homens que querem emagrecer)",
)
@app_commands.choices(
    formato=[
        app_commands.Choice(name="📱 Story Instagram", value="story"),
        app_commands.Choice(name="📝 Post Feed", value="post"),
        app_commands.Choice(name="📧 E-mail", value="email"),
        app_commands.Choice(name="💬 WhatsApp", value="whatsapp"),
        app_commands.Choice(name="📢 Anúncio Pago", value="anuncio"),
    ]
)
async def copy(
    interaction: discord.Interaction,
    produto: str,
    formato: str,
    publico: str = "público geral",
):
    await interaction.response.defer(thinking=True)

    plano = get_plano_usuario(interaction.user)
    if plano == "gratuito":
        await interaction.followup.send(embed=embed_erro_plano("gratuito", "starter"), ephemeral=True)
        return

    formatos_map = {
        "story": "Story do Instagram (15 segundos de leitura, CTA no final)",
        "post": "Post do feed Instagram (caption engajante, até 200 palavras)",
        "email": "E-mail marketing (assunto + corpo + CTA, tom pessoal)",
        "whatsapp": "Mensagem de WhatsApp (informal, com senso de urgência)",
        "anuncio": "Anúncio pago (headline + descrição + CTA, foco em conversão)",
    }

    system = (
        "Você é um copywriter especialista em marketing de afiliados no Brasil. "
        "Crie copies que convertem de verdade, usando gatilhos mentais, prova social e urgência. "
        "Linguagem: natural, brasileira, sem ser vulgar. "
        "Nunca use frases genéricas como 'produto incrível' sem especificidade."
    )

    prompt = (
        f"Crie uma copy no formato: {formatos_map.get(formato, formato)}\n\n"
        f"Produto: {produto}\n"
        f"Público-alvo: {publico}\n\n"
        "Requisitos:\n"
        "• Use pelo menos 2 gatilhos mentais (urgência, escassez, autoridade, prova social)\n"
        "• CTA claro e direto\n"
        "• Linguagem natural e brasileira\n"
        "• Se for story/post, inclua sugestão de imagem/vídeo\n"
        "• Se for email, inclua linha de assunto\n\n"
        "Entregue a copy pronta para usar, sem explicações adicionais."
    )

    try:
        resposta = await ask_claude(prompt, system=system, max_tokens=700)

        nomes_formato = {
            "story": "📱 Story Instagram",
            "post": "📝 Post Feed",
            "email": "📧 E-mail",
            "whatsapp": "💬 WhatsApp",
            "anuncio": "📢 Anúncio Pago",
        }

        embed = discord.Embed(
            title=f"✍️ Copy Gerada — {nomes_formato.get(formato, formato)}",
            description=f"```\n{resposta[:3900]}\n```",
            color=0x9B59B6,
            timestamp=datetime.now(BRT),
        )
        embed.add_field(name="🛍️ Produto", value=produto[:50], inline=True)
        embed.add_field(name="👥 Público", value=publico[:50], inline=True)
        embed.set_footer(text="AfiliaHub Copy Generator • Clique em 📋 para copiar o texto")

        await interaction.followup.send(embed=embed)
        log.info(f"/copy | {interaction.user} | produto={produto} | formato={formato}")

    except Exception as e:
        log.error(f"/copy erro: {e}")
        await interaction.followup.send("❌ Erro ao gerar copy. Tente novamente.", ephemeral=True)


# ─── Comando /nicho ──────────────────────────────────────────────────────────
@bot.tree.command(
    name="nicho",
    description="🔍 Analise um nicho de mercado em profundidade",
)
@app_commands.describe(
    nicho="Nicho para analisar (ex: emagrecimento, finanças pessoais, ansiedade)",
)
async def nicho_cmd(
    interaction: discord.Interaction,
    nicho: str,
):
    await interaction.response.defer(thinking=True)

    plano = get_plano_usuario(interaction.user)

    system = (
        "Você é um estrategista de marketing digital especializado no mercado brasileiro de afiliados. "
        "Forneça análises profundas e acionáveis sobre nichos de mercado. "
        "Use dados reais, tendências do Google Trends, e benchmarks do mercado BR."
    )

    # Acesso completo apenas para Starter+
    if plano == "gratuito":
        prompt = (
            f"Faça uma análise BÁSICA do nicho '{nicho}' para afiliados iniciantes.\n"
            "Inclua apenas: 1) Potencial do nicho (1-10) 2) Perfil do comprador 3) Uma dica de entrada.\n"
            "Máximo 150 palavras. Mencione que a análise completa está disponível no plano Starter."
        )
    else:
        prompt = (
            f"Faça uma análise COMPLETA E PROFUNDA do nicho '{nicho}' para afiliados.\n\n"
            "Estruture assim:\n"
            "📊 **SCORE DO NICHO**: X/10 (com justificativa)\n"
            "👥 **AVATAR DETALHADO**: Quem compra, dores, desejos, objeções\n"
            "💰 **POTENCIAL FINANCEIRO**: Ticket médio, comissões esperadas, volume\n"
            "🏆 **CONCORRÊNCIA**: Nível, principais players, gaps de mercado\n"
            "📱 **MELHORES CANAIS**: Onde e como promover (Instagram, YouTube, etc.)\n"
            "🎯 **ESTRATÉGIA DE ENTRADA**: Passo a passo para um iniciante\n"
            "⚡ **PALAVRAS-CHAVE HOT**: 5 termos de busca com alto potencial\n"
            "⚠️ **RISCOS E ALERTAS**: O que evitar neste nicho\n\n"
            "Seja específico, use exemplos reais e seja direto. Máximo 500 palavras."
        )

    try:
        resposta = await ask_claude(prompt, system=system, max_tokens=900)

        cor = 0xE67E22 if plano == "gratuito" else 0xF39C12
        titulo = f"🔍 Análise de Nicho — {nicho.title()}"
        if plano == "gratuito":
            titulo += " (Versão Básica)"

        embed = discord.Embed(
            title=titulo,
            description=resposta,
            color=cor,
            timestamp=datetime.now(BRT),
        )
        embed.set_footer(text=f"AfiliaHub Nicho Analyzer • Plano {PLANOS[plano]['nome']}")
        await interaction.followup.send(embed=embed)
        log.info(f"/nicho | {interaction.user} | nicho={nicho} | plano={plano}")

    except Exception as e:
        log.error(f"/nicho erro: {e}")
        await interaction.followup.send("❌ Erro na análise. Tente novamente.", ephemeral=True)


# ─── Comando /meu-plano ──────────────────────────────────────────────────────
@bot.tree.command(
    name="meu-plano",
    description="📋 Veja seu plano atual, benefícios e como fazer upgrade",
)
async def meu_plano(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True, ephemeral=True)

    plano_key = get_plano_usuario(interaction.user)
    plano = PLANOS[plano_key]

    embed = discord.Embed(
        title=f"📋 Seu Plano: {plano['nome']}",
        description=plano["descricao"],
        color=plano["cor"],
        timestamp=datetime.now(BRT),
    )

    embed.add_field(
        name="🎁 Seus Benefícios",
        value="\n".join(BENEFICIOS_PLANOS.get(plano_key, [])),
        inline=False,
    )

    proximo = PROXIMOS_PLANOS.get(plano_key)
    if proximo:
        proximo_key, preco, descricao = proximo
        proximo_plano = PLANOS[proximo_key]
        embed.add_field(
            name=f"⬆️ Próximo Nível: {proximo_plano['nome']}",
            value=(
                f"Por apenas **{preco}** — {descricao}\n"
                f"👉 [Fazer upgrade agora](https://afiliahub.com.br/planos)"
            ),
            inline=False,
        )
    else:
        embed.add_field(
            name="👑 Você está no topo!",
            value="Aproveite todos os recursos exclusivos do Pro Anual! 🔥",
            inline=False,
        )

    member = interaction.guild.get_member(interaction.user.id)
    dias_servidor = (datetime.now(BRT) - member.joined_at.astimezone(BRT)).days if member.joined_at else 0
    embed.add_field(name="📅 Dias na comunidade", value=str(dias_servidor), inline=True)
    embed.add_field(name="🏅 Cargos", value=", ".join(r.name for r in member.roles[1:]) or "Nenhum", inline=True)

    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    embed.set_footer(text="AfiliaHub • Plataforma de Afiliados")

    await interaction.followup.send(embed=embed, ephemeral=True)
    log.info(f"/meu-plano | {interaction.user} | plano={plano_key}")


# ─── Comando /prompt ────────────────────────────────────────────────────────
@bot.tree.command(
    name="prompt",
    description="🎨 Lista todos os prompts de uma categoria",
)
@app_commands.describe(categoria="Categoria de prompts para listar")
@app_commands.choices(
    categoria=[
        app_commands.Choice(name="🚗 Carros & Motos (106)", value="carros"),
        app_commands.Choice(name="💪 Academia & Esporte (40)", value="academia"),
        app_commands.Choice(name="🌊 Natureza & Paisagem (41)", value="natureza"),
        app_commands.Choice(name="💎 Lifestyle & Luxo (24)", value="luxo"),
        app_commands.Choice(name="✈️ Dubai & Viagem (8)", value="dubai"),
        app_commands.Choice(name="🎉 Festas & Datas (19)", value="festas"),
        app_commands.Choice(name="🙏 Fé & Espiritualidade (4)", value="fe"),
        app_commands.Choice(name="🌟 Variados (386)", value="variados"),
    ]
)
async def prompt_cmd(interaction: discord.Interaction, categoria: str):
    await interaction.response.defer(thinking=True)

    info = CATEGORIAS_INFO.get(categoria)
    if not info:
        await interaction.followup.send("❌ Categoria não encontrada.", ephemeral=True)
        return

    emoji, nome_cat, total = info
    prompts = PROMPTS_BANCO.get(categoria, [])

    # Monta lista numerada com todos os prompts do banco
    if prompts:
        lista = "\n".join([f"`{i+1}.` {p['nome']}" for i, p in enumerate(prompts)])
        rodape_lista = f"\n\n_Mostrando {len(prompts)} de {total} prompts disponíveis_"
    else:
        lista = "_Em breve mais prompts desta categoria!_"
        rodape_lista = ""

    embed = discord.Embed(
        title=f"{emoji} {nome_cat} — Lista de Prompts",
        description=(
            f"**{total} prompts** nesta categoria!\n\n"
            f"{lista}{rodape_lista}"
        ),
        color=0x9B59B6,
        timestamp=datetime.now(BRT),
    )
    embed.add_field(
        name="📥 Como ver o prompt completo",
        value=f"Use `/prompt-ver {categoria} [número]`\nEx: `/prompt-ver {categoria} 1`",
        inline=False,
    )
    embed.set_footer(text="AfiliaHub Biblioteca • +633 prompts disponíveis")

    await interaction.followup.send(embed=embed)
    log.info(f"/prompt | {interaction.user} | categoria={categoria}")


# ─── Comando /prompt-ver ─────────────────────────────────────────────────────
@bot.tree.command(
    name="prompt-ver",
    description="📋 Veja o texto completo de um prompt pelo número",
)
@app_commands.describe(
    categoria="Categoria do prompt",
    numero="Número do prompt (use /prompt para ver a lista)",
)
@app_commands.choices(
    categoria=[
        app_commands.Choice(name="🚗 Carros & Motos", value="carros"),
        app_commands.Choice(name="💪 Academia & Esporte", value="academia"),
        app_commands.Choice(name="🌊 Natureza & Paisagem", value="natureza"),
        app_commands.Choice(name="💎 Lifestyle & Luxo", value="luxo"),
        app_commands.Choice(name="✈️ Dubai & Viagem", value="dubai"),
        app_commands.Choice(name="🎉 Festas & Datas", value="festas"),
        app_commands.Choice(name="🙏 Fé & Espiritualidade", value="fe"),
        app_commands.Choice(name="🌟 Variados", value="variados"),
    ]
)
async def prompt_ver(interaction: discord.Interaction, categoria: str, numero: int):
    await interaction.response.defer(thinking=True)

    prompts = PROMPTS_BANCO.get(categoria, [])
    info = CATEGORIAS_INFO.get(categoria)

    if not prompts or not info:
        await interaction.followup.send("❌ Categoria não encontrada.", ephemeral=True)
        return

    if numero < 1 or numero > len(prompts):
        await interaction.followup.send(
            f"❌ Número inválido! Use entre 1 e {len(prompts)}. Use `/prompt {categoria}` para ver a lista.",
            ephemeral=True,
        )
        return

    emoji, nome_cat, _ = info
    p = prompts[numero - 1]

    embed = discord.Embed(
        title=f"{emoji} {p['nome']}",
        description=f"```\n{p['prompt']}\n```",
        color=0x2ECC71,
        timestamp=datetime.now(BRT),
    )
    embed.add_field(name="🤖 IA recomendada", value=p["ia"], inline=True)
    embed.add_field(name="📂 Categoria", value=nome_cat, inline=True)
    embed.add_field(
        name="💡 Como usar",
        value="Copie o texto acima → cole no Gemini, ChatGPT ou Leonardo.ai → gere!",
        inline=False,
    )
    embed.set_footer(text=f"AfiliaHub • Prompt {numero}/{len(prompts)} de {nome_cat}")

    await interaction.followup.send(embed=embed)
    log.info(f"/prompt-ver | {interaction.user} | {categoria} #{numero}")


async def postar_tutorial_biblioteca():
    """Posta o tutorial no canal #como-usar-prompts (execute uma vez manualmente)."""
    canal_id = int(os.environ.get("CANAL_TUTORIAL_ID", "0"))
    if not canal_id:
        log.warning("CANAL_TUTORIAL_ID não configurado — tutorial não postado.")
        return

    canal = bot.get_channel(canal_id)
    if not canal:
        return

    # Verifica se já existe mensagem fixada
    pins = await canal.pins()
    if pins:
        log.info("Tutorial já postado e fixado.")
        return

    msg = await canal.send(TUTORIAL_COMO_USAR)
    await msg.pin()
    log.info("✅ Tutorial postado e fixado em #como-usar-prompts")


# ─── Comando /postar ─────────────────────────────────────────────────────────
@bot.tree.command(
    name="postar",
    description="📢 [ADMIN] Posta uma mensagem como AfiliaHub em qualquer canal",
)
@app_commands.describe(
    canal="Canal onde a mensagem será postada",
    mensagem="Texto da mensagem (use \\n para quebrar linha)",
    titulo="Título do embed (opcional)",
    fixar="Fixar a mensagem no canal?",
)
@app_commands.choices(
    fixar=[
        app_commands.Choice(name="Sim — fixar a mensagem", value="sim"),
        app_commands.Choice(name="Não", value="nao"),
    ]
)
async def postar(
    interaction: discord.Interaction,
    canal: discord.TextChannel,
    mensagem: str,
    titulo: str = "",
    fixar: str = "nao",
):
    # Apenas admins e moderadores podem usar
    cargos_permitidos = ["⚙️ Admin", "🛡️ Moderador"]
    nomes_cargos = [r.name for r in interaction.user.roles]
    if not any(c in nomes_cargos for c in cargos_permitidos):
        await interaction.response.send_message(
            "❌ Apenas **Admins** e **Moderadores** podem usar este comando.",
            ephemeral=True,
        )
        return

    await interaction.response.defer(ephemeral=True)

    # Substitui \n por quebra de linha real
    mensagem_formatada = mensagem.replace("\\n", "\n")

    try:
        if titulo:
            embed = discord.Embed(
                title=titulo,
                description=mensagem_formatada,
                color=0xF39C12,
                timestamp=datetime.now(BRT),
            )
            embed.set_footer(text="AfiliaHub")
            msg = await canal.send(embed=embed)
        else:
            msg = await canal.send(mensagem_formatada)

        if fixar == "sim":
            await msg.pin()
            await interaction.followup.send(
                f"✅ Mensagem postada e fixada em {canal.mention}!", ephemeral=True
            )
        else:
            await interaction.followup.send(
                f"✅ Mensagem postada em {canal.mention}!", ephemeral=True
            )

        log.info(f"/postar | {interaction.user} | canal={canal.name} | fixar={fixar}")

    except discord.Forbidden:
        await interaction.followup.send(
            f"❌ Sem permissão para postar em {canal.mention}.", ephemeral=True
        )
    except Exception as e:
        log.error(f"/postar erro: {e}")
        await interaction.followup.send("❌ Erro ao postar. Tente novamente.", ephemeral=True)


# ─── Comando /postar-embed ────────────────────────────────────────────────────
@bot.tree.command(
    name="anuncio",
    description="📣 [ADMIN] Posta um anúncio oficial estilizado como AfiliaHub",
)
@app_commands.describe(
    canal="Canal do anúncio",
    titulo="Título do anúncio",
    mensagem="Corpo do anúncio (use \\n para quebrar linha)",
    cor="Cor do embed (laranja, azul, verde, roxo, vermelho)",
    mencionar="Mencionar @everyone?",
)
@app_commands.choices(
    cor=[
        app_commands.Choice(name="🟠 Laranja (padrão)", value="laranja"),
        app_commands.Choice(name="🔵 Azul", value="azul"),
        app_commands.Choice(name="🟢 Verde", value="verde"),
        app_commands.Choice(name="🟣 Roxo", value="roxo"),
        app_commands.Choice(name="🔴 Vermelho", value="vermelho"),
        app_commands.Choice(name="⭐ Dourado", value="dourado"),
    ],
    mencionar=[
        app_commands.Choice(name="Sim — @everyone", value="sim"),
        app_commands.Choice(name="Não", value="nao"),
    ]
)
async def anuncio(
    interaction: discord.Interaction,
    canal: discord.TextChannel,
    titulo: str,
    mensagem: str,
    cor: str = "laranja",
    mencionar: str = "nao",
):
    cargos_permitidos = ["⚙️ Admin", "🛡️ Moderador"]
    nomes_cargos = [r.name for r in interaction.user.roles]
    if not any(c in nomes_cargos for c in cargos_permitidos):
        await interaction.response.send_message(
            "❌ Apenas **Admins** e **Moderadores** podem usar este comando.",
            ephemeral=True,
        )
        return

    await interaction.response.defer(ephemeral=True)

    cores_map = {
        "laranja": 0xF39C12,
        "azul": 0x3498DB,
        "verde": 0x2ECC71,
        "roxo": 0x9B59B6,
        "vermelho": 0xE74C3C,
        "dourado": 0xF1C40F,
    }

    mensagem_formatada = mensagem.replace("\\n", "\n")

    embed = discord.Embed(
        title=f"📣 {titulo}",
        description=mensagem_formatada,
        color=cores_map.get(cor, 0xF39C12),
        timestamp=datetime.now(BRT),
    )
    embed.set_author(
        name="AfiliaHub — Comunicado Oficial",
        icon_url=interaction.guild.icon.url if interaction.guild.icon else None,
    )
    embed.set_footer(text="AfiliaHub • Plataforma de Afiliados")

    conteudo = "@everyone" if mencionar == "sim" else ""

    try:
        msg = await canal.send(content=conteudo, embed=embed)
        await msg.pin()
        await interaction.followup.send(
            f"✅ Anúncio postado e fixado em {canal.mention}!", ephemeral=True
        )
        log.info(f"/anuncio | {interaction.user} | canal={canal.name} | titulo={titulo}")
    except Exception as e:
        log.error(f"/anuncio erro: {e}")
        await interaction.followup.send("❌ Erro ao postar anúncio.", ephemeral=True)


# ─── Post Diário às 9h ───────────────────────────────────────────────────────
@tasks.loop(time=DAILY_POST_TIME)
async def post_diario():
    """Envia post motivacional/educativo diariamente às 9h BRT."""
    canal_id = int(os.environ.get("CANAL_DIARIO_ID", "0"))
    if not canal_id:
        log.warning("CANAL_DIARIO_ID não configurado — post diário ignorado.")
        return

    canal = bot.get_channel(canal_id)
    if not canal:
        log.error(f"Canal {canal_id} não encontrado.")
        return

    hoje = datetime.now(BRT)
    dia_semana = hoje.weekday()  # 0=seg ... 6=dom

    temas = {
        0: ("💡 Dica de Segunda", "tráfego orgânico para afiliados iniciantes"),
        1: ("📊 Terça dos Dados", "métricas essenciais que todo afiliado deve acompanhar"),
        2: ("🛠️ Quarta das Ferramentas", "ferramenta gratuita que aumenta conversões"),
        3: ("🎯 Quinta da Estratégia", "estratégia de posicionamento para se diferenciar"),
        4: ("💰 Sexta do Financeiro", "como organizar as finanças como afiliado"),
        5: ("🚀 Sábado de Cases", "case de sucesso real de um afiliado brasileiro"),
        6: ("🧠 Domingo Mindset", "mentalidade vencedora para afiliados"),
    }

    titulo_dia, tema = temas[dia_semana]
    data_str = hoje.strftime("%d/%m/%Y")

    system = (
        "Você é o assistente oficial da AfiliaHub, plataforma para afiliados iniciantes no Brasil. "
        "Crie conteúdo educativo, motivador e 100% prático. "
        "Tom: amigável, entusiasmado mas profissional. "
        "Inclua sempre uma ação concreta que o membro pode fazer HOJE."
    )

    prompt = (
        f"Crie o post diário da AfiliaHub para {data_str} com o tema: '{tema}'.\n\n"
        "Estrutura obrigatória:\n"
        "1. Abertura impactante (1-2 linhas)\n"
        "2. Conteúdo principal (3-4 parágrafos práticos)\n"
        "3. Exemplo real ou dado concreto\n"
        "4. MISSÃO DO DIA: uma ação específica para fazer hoje\n"
        "5. Frase motivacional de encerramento\n\n"
        "Use emojis estrategicamente. Máximo 350 palavras. "
        "Mencione que podem usar /radar, /copy ou /nicho para aprofundar."
    )

    try:
        conteudo = await ask_claude(prompt, system=system, max_tokens=700)

        embed = discord.Embed(
            title=f"{titulo_dia} — {data_str}",
            description=conteudo,
            color=0x2ECC71,
            timestamp=hoje,
        )
        embed.set_author(name="AfiliaHub Daily", icon_url=canal.guild.icon.url if canal.guild.icon else None)
        embed.set_footer(text="📌 Use /radar • /copy • /nicho para aprofundar • AfiliaHub")

        await canal.send(
            content="@everyone 🌅 **Bom dia, AfiliaHub!** Seu conteúdo diário chegou:",
            embed=embed,
        )
        log.info(f"Post diário enviado | {data_str} | tema={tema}")

    except Exception as e:
        log.error(f"Erro no post diário: {e}")


# ─── Eventos do bot ──────────────────────────────────────────────────────────
@bot.event
async def on_ready():
    log.info(f"✅ Bot online como {bot.user} ({bot.user.id})")

    guild_id = int(os.environ.get("GUILD_ID", "0"))

    try:
        if guild_id:
            # Sync rápido no servidor específico (instantâneo)
            guild = discord.Object(id=guild_id)
            bot.tree.copy_global_to(guild=guild)
            synced = await bot.tree.sync(guild=guild)
            log.info(f"📡 {len(synced)} comandos sincronizados no servidor (instantâneo)")
        else:
            # Sync global (demora até 1 hora)
            synced = await bot.tree.sync()
            log.info(f"📡 {len(synced)} comandos sincronizados globalmente")
    except Exception as e:
        log.error(f"Erro ao sincronizar comandos: {e}")

    post_diario.start()
    log.info("⏰ Post diário agendado para 09:00 BRT")

    # Posta tutorial na biblioteca se ainda não foi feito
    await asyncio.sleep(5)
    await postar_tutorial_biblioteca()


@bot.event
async def on_member_join(member: discord.Member):
    """Boas-vindas para novos membros."""
    canal_id = int(os.environ.get("CANAL_BOAS_VINDAS_ID", "0"))
    if not canal_id:
        return

    canal = bot.get_channel(canal_id)
    if not canal:
        return

    embed = discord.Embed(
        title=f"🎉 Bem-vindo(a), {member.display_name}!",
        description=(
            f"Olá {member.mention}! Você acabou de entrar na **AfiliaHub** — "
            "a comunidade para afiliados que querem resultados reais! 🚀\n\n"
            "**Por onde começar:**\n"
            "📌 Leia as regras em <#CANAL_REGRAS>\n"
            "🎯 Apresente-se em <#CANAL_APRESENTACOES>\n"
            "🤖 Use `/nicho`, `/radar` e `/copy` para começar a explorar\n"
            "📋 Veja seu plano com `/meu-plano`\n\n"
            "Qualquer dúvida, use `/ajuda` ou chame a equipe! 💪"
        ),
        color=0x2ECC71,
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.set_footer(text=f"Membro #{member.guild.member_count} da AfiliaHub")

    await canal.send(embed=embed)

    # Atribui cargo "Membro" automaticamente
    cargo_membro = discord.utils.get(member.guild.roles, name="Membro")
    if cargo_membro:
        await member.add_roles(cargo_membro)
        log.info(f"Cargo Membro atribuído a {member}")


@bot.event
async def on_command_error(ctx, error):
    log.error(f"Erro no comando: {error}")


# ─── Entry point ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    token = os.environ.get("DISCORD_TOKEN")
    if not token:
        raise RuntimeError("DISCORD_TOKEN não configurado!")
    bot.run(token)
