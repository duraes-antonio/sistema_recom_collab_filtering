import urllib.request
from typing import List

from avaliacao import Avaliacao, parser_linha_avaliacao, agrupar_por_filme, agrupar_por_autor
from filme import Filme, parser_linha_filme, sortear_filmes
from filtro_colab import filtro_colab
from util_entrada import capturar_avalicoes


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


def main():
    url_gh = 'https://raw.githubusercontent.com/duraes-antonio/sistema_recom_collab_filtering/master/data/ml-latest-small'
    usuario_id = 9666

    print('#Lendo arquivo de filmes...')
    filmes: List[Filme] = popular_filmes(f'{url_gh}/movies.csv')

    print('#Lendo arquivo de avaliações...')
    avaliacoes: List[Avaliacao] = popular_avaliacoes(f'{url_gh}/ratings.csv')

    # Converta a lista de filmes em um dicionário <id_filme, Filme>
    print('#Convertendo lista de filmes para dicionário...')
    dict_filme = {f.id: f for f in filmes}

    # Converta a lista de avaliações em um dicionário <id_filme, [Avaliações]>
    print('#Agrupando avaliações por filmes...')
    dict_f_id_avals = agrupar_por_filme(avaliacoes)

    # Converta a lista de avaliações em um dicionário <id_autor, [Avaliações]>
    print('#Agrupando avaliações por autor...')
    dict_u_id_avals = agrupar_por_autor(avaliacoes)

    minhas_avals = capturar_avalicoes(usuario_id, sortear_filmes(filmes, 10))

    recomendacoes = filtro_colab(minhas_avals, usuario_id, dict_filme, dict_u_id_avals, dict_f_id_avals)

    print('\n-> Filmes sugeridos:')
    for filme, nota in recomendacoes:
        print(f"{filme}Score:\t\t{nota}\n")

    return 0


main()
