from flask import Flask, render_template, jsonify
import agencia
import cliente
import conta
import menu

app = Flask(__name__, template_folder='templates', static_folder='static')

# Carrega os dados persistidos do JSON na inicialização
menu.carregar_json()

@app.route('/')
def dashboard():
    metrics = conta.obter_dados_dashboard()
    clientes_list = list(cliente.clientes.values())
    agencias_list = list(agencia.agencias.values())
    contas_positivas = conta.listar_contas_saldo_positivo()
    
    return render_template(
        'index.html',
        metrics=metrics,
        clientes=clientes_list,
        agencias=agencias_list,
        contas_positivas=contas_positivas
    )

if __name__ == '__main__':
    print(" Servidor Web rodando em: http://127.0.0.1:5000")
    app.run(debug=True)