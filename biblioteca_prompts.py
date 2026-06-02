"""
AfiliaHub — Conteúdo da Biblioteca de Prompts
"""

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
✅ Use `/prompt [categoria]` para listar todos os prompts
✅ Use `/prompt-ver [categoria] [número]` para ver o prompt completo

👉 `/meu-plano` para ver como fazer upgrade 🚀"""

# ─── BANCO COMPLETO DE PROMPTS ───────────────────────────────────────────────

PROMPTS_BANCO = {
    "carros": [
        {"nome": "BMW Interior Luxo", "prompt": "Ultra-realistic 8K photograph of the interior of a luxury BMW sedan, cream leather seats, panoramic sunroof open, ambient lighting in blue tones, dashboard with digital displays, shot from the driver's seat angle, shallow depth of field, professional automotive photography, no AI artifacts, photorealistic", "ia": "Gemini ou ChatGPT"},
        {"nome": "Moto GS no Posto", "prompt": "Ultra-realistic 8K photo, BMW GS 1200 motorcycle parked at a gas station at night, neon lights reflecting on the chrome parts, dramatic lighting, street photography style, Brazil urban setting, photorealistic, no AI look", "ia": "Gemini ou Leonardo.ai"},
        {"nome": "Hilux na Estrada de Terra", "prompt": "Ultra-realistic 8K photograph, Toyota Hilux pickup truck on a dirt road in rural Brazil, golden hour lighting, dust rising behind the truck, dramatic sky with clouds, cinematic shot, professional photography, no AI artifacts", "ia": "Gemini"},
        {"nome": "Hayabusa na Pista", "prompt": "Ultra-realistic 8K photo, Suzuki Hayabusa motorcycle on a racetrack, motion blur effect on wheels, rider in full gear leaning into a curve, dramatic lighting, speed photography, no AI artifacts, photorealistic", "ia": "Leonardo.ai"},
        {"nome": "Hornet na Cidade", "prompt": "Ultra-realistic 8K photograph, Honda Hornet motorcycle in urban setting at night, city lights bokeh, rider stopped at traffic light, cinematic lighting, street photography, Brazil city backdrop, photorealistic", "ia": "Gemini"},
        {"nome": "Audi R8 Estacionado", "prompt": "Ultra-realistic 8K photograph of an Audi R8 sports car parked in front of a luxury building at night, dramatic lighting, reflections on the car body, editorial automotive photography, no AI artifacts", "ia": "Gemini ou ChatGPT"},
        {"nome": "Banho na BMW", "prompt": "Ultra-realistic 8K photo, person washing a BMW motorcycle, water droplets on chrome parts, golden hour sunlight, garage setting, lifestyle photography, photorealistic, no AI look", "ia": "Gemini"},
        {"nome": "Interior Mercedes Preto", "prompt": "Ultra-realistic 8K photograph inside a black Mercedes-Benz, leather interior, ambient orange lighting, steering wheel detail, dashboard technology display, night setting, luxury car photography, no AI artifacts", "ia": "ChatGPT"},
        {"nome": "GS 1200 Aventura", "prompt": "Ultra-realistic 8K photo, BMW GS 1200 adventure motorcycle on a mountain road in Brazil, dramatic landscape, rider with luggage, adventure travel photography, cinematic shot, photorealistic", "ia": "Gemini"},
        {"nome": "Banco Traseiro do Carro", "prompt": "Ultra-realistic 8K photograph, luxury car backseat perspective, leather seats, city lights through window at night, wealthy lifestyle, editorial photography, no AI artifacts, cinematic", "ia": "Gemini ou Leonardo.ai"},
    ],
    "academia": [
        {"nome": "Boxe no Saco", "prompt": "Ultra-realistic 8K photograph of a male boxer training in a professional gym, hitting a heavy bag, dramatic side lighting, sweat drops visible, intense expression, black background, sports photography, no AI artifacts, photorealistic", "ia": "ChatGPT ou Gemini"},
        {"nome": "Atleta Corrida Noite", "prompt": "Ultra-realistic 8K photo of an athlete running at night in a city, motion blur on legs, city lights bokeh in background, sports wear, determined expression, cinematic lighting, street photography, no AI look", "ia": "Gemini"},
        {"nome": "Musculação Pesada", "prompt": "Ultra-realistic 8K photograph, muscular man lifting heavy barbell in gym, dramatic lighting from above, sweat, intense focus, black background, fitness photography, photorealistic, no AI artifacts", "ia": "Leonardo.ai"},
        {"nome": "UFC Octógono", "prompt": "Ultra-realistic 8K photo, MMA fighter inside UFC octagon, dramatic ring lighting, fighting stance, crowd blurred in background, sports photography, cinematic shot, no AI artifacts", "ia": "Gemini"},
        {"nome": "Corrida no Autódromo", "prompt": "Ultra-realistic 8K photograph of an athlete running on a professional athletics track, motion blur, competitive race, stadium lights, sports photography, dramatic perspective, photorealistic", "ia": "Gemini"},
        {"nome": "Futebol Estadio", "prompt": "Ultra-realistic 8K photo, football player kicking ball in a packed stadium, dramatic stadium lighting, crowd in background, action shot, sports photography, cinematic, no AI artifacts", "ia": "ChatGPT ou Gemini"},
        {"nome": "Personal Trainer", "prompt": "Ultra-realistic 8K photograph of a personal trainer coaching client in modern gym, motivational moment, gym equipment background, professional sports photography, natural lighting, photorealistic", "ia": "Gemini"},
        {"nome": "Atleta Pódio", "prompt": "Ultra-realistic 8K photo of an athlete on a victory podium, gold medal, crowd celebrating, confetti falling, emotional moment, sports photography, cinematic lighting, no AI artifacts", "ia": "Gemini"},
    ],
    "natureza": [
        {"nome": "Praia Paradisíaca", "prompt": "Ultra-realistic 8K photograph of a pristine Brazilian beach, crystal clear turquoise water, white sand, coconut palms, golden hour lighting, aerial perspective, travel photography, no AI artifacts, photorealistic", "ia": "Gemini ou Copilot"},
        {"nome": "Cachoeira na Floresta", "prompt": "Ultra-realistic 8K photo of a waterfall deep in the Amazon rainforest, lush green vegetation, mist rising from the water, magical lighting through the canopy, nature photography, long exposure effect, no AI look", "ia": "Leonardo.ai"},
        {"nome": "Pôr do Sol no Mar", "prompt": "Ultra-realistic 8K photograph of a dramatic sunset over the ocean, orange and pink sky, silhouette of palm trees, reflection on calm water, travel photography, no AI artifacts, photorealistic", "ia": "Gemini"},
        {"nome": "Montanha Nevada", "prompt": "Ultra-realistic 8K photo, snow-capped mountain peak above clouds, dramatic sky, golden hour lighting, landscape photography, epic scenery, no AI artifacts, photorealistic", "ia": "Gemini ou Leonardo.ai"},
        {"nome": "Floresta Tropical", "prompt": "Ultra-realistic 8K photograph inside the Amazon rainforest, rays of sunlight through dense canopy, exotic flowers, misty atmosphere, nature photography, cinematic lighting, no AI artifacts", "ia": "Leonardo.ai"},
        {"nome": "Praia ao Entardecer", "prompt": "Ultra-realistic 8K photo of a Brazilian beach at sunset, warm orange tones, couple walking on shoreline, gentle waves, travel photography, golden hour, photorealistic, no AI look", "ia": "Gemini"},
        {"nome": "Lago Espelho", "prompt": "Ultra-realistic 8K photograph, mirror-like lake reflecting mountains and sky, perfect reflection, serene landscape, golden hour, nature photography, no AI artifacts, photorealistic", "ia": "Gemini ou Copilot"},
        {"nome": "Chuva na Floresta", "prompt": "Ultra-realistic 8K photo, rain falling in a tropical forest, water drops on leaves, misty atmosphere, green tones, moody nature photography, long exposure, no AI artifacts", "ia": "Leonardo.ai"},
    ],
    "luxo": [
        {"nome": "Beira da Piscina Infinita", "prompt": "Ultra-realistic 8K photograph, man relaxing at the edge of an infinity pool overlooking Rio de Janeiro at sunset, luxury lifestyle, champagne glass on the side, warm golden lighting, editorial photography style, no AI artifacts", "ia": "Gemini ou Leonardo.ai"},
        {"nome": "Boate VIP", "prompt": "Ultra-realistic 8K photo inside an exclusive nightclub VIP area, bottle service, sparklers on bottles, purple and blue ambient lighting, crowd in background blurred, luxury lifestyle photography, no AI look", "ia": "ChatGPT"},
        {"nome": "Laje do Rio", "prompt": "Ultra-realistic 8K photograph, rooftop party overlooking Rio de Janeiro skyline, luxury outdoor lounge, Sugarloaf Mountain in background, golden hour, lifestyle photography, no AI artifacts", "ia": "Gemini"},
        {"nome": "Champagne no Yacht", "prompt": "Ultra-realistic 8K photo, luxury yacht deck, champagne bottles in ice bucket, ocean backdrop, golden sunset, wealthy lifestyle photography, editorial style, no AI artifacts", "ia": "Gemini ou ChatGPT"},
        {"nome": "Suite Hotel 5 Estrelas", "prompt": "Ultra-realistic 8K photograph inside a 5-star hotel suite, city view through floor-to-ceiling windows, luxury furniture, elegant decor, soft lighting, architectural photography, no AI artifacts", "ia": "Gemini"},
        {"nome": "Jantar Exclusivo", "prompt": "Ultra-realistic 8K photo, exclusive fine dining restaurant, elegant table setting, candles, luxury atmosphere, couple dining, editorial lifestyle photography, no AI look", "ia": "ChatGPT"},
    ],
    "dubai": [
        {"nome": "Dubai Skyline Noturno", "prompt": "Ultra-realistic 8K photograph of Dubai skyline at night from a rooftop, Burj Khalifa in background, luxury lifestyle, man in stylish outfit looking at the view, city lights reflection, cinematic photography, no AI artifacts", "ia": "Gemini"},
        {"nome": "Aeroporto Dubai", "prompt": "Ultra-realistic 8K photo inside Dubai International Airport, modern architecture, luxury shops in background, traveler with designer luggage, cinematic lighting, travel photography, no AI artifacts", "ia": "Gemini ou ChatGPT"},
        {"nome": "Deserto Dubai", "prompt": "Ultra-realistic 8K photograph, luxury 4x4 vehicle in Dubai desert at sunset, sand dunes, dramatic orange sky, adventure lifestyle, cinematic shot, no AI artifacts, photorealistic", "ia": "Gemini"},
        {"nome": "Palm Jumeirah Vista", "prompt": "Ultra-realistic 8K aerial photograph of Palm Jumeirah Dubai, luxury hotels and residences, turquoise water, clear sky, travel photography, drone shot, no AI artifacts", "ia": "Gemini ou Leonardo.ai"},
    ],
    "festas": [
        {"nome": "Ano Novo Copacabana", "prompt": "Ultra-realistic 8K photograph of New Year's Eve celebration in Rio de Janeiro, fireworks over Copacabana beach, crowd celebrating, colorful lights reflected on the water, aerial view, festive atmosphere, photorealistic, no AI artifacts", "ia": "Gemini"},
        {"nome": "Carnaval Rio", "prompt": "Ultra-realistic 8K photo of Rio Carnival parade, samba dancers in elaborate costumes, confetti, sambadrome, vibrant colors, celebration photography, cinematic lighting, no AI look", "ia": "Gemini ou ChatGPT"},
        {"nome": "Aniversário Surpresa", "prompt": "Ultra-realistic 8K photograph, surprise birthday party scene, confetti falling, birthday cake with candles, excited expression, warm lighting, celebration photography, no AI artifacts", "ia": "ChatGPT"},
        {"nome": "Casamento ao Pôr do Sol", "prompt": "Ultra-realistic 8K photograph, outdoor wedding ceremony at sunset, couple exchanging vows, flower decorations, warm golden light, romantic photography, cinematic style, no AI artifacts, photorealistic", "ia": "Gemini"},
        {"nome": "Festa Piscina", "prompt": "Ultra-realistic 8K photo, luxury pool party, people celebrating, tropical drinks, summer vibes, golden hour lighting, lifestyle photography, no AI look", "ia": "Gemini ou Leonardo.ai"},
    ],
    "fe": [
        {"nome": "Agradecendo a Deus", "prompt": "Ultra-realistic 8K photograph of a person kneeling in prayer in a beautiful church, rays of light coming through stained glass windows, peaceful and spiritual atmosphere, emotional photography, no AI artifacts, photorealistic", "ia": "Gemini ou ChatGPT"},
        {"nome": "Luz Divina na Igreja", "prompt": "Ultra-realistic 8K photo inside a majestic cathedral, dramatic rays of light through stained glass, golden dust particles, spiritual atmosphere, architectural photography, no AI artifacts", "ia": "Leonardo.ai"},
        {"nome": "Mãos em Oração", "prompt": "Ultra-realistic 8K close-up photograph of hands clasped in prayer, soft warm lighting, bokeh background, spiritual and peaceful mood, fine art photography, no AI artifacts, photorealistic", "ia": "Gemini"},
        {"nome": "Nascer do Sol Fé", "prompt": "Ultra-realistic 8K photograph, person with arms raised toward a dramatic sunrise, silhouette against colorful sky, spiritual moment, inspirational photography, no AI artifacts", "ia": "Gemini ou Copilot"},
    ],
    "variados": [
        {"nome": "Empresário no Escritório", "prompt": "Ultra-realistic 8K photograph, successful businessman in modern office, city view through window, professional suit, confident posture, editorial business photography, no AI artifacts, photorealistic", "ia": "Gemini"},
        {"nome": "Chef Cozinhando", "prompt": "Ultra-realistic 8K photo, professional chef in restaurant kitchen, plating gourmet dish, dramatic lighting, steam rising, culinary photography, cinematic style, no AI artifacts", "ia": "ChatGPT ou Gemini"},
        {"nome": "DJ na Balada", "prompt": "Ultra-realistic 8K photograph, DJ performing at night club, LED lights, crowd in background, hands on mixer, music and nightlife photography, dramatic lighting, no AI look", "ia": "Leonardo.ai"},
        {"nome": "Influencer Foto Studio", "prompt": "Ultra-realistic 8K photo, social media influencer in professional photo studio, ring light setup, camera in background, lifestyle content creation, editorial photography, no AI artifacts", "ia": "Gemini"},
        {"nome": "Barber Shop Estilo", "prompt": "Ultra-realistic 8K photograph inside a stylish barbershop, barber cutting client hair, vintage decor, warm lighting, lifestyle photography, editorial style, no AI artifacts, photorealistic", "ia": "ChatGPT"},
        {"nome": "Skate no Parque", "prompt": "Ultra-realistic 8K action photo, skateboarder performing trick at skate park, motion blur, urban environment, golden hour, youth lifestyle photography, cinematic, no AI look", "ia": "Gemini ou Leonardo.ai"},
        {"nome": "Tatuador no Trabalho", "prompt": "Ultra-realistic 8K photo, tattoo artist working on client, close up of detailed tattoo, studio setting, artistic atmosphere, lifestyle photography, no AI artifacts", "ia": "Gemini"},
        {"nome": "Médico Consultório", "prompt": "Ultra-realistic 8K photograph, doctor in modern medical office, white coat, professional setting, warm lighting, healthcare photography, editorial style, no AI artifacts, photorealistic", "ia": "ChatGPT"},
        {"nome": "Advogado Escritório", "prompt": "Ultra-realistic 8K photo, lawyer in prestigious law office, bookshelves with books, professional suit, confident expression, business photography, no AI look", "ia": "Gemini"},
        {"nome": "Mulher Executiva", "prompt": "Ultra-realistic 8K photograph, successful businesswoman in modern office, power suit, city view background, confident posture, editorial business photography, no AI artifacts, photorealistic", "ia": "Gemini ou ChatGPT"},
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

# Alias para compatibilidade
PROMPTS_EXEMPLOS = PROMPTS_BANCO
