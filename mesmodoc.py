import math
import csv # Para ler arquivos CSV
import numpy as np # Embora não seja estritamente necessário para o CSV, é bom para operações numéricas se for usar depois

# Definimos o nome do arquivo CSV para ser o mesmo que o gerado anteriormente
FILENAME = "dados.csv"

def calcular_media(dados):
    """
    Calcula a média aritmética de uma lista/array de dados.
    Corresponde à função 'calcular_media' em C.
    """
    if not dados:
        return 0.0
    soma = sum(dados)
    return soma / len(dados)

def calcular_desvio_padrao(dados, media):
    """
    Calcula o desvio padrão de uma lista/array de dados.
    Corresponde à função 'calcular_desvio_padrao' em C.
    """
    if not dados:
        return 0.0
    soma_dif_quad = 0.0
    for x in dados:
        diff = x - media
        soma_dif_quad += diff * diff
    return math.sqrt(soma_dif_quad / len(dados))

def normalizar_zscore(entrada):
    """
    Realiza a normalização Z-score em uma lista/array de dados.
    Corresponde à função 'normalizar_zscore' em C.
    """
    n = len(entrada)
    if n == 0:
        return []

    media = calcular_media(entrada)
    desvio = calcular_desvio_padrao(entrada, media)

    saida = [0.0] * n

    if desvio == 0.0:
        for i in range(n):
            saida[i] = 0.0
    else:
        for i in range(n):
            saida[i] = (entrada[i] - media) / desvio
    
    return saida

def ler_dados_csv(nome_arquivo):
    """
    Lê dados numéricos de um arquivo CSV.
    Assume que os números estão separados por vírgulas em uma ou mais linhas.
    """
    dados = []
    try:
        with open(nome_arquivo, 'r', newline='') as arquivo_csv:
            reader = csv.reader(arquivo_csv)
            for row in reader:
                for item in row:
                    try:
                        # Tenta converter cada item para float
                        dados.append(float(item.strip())) # .strip() para remover espaços em branco
                    except ValueError:
                        print(f"Aviso: Ignorando valor não numérico '{item}' no CSV.")
                        continue # Pula para o próximo item se não for um número
        return dados
    except FileNotFoundError:
        print(f"Erro: O arquivo '{nome_arquivo}' não foi encontrado.")
        return None
    except IOError as e:
        print(f"Erro ao ler o arquivo {nome_arquivo}: {e}")
        return None

def main_python_com_csv():
    """
    Função principal que lê dados de um CSV, normaliza e imprime os resultados.
    """
    # 1. Ler os dados do arquivo CSV
    dados = ler_dados_csv(FILENAME)

    if dados is None or not dados:
        print("Nenhum dado válido foi lido. Encerrando.")
        return

    N = len(dados) # Atualiza N com a quantidade real de dados lidos

    print(f"Lidos {N} valores do arquivo '{FILENAME}'.")

    # 2. Realizar a normalização Z-score
    normalizado = normalizar_zscore(dados)

    # 3. Impressão dos primeiros valores normalizados para teste
    print("\nPrimeiros 10 valores normalizados (Python lendo CSV):")
    for i in range(min(10, N)): # Garante que não tente imprimir mais do que N valores
        print(f"normalizado[{i}] = {normalizado[i]:.6f}")

    # Opcional: imprimir os últimos 10 valores para comparação
    if N > 10:
        print("\nÚltimos 10 valores normalizados (Python lendo CSV):")
        for i in range(max(0, N - 10), N):
            print(f"normalizado[{i}] = {normalizado[i]:.6f}")

    # Opcional: Imprimir média e desvio padrão dos dados normalizados para verificar se estão próximos de 0 e 1
    media_normalizada = calcular_media(normalizado)
    desvio_normalizado = calcular_desvio_padrao(normalizado, media_normalizada)
    print(f"\nMédia dos dados normalizados (Python): {media_normalizada:.6e}")
    print(f"Desvio padrão dos dados normalizados (Python): {desvio_normalizado:.6f}")


if __name__ == "__main__":
    main_python_com_csv()