import sqlite3
import pandas as pd

print("Conectando ao banco de dados para consulta...\n")
conexao = sqlite3.connect('banco_acoes.db')

# Aqui você escreve SQL puro! Vamos pedir as 5 primeiras linhas apenas da Petrobras
query_sql = """
SELECT data_pregao, preco_fechamento, volume_negociado 
FROM historico_acoes 
WHERE codigo_ativo = 'PETR4.SA'
ORDER BY data_pregao DESC
LIMIT 5
"""

# O Pandas executa a query no banco e já nos devolve uma tabela arrumada
resultado = pd.read_sql_query(query_sql, conexao)

print("=== Últimos 5 pregões da PETR4 ===")
print(resultado)

conexao.close()