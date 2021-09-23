# Ranking do Enem 2019 (RJ)

Ranking do estado do Rio de Janeiro, é fácil mudar para outros estados. Só mexer no CO_UF para o correto.

## Para executar

1. Crie o ambiente conda com `conda env create -f enviroment.yml`
1. Baixe os dados executando `python 01_baixadados.py` e vá tomar um café.
1. Execute o notebook `ledados.ipynb`. Isso cria as estrututuras básicas, já o INEP gosta de dificultar nossa vida mudando arbitrariamente o nome das colunas a cada ano.
1. Execute o `analisa.ipynb` para ver a análise.

## Dados

Dados com endereços das escolas [baixado manualmente do INEP](https://inepdata.inep.gov.br/analytics/saw.dll?Dashboard&PortalPath=%2Fshared%2FCenso%20da%20Educa%C3%A7%C3%A3o%20B%C3%A1sica%2F_portal%2FCat%C3%A1logo%20de%20Escolas&Page=Lista%20das%20Escolas&P1=dashboard&Action=Navigate&ViewState=84khbmj660oafb4etgmn3npq4e&P16=NavRuleDefault&NavFromViewID=d%3Adashboard~p%3Asf156n9k0qs70741)

Outros dados do portal de microdados. Veja arquivo 01_baixar_dados.py