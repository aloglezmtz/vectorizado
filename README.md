# Práctica 1 · Uso de hilos (threads) en Python

Programación paralela y recurrente · Universidad de Guadalajara (CUCEI)
Alumna: Alondra Goretti González Martínez · Código 218534681

Suma de los números del 1 al 1,000,000 repartiendo el trabajo entre N hilos y comparación
con la suma secuencial y con la fórmula de Gauss.

## Simulador interactivo

Animación paso a paso del reparto, el cálculo y el `join()` de los hilos:

**https://TU-USUARIO.github.io/practica1-hilos/**

(Reemplaza `TU-USUARIO` por tu usuario de GitHub.)

## Archivos

| Archivo | Descripción |
|---|---|
| `index.html` | Simulador visual (HTML + CSS + JavaScript, sin dependencias) |
| `suma_hilos.py` | Programa de la práctica (hilos vs. secuencial) |
| `benchmark_hilos.py` | Mide tiempos con 1 a 32 hilos (mediana de 7 corridas) |
| `Practica1_Hilos_Gonzalez_Martinez.pdf` | Informe de la práctica |

## Cómo ejecutar el programa

```bash
python suma_hilos.py -n 4
python suma_hilos.py -n 8 --fin 5000000
python benchmark_hilos.py
```

Requiere Python 3.8 o superior; no usa librerías externas.
