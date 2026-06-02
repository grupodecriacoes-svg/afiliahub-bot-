"""
AfiliaHub — Conteúdo da Biblioteca de Prompts
Textos fixados nos canais + comando /prompt para buscar prompts por categoria.
Cole este arquivo na pasta bot/ e importe no bot.py
"""

# ─── TUTORIAL FIXADO NO CANAL #como-usar-prompts ────────────────────────────

TUTORIAL_COMO_USAR = """🎨 **BIBLIOTECA DE PROMPTS — +633 PROMPTS GRATUITOS!**

**📱 COMO USAR:**
1️⃣ Escolha um prompt nos canais abaixo
2️⃣ Copie o texto completo
3️⃣ Cole em uma IA gratuita e gere sua imagem
4️⃣ Compartilhe em #🖼️│resultados-da-comunidade

**🤖 IAS GRATUITAS:**
🟢 Google Gemini → gemini.google.com (recomendado!)
🟡 ChatGPT → chatgpt.com → "Gerar imagem"
🔵 Microsoft Copilot → copilot.microsoft.com
🟣 Leonardo.ai → leonardo.ai

**📂 CATEGORIAS:**
🚗 Carros & Motos (106) • 💪 Academia (40) • 🌊 Natureza (41)
💎 Luxo (24) • ✈️ Dubai (8) • 🎉 Festas (19) • 🌟 Variados (386)

**💡 DICAS:**
✅ Cole o prompt completo — não corte nada
✅ Adicione "no Brasil" no Gemini para localizar
✅ Use `/prompt [categoria]` para buscar por tema
✅ Membros Pro pedem prompts personalizados em #🤖│pedir-prompt-personalizado

👉 `/meu-plano` para ver como fazer upgrade 🚀"""

# ─── BANCO DE PROMPTS POR CATEGORIA (EXEMPLOS DO ACERVO) ────────────────────

PROMPTS_EXEMPLOS = {
    "carros": [
        {
            "nome": "BMW Interior Luxo",
            "prompt": "Ultra-realistic 8K photograph of the interior of a luxury BMW sedan, cream leather seats, panoramic sunroof open, ambient lighting in blue tones, dashboard with digital displays, shot from the driver's seat angle, shallow depth of field, professional automotive photography, no AI artifacts, photorealistic",
            "ia": "Gemini ou ChatGPT",
        },
        {
            "nome": "Moto GS no Posto",
            "prompt": "Ultra-realistic 8K photo, BMW GS 1200 motorcycle parked at a gas station at night, neon lights reflecting on the chrome parts, dramatic lighting, street photography style, Brazil urban setting, photorealistic, no AI look",
            "ia": "Gemini ou Leonardo.ai",
        },
        {
            "nome": "Hilux na Estrada",
            "prompt": "Ultra-realistic 8K photograph, Toyota Hilux pickup truck on a dirt road in rural Brazil, golden hour lighting, dust rising behind the truck, dramatic sky with clouds, cinematic shot, professional photography, no AI artifacts",
            "ia": "Gemini",
        },
    ],
    "academia": [
        {
            "nome": "Boxe Treino",
            "prompt": "Ultra-realistic 8K photograph of a male boxer training in a professional gym, hitting a heavy bag, dramatic side lighting, sweat drops visible, intense expression, black background, sports photography, no AI artifacts, photorealistic",
            "ia": "ChatGPT ou Gemini",
        },
        {
            "nome": "Atleta Corrida Noite",
            "prompt": "Ultra-realistic 8K photo of an athlete running at night in a city, motion blur on legs, city lights bokeh in background, sports wear, determined expression, cinematic lighting, street photography, no AI look",
            "ia": "Gemini",
        },
    ],
    "luxo": [
        {
            "nome": "Beira da Piscina",
            "prompt": "Ultra-realistic 8K photograph, man relaxing at the edge of an infinity pool overlooking Rio de Janeiro at sunset, luxury lifestyle, champagne glass on the side, warm golden lighting, editorial photography style, no AI artifacts",
            "ia": "Gemini ou Leonardo.ai",
        },
        {
            "nome": "Boate VIP",
            "prompt": "Ultra-realistic 8K photo inside an exclusive nightclub VIP area, bottle service, sparklers on bottles, purple and blue ambient lighting, crowd in background blurred, luxury lifestyle photography, no AI look",
            "ia": "ChatGPT",
        },
    ],
    "dubai": [
        {
            "nome": "Dubai Skyline",
            "prompt": "Ultra-realistic 8K photograph of Dubai skyline at night from a rooftop, Burj Khalifa in background, luxury lifestyle, man in stylish outfit looking at the view, city lights reflection, cinematic photography, no AI artifacts",
            "ia": "Gemini",
        },
    ],
    "natureza": [
        {
            "nome": "Praia Paradisíaca",
            "prompt": "Ultra-realistic 8K photograph of a pristine Brazilian beach, crystal clear turquoise water, white sand, coconut palms, golden hour lighting, aerial perspective, travel photography, no AI artifacts, photorealistic",
            "ia": "Gemini ou Copilot",
        },
        {
            "nome": "Cachoeira na Floresta",
            "prompt": "Ultra-realistic 8K photo of a waterfall deep in the Amazon rainforest, lush green vegetation, mist rising from the water, magical lighting through the canopy, nature photography, long exposure effect, no AI look",
            "ia": "Leonardo.ai",
        },
    ],
    "festas": [
        {
            "nome": "Ano Novo Fogos",
            "prompt": "Ultra-realistic 8K photograph of New Year's Eve celebration in Rio de Janeiro, fireworks over Copacabana beach, crowd celebrating, colorful lights reflected on the water, aerial view, festive atmosphere, photorealistic, no AI artifacts",
            "ia": "Gemini",
        },
    ],
    "fe": [
        {
            "nome": "Agradecendo a Deus",
            "prompt": "Ultra-realistic 8K photograph of a person kneeling in prayer in a beautiful church, rays of light coming through stained glass windows, peaceful and spiritual atmosphere, emotional photography, no AI artifacts, photorealistic",
            "ia": "Gemini ou ChatGPT",
        },
    ],
}

CATEGORIAS_INFO = {
    "carros": ("🚗", "Carros & Motos", 106),
    "academia": ("💪", "Academia & Esporte", 40),
    "natureza": ("🌊", "Natureza & Paisagem", 41),
    "luxo": ("💎", "Lifestyle & Luxo", 24),
    "dubai": ("✈️", "Dubai & Viagem", 8),
    "festas": ("🎉", "Festas & Datas", 19),
    "fe": ("🙏", "Fé & Espiritualidade", 4),
    "variados": ("🌟", "Variados", 386),
}
