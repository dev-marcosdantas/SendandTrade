from cliente import Cliente

class Conta:
    def __init__(self, numero: int, titular: Cliente, saldo_inicial: float = 0.0):
        self.numero = numero
        self.titular = titular
        self.saldo = float(saldo_inicial)

    def consultar_saldo(self) -> float:
        return self.saldo

    def depositar(self, valor: float) -> bool:
        if valor > 0:
            self.saldo += valor
            return True
        return False

    def sacar(self, valor: float) -> bool:
        if 0 < valor <= self.saldo:
            self.saldo -= valor
            return True
        return False

    def __str__(self):
        return f"Conta: {self.numero} | Titular: {self.titular.nome} (CPF: {self.titular.cpf}) | Saldo: R$ {self.saldo:.2f}"