from typing import List

from avaliacao import Avaliacao
from filme import Filme


def capturar_avalicao(u_id: int, filme: Filme, nota_min=0, nota_max=5) -> Avaliacao:
    pergunta = f"Se você gostou do filme exibido acima digite 'S', senão, 'N': "
    print(f"\n{filme}")
    resp = input(pergunta)

    while not resp or resp not in 'sSnN':
        resp = input(f"\nOps, não entendi!{pergunta}")

    return Avaliacao(u_id, filme.id, nota_min if resp in 'nN' else nota_max)


def capturar_avalicoes(u_id: int, filmes: List[Filme]) -> List[Avaliacao]:
    return [capturar_avalicao(u_id, filmes[i]) for i in range(len(filmes))]
