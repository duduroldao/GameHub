"""Classes do domínio do GameHub (o que o Diagrama de Classes descreve)."""
from abc import ABC, abstractmethod


class ValidacaoError(Exception):
    """Exceção personalizada: dados inválidos para criar/alterar uma entidade."""

    def __init__(self, mensagem):
        super().__init__(mensagem)


class Entidade(ABC):
    """Classe abstrata: todo objeto do sistema tem id e sabe virar dicionário."""

    def __init__(self, id=None):
        self.__id = id

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, valor):
        self.__id = valor

    @abstractmethod
    def to_dict(self):
        """Cada classe filha decide como se converte em dicionário (polimorfismo)."""
        pass


class Genero(Entidade):
    def __init__(self, id, nome):
        super().__init__(id)
        self.__nome = nome

    @property
    def nome(self):
        return self.__nome

    def to_dict(self):
        return {"id": self.id, "nome": self.__nome}


class Jogo(Entidade):
    ANO_MINIMO = 1970
    ANO_MAXIMO = 2100

    def __init__(self, id, titulo, desenvolvedora, ano_lancamento,
                 descricao, imagem="padrao.png", generos=None):
        super().__init__(id)
        # As atribuições abaixo passam pelos setters (que validam os dados).
        self.titulo = titulo
        self.desenvolvedora = desenvolvedora
        self.ano_lancamento = ano_lancamento
        self.descricao = descricao
        self.imagem = imagem
        self.__generos = generos if generos is not None else []

    # ---------- getters e setters com validação ----------
    @property
    def titulo(self):
        return self.__titulo

    @titulo.setter
    def titulo(self, valor):
        if not isinstance(valor, str) or valor.strip() == "":
            raise ValidacaoError("O título é obrigatório.")
        if len(valor.strip()) > 100:
            raise ValidacaoError("O título deve ter no máximo 100 caracteres.")
        self.__titulo = valor.strip()

    @property
    def desenvolvedora(self):
        return self.__desenvolvedora

    @desenvolvedora.setter
    def desenvolvedora(self, valor):
        if not isinstance(valor, str) or valor.strip() == "":
            raise ValidacaoError("A desenvolvedora é obrigatória.")
        if len(valor.strip()) > 100:
            raise ValidacaoError("A desenvolvedora deve ter no máximo 100 caracteres.")
        self.__desenvolvedora = valor.strip()

    @property
    def ano_lancamento(self):
        return self.__ano_lancamento

    @ano_lancamento.setter
    def ano_lancamento(self, valor):
        try:
            ano = int(valor)
        except (ValueError, TypeError):
            raise ValidacaoError("O ano de lançamento deve ser um número inteiro.")
        if ano < Jogo.ANO_MINIMO or ano > Jogo.ANO_MAXIMO:
            raise ValidacaoError(
                f"O ano de lançamento deve estar entre {Jogo.ANO_MINIMO} e {Jogo.ANO_MAXIMO}."
            )
        self.__ano_lancamento = ano

    @property
    def descricao(self):
        return self.__descricao

    @descricao.setter
    def descricao(self, valor):
        if not isinstance(valor, str) or len(valor.strip()) < 10:
            raise ValidacaoError("A descrição deve ter pelo menos 10 caracteres.")
        self.__descricao = valor.strip()

    @property
    def imagem(self):
        return self.__imagem

    @imagem.setter
    def imagem(self, valor):
        if valor is None or str(valor).strip() == "":
            valor = "padrao.png"
        valor = str(valor).strip()
        if "/" in valor or "\\" in valor:
            raise ValidacaoError("Informe apenas o nome do arquivo da imagem (ex.: capa.png).")
        if len(valor) > 255:
            raise ValidacaoError("O nome da imagem é muito longo.")
        self.__imagem = valor

    @property
    def generos(self):
        return self.__generos

    # ---------- comportamentos ----------
    def adicionar_genero(self, genero):
        self.__generos.append(genero)

    def to_dict(self):
        lista_generos = []
        for genero in self.__generos:
            lista_generos.append(genero.to_dict())
        return {
            "id": self.id,
            "titulo": self.__titulo,
            "desenvolvedora": self.__desenvolvedora,
            "ano_lancamento": self.__ano_lancamento,
            "descricao": self.__descricao,
            "imagem": self.__imagem,
            "generos": lista_generos,
        }

    @classmethod
    def from_dict(cls, dados, id=None):
        """Cria um Jogo a partir do JSON recebido (os gêneros são ligados depois)."""
        return cls(
            id,
            dados.get("titulo"),
            dados.get("desenvolvedora"),
            dados.get("ano_lancamento"),
            dados.get("descricao"),
            dados.get("imagem"),
        )
