import json
import os
import agencia
import cliente
import conta


# ---------- funções de apoio pra ler as entradas ----------

# lê um valor em dinheiro (aceita vírgula ou ponto), se for inválido devolve -1
def ler_valor(mensagem):
    texto = input(mensagem).strip().replace(",", ".")
    # tira um ponto só pra conferir se o resto é tudo número
    if texto.replace(".", "", 1).isdigit():
        return float(texto)
    return -1


# pede agência e número da conta e devolve a posição da conta (ou -1)
def pedir_conta():
    codigo = input("Código da agência: ").strip()
    if agencia.buscar_por_codigo(codigo) == -1:
        print(f"Erro: Agência {codigo} não encontrada.")
        return -1

    texto = input("Número da conta: ").strip()
    if texto.isdigit():
        numero = int(texto)
    else:
        print("Erro: Número da conta inválido.")
        return -1

    posicao = conta.buscar(codigo, numero)
    if posicao == -1:
        print(f"Erro: Conta {numero} não encontrada na Agência {codigo}.")
    return posicao


# mostra uma agência com a quantidade de contas dela
def mostrar_agencia(i):
    total = conta.contar_da_agencia(agencia.codigos[i])
    print(f"Agência Código: {agencia.codigos[i]} | Nome: {agencia.nomes[i]} | Total Contas: {total}")


# ---------- agências ----------

def cadastrar_agencia():
    print("\n--- CADASTRAR NOVA AGÊNCIA ---")
    codigo = input("Código da agência (ex: 0001): ").strip()

    # não deixa código vazio nem repetido
    if codigo == "":
        print("Erro: O código da agência não pode ser vazio.")
    elif agencia.buscar_por_codigo(codigo) != -1:
        print("Erro: Já existe uma agência cadastrada com este código.")
    else:
        nome = input("Nome/Região da agência: ").strip()
        agencia.cadastrar(codigo, nome)
        print(f"Agência '{nome}' (Código: {codigo}) cadastrada com sucesso!")


def procurar_agencia():
    print("\n--- PROCURAR AGÊNCIA ---")
    termo = input("Digite o código ou nome da agência: ").strip().lower()
    if termo == "":
        print("Erro: Termo de busca inválido.")
        return

    achadas = 0
    for i in range(len(agencia.codigos)):
        # serve se o termo aparecer em qualquer parte do código ou do nome
        if termo in agencia.codigos[i].lower() or termo in agencia.nomes[i].lower():
            achadas = achadas + 1
            print()
            mostrar_agencia(i)

            # mostra as contas que são dessa agência
            print("  Contas vinculadas nesta agência:")
            qtd_contas = 0
            for j in range(len(conta.numeros)):
                if conta.agencias[j] == agencia.codigos[i]:
                    print(f"    - {conta.descricao(j)}")
                    qtd_contas = qtd_contas + 1
            if qtd_contas == 0:
                print("    - Nenhuma conta vinculada.")

    if achadas == 0:
        print(f"Nenhuma agência encontrada com o termo '{termo}'.")


def apagar_agencia():
    print("\n--- APAGAR AGÊNCIA ---")
    codigo = input("Digite o código da agência a ser removida: ").strip()
    posicao = agencia.buscar_por_codigo(codigo)
    qtd_contas = conta.contar_da_agencia(codigo)

    # só deixa apagar se a agência existir e não tiver nenhuma conta
    if posicao == -1:
        print(f"Erro: Agência {codigo} não encontrada.")
    elif qtd_contas > 0:
        print(f"Erro: A agência {codigo} possui {qtd_contas} conta(s) ativa(s) e não pode ser apagada.")
    else:
        agencia.remover(posicao)
        print(f"Agência {codigo} removida com sucesso!")


# ---------- clientes e contas ----------

def cadastrar_cliente_e_conta():
    print("\n--- CADASTRO DE CLIENTE E ABERTURA DE CONTA ---")
    # precisa ter pelo menos uma agência pra abrir conta
    if len(agencia.codigos) == 0:
        print("Erro: Nenhuma agência cadastrada. Cadastre uma agência primeiro (Opção 1).")
        return

    codigo = input("Código da Agência onde a conta será aberta: ").strip()
    if agencia.buscar_por_codigo(codigo) == -1:
        print(f"Erro: Agência {codigo} não encontrada.")
        return

    nome = input("Nome do cliente: ").strip()
    cpf = input("CPF do cliente (apenas números): ").strip()
    if nome == "" or cpf == "":
        print("Erro: Nome e CPF são obrigatórios.")
        return

    # se o cpf já tá cadastrado usa o mesmo cliente, senão cadastra
    pos_cliente = cliente.buscar_por_cpf(cpf)
    if pos_cliente == -1:
        pos_cliente = cliente.cadastrar(nome, cpf)

    numero = conta.abrir(codigo, cpf)
    print(f"\nConta {numero} criada com sucesso na Agência {codigo}!")
    print(f"Titular: {cliente.nomes[pos_cliente]}")


def procurar_cliente():
    print("\n--- PROCURAR CLIENTE ---")
    termo = input("Digite o CPF ou nome do cliente: ").strip().lower()
    if termo == "":
        print("Erro: Termo de busca inválido.")
        return

    achados = 0
    for i in range(len(cliente.cpfs)):
        if termo in cliente.cpfs[i].lower() or termo in cliente.nomes[i].lower():
            achados = achados + 1
            print(f"\n{cliente.descricao(i)}")

            # procura nos titulares todas as contas desse cpf
            print("  Contas associadas:")
            qtd_contas = 0
            for j in range(len(conta.tit_cpfs)):
                if conta.tit_cpfs[j] == cliente.cpfs[i]:
                    p = conta.buscar_por_numero(conta.tit_contas[j])
                    print(f"    - Agência: {conta.agencias[p]} | Conta: {conta.numeros[p]} | Saldo: R$ {conta.saldos[p]:.2f}")
                    qtd_contas = qtd_contas + 1
            if qtd_contas == 0:
                print("    - Nenhuma conta vinculada no momento.")

    if achados == 0:
        print(f"Nenhum cliente encontrado para '{termo}'.")


def adicionar_titular_em_conta():
    print("\n--- ADICIONAR NOVO TITULAR A UMA CONTA EXISTENTE ---")
    posicao = pedir_conta()
    if posicao == -1:
        return

    cpf = input("CPF do novo titular a ser adicionado: ").strip()
    if cpf == "":
        print("Erro: CPF é obrigatório.")
        return

    # se o cliente ainda não existe, cadastra ele antes
    if cliente.buscar_por_cpf(cpf) == -1:
        print("Cliente não encontrado com esse CPF. Vamos cadastrá-lo.")
        nome = input("Nome do novo cliente: ").strip()
        if nome == "":
            print("Erro: Nome é obrigatório.")
            return
        cliente.cadastrar(nome, cpf)

    # não deixa colocar a mesma pessoa duas vezes na conta
    numero = conta.numeros[posicao]
    if conta.buscar_titular(numero, cpf) != -1:
        print("Este cliente já é titular desta conta.")
    else:
        conta.adicionar_titular(numero, cpf)
        print(f"Cliente {cliente.nome_do_cpf(cpf)} adicionado como co-titular da Conta {numero}!")


# ---------- operações da conta ----------

def consultar_saldo():
    print("\n--- CONSULTA DE SALDO ---")
    posicao = pedir_conta()
    if posicao != -1:
        print(f"\n{conta.descricao(posicao)}")


def realizar_deposito():
    print("\n--- REALIZAR DEPÓSITO ---")
    posicao = pedir_conta()
    if posicao == -1:
        return

    # confere o valor antes de mexer no saldo
    valor = ler_valor("Valor a depositar: R$ ")
    if valor == -1:
        print("Erro: Valor monetário inválido.")
    elif valor <= 0:
        print("Erro: O valor deve ser maior que zero.")
    else:
        conta.depositar(posicao, valor)
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso! Saldo atual: R$ {conta.saldos[posicao]:.2f}")


def realizar_saque():
    print("\n--- REALIZAR SAQUE ---")
    posicao = pedir_conta()
    if posicao == -1:
        return

    # não deixa sacar mais do que tem na conta
    valor = ler_valor("Valor a sacar: R$ ")
    if valor == -1:
        print("Erro: Valor monetário inválido.")
    elif valor <= 0 or valor > conta.saldos[posicao]:
        print("Erro: Saldo insuficiente ou valor inválido.")
    else:
        conta.sacar(posicao, valor)
        print(f"Saque de R$ {valor:.2f} realizado com sucesso! Saldo restante: R$ {conta.saldos[posicao]:.2f}")


# ---------- listagens (sempre ordenadas por nome) ----------

def listar_agencias():
    print("\n--- LISTA DE AGÊNCIAS ---")
    if len(agencia.codigos) == 0:
        print("Nenhuma agência cadastrada.")
    else:
        agencia.ordenar_por_nome()
        for i in range(len(agencia.codigos)):
            mostrar_agencia(i)


def listar_clientes():
    print("\n--- LISTA DE CLIENTES ---")
    if len(cliente.cpfs) == 0:
        print("Nenhum cliente cadastrado.")
    else:
        cliente.ordenar_por_nome()
        for i in range(len(cliente.cpfs)):
            print(cliente.descricao(i))


def listar_contas():
    print("\n--- LISTA DE CONTAS ---")
    if len(conta.numeros) == 0:
        print("Nenhuma conta cadastrada.")
    else:
        conta.ordenar_por_titular()
        for i in range(len(conta.numeros)):
            print(conta.descricao(i))


# ---------- relatório ----------

def gerar_relatorio_banco():
    print("\n" + "=" * 50)
    print("           RELATÓRIO GERAL DO BANCO          ")
    print("=" * 50)

    # soma o saldo de todas as contas
    saldo_total = 0.0
    for i in range(len(conta.saldos)):
        saldo_total = saldo_total + conta.saldos[i]

    print(f"Total de Agências Cadastradas: {len(agencia.codigos)}")
    print(f"Total de Clientes Cadastrados: {len(cliente.cpfs)}")
    print(f"Total de Contas Abertas:      {len(conta.numeros)}")
    print(f"Saldo Total no Banco:          R$ {saldo_total:.2f}")
    print("=" * 50)


# ---------- salvar e carregar o json ----------

# joga cada item de uma lista pra dentro de outra
def copiar(origem, destino):
    for item in origem:
        destino.append(item)


def salvar_json():
    # junta todas as listas numa só pra salvar
    # a ordem aqui tem que ser a mesma do carregar_json
    dados = [agencia.codigos, agencia.nomes,
             cliente.nomes, cliente.cpfs,
             conta.numeros, conta.agencias, conta.saldos,
             conta.tit_contas, conta.tit_cpfs]

    arquivo = open("banco.json", "w", encoding="utf-8")
    json.dump(dados, arquivo, ensure_ascii=False, indent=4)
    arquivo.close()
    print("\nDados salvos em 'banco.json' com sucesso!")


def carregar_json():
    # se ainda não tem arquivo, o sistema começa vazio
    if not os.path.exists("banco.json"):
        print("Nenhum arquivo 'banco.json' encontrado. Iniciando com sistema limpo.")
        return

    arquivo = open("banco.json", "r", encoding="utf-8")
    dados = json.load(arquivo)
    arquivo.close()

    # devolve cada lista pro seu lugar, na mesma ordem do salvar_json
    copiar(dados[0], agencia.codigos)
    copiar(dados[1], agencia.nomes)
    copiar(dados[2], cliente.nomes)
    copiar(dados[3], cliente.cpfs)
    copiar(dados[4], conta.numeros)
    copiar(dados[5], conta.agencias)
    copiar(dados[6], conta.saldos)
    copiar(dados[7], conta.tit_contas)
    copiar(dados[8], conta.tit_cpfs)
    print("Dados carregados com sucesso a partir de 'banco.json'!")


# ---------- menu principal ----------

def exibir_menu():
    carregar_json()
    opcao = ""

    # fica repetindo até escolher 0
    while opcao != "0":
        print("\n" + "=" * 50)
        print("         SISTEMA BANCARIO - SEND&TRADE       ")
        print("=" * 50)
        print(" 1 - Cadastrar Agência")
        print(" 2 - Procurar Agência (Por código ou nome)")
        print(" 3 - Apagar Agência")
        print(" 4 - Cadastrar Cliente e Abrir Conta")
        print(" 5 - Procurar Cliente (Por CPF ou nome)")
        print(" 6 - Adicionar Co-titular em Conta")
        print(" 7 - Consultar Saldo")
        print(" 8 - Realizar Depósito")
        print(" 9 - Realizar Saque")
        print("10 - Listar Agências")
        print("11 - Listar Clientes")
        print("12 - Listar Contas")
        print("13 - Relatório Geral do Banco")
        print("14 - Salvar em JSON")
        print(" 0 - Sair")
        print("=" * 50)

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_agencia()
        elif opcao == "2":
            procurar_agencia()
        elif opcao == "3":
            apagar_agencia()
        elif opcao == "4":
            cadastrar_cliente_e_conta()
        elif opcao == "5":
            procurar_cliente()
        elif opcao == "6":
            adicionar_titular_em_conta()
        elif opcao == "7":
            consultar_saldo()
        elif opcao == "8":
            realizar_deposito()
        elif opcao == "9":
            realizar_saque()
        elif opcao == "10":
            listar_agencias()
        elif opcao == "11":
            listar_clientes()
        elif opcao == "12":
            listar_contas()
        elif opcao == "13":
            gerar_relatorio_banco()
        elif opcao == "14":
            salvar_json()
        elif opcao == "0":
            # salva sozinho antes de sair pra não perder nada
            salvar_json()
            print("\nEncerrando o sistema...")
        else:
            print(f"\nOpção '{opcao}' inválida.")
