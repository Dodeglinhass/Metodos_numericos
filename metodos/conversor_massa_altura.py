# Criação da função conforme pedido no enunciado 
def SIparaIng(cm, kg):

    # fatores de conversão
    cm_para_pol = 0.393701
    kg_para_lib = 2.20462

    pol = cm * cm_para_pol
    lib = kg * kg_para_lib

    return pol, lib

# Exemplo do enunciado
massa_kg = 85
altura_cm = 178

pol, lib = SIparaIng(altura_cm, massa_kg)

print(f"Altura: {pol:.2f} polegadas")
print(f"Massa: {lib:.2f} libras")