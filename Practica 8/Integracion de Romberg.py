import numpy as np
import math


def f(x, expr):
    return eval(expr, {'np': np, 'math': math, 'x': x})


def evaluate_limit(limit_str):
    """Evalúa expresiones como 'math.pi/4' en los límites."""
    return eval(limit_str, {'math': math, 'np': np})


def romberg_integral(expr, a, b, max_iter=10, tol=None):
    R = np.zeros((max_iter + 1, max_iter + 1))
    h = b - a

    # Iteración inicial (trapecio simple)
    R[0, 0] = (h / 2) * (f(a, expr) + f(b, expr))
    print(f"\n=== Iteración 0 ===")
    print(f"R[0, 0] = {R[0, 0]:.10f}")

    for i in range(1, max_iter + 1):
        h /= 2
        # Regla del trapecio compuesto
        sumatoria = sum(f(a + (2 * k - 1) * h, expr) for k in range(1, 2 ** (i - 1) + 1))
        R[i, 0] = 0.5 * R[i - 1, 0] + h * sumatoria

        # Extrapolación de Richardson
        for j in range(1, i + 1):
            R[i, j] = R[i, j - 1] + (R[i, j - 1] - R[i - 1, j - 1]) / (4 ** j - 1)

        # Mostrar resultados
        print(f"\n=== Iteración {i} ===")
        for j in range(i + 1):
            print(f"R[{i},{j}] = {R[i, j]:.10f}")

        # Verificar convergencia
        if tol and abs(R[i, i] - R[i - 1, i - 1]) < tol:
            print(f"\n¡Convergencia alcanzada en iteración {i}!")
            print(f"Resultado final: R[{i},{i}] = {R[i, i]:.12f}")
            return R[i, i]

    print(f"\nResultado final (sin convergencia): R[{max_iter},{max_iter}] = {R[max_iter, max_iter]:.12f}")
    return R[max_iter, max_iter]


def main():
    print("=== INTEGRACIÓN DE ROMBERG ===")
    expr = input("Ingresa la función f(x) (ej: 'x**2 * math.sin(x)'): ")

    # Procesar límites con expresiones matemáticas
    a_str = input("Límite inferior (a, ej: '0' o 'math.pi/4'): ")
    a = evaluate_limit(a_str)

    b_str = input("Límite superior (b, ej: '1.5' o 'math.pi/2'): ")
    b = evaluate_limit(b_str)

    max_iter = int(input("Máximo de iteraciones (n): "))
    tol_input = input("Tolerancia (opcional, ej: 1e-6): ")
    tol = float(tol_input) if tol_input else None

    romberg_integral(expr, a, b, max_iter, tol)


if __name__ == "__main__":
    main()