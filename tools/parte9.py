# Parte 9 da Oficina Flutter 2: mais gêneros e técnicas (IA de turnos, quebra-cabeças em grade, câmera,
# salvar o jogo inteiro, replay, ritmo, campo de visão) e o Projeto 7 · Torres do Caramelo.
import pathlib
import solucoes

PASTA = pathlib.Path(__file__).resolve().parent / 'parte9'
PARTE = 'Parte 9 · Mais gêneros e técnicas'


def codigo(nome):
    c = (PASTA / (nome + '.dart')).read_text(encoding='utf-8')
    assert "'''" not in c
    return '\n' + c


SETUP_HIVE = 'No terminal do projeto:\n  flutter pub add hive_flutter\n\nNo simulador as caixas do Hive ficam guardadas neste navegador (↺ Reiniciar apaga).'


def adicionar(aula, PARTS, SETUP_FLAME):
    aula(
        'IA de turnos: o gato que pensa (minimax)',
        'Em jogos de turno (jogo da velha, damas, xadrez), o computador pode escolher a jogada imaginando o futuro. O '
        'minimax experimenta cada jogada possível, depois cada resposta do adversário, e assim por diante, como uma árvore. '
        'No fim de cada galho dá uma nota: +10 se o gato vence, -10 se o caramelo vence, 0 se empata. Subindo a árvore, na '
        'vez do gato fica a MAIOR nota dos filhos (ele escolhe o melhor para si) e na vez do caramelo fica a MENOR (o gato '
        'supõe que você jogará bem). Para não pensar em milhares de posições à toa, a poda alfa-beta para de olhar um galho '
        'assim que fica claro que o outro jogador nunca deixaria a partida chegar lá. A dificuldade vira um número: '
        'olharFrente diz quantas jogadas o gato imagina; com 1 ele só vê o óbvio, com 9 ele nunca perde. A função '
        'experimenta a jogada no próprio tabuleiro e desfaz logo depois (t[i] = \'\'), em vez de copiar a lista a cada passo.',
        'Em ▶ Testar, jogue algumas partidas com o gato pensando 9 jogadas à frente (tente empatar) e depois com 1 ou 2. '
        'Leia no aviso quantas posições ele analisou. Depois deixe o gato distraído, mude o padrão de dificuldade e troque o rival.',
        codigo('velha'),
        [
            ['Gato distraído', 'Troque final double chanceDeErro = 0.0 por 0.3: em 30% das vezes o gato joga ao acaso.', r'chanceDeErro\s*=\s*(?!0(?:\.0+)?\s*;)[\d.]+\s*;'],
            ['Dificuldade inicial', 'Troque int olharFrente = 9 por 3: o jogo começa num nível médio.', r'int olharFrente\s*=\s*(?!9\b)\d+'],
            ['Outro rival', "Troque const gato = '🐱' por const gato = '🐭'.", r"const gato\s*=\s*'(?!🐱')[^']+'"],
        ],
    )
    PARTS.append(['IA de turnos: o gato que pensa (minimax)', PARTE])

    aula(
        'Quebra-cabeça em grade: combinar 3',
        'Os jogos de combinar 3 guardam o tabuleiro numa lista só: a casa da linha l e coluna c fica no índice '
        'l * colunas + c. Trocar duas peças vizinhas só vale se formar uma fileira de 3 ou mais iguais; se não formar, a '
        'troca é desfeita. Achar as fileiras é percorrer cada linha (e depois cada coluna) contando quantas peças iguais '
        'vêm em seguida; quando a sequência quebra e tinha 3 ou mais, todas entram num Set (um Set não repete a casa que '
        'faz parte de uma fileira na linha e outra na coluna). Depois as peças somem, as de cima caem para ocupar os '
        'buracos e peças novas entram pelo topo. As que caíram podem formar outra fileira: é a cascata, e cada rodada a '
        'mais é um combo que multiplica os pontos. A cascata é uma função async que espera um pouco entre os passos, '
        'para dar tempo de ver, e chama a si mesma no fim até a grade se acalmar. A grade começa sem fileiras prontas: '
        'enquanto houver alguma, as peças dela são sorteadas de novo.',
        'Em ▶ Testar, toque numa peça e depois numa vizinha para trocar. Procure cascatas (combo x2, x3). Depois acrescente '
        'uma peça nova, mude os pontos do combo e o número de jogadas.',
        codigo('combina'),
        [
            ['Mais variedade', "Acrescente '🐟' na lista pecas: com 6 tipos, as combinações ficam mais difíceis.", r"const pecas = \[(?:\s*'[^']+',?){6,}\s*\]"],
            ['Pontos do combo', 'Troque achadas.length * 10 * combo por achadas.length * 25 * combo.', r'achadas\.length\s*\*\s*(?!10\b)\d+\s*\*\s*combo'],
            ['Partida mais longa', 'Troque final int jogadasPorPartida = 20 por 30.', r'jogadasPorPartida\s*=\s*(?!20\b)\d+'],
        ],
    )

    solucoes.MANUAL[('Quebra-cabeça em grade: combinar 3', 0)] = [("const pecas = ['🦴', '🐾', '⚽', '🍖', '🧶'];", "const pecas = ['🦴', '🐾', '⚽', '🍖', '🧶', '🐟'];")]

    aula(
        'Quebra-cabeça com desfazer: empurrar caixas',
        'Num quebra-cabeça de empurrar caixas, um erro pode prender uma caixa no canto para sempre. Por isso esses jogos '
        'têm o botão desfazer, e ele é uma pilha: antes de cada movimento, o jogo empilha uma "foto" do estado (onde estão o '
        'caramelo e as caixas); desfazer desempilha a última foto e volta para ela. A foto precisa ser uma cópia '
        '(Set<int>.from(caixas)): se guardasse o próprio Set, ela mudaria junto com o jogo e não serviria para voltar. As '
        'fases são texto, uma linha por fileira (# parede, . tapete, C caixa, @ caramelo), o que deixa fácil desenhar fases '
        'novas. O caramelo empurra, mas não puxa, e só empurra uma caixa por vez: se atrás dela houver parede ou outra '
        'caixa, nada acontece. A fase acaba quando todas as caixas estão em tapetes (caixas.every(...)).',
        'Em ▶ Testar, resolva as três fases usando as setas (ou arrastando o dedo) e use ↶ Desfazer quando errar. Depois '
        'limite o desfazer, crie uma fase nova e troque o desenho da caixa.',
        codigo('caixas'),
        [
            ['Desfazer limitado', 'Troque final int limiteDesfazer = 999 por 5: a pilha guarda só os 5 últimos movimentos.', r'limiteDesfazer\s*=\s*(?!999\b)\d+'],
            ['Fase nova', "Acrescente uma quarta fase na lista fases (uma lista de textos com #, ., C e @), com pelo menos uma caixa e um tapete.", r"const fases = \[(?:\s*\[[^\]]*\],?){4,}"],
            ['Outra caixa', "Troque const caixa = '📦' por const caixa = '🦴'.", r"const caixa\s*=\s*'(?!📦')[^']+'"],
        ],
    )
    solucoes.MANUAL[('Quebra-cabeça com desfazer: empurrar caixas', 1)] = [(
        "    '########',\n  ],\n];",
        "    '########',\n  ],\n  [\n    '######',\n    '#@ C.#',\n    '# C .#',\n    '######',\n  ],\n];")]

    aula(
        'Câmera: seguir, limites e tremor',
        'A câmera decide o que o jogador vê, e o jeito de ela andar muda a sensação do jogo. Grudada no herói (direto), '
        'ela repete cada tranco do movimento. Suave, ela anda a cada quadro uma fração do caminho até o alvo '
        '(foco += (alvo - foco) * suavidade * dt): rápido quando está longe, devagar quando está perto. Olhar à frente '
        'desloca o alvo para o lado em que o herói corre, mostrando mais do que vem pela frente. A zona morta deixa o herói '
        'andar num retângulo no meio da tela sem mexer a câmera, o que evita que ela balance com pequenos passos. Em '
        'todos os modos, o foco é limitado (clamp) às bordas do mundo, para nunca mostrar o vazio fora do mapa. O tremor '
        'soma ao foco um empurrão aleatório que diminui a cada quadro; a força é tremor ao quadrado, então tremores fracos '
        'quase não aparecem e os fortes chacoalham. É um dos truques de "suco" mais baratos: aterrissagens fortes e o botão '
        '💥 usam tremer(...).',
        'Em ▶ Testar, ande com ◀ ▶, pule com ⤒ e troque o modo da câmera no 🎥 para comparar. Toque 💥 para tremer. Depois '
        'deixe a câmera mais preguiçosa, olhe mais longe e aumente o tremor.',
        codigo('camera'),
        [
            ['Câmera preguiçosa', 'Troque final double suavidade = 4 por 1.5.', r'double suavidade\s*=\s*(?!4\s*;)[\d.]+'],
            ['Olhar mais longe', 'Troque caramelo.direcao * 140 por caramelo.direcao * 220.', r'caramelo\.direcao\s*\*\s*(?!140\b)\d+'],
            ['Tremor forte', 'Troque tremor * tremor * 18 por tremor * tremor * 30.', r'tremor\s*\*\s*tremor\s*\*\s*(?!18\b)\d+'],
            ['Zona morta larga', 'Troque final double zonaMorta = 80 por 130.', r'zonaMorta\s*=\s*(?!80\b)\d+'],
        ],
        lim='No simulador o tremor e a câmera funcionam como no Flame; os botões aceitam mouse e dedo.',
        setup=SETUP_FLAME,
    )

    aula(
        'Salvar o jogo inteiro: espaços de save',
        'Salvar um recorde é guardar um número; salvar o jogo é guardar tudo o que precisa voltar igual: posição, fase, '
        'passos e quais ossos ainda estão no chão. O caminho é o mesmo da mochila: o estado vira um Map (paraJson), o Map '
        'vira texto (jsonEncode) e o texto vai para o Hive, numa chave por espaço de save ("auto", "1", "2"...). Carregar '
        'é o contrário (jsonDecode) e cada campo volta para o seu lugar. Cada save leva uma versão: quando o jogo muda e o '
        'save ganha campos novos, o código de carregar sabe completar o que falta nos saves antigos em vez de quebrar '
        '(aqui, os saves da versão 1 não tinham passos). O cartão de cada espaço mostra um resumo (fase, ossos, data) sem '
        'carregar o jogo. O espaço automático é salvo por um Timer.periodic, para o jogador não perder tudo se fechar o '
        'jogo sem salvar.',
        'Em ▶ Testar, ande, salve no espaço 1, ande mais e carregue de volta. Espere 10 segundos e veja o espaço automático. '
        'Depois crie um quarto espaço, salve automaticamente mais vezes e mostre os passos no resumo.',
        codigo('saves'),
        [
            ['Mais um espaço', "Troque const espacos = ['auto', '1', '2', '3'] por const espacos = ['auto', '1', '2', '3', '4'].", r"const espacos = \[[^\]]*'4'"],
            ['Automático mais frequente', 'Troque const Duration(seconds: 10) por const Duration(seconds: 5).', r'Duration\(seconds:\s*(?!10\b)\d+\)'],
            ['Resumo com passos', "No atualizarResumos, acrescente · ${d['passos']} passos no texto do resumo.", r"resumos\[n\]\s*=\s*'[^;]*d\['passos'\]"],
        ],
        lim='No simulador os saves ficam guardados neste navegador (↺ Reiniciar apaga). O relógio do resumo é o do seu computador.',
        setup=SETUP_HIVE,
    )
    solucoes.MANUAL[('Salvar o jogo inteiro: espaços de save', 0)] = [("const espacos = ['auto', '1', '2', '3'];", "const espacos = ['auto', '1', '2', '3', '4'];")]
    solucoes.MANUAL[('Salvar o jogo inteiro: espaços de save', 1)] = [('const Duration(seconds: 10)', 'const Duration(seconds: 5)')]
    solucoes.MANUAL[('Salvar o jogo inteiro: espaços de save', 2)] = [(
        "resumos[n] = 'Fase ${d['fase']} · ${d['ossos'].length} ossos · ${d['quando']}';",
        "resumos[n] = 'Fase ${d['fase']} · ${d['ossos'].length} ossos · ${d['passos']} passos · ${d['quando']}';")]

    aula(
        'Replay e fantasma: gravar as entradas',
        'Para gravar uma partida não é preciso guardar a posição de tudo a cada quadro: basta guardar as entradas do '
        'jogador (aqui, onde estava o dedo em cada passo). Começando do mesmo estado e repetindo as mesmas entradas, o '
        'jogo refaz exatamente a mesma corrida. Isso só funciona se o jogo for determinístico: o mesmo começo e as mesmas '
        'entradas sempre dão o mesmo resultado. Por isso a simulação anda em passos fixos de 1/60 de segundo, '
        'independentes da velocidade do aparelho: o Ticker acumula o tempo real e roda quantos passos fixos couberem '
        '(o laço while com acumulado). Com dt variável, cada replay sairia um pouco diferente. Com a gravação em mãos, '
        'ver o replay é rodar a simulação com as entradas gravadas, e o fantasma é um segundo corredor que repete, ao mesmo '
        'tempo que você, as entradas da sua melhor corrida. A gravação é pequena (uma entrada por passo) e cabe num save.',
        'Em ▶ Testar, toque em 🏁 Correr e arraste o dedo para levar o caramelo pelas bandeiras 1, 2, 3 e 4. Corra de novo '
        'contra o fantasma (o círculo cinza) e veja o replay. Depois deixe o fantasma mais visível, ponha uma bandeira a '
        'mais e mude o atrito.',
        codigo('fantasma'),
        [
            ['Fantasma visível', 'Troque const corFantasma = Color(0x6690A4AE) por Color(0xAA90A4AE).', r'corFantasma\s*=\s*Color\(0x(?!6690A4AE)[0-9A-Fa-f]{8}\)'],
            ['Mais uma bandeira', 'Acrescente Offset(300, 400) no fim da lista bandeiras.', r'const bandeiras = \[(?:\s*Offset\([^)]*\),?){5,}'],
            ['Pista escorregadia', 'Troque vel = vel * 0.94 por vel = vel * 0.97.', r'vel = vel \* (?!0\.94\b)0\.\d+'],
        ],
    )
    solucoes.MANUAL[('Replay e fantasma: gravar as entradas', 1)] = [("Offset(80, 380)];", "Offset(80, 380), Offset(300, 400)];")]

    aula(
        'Jogo de ritmo: acertar na batida',
        'Num jogo de ritmo, tudo é medido em batidas: com bpm batidas por minuto, uma batida dura 60 / bpm segundos. A '
        'partitura diz em que batida cai cada nota e em qual pista. A posição da nota na tela vem do tempo que falta para '
        'ela chegar na linha: y = linhaAlvo - (tempoDaNota - agora) * velocidade. O tempo da música vem do relógio do '
        'Ticker (agora), e não de somar dt a cada quadro: somar acumula pequenos erros e a música sai do ritmo. No toque, '
        'o jogo procura a nota daquela pista mais perto do tempo atual e mede a diferença: dentro de janelaPerfeito é '
        '"perfeito", dentro de janelaBom é "bom", e longe demais o toque é ignorado (não pune quem toca cedo). Nota que '
        'passa da linha sem toque é erro e zera o combo. O metrônomo toca um som a cada batida para o jogador sentir o '
        'ritmo.',
        'Em ▶ Testar, toque em Começar e acerte as notas tocando nos botões coloridos quando elas passarem na linha branca. '
        'Depois acelere a música, aperte a janela do perfeito e acrescente uma nota.',
        codigo('ritmo'),
        [
            ['Mais rápido', 'Troque final double bpm = 100 por 130.', r'double bpm\s*=\s*(?!100\b)\d+'],
            ['Perfeito difícil', 'Troque final double janelaPerfeito = 0.06 por 0.03.', r'janelaPerfeito\s*=\s*(?!0\.06\b)0\.\d+'],
            ['Nota nova', 'Acrescente a nota [16, 2] no fim da partitura.', r'\[\s*16\s*,\s*[0-2]\s*\],?\s*\];'],
        ],
        lim='No simulador o metrônomo e o acerto usam sons sintetizados, que só tocam depois do primeiro toque. Em aparelhos reais, '
            'o som pode chegar alguns milissegundos atrasado; jogos de ritmo costumam ter uma calibração para compensar.',
        setup='No terminal do projeto:\n  flutter pub add audioplayers\n\nE declare a pasta assets/sons/ no pubspec.yaml.',
    )
    solucoes.MANUAL[('Jogo de ritmo: acertar na batida', 2)] = [("  [14, 1], [14.5, 0], [15, 1],\n];", "  [14, 1], [14.5, 0], [15, 1],\n  [16, 2],\n];")]

    aula(
        'Campo de visão e névoa de guerra',
        'Em jogos de exploração e estratégia, o jogador só vê o que o personagem enxerga. Para saber se uma casa está à '
        'vista, o jogo traça uma linha reta do caramelo até ela, casa por casa (o algoritmo de Bresenham, que anda na grade '
        'sem usar números quebrados); se a linha passar por uma parede antes de chegar, a casa está escondida. Fazendo isso '
        'para cada casa dentro do raio de visão, sai o conjunto das visíveis. A névoa de guerra tem três estados: nunca '
        'vista (preta), já vista (escurecida, o jogo lembra o mapa) e visível agora (clara). O que se move, como o gato, só '
        'aparece nas casas visíveis. A mesma função serve para o inimigo: o gato "vê" o caramelo se ele estiver perto e a '
        'linha entre os dois estiver livre, o que permite fazer jogos de esconder.',
        'Em ▶ Testar, explore o labirinto com as setas, desligue e ligue a névoa e tente passar pelo gato sem ser visto. '
        'Depois aumente a visão do caramelo, deixe a memória mais escura e o gato mais atento.',
        codigo('visao'),
        [
            ['Enxergar longe', 'Troque final int raioVisao = 5 por 7.', r'int raioVisao\s*=\s*(?!5\b)\d+'],
            ['Memória fraca', 'Troque const corLembrada = Color(0x99000000) por Color(0xDD000000).', r'corLembrada\s*=\s*Color\(0x(?!99000000)[0-9A-Fa-f]{8}\)'],
            ['Gato atento', 'Troque final int raioGato = 4 por 6.', r'int raioGato\s*=\s*(?!4\b)\d+'],
        ],
    )

    aula(
        'Projeto · Torres do Caramelo',
        'O sétimo projeto é um jogo de defesa de torres. Gatos entram pela casa vermelha em ondas e tentam fugir pela '
        'amarela com a comida; cada um que foge custa uma vida. Toque numa casa para pôr um caramelo de guarda (10 ossos), '
        'que joga ossos no gato ao alcance que está mais perto de fugir. Os gatos não seguem um caminho fixo: um BFS a '
        'partir da saída (a mesma busca da aula de caminhos) marca em cada casa quantos passos faltam, e cada gato só vai '
        'para o vizinho com o número menor. Quando você põe uma torre, o BFS roda de novo e os gatos desviam; se a torre '
        'fechasse o caminho por completo, ela é recusada. Os tiros são reaproveitados: em vez de criar e destruir um '
        'componente a cada tiro, o jogo guarda uma reserva e pega um tiro parado (veja "tiros criados" no placar parar de '
        'crescer). A economia fecha o ciclo: derrotar gatos e vencer ondas dá ossos para novas torres, e cada onda tem '
        'mais gatos, mais resistentes.',
        'Em ▶ Testar, monte um labirinto de caramelos e toque ▶ para chamar cada onda. Quantas ondas você aguenta? Depois '
        'ajuste o começo, o alcance das torres, o tamanho das ondas e a velocidade dos gatos.',
        codigo('torres'),
        [
            ['Começo rico', 'Troque const int ossosIniciais = 30 por 50.', r'ossosIniciais\s*=\s*(?!30\b)\d+'],
            ['Guarda de longe', 'Na classe Torre, troque final double alcance = 90 por 130.', r'double alcance\s*=\s*(?!90\b)\d+'],
            ['Ondas maiores', 'Troque faltamNascer = 5 + onda * 2 por faltamNascer = 5 + onda * 3.', r'faltamNascer = 5\s*\+\s*onda\s*\*\s*(?!2\b)\d+'],
            ['Gatos ligeiros', 'Na classe Gato, troque final double velocidade = 50 por 70.', r'double velocidade\s*=\s*(?!50\b)\d+;\s*\n\s*int coluna'],
        ],
        lim='No simulador os sons são sintetizados e só tocam depois do primeiro toque.',
        setup=SETUP_FLAME,
    )
    PARTS.append(['Projeto · Torres do Caramelo', 'Projeto 7 · Torres do Caramelo'])
