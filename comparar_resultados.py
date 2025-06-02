import csv
import numpy as np

# Nomes dos arquivos CSV a serem comparados
FILE_C_OUTPUT = "normalizados.csv"         # Saída do seu programa C
FILE_PYTHON_LIB_OUTPUT = "normalizado_biblioteca.csv" # Saída do script Python com a biblioteca

# Tolerância para comparação de ponto flutuante (um valor pequeno, e.g., 1e-6 ou 1e-9)
TOLERANCIA = 1e-6 # 0.000001 - Ajuste conforme a precisão esperada

def ler_dados_csv(nome_arquivo):
    """
    Lê dados numéricos de um arquivo CSV, assumindo que estão em uma única linha,
    separados por vírgulas.
    """
    dados = []
    try:
        with open(nome_arquivo, 'r', newline='') as arquivo_csv:
            reader = csv.reader(arquivo_csv)
            for row in reader:
                for item in row:
                    try:
                        dados.append(float(item.strip()))
                    except ValueError:
                        print(f"Aviso: Ignorando valor não numérico '{item}' em '{nome_arquivo}'.")
                        continue
        return dados
    except FileNotFoundError:
        print(f"Erro: O arquivo '{nome_arquivo}' não foi encontrado.")
        return None
    except IOError as e:
        print(f"Erro ao ler o arquivo {nome_arquivo}: {e}")
        return None

def comparar_normalizacoes(dados_c, dados_python_lib, tolerancia):
    """
    Compara duas listas de dados normalizados, verificando se são "quase" iguais.
    """
    if dados_c is None or dados_python_lib is None:
        print("Erro: Uma das listas de dados é nula. Não é possível comparar.")
        return False

    len_c = len(dados_c)
    len_python = len(dados_python_lib)

    if len_c != len_python:
        print(f"Diferença no número de valores: C ({len_c}), Python ({len_python}).")
        return False

    diferencas_encontradas = 0
    primeiras_diferencas = []
    for i in range(len_c):
        diff_completo = abs(dados_c[i]) - abs(dados_python_lib[i])
        diff = round(diff_completo, 6)
        if diff > tolerancia:
            diferencas_encontradas += 1
            if len(primeiras_diferencas) < 5: # Registra as primeiras 5 diferenças para análise
                primeiras_diferencas.append({
                    "indice": i,
                    "valor_c": dados_c[i],
                    "valor_python": dados_python_lib[i],
                    "diferenca": diff
                })
    
    if diferencas_encontradas == 0:
        print(f"\nRESULTADO: Os dados normalizados são considerados IGUAIS (dentro da tolerância de {tolerancia}).")
        return True
    else:
        print(f"\nRESULTADO: Foram encontradas {diferencas_encontradas} diferenças maiores que a tolerância de {tolerancia}.")
        print("\nPrimeiras diferenças encontradas:")
        for diff_info in primeiras_diferencas:
            print(f"Índice: {diff_info['indice']}")
            print(f"  Valor C:       {diff_info['valor_c']:.6f}")
            print(f"  Valor Python:  {diff_info['valor_python']:.6f}")
            print(f"  Diferença:     {diff_info['diferenca']:.6f}\n")
        return False

if __name__ == "__main__":
    print(f"Iniciando a comparação entre '{FILE_C_OUTPUT}' e '{FILE_PYTHON_LIB_OUTPUT}'...")

    # 1. Ler os dados do arquivo gerado pelo programa C
    dados_c = ler_dados_csv(FILE_C_OUTPUT)

    # 2. Ler os dados do arquivo gerado pelo script Python com a biblioteca
    dados_python_lib = ler_dados_csv(FILE_PYTHON_LIB_OUTPUT)

    if dados_c is None or dados_python_lib is None:
        print("Não foi possível carregar ambos os arquivos para comparação. Verifique os erros acima.")
    else:
        # 3. Comparar os dados normalizados
        comparar_normalizacoes(dados_c, dados_python_lib, TOLERANCIA)