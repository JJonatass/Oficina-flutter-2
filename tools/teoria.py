# Aulas conteudistas (leitura) da Oficina Flutter 2: matemática de jogos, game design, arte e som.
# Cada aula tem uma leitura (blocos com títulos, parágrafos, figuras animadas e dicas), um teste rápido
# e um código de demonstração com exercícios, como as outras aulas.
import pathlib

PASTA = pathlib.Path(__file__).resolve().parent / 'teoria'


def codigo(nome):
    c = (PASTA / (nome + '.dart')).read_text(encoding='utf-8')
    assert "'''" not in c
    return '\n' + c


AULAS = []


def leitura(antes, t, text, tryit, arquivo, ex, blocos, quiz, parte=None, lim=None, setup=None):
    AULAS.append({'antes': antes, 'parte': parte, 't': t, 'text': text, 'tryit': tryit, 'code': codigo(arquivo),
                  'ex': ex, 'leitura': blocos, 'quiz': quiz, 'lim': lim, 'setup': setup})


# ------------------------------------------------------------------ Matemática de jogos
leitura(
    'Arrastar: a raquete segue o dedo',
    'Matemática de jogos: vetores',
    'Leitura: posição, deslocamento, distância e direção são vetores. Abra a leitura, depois brinque com o código: '
    'toque na tela e o caramelo anda até o dedo usando a direção do vetor.',
    'Em ▶ Testar, toque em vários pontos e acompanhe os números no título. Deixe o caramelo mais rápido, aumente a '
    'seta amarela e faça ele parar antes de chegar no dedo.',
    'vetores',
    [
        ['Mais rápido', 'Troque double velocidade = 120 por 240.', r'double velocidade\s*=\s*(?!120\b)\d+'],
        ['Seta unitária maior', 'Troque escalaSeta = 60 por 100: o vetor unitário continua com tamanho 1, só o desenho cresce.', r'escalaSeta\s*=\s*(?!60\b)\d+'],
        ['Parar antes do dedo', 'Troque d.distance > 2 por d.distance > 40: o caramelo para a 40 pixels do alvo.', r'if \(d\.distance\s*>\s*(?!2\b)\d+\)\s*\{'],
    ],
    [
        {'h': 'Uma seta com tamanho e direção'},
        {'p': 'Quase tudo que se mexe num jogo é descrito por **vetores**. Um vetor é um par de números, como `Offset(3, 4)`, '
              'que pode significar um lugar (a posição do caramelo), um passo (quanto andar neste quadro) ou uma '
              'velocidade (quantos pixels por segundo em cada eixo). No Flutter, o `Offset` faz esse papel; no Flame, o `Vector2`.'},
        {'p': 'O primeiro número é o deslocamento na horizontal (**dx**) e o segundo, na vertical (**dy**). Na tela, o y cresce '
              'para baixo: `dy` positivo é descer. Por isso, para pular, a velocidade vertical começa negativa.'},
        {'fig': 'vetor', 'legenda': 'A seta escura vai do caramelo até o alvo. Em vermelho, quanto andar em x (**dx**); em verde, '
                                    'quanto andar em y (**dy**). A seta amarela é o vetor unitário: a mesma direção, com tamanho 1.'},
        {'h': 'De onde estou para onde vou'},
        {'p': 'Para saber o caminho até um alvo, subtraia: `alvo - posicao`. O resultado aponta do primeiro para o segundo. '
              'Somar faz o caminho de volta: `posicao + passo` é onde o caramelo vai estar depois de dar o passo.'},
        {'p': 'O tamanho do vetor é a distância, calculada pelo teorema de Pitágoras: `sqrt(dx² + dy²)`. No Flutter ela já vem '
              'pronta em `offset.distance` (no Flame, `vetor.length`). É com ela que um jogo decide se dois objetos estão perto, '
              'se o osso foi pego ou se o gato enxergou o caramelo.'},
        {'h': 'Normalizar: só a direção'},
        {'p': 'Se o caramelo andasse `alvo - posicao` inteiro de uma vez, ele teletransportaria. O que queremos é a **direção**, '
              'com a velocidade escolhida por nós. Dividindo o vetor pelo próprio tamanho, sobra um vetor de tamanho 1, chamado '
              '**unitário** ou **normalizado**: `d / d.distance`. Multiplicando pela velocidade e por dt, temos o passo do quadro.'},
        {'dica': 'Antes de dividir pela distância, confira se ela não é zero. Com o caramelo em cima do alvo, `d.distance` vale 0 '
                 'e a divisão dá um número inválido (NaN), que faz o personagem sumir da tela. Por isso o código só anda se a '
                 'distância for maior que 2.', 'titulo': 'Cuidado'},
        {'h': 'Velocidade e aceleração também são vetores'},
        {'p': 'Uma bola quicando tem uma velocidade `(vx, vy)`. A gravidade é uma aceleração que só mexe em y: a cada quadro, '
              '`vy += gravidade * dt`. Bater numa parede lateral inverte `vx`; bater no chão inverte `vy`. Arremessar é medir a '
              'velocidade do dedo, que o Flutter entrega pronta em `velocity.pixelsPerSecond`, também um vetor.'},
    ],
    [
        {'q': 'O caramelo está em (100, 300) e o osso em (160, 220). Qual vetor leva do caramelo até o osso?',
         'ops': ['(60, -80)', '(-60, 80)', '(260, 520)', '(160, 220)'], 'ok': 0,
         'exp': 'Alvo menos posição: (160 − 100, 220 − 300) = (60, −80). O y negativo quer dizer subir na tela.'},
        {'q': 'Qual é a distância entre eles?', 'ops': ['140', '100', '20', '60'], 'ok': 1,
         'exp': 'sqrt(60² + 80²) = sqrt(3600 + 6400) = sqrt(10000) = 100.'},
        {'q': 'Para andar na direção do osso a 120 pixels por segundo, o passo de cada quadro é...',
         'ops': ['d * 120', 'd / d.distance * 120 * dt', 'd.distance * 120', 'd / 120'], 'ok': 1,
         'exp': 'Normaliza (d / d.distance) para ficar só a direção, multiplica pela velocidade e pelo tempo do quadro.'},
        {'q': 'Por que o código só anda quando a distância é maior que 2?',
         'ops': ['Para economizar bateria', 'Para não dividir por zero quando o caramelo já chegou', 'Porque o Flutter exige', 'Para o caramelo pular'], 'ok': 1,
         'exp': 'Com distância zero, d / d.distance vira NaN e a posição fica inválida.'},
    ],
    parte='Parte 2 · Entrada: arrastar e teclado',
)

leitura(
    'Teclado: setas e espaço',
    'Matemática de jogos: ângulos, seno e cosseno',
    'Leitura: ângulos em radianos, seno e cosseno para andar em círculo e atan2 para mirar. No código, o canhão '
    'gira para o dedo e a lua dá voltas no sol.',
    'Em ▶ Testar, arraste o dedo para mirar e toque para atirar ossos. Aumente a órbita, deixe o tiro mais rápido e faça '
    'a lua girar ao contrário.',
    'angulos',
    [
        ['Órbita maior', 'Troque double raioOrbita = 80 por 120.', r'raioOrbita\s*=\s*(?!80\b)\d+'],
        ['Tiro mais rápido', 'Troque double velocidadeTiro = 300 por 500.', r'velocidadeTiro\s*=\s*(?!300\b)\d+'],
        ['Lua ao contrário', 'Troque Offset(cos(tempo), sin(tempo)) por Offset(cos(-tempo), sin(-tempo)).', r'cos\(\s*-\s*tempo\s*\)'],
    ],
    [
        {'h': 'Graus e radianos'},
        {'p': 'No dia a dia medimos ângulos em graus: uma volta tem 360°. Em programação, quase sempre se usa **radiano**: uma '
              'volta tem 2π radianos (mais ou menos 6,28). Meia volta é π, um quarto de volta é π/2. Para converter, '
              '`graus = radianos * 180 / pi`. O `canvas.rotate`, o `angle` do Flame e as funções `sin` e `cos` do `dart:math` '
              'esperam radianos.'},
        {'h': 'Seno e cosseno: andar em círculo'},
        {'p': 'Imagine um ponto girando num círculo de raio 1. Para cada ângulo, o **cosseno** diz quanto ele está para o lado '
              '(x) e o **seno**, quanto está para cima ou para baixo (y). Os dois vão de −1 a 1. Multiplicando pelo raio e '
              'somando o centro, temos qualquer círculo: `x = cx + cos(a) * raio` e `y = cy + sin(a) * raio`.'},
        {'fig': 'circulo', 'legenda': 'Conforme o ângulo cresce, o cosseno (vermelho) e o seno (verde) mudam. Juntos, eles dão a '
                                      'posição do ponto no círculo.'},
        {'p': 'Trocando o ângulo pelo tempo, o objeto gira sozinho: é assim que a lua orbita o sol na demonstração. O seno '
              'sozinho também é útil: `sin(tempo * 3) * 8` faz algo boiar para cima e para baixo, como um osso flutuando ou '
              'um barco na água.'},
        {'h': 'De volta: atan2 para mirar'},
        {'p': 'O caminho contrário também aparece muito: sei o vetor até o alvo e quero o ângulo. A função `atan2(dy, dx)` '
              'responde isso, já considerando o quadrante certo (note que o **y vem primeiro**). O canhão usa '
              '`atan2(dedo.dy - canhao.dy, dedo.dx - canhao.dx)` e gira o desenho com `canvas.rotate(angulo)`.'},
        {'p': 'E do ângulo de novo para um vetor: `Offset(cos(a), sin(a))` já é um vetor unitário apontando para aquele lado. '
              'Multiplicado pela velocidade, vira a velocidade do tiro. Ângulo e vetor são duas formas de dizer a mesma direção.'},
        {'dica': 'Na tela o y cresce para baixo, então o ângulo cresce no sentido horário: 90° (π/2) aponta para baixo, não '
                 'para cima. Se uma rotação parecer espelhada, troque o sinal do ângulo.', 'titulo': 'Atenção ao eixo y'},
    ],
    [
        {'q': 'Quantos radianos tem meia volta?', 'ops': ['180', 'π', '2π', 'π/2'], 'ok': 1,
         'exp': 'Uma volta inteira é 2π; meia volta é π (cerca de 3,14).'},
        {'q': 'Um objeto gira num círculo de raio 50 em volta de (200, 200). Onde ele está quando o ângulo é 0?',
         'ops': ['(200, 150)', '(250, 200)', '(200, 250)', '(150, 200)'], 'ok': 1,
         'exp': 'cos(0) = 1 e sin(0) = 0: x = 200 + 50, y = 200 + 0.'},
        {'q': 'Para o canhão olhar para o dedo, qual chamada dá o ângulo?',
         'ops': ['atan2(dx, dy)', 'atan2(dy, dx)', 'sin(dx / dy)', 'cos(dy) * dx'], 'ok': 1,
         'exp': 'atan2 recebe primeiro o y e depois o x da diferença entre o alvo e o canhão.'},
        {'q': 'O que faz `y = base + sin(tempo * 3) * 8`?',
         'ops': ['Cai cada vez mais rápido', 'Sobe e desce entre base − 8 e base + 8', 'Gira em círculo', 'Fica parado'], 'ok': 1,
         'exp': 'O seno oscila entre −1 e 1; multiplicado por 8, o objeto boia 8 pixels para cima e para baixo.'},
    ],
)

leitura(
    'Flame: efeitos',
    'Matemática de jogos: interpolação e curvas',
    'Leitura: lerp, curvas de suavização (easing) e como seguir um alvo de forma suave sem depender do ritmo dos '
    'quadros. No código, quatro bolinhas fazem o mesmo trajeto com curvas diferentes.',
    'Em ▶ Testar, compare as quatro bolinhas e arraste o dedo: o caramelo segue com suavidade. Deixe o ciclo mais longo, '
    'o seguidor mais preguiçoso e a curva de frear mais forte.',
    'lerp',
    [
        ['Ciclo de 4 segundos', 'Troque double duracao = 2 por 4.', r'double duracao\s*=\s*(?!2\b)[\d.]+'],
        ['Seguidor preguiçoso', 'Troque pow(0.02, dt) por pow(0.3, dt): ele percorre uma fração menor do caminho a cada segundo.', r'pow\(\s*0\.(?!02\b)\d+\s*,\s*dt'],
        ['Frear mais forte', 'Na função freia, troque 1 - (1 - t) * (1 - t) por 1 - (1 - t) * (1 - t) * (1 - t).', r'1\s*-\s*\(1\s*-\s*t\)\s*\*\s*\(1\s*-\s*t\)\s*\*\s*\(1\s*-\s*t\)'],
    ],
    [
        {'h': 'Lerp: o caminho entre dois valores'},
        {'p': '**Interpolar** é calcular um valor intermediário. A fórmula básica, chamada **lerp** (de _linear interpolation_), '
              'é `a + (b - a) * t`: com t = 0 dá a, com t = 1 dá b, e com t = 0,5 dá o meio. O Flutter tem `lerpDouble`, '
              '`Offset.lerp` e `Color.lerp`; o Flame tem `Vector2` com `lerp`. Quase toda animação é um lerp com t andando de 0 a 1.'},
        {'h': 'Curvas: mudar o ritmo, não o caminho'},
        {'p': 'Se t cresce em ritmo constante, o movimento é robótico: começa e para de repente. Uma **curva** (easing) troca '
              't por outra conta antes do lerp. `t * t` começa devagar e acelera; `1 - (1 - t)²` começa rápido e freia; '
              '`t * t * (3 - 2t)`, chamada _smoothstep_, faz as duas coisas. Os `Curves.easeIn`, `easeOut` e `easeInOut` do '
              'Flutter são versões disso.'},
        {'fig': 'curvas', 'legenda': 'As quatro bolinhas saem e chegam juntas; muda só o ritmo. À direita, o gráfico de cada curva: '
                                     'quanto mais inclinada, mais rápido naquele trecho.'},
        {'p': 'Escolher a curva é escolher a sensação. Um menu que entra freando parece leve; um objeto que cai acelerando parece '
              'pesado; algo que vai e volta com _smoothstep_ parece vivo. Os efeitos do Flame aceitam a curva no `EffectController`.'},
        {'h': 'Seguir um alvo com suavidade'},
        {'p': 'Uma câmera que segue o jogador "na hora" treme a cada passo. O truque é andar só uma fração do que falta a cada '
              'quadro: `pos = Offset.lerp(pos, alvo, fracao)`. Longe, a fração vira um passo grande; perto, um passo pequeno, e o '
              'movimento freia sozinho.'},
        {'fig': 'seguidor', 'legenda': 'Dois seguidores atrás do mesmo alvo: com fração maior por segundo, o laranja acompanha de perto; '
                                       'o cinza fica para trás.'},
        {'dica': 'Uma fração fixa por quadro (como 0,1) deixa o jogo mais rápido em telas de 120 Hz do que em telas de 60 Hz. '
                 'Para não depender dos quadros, use `1 - pow(sobra, dt)`: `sobra` é quanto do caminho ainda falta depois de '
                 '1 segundo (0,02 é 2%).', 'titulo': 'Independente dos quadros'},
    ],
    [
        {'q': 'Quanto vale lerp(10, 50, 0.25)?', 'ops': ['20', '15', '35', '12,5'], 'ok': 0,
         'exp': '10 + (50 − 10) × 0,25 = 10 + 10 = 20.'},
        {'q': 'Qual curva começa devagar e vai acelerando?', 'ops': ['t', 't * t', '1 - (1 - t) * (1 - t)', '1 - t'], 'ok': 1,
         'exp': 't² cresce pouco no começo (0,1² = 0,01) e muito no fim.'},
        {'q': 'Por que `pos = lerp(pos, alvo, 0.1)` em cada quadro fica diferente em telas de 60 Hz e de 120 Hz?',
         'ops': ['Porque o lerp não funciona em 120 Hz', 'Porque em 120 Hz a conta roda duas vezes mais por segundo', 'Porque a tela é maior', 'Não fica diferente'], 'ok': 1,
         'exp': 'Mais quadros por segundo aplicam a fração mais vezes. A versão com pow(sobra, dt) corrige isso.'},
        {'q': 'Uma janela que entra na tela e para suavemente usa qual tipo de curva?', 'ops': ['Acelera (ease in)', 'Freia (ease out)', 'Linear', 'Nenhuma'], 'ok': 1,
         'exp': 'Chegar freando dá a impressão de que o objeto encaixa no lugar.'},
    ],
    parte='Parte 5 · Efeitos, telas e gestos',
)

# ------------------------------------------------------------------ Game design
leitura(
    'Projeto · Pula-Caixa',
    'Game design: objetivo, desafio e recompensa',
    'Leitura: o que faz um jogo ser jogo, o ciclo principal e como dar retorno ao jogador. No código, um ciclo bem curto: '
    'pegar o osso antes que ele suma, com combo para quem acerta em sequência.',
    'Em ▶ Testar, pegue alguns ossos e veja o combo crescer. Depois mexa no desafio e na recompensa e sinta como o jogo muda.',
    'ciclo',
    [
        ['Mais pressão', 'Troque double tempoLimite = 1.5 por 1.0.', r'double tempoLimite\s*=\s*(?!1\.5\b)[\d.]+'],
        ['Combo com teto', 'Troque pontos += combo por pontos += min(combo, 5): o combo continua contando, mas paga no máximo 5.', r'pontos\s*\+=\s*min\(\s*combo'],
        ['Cada vez mais difícil', 'Depois de combo++, acrescente tempoLimite = max(0.6, tempoLimite - 0.05);', r'tempoLimite\s*=\s*max\('],
    ],
    [
        {'h': 'O que faz um jogo ser jogo'},
        {'p': 'Um jogo tem um **objetivo** (o que o jogador quer), **regras** (o que pode e o que não pode), um **desafio** (o que '
              'atrapalha) e **retorno** (o jogo responde ao que o jogador faz). Tire o desafio e vira um brinquedo; tire o objetivo '
              'e vira um passatempo sem fim; tire o retorno e o jogador não entende o que aconteceu.'},
        {'h': 'O ciclo principal'},
        {'p': 'Todo jogo tem uma ação que se repete o tempo todo: pular caixas, pegar maçãs, fugir dos gatos. Esse **ciclo '
              'principal** (_core loop_) precisa ser gostoso sozinho, porque é o que o jogador mais faz. Fases, lojas e histórias '
              'vêm depois e só funcionam se o ciclo for bom.'},
        {'fig': 'ciclo', 'legenda': 'O ciclo do Caça-Ossos em miniatura: ver o osso (objetivo), correr contra o tempo (desafio) e '
                                    'ganhar pontos (recompensa), e de novo.'},
        {'h': 'Recompensas'},
        {'p': 'Recompensa é tudo que faz o jogador sentir que valeu a pena: pontos, um som, uma animação, um item novo, uma fase '
              'nova. Recompensas **imediatas** (o som da moeda) mantêm o ritmo; **acumuladas** (o recorde, uma nova fase) dão '
              'motivo para continuar. O combo da demonstração junta as duas: cada acerto vale mais quando vem em sequência, e '
              'errar tem um custo claro.'},
        {'h': 'Retorno claro'},
        {'p': 'O jogador precisa entender na hora o que aconteceu e por quê. A barra que encolhe mostra o tempo, fica vermelha '
              'quando está acabando e o aviso explica que o combo zerou. Se o jogador perde e não sabe o motivo, ele culpa o '
              'jogo, não a si mesmo, e desiste.'},
        {'dica': 'Antes de fazer gráficos bonitos, teste o ciclo com quadrados e círculos, como na Parte 1. Se for divertido '
                 'assim, vai ser mais ainda com sprites e som. Esse primeiro teste se chama protótipo.', 'titulo': 'Prototipe cedo'},
    ],
    [
        {'q': 'O que é o ciclo principal de um jogo?', 'ops': ['A tela inicial', 'A ação que o jogador repete o tempo todo', 'A música de fundo', 'O último chefe'], 'ok': 1,
         'exp': 'É a ação central, como pular, atirar ou coletar, que se repete durante toda a partida.'},
        {'q': 'No Pula-Caixa, qual é o desafio?', 'ops': ['Os metros percorridos', 'As caixas que chegam cada vez mais rápido', 'O recorde', 'O céu azul'], 'ok': 1,
         'exp': 'As caixas são o obstáculo; os metros e o recorde são a recompensa.'},
        {'q': 'Por que o combo deixa o jogo mais interessante?', 'ops': ['Porque deixa o jogo mais lento', 'Porque recompensa a sequência de acertos e dá um custo claro ao erro', 'Porque some com o desafio', 'Porque muda as cores'], 'ok': 1,
         'exp': 'O jogador ganha um motivo para arriscar e manter a sequência.'},
        {'q': 'O que fazer primeiro ao criar um jogo novo?', 'ops': ['Desenhar todos os sprites', 'Compor a música', 'Testar o ciclo principal com formas simples', 'Escrever a história'], 'ok': 2,
         'exp': 'Um protótipo rápido mostra se a ideia é divertida antes de gastar tempo com arte.'},
    ],
)

leitura(
    'Projeto · Pega-Maçã',
    'Game design: dificuldade e curva de aprendizado',
    'Leitura: como a dificuldade deve crescer, o estado de fluxo e por que o jogo precisa de respiros. No código, três '
    'curvas de dificuldade controlam a chuva de caixas.',
    'Em ▶ Testar, escolha cada curva e observe a chuva e o gráfico. Encurte os degraus, acalme as ondas e deixe a partida mais longa.',
    'dificuldade',
    [
        ['Degraus mais curtos', 'Na função degraus, troque (t / 15) por (t / 10).', r'\(t\s*/\s*(?!15\b)\d+\)'],
        ['Ondas mais calmas', 'Na função ondas, troque 0.5 * sin(t * 0.6) por 0.2 * sin(t * 0.6).', r'0\.(?!5\b)\d+\s*\*\s*sin\(t'],
        ['Partida mais longa', 'Troque double duracaoPartida = 60 por 90.', r'duracaoPartida\s*=\s*(?!60\b)\d+'],
    ],
    [
        {'h': 'Nem fácil demais, nem difícil demais'},
        {'p': 'Quando o desafio é muito maior que a habilidade, o jogador fica **ansioso** e desiste. Quando é muito menor, fica '
              '**entediado** e também desiste. Entre os dois existe uma faixa em que a pessoa se concentra e perde a noção do '
              'tempo: o **fluxo**. O trabalho do designer é manter o jogador nessa faixa enquanto ele melhora.'},
        {'fig': 'fluxo', 'legenda': 'Conforme o jogador ganha habilidade, o desafio sobe junto. O caminho em zigue-zague fica dentro do '
                                    'fluxo: aperta um pouco, alivia um pouco.'},
        {'h': 'Curvas de dificuldade'},
        {'p': 'Uma **reta** sobe sempre no mesmo ritmo: simples, mas cansa. **Degraus** mantêm a dificuldade por um tempo e '
              'sobem de uma vez, como fases ou ondas de inimigos; o jogador tem tempo de dominar cada nível. **Ondas** sobem '
              'com altos e baixos: depois de um trecho difícil vem um respiro, e a tensão volta. A maioria dos jogos de ação '
              'combina degraus e ondas.'},
        {'p': 'Na demonstração, a curva diz quantas caixas nascem por segundo. Repare que as três terminam no mesmo lugar, '
              'mas a sensação durante a partida é bem diferente.'},
        {'h': 'Ensinar jogando'},
        {'p': 'A **curva de aprendizado** é o caminho que o jogador faz para entender o jogo. Bons jogos apresentam uma ideia por '
              'vez: primeiro só andar, depois um obstáculo parado, depois um que se mexe, e só então os dois juntos. Cada ideia '
              'aparece num lugar seguro antes de virar perigo. Texto explicando ajuda pouco; um desafio que obriga a usar a ideia '
              'ensina muito mais.'},
        {'dica': 'Veja outras pessoas jogarem sem dar dicas. Onde elas travam, a curva está íngreme demais; onde elas se distraem, '
                 'está plana demais. Anote e ajuste os números, como você fez nos exercícios.', 'titulo': 'Teste com gente de verdade'},
    ],
    [
        {'q': 'O que acontece quando o desafio fica muito acima da habilidade do jogador?', 'ops': ['Tédio', 'Ansiedade', 'Fluxo', 'Nada'], 'ok': 1,
         'exp': 'O jogador sente que não tem chance e tende a desistir.'},
        {'q': 'Qual curva dá respiros depois dos trechos difíceis?', 'ops': ['Reta', 'Degraus', 'Ondas', 'Nenhuma'], 'ok': 2,
         'exp': 'As ondas sobem com altos e baixos, alternando tensão e alívio.'},
        {'q': 'Qual é a melhor forma de ensinar uma mecânica nova?', 'ops': ['Um texto longo antes da fase', 'Apresentar a ideia num lugar seguro e depois usá-la como desafio', 'Colocar todas as mecânicas juntas na primeira fase', 'Não ensinar'], 'ok': 1,
         'exp': 'O jogador experimenta sem risco e depois aplica o que aprendeu.'},
        {'q': 'Na demonstração, a função da curva devolve...', 'ops': ['A cor das caixas', 'Quantas caixas nascem por segundo naquele momento', 'A velocidade do caramelo', 'O recorde'], 'ok': 1,
         'exp': 'O valor é somado a um acumulador; a cada 1 inteiro nasce uma caixa.'},
    ],
)

leitura(
    'Projeto · Céu Agitado',
    'Game design: game feel e "suco"',
    'Leitura: por que alguns jogos parecem gostosos de jogar mesmo fazendo pouco. No código, a mesma batida com e sem '
    'tremida, esmagamento, faíscas, clarão e som.',
    'Em ▶ Testar, toque com o suco ligado e desligado e compare. Aumente a tremida, solte mais faíscas e comece com o suco desligado.',
    'suco',
    [
        ['Tremida maior', 'Troque double forcaTremida = 10 por 20.', r'forcaTremida\s*=\s*(?!10\b)[\d.]+'],
        ['Mais faíscas', 'No bater, troque i < 14 por i < 30.', r'i\s*<\s*(?!14\b)\d+;\s*i\+\+\)\s*\{\s*final a'],
        ['Começar sem suco', 'Troque bool comSuco = true por false.', r'bool comSuco\s*=\s*false'],
    ],
    [
        {'h': 'O que é game feel'},
        {'p': '**Game feel** é a sensação de controlar alguma coisa no jogo: se o pulo parece pesado ou leve, se a batida parece '
              'forte, se a nave responde na hora. Dois jogos com as mesmas regras podem parecer completamente diferentes só '
              'por causa dela. Muitas vezes, o que separa um jogo "ok" de um jogo gostoso são detalhes de meio segundo.'},
        {'h': 'Suco: exagerar a resposta'},
        {'p': 'Os desenvolvedores chamam de **suco** (_juice_) os efeitos que exageram a resposta a uma ação: a tela treme '
              'na batida, a caixa esmaga e volta, saem faíscas, a cor pisca e um som marca o momento. Nenhum muda as regras, '
              'mas todos dizem ao jogador "isso foi importante".'},
        {'fig': 'suco', 'legenda': 'A mesma batida duas vezes. À esquerda, só a caixa parada; à direita, com tremida, esmagamento, '
                                   'clarão e faíscas.'},
        {'h': 'As ferramentas'},
        {'p': '**Tremida de tela** (_screen shake_): deslocar tudo um pouco, em direções sorteadas, por um instante. **Esmagar e '
              'esticar**: deformar o objeto no impacto, mantendo a área. **Partículas**: pedacinhos que saem e somem. **Clarão**: '
              'a cor vai ao branco e volta. **Som**: curto, no exato momento. **Pausa de impacto**: congelar o jogo por 2 ou 3 '
              'quadros numa batida forte.'},
        {'p': 'O segredo é que tudo **decai**: começa forte e volta ao normal em poucos décimos de segundo. Na demonstração, '
              'cada efeito é um número que vai a 1 no toque e desce até 0 com o tempo (`max(0, valor - dt * velocidade)`).'},
        {'dica': 'Suco demais cansa e atrapalha: uma tela que treme o tempo todo esconde o que importa. Guarde os efeitos grandes '
                 'para os momentos grandes (perder uma vida, derrotar um chefe) e use efeitos pequenos nas ações comuns. E dê '
                 'ao jogador uma opção para reduzir a tremida.', 'titulo': 'Na medida certa'},
    ],
    [
        {'q': 'O que o suco muda nas regras do jogo?', 'ops': ['Muda a pontuação', 'Nada: muda a sensação de cada ação', 'Muda a dificuldade', 'Muda os controles'], 'ok': 1,
         'exp': 'Os efeitos de suco só reforçam o retorno; as regras continuam iguais.'},
        {'q': 'Por que os efeitos precisam decair rapidamente?', 'ops': ['Para economizar memória', 'Para marcar o momento sem atrapalhar a leitura do jogo', 'Porque o Flutter exige', 'Para o jogo ficar mais difícil'], 'ok': 1,
         'exp': 'Um efeito curto marca o impacto; um efeito longo vira ruído.'},
        {'q': 'Esmagar e esticar deve manter o quê?', 'ops': ['A cor', 'A área (fica mais largo quando fica mais baixo)', 'A posição do topo', 'O número de quadros'], 'ok': 1,
         'exp': 'Manter a área faz a deformação parecer elástica e natural.'},
        {'q': 'Onde usar a tremida de tela mais forte?', 'ops': ['Em cada passo do personagem', 'Nos momentos importantes, como levar dano', 'Na tela de menu', 'O tempo todo'], 'ok': 1,
         'exp': 'Efeitos grandes em momentos grandes; nas ações comuns, efeitos pequenos.'},
    ],
)

# ------------------------------------------------------------------ Arte e som
leitura(
    'Sprites: imagens no Canvas',
    'Arte de jogos: pixel art e paletas',
    'Leitura: como funciona a pixel art, por que usar poucas cores e como a paleta muda o personagem inteiro. No código, '
    'o caramelo é desenhado pixel por pixel a partir de letras.',
    'Em ▶ Testar, troque a paleta e ligue e desligue a grade. Crie uma paleta nova, aumente os pixels e mude um pixel do desenho.',
    'pixel',
    [
        ['Uma paleta nova', "No mapa paletas, acrescente uma quarta paleta, por exemplo 'Dourado': {'C': Color(0xFFE0A100), 'D': Color(0xFF9C6B00), 'L': Color(0xFFFFE08A), 'k': Color(0xFF222034), 't': Color(0xFFEC6878)},", r"'(?!Caramelo'|Pretinho'|Malhado')[A-ZÀ-Ú]\w*'\s*:\s*\{"],
        ['Pixels maiores', 'Troque double tamanhoPixel = 18 por 20.', r'tamanhoPixel\s*=\s*(?!18\b)\d+'],
        ['Língua para dentro', "No desenho, troque a linha '...DC...CCCC.t..' por '...DC...CCCC....'.", r"'\.\.\.DC\.\.\.CCCC\.\.\.\.'"],
    ],
    [
        {'h': 'Desenhar com quadradinhos'},
        {'p': 'Na **pixel art** cada pixel é colocado de propósito. O caramelo tem 16 × 16 pixels: 256 quadradinhos, a maioria '
              'transparente. Em tão pouco espaço, cada pixel conta: um só vira o olho, dois viram a língua. É uma arte de escolher '
              'o que mostrar e o que deixar de fora.'},
        {'fig': 'pixel', 'legenda': 'O mesmo desenho ampliado e em tamanho real. A cada ciclo, a paleta muda e o personagem vira outro, '
                                    'sem mexer em nenhum pixel.'},
        {'h': 'Paletas: poucas cores, bem escolhidas'},
        {'p': 'Uma **paleta** é o conjunto limitado de cores do desenho. O caramelo usa cinco: o pelo, uma sombra mais escura, '
              'a parte clara da barriga e do focinho, o preto do olho e do nariz e o rosa da língua. Poucas cores deixam o '
              'desenho legível de longe e fazem todos os sprites do jogo parecerem do mesmo mundo.'},
        {'p': 'Na demonstração, o desenho é uma lista de textos em que cada letra é uma cor (`C` pelo, `D` sombra, `L` claro). '
              'Trocar o mapa de cores troca a paleta inteira de uma vez: assim os jogos fazem o "jogador 2" de outra cor ou o '
              'inimigo mais forte em vermelho.'},
        {'h': 'Luz, sombra e contorno'},
        {'p': 'Para dar volume, escolha de onde vem a luz (em geral, de cima) e use uma cor mais escura no lado oposto: a orelha '
              'e o rabo do caramelo são mais escuros, e a barriga é mais clara. Um contorno escuro separa o personagem do fundo; '
              'sem contorno, ele precisa contrastar pela cor.'},
        {'dica': 'Pixel art ampliada precisa continuar nítida. No Canvas, desenhe com `FilterQuality.none` (o padrão do '
                 '`drawImageRect` com Paint simples); no Flame, os sprites já saem nítidos. Amplie sempre por números inteiros '
                 '(2×, 3×, 4×) para todos os pixels ficarem do mesmo tamanho.', 'titulo': 'Nítido, não borrado'},
    ],
    [
        {'q': 'Quantos pixels tem um sprite de 16 × 16?', 'ops': ['32', '160', '256', '1600'], 'ok': 2, 'exp': '16 × 16 = 256 pixels.'},
        {'q': 'Por que usar uma paleta pequena?', 'ops': ['Porque o celular não mostra muitas cores', 'Para o desenho ficar legível e os sprites combinarem entre si', 'Para o arquivo ficar colorido', 'Não há motivo'], 'ok': 1,
         'exp': 'Poucas cores bem escolhidas dão unidade e clareza ao jogo.'},
        {'q': 'Na demonstração, como o caramelo vira o Pretinho?', 'ops': ['Redesenhando todos os pixels', 'Trocando o mapa de cores (a paleta)', 'Girando a imagem', 'Mudando o tamanho do pixel'], 'ok': 1,
         'exp': 'As letras do desenho continuam iguais; só a cor de cada letra muda.'},
        {'q': 'Qual ampliação mantém a pixel art nítida?', 'ops': ['1,5×', '2,7×', '3×', 'Qualquer uma'], 'ok': 2,
         'exp': 'Ampliar por inteiros deixa todos os pixels com o mesmo tamanho.'},
    ],
    parte='Parte 3 · Sprites, animação, som e texto',
)

leitura(
    'Animação com folha de sprites',
    'Arte de jogos: princípios de animação',
    'Leitura: quadros e tempo, espaçamento, esmagar e esticar, antecipação e exagero. No código, uma bola quica e mostra '
    'o rastro dos quadros.',
    'Em ▶ Testar, mexa no controle de exagero e compare. Deixe a bola exagerada desde o começo, o quique mais rápido e o pulo mais alto.',
    'animacao',
    [
        ['Exagero máximo', 'Troque double exagero = 0.6 por 1.0.', r'double exagero\s*=\s*(?!0\.6\b)[\d.]+'],
        ['Quique mais rápido', 'Troque double periodo = 1.2 por 0.8.', r'double periodo\s*=\s*(?!1\.2\b)[\d.]+'],
        ['Pulo mais alto', 'No desenhar, troque p.altura * 260 por p.altura * 320.', r'p\.altura\s*\*\s*(?!260\b)\d+'],
    ],
    [
        {'h': 'Quadros e tempo'},
        {'p': 'Animar é mostrar desenhos parecidos em sequência, rápido o bastante para o olho ver movimento. Nos jogos, o '
              'caramelo andando tem 4 quadros trocados 8 a 10 vezes por segundo. Mais quadros deixam mais suave, mas o que mais '
              'importa é o **tempo** de cada pose: uma pose que fica mais tempo na tela chama mais atenção.'},
        {'h': 'Espaçamento'},
        {'p': '**Espaçamento** é a distância entre uma pose e a próxima. Poses próximas parecem lentas; afastadas, rápidas. '
              'Uma bola jogada para cima tem poses afastadas perto do chão (rápida) e juntas no alto (lenta, quase parando). É '
              'isso que o rastro da demonstração mostra, e é a mesma ideia das curvas de suavização.'},
        {'fig': 'squash', 'legenda': 'À esquerda, uma bola rígida; à direita, a mesma bola esmagando no chão e esticando no ar. As duas '
                                     'quicam no mesmo ritmo, mas só uma parece de borracha.'},
        {'h': 'Esmagar e esticar'},
        {'p': 'Ao bater no chão, a bola **esmaga**: fica mais larga e mais baixa. Quando está rápida no ar, **estica** na direção '
              'do movimento. A área se mantém (se fica mais larga, fica mais baixa), por isso parece elástica e não muda de '
              'tamanho. O mesmo vale para personagens: o caramelo agacha antes de pular e estica no ar.'},
        {'h': 'Antecipação e exagero'},
        {'p': '**Antecipação** é o pequeno movimento contrário antes da ação: agachar antes de pular, puxar o braço antes de '
              'jogar. Ela prepara o olho para o que vem. **Exagero** é empurrar tudo um pouco além do real: o jogo é um '
              'desenho, e o movimento realista costuma parecer sem graça. Na demonstração, o controle de exagero mostra o '
              'quanto isso muda a sensação.'},
        {'dica': 'Em jogo, a resposta ao toque precisa ser imediata. Se o pulo tiver uma antecipação longa, o jogador sente '
                 'atraso. Use antecipações de 1 ou 2 quadros nas ações do jogador e guarde as longas para os inimigos, que '
                 'assim avisam o que vão fazer.', 'titulo': 'Animação de jogo responde rápido'},
    ],
    [
        {'q': 'Poses muito próximas umas das outras dão a impressão de...', 'ops': ['Movimento rápido', 'Movimento lento', 'Cor diferente', 'Tamanho maior'], 'ok': 1,
         'exp': 'Pouca distância entre quadros é pouco movimento por tempo: parece devagar.'},
        {'q': 'Ao esmagar no chão, a bola fica...', 'ops': ['Mais alta e mais fina', 'Mais larga e mais baixa', 'Menor em tudo', 'Igual'], 'ok': 1,
         'exp': 'Ela achata mantendo a área: o que perde em altura ganha em largura.'},
        {'q': 'O que é antecipação?', 'ops': ['Começar a fase antes', 'Um movimento contrário curto antes da ação', 'Repetir a animação', 'Animar mais rápido'], 'ok': 1,
         'exp': 'Agachar antes de pular é o exemplo clássico.'},
        {'q': 'Por que a antecipação do pulo do jogador deve ser curta?', 'ops': ['Para economizar quadros', 'Para o controle não parecer atrasado', 'Porque o Flame exige', 'Para o pulo ser mais alto'], 'ok': 1,
         'exp': 'O jogador espera resposta imediata ao apertar o botão.'},
    ],
)

leitura(
    'Som: efeitos com audioplayers',
    'Som de jogos: efeitos e música',
    'Leitura: para que serve o som no jogo, como um efeito é construído (envelope), música em loop e mixagem. No código, '
    'uma mesa de som toca os efeitos da Oficina e mostra o envelope de cada um.',
    'Em ▶ Testar, toque cada efeito e compare os envelopes; ligue a música e ajuste os volumes. Depois deixe a música mais '
    'baixa, troque a música e acrescente um botão para o som de dano.',
    'som',
    [
        ['Música mais baixa', 'Troque double volumeMusica = 0.4 por 0.2.', r'double volumeMusica\s*=\s*(?!0\.4\b)[\d.]+'],
        ['Outra música', "Troque 'sons/musica_aventura.mp3' por 'sons/musica_espaco.mp3'.", r'sons/musica_(?:espaco|menu)\.mp3'],
        ['Botão de dano', "No mapa efeitos, acrescente 'dano': Envelope(0.0, 0.15, 0.2, 0.1), antes do fecha-chaves.", r"'dano'\s*:\s*Envelope\("],
    ],
    [
        {'h': 'Som é metade da sensação'},
        {'p': 'Feche os olhos durante um jogo: você ainda sabe quando pegou um item, levou dano ou passou de fase. O som dá **retorno** '
              'mais rápido que a imagem, marca o ritmo e cria o clima. Um mesmo acerto parece fraco sem som e forte com um "plim" '
              'bem escolhido.'},
        {'h': 'O envelope de um efeito'},
        {'p': 'Um efeito curto tem uma forma de volume no tempo, chamada **envelope** ou ADSR: o **ataque** (quanto demora para '
              'chegar ao máximo), o **decaimento** (quanto cai depois do pico), a **sustentação** (o nível em que fica) e a '
              '**soltura** (quanto demora para sumir). Uma batida tem ataque zero e some rápido; uma vitória tem notas que '
              'sustentam e se soltam devagar.'},
        {'fig': 'adsr', 'legenda': 'O envelope de um efeito: sobe no ataque, cai no decaimento, fica na sustentação e some na soltura. '
                                   'A barra laranja mostra o volume naquele instante.'},
        {'p': 'Os sons da Oficina são **sintetizados**: o navegador gera ondas (quadrada, triangular, ruído) e aplica um envelope. '
              'É o mesmo jeito dos videogames antigos, e por isso eles têm aquele timbre. Nos seus jogos, você pode usar arquivos '
              'gravados (.wav, .mp3, .ogg) feitos em programas como o jsfxr ou bancos de sons gratuitos.'},
        {'h': 'Música em loop'},
        {'p': 'A música de fundo precisa tocar sem fim, então ela é feita para **emendar**: o final leva de volta ao começo sem '
              'corte. No audioplayers, isso é `setReleaseMode(ReleaseMode.loop)`; no Flame, `FlameAudio.bgm.play`. Músicas '
              'diferentes para menu, fase e chefe ajudam o jogador a saber em que momento está.'},
        {'h': 'Mixagem: cada som no seu volume'},
        {'p': '**Mixar** é equilibrar os volumes. A música fica mais baixa que os efeitos, para não esconder a informação; '
              'efeitos frequentes (passos) ficam mais baixos que os raros (vitória). Dar ao jogador controles separados de '
              'música e efeitos, como na demonstração, é uma gentileza que quase todo jogo oferece.'},
        {'dica': 'Muitas pessoas jogam no celular sem som. Todo som importante precisa de um sinal visual também: o dano pisca '
                 'o personagem, o osso pego mostra um número. Assim ninguém perde informação.', 'titulo': 'Acessibilidade'},
    ],
    [
        {'q': 'Qual parte do envelope controla quanto o som demora para sumir?', 'ops': ['Ataque', 'Decaimento', 'Sustentação', 'Soltura'], 'ok': 3,
         'exp': 'A soltura (release) é o fim do som, depois que a nota é solta.'},
        {'q': 'Um som de batida tem ataque...', 'ops': ['Longo', 'Quase zero', 'Igual à soltura', 'Negativo'], 'ok': 1,
         'exp': 'O impacto chega ao máximo na hora; por isso parece seco e forte.'},
        {'q': 'Como fazer a música tocar sem parar no audioplayers?', 'ops': ['play duas vezes', 'setReleaseMode(ReleaseMode.loop)', 'setVolume(2)', 'dispose()'], 'ok': 1,
         'exp': 'O modo loop recomeça a música quando ela acaba.'},
        {'q': 'Por que todo som importante precisa de um sinal visual?', 'ops': ['Para gastar menos bateria', 'Porque muita gente joga sem som', 'Porque o Flutter não toca som', 'Não precisa'], 'ok': 1,
         'exp': 'Quem joga no mudo ou não ouve bem continua recebendo a informação.'},
    ],
)


def inserir(LESSONS, EXERCISES, PARTS):
    """Põe cada aula de leitura antes da aula indicada e acerta o início das partes."""
    for a in AULAS:
        idx = next(i for i, L in enumerate(LESSONS) if L['t'] == a['antes'])
        LESSONS.insert(idx, {'t': a['t'], 'text': a['text'], 'tryit': a['tryit'], 'code': a['code'], 'lim': a['lim'],
                             'setup': a['setup'], 'leitura': a['leitura'], 'quiz': a['quiz']})
        EXERCISES[a['t']] = a['ex']
        if a['parte']:
            ps = [p for p in PARTS if p[1] == a['parte']]
            assert len(ps) == 1, a['parte']
            ps[0][0] = a['t']
