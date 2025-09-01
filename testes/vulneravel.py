import sqlite3
import os
import subprocess
from flask import Flask, request

app = Flask(__name__)

def login(usuario, senha):
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE usuario = '{usuario}' AND senha = '{senha}'" 
    result = cursor.fetchall()
    conn.close()
    return result


def listar_diretorio(path):
    comando = f"ls {path}"
    return subprocess.getoutput(comando)


API_KEY = "12345-super-secreta"

def usar_chave():
    return f"Usando a chave secreta: {API_KEY}"


@app.route("/ler_arquivo", methods=["GET"])
def ler_arquivo():
    nome = request.args.get("file", "")
    with open(nome, "r") as f:
        return f.read()


@app.route("/comentar", methods=["POST"])
def comentar():
    comentario = request.form["comentario"]
    return f"<h1>Comentário recebido:</h1><p>{comentario}</p>"


def calcular(expressao):
    return eval(expressao)


if __name__ == "__main__":
    app.run(debug=True)
