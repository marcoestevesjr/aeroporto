# Lista de nomes de aeroportos
airports = ['Aeroporto 1', 'Aeroporto 2', 'Aeroporto 3', 'Aeroporto 4', 'Aeroporto 5', 'Aeroporto 6']

# Matriz de adjacência que representa as rotas entre aeroportos
# Exemplo: Entre o 'Aeroporto 1' e 'Aeroporto 2' existe conexão
routes = [[False, True, False, False, True, False],
          [True, False, True, False, True, False],
          [False, True, False, True, False, False],
          [False, False, True, False, True, True],
          [True, True, False, True, False, False],
          [False, False, False, True, False, False]]

# Matriz com a duração em horas dos vôos de um determinado aeroporto para outro.
# Exemplo: Entre o 'Aeroporto 1' e 'Aeroporto 2' o tempo de viagem são de 4 horas.
duration = [[0, 4, 0, 0, 5, 0],
            [3, 0, 7, 0, 4, 0],
            [0, 5, 0, 3, 0, 0],
            [0, 0, 4, 0, 7, 9],
            [3, 2, 0, 4, 0, 0],
            [0, 0, 0, 4, 0, 0]]

# Matriz com os horários dos vôos disponíveis de um determinado aeroporto para outro.
# Exemplo: Entre o 'Aeroporto 1' e 'Aeroporto 2' os horários disponíveis são: 0h, 6h, 12h, 18h.
schedule = [[None, [0, 6, 12, 18], None, None, [3, 7, 11, 15, 19, 22], None],
            [[1, 5, 9, 13, 17, 21], None, [2, 4, 8, 15, 20, 23], None, [3, 6, 9, 12, 19], None],
            [None, [0, 6, 12, 18], None, [1, 5, 9, 13, 17, 21], None, None],
            [None, None, [3, 7, 11, 15, 19, 23], None, [3, 6, 9, 12, 19], [0, 6, 12, 18]],
            [[0, 6, 12, 18], [3, 7, 11, 15, 19, 23], None, [1, 5, 9, 13, 17, 21], None, None],
            [None, None, None, [0, 6, 12, 18], None, None]]


# Função que retorna as possíveis rotas entre dois aerportos.
# Exemplo: calculate_paths(0, 1) -> [[0, 1], [0, 4, 1], [0, 4, 3, 2, 1]]
def calculate_paths(origin, destiny, iteration=0):
    paths = []

    # A variável 'iteration' armazena o nível de profundidade que estamos na função.
    # Caso 'iteration' seja maior que o número de aeroportos, sabemos que algum foi
    # visitdo mais de uma vez, logo, encerrar o ciclo.
    if iteration >= len(routes):
        return paths
    else:
        iteration += 1

    # Verifica a existência de conexão entre origem e os demais aeroportos.
    # Caso exista uma conexão direta entre a origem e o destino, adicionar aos caminhos.
    # Senão calcula os caminhos entre os demais aeroporos e o destino, caso exista algum aeroporto repetido
    # desconsidera o caminho retornado.
    for i in range(len(routes)):

        if routes[origin][i]:
            if i == destiny:
                paths.append([origin, destiny])
            else:
                paths_from_i_to_dest = calculate_paths(i, destiny, iteration)
                for path in paths_from_i_to_dest:
                    if origin not in path:
                        paths.append([origin] + path)

    return paths


# Função que retorna a menor rota e o menor tempo de duração da viagem possíveis
# dado sua origem, horário de check-in e destino.
def calculate_best_path(origin, destiny, checkin):
    # Calcula todas as rotas possíveis entre a origem e o destino.
    paths = calculate_paths(origin, destiny)

    min_time = -1
    min_path = None

    # Para cada rota, calcula o tempo necessário para terminar a viagem.
    # Caso seja menor do que o existe, substitui.
    # Caso seja igual ao existente, substitui caso a rota seja menor.
    for path in paths:

        # A variável current_time descreve o tempo decorrido da viagem para cada caminho.
        current_time = checkin

        for i in range(len(path) - 1):

            fly_schedule = schedule[path[i]][path[i + 1]]

            waiting_time = -1

            # Verifica se existe vôo para o mesmo dia e calcula o tempo de aguardo necessário.
            for fly_time in fly_schedule:
                if fly_time >= current_time % 24:
                    waiting_time = fly_time - current_time % 24
                    break

            # Caso não exista vôo no mesmo dia, pega o primeiro vôo do dia seguinte e calcula o tempo de aguardo
            # necessário.
            if waiting_time == -1:
                waiting_time = fly_schedule[0] + (24 - current_time % 24)

            current_time += waiting_time + duration[path[i]][path[i + 1]]

        # Calcula o tempo decorrido desde a hora de checkin até sua chegada no aeroporto de destino.
        total_time = current_time - checkin

        if min_time == -1 or (min_time > total_time) or (min_time == total_time and len(min_path) > len(path)):
            min_time = total_time
            min_path = path

    return min_path, min_time


if __name__ == '__main__':
    origin = 0
    destiny = 5
    checkin = 23
    (path, duration) = calculate_best_path(origin, destiny, checkin)

    if path is None:
        print("Não existe rota de {} para {}.".format(airports[origin], airports[destiny]))
    else:
        print("A melhor rota de {} para {} é: ".format(airports[origin], airports[destiny]))
        for i in range(len(path) - 1):
            print("{} -> {}".format(airports[path[i]], airports[path[i + 1]]))
        print("Duração: {} hora(s)".format(duration))
