from abc import ABC, abstractmethod


class Conta(ABC):
    # Classe abstrata: não dá para criar uma Conta, só Corrente ou Poupança

    def __init__(self, numero, cliente, saldo=0.0):
        self.numero = numero
        self.cliente = cliente  # cada conta tem apenas 1 cliente
        self.saldo = saldo

    @abstractmethod
    def tipo(self):
        pass

    @abstractmethod
    def pode_sacar(self, valor):
        pass

    def depositar(self, valor):
        if valor <= 0:
            return False
        self.saldo = self.saldo + valor
        return True

    def sacar(self, valor):
        if valor <= 0:
            return False
        if not self.pode_sacar(valor):
            return False
        self.saldo = self.saldo - valor
        return True

    def descricao(self):
        return (f"Conta {self.numero} | {self.tipo()} | Titular: {self.cliente.nome} "
                f"| Saldo: R$ {self.saldo:.2f}")


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, saldo=0.0, limite=500.0):
        super().__init__(numero, cliente, saldo)
        self.limite = limite  # cheque especial

    def tipo(self):
        return "Corrente"

    def pode_sacar(self, valor):
        return valor <= self.saldo + self.limite


class ContaPoupanca(Conta):
    def __init__(self, numero, cliente, saldo=0.0, taxa=0.005):
        super().__init__(numero, cliente, saldo)
        self.taxa = taxa  # 0,5% de rendimento

    def tipo(self):
        return "Poupança"

    def pode_sacar(self, valor):
        return valor <= self.saldo  # poupança não fica negativa

    def render_juros(self):
        if self.saldo > 0:
            self.saldo = self.saldo + self.saldo * self.taxa
