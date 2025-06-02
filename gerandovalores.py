import csv
import random

def gerar_e_salvar_csv(nome_arquivo="dados.csv", num_valores=2000):
    valores = []
    for _ in range(num_valores):
        # Gerando valores aleatórios entre 0 e 100
        valores.append(random.uniform(0.0, 100.0))

    try:
        with open(nome_arquivo, 'w', newline='') as arquivo_csv:
            writer = csv.writer(arquivo_csv)
            writer.writerow(valores) # Escreve todos os valores em uma única linha

        print(f"Arquivo '{nome_arquivo}' com {num_valores} valores gerado com sucesso!")
    except IOError as e:
        print(f"Erro ao escrever no arquivo {nome_arquivo}: {e}")

# Exemplo de uso:
if __name__ == "__main__":
    gerar_e_salvar_csv()