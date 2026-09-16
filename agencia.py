class Agencia:
    def __init__(self, codigo: str, nome: str):
        self.codigo = codigo.strip()
        self.nome = nome.strip()
        self.contas = {}  # Mapeia numero_conta -> Conta

    def adicionar_conta(self, conta):
        self.contas[conta.numero] = conta

    def remover_conta(self, numero_conta: int) -> bool:
        if numero_conta in self.contas:
            del self.contas[numero_conta]
            return True
        return False

    def __str__(self):
        return f"Agência Código: {self.codigo} | Nome: {self.nome} | Total Contas: {len(self.contas)}"