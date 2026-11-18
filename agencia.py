import json
import os
from functools import reduce

from cliente import Cliente, validar_cpf
from conta import ContaCorrente, ContaPoupanca


class Agencia:
    def __init__(self, codigo, nome):
        self.codigo = codigo
        self.nome = nome
        self.clientes = {}  # CPF -> objeto Cliente
        self.contas = {}    # número -> objeto Conta

    # ---------- clientes ----------
    def cadastrar_cliente(self, nome, cpf):
        cpf = validar_cpf(cpf)
        if cpf is None:
            return "Erro: CPF inválido."
        if cpf in self.clientes:
            return "Erro: CPF já cadastrado."
        if nome.strip() == "":
            return "Erro: nome vazio."
        self.clientes[cpf] = Cliente(nome.strip(), cpf)
        return "Cliente cadastrado com sucesso!"

    def buscar_cliente(self, cpf):
        cpf = validar_cpf(cpf)
        if cpf in self.clientes:
            return self.clientes[cpf]
        return None

    def procurar_clientes(self, termo):
        termo = termo.lower()
        achados = []
        for cli in self.clientes.values():
            if termo in cli.cpf or termo in cli.nome.lower():
                achados.append(cli)
        return achados

    # ---------- contas ----------
    def abrir_conta(self, cpf, tipo):
        cli = self.buscar_cliente(cpf)
        if cli is None:
            return "Erro: cliente não encontrado."

        numero = len(self.contas) + 1
        if tipo == "Poupança":
            conta = ContaPoupanca(numero, cli)
        else:
            conta = ContaCorrente(numero, cli)

        self.contas[numero] = conta
        cli.adicionar_conta(conta)
        return f"Conta {tipo} nº {numero} aberta com sucesso!"

    def buscar_conta(self, numero):
        if str(numero).isdigit() and int(numero) in self.contas:
            return self.contas[int(numero)]
        return None

    def depositar(self, numero, valor):
        conta = self.buscar_conta(numero)
        if conta is None:
            return "Erro: conta não encontrada."
        if conta.depositar(valor):
            return "Depósito realizado!"
        return "Erro: valor inválido."

    def sacar(self, numero, valor):
        conta = self.buscar_conta(numero)
        if conta is None:
            return "Erro: conta não encontrada."
        if conta.sacar(valor):
            return "Saque realizado!"
        return "Erro: saldo insuficiente ou valor inválido."

    def transferir(self, origem, destino, valor):
        conta_origem = self.buscar_conta(origem)
        conta_destino = self.buscar_conta(destino)
        if conta_origem is None or conta_destino is None:
            return "Erro: conta não encontrada."
        if conta_origem == conta_destino:
            return "Erro: origem e destino iguais."
        if conta_origem.sacar(valor):
            conta_destino.depositar(valor)
            return "Transferência realizada!"
        return "Erro: saldo insuficiente ou valor inválido."

    def render_poupancas(self):
        for conta in self.contas.values():
            if conta.tipo() == "Poupança":
                conta.render_juros()
        return "Rendimento aplicado nas poupanças!"

    # ---------- listagens (Etapa 4) ----------
    def clientes_ordenados(self):
        return sorted(self.clientes.values(), key=lambda c: c.nome.lower())

    def contas_ordenadas(self):
        return sorted(self.contas.values(), key=lambda c: c.cliente.nome.lower())

    def contas_saldo_positivo(self):
        return list(filter(lambda c: c.saldo > 0, self.contas.values()))

    def montante_total(self):
        return reduce(lambda soma, c: soma + c.saldo, self.contas.values(), 0.0)

    def maior_saldo(self):
        if len(self.contas) == 0:
            return 0.0
        return max(self.contas.values(), key=lambda c: c.saldo).saldo

    def menor_saldo(self):
        if len(self.contas) == 0:
            return 0.0
        return min(self.contas.values(), key=lambda c: c.saldo).saldo

    def saldo_medio(self):
        if len(self.contas) == 0:
            return 0.0
        return self.montante_total() / len(self.contas)

    # ---------- JSON (só ao abrir e ao fechar) ----------
    def salvar(self, arquivo="banco.json"):
        lista_clientes = []
        for cli in self.clientes.values():
            lista_clientes.append({"nome": cli.nome, "cpf": cli.cpf})

        lista_contas = []
        for conta in self.contas.values():
            lista_contas.append({
                "numero": conta.numero,
                "tipo": conta.tipo(),
                "cpf": conta.cliente.cpf,
                "saldo": conta.saldo
            })

        dados = {
            "agencia": {"codigo": self.codigo, "nome": self.nome},
            "clientes": lista_clientes,
            "contas": lista_contas
        }
        with open(arquivo, "w", encoding="utf-8") as arq:
            json.dump(dados, arq, ensure_ascii=False, indent=4)
        print("Dados salvos em", arquivo)

    def carregar(self, arquivo="banco.json"):
        if not os.path.exists(arquivo):
            print("Arquivo não encontrado. Começando do zero.")
            return

        with open(arquivo, "r", encoding="utf-8") as arq:
            dados = json.load(arq)

        self.codigo = dados["agencia"]["codigo"]
        self.nome = dados["agencia"]["nome"]

        for c in dados["clientes"]:
            self.clientes[c["cpf"]] = Cliente(c["nome"], c["cpf"])

        for c in dados["contas"]:
            cli = self.clientes[c["cpf"]]
            if c["tipo"] == "Poupança":
                conta = ContaPoupanca(c["numero"], cli, c["saldo"])
            else:
                conta = ContaCorrente(c["numero"], cli, c["saldo"])
            self.contas[conta.numero] = conta
            cli.adicionar_conta(conta)
        print("Dados carregados de", arquivo)
