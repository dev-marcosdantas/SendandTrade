import agencia
import cliente

# listas das contas: a mesma posição é a mesma conta
numeros = []
agencias = []  # código da agência de cada conta
saldos = []

# titulares ficam separados: cada posição liga um número de conta a um cpf
# fiz assim pra uma conta poder ter mais de um titular
tit_contas = []
tit_cpfs = []


# acha a conta pela agência + número (se não achar devolve -1)
def buscar(codigo_agencia, numero):
    posicao = -1
    i = 0
    while i < len(numeros) and posicao == -1:
        if numeros[i] == numero and agencias[i] == codigo_agencia:
            posicao = i
        i = i + 1
    return posicao


# acha a conta só pelo número (usado na busca de cliente)
def buscar_por_numero(numero):
    posicao = -1
    i = 0
    while i < len(numeros) and posicao == -1:
        if numeros[i] == numero:
            posicao = i
        i = i + 1
    return posicao


# vê se o cpf já é titular dessa conta (devolve -1 se não for)
def buscar_titular(numero, cpf):
    posicao = -1
    i = 0
    while i < len(tit_contas) and posicao == -1:
        if tit_contas[i] == numero and tit_cpfs[i] == cpf:
            posicao = i
        i = i + 1
    return posicao


# liga mais um cpf na conta
def adicionar_titular(numero, cpf):
    tit_contas.append(numero)
    tit_cpfs.append(cpf)


# abre a conta com saldo zero e já coloca o primeiro titular
# nenhuma conta é apagada, então o número novo é a quantidade + 1
def abrir(codigo_agencia, cpf):
    numero = len(numeros) + 1
    numeros.append(numero)
    agencias.append(codigo_agencia)
    saldos.append(0.0)
    adicionar_titular(numero, cpf)
    return numero


# o valor já vem conferido do menu, aqui só soma/subtrai
def depositar(posicao, valor):
    saldos[posicao] = saldos[posicao] + valor


def sacar(posicao, valor):
    saldos[posicao] = saldos[posicao] - valor


# conta quantas contas uma agência tem
def contar_da_agencia(codigo_agencia):
    total = 0
    for i in range(len(agencias)):
        if agencias[i] == codigo_agencia:
            total = total + 1
    return total


# junta o nome de todos os titulares da conta separados por vírgula
def nomes_titulares(numero):
    texto = ""
    for i in range(len(tit_contas)):
        if tit_contas[i] == numero:
            if texto != "":
                texto = texto + ", "
            texto = texto + cliente.nome_do_cpf(tit_cpfs[i])
    return texto


# ordena as contas pelo nome dos titulares (bolha)
# troca número, agência e saldo juntos pra não misturar as contas
# os titulares não precisam trocar pq estão ligados pelo número da conta
def ordenar_por_titular():
    for i in range(len(numeros)):
        for j in range(len(numeros) - 1 - i):
            nome_atual = nomes_titulares(numeros[j]).lower()
            nome_prox = nomes_titulares(numeros[j + 1]).lower()
            if nome_atual > nome_prox:
                numeros[j], numeros[j + 1] = numeros[j + 1], numeros[j]
                agencias[j], agencias[j + 1] = agencias[j + 1], agencias[j]
                saldos[j], saldos[j + 1] = saldos[j + 1], saldos[j]


# texto da conta pra mostrar na tela
def descricao(i):
    pos_agencia = agencia.buscar_por_codigo(agencias[i])
    nome_agencia = agencia.nomes[pos_agencia]
    return (f"Agência: {agencias[i]} ({nome_agencia}) | Conta: {numeros[i]} | "
            f"Titulares: [{nomes_titulares(numeros[i])}] | Saldo: R$ {saldos[i]:.2f}")
