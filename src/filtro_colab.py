from typing import List, Dict, Tuple

from avaliacao import Avaliacao
from filme import Filme


def filtro_colab(
        minhas_avals: List[Avaliacao], meu_usuario_id: int,
        f_id_filme: Dict[int, Filme], u_id_avaliacoes: Dict[int, List[Avaliacao]],
        f_id_avaliacoes: Dict[int, List[Avaliacao]], n_recom=5
) -> List[Tuple[Filme, int]]:
    f_id_score: Dict[int, int] = {}
    u_id_simil: Dict[int, int] = {}
    id_filmes_vistos = [a.filme_id for a in minhas_avals]

    # Itere sobre cada avaliação do usuário alvo
    for a in minhas_avals:

        # Para cada avaliação de outros usuários, se o autor não for o
        # usuário alvo e o aprovação for igual à da avaliação do usuário
        # alvo, incremente a similaridade com esse autor
        for f_aval in f_id_avaliacoes[a.filme_id]:
            if f_aval.usuario_id != meu_usuario_id and f_aval.gostou == a.gostou:
                if f_aval.usuario_id in u_id_simil:
                    u_id_simil[f_aval.usuario_id] += 1
                else:
                    u_id_simil[f_aval.usuario_id] = 1

    for u_id in u_id_simil:
        # Para cada avaliação do usuário similar atual, se o autor gostou
        # do filme avaliado, então incremente a chance de recomendá-lo
        for a in u_id_avaliacoes[u_id]:
            if a.gostou and a.filme_id not in id_filmes_vistos:
                if a.filme_id in f_id_score:
                    f_id_score[a.filme_id] += 1
                else:
                    f_id_score[a.filme_id] = 1

    # Gere uma lista de tuplas no formato (filme_id, score) e ordene dec.
    pares_filme_nota = [(f_id, f_id_score[f_id]) for f_id in f_id_score]
    pares_filme_nota.sort(key=lambda f: f[1], reverse=True)

    # Retorne uma lista com N tuplas no formato (Filme, score)
    return [(f_id_filme[f_id_nota[0]], f_id_nota[1]) for f_id_nota in pares_filme_nota[:n_recom]]
