import random
import matplotlib.pyplot as plt
import numpy as np
from memory_profiler import memory_usage

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
    """Fibonacci recursivo O(2^n) - Alto custo de tempo e profundidade de recursão"""
    if n == 0 or n == 1:
        return n

    return fibonacci_recursivo(n - 1) + fibonacci_recursivo(n - 2)


def fibonacci_iterativo(n):
    """Fibonacci iterativo O(n) - Baixo custo de memória e tempo"""
    if n == 0 or n == 1:
        return n

    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


# --- Configurações de Execução ---
NUM_EXECUCOES = 20
tamanhos_busca = [1000, 2000, 3000]
n_fib_termos = [10, 15, 20, 25, 30]

media_busca_linear = []
media_busca_binaria = []
media_fib_iter = []
media_fib_rec = []

print(f"Iniciando testes de uso de memória (Executando {NUM_EXECUCOES} vezes cada caso)...")


def medir_memoria_media(func, args, num_execs):
    """Executa a função N vezes e retorna a média do pico de uso de memória."""
    picos_memoria = []

    # Prepara os dados antes da medição para isolar o consumo do algoritmo
    if func in [busca_linear, busca_binaria]:
        # Para testes de busca
        n = args[0]

        lista_completa = random.sample(range(n * 10), n)
        lista_ordenada = sorted(lista_completa)
        alvo = random.choice(lista_completa)

        args_func = (
            (lista_ordenada, alvo) if func == busca_binaria else (lista_completa, alvo)
        )
    elif func in [fibonacci_iterativo, fibonacci_recursivo]:
        # Para testes de Fibonacci
        args_func = args  # Termo N

    for _ in range(num_execs):
        mem_samples = memory_usage((func, args_func), interval=0.01, timeout=60)
        if mem_samples:
            picos_memoria.append(max(mem_samples))
        else:
            # Adiciona 0 se o timeout for atingido ou ocorrer um erro
            picos_memoria.append(0)

    # Retorna a média apenas se houver medições válidas
    return np.mean(picos_memoria) if picos_memoria else 0


# --- 1. Testes de Busca ---
for n in tamanhos_busca:
    print(f"Testando Busca para N={n}...")

    # 1. Busca Linear
    mem_lin = medir_memoria_media(busca_linear, (n,), NUM_EXECUCOES)
    media_busca_linear.append(mem_lin)

    # 2. Busca Binária
    mem_bin = medir_memoria_media(busca_binaria, (n,), NUM_EXECUCOES)
    media_busca_binaria.append(mem_bin)


# --- 2. Testes de Fibonacci ---
for n in n_fib_termos:
    print(f"Testando Fibonacci para N={n}...")

    # 1. Fibonacci Iterativo
    mem_iter = medir_memoria_media(fibonacci_iterativo, (n,), NUM_EXECUCOES)
    media_fib_iter.append(mem_iter)

    # 2. Fibonacci Recursivo
    mem_rec = medir_memoria_media(fibonacci_recursivo, (n,), NUM_EXECUCOES)
    media_fib_rec.append(mem_rec)


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
    label="Busca Linear (O(n))",
    color="skyblue",
)
plt.bar(
    ind_busca + largura_barra / 2,
    media_busca_binaria,
    width=largura_barra,
    label="Busca Binária (O(log n))",
    color="salmon",
)

plt.xlabel("Tamanho da Lista (N)")
plt.ylabel("Pico Médio de Uso de Memória (MiB)")
plt.title("Uso de Memória: Busca Linear vs Binária (Escala Logarítmica)")
plt.xticks(ind_busca, tamanhos_busca)
plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.7)

plt.yscale("log")

# Gráfico 2: Fibonacci
plt.subplot(1, 2, 2)
ind_fib = np.arange(len(n_fib_termos))

plt.bar(
    ind_fib - largura_barra / 2,
    media_fib_iter,
    width=largura_barra,
    label="Fibonacci Iterativo (O(n))",
    color="lightgreen",
)
plt.bar(
    ind_fib + largura_barra / 2,
    media_fib_rec,
    width=largura_barra,
    label="Fibonacci Recursivo (O(2^n))",
    color="orange",
)

plt.xlabel("Termo de Fibonacci (N)")
plt.ylabel("Pico Médio de Uso de Memória (MiB)")
plt.title("Uso de Memória: Fibonacci Iterativo vs Recursivo (Escala Logarítmica)")
plt.xticks(ind_fib, n_fib_termos)
plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.7)

plt.yscale("log")

plt.tight_layout()
plt.show()
