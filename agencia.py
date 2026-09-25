# listas das agências: a mesma posição é a mesma agência
codigos = []
nomes = []


# procura o código e devolve a posição (se não achar devolve -1)
def buscar_por_codigo(codigo):
    posicao = -1
    i = 0
    while i < len(codigos) and posicao == -1:
        if codigos[i] == codigo:
            posicao = i
        i = i + 1
    return posicao


# coloca a agência nova no final das listas
def cadastrar(codigo, nome):
    codigos.append(codigo)
    nomes.append(nome)


# tira a agência das duas listas na mesma posição
def remover(posicao):
    codigos.pop(posicao)
    nomes.pop(posicao)


# ordena pelo nome (bolha), trocando código e nome juntos
def ordenar_por_nome():
    for i in range(len(nomes)):
        for j in range(len(nomes) - 1 - i):
            if nomes[j].lower() > nomes[j + 1].lower():
                nomes[j], nomes[j + 1] = nomes[j + 1], nomes[j]
                codigos[j], codigos[j + 1] = codigos[j + 1], codigos[j]
