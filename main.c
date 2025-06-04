#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define MAXIMODOSDADOS 2000

// Calculando a média aritmética
double calcular_media(const double *dados, int n) {
    double soma = 0.0;
    for (int i = 0; i < n; i++) {
        soma += dados[i];
    }
    return soma / n;
}

// Calculando o desvio padrão
double calcular_desvio_padrao(const double *dados, int n, double media) {
    double soma_diferenca_quadrado = 0.0;
    for (int i = 0; i < n; i++) {
        double diff = dados[i] - media;
        soma_diferenca_quadrado += diff * diff;
    }
    return sqrt(soma_diferenca_quadrado / n);
}

// Faz a normalização z score
void normalizar_zscore(const double *entrada, double *saida, int n) {
    double media = calcular_media(entrada, n);
    double desvio = calcular_desvio_padrao(entrada, n, media);

    if (desvio == 0.0) {
        for (int i = 0; i < n; i++) {
            saida[i] = 0.0;
        }
    } else {
        for (int i = 0; i < n; i++) {
            saida[i] = (entrada[i] - media) / desvio;
        }
    }
}

int main() {
    double dados[MAXIMODOSDADOS];
    double normalizado[MAXIMODOSDADOS]; // vetor de saída
    FILE *arquivo_entrada;
    FILE *arquivo_saida;
    int i = 0;
    double valor_temporario; // para armazenar o valor lido
    int valores_lidos = 0;

    // Abre o arquivo para leitura
    arquivo_entrada = fopen("dados.csv", "r");

    // Testando se o arquivo abriu de boas
    if (arquivo_entrada == NULL) {
        perror("Erro ao abrir o arquivo");
        return EXIT_FAILURE;
    }

    // Ler o CSV
    while (valores_lidos < MAXIMODOSDADOS && fscanf(arquivo_entrada, "%lf", &valor_temporario) == 1) {
        dados[valores_lidos] = valor_temporario;
        valores_lidos++;
        int c;
        while ((c = fgetc(arquivo_entrada)) != EOF && (c == ',' || c == ' ' || c == '\n' || c == '\r')) {
        }
        if (c != EOF) ungetc(c, arquivo_entrada);
    }

    fclose(arquivo_entrada);

    // Fazendo normalização Z-score com os dados lidos
    normalizar_zscore(dados, normalizado, valores_lidos);

    // Abrindo o arquivo de saida
    arquivo_saida = fopen("normalizados.csv", "w");

    // Testando se o arquivo de saída abriu de boas
    if (arquivo_saida == NULL) {
        perror("Erro ao abrir o arquivo de saída");
        return EXIT_FAILURE;
    }

    // Escrevendo os valores normalizados no arquivo CSV de saida
    for (i = 0; i < valores_lidos; i++) {
        fprintf(arquivo_saida, "%lf", normalizado[i]);
        if (i < valores_lidos - 1) fprintf(arquivo_saida, ",");
    }
    fprintf(arquivo_saida, "\n"); //Quebra de linha no final

    fclose(arquivo_saida);

    printf("Resultados normalizados salvos em '%s'.\n", "normalizados.csv");

    return 0;
}