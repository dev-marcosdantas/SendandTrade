# Banco-PA
Projeto de simulação de operações bancárias em Python.

### Registro de Desenvolvimento (17/09/2026)
**Desenvolvido por: Mateus Macedo Gonzaga**

- **Implementação do .gitignore ao banco de dados**: Implementação do sistema para não exibir dados armazenados pelo programa durante o funcionamento.

### Registro de Desenvolvimento (16/09/2026)
**Desenvolvido por: Mell Mass Ribeiro Melo**

Novas funcionalidades e persitência implementadas (16/09/2026):
- **Persistência de Dados em JSON (`salvar_json` e `carregar_json`)**: Implementado o salvamento automático e manual do estado do sistema (agências, clientes, contas e saldos) em arquivo `banco.json`, garantindo a manutenção dos dados entre execuções.
- **Relatório Geral do Banco (`gerar_relatorio_banco`)**: Criada funcionalidade para consolidação de métricas globais do banco, exibindo o total de agências, clientes, contas abertas e o saldo geral custodiado.
- **Listagens do Sistema (`listar_agencias`, `listar_clientes`, `listar_contas`)**: Adicionados métodos de consulta para exibição estruturada e individual de todas as agências, clientes e contas cadastradas.
- **Atualização da Interface (`exibir_menu`)**: Expandido o menu interativo em `menu.py` para comportar as novas opções de relatório, listagem e salvamento dos dados em JSON.
- **Configuração do Git (`.gitignore`)**: Criado o arquivo de filtro para ignorar arquivos temporários do Python, configurações de IDEs e o arquivo de persistência local (`banco.json`).

---

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
