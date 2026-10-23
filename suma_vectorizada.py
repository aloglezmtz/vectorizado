"""Práctica 4: Suma de listas vectorizada con NumPy.
Alumna: Alondra Goretti González Martínez (218534681)
Materia: Programación paralela y recurrente - Mtro. Zeus Cobián

Suma dos arreglos de NumPy con la operación vectorizada a_np + b_np y mide
el tiempo para 100,000, 1,000,000 y 5,000,000 de elementos.

Uso:
    python suma_vectorizada.py
"""
import gc
import statistics
import time

import numpy as np

TAMANOS = [100_000, 1_000_000, 5_000_000]
REPETICIONES = 5          # se reporta la mediana para reducir el ruido


def crear_arreglos(n):
    """Crea dos arreglos de n flotantes aleatorios (misma semilla que el bucle)."""
    rng = np.random.default_rng(42)
    return rng.random(n), rng.random(n)


def suma_vectorizada(a_np, b_np):
    """Suma todos los elementos a la vez; el bucle ocurre dentro de NumPy (en C)."""
    return a_np + b_np


def main():
    print("SUMA VECTORIZADA CON NUMPY (a_np + b_np)")
    print("-" * 46)
    for n in TAMANOS:
        a_np, b_np = crear_arreglos(n)
        tiempos = []
        for _ in range(REPETICIONES):
            gc.collect(); gc.disable()                # sin GC (como timeit)
            t0 = time.perf_counter()              # inicio de la medición
            r = suma_vectorizada(a_np, b_np)
            tiempos.append(time.perf_counter() - t0)
            gc.enable()
        assert np.allclose(r, a_np + b_np)       # verificación rápida
        print(f"N = {n:>9,}  |  tiempo (mediana) = {statistics.median(tiempos):.6f} s")


if __name__ == "__main__":
    main()
