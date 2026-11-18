"""
Agente simples para usar o Instagram como uma pessoa:
assistir reels e rolar o feed, com pausas aleatórias.

Uso:
    python -m agente.agente login     # abre o navegador para você entrar (só a 1ª vez)
    python -m agente.agente reels     # assiste alguns reels
    python -m agente.agente feed      # rola o feed
    python -m agente.agente tudo      # feed + reels
"""
import random
import sys
import time

from playwright.sync_api import sync_playwright, Page

from agente import config

URL = "https://www.instagram.com/"
ROTULOS_CURTIR = ("Curtir", "Like")


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def pausa(intervalo: tuple[float, float]) -> None:
    time.sleep(random.uniform(*intervalo))


def abrir_navegador(p):
    return p.chromium.launch_persistent_context(
        config.PASTA_SESSAO,
        headless=False,               # janela visível: você vê o que ele faz
        viewport={"width": 1280, "height": 860},
        locale="pt-BR",
    )


def esta_logado(page: Page) -> bool:
    page.goto(URL, wait_until="domcontentloaded")
    pausa((3, 5))
    return page.locator('input[name="username"]').count() == 0


class Curtidor:
    def __init__(self) -> None:
        self.total = 0

    def talvez_curtir(self, page: Page) -> None:
        if config.CHANCE_CURTIR <= 0 or self.total >= config.MAX_CURTIDAS_POR_SESSAO:
            return
        if random.random() > config.CHANCE_CURTIR:
            return
        for rotulo in ROTULOS_CURTIR:
            botao = page.locator(f'svg[aria-label="{rotulo}"]').first
            if botao.count() and botao.is_visible():
                botao.click()
                self.total += 1
                log(f"  curtiu ({self.total}/{config.MAX_CURTIDAS_POR_SESSAO})")
                pausa((1, 2))
                return


def assistir_reels(page: Page, curtidor: Curtidor) -> None:
    qtd = random.randint(*config.REELS_POR_SESSAO)
    log(f"Abrindo Reels — vai assistir {qtd}")
    page.goto(URL + "reels/", wait_until="domcontentloaded")
    pausa((4, 6))
    page.mouse.move(640, 430)
    for i in range(1, qtd + 1):
        tempo = random.uniform(*config.TEMPO_POR_REEL_SEG)
        log(f"Reel {i}/{qtd}: assistindo {tempo:.0f}s")
        time.sleep(tempo)
        curtidor.talvez_curtir(page)
        page.mouse.wheel(0, random.randint(700, 900))   # próximo reel
        pausa((1, 2.5))


def rolar_feed(page: Page, curtidor: Curtidor) -> None:
    qtd = random.randint(*config.ROLAGENS_FEED)
    log(f"Abrindo feed — {qtd} rolagens")
    page.goto(URL, wait_until="domcontentloaded")
    pausa((4, 6))
    page.mouse.move(640, 430)
    for i in range(1, qtd + 1):
        page.mouse.wheel(0, random.randint(300, 750))
        log(f"Feed {i}/{qtd}")
        pausa(config.PAUSA_FEED_SEG)
        curtidor.talvez_curtir(page)


def main() -> None:
    modo = sys.argv[1] if len(sys.argv) > 1 else "tudo"
    if modo not in {"login", "reels", "feed", "tudo"}:
        print(__doc__)
        sys.exit(1)

    with sync_playwright() as p:
        ctx = abrir_navegador(p)
        page = ctx.pages[0] if ctx.pages else ctx.new_page()

        if modo == "login":
            page.goto(URL)
            log("Entre na sua conta na janela aberta. Depois volte aqui e aperte Enter.")
            input()
            log("Sessão salva!" if esta_logado(page) else "Ainda não parece logado.")
            ctx.close()
            return

        if not esta_logado(page):
            log("Você não está logado. Rode primeiro:  python -m agente.agente login")
            ctx.close()
            sys.exit(1)

        curtidor = Curtidor()
        try:
            if modo in ("feed", "tudo"):
                rolar_feed(page, curtidor)
            if modo in ("reels", "tudo"):
                assistir_reels(page, curtidor)
        except KeyboardInterrupt:
            log("Interrompido por você.")
        log(f"Fim da sessão. Curtidas: {curtidor.total}")
        ctx.close()


if __name__ == "__main__":
    main()
