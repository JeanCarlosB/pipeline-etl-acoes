import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import sqlite3

def extrair_dados_acoes(tickers, dias_historico=180):
    """
    Função para extrair o histórico de ações do Yahoo Finance.
    """
    print(f"Iniciando a extração para os ativos: {tickers}...")
    
    data_fim = datetime.today().strftime('%Y-%m-%d')
    data_inicio = (datetime.today() - timedelta(days=dias_historico)).strftime('%Y-%m-%d')
    
    df_consolidado = pd.DataFrame()

    for ticker in tickers:
        print(f"Baixando dados de {ticker}...")
        acao = yf.download(ticker, start=data_inicio, end=data_fim, progress=False)
        
        # === A CORREÇÃO ENTRA AQUI ===
        # Se o yfinance trouxer colunas duplas (MultiIndex), nós achatamos pegando só o primeiro nível (Open, Close, etc)
        if isinstance(acao.columns, pd.MultiIndex):
            acao.columns = acao.columns.get_level_values(0)
        # ==============================
        
        acao.reset_index(inplace=True)
        acao['Ativo'] = ticker
        
        df_consolidado = pd.concat([df_consolidado, acao], ignore_index=True)

    print("Extração concluída com sucesso!\n")
    return df_consolidado

def limpar_e_transformar_dados(df):
    """
    Função para tratar os dados brutos e deixá-los prontos para o banco.
    """
    print("Iniciando a limpeza dos dados...")
    
    # Seleciona apenas as colunas que importam para nós
    # Date (Data), Open (Abertura), High (Máxima), Low (Mínima), Close (Fechamento), Volume, Ativo
    df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Ativo']]
    
    # Renomeia as colunas para português e para um padrão fácil de ler (sem espaços ou caracteres especiais)
    df.columns = ['data_pregao', 'preco_abertura', 'preco_maximo', 'preco_minimo', 'preco_fechamento', 'volume_negociado', 'codigo_ativo']
    
    # Arredonda os valores financeiros para 2 casas decimais
    colunas_financeiras = ['preco_abertura', 'preco_maximo', 'preco_minimo', 'preco_fechamento']
    df[colunas_financeiras] = df[colunas_financeiras].round(2)
    
    # Formata a data para ficar apenas Ano-Mês-Dia (sem horas)
    df['data_pregao'] = pd.to_datetime(df['data_pregao']).dt.date
    
    print("Limpeza concluída!\n")
    return df

def salvar_no_banco(df, nome_banco='banco_acoes.db'):
    """
    Função para carregar os dados limpos em um banco de dados relacional (SQLite).
    """
    print(f"Conectando ao banco de dados '{nome_banco}'...")
    
    # Cria a conexão com o banco (se o arquivo não existir, o Python cria ele na hora)
    conexao = sqlite3.connect(nome_banco)
    cursor = conexao.cursor()
    
    # === Demonstração de SQL Puro ===
    # Criando a estrutura da tabela se ela ainda não existir
    query_criar_tabela = '''
    CREATE TABLE IF NOT EXISTS historico_acoes (
        data_pregao TEXT,
        preco_abertura REAL,
        preco_maximo REAL,
        preco_minimo REAL,
        preco_fechamento REAL,
        volume_negociado INTEGER,
        codigo_ativo TEXT
    )
    '''
    cursor.execute(query_criar_tabela)
    
    print("Injetando os dados na tabela 'historico_acoes'...")
    
    # O Pandas tem um método excelente para mandar o DataFrame inteiro para o SQL
    # if_exists='replace' garante que nos nossos testes ele vai sobrescrever e não duplicar os dados.
    # (Em um ambiente de produção real diário, usaríamos 'append' para ir somando os dias).
    df.to_sql('historico_acoes', conexao, if_exists='replace', index=False)
    
    # Salva as alterações e fecha a porta do banco
    conexao.commit()
    conexao.close()
    
    print("Dados salvos com sucesso no banco de dados!\n")

# === Execução do Script ===
if __name__ == "__main__":
    minhas_acoes = ['PETR4.SA', 'VALE3.SA', 'ITUB4.SA', 'BBDC4.SA']
    
    # 1. Extração (E)
    dados_brutos = extrair_dados_acoes(minhas_acoes, dias_historico=30)
    
    # 2. Transformação (T)
    dados_limpos = limpar_e_transformar_dados(dados_brutos)
    
    # 3. Load / Carga (L) -> A Mágica Acontece Aqui
    salvar_no_banco(dados_limpos)