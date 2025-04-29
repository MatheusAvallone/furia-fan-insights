import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="FURIA Fan Insights", layout="wide")

st.title("📊 FURIA Fan Insights Dashboard")

# --- 1. Formulário de Cadastro ---
st.header("👤 Cadastrar novo fã")
with st.form(key="form_fan"):
    nome = st.text_input("Nome")
    idade = st.number_input("Idade", min_value=0, max_value=100, step=1)
    jogo_favorito = st.selectbox("Jogo Favorito", ["Valorant", "CS2", "League of Legends", "Outro"])
    localizacao = st.text_input("Localização")  # Novo campo para a localização
    submit_button = st.form_submit_button(label="Cadastrar")

    if submit_button:
        novo_fan = {
            "nome": nome,
            "idade": idade,
            "jogo_favorito": jogo_favorito,
            "localizacao": localizacao  # Incluindo a localização
        }

        # Realizando o POST na API
        try:
            res = requests.post(f"{API_URL}/fans/", json=novo_fan)
            st.write(f"Status Code: {res.status_code}")  # Verifica o código da resposta
            st.write(f"Resposta da API: {res.text}")  # Mostra a resposta completa da API

            if res.status_code == 200:
                st.success("Fã cadastrado com sucesso!")
            else:
                st.error(f"Erro ao cadastrar fã: {res.status_code}. Resposta da API: {res.text}")

        except Exception as e:
            st.error(f"Erro ao se conectar com a API: {e}")

# --- 2. Buscar Fãs e Aplicar Filtros ---

st.header("🔎 Lista de fãs com filtros")

def buscar_fans():
    for i in range(1, 1000):
        res = requests.get(f"{API_URL}/fans/{i}")
        if res.status_code != 200:
            break
        yield res.json()

dados_fans = list(buscar_fans())

if dados_fans:
    df = pd.DataFrame(dados_fans)

    filtro_jogo = st.selectbox("Filtrar por jogo favorito", options=["Todos"] + sorted(df["jogo_favorito"].unique().tolist()))

    if filtro_jogo != "Todos":
        df = df[df["jogo_favorito"] == filtro_jogo]

    st.dataframe(df, use_container_width=True)

    # --- 3. Gráficos ---
    st.subheader("📈 Estatísticas de fãs")

    col1, col2 = st.columns(2)

    with col1:
        fig_idade = px.histogram(df, x="idade", nbins=10, title="Distribuição de idade")
        st.plotly_chart(fig_idade, use_container_width=True)

    with col2:
        fig_jogo = px.pie(df, names="jogo_favorito", title="Jogo favorito dos fãs")
        st.plotly_chart(fig_jogo, use_container_width=True)
else:
    st.warning("Nenhum fã encontrado.")

def obter_fans_filtrados(localizacao: str = None, jogo_favorito: str = None):
    params = {}
    if localizacao:
        params["localizacao"] = localizacao
    if jogo_favorito:
        params["jogo_favorito"] = jogo_favorito

    response = requests.get("http://127.0.0.1:8000/fans/filter/", params=params)
    return response.json()

def exibir_graficos():
    st.title("Distribuição de Fãs")

    # Gráfico de idade por jogo favorito
    fans_data = [
        {"nome": "Lucas", "jogo_favorito": "League of Legends", "idade": 25},
        {"nome": "Mariana", "jogo_favorito": "Valorant", "idade": 22},
        {"nome": "Carlos", "jogo_favorito": "League of Legends", "idade": 28}
    ]
    
    df = pd.DataFrame(fans_data)
    fig = px.histogram(df, x="jogo_favorito", color="idade", title="Distribuição de Idade por Jogo Favorito")
    st.plotly_chart(fig)

# Exemplo de filtragem de fãs
localizacao = st.text_input("Filtrar por localização")
jogo_favorito = st.text_input("Filtrar por jogo favorito")

if st.button("Filtrar Fãs"):
    fãs = obter_fans_filtrados(localizacao, jogo_favorito)
    st.write(f"Fãs encontrados: {fãs}")

exibir_graficos()
