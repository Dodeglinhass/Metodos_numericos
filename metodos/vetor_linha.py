"""
Um vetor linha com elementos igualmente espaçados é uma PA
onde o primeiro termo é 4, o último termo é 61 e o número
total de elementos é 16.
"""

primeiro_termo = 4
ultimo_termo = 61
numero_elementos = 16

razao = (ultimo_termo - primeiro_termo) / (numero_elementos - 1)

# função para formatar 
def formatar_vetor(vetor):
    lista_elementos = []
    for x in vetor:
        if x.is_integer():
            lista_elementos.append(str(int(x)))
        else:
            lista_elementos.append(f"{x:.1f}") # mantém 1 casa decimal
    
    vetor_string = f"[{' '.join(lista_elementos)}]"
    return vetor_string

vetor = []
for i in range(numero_elementos):
    valor = primeiro_termo + i * razao
    vetor.append(valor)

novo_vetor = formatar_vetor(vetor)
print(novo_vetor)





