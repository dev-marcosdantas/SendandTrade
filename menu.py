from agencia import Agencia


def ler_valor(texto):
    texto = input(texto).strip().replace(",", ".")
    if texto.replace(".", "", 1).isdigit():
        return float(texto)
    return -1


def escolher_tipo():
    op = input("Tipo de conta (1 - Corrente, 2 - Poupança): ").strip()
    if op == "2":
        return "Poupança"
    return "Corrente"


def exibir_menu():
    banco = Agencia("0001", "Central")
    banco.carregar()  # JSON lido só aqui

    opcao = ""
    while opcao != "0":
        print("\n" + "=" * 45)
        print("     SEND&TRADE - Agência", banco.codigo, "-", banco.nome)
        print("=" * 45)
        print(" 1 - Cadastrar cliente e abrir conta")
        print(" 2 - Abrir nova conta para cliente")
        print(" 3 - Procurar cliente")
        print(" 4 - Consultar conta")
        print(" 5 - Depositar")
        print(" 6 - Sacar")
        print(" 7 - Transferir")
        print(" 8 - Render poupanças")
        print(" 9 - Listar clientes")
        print("10 - Listar contas")
        print("11 - Relatório geral")
        print(" 0 - Sair e salvar")
        opcao = input("Opção: ").strip()

        if opcao == "1":
            nome = input("Nome: ")
            cpf = input("CPF: ")
            msg = banco.cadastrar_cliente(nome, cpf)
            print(msg)
            if not msg.startswith("Erro"):
                print(banco.abrir_conta(cpf, escolher_tipo()))

        elif opcao == "2":
            cpf = input("CPF do cliente: ")
            print(banco.abrir_conta(cpf, escolher_tipo()))

        elif opcao == "3":
            termo = input("CPF ou nome: ")
            achados = banco.procurar_clientes(termo)
            if len(achados) == 0:
                print("Nenhum cliente encontrado.")
            for cli in achados:
                print(cli.descricao())
                for conta in cli.contas:
                    print("   -", conta.descricao())

        elif opcao == "4":
            conta = banco.buscar_conta(input("Número da conta: "))
            if conta is None:
                print("Conta não encontrada.")
            else:
                print(conta.descricao())

        elif opcao == "5":
            numero = input("Número da conta: ")
            valor = ler_valor("Valor: R$ ")
            print(banco.depositar(numero, valor))

        elif opcao == "6":
            numero = input("Número da conta: ")
            valor = ler_valor("Valor: R$ ")
            print(banco.sacar(numero, valor))

        elif opcao == "7":
            origem = input("Conta de origem: ")
            destino = input("Conta de destino: ")
            valor = ler_valor("Valor: R$ ")
            print(banco.transferir(origem, destino, valor))

        elif opcao == "8":
            print(banco.render_poupancas())

        elif opcao == "9":
            for cli in banco.clientes_ordenados():
                print(cli.descricao())

        elif opcao == "10":
            for conta in banco.contas_ordenadas():
                print(conta.descricao())

        elif opcao == "11":
            print("Clientes:", len(banco.clientes))
            print("Contas:", len(banco.contas))
            print(f"Saldo total: R$ {banco.montante_total():.2f}")
            print(f"Saldo médio: R$ {banco.saldo_medio():.2f}")
            print(f"Maior saldo: R$ {banco.maior_saldo():.2f}")
            print(f"Menor saldo: R$ {banco.menor_saldo():.2f}")

        elif opcao == "0":
            banco.salvar()  # JSON gravado só aqui
            print("Encerrando...")

        else:
            print("Opção inválida.")
