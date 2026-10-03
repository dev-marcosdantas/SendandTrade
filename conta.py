import agencia
import cliente

# Mapeia Número da Conta -> Dicionário da Conta
contas = {}


def buscar_por_numero(numero):
    if numero in contas:
        return contas[numero]
    return None


def buscar_por_agencia_e_numero(codigo_agencia, numero):
    conta = buscar_por_numero(numero)
    if conta and conta["agencia"] == codigo_agencia:
        return conta
    return None


def abrir(codigo_agencia, cpf, tipo="Corrente"):
    ag = agencia.buscar_por_codigo(codigo_agencia)
    if not ag:
        print("Erro: Agência não existe.")
        return None

    cli = cliente.buscar_por_cpf(cpf)
    if not cli:
        print("Erro: Cliente não cadastrado.")
        return None

    tipos_validos = ["Corrente", "Poupança", "Salário"]
    if tipo not in tipos_validos:
        tipo = "Corrente"

    numero = len(contas) + 1
    nova_conta = {
        "numero": numero,
        "agencia": codigo_agencia,
        "tipo": tipo,
        "saldo": 0.0,
        "titulares": [cli["cpf"]]
    }
    contas[numero] = nova_conta
    return numero


def adicionar_titular(numero, cpf):
    conta = buscar_por_numero(numero)
    cpf_valido = cliente.validar_cpf(cpf)
    if conta and cpf_valido:
        if cpf_valido not in conta["titulares"]:
            conta["titulares"].append(cpf_valido)
            return True
    return False


def depositar(numero, valor):
    conta = buscar_por_numero(numero)
    if conta and valor > 0:
        conta["saldo"] += valor
        return True
    return False


def sacar(numero, valor):
    conta = buscar_por_numero(numero)
    if not conta or valor <= 0:
        return False

    # Regras por tipo de conta
    if conta["tipo"] == "Salário" and valor > conta["saldo"]:
        print("Erro: Conta Salário não permite saldo negativo.")
        return False

    if conta["saldo"] >= valor:
        conta["saldo"] -= valor
        return True
    
    return False


def contar_da_agencia(codigo_agencia):
    total = 0
    for conta in contas.values():
        if conta["agencia"] == codigo_agencia:
            total += 1
    return total


def nomes_titulares(conta):
    nomes = []
    for cpf in conta["titulares"]:
        cli = cliente.buscar_por_cpf(cpf)
        if cli:
            nomes.append(cli["nome"])
        else:
            nomes.append("?")
    return ", ".join(nomes)


def ordenar_por_titular():
    lista = list(contas.values())
    for i in range(len(lista)):
        for j in range(len(lista) - 1 - i):
            if nomes_titulares(lista[j]).lower() > nomes_titulares(lista[j + 1]).lower():
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
    return lista


def descricao(conta):
    ag = agencia.buscar_por_codigo(conta["agencia"])
    nome_ag = ag["nome"] if ag else "Desconhecida"
    return (f"Agência: {conta['agencia']} ({nome_ag}) | Conta: {conta['numero']} | "
            f"Tipo: {conta['tipo']} | Titulares: [{nomes_titulares(conta)}] | Saldo: R$ {conta['saldo']:.2f}")