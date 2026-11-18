# Automação Kairon — Agente de Instagram

Agente que usa o Instagram como uma pessoa: **assiste reels** e **rola o feed**,
com pausas aleatórias. Você vê tudo acontecendo numa janela do navegador.

> ⚠️ Os termos do Instagram não permitem automação. Use com moderação
> (poucas sessões por dia), deixe curtidas desligadas no começo e, se puder,
> teste numa conta secundária.

## Instalação (no seu computador)

Precisa de Python 3.10+.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
```

## Uso

1. **Login (só a primeira vez)**, feito por você na janela que abrir:
   ```bash
   python -m agente.agente login
   ```
2. **Rodar:**
   ```bash
   python -m agente.agente reels   # só reels
   python -m agente.agente feed    # só feed
   python -m agente.agente tudo    # feed e depois reels
   ```
   `Ctrl+C` para parar a qualquer momento.

## Ajustes

Edite `agente/config.py`: quantidade de reels, tempo assistindo, rolagens do
feed e chance de curtir (`CHANCE_CURTIR = 0.1` → curte ~10%).

O login fica salvo na pasta `sessao/`, que está no `.gitignore` e **nunca**
deve ser enviada ao GitHub.

## Próximos passos

- Postagem pelo agente via API oficial da Meta (exige conta Profissional).
