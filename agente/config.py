"""Configurações do agente. Ajuste à vontade."""

# Pasta onde o navegador guarda seu login (fica só no seu computador).
PASTA_SESSAO = "sessao"

# Reels
REELS_POR_SESSAO = (8, 15)          # quantidade sorteada entre min e max
TEMPO_POR_REEL_SEG = (6, 25)        # quanto tempo "assiste" cada reel

# Feed
ROLAGENS_FEED = (10, 20)            # quantas vezes rola o feed
PAUSA_FEED_SEG = (2, 7)             # pausa olhando cada parte do feed

# Curtidas: 0.0 = nunca curte (padrão, mais seguro). 0.1 = curte ~10%.
CHANCE_CURTIR = 0.0
MAX_CURTIDAS_POR_SESSAO = 5
