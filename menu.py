from cliente import Cliente
from agencia import Agencia
from conta import Conta

class MenuInterface:
    def __init__(self):
        self.agencias = {}       # Mapeia codigo_agencia -> Agencia
        self.clientes = {}       # Mapeia cpf -> Cliente
        self.contador_conta = 1  # Gera número sequencial para as contas

    # --- GERENCIAMENTO E BUSCA DE AGÊNCIAS ---
    def cadastrar_agencia(self):
        print("\n--- CADASTRAR NOVA AGÊNCIA ---")
        codigo = input("Código da agência (ex: 0001): ").strip()
        if not codigo:
            print("Erro: O código da agência não pode ser vazio.")
            return

        if codigo in self.agencias:
            print("Erro: Já existe uma agência cadastrada com este código.")
            return

        nome = input("Nome/Região da agência: ").strip()
        nova_agencia = Agencia(codigo, nome)
        self.agencias[codigo] = nova_agencia
        print(f"Agência '{nome}' (Código: {codigo}) cadastrada com sucesso!")

    def procurar_agencia(self):
        print("\n--- PROCURAR AGÊNCIA ---")
        termo = input("Digite o código ou nome da agência: ").strip().lower()
        if not termo:
            print("Erro: Termo de busca inválido.")
            return

        encontradas = [
            ag for ag in self.agencias.values()
            if termo in ag.codigo.lower() or termo in ag.nome.lower()
        ]

        if not encontradas:
            print(f"Nenhuma agência encontrada com o termo '{termo}'.")
            return

        print(f"\nResultado(s) da busca por '{termo}':")
        for ag in encontradas:
            print(f"\n{ag}")
            print("  Contas vinculadas nesta agência:")
            if not ag.contas:
                print("    - Nenhuma conta vinculada.")
            else:
                for conta in ag.contas.values():
                    print(f"    - {conta}")

    def apagar_agencia(self):
        print("\n--- APAGAR AGÊNCIA ---")
        codigo = input("Digite o código da agência a ser removida: ").strip()
        agencia = self.agencias.get(codigo)

        if not agencia:
            print(f"Erro: Agência {codigo} não encontrada.")
            return

        if agencia.contas:
            print(f"Erro: A agência {codigo} possui {len(agencia.contas)} conta(s) ativa(s) e não pode ser apagada.")
            return

        del self.agencias[codigo]
        print(f"Agência {codigo} removida com sucesso!")

    # --- GERENCIAMENTO E BUSCA DE CLIENTES E CONTAS ---
    def cadastrar_cliente_e_conta(self):
        print("\n--- CADASTRO DE CLIENTE E ABERTURA DE CONTA ---")
        if not self.agencias:
            print("Erro: Nenhuma agência cadastrada. Cadastre uma agência primeiro (Opção 1).")
            return

        cod_agencia = input("Código da Agência onde a conta será aberta: ").strip()
        agencia = self.agencias.get(cod_agencia)
        if not agencia:
            print(f"Erro: Agência {cod_agencia} não encontrada.")
            return

        nome = input("Nome do cliente: ").strip()
        cpf = input("CPF do cliente (apenas números): ").strip()

        if not nome or not cpf:
            print("Erro: Nome e CPF são obrigatórios.")
            return

        cliente = self.clientes.get(cpf)
        if not cliente:
            cliente = Cliente(nome, cpf)
            self.clientes[cpf] = cliente

        numero_nova_conta = self.contador_conta
        nova_conta = Conta(agencia=agencia, numero=numero_nova_conta)
        nova_conta.adicionar_titular(cliente)
        
        agencia.adicionar_conta(nova_conta)
        self.contador_conta += 1

        print(f"\nConta {numero_nova_conta} criada com sucesso na Agência {agencia.codigo}!")
        print(f"Titular: {cliente.nome}")

    def procurar_cliente(self):
        print("\n--- PROCURAR CLIENTE ---")
        termo = input("Digite o CPF ou nome do cliente: ").strip().lower()
        if not termo:
            print("Erro: Termo de busca inválido.")
            return

        clientes_encontrados = [
            c for c in self.clientes.values()
            if termo in c.cpf.lower() or termo in c.nome.lower()
        ]

        if not clientes_encontrados:
            print(f"Nenhum cliente encontrado para '{termo}'.")
            return

        for cliente in clientes_encontrados:
            print(f"\n{cliente}")
            print("  Contas associadas:")
            contas_do_cliente = []
            
            # Varre todas as contas de todas as agências para localizar as do cliente
            for agencia in self.agencias.values():
                for conta in agencia.contas.values():
                    if cliente in conta.titulares:
                        contas_do_cliente.append(conta)

            if not contas_do_cliente:
                print("    - Nenhuma conta vinculada no momento.")
            else:
                for conta in contas_do_cliente:
                    print(f"    - Agência: {conta.agencia.codigo} | Conta: {conta.numero} | Saldo: R$ {conta.saldo:.2f}")

    def adicionar_titular_em_conta(self):
        print("\n--- ADICIONAR NOVO TITULAR A UMA CONTA EXISTENTE ---")
        agencia, conta = self._buscar_conta_input()
        if not conta:
            return

        cpf = input("CPF do novo titular a ser adicionado: ").strip()
        cliente = self.clientes.get(cpf)

        if not cliente:
            print("Cliente não encontrado com esse CPF. Vamos cadastrá-lo.")
            nome = input("Nome do novo cliente: ").strip()
            if not nome:
                print("Erro: Nome é obrigatório.")
                return
            cliente = Cliente(nome, cpf)
            self.clientes[cpf] = cliente

        if conta.adicionar_titular(cliente):
            print(f"Cliente {cliente.nome} adicionado como co-titular da Conta {conta.numero}!")
        else:
            print("Este cliente já é titular desta conta.")

    # --- OPERAÇÕES BANCÁRIAS ---
    def consultar_saldo(self):
        print("\n--- CONSULTA DE SALDO ---")
        _, conta = self._buscar_conta_input()
        if conta:
            print(f"\n{conta}")

    def realizar_deposito(self):
        print("\n--- REALIZAR DEPÓSITO ---")
        _, conta = self._buscar_conta_input()
        if not conta:
            return

        try:
            valor = float(input("Valor a depositar: R$ ").strip().replace(",", "."))
        except ValueError:
            print("Erro: Valor monetário inválido.")
            return

        if conta.depositar(valor):
            print(f"Depósito de R$ {valor:.2f} realizado com sucesso! Saldo atual: R$ {conta.consultar_saldo():.2f}")
        else:
            print("Erro: O valor deve ser maior que zero.")

    def realizar_saque(self):
        print("\n--- REALIZAR SAQUE ---")
        _, conta = self._buscar_conta_input()
        if not conta:
            return

        try:
            valor = float(input("Valor a sacar: R$ ").strip().replace(",", "."))
        except ValueError:
            print("Erro: Valor monetário inválido.")
            return

        if conta.sacar(valor):
            print(f"Saque de R$ {valor:.2f} realizado com sucesso! Saldo restante: R$ {conta.consultar_saldo():.2f}")
        else:
            print("Erro: Saldo insuficiente ou valor inválido.")

    # --- MÉTODOS AUXILIARES E LOOP PRINCIPAL ---
    def _buscar_conta_input(self):
        cod_agencia = input("Código da agência: ").strip()
        agencia = self.agencias.get(cod_agencia)
        if not agencia:
            print(f"Erro: Agência {cod_agencia} não encontrada.")
            return None, None

        try:
            num_conta = int(input("Número da conta: ").strip())
        except ValueError:
            print("Erro: Número da conta inválido.")
            return None, None

        conta = agencia.contas.get(num_conta)
        if not conta:
            print(f"Erro: Conta {num_conta} não encontrada na Agência {cod_agencia}.")
            return None, None

        return agencia, conta

    def exibir_menu(self):
        while True:
            print("\n" + "=" * 50)
            print("         SISTEMA BANCARIO - SEND&TRADE       ")
            print("=" * 50)
            print(" 1 - Cadastrar Agência")
            print(" 2 - Procurar Agência (Por código ou nome)")
            print(" 3 - Apagar Agência")
            print(" 4 - Cadastrar Cliente e Abrir Conta")
            print(" 5 - Procurar Cliente (Por CPF ou nome)")
            print(" 6 - Adicionar Co-titular (Segundo Cliente) em Conta")
            print(" 7 - Consultar Saldo")
            print(" 8 - Realizar Depósito")
            print(" 9 - Realizar Saque")
            print(" 0 - Sair")
            print("=" * 50)

            opcao = input("Escolha uma opção: ").strip()

            if opcao == "1":
                self.cadastrar_agencia()
            elif opcao == "2":
                self.procurar_agencia()
            elif opcao == "3":
                self.apagar_agencia()
            elif opcao == "4":
                self.cadastrar_cliente_e_conta()
            elif opcao == "5":
                self.procurar_cliente()
            elif opcao == "6":
                self.adicionar_titular_em_conta()
            elif opcao == "7":
                self.consultar_saldo()
            elif opcao == "8":
                self.realizar_deposito()
            elif opcao == "9":
                self.realizar_saque()
            elif opcao == "0":
                print("\nEncerrando o sistema...")
                break
            else:
                print(f"\nOpção '{opcao}' inválida.")