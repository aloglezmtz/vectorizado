"""Práctica 4: Suma de listas con un bucle tradicional (Python puro).
Alumna: Alondra Goretti González Martínez (218534681)
Materia: Programación paralela y recurrente - Mtro. Zeus Cobián

Suma elemento por elemento dos listas usando un bucle for y mide el tiempo
para 100,000, 1,000,000 y 5,000,000 de elementos.

Uso:
    python suma_bucle.py
"""
import gc
import random
import time
import statistics

TAMANOS = [100_000, 1_000_000, 5_000_000]
REPETICIONES = 3          # se reporta la mediana para reducir el ruido


def crear_listas(n):
    """Crea dos listas de n números flotantes aleatorios (semilla fija)."""
    random.seed(42)
    a = [random.random() for _ in range(n)]
    b = [random.random() for _ in range(n)]
    return a, b


def suma_bucle(a, b):
    """Suma a[i] + b[i] con un bucle for tradicional."""
    resultado = []
    for i in range(len(a)):           # el intérprete ejecuta cada iteración
        resultado.append(a[i] + b[i])
    return resultado


def main():
    print("SUMA DE LISTAS CON BUCLE FOR (Python puro)")
    print("-" * 46)
    for n in TAMANOS:
        a, b = crear_listas(n)
        tiempos = []
        for _ in range(REPETICIONES):
            gc.collect(); gc.disable()                # sin GC (como timeit)
            t0 = time.perf_counter()              # inicio de la medición
            r = suma_bucle(a, b)
            tiempos.append(time.perf_counter() - t0)
            gc.enable()
        # Verificación rápida de que la suma es correcta
        assert r[0] == a[0] + b[0] and r[-1] == a[-1] + b[-1]
        print(f"N = {n:>9,}  |  tiempo (mediana) = {statistics.median(tiempos):.4f} s")


if __name__ == "__main__":
    main()
