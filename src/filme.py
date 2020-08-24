import random
from typing import List


class Filme():
    generos: List[str] = []
    id = 0
    titulo = ''

    def __init__(self, titulo: str, generos: List[str], id: int):
        self.generos = generos
        self.id = id
        self.titulo = titulo

    def __str__(self):
        return f"""Título:\t\t{self.titulo}\nGêneros:\t{', '.join(self.generos)}"""


def parser_linha_filme(linha: str, sep=',', segundo_sep="\"", genero_sep='|') -> Filme:
    """
    Converte uma linha de texto em uma instância de Filme

    :param linha: Linha contendo Id, título e uma lista de gêneros
    :param sep: Separador dos três atributos (Id, título e gêneros)
    :param segundo_sep: Separador para títulos que contém virgula
    :param genero_sep: Separador da lista de gêneros
    :return: Nova instância de Filme
    """
    id_titulo_generos: List[str] = []

    if segundo_sep in linha:
        novo_sep = ';'
        linha_sep_pt_virg = linha.replace(sep + segundo_sep, novo_sep)
        linha_sep_pt_virg = linha_sep_pt_virg.replace(segundo_sep + sep, novo_sep)
        id_titulo_generos = linha_sep_pt_virg.split(novo_sep)

    else:
        id_titulo_generos = linha.split(sep)

    return Filme(
        id_titulo_generos[1], id_titulo_generos[2].split(genero_sep),
        int(id_titulo_generos[0])
    )


def sortear_filmes(filmes: List[Filme], qtd: int) -> List[Filme]:
    """
    Retorna uma lista com N filmes em ordem randômica

    :param filmes: Lista com todos filmes disponíveis para sortear
    :param qtd: Quantidade de itens a serem sorteados e retornados
    :return: Lista randomizada de filmes
    """
    total = len(filmes)
    indices_aleat = random.sample(range(0, total), min(total, qtd))
    return [filmes[i] for i in indices_aleat]
