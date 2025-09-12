import json
import os
import numpy as np
import matplotlib.pyplot as plt

# Nome do arquivo para salvar a matriz
ARQUIVO_MATRIZ = "matriz_armazenada.json"


# Função para formatar número com 6 algarismos significativos
def formatar_significativos(numero):
    return f"{numero:.6g}"


# Função para exibir a matriz no console
def exibir_matriz(matriz):
    print("\nMatriz armazenada (com 6 algarismos significativos):")
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            print(formatar_significativos(matriz[i][j]), end="\t")
        print()  # Nova linha após cada linha da matriz


# Função para plotar a matriz como um heatmap
def plotar_matriz(matriz):
    if not matriz:
        print("Não há matriz para plotar.")
        return

    # Converte a matriz para array NumPy
    matriz_np = np.array(matriz)
    linhas, colunas = matriz_np.shape

    # Cria a figura
    plt.figure(figsize=(max(6, colunas * 0.8), max(4, linhas * 0.8)))
    heatmap = plt.imshow(matriz_np, cmap='viridis', interpolation='nearest')

    # Adiciona os valores da matriz em cada célula
    for i in range(linhas):
        for j in range(colunas):
            plt.text(j, i, formatar_significativos(matriz_np[i, j]),
                     ha='center', va='center', color='white' if matriz_np[i, j] < np.mean(matriz_np) else 'black')

    # Configurações de formatação
    plt.title('Matriz Armazenada', fontsize=14, pad=15)
    plt.xlabel('Colunas', fontsize=12)
    plt.ylabel('Linhas', fontsize=12)
    plt.colorbar(heatmap, label='Valores')
    plt.xticks(np.arange(colunas), np.arange(1, colunas + 1))
    plt.yticks(np.arange(linhas), np.arange(1, linhas + 1))
    plt.tight_layout()
    plt.show()


# Função para carregar a matriz do arquivo
def carregar_matriz():
    if os.path.exists(ARQUIVO_MATRIZ):
        try:
            with open(ARQUIVO_MATRIZ, 'r') as arquivo:
                return json.load(arquivo)
        except json.JSONDecodeError:
            print("Erro ao carregar o arquivo. Iniciando com matriz vazia.")
            return []
    return []


# Função para salvar a matriz no arquivo
def salvar_matriz(matriz):
    with open(ARQUIVO_MATRIZ, 'w') as arquivo:
        json.dump(matriz, arquivo)


# Carrega a matriz armazenada ao iniciar o programa
matriz_armazenada = carregar_matriz()

while True:
    # Pergunta se deseja inserir uma nova matriz
    resposta = input("\nDeseja inserir uma nova matriz? (sim/não): ").strip().lower()

    if resposta == "sim":
        # Solicita dimensões da nova matriz
        try:
            linhas = int(input("Digite o número de linhas da matriz: "))
            colunas = int(input("Digite o número de colunas da matriz: "))
        except ValueError:
            print("Erro: Digite números inteiros válidos para linhas e colunas.")
            continue

        # Inicializa a nova matriz vazia
        matriz_armazenada = []

        # Solicita os elementos da matriz
        print("Digite os elementos da matriz:")
        for i in range(linhas):
            linha = []
            for j in range(colunas):
                try:
                    elemento = float(input(f"Elemento [{i + 1}][{j + 1}]: "))
                    linha.append(elemento)
                except ValueError:
                    print("Erro: Digite um número válido.")
                    linha = []  # Reseta a linha se houver erro
                    break
            if linha:  # Só adiciona a linha se não houve erro
                matriz_armazenada.append(linha)
            else:
                matriz_armazenada = []  # Reseta a matriz se houve erro
                break

        if matriz_armazenada:  # Só salva e exibe se a matriz foi preenchida corretamente
            # Salva a nova matriz no arquivo
            salvar_matriz(matriz_armazenada)
            # Exibe a matriz recém-inserida
            exibir_matriz(matriz_armazenada)
            # Plota a matriz
            plotar_matriz(matriz_armazenada)

    elif resposta == "não":
        # Verifica se há uma matriz armazenada
        if matriz_armazenada:
            exibir_matriz(matriz_armazenada)
            # Plota a matriz
            plotar_matriz(matriz_armazenada)
        else:
            print("\nNenhuma matriz foi armazenada ainda.")
    else:
        print("\nResposta inválida. Digite 'sim' ou 'não'.")

    # Pergunta se deseja continuar
    continuar = input("\nDeseja continuar? (sim/não): ").strip().lower()
    if continuar != "sim":
        print("Programa encerrado.")
        break