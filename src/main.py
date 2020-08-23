import random
import time
import urllib.request
from typing import Dict

from avaliacao import *
from filme import Filme, parser_linha_filme


def popular_filmes(csv_path: str) -> List[Filme]:
    with urllib.request.urlopen(csv_path) as csv:
        linhas = csv.readlines()
        del linhas[0]
        return [parser_linha_filme(l.decode('utf8')) for l in linhas]


def popular_avaliacoes(csv_path: str) -> List[Avaliacao]:
    with urllib.request.urlopen(csv_path) as csv:
        linhas = csv.readlines()
        del linhas[0]
        return [parser_linha_avaliacao(l.decode('utf8')) for l in linhas]


def sortear_filmes(filmes: List[Filme], qtd: int) -> List[Filme]:
    total = len(filmes)
    indices_aleat = random.sample(range(0, total), min(total, qtd))
    print(indices_aleat)
    return [filmes[i] for i in indices_aleat]


def capturar_avalicao(u_id: int, filme: Filme, nota_min=0, nota_max=5) -> Avaliacao:
    pergunta = f"Se você gostou do filme exibido acima digite 'S', senão, 'N': "
    print(f"\n{filme}")
    resp = input(pergunta)

    while not resp or resp not in 'sSnN':
        resp = input(f"\nOps, não entendi!{pergunta}")

    return Avaliacao(u_id, filme.id, nota_min if resp in 'nN' else nota_max)


def capturar_avalicoes(u_id: int, filmes: List[Filme]) -> List[Avaliacao]:
    return [capturar_avalicao(u_id, filmes[i]) for i in range(len(filmes))]


def filtro_colab_bool(
        filmes: List[Filme], avaliacoes: List[Avaliacao],
        minhas_avals: List[Avaliacao], meu_usuario_id: int,
        n_recom=10
) -> List[Filme]:
    # Inicialize o par Filme-Pontuação com zero para todos filmes
    filme_id_score: Dict[int, int] = {f.id: 0 for f in filmes}

    # Inicialize um dicionário c/ o Id de cada usuário e sua similidade
    # com as preferências do usuário atual
    u_id_simil: Dict[int, int] = {a.usuario_id: 0 for a in avaliacoes}

    # Inicialize um dicionário c/ o Id de cada usuário e suas avaliações
    u_id_avals: Dict[int, List[Avaliacao]] = {
        id: filtrar_por_usuario(avaliacoes, id) for id in u_id_simil
    }

    # Inicialize um dicionário c/ o Id de cada filme e suas avaliações
    f_id_avals: Dict[int, List[Avaliacao]] = {
        a.filme_id: filtrar_por_filme(avaliacoes, a.filme_id)
        for a in minhas_avals
    }

    # Itere sobre cada avaliação do usuário
    for minha_a in minhas_avals:
        for outra_a in f_id_avals[minha_a.filme_id]:
            if outra_a.usuario_id != meu_usuario_id and outra_a.gostou == minha_a.gostou:
                u_id_simil[outra_a.usuario_id] += 1

    for u_id in u_id_simil:
        if u_id_simil[u_id] > 0 and u_id != meu_usuario_id:
            for aval in u_id_avals[u_id]:
                if aval.gostou:
                    filme_id_score[aval.filme_id] += 1

    par_filme_nota = [(f_id, filme_id_score[f_id]) for f_id in filme_id_score if filme_id_score[f_id]]
    par_filme_nota.sort(key=lambda f: f[1], reverse=True)
    par_filme_nota = par_filme_nota[:n_recom]

    for f_n in par_filme_nota:
        print([f for f in filmes if f.id == f_n[0]][0])
        print("Nota:", f_n[1])

    # ordernar lista de filmes pelo score decrescente e retornar os N
    return []


def main():
    start_filme_leitura = time.time()
    filmes: List[Filme] = popular_filmes(
        'https://raw.githubusercontent.com/duraes-antonio/sistema_recom_collab_filtering/master/data/ml-latest-small/movies.csv')
    end_filme_leitura = time.time()
    print(f"Filme leitura: {end_filme_leitura - start_filme_leitura}")

    start_aval_leitura = time.time()
    avaliacoes: List[Avaliacao] = popular_avaliacoes(
        'https://raw.githubusercontent.com/duraes-antonio/sistema_recom_collab_filtering/master/data/ml-latest-small/ratings.csv'
    )
    end_aval_leitura = time.time()
    print(f"Aval leitura: {end_aval_leitura - start_aval_leitura}")

    usuario_id = 9666
    minhas_avals = capturar_avalicoes(usuario_id, sortear_filmes(filmes, 10))
    avaliacoes.extend(minhas_avals)

    start_filter = time.time()
    filtro_colab_bool(filmes, avaliacoes, minhas_avals, usuario_id, 5)
    end_filter = time.time()
    print(f"Colab: {end_filter - start_filter}")

    return 0


main()
