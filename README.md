# 📈 Pipeline ETL Automatizado de Dados Financeiros

Este projeto consiste em um pipeline de Engenharia de Dados (ETL) construído inteiramente em Python para automação de coleta, limpeza e armazenamento de dados do mercado financeiro.

### 🎯 O Problema Resolvido
Eliminar o trabalho manual de extração de planilhas diárias do mercado financeiro, criando um processo automatizado, escalável e livre de erros humanos.

### 🛠️ Arquitetura e Tecnologias
* **Extract (Extração):** Consumo da API do Yahoo Finance via biblioteca `yfinance` para capturar o histórico diário de ações brasileiras (PETR4, VALE3, ITUB4, BBDC4).
* **Transform (Transformação):** Utilização do `Pandas` para higienização dos dados: tratamento de colunas, formatação de datas, padronização de nomenclatura e nivelamento de índices (MultiIndex).
* **Load (Carga):** Injeção automatizada dos dados limpos em um banco de dados relacional `SQLite3`, utilizando queries em **SQL puro** executadas diretamente pelo script Python.

### 🚀 Como executar
1. Instale as dependências: `pip install yfinance pandas`
2. Execute o extrator: `python extrator_acoes.py` (Isso irá gerar o arquivo `.db`)
3. Teste o banco de dados: `python consultar_banco.py` (Realiza um `SELECT` no banco via Pandas)
