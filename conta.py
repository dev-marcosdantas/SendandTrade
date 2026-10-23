import agencia
import cliente
from functools import reduce

# Mapeia Número da Conta -> Dicionário da Conta
contas = {}


def buscar_por_numero(numero):
    return contas.get(numero, None)


def buscar_por_agencia_e_numero(codigo_agencia, numero):
    conta = buscar_por_numero(numero)
    if conta and conta["agencia"] == codigo_agencia:
        return conta
    return None


def abrir(codigo_agencia, cpf, tipo="Corrente"):
    ag = agencia.buscar_por_codigo(codigo_agencia)
    if not ag:
        print("Erro: Agência não existe.")
        return None

    cli = cliente.buscar_por_cpf(cpf)
    if not cli:
        print("Erro: Cliente não cadastrado.")
        return None

    tipos_validos = ["Corrente", "Poupança", "Salário"]
    if tipo not in tipos_validos:
        tipo = "Corrente"

    numero = len(contas) + 1
    nova_conta = {
        "numero": numero,
        "agencia": codigo_agencia,
        "tipo": tipo,
        "saldo": 0.0,
        "titulares": [cli["cpf"]]
    }
    contas[numero] = nova_conta
    return numero


def adicionar_titular(numero, cpf):
    conta = buscar_por_numero(numero)
    cpf_valido = cliente.validar_cpf(cpf)
    if conta and cpf_valido:
        if cpf_valido not in conta["titulares"]:
            conta["titulares"].append(cpf_valido)
            return True
    return False


def depositar(numero, valor):
    conta = buscar_por_numero(numero)
    if conta and valor > 0:
        conta["saldo"] += valor
        return True
    return False


def sacar(numero, valor):
    conta = buscar_por_numero(numero)
    if not conta or valor <= 0:
        return False

    if conta["tipo"] == "Salário" and valor > conta["saldo"]:
        print("Erro: Conta Salário não permite saldo negativo.")
        return False

    if conta["saldo"] >= valor:
        conta["saldo"] -= valor
        return True
    
    return False


# ------------------------------------------------------------------------------
# MODIFICAÇÃO / REFACTOR: Uso de filter() e lambda para funções da Etapa 4
# ------------------------------------------------------------------------------

def contar_da_agencia(codigo_agencia):
    # MODIFICAÇÃO: Substituted laço manual por filter + lambda para contar contas
    return len(list(filter(lambda c: c["agencia"] == codigo_agencia, contas.values())))


def nomes_titulares(conta):
    # MODIFICAÇÃO: Uso da função map() com lambda para extrair nomes de titulares por CPF
    buscar_nome = lambda cpf: cliente.buscar_por_cpf(cpf)["nome"] if cliente.buscar_por_cpf(cpf) else "?"
    return ", ".join(list(map(buscar_nome, conta["titulares"])))


def ordenar_por_titular():
    # MODIFICAÇÃO: Substituído o Bubble Sort por sorted() com chave lambda
    return sorted(contas.values(), key=lambda c: nomes_titulares(c).lower())


def descricao(conta):
    ag = agencia.buscar_por_codigo(conta["agencia"])
    nome_ag = ag["nome"] if ag else "Desconhecida"
    return (f"Agência: {conta['agencia']} ({nome_ag}) | Conta: {conta['numero']} | "
            f"Tipo: {conta['tipo']} | Titulares: [{nomes_titulares(conta)}] | Saldo: R$ {conta['saldo']:.2f}")



#  FUNÇÕES DA ETAPA 4 (Comentadas com as correções de conflito)

def listar_contas_saldo_positivo():
    """Retorna apenas as contas com saldo > 0 usando filter() e lambda."""
    return list(filter(lambda c: c["saldo"] > 0, contas.values()))


def montante_total_banco(colecao_contas=None):
    """
    MODIFICAÇÃO DE ERRO / CONFLITO:
    O código original tentava acessar conta.saldo (como atributo de objeto).
    Como as contas estão salvas como dicionários c['saldo'], isso gerava AttributeError.
    Ajustado para aceitar tanto dicionário c['saldo'] quanto fallback para o menu/web.
    """
    alvo = colecao_contas if colecao_contas is not None else contas.values()
    alvo_lista = list(alvo.values()) if isinstance(alvo, dict) else list(alvo)
    if not alvo_lista:
        return 0.0
    return reduce(lambda acc, c: acc + (c["saldo"] if isinstance(c, dict) else getattr(c, 'saldo', 0.0)), alvo_lista, 0.0)


def busca_maior_saldo(colecao_contas=None):
    """
    MODIFICAÇÃO DE ERRO / CONFLITO:
    Corrigido o erro de AttributeError na função max().
    Agora utiliza c['saldo'] ao invés de tentar ler atributos de objetos não existentes.
    """
    alvo = colecao_contas if colecao_contas is not None else contas.values()
    alvo_lista = list(alvo.values()) if isinstance(alvo, dict) else list(alvo)
    if not alvo_lista:
        return 0.0
    maior_c = max(alvo_lista, key=lambda c: c["saldo"] if isinstance(c, dict) else getattr(c, 'saldo', 0.0))
    return maior_c["saldo"] if isinstance(maior_c, dict) else getattr(maior_c, 'saldo', 0.0)


def busca_menor_saldo(colecao_contas=None):
    """
    MODIFICAÇÃO: Nova função adicionada conforme as regras da Etapa 4,
    encontrando o menor saldo via min() e lambda.
    """
    alvo = colecao_contas if colecao_contas is not None else contas.values()
    alvo_lista = list(alvo.values()) if isinstance(alvo, dict) else list(alvo)
    if not alvo_lista:
        return 0.0
    menor_c = min(alvo_lista, key=lambda c: c["saldo"] if isinstance(c, dict) else getattr(c, 'saldo', 0.0))
    return menor_c["saldo"] if isinstance(menor_c, dict) else getattr(menor_c, 'saldo', 0.0)


def obter_dados_dashboard():
    """Gera todas as métricas consolidadas para o Dashboard do Banco."""
    total_clientes = len(cliente.clientes)
    total_contas = len(contas)
    saldo_total = montante_total_banco()
    maior_saldo = busca_maior_saldo()
    menor_saldo = busca_menor_saldo()
    saldo_medio = (saldo_total / total_contas) if total_contas > 0 else 0.0

    return {
        "total_clientes": total_clientes,
        "total_contas": total_contas,
        "saldo_total": saldo_total,
        "maior_saldo": maior_saldo,
        "menor_saldo": menor_saldo,
        "saldo_medio": saldo_medio
    }