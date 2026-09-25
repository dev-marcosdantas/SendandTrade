# listas dos clientes: a mesma posição nas duas listas é o mesmo cliente
nomes = []
cpfs = []


# procura o cpf na lista e devolve a posição (se não achar devolve -1)
def buscar_por_cpf(cpf):
    posicao = -1
    i = 0
    while i < len(cpfs) and posicao == -1:
        if cpfs[i] == cpf:
            posicao = i
        i = i + 1
    return posicao


# coloca o cliente novo no final das listas e devolve a posição dele
def cadastrar(nome, cpf):
    nomes.append(nome)
    cpfs.append(cpf)
    return len(nomes) - 1


# pega o nome pelo cpf, usado pra mostrar os titulares das contas
def nome_do_cpf(cpf):
    posicao = buscar_por_cpf(cpf)
    if posicao == -1:
        return "?"
    return nomes[posicao]


# ordena por nome (bolha), trocando nome e cpf juntos pra não misturar
def ordenar_por_nome():
    for i in range(len(nomes)):
        for j in range(len(nomes) - 1 - i):
            if nomes[j].lower() > nomes[j + 1].lower():
                nomes[j], nomes[j + 1] = nomes[j + 1], nomes[j]
                cpfs[j], cpfs[j + 1] = cpfs[j + 1], cpfs[j]


# texto do cliente pra mostrar na tela
def descricao(i):
    return f"Cliente: {nomes[i]} | CPF: {cpfs[i]}"
