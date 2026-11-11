"""Acesso ao banco (padrão DAO). Só este arquivo conversa com o MySQL."""
import mysql.connector
from conexao import Conexao
from models import Jogo, Genero


class ErroBancoDados(Exception):
    """Exceção personalizada: falha ao acessar o MySQL."""

    def __init__(self, mensagem):
        super().__init__(mensagem)


class GeneroDAO:
    def __init__(self):
        self.__conexao = Conexao()

    def listar_todos(self):
        conexao = None
        try:
            conexao = self.__conexao.conectar()
            cursor = conexao.cursor()
            cursor.execute("SELECT id, nome FROM generos ORDER BY nome")
            return [Genero(*linha) for linha in cursor.fetchall()]
        except mysql.connector.Error as erro:
            raise ErroBancoDados(str(erro))
        finally:
            if conexao is not None:
                conexao.close()


class JogoDAO:
    def __init__(self):
        self.__conexao = Conexao()

    def __carregar_generos(self, cursor, id_jogo):
        """Busca os gêneros de um jogo usando INNER JOIN com a tabela associativa."""
        cursor.execute(
            "SELECT g.id, g.nome FROM generos g "
            "INNER JOIN jogo_genero jg ON jg.genero_id = g.id "
            "WHERE jg.jogo_id = %s ORDER BY g.nome",
            (id_jogo,),
        )
        return [Genero(*linha) for linha in cursor.fetchall()]

    def __ligar_generos(self, cursor, id_jogo, generos):
        for genero in generos:
            cursor.execute(
                "INSERT INTO jogo_genero (jogo_id, genero_id) VALUES (%s, %s)",
                (id_jogo, genero.id),
            )

    def listar_todos(self):
        conexao = None
        try:
            conexao = self.__conexao.conectar()
            cursor = conexao.cursor()
            cursor.execute(
                "SELECT id, titulo, desenvolvedora, ano_lancamento, descricao, imagem "
                "FROM jogos ORDER BY id"
            )
            linhas = cursor.fetchall()
            jogos = []
            for linha in linhas:
                jogo = Jogo(*linha)
                for genero in self.__carregar_generos(cursor, jogo.id):
                    jogo.adicionar_genero(genero)
                jogos.append(jogo)
            return jogos
        except mysql.connector.Error as erro:
            raise ErroBancoDados(str(erro))
        finally:
            if conexao is not None:
                conexao.close()

    def buscar_por_id(self, id_jogo):
        """Devolve o Jogo ou None se não existir."""
        conexao = None
        try:
            conexao = self.__conexao.conectar()
            cursor = conexao.cursor()
            cursor.execute(
                "SELECT id, titulo, desenvolvedora, ano_lancamento, descricao, imagem "
                "FROM jogos WHERE id = %s",
                (id_jogo,),
            )
            linhas = cursor.fetchall()
            if len(linhas) == 0:
                return None
            jogo = Jogo(*linhas[0])
            for genero in self.__carregar_generos(cursor, jogo.id):
                jogo.adicionar_genero(genero)
            return jogo
        except mysql.connector.Error as erro:
            raise ErroBancoDados(str(erro))
        finally:
            if conexao is not None:
                conexao.close()

    def inserir(self, jogo):
        """Cadastra o jogo e seus gêneros. Devolve o id gerado."""
        conexao = None
        try:
            conexao = self.__conexao.conectar()
            cursor = conexao.cursor()
            cursor.execute(
                "INSERT INTO jogos (titulo, desenvolvedora, ano_lancamento, descricao, imagem) "
                "VALUES (%s, %s, %s, %s, %s)",
                (jogo.titulo, jogo.desenvolvedora, jogo.ano_lancamento,
                 jogo.descricao, jogo.imagem),
            )
            id_gerado = cursor.lastrowid
            self.__ligar_generos(cursor, id_gerado, jogo.generos)
            conexao.commit()  # só grava tudo se nenhum comando falhou
            return id_gerado
        except mysql.connector.Error as erro:
            raise ErroBancoDados(str(erro))
        finally:
            if conexao is not None:
                conexao.close()

    def atualizar(self, id_jogo, jogo):
        conexao = None
        try:
            conexao = self.__conexao.conectar()
            cursor = conexao.cursor()
            cursor.execute(
                "UPDATE jogos SET titulo = %s, desenvolvedora = %s, ano_lancamento = %s, "
                "descricao = %s, imagem = %s WHERE id = %s",
                (jogo.titulo, jogo.desenvolvedora, jogo.ano_lancamento,
                 jogo.descricao, jogo.imagem, id_jogo),
            )
            # refaz as associações: apaga as antigas e insere as novas
            cursor.execute("DELETE FROM jogo_genero WHERE jogo_id = %s", (id_jogo,))
            self.__ligar_generos(cursor, id_jogo, jogo.generos)
            conexao.commit()
        except mysql.connector.Error as erro:
            raise ErroBancoDados(str(erro))
        finally:
            if conexao is not None:
                conexao.close()

    def excluir(self, id_jogo):
        """Apaga primeiro as ligações em jogo_genero (a FK exige) e depois o jogo."""
        conexao = None
        try:
            conexao = self.__conexao.conectar()
            cursor = conexao.cursor()
            cursor.execute("DELETE FROM jogo_genero WHERE jogo_id = %s", (id_jogo,))
            cursor.execute("DELETE FROM jogos WHERE id = %s", (id_jogo,))
            conexao.commit()
        except mysql.connector.Error as erro:
            raise ErroBancoDados(str(erro))
        finally:
            if conexao is not None:
                conexao.close()
