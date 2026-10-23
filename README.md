# Banco-PA
Projeto de simulação de operações bancárias em Python.
### Registro de Desenvolvimento (22/10/2026)
**Desenvolvido por: Marcos Antônio Brito Dantas**

[#### 1. Resumo das Modificações e Implementações (Etapa 4):
- **Ajustes na Arquitetura para Suporte Híbrido (Terminal + Web)**: Refatoração dos módulos `conta.py` e `menu.py` para corrigir inconsistências de compatibilidade, garantindo que o sistema funcione de forma integrada tanto via terminal quanto na interface web sem quebras ou conflitos com o arquivo de persistência `banco.json`.
- **Implementação de Funções de Alta Ordem e Programação Funcional**:
  - `listar_contas_saldo_positivo()`: Filtra contas ativas com saldo maior que zero utilizando `filter()` e expressões `lambda`.
  - `montante_total_banco()`: Recalcula e consolida o saldo total custodiado pelo banco utilizando `reduce()`.
  - `busca_maior_saldo()` e `busca_menor_saldo()`: Identificam os valores extremos de saldo do banco via `max()` e `min()`.
  - `obter_dados_dashboard()`: Método estruturado que consolida métricas para alimentar a interface do Dashboard.
- **Refatoração de Ordenações**: Atualização das funções de ordenação de contas, clientes e agências utilizando `sorted()` e chaves `lambda` em substituição a laços manuais.
- **Criação da Interface Web (Dashboard)**:
  - Criação do servidor em Flask (`app.py`) para leitura e disponibilização dos dados em formato web.
  - Implementação do Front-End em HTML5 (`templates/index.html`) e estilização com CSS3 (`static/style.css`) para exibição das métricas financeiras (total de clientes, contas, saldo total, saldo médio, maior/menor saldo e listagens).

---

### 🚀 Como Rodar o Projeto (Instruções para a Equipe)

O projeto pode ser executado em dois modos: **Modo Terminal** ou **Modo Web (Dashboard)**.

#### Pré-requisito Único
Certifique-se de ter o Python instalado na sua máquina. Para rodar a interface Web, instale o Flask executando no terminal:
```bash](http://127.0.0.1:5000)
pip install flask

### Registro de Desenvolvimento (21/10/2026)
**Desenvolvido por: Mateus Macedo Gonzaga**

- **Implementação de funções da etapa 4**: listar clientes e agências, calcular saldo total do banco, encontrar maior saldo

---

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

### Registro de Desenvolvimento (25/09/2026)
**Desenvolvido por: Mell Mass Ribeiro Melo**

Refatoração do sistema (25/09/2026):
- Listas paralelas: classes e dicionários substituídos por listas em `agencia.py`, `cliente.py` e `conta.py`, ligadas pela mesma posição.
- Co-titulares: vínculo entre contas e clientes guardado nas listas `tit_contas` e `tit_cpfs`.
- Ordenação por nome: listagens de agências, clientes e contas ordenadas com o método bolha.
- Novo formato do `banco.json`: dados salvos como listas, sem dicionários.
