class Avaliacao():
    filme_id = 0
    nota = 0
    usuario_id = 0

    def __init__(self, usuario_id: int, filme_id: int, nota: float):
        self.filme_id = filme_id
        self.nota = nota
        self.usuario_id = usuario_id


def parser_linha_avaliacao(linha: str, sep=',') -> Avaliacao:
    """
    Converte uma linha de texto em uma instância de uma Avaliação
    :param linha: Linha contendo id do usuário, id do filme e nota
    :param sep: Separador dos três atributos
    :return: Nova Avaliação
    """
    uid_fid_nota = linha.split(sep)
    return Avaliacao(int(uid_fid_nota[0]), int(uid_fid_nota[1]), float(uid_fid_nota[2]))
