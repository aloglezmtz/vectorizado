"""Práctica 1: Uso de hilos (threads) en Python.
Alumna: Alondra Goretti González Martínez (218534681)
Materia: Programación paralela y recurrente - Mtro. Zeus Cobián

Suma de los números de un rango [inicio, fin] de dos formas:
  1) En paralelo, dividiendo el rango entre N hilos.
  2) De forma secuencial (sin hilos).
Después compara ambos resultados.

Uso:
    python suma_hilos.py                    # pide N por teclado (rango 1..1,000,000)
    python suma_hilos.py -n 4               # 4 hilos
    python suma_hilos.py -n 8 --fin 5000000 # 8 hilos, rango 1..5,000,000
"""
import argparse
import threading
import time


def dividir_rango(inicio, fin, n_hilos):
    """Divide [inicio, fin] en n_hilos subrangos contiguos y casi iguales.

    Si la cantidad de números no es divisible entre n_hilos, los primeros
    'residuo' hilos reciben un número extra, así no se pierde ningún valor.
    """
    total = fin - inicio + 1
    base, residuo = divmod(total, n_hilos)
    rangos = []
    actual = inicio
    for i in range(n_hilos):
        tamano = base + (1 if i < residuo else 0)
        rangos.append((actual, actual + tamano - 1))
        actual += tamano
    return rangos


def suma_parcial(indice, inicio, fin, resultados):
    """Trabajo de cada hilo: suma los enteros de [inicio, fin].

    Cada hilo escribe solo en su propia posición de 'resultados', por lo que
    no hay condición de carrera y no se necesita un candado (Lock).
    """
    acumulado = 0
    for numero in range(inicio, fin + 1):
        acumulado += numero
    resultados[indice] = acumulado


def suma_con_hilos(inicio, fin, n_hilos):
    """Suma el rango usando n_hilos hilos. Devuelve (suma, rangos, parciales)."""
    rangos = dividir_rango(inicio, fin, n_hilos)
    resultados = [0] * n_hilos
    hilos = []

    for i, (ini, fi) in enumerate(rangos):
        hilo = threading.Thread(target=suma_parcial, args=(i, ini, fi, resultados))
        hilos.append(hilo)
        hilo.start()

    # El hilo principal espera a que todos terminen
    for hilo in hilos:
        hilo.join()

    return sum(resultados), rangos, resultados


def suma_secuencial(inicio, fin):
    """Suma el rango en un solo flujo de ejecución (sin hilos)."""
    acumulado = 0
    for numero in range(inicio, fin + 1):
        acumulado += numero
    return acumulado


def leer_argumentos():
    parser = argparse.ArgumentParser(description="Suma de un rango con hilos vs secuencial")
    parser.add_argument("-n", "--hilos", type=int, help="número de hilos (N)")
    parser.add_argument("--inicio", type=int, default=1, help="inicio del rango (default 1)")
    parser.add_argument("--fin", type=int, default=1_000_000, help="fin del rango (default 1,000,000)")
    args = parser.parse_args()

    if args.hilos is None:
        try:
            args.hilos = int(input("Número de hilos (N): "))
        except ValueError:
            parser.error("N debe ser un entero")

    if args.hilos < 1:
        parser.error("N debe ser mayor o igual a 1")
    if args.fin < args.inicio:
        parser.error("--fin debe ser mayor o igual a --inicio")
    if args.hilos > args.fin - args.inicio + 1:
        parser.error("N no puede ser mayor que la cantidad de números del rango")
    return args


def main():
    args = leer_argumentos()

    print(f"Rango: {args.inicio:,} a {args.fin:,}  |  Hilos (N): {args.hilos}\n")

    # --- Suma con hilos ---
    t0 = time.perf_counter()
    total_hilos, rangos, parciales = suma_con_hilos(args.inicio, args.fin, args.hilos)
    t_hilos = time.perf_counter() - t0

    for i, ((ini, fi), parcial) in enumerate(zip(rangos, parciales), start=1):
        print(f"Hilo {i:>2}: [{ini:>9,} - {fi:>9,}]  suma parcial = {parcial:,}")

    # --- Suma secuencial ---
    t0 = time.perf_counter()
    total_sec = suma_secuencial(args.inicio, args.fin)
    t_sec = time.perf_counter() - t0

    # --- Verificación extra con la fórmula de Gauss ---
    n = args.fin - args.inicio + 1
    total_formula = (args.inicio + args.fin) * n // 2

    print("\n" + "=" * 60)
    print(f"Suma con {args.hilos} hilo(s): {total_hilos:,}   ({t_hilos:.4f} s)")
    print(f"Suma secuencial   : {total_sec:,}   ({t_sec:.4f} s)")
    print(f"Fórmula de Gauss  : {total_formula:,}")
    print("=" * 60)

    if total_hilos == total_sec == total_formula:
        print("RESULTADO: los tres valores COINCIDEN.")
    else:
        print("RESULTADO: los valores NO coinciden (revisar el programa).")


if __name__ == "__main__":
    main()
