import time
import random
import matplotlib.pyplot as plt
import numpy as np

# --- Definição dos Algoritmos ---
def busca_linear(lista, elem):
    """Busca linear O(n)"""
    for i in range(len(lista)):
        if lista[i] == elem:
            return i
    return None


def busca_binaria(lista, elem, ind_in=0, ind_fim=None):
    """Busca binária O(log n)"""
    if ind_fim is None:
        ind_fim = len(lista) - 1

    if ind_in <= ind_fim:
        meio = (ind_in + ind_fim) // 2

        if lista[meio] == elem:
            return meio
        elif elem < lista[meio]:
            return busca_binaria(lista, elem, ind_in, meio - 1)
        else:
            return busca_binaria(lista, elem, meio + 1, ind_fim)
    return None


def fibonacci_recursivo(n):
    """Fibonacci recursivo O(2^n)"""
    if n == 0 or n == 1:
        return n
    return fibonacci_recursivo(n - 1) + fibonacci_recursivo(n - 2)


def fibonacci_iterativo(n):
    """Fibonacci iterativo O(n)"""
    if n == 0 or n == 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


NUM_EXECUCOES = 20  
tamanhos_busca = [1000, 2000, 3000, 4000, 5000]  
n_fib_termos = [5, 10, 15, 20, 25]  

media_busca_linear = []
media_busca_binaria = []
media_fib_iter = []
media_fib_rec = []

print(f"Iniciando testes (Executando {NUM_EXECUCOES} vezes cada caso)...")

# --- 1. Testes de Busca ---
for n in tamanhos_busca:
    tempos_lin_temp = []
    tempos_bin_temp = []

    for _ in range(NUM_EXECUCOES):
        lista = random.sample(range(n * 10), n)
        lista_ordenada = sorted(lista)
        alvo = random.choice(lista)

        # Linear
        inicio = time.perf_counter()
        busca_linear(lista, alvo)
        fim = time.perf_counter()
        tempos_lin_temp.append(fim - inicio)

        # Binária
        inicio = time.perf_counter()
        busca_binaria(lista_ordenada, alvo)
        fim = time.perf_counter()
        tempos_bin_temp.append(fim - inicio)

    # Calcula a média
    media_busca_linear.append(np.mean(tempos_lin_temp))
    media_busca_binaria.append(np.mean(tempos_bin_temp))

# --- 2. Testes de Fibonacci ---
for n in n_fib_termos:
    tempos_iter_temp = []
    tempos_rec_temp = []

    for _ in range(NUM_EXECUCOES):
        # Iterativo
        inicio = time.perf_counter()
        fibonacci_iterativo(n)
        fim = time.perf_counter()
        tempos_iter_temp.append(fim - inicio)

        # Recursivo
        inicio = time.perf_counter()
        fibonacci_recursivo(n)
        fim = time.perf_counter()
        tempos_rec_temp.append(fim - inicio)

    # Calcula a média
    media_fib_iter.append(np.mean(tempos_iter_temp))
    media_fib_rec.append(np.mean(tempos_rec_temp))

print("Testes concluídos. Gerando gráficos...")

plt.figure(figsize=(14, 6))

largura_barra = 0.35

# Gráfico 1: Busca
plt.subplot(1, 2, 1)
ind_busca = np.arange(len(tamanhos_busca)) 

plt.bar(
    ind_busca - largura_barra / 2,
    media_busca_linear,
    width=largura_barra,
    label="Busca Linear",
    color="skyblue",
)
plt.bar(
    ind_busca + largura_barra / 2,
    media_busca_binaria,
    width=largura_barra,
    label="Busca Binária",
    color="salmon",
)

plt.xlabel("Tamanho da Lista (N)")
plt.ylabel("Tempo Médio (s)")
plt.title("Média de Tempo: Busca Linear vs Binária")
plt.xticks(ind_busca, tamanhos_busca)  
plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.7)

# Gráfico 2: Fibonacci
plt.subplot(1, 2, 2)
ind_fib = np.arange(len(n_fib_termos))

plt.bar(
    ind_fib - largura_barra / 2,
    media_fib_iter,
    width=largura_barra,
    label="Fibonacci Iterativo",
    color="lightgreen",
)
plt.bar(
    ind_fib + largura_barra / 2,
    media_fib_rec,
    width=largura_barra,
    label="Fibonacci Recursivo",
    color="orange",
)

plt.xlabel("Termo de Fibonacci (N)")
plt.ylabel("Tempo Médio (s)")
plt.title("Média de Tempo: Fibonacci Iterativo vs Recursivo")
plt.xticks(ind_fib, n_fib_termos)
plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.7)

plt.yscale("log")
plt.text(
    0,
    -0.15,
    "*Eixo Y em escala logarítmica para visualização",
    transform=plt.gca().transAxes,
    fontsize=9,
)

plt.tight_layout()
plt.show()
