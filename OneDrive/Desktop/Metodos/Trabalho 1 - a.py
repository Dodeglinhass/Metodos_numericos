import math

# --- Valores Definidos  ---
a = 14.75
b = -5.92
c = 61.4
d = -89.232

numerador = a * b * (a + d)**2
denominador = c * math.sqrt(abs(a * b))
resultado_fracao = numerador / denominador
resultado_final_com_a = a + resultado_fracao

# --- Exibição do Resultado Final ---
print(f"--- Cálculo Final da Expressão: a + [ab(a+d)² / c√|ab|] ---")
print(f"Valor da fração [ab(a+d)² / c√|ab|]: {resultado_fracao}")
print(f"Valor de 'a': {a}")
print("-" * 30)
print(f"Resultado Final (a + fração): {resultado_final_com_a:.5f}") # Formatado para 5 casas decimais