# ==============================================================================
# app.py - Dashboard Fome Zero com Streamlit
# ==============================================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import warnings

warnings.filterwarnings('ignore')

# ==============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ==============================================================================
st.set_page_config(
    page_title="Fome Zero - Dashboard Gerencial",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# FUNÇÕES AUXILIARES (Mesmas do script de análise)
# ==============================================================================

# Dicionário de países
COUNTRIES = {
    1: "India", 14: "Australia", 30: "Brazil", 37: "Canada", 94: "Indonesia",
    148: "New Zeland", 162: "Philippines", 166: "Qatar", 184: "Singapure",
    189: "South Africa", 191: "Sri Lanka", 208: "Turkey", 214: "United Arab Emirates",
    215: "England", 216: "United States of America",
}

def country_name(country_id):
    """Retorna o nome do país com base no ID"""
    return COUNTRIES.get(country_id, "Unknown")

def create_price_type(price_range):
    """Cria a categoria de preço com base no valor"""
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"

def rename_columns(dataframe):
    """Renomeia as colunas do dataframe para o formato snake_case"""
    df = dataframe.copy()
    new_cols = [col.replace(' ', '_').lower() for col in df.columns]
    df.columns = new_cols
    return df

# ==============================================================================
# CARREGAR E PROCESSAR OS DADOS
# ==============================================================================

@st.cache_data
def load_data():
    """
    Carrega e processa os dados do arquivo zomato.csv
    O decorator @st.cache_data melhora a performance ao cachear os dados
    """
    # Caminho completo para o arquivo
    caminho_arquivo = r"C:\Users\rfppr\Downloads\COMUNIDADE DS\repos\portifolio_projetos\ProjetoFomeZero\kaggle\zomato.csv"
    
    # Carregar os dados
    df = pd.read_csv(caminho_arquivo)
    
    # Renomear colunas
    df = rename_columns(df)
    
    # Remover linhas com 'cuisines' nulo
    df = df.dropna(subset=['cuisines'])
    
    # Padronizar a coluna 'cuisines' para ter apenas um tipo
    df["cuisines"] = df.loc[:, "cuisines"].astype(str).apply(lambda x: x.split(",")[0])
    
    # Criar novas colunas
    df['country'] = df['country_code'].apply(country_name)
    df['price_type'] = df['price_range'].apply(create_price_type)
    
    # Remover duplicatas
    df = df.drop_duplicates().reset_index(drop=True)
    
    return df

# Carregar os dados
df1 = load_data()

# ==============================================================================
# TÍTULO E DESCRIÇÃO
# ==============================================================================

st.title("🍽️ Projeto FTC - Fome Zero")
st.markdown("""
    Bem-vindo ao Dashboard Gerencial da Fome Zero!
    
    Esta plataforma oferece insights detalhados sobre restaurantes, cidades e países,
    ajudando na tomada de decisões estratégicas.
""")

st.markdown("---")

# ==============================================================================
# BARRA LATERAL (FILTROS)
# ==============================================================================

st.sidebar.header("🔍 Filtros")

# Filtro de países
paises_disponiveis = sorted(df1['country'].unique().tolist())
paises_selecionados = st.sidebar.multiselect(
    "Escolha os Países",
    paises_disponiveis,
    default=['Brazil', 'India', 'England', 'United States of America']
)

# Filtro de tipo de culinária
cuisines_disponiveis = sorted(df1['cuisines'].unique().tolist())
cuisines_selecionadas = st.sidebar.multiselect(
    "Escolha os Tipos de Culinária",
    cuisines_disponiveis,
    default=None
)

# Filtro de faixa de preço
price_types = sorted(df1['price_type'].unique().tolist())
price_types_selecionados = st.sidebar.multiselect(
    "Escolha a Faixa de Preço",
    price_types,
    default=None
)

# Aplicar filtros ao dataframe
df_filtrado = df1[df1['country'].isin(paises_selecionados)]

if cuisines_selecionadas:
    df_filtrado = df_filtrado[df_filtrado['cuisines'].isin(cuisines_selecionadas)]

if price_types_selecionados:
    df_filtrado = df_filtrado[df_filtrado['price_type'].isin(price_types_selecionados)]

# ==============================================================================
# ABAS PRINCIPAIS
# ==============================================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Visão Geral",
    "🌍 Visão por País",
    "🏙️ Visão por Cidade",
    "🍴 Visão por Culinária"
])

# --- TAB 1: VISÃO GERAL ---
with tab1:
    st.header("📊 Métricas Gerais")
    
    # Criar colunas para as métricas
    col1, col2, col3, col4, col5 = st.columns(5)
    
    col1.metric(
        "🏪 Restaurantes",
        df_filtrado['restaurant_id'].nunique()
    )
    col2.metric(
        "🌎 Países",
        df_filtrado['country'].nunique()
    )
    col3.metric(
        "🏙️ Cidades",
        df_filtrado['city'].nunique()
    )
    col4.metric(
        "⭐ Avaliações",
        f"{df_filtrado['votes'].sum():,}"
    )
    col5.metric(
        "🍽️ Tipos de Culinária",
        df_filtrado['cuisines'].nunique()
    )
    
    st.markdown("---")
    
    # Gráfico 1: Restaurantes por país
    st.subheader("Quantidade de Restaurantes por País")
    fig1 = px.bar(
        df_filtrado.groupby('country')['restaurant_id'].nunique().reset_index(name='count'),
        x='country',
        y='count',
        title='Restaurantes por País',
        labels={'country': 'País', 'count': 'Quantidade'},
        color='count',
        color_continuous_scale='Blues'
    )
    fig1.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig1, use_container_width=True)
    
    # Gráfico 2: Avaliações por país
    st.subheader("Total de Avaliações por País")
    fig2 = px.bar(
        df_filtrado.groupby('country')['votes'].sum().reset_index(name='total_votes'),
        x='country',
        y='total_votes',
        title='Avaliações por País',
        labels={'country': 'País', 'total_votes': 'Total de Avaliações'},
        color='total_votes',
        color_continuous_scale='Greens'
    )
    fig2.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

# --- TAB 2: VISÃO POR PAÍS ---
with tab2:
    st.header("🌍 Análise por País")
    
    # Gráfico 1: Nota média por país
    st.subheader("Nota Média por País")
    fig3 = px.bar(
        df_filtrado.groupby('country')['aggregate_rating'].mean().round(2).reset_index(),
        x='country',
        y='aggregate_rating',
        title='Nota Média por País',
        labels={'country': 'País', 'aggregate_rating': 'Nota Média'},
        color='aggregate_rating',
        color_continuous_scale='RdYlGn'
    )
    fig3.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig3, use_container_width=True)
    
    # Gráfico 2: Preço médio por país
    st.subheader("Preço Médio de um Prato para Dois por País")
    fig4 = px.bar(
        df_filtrado.groupby('country')['average_cost_for_two'].mean().round(2).reset_index(),
        x='country',
        y='average_cost_for_two',
        title='Preço Médio por País',
        labels={'country': 'País', 'average_cost_for_two': 'Preço Médio'},
        color='average_cost_for_two',
        color_continuous_scale='Viridis'
    )
    fig4.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig4, use_container_width=True)
    
    # Tabela: Resumo por país
    st.subheader("Resumo por País")
    resumo_pais = df_filtrado.groupby('country').agg({
        'restaurant_id': 'nunique',
        'city': 'nunique',
        'cuisines': 'nunique',
        'votes': 'sum',
        'aggregate_rating': 'mean',
        'average_cost_for_two': 'mean'
    }).round(2).reset_index()
    
    resumo_pais.columns = ['País', 'Restaurantes', 'Cidades', 'Tipos de Culinária', 'Total de Avaliações', 'Nota Média', 'Preço Médio']
    
    st.dataframe(resumo_pais, use_container_width=True)

# --- TAB 3: VISÃO POR CIDADE ---
with tab3:
    st.header("🏙️ Análise por Cidade")
    
    # Gráfico 1: Top 10 cidades com mais restaurantes
    st.subheader("Top 10 Cidades com Mais Restaurantes")
    top_cidades = df_filtrado.groupby('city')['restaurant_id'].nunique().nlargest(10).reset_index(name='count')
    fig5 = px.bar(
        top_cidades,
        x='count',
        y='city',
        orientation='h',
        title='Top 10 Cidades com Mais Restaurantes',
        labels={'city': 'Cidade', 'count': 'Quantidade'},
        color='count',
        color_continuous_scale='Oranges'
    )
    fig5.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig5, use_container_width=True)
    
    # Gráfico 2: Nota média por cidade
    st.subheader("Nota Média por Cidade (Top 10)")
    top_cidades_nota = df_filtrado.groupby('city')['aggregate_rating'].mean().nlargest(10).reset_index()
    fig6 = px.bar(
        top_cidades_nota,
        x='aggregate_rating',
        y='city',
        orientation='h',
        title='Top 10 Cidades com Melhor Nota Média',
        labels={'city': 'Cidade', 'aggregate_rating': 'Nota Média'},
        color='aggregate_rating',
        color_continuous_scale='RdYlGn'
    )
    fig6.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig6, use_container_width=True)

# --- TAB 4: VISÃO POR CULINÁRIA ---
with tab4:
    st.header("🍴 Análise por Tipo de Culinária")
    
    # Gráfico 1: Top 10 culinarias com mais restaurantes
    st.subheader("Top 10 Tipos de Culinária com Mais Restaurantes")
    top_cuisines = df_filtrado.groupby('cuisines')['restaurant_id'].nunique().nlargest(10).reset_index(name='count')
    fig7 = px.bar(
        top_cuisines,
        x='cuisines',
        y='count',
        title='Top 10 Tipos de Culinária',
        labels={'cuisines': 'Tipo de Culinária', 'count': 'Quantidade'},
        color='count',
        color_continuous_scale='Purples'
    )
    fig7.update_layout(height=400, showlegend=False, xaxis_tickangle=-45)
    st.plotly_chart(fig7, use_container_width=True)
    
    # Gráfico 2: Nota média por culinária
    st.subheader("Nota Média por Tipo de Culinária (Top 10)")
    top_cuisines_nota = df_filtrado.groupby('cuisines')['aggregate_rating'].mean().nlargest(10).reset_index()
    fig8 = px.bar(
        top_cuisines_nota,
        x='cuisines',
        y='aggregate_rating',
        title='Top 10 Tipos de Culinária com Melhor Nota Média',
        labels={'cuisines': 'Tipo de Culinária', 'aggregate_rating': 'Nota Média'},
        color='aggregate_rating',
        color_continuous_scale='RdYlGn'
    )
    fig8.update_layout(height=400, showlegend=False, xaxis_tickangle=-45)
    st.plotly_chart(fig8, use_container_width=True)

# ==============================================================================
# RODAPÉ
# ==============================================================================

st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        <p>Projeto Comunidade DS © 2025</p>
        <p>Desenvolvido por Pinheiro DataWorks</p>
    </div>
""", unsafe_allow_html=True)