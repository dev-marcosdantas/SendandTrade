import json
import os
import agencia
import cliente
import conta


def ler_valor(mensagem):
    texto = input(mensagem).strip().replace(",", ".")
    if texto.replace(".", "", 1).isdigit():
        return float(texto)
    return -1


def pedir_conta():
    codigo = input("Código da agência: ").strip()
    if not agencia.buscar_por_codigo(codigo):
        print(f"Erro: Agência {codigo} não encontrada.")
        return None

    texto = input("Número da conta: ").strip()
    if not texto.isdigit():
        print("Erro: Número da conta inválido.")
        return None

    numero = int(texto)
    c = conta.buscar_por_agencia_e_numero(codigo, numero)
    if not c:
        print(f"Erro: Conta {numero} não encontrada na Agência {codigo}.")
        return None

    return c


# ---------- agências ----------

def cadastrar_agencia():
    print("\n--- CADASTRAR NOVA AGÊNCIA ---")
    codigo = input("Código da agência (ex: 0001): ").strip()
    if codigo == "":
        print("Erro: Código não pode ser vazio.")
        return

    nome = input("Nome/Região da agência: ").strip()
    if agencia.cadastrar(codigo, nome):
        print(f"Agência '{nome}' (Código: {codigo}) cadastrada com sucesso!")


def procurar_agencia():
    print("\n--- PROCURAR AGÊNCIA ---")
    termo = input("Digite o código ou nome da agência: ").strip().lower()
    achou = False
    for ag in agencia.agencias.values():
        if termo in ag["codigo"].lower() or termo in ag["nome"].lower():
            achou = True
            print(f"\n{agencia.descricao(ag)}")
            print("  Contas vinculadas nesta agência:")
            total = 0
            for c in conta.contas.values():
                if c["agencia"] == ag["codigo"]:
                    print(f"    - {conta.descricao(c)}")
                    total += 1
            if total == 0:
                print("    - Nenhuma conta vinculada.")
    if not achou:
        print(f"Nenhuma agência encontrada com o termo '{termo}'.")


def apagar_agencia():
    print("\n--- APAGAR AGÊNCIA ---")
    codigo = input("Digite o código da agência a remover: ").strip()
    qtd_contas = conta.contar_da_agencia(codigo)
    if qtd_contas > 0:
        print(f"Erro: A agência {codigo} possui {qtd_contas} conta(s) ativa(s) e não pode ser apagada.")
    elif agencia.remover(codigo):
        print(f"Agência {codigo} removida com sucesso!")
    else:
        print(f"Erro: Agência {codigo} não encontrada.")


# ---------- clientes e contas ----------

def cadastrar_cliente_e_conta():
    print("\n--- CADASTRO DE CLIENTE E ABERTURA DE CONTA ---")
    if len(agencia.agencias) == 0:
        print("Erro: Nenhuma agência cadastrada. Cadastre uma agência primeiro.")
        return

    codigo_ag = input("Código da agência: ").strip()
    if not agencia.buscar_por_codigo(codigo_ag):
        print("Erro: Agência não encontrada.")
        return

    nome = input("Nome do cliente: ").strip()
    cpf = input("CPF do cliente (11 dígitos): ").strip()

    cpf_valido = cliente.validar_cpf(cpf)
    if not cpf_valido:
        print("Erro: CPF inválido.")
        return

    cli = cliente.buscar_por_cpf(cpf_valido)
    if not cli:
        cli = cliente.cadastrar(nome, cpf_valido)

    print("\nEscolha o Tipo de Conta:")
    print("1 - Corrente")
    print("2 - Poupança")
    print("3 - Salário")
    op_tipo = input("Opção: ").strip()

    tipo = "Corrente"
    if op_tipo == "2":
        tipo = "Poupança"
    elif op_tipo == "3":
        tipo = "Salário"

    num_conta = conta.abrir(codigo_ag, cpf_valido, tipo)
    if num_conta:
        print(f"\nConta {tipo} nº {num_conta} criada com sucesso!")


def procurar_cliente():
    print("\n--- PROCURAR CLIENTE POR CPF OU NOME ---")
    termo = input("Digite o CPF ou Nome do cliente: ").strip().lower()
    achados = 0
    for cli in cliente.clientes.values():
        if termo in cli["cpf"] or termo in cli["nome"].lower():
            achados += 1
            print(f"\n{cliente.descricao(cli)}")
            print("  Contas associadas:")
            qtd_c = 0
            for c in conta.contas.values():
                if cli["cpf"] in c["titulares"]:
                    print(f"    - Agência: {c['agencia']} | Conta nº: {c['numero']} | Tipo: {c['tipo']} | Saldo: R$ {c['saldo']:.2f}")
                    qtd_c += 1
            if qtd_c == 0:
                print("    - Nenhuma conta vinculada.")

    if achados == 0:
        print("Nenhum cliente encontrado.")


def adicionar_titular_em_conta():
    print("\n--- ADICIONAR CO-TITULAR EM CONTA ---")
    c = pedir_conta()
    if not c:
        return

    cpf = input("CPF do novo titular: ").strip()
    cpf_valido = cliente.validar_cpf(cpf)
    if not cpf_valido:
        print("Erro: CPF inválido.")
        return

    if not cliente.buscar_por_cpf(cpf_valido):
        print("Cliente novo. Vamos cadastrar:")
        nome = input("Nome do cliente: ").strip()
        cliente.cadastrar(nome, cpf_valido)

    if conta.adicionar_titular(c["numero"], cpf_valido):
        print("Co-titular adicionado com sucesso!")
    else:
        print("Erro: Cliente já é titular desta conta ou dados inválidos.")


# ---------- operações ----------

def consultar_saldo():
    print("\n--- CONSULTAR SALDO ---")
    c = pedir_conta()
    if c:
        print(f"\n{conta.descricao(c)}")


def realizar_deposito():
    print("\n--- REALIZAR DEPÓSITO ---")
    c = pedir_conta()
    if not c:
        return

    valor = ler_valor("Valor a depositar: R$ ")
    if conta.depositar(c["numero"], valor):
        print(f"Depósito de R$ {valor:.2f} realizado! Saldo atual: R$ {c['saldo']:.2f}")
    else:
        print("Erro: Valor inválido para depósito.")


def realizar_saque():
    print("\n--- REALIZAR SAQUE ---")
    c = pedir_conta()
    if not c:
        return

    valor = ler_valor("Valor a sacar: R$ ")
    if conta.sacar(c["numero"], valor):
        print(f"Saque de R$ {valor:.2f} realizado! Saldo restante: R$ {c['saldo']:.2f}")
    else:
        print("Erro: Saque não permitido ou saldo insuficiente.")


# ---------- listagens e relatório ----------

def listar_agencias():
    print("\n--- LISTA DE AGÊNCIAS ---")
    lista = agencia.ordenar_por_nome()
    for ag in lista:
        print(agencia.descricao(ag))


def listar_clientes():
    print("\n--- LISTA DE CLIENTES ---")
    lista = cliente.ordenar_por_nome()
    for cli in lista:
        print(cliente.descricao(cli))


def listar_contas():
    print("\n--- LISTA DE CONTAS ---")
    lista = conta.ordenar_por_titular()
    for c in lista:
        print(conta.descricao(c))


def gerar_relatorio_banco():
    print("\n" + "=" * 50)
    print("           RELATÓRIO GERAL DO BANCO          ")
    print("=" * 50)
    saldo_total = sum(c["saldo"] for c in conta.contas.values())
    print(f"Total de Agências Cadastradas: {len(agencia.agencias)}")
    print(f"Total de Clientes Cadastrados: {len(cliente.clientes)}")
    print(f"Total de Contas Abertas:      {len(conta.contas)}")
    print(f"Saldo Total no Banco:          R$ {saldo_total:.2f}")
    print("=" * 50)


# ---------- JSON com Dicionários ----------

def salvar_json():
    dados = {
        "agencias": list(agencia.agencias.values()),
        "clientes": list(cliente.clientes.values()),
        "contas": list(conta.contas.values())
    }
    try:
        with open("banco.json", "w", encoding="utf-8") as arq:
            json.dump(dados, arq, ensure_ascii=False, indent=4)
        print("\nDados salvos em 'banco.json' com sucesso!")
    except Exception as e:
        print(f"Erro ao salvar arquivo JSON: {e}")


def carregar_json():
    if not os.path.exists("banco.json"):
        print("Nenhum arquivo 'banco.json' encontrado. Sistema iniciado limpo.")
        return

    try:
        with open("banco.json", "r", encoding="utf-8") as arq:
            dados = json.load(arq)

        # Reconstrui agências
        for ag in dados.get("agencias", []):
            agencia.agencias[ag["codigo"]] = ag

        # Reconstrui clientes
        for cli in dados.get("clientes", []):
            cliente.clientes[cli["cpf"]] = cli

        # Reconstrui contas
        for c in dados.get("contas", []):
            conta.contas[c["numero"]] = c

        print("Dados carregados com sucesso a partir de 'banco.json'!")
    except Exception as e:
        print(f"Erro ao carregar 'banco.json': {e}")


# ---------- menu principal ----------

def exibir_menu():
    carregar_json()
    opcao = ""

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
            salvar_json()
            print("\nEncerrando o sistema...")
        else:
            print(f"\nOpção '{opcao}' inválida.")