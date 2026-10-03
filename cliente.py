# Mapeia CPF -> Dicionário do Cliente
clientes = {}


def validar_cpf(cpf):
    # Remove espaços e caracteres não numéricos simples
    cpf_limpo = cpf.strip().replace(".", "").replace("-", "")
    if len(cpf_limpo) == 11 and cpf_limpo.isdigit():
        return cpf_limpo
    return None


def buscar_por_cpf(cpf):
    cpf_valido = validar_cpf(cpf)
    if cpf_valido and cpf_valido in clientes:
        return clientes[cpf_valido]
    return None


def cadastrar(nome, cpf):
    cpf_valido = validar_cpf(cpf)
    if not cpf_valido:
        print("Erro: CPF inválido. Deve conter 11 dígitos numéricos.")
        return None

    if cpf_valido in clientes:
        print("Erro: Já existe um cliente cadastrado com este CPF.")
        return None

    cliente = {
        "nome": nome.strip(),
        "cpf": cpf_valido
    }
    clientes[cpf_valido] = cliente
    return cliente


def ordenar_por_nome():
    # Ordena a lista de dicionários de clientes pelo nome
    lista = list(clientes.values())
    for i in range(len(lista)):
        for j in range(len(lista) - 1 - i):
            if lista[j]["nome"].lower() > lista[j + 1]["nome"].lower():
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
    return lista


def descricao(cliente):
    return f"Cliente: {cliente['nome']} | CPF: {cliente['cpf']}"