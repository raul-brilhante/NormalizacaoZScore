import numpy as np
from scipy.stats import zscore
import csv

FILENAME_INPUT = "dados.csv"
FILENAME_OUTPUT = "normalizado_biblioteca.csv" # Novo nome de arquivo de saída

def ler_dados_csv(nome_arquivo):
    """
    Lê dados numéricos de um arquivo CSV.
    Assume que os números estão separados por vírgulas em uma única linha.
    """
    dados_lidos = []
    try:
        with open(nome_arquivo, 'r', newline='') as arquivo_csv:
            reader = csv.reader(arquivo_csv)
            for row in reader:
                for item in row:
                    try:
                        # Tenta converter cada item para float (Python nativo, que é double-precision)
                        dados_lidos.append(float(item.strip()))
                    except ValueError:
                        print(f"Aviso: Ignorando valor não numérico '{item}' no CSV.")
                        continue
        return dados_lidos
    except FileNotFoundError:
        print(f"Erro: O arquivo '{nome_arquivo}' não foi encontrado.")
        return None
    except IOError as e:
        print(f"Erro ao ler o arquivo {nome_arquivo}: {e}")
        return None

def calcular_zscore_com_biblioteca_float(dados):
    """
    Calcula o Z-score de uma lista/array de dados usando a biblioteca scipy.stats,
    forçando a precisão float32 (precisão simples).

    Args:
        dados (list or np.array): Uma lista ou array de números.

    Returns:
        np.array: Um array NumPy contendo os valores normalizados por Z-score (float32).
                  Retorna um array vazio se a entrada for vazia.
    """
    if not dados:
        return np.array([], dtype=np.float64) # Garante que o array vazio também seja float32

    # Converte a lista para um array NumPy, FORÇANDO o tipo de dado para float32
    dados_array = np.array(dados, dtype=np.float64)
    
    # O zscore do scipy.stats vai operar com base no dtype do array de entrada
    return zscore(dados_array)

def salvar_dados_csv(nome_arquivo, dados, casas_decimais=6):
    """
    Salva uma lista/array de dados em um arquivo CSV, em uma única linha,
    formatando cada número para um número específico de casas decimais.
    """
    try:
        with open(nome_arquivo, 'w', newline='') as arquivo_csv:
            writer = csv.writer(arquivo_csv)
            # Converte cada float para string com a formatação desejada antes de escrever
            dados_formatados = [f"{valor:.{casas_decimais}f}" for valor in dados]
            writer.writerow(dados_formatados) # Escreve todos os valores em uma única linha
        print(f"Dados normalizados pela biblioteca (float32, {casas_decimais} decimais) salvos em '{nome_arquivo}' com sucesso!")
    except IOError as e:
        print(f"Erro ao escrever no arquivo {nome_arquivo}: {e}")

if __name__ == "__main__":
    # Garanta que 'dados.csv' foi gerado por 'gerandovalores.py' antes de executar este script.
    print(f"Iniciando a normalização Z-score usando a biblioteca Python (float32) e salvando em '{FILENAME_OUTPUT}'...")

    # 1. Ler os dados originais do arquivo CSV
    dados_originais = ler_dados_csv(FILENAME_INPUT)

    if dados_originais is None or not dados_originais:
        print("Nenhum dado válido foi lido do arquivo de entrada. Por favor, verifique se 'dados.csv' existe e contém números.")
    else:
        # 2. Calcular Z-scores usando a biblioteca scipy.stats com float32
        zscores_calculados = calcular_zscore_com_biblioteca_float(dados_originais)

        # 3. Salvar os Z-scores calculados em um novo arquivo CSV com 6 casas decimais
        salvar_dados_csv(FILENAME_OUTPUT, zscores_calculados, casas_decimais=6)

        # 4. Opcional: Imprimir alguns resultados para verificação rápida
        print("\n--- Amostra dos resultados ---")
        print(f"Número total de valores normalizados: {len(zscores_calculados)}")

        