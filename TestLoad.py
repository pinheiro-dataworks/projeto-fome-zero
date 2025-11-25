# ==============================================================================
# TESTE DE CARREGAMENTO - Verificar se tudo está funcionando
# ==============================================================================
import pandas as pd
import numpy as np

print("✓ Bibliotecas importadas com sucesso!")

# Caminho completo para o arquivo
caminho_arquivo = r"C:\Users\rfppr\Downloads\COMUNIDADE DS\repos\portifolio_projetos\ProjetoFomeZero\kaggle\zomato.csv"

# Carregar os dados
df = pd.read_csv(caminho_arquivo)

print(f"✓ Arquivo carregado com sucesso!")
print(f"✓ Dimensões do DataFrame: {df.shape}")
print(f"✓ Primeiras linhas:")
print(df.head())