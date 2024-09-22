import requests
from bs4 import BeautifulSoup
import pandas as pd
import os


# Função para extrair dados de uma página web e salvar em um arquivo CSV
def extract_web_data_to_csv(url, output_file):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Exemplo: extrair títulos de notícias de uma página (ajuste conforme a estrutura da página)
        titles = soup.find_all('h2')  # Ajuste a tag e a classe conforme necessário

        # Processar os dados em um DataFrame
        data = []
        for title in titles:
            data.append({'Título': title.get_text().strip()})

        df = pd.DataFrame(data)

        # Criar diretório se não existir
        if not os.path.exists('data'):
            os.makedirs('data')

        # Salvar em um arquivo CSV
        output_path = os.path.join('data', output_file)
        df.to_csv(output_path, index=False)
        print(f"Dados salvos em {output_path}")
    else:
        print(f"Falha ao acessar a página. Status code: {response.status_code}")


# Função para extrair dados e salvar em um arquivo TXT
def extract_web_data_to_txt(url, output_file):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Exemplo: extrair parágrafos de uma página (ajuste conforme a estrutura da página)
        paragraphs = soup.find_all('p')

        # Criar diretório se não existir
        if not os.path.exists('data'):
            os.makedirs('data')

        # Escrever os dados em um arquivo TXT
        with open(os.path.join('data', output_file), 'w', encoding='utf-8') as f:
            for para in paragraphs:
                f.write(para.get_text().strip() + '\n')

        print(f"Dados salvos em data/{output_file}")
    else:
        print(f"Falha ao acessar a página. Status code: {response.status_code}")


# Exemplo de uso
url_csv = 'https://reliefweb.int/reports'
url_txt = 'https://reliefweb.int/reports'

# Extração de dados para CSV
extract_web_data_to_csv(url_csv, 'noticias.csv')

# Extração de dados para TXT
extract_web_data_to_txt(url_txt, 'artigos.txt')
