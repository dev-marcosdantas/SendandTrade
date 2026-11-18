def validar_cpf(cpf):
    cpf = cpf.strip().replace(".", "").replace("-", "")
    if len(cpf) == 11 and cpf.isdigit():
        return cpf
    return None


class Cliente:
    def __init__(self, nome, cpf):
        self.nome = nome
        self.cpf = cpf
        self.contas = []  # um cliente pode ter várias contas

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def saldo_total(self):
        total = 0
        for conta in self.contas:
            total = total + conta.saldo
        return total

    def descricao(self):
        return f"Cliente: {self.nome} | CPF: {self.cpf} | Contas: {len(self.contas)}"
