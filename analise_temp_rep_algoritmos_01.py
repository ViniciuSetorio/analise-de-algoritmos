import time
import random
import numpy as np
import matplotlib.pyplot as plt

# --- Algoritmos de Ordenação ---
def insertion_sort(lista):
    for i in range(1, len(lista)):
        j = i
        while j > 0 and lista[j - 1] > lista[j]:
            lista[j - 1], lista[j] = lista[j], lista[j - 1]
            j -= 1


def particion(lista, inicio, fim):
    pivo_ind = random.randint(inicio, fim)
    lista[pivo_ind], lista[fim] = lista[fim], lista[pivo_ind]
    pivo = lista[fim]
    i = inicio
    for j in range(inicio, fim):
        if lista[j] <= pivo:
            lista[j], lista[i] = lista[i], lista[j]
            i += 1
    lista[i], lista[fim] = lista[fim], lista[i]
    return i


def quick_sort(lista, inicio=0, fim=None):
    if fim is None:
        fim = len(lista) - 1
    if inicio < fim:
        p = particion(lista, inicio, fim)
        quick_sort(lista, inicio, p - 1)
        quick_sort(lista, p + 1, fim)


def selection_sort(lista):
    for i in range(len(lista) - 1):
        min_ind = i
        for j in range(i + 1, len(lista)):
            if lista[j] < lista[min_ind]:
                min_ind = j
        lista[i], lista[min_ind] = lista[min_ind], lista[i]


# --- Configuração do Experimento ---
tamanhos = [500, 1000, 1500]
NUM_EXECUCOES = 20

resultados_medias = {"Insertion Sort": [], "Quick Sort": [], "Selection Sort": []}

print(f"Iniciando benchmark com {NUM_EXECUCOES} execuções por tamanho...")

for tamanho in tamanhos:
    print(f"Processando listas de tamanho: {tamanho}")

    tempos_insertion = []
    tempos_quick = []
    tempos_selection = []

    for _ in range(NUM_EXECUCOES):
        array_base = np.random.randint(0, tamanho * 10, tamanho)

        # Teste Insertion
        copia_arr = array_base.copy()
        inicio = time.time()
        insertion_sort(copia_arr)
        fim = time.time()
        tempos_insertion.append(fim - inicio)

        # Teste Quick
        copia_arr = array_base.copy()
        inicio = time.time()
        quick_sort(copia_arr)
        fim = time.time()
        tempos_quick.append(fim - inicio)

        # Teste Selection
        copia_arr = array_base.copy()
        inicio = time.time()
        selection_sort(copia_arr)
        fim = time.time()
        tempos_selection.append(fim - inicio)

    # Armazenar e Calcular a média
    resultados_medias["Insertion Sort"].append(np.mean(tempos_insertion))
    resultados_medias["Quick Sort"].append(np.mean(tempos_quick))
    resultados_medias["Selection Sort"].append(np.mean(tempos_selection))


# ---Exibição em Gráfico de Colunas ---
x = np.arange(len(tamanhos)) 
largura = 0.25  

fig, ax = plt.subplots(figsize=(10, 6))

# Criando as barras agrupadas
rects1 = ax.bar(
    x - largura, resultados_medias["Insertion Sort"], largura, label="Insertion Sort"
)
rects2 = ax.bar(x, resultados_medias["Quick Sort"], largura, label="Quick Sort")
rects3 = ax.bar(
    x + largura, resultados_medias["Selection Sort"], largura, label="Selection Sort"
)

ax.set_ylabel("Tempo Médio (segundos)")
ax.set_xlabel("Tamanho da Entrada (n)")
ax.set_title(f"Tempo Médio de Execução ({NUM_EXECUCOES} execuções)")
ax.set_xticks(x)
ax.set_xticklabels(tamanhos)
ax.legend()

ax.yaxis.grid(True, linestyle="--", alpha=0.7)

plt.tight_layout()
plt.show()