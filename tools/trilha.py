# Oficina Flutter 2 · a trilha didática: põe cada desafio logo depois da parte que ele consolida e
# guarda os pré-requisitos de cada aula (a linha "Você vai usar" mostrada na aula).

# desafio, aula depois da qual ele entra, nome do grupo no menu de aulas
DESAFIOS = [
    ('Desafio · Relógio de reação', 'Projeto · Pula-Caixa', 'Desafio 1 · Relógio de reação'),
    ('Desafio · Cobrinha do caramelo', 'Teclado: setas e espaço', 'Desafio 2 · Cobrinha do caramelo'),
    ('Desafio · Quebra-blocos', 'Desafio · Cobrinha do caramelo', 'Desafio 3 · Quebra-blocos'),
    ('Desafio · Jogo da memória', 'Projeto · Pega-Maçã', 'Desafio 4 · Jogo da memória'),
    ('Desafio · Caramelo voador', 'Projeto · Pula-Caixa em Flame', 'Desafio 5 · Caramelo voador'),
]

LACO = 'O laço do jogo com Timer.periodic'
TICKER = 'Ticker e delta time'
PINTOR = 'Desenhando o jogo com CustomPainter'
LISTAS = 'Muitos objetos: lista, sorteio e remoção'
AABB = 'Colisão com retângulos (AABB)'
ESTADOS = 'Estados do jogo: pronto, jogando e fim'
HIVE = 'Salvar o jogo: recorde com Hive'

# aula: aulas anteriores que ela usa (as mais importantes, no máximo 3)
USA = {
    'Ticker e delta time': [LACO],
    'Desenhando o jogo com CustomPainter': [TICKER],
    'Toque: o personagem vai até o dedo': [PINTOR],
    'Matemática de jogos: física e passo de tempo': [TICKER],
    'Gravidade e pulo': ['Matemática de jogos: física e passo de tempo', 'Toque: o personagem vai até o dedo'],
    'Muitos objetos: lista, sorteio e remoção': ['Gravidade e pulo'],
    'Colisão com retângulos (AABB)': [LISTAS],
    'Estados do jogo: pronto, jogando e fim': [AABB],
    'Game design: objetivo, desafio e recompensa': [ESTADOS],
    'Projeto · Pula-Caixa': ['Gravidade e pulo', AABB, ESTADOS],
    'Desafio · Relógio de reação': [ESTADOS, LISTAS],
    'Matemática de jogos: vetores': ['Toque: o personagem vai até o dedo'],
    'Arrastar: a raquete segue o dedo': ['Matemática de jogos: vetores', PINTOR],
    'Arremessar: a velocidade do arrasto': ['Arrastar: a raquete segue o dedo', 'Gravidade e pulo'],
    'Matemática de jogos: ângulos, seno e cosseno': ['Matemática de jogos: vetores'],
    'Teclado: setas e espaço': [ESTADOS],
    'Desafio · Cobrinha do caramelo': [LACO, PINTOR, 'Arremessar: a velocidade do arrasto'],
    'Desafio · Quebra-blocos': [TICKER, 'Arrastar: a raquete segue o dedo', AABB],
    'Sprites: imagens no Canvas': [PINTOR, 'Arte de jogos: pixel art e paletas'],
    'Arte de jogos: princípios de animação': ['Sprites: imagens no Canvas'],
    'Animação com folha de sprites': ['Sprites: imagens no Canvas', 'Arte de jogos: princípios de animação'],
    'Som: efeitos com audioplayers': ['Som de jogos: efeitos e música'],
    'Texto de jogo: contorno, sombra e fonte': [PINTOR],
    'Efeitos visuais: degradê, brilho e sombra': [PINTOR],
    'Game design: dificuldade e curva de aprendizado': ['Game design: objetivo, desafio e recompensa'],
    'Projeto · Pega-Maçã': ['Animação com folha de sprites', 'Som: efeitos com audioplayers', 'Game design: dificuldade e curva de aprendizado'],
    'Desafio · Jogo da memória': [ESTADOS, LISTAS],
    'Programação de jogos: Flutter puro ou Flame?': [PINTOR, TICKER],
    'Flame: o primeiro jogo': ['Programação de jogos: Flutter puro ou Flame?', TICKER],
    'Flame: sprites e animação': ['Flame: o primeiro jogo', 'Animação com folha de sprites'],
    'Flame: toque e arrasto em componentes': ['Flame: o primeiro jogo', 'Arrastar: a raquete segue o dedo'],
    'Matemática de jogos: colisão em detalhes': [AABB],
    'Flame: colisões com hitboxes': ['Flame: o primeiro jogo', 'Matemática de jogos: colisão em detalhes'],
    'Flame: teclado, mundo e câmera': ['Teclado: setas e espaço', 'Flame: colisões com hitboxes'],
    'Projeto · Pula-Caixa em Flame': ['Projeto · Pula-Caixa', 'Flame: colisões com hitboxes', 'Flame: teclado, mundo e câmera'],
    'Desafio · Caramelo voador': ['Flame: sprites e animação', 'Flame: toque e arrasto em componentes', 'Flame: colisões com hitboxes'],
    'Matemática de jogos: interpolação e curvas': ['Matemática de jogos: vetores'],
    'Flame: efeitos': ['Matemática de jogos: interpolação e curvas', 'Flame: o primeiro jogo'],
    'Flame: partículas': ['Flame: efeitos'],
    'Flame: paralaxe': ['Flame: teclado, mundo e câmera'],
    'Flame: overlays, pausa e música': ['Flame: o primeiro jogo', 'Som: efeitos com audioplayers'],
    'Flame: obstáculos que giram e consultas': ['Matemática de jogos: ângulos, seno e cosseno', 'Flame: colisões com hitboxes'],
    'Pinça: zoom com dois dedos': ['Arrastar: a raquete segue o dedo'],
    'Game design: game feel e "suco"': ['Flame: efeitos', 'Flame: partículas'],
    'Projeto · Céu Agitado': ['Flame: partículas', 'Flame: paralaxe', 'Flame: overlays, pausa e música'],
    'Joystick e botões na tela': ['Arte de jogos: interface e acessibilidade', 'Flame: teclado, mundo e câmera'],
    'Efeitos de cor e de caminho': ['Efeitos visuais: degradê, brilho e sombra'],
    'Forge2D: corpos, gravidade e quiques': ['Matemática de jogos: física e passo de tempo', 'Flame: o primeiro jogo'],
    'Forge2D: impulsos e contatos': ['Forge2D: corpos, gravidade e quiques'],
    'Forge2D: juntas e raio': ['Forge2D: impulsos e contatos'],
    'Sensores: inclinar o celular': ['Matemática de jogos: vetores'],
    'Tiled: mapas prontos': ['Flame: teclado, mundo e câmera'],
    'Inimigos que pensam: estados': [ESTADOS, 'Tiled: mapas prontos'],
    'Salvar o jogo: recorde com Hive': [ESTADOS],
    'Ranking online com Supabase': [HIVE],
    'Projeto · Caça-Ossos': ['Joystick e botões na tela', 'Inimigos que pensam: estados', HIVE],
    'Navegação: menu, fases e pausa': ['Flame: overlays, pausa e música'],
    'Game design: design de fases e ritmo': ['Game design: dificuldade e curva de aprendizado'],
    'Plataforma: gravidade e colisão com o mapa': ['Gravidade e pulo', 'Tiled: mapas prontos'],
    'Fases e estrelas: progresso com Hive': [HIVE, 'Navegação: menu, fases e pausa'],
    'Game design: economia e balanceamento': ['Game design: dificuldade e curva de aprendizado'],
    'Matemática de jogos: probabilidade e sorteio': [LISTAS],
    'Geração procedural: semente, labirinto e cavernas': ['Matemática de jogos: probabilidade e sorteio'],
    'Caminho até o alvo: BFS e A*': ['Geração procedural: semente, labirinto e cavernas'],
    'Desempenho: medir FPS e reaproveitar objetos': ['Flame: partículas'],
    'Programação de jogos: arquitetura em camadas': ['Navegação: menu, fases e pausa'],
    'Multijogador em tempo real com Supabase': ['Ranking online com Supabase'],
    'Game design: testar com jogadores': ['Game design: objetivo, desafio e recompensa'],
    'Projeto · Trilha do Caramelo': ['Navegação: menu, fases e pausa', 'Plataforma: gravidade e colisão com o mapa', 'Fases e estrelas: progresso com Hive'],
    'Diálogos e escolhas': ['Game design: narrativa e personagens', LACO],
    'Inventário e itens salvos em JSON': [HIVE],
    'Game design: ética e bem-estar do jogador': ['Matemática de jogos: probabilidade e sorteio'],
    'Conquistas': [HIVE, 'Game design: ética e bem-estar do jogador'],
    'Bando: comportamento de grupo': ['Matemática de jogos: vetores', TICKER],
    'Conta do jogador e progresso na nuvem': ['Ranking online com Supabase'],
    'Tradução: o jogo em vários idiomas': ['Diálogos e escolhas'],
    'Game design: analisar um jogo (MDA)': ['Game design: objetivo, desafio e recompensa'],
    'Programação de jogos: recursão': [PINTOR],
    'IA de turnos: o gato que pensa (minimax)': ['Programação de jogos: recursão', ESTADOS],
    'Quebra-cabeça em grade: combinar 3': [LISTAS, 'Desafio · Jogo da memória'],
    'Quebra-cabeça com desfazer: empurrar caixas': [LISTAS, 'Arremessar: a velocidade do arrasto'],
    'Câmera: seguir, limites e tremor': ['Flame: teclado, mundo e câmera', 'Matemática de jogos: interpolação e curvas', 'Game design: game feel e "suco"'],
    'Salvar o jogo inteiro: espaços de save': ['Inventário e itens salvos em JSON'],
    'Replay e fantasma: gravar as entradas': ['Matemática de jogos: física e passo de tempo', TICKER],
    'Jogo de ritmo: acertar na batida': ['Som: efeitos com audioplayers', TICKER],
    'Campo de visão e névoa de guerra': ['Caminho até o alvo: BFS e A*', PINTOR],
    'Projeto · Torres do Caramelo': ['Caminho até o alvo: BFS e A*', 'Desempenho: medir FPS e reaproveitar objetos', 'Game design: economia e balanceamento'],
    'Projeto final: o seu jogo': ['Game design: objetivo, desafio e recompensa', 'Game design: testar com jogadores'],
    'Carreira: game jams, portfólio e mercado': ['Produção: publicar o jogo'],
    'Sala de jogos (galeria)': ['Projeto final: o seu jogo'],
}


def reorganizar(LESSONS, PARTS):
    titulos = [L['t'] for L in LESSONS]
    for desafio, depois, grupo in DESAFIOS:
        i = titulos.index(desafio)
        L = LESSONS.pop(i)
        titulos.pop(i)
        j = titulos.index(depois) + 1
        LESSONS.insert(j, L)
        titulos.insert(j, desafio)
        PARTS.append([desafio, grupo])
    # a Parte 10 agora é só o projeto final (leitura do projeto, carreira e sala de jogos)
    PARTS.append(['Projeto final: o seu jogo', 'Parte 10 · Projeto final'])
    PARTS.sort(key=lambda p: titulos.index(p[0]))
    for t, us in USA.items():
        assert t in titulos, f'trilha: aula "{t}" não existe'
        for u in us:
            assert u in titulos, f'trilha: "{t}" usa "{u}", que não existe'
            assert titulos.index(u) < titulos.index(t), f'trilha: "{t}" usa "{u}", que vem depois'
