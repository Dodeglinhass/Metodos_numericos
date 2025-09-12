import math

# --- Valores das variáveis ---
a = 14.75
b = -5.92
c = 61.4
d = -89.232

resultado_etapa1 = (d * (a + c)) / ((25 / a) + (35 / b))
divisor_etapa2 = a + b + c + d
resultado_etapa2 = resultado_etapa1 / divisor_etapa2
expoente = d / 2
valor_exponencial = math.exp(expoente)
euler = d * valor_exponencial
resultado_final = euler + resultado_etapa2

# --- Exibição dos Resultados ---
print(f"Resultado da Etapa 1: {resultado_etapa1}")
print(f"Resultado da Etapa 2: {resultado_etapa2}")
print(f"Expoente (d/2): {expoente}")
print(f"Valor Exponencial (e^(d/2)): {valor_exponencial:e}") # Exibido em notação científica
print(f"Euler (d*e^(d/2)): {euler:e}") # Exibido em notação científica
print("-" * 30)
print(f"Resultado Final (Euler + Etapa 2): {resultado_final:.5f}")