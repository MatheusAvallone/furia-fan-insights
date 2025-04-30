import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = "http://127.0.0.1:8000"

# Configuração da página

st.set_page_config(page_title="FURIA Fan Insights", layout="wide")
st.title("🎮 FURIA Fan Insights Dashboard")

# Função para buscar fãs da API

def buscar_fans():
    try:
        res = requests.get(f"{API_URL}/fans/")
        if res.status_code == 200:
            return res.json()
        else:
            return []
    except Exception as e:
        st.error(f"Erro ao buscar fãs: {e}")
        return []

# --- 1. Formulário de Cadastro ---

with st.expander("👤 Cadastrar novo fã", expanded=True):
    with st.form(key="form_fan", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome", placeholder="Digite o nome do fã")
            idade = st.number_input("Idade", min_value=0, max_value=100, step=1)
        with col2:
            jogo_favorito = st.selectbox("Jogo Favorito", ["Valorant", "CS2", "League of Legends", "Outro"])
            localizacao = st.text_input("Localização", placeholder="Onde você mora?")

        submit_button = st.form_submit_button(label="Cadastrar Fã", use_container_width=True)

        if submit_button:
            novo_fan = {
                "nome": nome,
                "idade": idade,
                "jogo_favorito": jogo_favorito,
                "localizacao": localizacao
            }

            try:
                # Cadastra o fã na API
                res = requests.post(f"{API_URL}/fans/", json=novo_fan)
                if res.status_code == 200:
                    st.success("Fã cadastrado com sucesso! 🎉")
                    
                    # Atualiza a lista de fãs no session_state
                    if "fans" not in st.session_state:
                        st.session_state.fans = []
                    # Não sobrescreve, apenas adiciona o novo fã à lista existente
                    st.session_state.fans.append(novo_fan)
                    
                else:
                    st.error(f"Erro ao cadastrar fã: {res.status_code}. Resposta: {res.text}")
            except Exception as e:
                st.error(f"Erro ao se conectar com a API: {e}")

# --- 2. Buscar Fãs e Visualizar ---

st.header("🔎 Lista de Fãs com Filtros")

# Carregar a lista de fãs após o cadastro

dados_fans = st.session_state.get("fans", buscar_fans())  # Tenta carregar da sessão ou buscar da API

if dados_fans:
    df = pd.DataFrame(dados_fans)

    # Filtro de jogo
    filtro_jogo = st.selectbox("🎮 Filtrar por Jogo Favorito", options=["Todos"] + sorted(df["jogo_favorito"].unique().tolist()))
    if filtro_jogo != "Todos":
        df = df[df["jogo_favorito"] == filtro_jogo]

    # Exibe a tabela de fãs
    st.dataframe(df, use_container_width=True)

    # --- 3. Estatísticas e Gráficos ---
    with st.expander("📈 Estatísticas dos Fãs"):
        col1, col2 = st.columns(2)

        with col1:
            fig_idade = px.histogram(df, x="idade", nbins=10, title="Distribuição de Idade")
            st.plotly_chart(fig_idade, use_container_width=True)

        with col2:
            fig_jogo = px.pie(df, names="jogo_favorito", title="Distribuição por Jogo Favorito")
            st.plotly_chart(fig_jogo, use_container_width=True)

else:
    st.warning("Nenhum fã encontrado. 🙁")

# --- 4. Edição de Fã ---

with st.expander("✏️ Editar Informações de um Fã", expanded=False):
    if dados_fans:
        # Adaptação para caso não tenha o 'id' e usarmos 'nome' ou outro identificador
        ids_fans = {f"{fan['nome']}": fan for fan in dados_fans}
        fan_selecionado_nome = st.selectbox("Selecione o Fã", list(ids_fans.keys()))
        fan_info = ids_fans.get(fan_selecionado_nome)

        if fan_info:
            with st.form(key="editar_fan_form"):
                nome_editado = st.text_input("Nome", value=fan_info["nome"])
                idade_editada = st.number_input("Idade", value=fan_info["idade"], min_value=0, max_value=120, step=1)

                jogos_validos = ["Valorant", "CS2", "League of Legends", "Outro"]
                jogo_atual = fan_info.get("jogo_favorito", "Outro")
                if jogo_atual not in jogos_validos:
                    jogos_validos.append(jogo_atual)

                jogo_favorito_editado = st.selectbox("Jogo Favorito", jogos_validos, index=jogos_validos.index(jogo_atual))
                localizacao_editada = st.text_input("Localização", value=fan_info.get("localizacao", ""))

                enviar_edicao = st.form_submit_button("Salvar Alterações")

                if enviar_edicao:
                    atualizado = {
                        "nome": nome_editado,
                        "idade": idade_editada,
                        "jogo_favorito": jogo_favorito_editado,
                        "localizacao": localizacao_editada
                    }

                    try:
                        resposta = requests.put(
                            f"{API_URL}/fans/{fan_info['id']}",
                            json=atualizado  # envia os dados atualizados
                        )
                        if resposta.status_code == 200:
                            st.success("Fã Atualizado com sucesso!")
                            # Atualiza a lista local removendo o antigo e adicionando o novo
                            if "fans" not in st.session_state:
                                st.session_state.fans = []
                            st.session_state.fans = [
                                f for f in st.session_state.fans if f["id"] != fan_info["id"]
                            ] + [fan_info]
                        else:
                            st.error(f"Erro ao atualizar fã: {resposta.status_code}")
                    except Exception as e:
                        st.error(f"Erro ao se conectar com a API: {e}")

                    # Garante que a lista está inicializada
                    if "fans" not in st.session_state:
                        st.session_state.fans = []

                    # Atualiza o fã na lista
                    st.session_state.fans = [
                        fan if fan["nome"] != fan_info["nome"] else fan_info
                        for fan in st.session_state.fans
                    ]

                    st.success("Fã atualizado com sucesso!")

                    # Deletar fã fora do formulário
            if st.button("🗑️ Deletar Fã", use_container_width=True, type="secondary"):
                try:
                    resposta = requests.delete(f"{API_URL}/fans/{fan_info['id']}")
                    if resposta.status_code == 200:
                        st.success("Fã deletado com sucesso!")
                        # Remove o fã da lista local
                        st.session_state.fans = [f for f in st.session_state.fans if f["id"] != fan_info["id"]]
                    else:
                        st.error(f"Erro ao deletar fã: {resposta.status_code}")
                except Exception as e:
                    st.error(f"Erro ao se conectar com a API: {e}")

# --- 5. Filtros Avançados ---

with st.expander("🎯 Filtros Avançados por Localização e Jogo"):
    def obter_fans_filtrados(localizacao: str = None, jogo_favorito: str = None):
        params = {}
        if localizacao:
            params["localizacao"] = localizacao
        if jogo_favorito:
            params["jogo_favorito"] = jogo_favorito

        response = requests.get(f"{API_URL}/fans/filter/", params=params)
        return response.json()

    localizacao_input = st.text_input("Filtrar por Localização")
    jogo_input = st.text_input("Filtrar por Jogo Favorito")

    if st.button("Aplicar Filtros"):
        filtrados = obter_fans_filtrados(localizacao_input, jogo_input)
        if filtrados:
            st.write("Fãs encontrados:", filtrados)
        else:
            st.warning("Nenhum fã encontrado com os filtros aplicados.")

# --- 6. Gráfico adicional fixo (exemplo) ---

with st.expander("📊 Gráfico de Exemplo Fixo"):
    fans_data = [
        {"nome": "Lucas", "jogo_favorito": "League of Legends", "idade": 25},
        {"nome": "Mariana", "jogo_favorito": "Valorant", "idade": 22},
        {"nome": "Carlos", "jogo_favorito": "League of Legends", "idade": 28}
    ]
    df_exemplo = pd.DataFrame(fans_data)
    fig = px.histogram(df_exemplo, x="jogo_favorito", color="idade", title="Idade por Jogo Favorito (Exemplo)")
    st.plotly_chart(fig, use_container_width=True)
