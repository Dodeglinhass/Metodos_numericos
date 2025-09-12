import json
import os
import numpy as np
import matplotlib.pyplot as plt
import re

# Nome do arquivo para salvar os dados
ARQUIVO_DADOS = "dados_armazenados.json"


# Função para formatar número com 6 algarismos significativos
def formatar_significativos(numero):
    return f"{numero:.6g}"


# Função para carregar e validar os dados do arquivo
def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):
        try:
            with open(ARQUIVO_DADOS, 'r') as arquivo:
                dados = json.load(arquivo)
            # Validação do conteúdo
            if not isinstance(dados, dict):
                print("Erro: Arquivo JSON não contém um dicionário válido.")
                return {}
            if 'escalar' not in dados or 'vetor' not in dados or 'funcao' not in dados:
                print("Erro: Dados incompletos no arquivo JSON (falta escalar, vetor ou função).")
                return {}
            if not dados['vetor'] or not all(isinstance(x, (int, float)) for x in dados['vetor']):
                print("Erro: Vetor inválido ou vazio no arquivo JSON.")
                return {}
            if 'numerador' not in dados['funcao'] or 'tem_denominador' not in dados['funcao']:
                print("Erro: Dados da função incompletos no arquivo JSON.")
                return {}
            # Revalida a função
            valido, _, _ = validar_e_avaliar_funcao(
                dados['funcao']['numerador'],
                dados['funcao'].get('denominador', '1'),
                x_teste=dados['vetor'][0],
                a_teste=dados['escalar'],
                tem_denominador=dados['funcao']['tem_denominador']
            )
            if not valido:
                print("Erro: Função armazenada é inválida.")
                return {}
            return dados
        except json.JSONDecodeError:
            print("Erro ao carregar o arquivo. Iniciando com dados vazios.")
            return {}
    return {}


# Função para salvar os dados no arquivo
def salvar_dados(dados):
    with open(ARQUIVO_DADOS, 'w') as arquivo:
        json.dump(dados, arquivo)


# Função para exibir os dados armazenados
def exibir_dados(dados):
    if dados:
        print("\nDados armazenados:")
        print(f"Escalar a: {formatar_significativos(dados['escalar'])}")
        print(f"Vetor x_i: {[formatar_significativos(x) for x in dados['vetor']]}")
        print(f"Função y = f(x): {dados['funcao']['numerador']}", end="")
        if dados['funcao']['tem_denominador']:
            print(f" / ({dados['funcao']['denominador']})")
        else:
            print()
    else:
        print("\nNenhum dado foi armazenado ainda.")


# Função para inserir operador * entre número e variável
def corrigir_expressao(expr):
    expr = expr.replace('^', '**').strip()
    expr = re.sub(r'(\d+)([a-zA-Z])', r'\1*\2', expr)
    expr = re.sub(r'(\d+)([a-zA-Z])\*\*', r'\1*\2**', expr)
    expr = re.sub(r'\s*([+\-*/])\s*', r'\1', expr)
    return expr


# Função para validar e avaliar a função com segurança
def validar_e_avaliar_funcao(numerador, denominador, x_teste=0, a_teste=1, tem_denominador=False):
    try:
        numerador = corrigir_expressao(numerador)
        if tem_denominador:
            denominador = corrigir_expressao(denominador)
            expr = f"({numerador})/({denominador})"
        else:
            expr = f"({numerador})"

        compiled_expr = compile(expr, '<string>', 'eval')
        eval(compiled_expr, {"__builtins__": {}, "np": np}, {"x": x_teste, "a": a_teste})

        print("Função validada com sucesso!")
        return True, expr, compiled_expr
    except SyntaxError as e:
        print(f"Erro de sintaxe na expressão '{expr}': {e}")
        print(
            "Dicas: Verifique parênteses balanceados, operadores corretos (use * para multiplicação, ** para potência). Exemplo: '2*a*x**2 + 1'")
        return False, None, None
    except Exception as e:
        print(f"Erro ao validar/avaliar a função: {e}")
        print("Dicas: Evite divisão por zero no teste; verifique se usa 'x' e/ou 'a' corretamente.")
        return False, None, None


# Função para avaliar a função em um array x
def avaliar_funcao(compiled_expr, x, a):
    try:
        return np.array([eval(compiled_expr, {"__builtins__": {}, "np": np}, {"x": xi, "a": a}) for xi in x])
    except Exception as e:
        print(f"Erro ao avaliar a função no gráfico: {e}")
        return None


# Função para plotar o gráfico
def plotar_grafico(vetor, numerador, denominador, tem_denominador, escalar):
    try:
        numerador = corrigir_expressao(numerador)
        if tem_denominador:
            denominador = corrigir_expressao(denominador)
            expr = f"({numerador})/({denominador})"
        else:
            expr = f"({numerador})"

        compiled_expr = compile(expr, '<string>', 'eval')
        x = np.array(vetor)
        y = avaliar_funcao(compiled_expr, x, escalar)
        if y is None:
            return

        plt.figure(figsize=(10, 6))
        plt.plot(x, y, 'bo-', label=f"y = {numerador}" + (f"/({denominador})" if tem_denominador else ""))
        plt.xlabel('x', fontsize=12)
        plt.ylabel('y', fontsize=12)
        plt.title('Gráfico da Função y = f(x)', fontsize=14)
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"Erro ao plotar o gráfico: {e}")


# Carrega os dados armazenados ao iniciar o programa
dados_armazenados = carregar_dados()

while True:
    # Pergunta se deseja inserir novos dados
    resposta = input("\nDeseja inserir novos dados? (sim/não): ").strip().lower()

    if resposta == "sim":
        dados = {}
        try:
            # Solicita o escalar
            dados['escalar'] = float(input("Digite o escalar a: "))

            # Pergunta como alimentar o vetor
            metodo_vetor = input(
                "Deseja inserir o vetor x_i manualmente ou por intervalo? (manual/intervalo): ").strip().lower()
            vetor = []
            if metodo_vetor == "intervalo":
                try:
                    inicio = float(input("Digite o valor inicial do intervalo: "))
                    fim = float(input("Digite o valor final do intervalo: "))
                    incremento = float(input("Digite o incremento: "))
                    if incremento <= 0:
                        print("Erro: O incremento deve ser positivo.")
                        continue
                    if inicio > fim:
                        print("Erro: O valor inicial deve ser menor ou igual ao valor final.")
                        continue
                    vetor = np.arange(inicio, fim + incremento, incremento).tolist()
                    if not vetor:
                        print("Erro: O intervalo gerou um vetor vazio.")
                        continue
                except ValueError:
                    print("Erro: Digite números válidos para o intervalo e incremento.")
                    continue
            elif metodo_vetor == "manual":
                n = int(input("Digite o número de elementos do vetor x_i: "))
                print("Digite os elementos do vetor x_i:")
                for i in range(n):
                    try:
                        elemento = float(input(f"Elemento x_{i + 1}: "))
                        vetor.append(elemento)
                    except ValueError:
                        print("Erro: Digite um número válido.")
                        vetor = []
                        break
            else:
                print("Erro: Escolha 'manual' ou 'intervalo'.")
                continue

            if not vetor:
                continue
            dados['vetor'] = vetor

            # Solicita informações sobre a função
            dados['funcao'] = {}
            tem_denominador = input("A função possui denominador? (sim/não): ").strip().lower() == "sim"
            dados['funcao']['tem_denominador'] = tem_denominador
            usar_vetor = input("A função deve usar as variáveis do vetor x_i? (sim/não): ").strip().lower() == "sim"
            usar_escalar = input("A função deve usar o escalar a? (sim/não): ").strip().lower() == "sim"

            # Validação inicial de uso de variáveis
            if not usar_vetor and not usar_escalar:
                print("Erro: A função deve usar pelo menos o vetor x_i ('x') ou o escalar a ('a').")
                continue

            # Loop para inserção e validação da função
            while True:
                numerador = input("Digite o numerador da função (use 'x' para variável e 'a' para escalar): ").strip()
                dados['funcao']['numerador'] = numerador
                denominador = "1"
                if tem_denominador:
                    denominador = input(
                        "Digite o denominador da função (use 'x' para variável e 'a' para escalar): ").strip()
                    dados['funcao']['denominador'] = denominador
                else:
                    dados['funcao']['denominador'] = ""

                # Valida a função
                valido, expr, compiled_expr = validar_e_avaliar_funcao(numerador, denominador, vetor[0],
                                                                       dados['escalar'], tem_denominador)
                if valido:
                    break
                else:
                    reconfirmar = input("Deseja tentar novamente? (sim/não): ").strip().lower()
                    if reconfirmar != "sim":
                        break
                    continue

                if not valido:
                    continue

            if not valido:
                continue

            # Salva os dados no arquivo
            dados['funcao']['expr_compiled'] = expr
            salvar_dados(dados)
            dados_armazenados = dados

            # Exibe os dados inseridos
            exibir_dados(dados)

            # Plota o gráfico
            plotar_grafico(vetor, numerador, denominador, tem_denominador, dados['escalar'])

        except ValueError:
            print("Erro: Digite números válidos para o escalar ou elementos do vetor.")
            continue

    elif resposta == "não":
        # Exibe os dados armazenados
        exibir_dados(dados_armazenados)
        # Plota o gráfico com os dados armazenados, se existirem
        if dados_armazenados and 'funcao' in dados_armazenados:
            plotar_grafico(
                dados_armazenados['vetor'],
                dados_armazenados['funcao']['numerador'],
                dados_armazenados['funcao']['denominador'],
                dados_armazenados['funcao']['tem_denominador'],
                dados_armazenados['escalar']
            )

    else:
        print("\nResposta inválida. Digite 'sim' ou 'não'.")

    # Pergunta se deseja continuar
    continuar = input("\nDeseja continuar? (sim/não): ").strip().lower()
    if continuar != "sim":
        print("Programa encerrado.")
        break