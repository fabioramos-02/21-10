from bs4 import BeautifulSoup
import requests
from crewai_tools import tool
import pandas as pd
import matplotlib.pyplot as plt

@tool
def check_images_alt_in_page(url: str) -> str:
    """
    A tool to check if images in a page have alt attributes.
    
    Parameters:
    - url: The webpage URL to check.
    
    Returns:
    - A string report indicating which images are missing alt attributes.
    """
    try:
        # Access the webpage
        response = requests.get(url)
        response.raise_for_status()
        
        # Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        images = soup.find_all('img')
        
        # Check for missing alt attributes
        missing_alt = []
        for img in images:
            if not img.get('alt'):
                missing_alt.append(str(img))
        
        # Generate a report
        if missing_alt:
            report = f"Found {len(missing_alt)} images without alt attributes:\n" + "\n".join(missing_alt)
        else:
            report = "All images have alt attributes."
        
        return report
    except requests.RequestException as e:
        return f"Error accessing the page: {e}"
@tool
def generate_bi_report(file_path: str) -> str:
    """
    Gera um relatório de BI com insights dos dados.
    
    Parâmetros:
    - file_path: Caminho para o arquivo CSV contendo os dados.
    
    Retorna:
    - Um relatório com insights em formato de string.
    """
    try:
        # Carregar os dados
        data = pd.read_csv(file_path)
        
        # Resumo estatístico básico dos dados
        summary = data.describe(include='all').to_string()
        
        # Criar gráficos e salvar
        plt.figure(figsize=(10, 6))
        data.hist(bins=20, figsize=(20, 15))
        plt.tight_layout()
        plt.savefig("/mnt/data/bi_report_histogram.png")  # Salvando o gráfico no diretório
        
        # Identificar anomalias (exemplo simples)
        outliers = data[data.apply(lambda x: (x - x.mean()).abs() > 3 * x.std())]
        if outliers.empty:
            outlier_report = "Nenhuma anomalia encontrada."
        else:
            outlier_report = f"Foram encontradas anomalias em {len(outliers)} linhas:\n{outliers.to_string()}"
        
        # Relatório final
        report = f"Resumo Estatístico dos Dados:\n{summary}\n\nRelatório de Anomalias:\n{outlier_report}\n\n"
        report += "Os gráficos foram salvos como bi_report_histogram.png."
        
        return report
    
    except Exception as e:
        return f"Erro ao processar o arquivo: {str(e)}"