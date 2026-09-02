from cliente import Cliente
from conta import Conta

clientes = {}      # Mapeia CPF -> Cliente
contas = {}        # Mapeia numero_conta -> Conta
contador_conta = 1 # Gera números automáticos: 1, 2, 3...

def cadastrar_cliente_e_conta():
    global contador_conta
    print("\n--- CADASTRO DE CLIENTE (COM CONTA AUTOMATICA) ---")
    nome = input("Nome do cliente: ").strip()
    cpf = input("CPF do cliente (apenas numeros): ").strip()

    if not nome or not cpf:
        print("Erro: Nome e CPF sao obrigatorios.")
        return

    if cpf in clientes:
        print("Erro: Ja existe um cliente com este CPF.")
        return

    # 1. Cria o cliente
    cliente = Cliente(nome, cpf)
    clientes[cpf] = cliente

    # 2. Gera a conta automaticamente para ele
    numero_nova_conta = contador_conta
    nova_conta = Conta(numero=numero_nova_conta, titular=cliente)
    contas[numero_nova_conta] = nova_conta
    contador_conta += 1

    print("\nCliente cadastrado e conta aberta com sucesso!")
    print(f"Titular: {cliente.nome}")
    print(f"CPF: {cliente.cpf}")
    print(f"NUMERO DA SUA CONTA: {numero_nova_conta}")
    print("Guarde esse numero para fazer depositos, saques e consultas.\n")

def criar_nova_conta_para_cliente():
    global contador_conta
    print("\n--- ABRIR NOVA CONTA PARA CLIENTE JA CADASTRADO ---")
    cpf = input("Informe o CPF do titular ja existente: ").strip()
    cliente = clientes.get(cpf)

    if not cliente:
        print("Erro: Nenhum cliente encontrado com esse CPF. Cadastre na opcao 1 primeiro.")
        return

    numero_nova_conta = contador_conta
    nova_conta = Conta(numero=numero_nova_conta, titular=cliente)
    contas[numero_nova_conta] = nova_conta
    contador_conta += 1

    print(f"\nMais uma conta criada com sucesso para {cliente.nome}!")
    print(f"Novo numero de conta: {numero_nova_conta}\n")

def consultar_saldo():
    print("\n--- CONSULTA DE SALDO ---")
    entrada = input("Digite o numero da conta: ").strip()
    if not entrada.isdigit():
        print("Erro: Digite apenas numeros inteiros para o numero da conta.")
        return

    num = int(entrada)
    conta = contas.get(num)
    if not conta:
        print(f"Erro: Conta {num} nao encontrada no sistema.")
        return

    print(f"\nTitular: {conta.titular.nome} | CPF: {conta.titular.cpf}")
    print(f"Saldo Atual: R$ {conta.consultar_saldo():.2f}")

def realizar_deposito():
    print("\n--- REALIZAR DEPOSITO ---")
    entrada_num = input("Digite o numero da conta de destino: ").strip()
    if not entrada_num.isdigit():
        print("Erro: Numero de conta invalido.")
        return

    num = int(entrada_num)
    conta = contas.get(num)
    if not conta:
        print(f"Erro: Conta {num} nao encontrada.")
        return

    entrada_valor = input("Valor a depositar: R$ ").strip().replace(",", ".")
    try:
        valor = float(entrada_valor)
    except ValueError:
        print("Erro: Valor monetario invalido.")
        return

    if conta.depositar(valor):
        print(f"\nDeposito de R$ {valor:.2f} realizado com sucesso na Conta {num} ({conta.titular.nome})!")
        print(f"Novo Saldo: R$ {conta.consultar_saldo():.2f}")
    else:
        print("Erro: O valor do deposito precisa ser maior que zero.")

def realizar_saque():
    print("\n--- REALIZAR SAQUE ---")
    entrada_num = input("Digite o numero da conta: ").strip()
    if not entrada_num.isdigit():
        print("Erro: Numero de conta invalido.")
        return

    num = int(entrada_num)
    conta = contas.get(num)
    if not conta:
        print(f"Erro: Conta {num} nao encontrada.")
        return

    entrada_valor = input("Valor a sacar: R$ ").strip().replace(",", ".")
    try:
        valor = float(entrada_valor)
    except ValueError:
        print("Erro: Valor monetario invalido.")
        return

    if conta.sacar(valor):
        print(f"\nSaque de R$ {valor:.2f} realizado com sucesso!")
        print(f"Saldo Restante: R$ {conta.consultar_saldo():.2f}")
    else:
        print("Erro: Saldo insuficiente ou valor invalido.")
        print(f"Saldo disponivel na conta: R$ {conta.consultar_saldo():.2f}")

def menu():
    while True:
        print("=" * 30)
        print("       SISTEMA BANCARIO       ")
        print("=" * 30)
        print("1 - Cadastrar Cliente (Gera Conta Automatica)")
        print("2 - Criar Outra Conta para Cliente Existente")
        print("3 - Consultar Saldo")
        print("4 - Realizar Deposito")
        print("5 - Realizar Saque")
        print("0 - Sair")
        print("=" * 30)

        opcao = input("Escolha uma opcao: ").strip()

        if opcao == "1":
            cadastrar_cliente_e_conta()
        elif opcao == "2":
            criar_nova_conta_para_cliente()
        elif opcao == "3":
            consultar_saldo()
        elif opcao == "4":
            realizar_deposito()
        elif opcao == "5":
            realizar_saque()
        elif opcao == "0":
            print("\nEncerrando o sistema...")
            break
        else:
            print(f"\nOpcao '{opcao}' invalida. Digite de 0 a 5.")

if __name__ == "__main__":
    menu()