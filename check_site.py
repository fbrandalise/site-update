import requests
import difflib
import os
import hashlib
import json
from slack_sdk import WebClient

# Configurações
URLS = [
    "https://olist.com/",
    "https://olist.com/planos/"
]

SLACK_TOKEN = os.getenv("SLACK_TOKEN")
SLACK_CANAL = "#monitoramento-site"

def hash_url(url):
    return hashlib.md5(url.encode()).hexdigest()

has_changes = False
changed_url = ""

for url in URLS:
    print(f"✅ Verificando: {url}")
    resposta = requests.get(url)
    pagina_atual = resposta.text

    hash_nome = hash_url(url)
    arquivo_antigo = f"pagina_antiga_{hash_nome}.html"

    mudanca_detectada = False
    diff_texto = ""

    if os.path.exists(arquivo_antigo):
        with open(arquivo_antigo, "r", encoding="utf-8") as f:
            pagina_antiga = f.read()

        diff = difflib.unified_diff(
            pagina_antiga.splitlines(),
            pagina_atual.splitlines(),
            lineterm=""
        )
        diff_texto = "\n".join(diff)

        if diff_texto.strip():
            mudanca_detectada = True
            print(f"⚠️ Mudança detectada em {url}!")
    else:
        print(f"Primeira execução para {url}, salvando versão inicial.")

    with open(arquivo_antigo, "w", encoding="utf-8") as f:
        f.write(pagina_atual)

    if mudanca_detectada:
        has_changes = True
        changed_url = url
        slack_client = WebClient(token=SLACK_TOKEN)
        slack_client.chat_postMessage(
            channel=SLACK_CANAL,
            text=(
                f":warning: *Mudança detectada!*\n"
                f"URL: {url}\n"
                f"Linhas modificadas: {len(diff_texto.splitlines())} linhas"
            )
        )

# Exporta outputs para o GitHub Actions
with open(os.getenv('GITHUB_OUTPUT'), 'a') as fh:
    fh.write(f"has_changes={'true' if has_changes else 'false'}\n")
    fh.write(f"changed_url={changed_url}\n")