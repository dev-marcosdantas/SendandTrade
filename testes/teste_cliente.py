import sys
import os

# Ajusta o caminho para enxergar os módulos do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import cliente


def testar_cadastro_e_validacao_cpf():
    print("--- TESTE 1: Validação de CPF e Cadastro de Cliente ---")
    
    # Teste de CPF Inválido
    res_invalido = cliente.cadastrar("João Silva", "123")
    assert res_invalido is None, "Deveria ter falhado com CPF curto"

    # Teste de CPF Válido
    cli = cliente.cadastrar("Marcos Dantas", "12345678901")
    assert cli is not None, "Deveria cadastrar cliente com CPF correto"
    assert cli["cpf"] == "12345678901"

    print("✅ Teste 1 (Cliente e CPF) passou com sucesso!\n")


if __name__ == "__main__":
    testar_cadastro_e_validacao_cpf()