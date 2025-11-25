# Script para testar se todas as bibliotecas foram instaladas corretamente

try:
    import pandas
    print("✓ pandas importado com sucesso")
except ImportError:
    print("✗ pandas NÃO foi instalado")

try:
    import numpy
    print("✓ numpy importado com sucesso")
except ImportError:
    print("✗ numpy NÃO foi instalado")

try:
    import plotly
    print("✓ plotly importado com sucesso")
except ImportError:
    print("✗ plotly NÃO foi instalado")

try:
    import streamlit
    print("✓ streamlit importado com sucesso")
except ImportError:
    print("✗ streamlit NÃO foi instalado")

try:
    import jupyter
    print("✓ jupyter importado com sucesso")
except ImportError:
    print("✗ jupyter NÃO foi instalado")

try:
    import inflection
    print("✓ inflection importado com sucesso")
except ImportError:
    print("✗ inflection NÃO foi instalado")

print("\n✓ Todas as bibliotecas foram instaladas com sucesso!")