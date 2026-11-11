"""API REST do GameHub (Flask). Rodar com:  python app.py"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
from dao import JogoDAO, GeneroDAO, ErroBancoDados
from models import Jogo, ValidacaoError

app = Flask(__name__)
CORS(app)  # libera o front-end (outra porta/origem) a chamar a API

jogo_dao = JogoDAO()
genero_dao = GeneroDAO()


def erro_json(mensagem, codigo):
    return jsonify({"erro": mensagem}), codigo


def ler_json():
    """Lê o corpo JSON da requisição e garante que é um objeto."""
    try:
        dados = request.json
    except HTTPException:
        raise ValidacaoError("O corpo da requisição deve ser um JSON válido.")
    if not isinstance(dados, dict):
        raise ValidacaoError("O corpo da requisição deve ser um objeto JSON.")
    return dados


def montar_jogo(dados, id_jogo=None):
    """Valida os dados recebidos e devolve um Jogo já com seus gêneros."""
    jogo = Jogo.from_dict(dados, id_jogo)
    ids = dados.get("generos")
    if not isinstance(ids, list) or len(ids) == 0:
        raise ValidacaoError("Selecione pelo menos um gênero.")
    existentes = {}
    for genero in genero_dao.listar_todos():
        existentes[genero.id] = genero
    for item in ids:
        if not isinstance(item, int) or isinstance(item, bool) or item not in existentes:
            raise ValidacaoError("Um dos gêneros informados não existe.")
        genero = existentes[item]
        if genero not in jogo.generos:
            jogo.adicionar_genero(genero)
    return jogo


@app.route("/api/jogos", methods=["GET"])
def listar_jogos():
    try:
        jogos = jogo_dao.listar_todos()
        return jsonify([j.to_dict() for j in jogos])
    except ErroBancoDados:
        return erro_json("Erro ao acessar o banco de dados.", 500)


@app.route("/api/jogos/<int:id_jogo>", methods=["GET"])
def buscar_jogo(id_jogo):
    try:
        jogo = jogo_dao.buscar_por_id(id_jogo)
        if jogo is None:
            return erro_json("Jogo não encontrado.", 404)
        return jsonify(jogo.to_dict())
    except ErroBancoDados:
        return erro_json("Erro ao acessar o banco de dados.", 500)


@app.route("/api/jogos", methods=["POST"])
def criar_jogo():
    try:
        jogo = montar_jogo(ler_json())
        id_gerado = jogo_dao.inserir(jogo)
        return jsonify(jogo_dao.buscar_por_id(id_gerado).to_dict()), 201
    except ValidacaoError as erro:
        return erro_json(str(erro), 400)
    except ErroBancoDados:
        return erro_json("Erro ao acessar o banco de dados.", 500)


@app.route("/api/jogos/<int:id_jogo>", methods=["PUT"])
def atualizar_jogo(id_jogo):
    try:
        if jogo_dao.buscar_por_id(id_jogo) is None:
            return erro_json("Jogo não encontrado.", 404)
        jogo = montar_jogo(ler_json(), id_jogo)
        jogo_dao.atualizar(id_jogo, jogo)
        return jsonify(jogo_dao.buscar_por_id(id_jogo).to_dict())
    except ValidacaoError as erro:
        return erro_json(str(erro), 400)
    except ErroBancoDados:
        return erro_json("Erro ao acessar o banco de dados.", 500)


@app.route("/api/jogos/<int:id_jogo>", methods=["DELETE"])
def excluir_jogo(id_jogo):
    try:
        if jogo_dao.buscar_por_id(id_jogo) is None:
            return erro_json("Jogo não encontrado.", 404)
        jogo_dao.excluir(id_jogo)
        return jsonify({"mensagem": "Jogo excluído com sucesso!"})
    except ErroBancoDados:
        return erro_json("Erro ao acessar o banco de dados.", 500)


@app.route("/api/generos", methods=["GET"])
def listar_generos():
    try:
        return jsonify([g.to_dict() for g in genero_dao.listar_todos()])
    except ErroBancoDados:
        return erro_json("Erro ao acessar o banco de dados.", 500)


if __name__ == "__main__":
    app.run(debug=True)
