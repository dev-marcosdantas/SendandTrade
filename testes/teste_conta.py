import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import agencia
import cliente
import conta


def testar_operacoes_conta():
    print("--- TESTE 2: Operações em Contas Diferentes ---")
    
    agencia.cadastrar("0001", "Agência Central")
    cliente.cadastrar("Mell Melo", "98765432100")

    # Abertura de Conta Salário
    num_conta = conta.abrir("0001", "98765432100", tipo="Salário")
    assert num_conta == 1

    # Depósito
    dep = conta.depositar(num_conta, 500.0)
    assert dep is True
    
    # Saque dentro do saldo
    saque_ok = conta.sacar(num_conta, 200.0)
    assert saque_ok is True
    
    # Saque maior que o saldo (Bloqueado em conta Salário)
    saque_inv = conta.sacar(num_conta, 1000.0)
    assert saque_inv is False

    print("✅ Teste 2 (Abertura, Depósito e Saque) passou com sucesso!\n")


if __name__ == "__main__":
    testar_operacoes_conta()