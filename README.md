# Banco-PA
Projeto de simulação de operações bancárias em Python.

### Registro de Desenvolvimento (15/09/2026)
**Desenvolvido por: Marcos Antônio Brito Dantas**

Novas funcionalidades e refatorações implementadas (15/09/2026):
- **Criação da Classe Agência (`agencia.py`)**: Implementado o suporte a múltiplas agências com operações para cadastrar, procurar (por código ou nome) e apagar agência.
- **Suporte a Múltiplos Titulares**: Refatorada a classe `Conta` (`conta.py`) para permitir a inclusão de mais de um cliente (co-titular) na mesma conta bancária.
- **Busca de Clientes**: Adicionada a funcionalidade para buscar clientes por CPF ou nome, listando todas as contas e agências vinculadas ao cliente.
- **Classe de Interface/Menu (`menu.py`)**: Desvinculado o menu do arquivo principal, criando uma classe própria para gerenciar a interface com o usuário e a lógica do sistema.
- **Refatoração do Arquivo Principal (`main.py`)**: Simplificado o ponto de entrada da aplicação, inicializando apenas a classe `MenuInterface`.
---

### Registro de Desenvolvimento (02/09/2026)
**Desenvolvido por: Marcos Antônio Brito Dantas**

Funcionalidades implementadas (02/09/2026):
- Cadastro de cliente com criação automática da conta
- Abertura de conta adicional para cliente já cadastrado
- Consulta de saldo
- Operação de depósito com validações de valor
- Operação de saque com verificação de saldo disponível
- Estruturação e modularização dos arquivos (`cliente.py`, `conta.py` e `main.py`)
