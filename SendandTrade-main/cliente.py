class Cliente:
    def __init__(self, nome: str, cpf: str):
        self.nome = nome.strip()
        self.cpf = cpf.strip()

    def __str__(self):
        return f"Cliente: {self.nome} | CPF: {self.cpf}"