"""Conexão com o MySQL.

Toda a configuração do banco fica somente aqui. Ajuste os valores abaixo
para o MySQL da sua máquina antes de rodar o Flask.
"""
import mysql.connector


class Conexao:
    def __init__(self):
        self.__host = "localhost"
        self.__usuario = "root"
        self.__senha = ""   # troque pela senha do seu MySQL
        self.__banco = "gamehub"

    def conectar(self):
        """Abre e devolve uma nova conexão com o banco gamehub."""
        return mysql.connector.connect(
            host=self.__host,
            user=self.__usuario,
            password=self.__senha,
            database=self.__banco,
        )
