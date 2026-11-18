from flask import Flask, render_template, request, redirect
from agencia import Agencia

app = Flask(__name__)

# Lê o JSON só uma vez, quando o servidor liga
banco = Agencia("0001", "Central")
banco.carregar()

mensagem = ""  # última mensagem mostrada na página


def ler_valor(texto):
    texto = texto.strip().replace(",", ".")
    if texto.replace(".", "", 1).isdigit():
        return float(texto)
    return -1


@app.route("/")
def index():
    global mensagem
    msg = mensagem
    mensagem = ""

    busca = request.args.get("busca", "")
    if busca != "":
        clientes = banco.procurar_clientes(busca)
    else:
        clientes = banco.clientes_ordenados()

    return render_template("index.html", banco=banco, clientes=clientes,
                           contas=banco.contas_ordenadas(), mensagem=msg, busca=busca)


@app.route("/cliente", methods=["POST"])
def novo_cliente():
    global mensagem
    nome = request.form["nome"]
    cpf = request.form["cpf"]
    mensagem = banco.cadastrar_cliente(nome, cpf)
    if not mensagem.startswith("Erro"):
        mensagem = banco.abrir_conta(cpf, request.form["tipo"])
    return redirect("/")


@app.route("/conta", methods=["POST"])
def nova_conta():
    global mensagem
    mensagem = banco.abrir_conta(request.form["cpf"], request.form["tipo"])
    return redirect("/")


@app.route("/deposito", methods=["POST"])
def deposito():
    global mensagem
    valor = ler_valor(request.form["valor"])
    mensagem = banco.depositar(request.form["numero"], valor)
    return redirect("/")


@app.route("/saque", methods=["POST"])
def saque():
    global mensagem
    valor = ler_valor(request.form["valor"])
    mensagem = banco.sacar(request.form["numero"], valor)
    return redirect("/")


@app.route("/transferencia", methods=["POST"])
def transferencia():
    global mensagem
    valor = ler_valor(request.form["valor"])
    mensagem = banco.transferir(request.form["origem"], request.form["destino"], valor)
    return redirect("/")


@app.route("/render", methods=["POST"])
def render():
    global mensagem
    mensagem = banco.render_poupancas()
    return redirect("/")


if __name__ == "__main__":
    print("Acesse: http://127.0.0.1:5000  (aperte Ctrl+C para salvar e sair)")
    try:
        app.run(debug=True, use_reloader=False)
    finally:
        # Salva o JSON só uma vez, quando o servidor é fechado
        banco.salvar()
