"""Benchmark complementario: mide el tiempo (mediana de varias repeticiones)
de la suma con N hilos frente a la suma secuencial.
Uso: python benchmark_hilos.py
"""
import json
import statistics
import time

from suma_hilos import suma_con_hilos, suma_secuencial

INICIO, FIN = 1, 1_000_000
REPETICIONES = 7
VALORES_N = [1, 2, 4, 8, 16, 32]


def medir(funcion, *args):
    tiempos = []
    for _ in range(REPETICIONES):
        t0 = time.perf_counter()
        funcion(*args)
        tiempos.append(time.perf_counter() - t0)
    return statistics.median(tiempos), min(tiempos), max(tiempos)


if __name__ == "__main__":
    resultados = {"secuencial": medir(suma_secuencial, INICIO, FIN), "hilos": {}}
    for n in VALORES_N:
        resultados["hilos"][n] = medir(suma_con_hilos, INICIO, FIN, n)
        print(f"N={n:>2} mediana={resultados['hilos'][n][0]:.4f} s")
    print(f"Secuencial mediana={resultados['secuencial'][0]:.4f} s")
    with open("benchmark.json", "w") as f:
        json.dump(resultados, f)
