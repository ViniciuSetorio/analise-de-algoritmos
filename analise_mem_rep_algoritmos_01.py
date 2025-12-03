import time
import random
import numpy as np
import matplotlib.pyplot as plt
from memory_profiler import memory_usage


# --- Algoritmos de Ordenação ---
def insertion_sort(lista):
    """
    Algoritmo de Ordenação: Insertion Sort
    """
    for i in range(1, len(lista)):
        j = i
        while j > 0 and lista[j - 1] > lista[j]:
            lista[j - 1], lista[j] = lista[j], lista[j - 1]
            j -= 1


def particion(lista, inicio, fim):
    """Função auxiliar para Quick Sort."""
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


# Definindo uma função wrapper para Quick Sort para facilitar a medição de memória
# sem os argumentos opcionais `inicio` e `fim`.
def quick_sort_wrapper(lista):
    """
    Algoritmo de Ordenação: Quick Sort (Wrapper para medição de memória)
    """
    quick_sort(lista, inicio=0, fim=len(lista) - 1)


def quick_sort(lista, inicio=0, fim=None):
    if fim is None:
        fim = len(lista) - 1
    if inicio < fim:
        p = particion(lista, inicio, fim)
        quick_sort(lista, inicio, p - 1)
        quick_sort(lista, p + 1, fim)


def selection_sort(lista):
    """
    Algoritmo de Ordenação: Selection Sort
    """
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

print(f"Iniciando benchmark de memória com {NUM_EXECUCOES} execuções por tamanho...")

for tamanho in tamanhos:
    print(f"Processando listas de tamanho: {tamanho}")

    memorias_insertion = []
    memorias_quick = []
    memorias_selection = []

    for _ in range(NUM_EXECUCOES):
        array_base = list(np.random.randint(0, tamanho * 10, tamanho))

        # Teste Insertion
        copia_arr = array_base.copy()
        mem_usos = memory_usage((insertion_sort, (copia_arr,)), interval=0.01)
        pico_memoria = max(mem_usos)
        memorias_insertion.append(pico_memoria)

        # Teste Quick
        copia_arr = array_base.copy()
        mem_usos = memory_usage((quick_sort_wrapper, (copia_arr,)), interval=0.01)
        pico_memoria = max(mem_usos)
        memorias_quick.append(pico_memoria)

        # Teste Selection
        copia_arr = array_base.copy()
        mem_usos = memory_usage((selection_sort, (copia_arr,)), interval=0.01)
        pico_memoria = max(mem_usos)
        memorias_selection.append(pico_memoria)

    resultados_medias["Insertion Sort"].append(np.mean(memorias_insertion))
    resultados_medias["Quick Sort"].append(np.mean(memorias_quick))
    resultados_medias["Selection Sort"].append(np.mean(memorias_selection))


# --- Exibição em Gráfico de Colunas (Escala Logarítmica no Eixo Y) ---
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

ax.set_ylabel("Uso de Memória Médio (MiB)")
ax.set_xlabel("Tamanho da Entrada (n)")
ax.set_title(
    f"Pico Médio de Uso de Memória em Escala Logarítmica ({NUM_EXECUCOES} execuções)"
)
ax.set_xticks(x)
ax.set_xticklabels(tamanhos)
ax.legend()

ax.set_yscale("log")

plt.tight_layout()
plt.show()
