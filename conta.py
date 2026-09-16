from cliente import Cliente

class Conta:
    def __init__(self, agencia, numero: int, saldo_inicial: float = 0.0):
        self.agencia = agencia
        self.numero = numero
        self.titulares = []  # Lista para permitir mais de um cliente por conta
        self.saldo = float(saldo_inicial)

    def adicionar_titular(self, cliente: Cliente):
        if cliente not in self.titulares:
            self.titulares.append(cliente)
            return True
        return False

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
        nomes_titulares = ", ".join([t.nome for t in self.titulares])
        return (f"Agência: {self.agencia.codigo} ({self.agencia.nome}) | "
                f"Conta: {self.numero} | Titulares: [{nomes_titulares}] | "
                f"Saldo: R$ {self.saldo:.2f}")