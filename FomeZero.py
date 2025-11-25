# =========================================================================
# 1. IMPORTAÇÃO DAS BIBLIOTECAS E CARREGAMENTO DOS DADOS
#=========================================================================
import pandas as pd
import numpy as np

# Caminho completo para o arquivo no seu computador
caminho_arquivo = r"C:\Users\rfppr\Downloads\COMUNIDADE DS\repos\portifolio_projetos\ProjetoFomeZero\kaggle\zomato.csv"

# Carregar os dados a partir do caminho especificado
df = pd.read_csv(caminho_arquivo)

# =========================================================================
# 2. FUNÇÕES AUXILIARES E LIMPEZA DOS DADOS
# =========================================================================

# Dicionário de países
COUNTRIES = {
    1: "India", 
    14: "Australia", 
    30: "Brazil", 
    37: "Canada", 
    94: "Indonesia",
    148: "New Zeland", 
    162: "Philippines", 
    166: "Qatar", 
    184: "Singapure",
    189: "South Africa", 
    191: "Sri Lanka", 
    208: "Turkey",  
    214: "United Arab Emirates",
    215: "England", 
    216: "United States of America",
}

def country_name(country_id):
    """ Retorna o nome do país com base no ID """
    return COUNTRIES.get(country_id)

def create_price_type(price_range):
    """ Cria a categoria de preço com base no valor """
    if price_range == 1: return "cheap"
    elif price_range == 2: return "normal"
    elif price_range == 3: return "expensive"
    else: return "gourmet"

def rename_columns(dataframe):
    """ Renomeia as colunas do dataframe para o formato snake_case """
    df = dataframe.copy()
    new_cols = [col.replace(' ', '_').lower() for col in df.columns]
    df.columns = new_cols
    return df

# --- Processo de Limpeza ---
# 1. Renomear colunas
df1 = rename_columns(df)

# 2. Remover linhas com 'cuisines' nulo
df1.dropna(subset=['cuisines'], inplace=True)

# 3. Padronizar a coluna 'cuisines' para ter apenas um tipo
df1["cuisines"] = df1.loc[:, "cuisines"].astype(str).apply(lambda x: x.split(",")[0])

# 4. Criar novas colunas
df1['country'] = df1['country_code'].apply(country_name)
df1['price_type'] = df1['price_range'].apply(create_price_type)

# 5. Remover duplicatas
df1 = df1.drop_duplicates().reset_index(drop=True)

print("DataFrame limpo e preparado para análise!")

# =========================================================================
# 3. RESPOSTAS DAS PERGUNTAS DE NEGÓCIO
# =========================================================================

# --- GERAL ---
# 1. Restaurantes únicos
r1 = df1['restaurant_id'].nunique()

# 2. Países únicos
r2 = df1['country'].nunique()

# 3. Cidades únicas
r3 = df1['city'].nunique()

# 4. Total de avaliações
r4 = df1['votes'].sum()

# 5. Tipos de culinária únicos
r5 = df1['cuisines'].nunique()

# --- PAÍS ---
# 6. País com mais cidades
r6 = df1.groupby('country')['city'].nunique().idxmax()

# 7. País com mais restaurantes
r7 = df1.groupby('country')['restaurant_id'].nunique().idxmax()

# 8. País com mais restaurantes gourmet (preço 4)
r8 = df1[df1['price_range'] == 4].groupby('country')['restaurant_id'].nunique().idxmax()

# 9. País com mais diversidade culinária
r9 = df1.groupby('country')['cuisines'].nunique().idxmax()

# 10. País com mais avaliações
r10 = df1.groupby('country')['votes'].sum().idxmax()

# 11. País com mais restaurantes com entrega
r11 = df1[df1['has_online_delivery'] == 1].groupby('country')['restaurant_id'].nunique().idxmax()

# 12. País com mais restaurantes com reserva
r12 = df1[df1['has_table_booking'] == 1].groupby('country')['restaurant_id'].nunique().idxmax()

# 13. País com maior média de avaliações
r13 = df1.groupby('country')['votes'].mean().idxmax()

# 14. País com maior nota média
r14 = df1.groupby('country')['aggregate_rating'].mean().idxmax()

# 15. País com menor nota média
r15 = df1.groupby('country')['aggregate_rating'].mean().idxmin()

# 16. Média de preço por país
r16_df =  df1.groupby('country')['average_cost_for_two'].mean().round(2).sort_values(ascending=False)
# (A resposta será a tabela gerada)

# --- CIDADE ---
# 17. Cidade com mais restaurantes
r17 = df1.groupby('city')['restaurant_id'].nunique().idxmax()

# 18. Cidade com mais restaurantes com nota > 4
r18 = df1[df1['aggregate_rating'] > 4].groupby('city')['restaurant_id'].nunique().idxmax()

# 19. Cidade com mais restaurantes com nota < 2.5
r19 = df1[df1['aggregate_rating'] < 2.5].groupby('city')['restaurant_id'].nunique().idxmax()

# 20. Cidade com maior valor médio de prato para dois
r20 = df1.groupby('city')['average_cost_for_two'].mean().idxmax()

# 21. Cidade com mais diversidade culinária
r21 = df1.groupby('city')['cuisines'].nunique().idxmax()

# 22. Cidade com mais restaurantes com reserva
r22 = df1[df1['has_table_booking'] == 1].groupby('city')['restaurant_id'].nunique().idxmax()

# 23. Cidade com mais restaurantes com entrega
r23 = df1[df1['has_online_delivery'] == 1].groupby('city')['restaurant_id'].nunique().idxmax()

# 24. Cidade com mais restaurantes com pedidos online
r24 = df1[df1['has_online_delivery'] == 1].groupby('city')['restaurant_id'].nunique().idxmax() # Mesma lógica da 23

# --- RESTAURANTES ---
# 25. Restaurante com mais avaliações
r25 = df1.sort_values(by=['votes', 'restaurant_id'], ascending=[False, True]).iloc[0]['restaurant_name']

# 26. Restaurante com maior nota média
r26 = df1.sort_values(by=['aggregate_rating', 'restaurant_id'], ascending=[False, True]).iloc[0]['restaurant_name']

# 27. Restaurante com maior valor de prato para dois
r27 = df1.sort_values(by=['average_cost_for_two', 'restaurant_id'], ascending=[False, True]).iloc[0]['restaurant_name']

# 28. Restaurante brasileiro com menor nota
r28 = df1[(df1['cuisines'] == 'Brazilian')].sort_values(by=['aggregate_rating', 'restaurant_id'], ascending=[True, True]).iloc[0]['restaurant_name']

# 29. Restaurante brasileiro no Brasil com maior nota
r29 = df1[(df1['cuisines'] == 'Brazilian') & (df1['country'] == 'Brazil')].sort_values(by=['aggregate_rating', 'restaurant_id'], ascending=[False, True]).iloc[0]['restaurant_name']

# 30. Pedido online vs. Média de avaliações
r30_yes = df1[df1['has_online_delivery'] == 1]['votes'].mean()
r30_no = df1[df1['has_online_delivery'] == 0]['votes'].mean()
r30 = "Sim" if r30_yes > r30_no else "Não"

# 31. Reserva vs. Preço médio para dois
r31_yes = df1[df1['has_table_booking'] == 1]['average_cost_for_two'].mean()
r31_no = df1[df1['has_table_booking'] == 0]['average_cost_for_two'].mean()
r31 = "Sim" if r31_yes > r31_no else "Não"

# 32. Japonesa vs. BBQ nos EUA
jp_usa = df1[(df1['country'] == 'United States of America') & (df1['cuisines'] == 'Japanese')]['average_cost_for_two'].mean()
bbq_usa = df1[(df1['country'] == 'United States of America') & (df1['cuisines'] == 'BBQ')]['average_cost_for_two'].mean()
r32 = "Não" if bbq_usa > jp_usa else "Sim" # A pergunta é se japonesa é MAIOR

# --- TIPOS DE CULINÁRIA ---
# 33. Melhor restaurante italiano
r33 = df1[df1['cuisines'] == 'Italian'].sort_values(by=['aggregate_rating', 'restaurant_id'], ascending=[False, True]).iloc[0]['restaurant_name']

# 34. Pior restaurante italiano
r34 = df1[df1['cuisines'] == 'Italian'].sort_values(by=['aggregate_rating', 'restaurant_id'], ascending=[True, True]).iloc[0]['restaurant_name']

# 35. Melhor restaurante americano
r35 = df1[df1['cuisines'] == 'American'].sort_values(by=['aggregate_rating', 'restaurant_id'], ascending=[False, True]).iloc[0]['restaurant_name']

# 36. Pior restaurante americano
r36 = df1[df1['cuisines'] == 'American'].sort_values(by=['aggregate_rating', 'restaurant_id'], ascending=[True, True]).iloc[0]['restaurant_name']

# 37. Melhor restaurante árabe
r37 = df1[df1['cuisines'] == 'Arabian'].sort_values(by=['aggregate_rating', 'restaurant_id'], ascending=[False, True]).iloc[0]['restaurant_name']

# 38. Pior restaurante árabe
r38 = df1[df1['cuisines'] == 'Arabian'].sort_values(by=['aggregate_rating', 'restaurant_id'], ascending=[True, True]).iloc[0]['restaurant_name']

# 39. Melhor restaurante japonês
r39 = df1[df1['cuisines'] == 'Japanese'].sort_values(by=['aggregate_rating', 'restaurant_id'], ascending=[False, True]).iloc[0]['restaurant_name']

# 40. Pior restaurante japonês
r40 = df1[df1['cuisines'] == 'Japanese'].sort_values(by=['aggregate_rating', 'restaurant_id'], ascending=[True, True]).iloc[0]['restaurant_name']

# 41. Melhor restaurante caseiro (Home-made)
r41 = df1[df1['cuisines'] == 'Home-made'].sort_values(by=['aggregate_rating', 'restaurant_id'], ascending=[False, True]).iloc[0]['restaurant_name']

# 42. Pior restaurante caseiro (Home-made)
r42 = df1[df1['cuisines'] == 'Home-made'].sort_values(by=['aggregate_rating', 'restaurant_id'], ascending=[True, True]).iloc[0]['restaurant_name']

# 43. Culinária com maior valor médio de prato para dois
r43 = df1.groupby('cuisines')['average_cost_for_two'].mean().idxmax()

# 44. Culinária com maior nota média
r44 = df1.groupby('cuisines')['aggregate_rating'].mean().idxmax()

# 45. Culinária com mais restaurantes com entrega e pedido online
r45 = df1[(df1['has_online_delivery'] == 1) & (df1['has_table_booking'] == 1)].groupby('cuisines').size().idxmax()
