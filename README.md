# Site Change Monitor Template

Este template monitora mudanças em páginas web e envia alertas no Slack e por e-mail.

## Páginas monitoradas

- https://olist.com/
- https://olist.com/planos/

## Como usar

1. Faça fork deste repositório ou clone.
2. Adicione os secrets no GitHub Actions:
    - **SLACK_TOKEN** → token do seu bot do Slack
    - **EMAIL_USERNAME** → seu e-mail (ex: meuemail@gmail.com)
    - **EMAIL_PASSWORD** → senha de app (para Gmail, gere em myaccount.google.com)
3. O workflow roda diariamente (pode ser ajustado no `.github/workflows/site-monitor.yml`).
4. Se alguma página mudar, você receberá um alerta no Slack e por e-mail.

## Customização

- Para adicionar/remover URLs, edite `check_site.py`, lista `URLS`.

## Notas

- Para Gmail, é necessário usar uma senha de app e não a senha da conta.