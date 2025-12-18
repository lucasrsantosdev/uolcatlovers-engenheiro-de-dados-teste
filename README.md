## Questão 1 – Extração de Cat Facts (Python)

Foi desenvolvido um script em Python para extração de fatos sobre gatos a partir da API pública Cat Facts, conforme documentação oficial.

Durante os testes, todos os endpoints da API (`/facts` e `/facts/random`) retornaram consistentemente erro HTTP 503 (Service Unavailable), indicando indisponibilidade do backend (Heroku free dyno descontinuado).

Mesmo diante dessa instabilidade externa, o script foi projetado para:

- Tratar falhas de forma resiliente
- Realizar múltiplas tentativas de coleta
- Manter o contrato de saída
- Gerar o arquivo CSV local com cabeçalho, mesmo sem registros

Isso garante que o pipeline funcione corretamente em cenários reais de falha de API, comportamento comum em integrações com serviços externos.
