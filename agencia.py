# Mapeia Código -> Dicionário da Agência
agencias = {}


def buscar_por_codigo(codigo):
    cod = codigo.strip()
    if cod in agencias:
        return agencias[cod]
    return None


def cadastrar(codigo, nome):
    cod = codigo.strip()
    if cod in agencias:
        print("Erro: Já existe agência cadastrada com este código.")
        return None

    agencia = {
        "codigo": cod,
        "nome": nome.strip()
    }
    agencias[cod] = agencia
    return agencia


def remover(codigo):
    cod = codigo.strip()
    if cod in agencias:
        del agencias[cod]
        return True
    return False


def ordenar_por_nome():
    lista = list(agencias.values())
    for i in range(len(lista)):
        for j in range(len(lista) - 1 - i):
            if lista[j]["nome"].lower() > lista[j + 1]["nome"].lower():
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
    return lista


def descricao(agencia):
    return f"Agência Código: {agencia['codigo']} | Nome: {agencia['nome']}"