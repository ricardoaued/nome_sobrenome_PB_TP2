import requests
import streamlit as st
import pandas as pd


# Cache para evitar fazer a mesma requisição à API várias vezes
@st.cache_data
def fetch_reliefweb_projects(query="projects", limit=10):
    url = "https://api.reliefweb.int/v1/reports"
    params = {
        "appname": "apidoc",
        "query[value]": query,
        "limit": limit,
        "profile": "full"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()["data"]
    else:
        st.error(f"Erro ao acessar a API da ReliefWeb. Status code: {response.status_code}")
        return []


# Processar dados da API em um DataFrame
def process_project_data(projects):
    project_list = []
    for project in projects:
        title = project['fields'].get('title', 'N/A')
        country = project['fields'].get('primary_country', {}).get('name', 'N/A')
        date = project['fields'].get('date', {}).get('created', 'N/A')
        summary = project['fields'].get('body', 'N/A')
        url = project.get('href', 'N/A')

        project_list.append({
            "Título": title,
            "País": country,
            "Data de Criação": date,
            "Resumo": summary,
            "URL": url
        })

    return pd.DataFrame(project_list)


# Função para fazer upload de um arquivo CSV e ler o conteúdo
def upload_csv():
    uploaded_file = st.file_uploader("Faça upload de um arquivo CSV para adicionar mais informações", type=["csv"])
    if uploaded_file is not None:
        return pd.read_csv(uploaded_file)
    return None


# Função para baixar um DataFrame como CSV
def download_csv(df):
    csv = df.to_csv(index=False)
    st.download_button(
        label="Baixar dados como CSV",
        data=csv,
        file_name="dados_projetos.csv",
        mime="text/csv"
    )


# Inicializar o número de projetos no estado de sessão
if 'num_projects' not in st.session_state:
    st.session_state.num_projects = 5  # Valor inicial padrão

# Controle do número de projetos exibidos
st.write("Escolha o número de projetos a serem exibidos:")
num_projects = st.slider("Número de projetos", min_value=1, max_value=50, value=st.session_state.num_projects)
st.session_state.num_projects = num_projects  # Atualizar o estado

# Carregar dados da API
st.write("Buscando projetos sociais da ReliefWeb API...")
projects = fetch_reliefweb_projects(limit=st.session_state.num_projects)

# Processar dados em um DataFrame
if projects:
    project_df = process_project_data(projects)

    # Permitir upload de arquivo CSV para complementar os dados
    additional_data = upload_csv()

    # Mesclar dados se um arquivo CSV foi enviado
    if additional_data is not None:
        # Mescla os dados do CSV carregado com os dados dos projetos, com base no título
        project_df = pd.merge(project_df, additional_data, on="Título", how="left")
        st.write("Dados adicionais carregados com sucesso!")

    # Opções para escolher quais informações exibir
    st.write("Escolha as informações que deseja visualizar sobre os projetos:")
    columns_to_display = st.multiselect(
        "Selecione os campos:",
        project_df.columns.tolist(),  # Mostra todas as colunas, incluindo as do CSV carregado
        default=["Título", "País", "Data de Criação"]
    )

    # Exibir a tabela com as colunas escolhidas
    if columns_to_display:
        st.dataframe(project_df[columns_to_display])

        # Botão para baixar os dados mostrados como CSV
        download_csv(project_df[columns_to_display])
    else:
        st.write("Nenhuma informação foi selecionada para exibição.")
else:
    st.write("Nenhum projeto encontrado.")

