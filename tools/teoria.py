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
              'cada efeito é um número que vai a 1 no toque e desce até 0 com o tempo (`max(0.0, valor - dt * velocidade)`).'},
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


# ------------------------------------------------------------------ Leituras da segunda leva
leitura(
    'Gravidade e pulo',
    'Matemática de jogos: física e passo de tempo',
    'Leitura: como a física avança quadro a quadro, por que o dt muda o resultado e o que é o passo fixo. No código, '
    'uma bola rápida atravessa uma parede fina quando o aparelho é lento.',
    'Em ▶ Testar, compare 60, 20 e 8 quadros por segundo e ligue o passo fixo. Depois engrosse a parede, diminua o passo e '
    'deixe a bola mais lenta.',
    'fisica',
    [
        ['Parede grossa', 'Troque const double paredeLargura = 6 por 40: a 8 fps ela para de ser atravessada.', r'paredeLargura\s*=\s*(?!6\b)\d+'],
        ['Passo menor', 'Troque double passo = 1 / 120 por 1 / 240.', r'double\s+passo\s*=\s*1\s*/\s*(?!120\b)\d+'],
        ['Bola mais lenta', 'Na classe Bola, troque Offset vel = const Offset(900, -150) por const Offset(400, -150).', r'vel\s*=\s*const\s+Offset\(\s*(?!900\b)\d+'],
    ],
    [
        {'h': 'A física anda em passos'},
        {'p': 'O jogo não calcula o movimento de forma contínua: a cada quadro ele dá um **passo**. Com a velocidade e a '
              'aceleração conhecidas, o passo mais usado é o de **Euler semi-implícito**: primeiro `vel += aceleracao * dt`, '
              'depois `pos += vel * dt`. É o que você já fez no pulo do caramelo: a gravidade muda a velocidade e a velocidade '
              'muda a posição.'},
        {'p': 'O `dt` é o tempo desde o quadro anterior. Multiplicar por ele faz o jogo andar na mesma rapidez em qualquer '
              'aparelho. Mas só a rapidez fica igual: o **caminho** muda. Com dt grande, a curva do pulo vira uma escada de '
              'pontos distantes, e a altura máxima muda um pouco.'},
        {'fig': 'passo', 'legenda': 'A mesma bola, rápida, contra uma parede fina. Com passos curtos ela cai dentro da parede e '
                                    'bate; com passos longos ela pula de um lado para o outro sem nunca estar dentro.'},
        {'h': 'Atravessar paredes'},
        {'p': 'Se a colisão só testa "está dentro agora?", um objeto rápido pode estar antes da parede num quadro e depois '
              'dela no seguinte. Esse problema tem nome: **tunelamento**. Ele aparece com objetos rápidos, paredes finas e '
              'aparelhos lentos, justamente no celular mais simples da turma.'},
        {'h': 'Passo fixo'},
        {'p': 'A solução clássica é separar o quadro da física. O jogo guarda o tempo que passou numa conta (`sobra += dt`) e '
              'executa vários passos **pequenos e sempre iguais** enquanto houver tempo: `while (sobra >= passo) { fisica(passo); '
              'sobra -= passo; }`. A física fica igual em qualquer aparelho, e as colisões não pulam paredes. Outras saídas: '
              'deixar paredes grossas, limitar a velocidade máxima ou testar o segmento entre a posição antiga e a nova.'},
        {'dica': 'Quando o jogo trava por um instante (uma notificação, por exemplo), o próximo dt pode ser enorme e jogar o '
                 'personagem através do chão. Limite o dt: `if (dt > 0.05) dt = 0.05;`.', 'titulo': 'Cuidado com o dt gigante'},
    ],
    [
        {'q': 'No Euler semi-implícito, o que se atualiza primeiro?', 'ops': ['A posição', 'A velocidade', 'O desenho', 'O dt'], 'ok': 1,
         'exp': 'Primeiro vel += aceleração * dt, depois pos += vel * dt.'},
        {'q': 'O que é tunelamento?', 'ops': ['Um efeito de câmera', 'Um objeto rápido atravessar uma parede entre dois passos', 'Um tipo de mapa', 'Pular duas vezes'], 'ok': 1,
         'exp': 'Num passo ele está antes da parede, no outro já está depois, e nunca dentro.'},
        {'q': 'O que o passo fixo garante?', 'ops': ['Mais quadros por segundo', 'A mesma física em qualquer aparelho', 'Sprites mais bonitos', 'Som sem atraso'], 'ok': 1,
         'exp': 'Os passos da física têm sempre o mesmo tamanho, não importa o ritmo dos quadros.'},
        {'q': 'Qual NÃO ajuda contra o tunelamento?', 'ops': ['Paredes mais grossas', 'Limitar a velocidade', 'Passos menores', 'Aumentar o dt'], 'ok': 3,
         'exp': 'Um dt maior faz passos mais longos e piora o problema.'},
    ],
)

leitura(
    'Flame: colisões com hitboxes',
    'Matemática de jogos: colisão em detalhes',
    'Leitura: os testes de colisão mais usados (círculo, retângulo, círculo com retângulo) e como empurrar um objeto para '
    'fora do outro. No código, você arrasta as formas e vê cada teste.',
    'Em ▶ Testar, arraste a forma laranja em cada modo. Depois mude o raio, o tamanho do retângulo e esconda a seta de '
    'empurrão.',
    'colisao',
    [
        ['Círculos maiores', 'Troque double raio = 50 por 70.', r'double\s+raio\s*=\s*(?!50\b)\d+'],
        ['Retângulo comprido', 'Troque Size tamanho = const Size(110, 80) por const Size(200, 40).', r'Size\s+tamanho\s*=\s*const\s+Size\(\s*(?!110\b)\d+'],
        ['Sem empurrão', 'Troque bool mostrarEmpurrao = true por false.', r'mostrarEmpurrao\s*=\s*false'],
    ],
    [
        {'h': 'Detectar e resolver'},
        {'p': 'Colisão tem duas partes. **Detectar** é responder "estão se tocando?". **Resolver** é decidir o que fazer: '
              'tirar vida, pegar o osso, ou empurrar um para fora do outro. Os jogos usam formas simples (círculos e '
              'retângulos) no lugar do desenho, porque o teste fica rápido. Essas formas são as **hitboxes**.'},
        {'fig': 'colisao', 'legenda': 'À esquerda, dois círculos: tocam quando a distância entre os centros é menor que a soma '
                                      'dos raios. À direita, dois retângulos: tocam quando as faixas em x e em y se cruzam.'},
        {'h': 'Os três testes'},
        {'p': '**Círculo com círculo**: `(a - b).distance < ra + rb`. **Retângulo com retângulo alinhados** (AABB): se cruzam '
              'quando `a.left < b.right && a.right > b.left && a.top < b.bottom && a.bottom > b.top`, que é o `overlaps` do '
              'Rect. **Círculo com retângulo**: acha o ponto do retângulo mais perto do centro (com `clamp` em x e em y) e '
              'testa se ele está dentro do círculo.'},
        {'p': 'Retângulos girados e polígonos usam o **teorema do eixo separador** (SAT): se existe uma linha que separa as '
              'duas formas, elas não se tocam. O Flame faz isso por você com `PolygonHitbox`.'},
        {'h': 'Empurrar para fora'},
        {'p': 'Para resolver uma batida contra parede, calcule o quanto um retângulo entrou no outro em cada lado e empurre '
              'pelo lado mais curto: é o vetor verde da demonstração. O jogo de plataforma da Parte 7 faz isso eixo por eixo, '
              'o que evita empurrões estranhos nos cantos.'},
        {'dica': 'Testar todo mundo contra todo mundo cresce rápido: 100 objetos dão quase 5 mil pares. Jogos maiores dividem o '
                 'mundo em células (uma grade) e só testam quem está na mesma célula. O HasCollisionDetection do Flame já faz '
                 'uma triagem assim.', 'titulo': 'Muitos objetos'},
    ],
    [
        {'q': 'Dois círculos de raio 30 têm centros a 50 pixels de distância. Estão colidindo?', 'ops': ['Sim', 'Não', 'Só se forem retângulos', 'Depende da cor'], 'ok': 0,
         'exp': '50 é menor que 30 + 30 = 60.'},
        {'q': 'Qual teste o Rect.overlaps faz?', 'ops': ['Círculo com círculo', 'Retângulos alinhados aos eixos (AABB)', 'Polígonos girados', 'Pixel por pixel'], 'ok': 1,
         'exp': 'Compara as bordas esquerda, direita, de cima e de baixo dos dois retângulos.'},
        {'q': 'Para círculo com retângulo, qual ponto se testa?', 'ops': ['O canto de cima', 'O centro do retângulo', 'O ponto do retângulo mais perto do centro do círculo', 'Qualquer ponto'], 'ok': 2,
         'exp': 'Se o ponto mais perto está dentro do círculo, eles se tocam.'},
        {'q': 'Ao resolver uma batida, por qual lado se empurra?', 'ops': ['Sempre para cima', 'Pelo lado em que entrou menos', 'Pelo lado em que entrou mais', 'Para a esquerda'], 'ok': 1,
         'exp': 'O menor empurrão desfaz a sobreposição com o menor movimento.'},
    ],
)

leitura(
    'Joystick e botões na tela',
    'Arte de jogos: interface e acessibilidade',
    'Leitura: o que mostrar no HUD, onde pôr os controles no celular e como deixar o jogo jogável por mais gente. No '
    'código, uma tela de jogo com opções de acessibilidade.',
    'Em ▶ Testar, mude o tamanho do texto e dos botões, ligue o modo canhoto e as cores para daltonismo. Depois deixe os '
    'botões maiores desde o início e comece com uma vida.',
    'hud',
    [
        ['Botões maiores', 'Troque double tamanhoBotao = 56 por 72.', r'tamanhoBotao\s*=\s*(?!56\b)\d+'],
        ['Cores seguras', 'Troque bool coresSeguras = false por true.', r'coresSeguras\s*=\s*true'],
        ['Uma vida', 'Troque int vidas = 2 por 1.', r'int\s+vidas\s*=\s*(?!2\b)\d+'],
    ],
    [
        {'h': 'O HUD'},
        {'p': 'O **HUD** é tudo que fica por cima do jogo: vidas, pontos, tempo, mapa, botões. Ele deve mostrar só o que o '
              'jogador precisa **agora**, num lugar fixo e fácil de achar. Informação que muda o tempo todo (vidas, pontos) '
              'costuma ficar nos cantos de cima; avisos aparecem perto de onde a ação acontece e somem.'},
        {'fig': 'hud', 'legenda': 'No celular, os polegares alcançam bem os cantos de baixo (em verde). Por isso os botões vão '
                                  'lá, e as informações vão no alto, onde a mão não cobre.'},
        {'h': 'Controles no celular'},
        {'p': 'Os botões ficam na **zona do polegar**, longe das bordas que o sistema usa para gestos. Cada um precisa de pelo '
              'menos **48** de área de toque (a recomendação do Material Design), mesmo que o desenho seja menor. Botões '
              'que se usam juntos (andar e pular) ficam um em cada mão. E vale oferecer o **modo canhoto**, que troca os '
              'lados.'},
        {'h': 'Acessibilidade'},
        {'p': 'Cerca de 1 em cada 12 homens tem algum tipo de daltonismo, e o par vermelho e verde é o mais confundido. Por '
              'isso a regra é: **nunca use só a cor** para informar. Junte cor com símbolo, forma ou texto (✓ e ✗ na '
              'demonstração) e prefira pares como azul e laranja. Outras opções que custam pouco: tamanho do texto, '
              'legendas para os sons, desligar a tremida de tela, velocidade do jogo e controles remapeáveis.'},
        {'dica': 'Jogue o seu jogo com o som desligado, com o celular longe do rosto e com uma mão só. Cada coisa difícil '
                 'nesses testes é uma melhoria para todo mundo, não só para quem precisa.', 'titulo': 'Teste rápido'},
    ],
    [
        {'q': 'Onde ficam melhor os botões num jogo de celular deitado?', 'ops': ['No meio da tela', 'Nos cantos de baixo, na zona do polegar', 'No alto, ao lado das vidas', 'Atrás do personagem'], 'ok': 1,
         'exp': 'Os polegares alcançam os cantos de baixo sem cobrir o jogo.'},
        {'q': 'Qual o tamanho mínimo recomendado para a área de toque?', 'ops': ['12', '24', '48', '200'], 'ok': 2,
         'exp': 'O Material Design recomenda pelo menos 48 por 48.'},
        {'q': 'Por que não informar só pela cor?', 'ops': ['Porque gasta bateria', 'Porque quem tem daltonismo pode não distinguir', 'Porque o Flutter não deixa', 'Porque fica feio'], 'ok': 1,
         'exp': 'Cor junto com símbolo ou texto funciona para todos.'},
        {'q': 'Qual par de cores é mais seguro para daltonismo?', 'ops': ['Vermelho e verde', 'Azul e laranja', 'Verde e marrom', 'Vermelho e marrom'], 'ok': 1,
         'exp': 'Azul e laranja continuam diferentes nos tipos mais comuns de daltonismo.'},
    ],
    parte='Parte 6 · Celular, física e mapas',
)

leitura(
    'Plataforma: gravidade e colisão com o mapa',
    'Game design: design de fases e ritmo',
    'Leitura: como montar uma fase que ensina, desafia e dá respiro, e como pensar o ritmo ao longo dela. No código, um '
    'gráfico de tensão que avisa os problemas mais comuns.',
    'Em ▶ Testar, toque nos trechos para trocar o tipo e observe os avisos. Depois aceite três desafios seguidos, comece a '
    'fase com um desafio e deixe o chefe menos intenso.',
    'ritmo',
    [
        ['Três seguidos', 'Troque final int limiteSeguidos = 2 por 3.', r'limiteSeguidos\s*=\s*(?!2\b)\d+'],
        ['Começo diferente', "Na lista trechos, troque o primeiro 'ensina' por 'desafio' e veja dois avisos.", r"trechos\s*=\s*\[\s*'(?!ensina')"],
        ['Chefe menos intenso', "No mapa tipos, troque 'chefe': 1.0 por 'chefe': 0.9.", r"'chefe'\s*:\s*0\.\d+"],
    ],
    [
        {'h': 'Uma fase conta uma história'},
        {'p': 'Uma boa fase não é uma pilha de obstáculos: ela tem começo, meio e fim. Um padrão muito usado tem quatro '
              'tempos: **apresentar** uma ideia num lugar seguro, **praticar** com pouco risco, **desafiar** com tudo junto e '
              'terminar com uma **surpresa** ou um momento forte. Muitas fases clássicas de plataforma seguem exatamente '
              'esse roteiro com uma mecânica só.'},
        {'fig': 'ritmo', 'legenda': 'A tensão de uma fase ao longo do tempo: sobe nos desafios, cai nos descansos e termina no '
                                    'ponto mais alto. O zigue-zague mantém o jogador atento sem esgotá-lo.'},
        {'h': 'Ritmo: tensão e respiro'},
        {'p': 'Depois de um trecho difícil, o jogador precisa de um **respiro**: um lugar seguro, um osso de presente, uma '
              'paisagem. Isso deixa o próximo desafio mais forte por contraste. Desafios demais em sequência cansam; '
              'descanso demais entedia. A demonstração conta quantos trechos difíceis vêm seguidos e avisa quando passa do '
              'limite.'},
        {'h': 'O cenário ensina'},
        {'p': 'O jogador lê o cenário. Um osso no alto ensina que dá para pular até lá; uma fileira de ossos indica o '
              'caminho; uma plataforma diferente chama atenção. **Pontos de controle** (checkpoints) antes de trechos '
              'difíceis evitam repetir a fase inteira, e caminhos secretos premiam quem explora sem atrapalhar quem só quer '
              'passar.'},
        {'dica': 'Desenhe a fase primeiro em papel quadriculado ou numa planilha: cada célula é um bloco. É o mesmo formato do '
                 'Tiled e das listas de texto dos mapas da Oficina, e é muito mais rápido de mudar.', 'titulo': 'Papel antes do código'},
    ],
    [
        {'q': 'Qual é a ordem do roteiro de quatro tempos?', 'ops': ['Desafiar, praticar, apresentar, surpreender', 'Apresentar, praticar, desafiar, surpreender', 'Surpreender, desafiar, praticar, apresentar', 'Praticar, desafiar, apresentar, surpreender'], 'ok': 1,
         'exp': 'Primeiro a ideia num lugar seguro, depois prática, depois o desafio e por fim a surpresa.'},
        {'q': 'Para que serve um trecho de descanso?', 'ops': ['Para encher a fase', 'Para baixar a tensão e dar força ao próximo desafio', 'Para o jogo carregar', 'Não serve para nada'], 'ok': 1,
         'exp': 'O contraste entre tensão e respiro mantém o jogador atento.'},
        {'q': 'Uma fileira de ossos no ar indica...', 'ops': ['Um bug', 'Um caminho para seguir', 'Que a fase acabou', 'Perigo'], 'ok': 1,
         'exp': 'Itens colecionáveis guiam o olhar e o caminho do jogador.'},
        {'q': 'Onde colocar um ponto de controle?', 'ops': ['No começo da fase', 'Logo antes de um trecho difícil', 'Depois da chegada', 'Em lugar nenhum'], 'ok': 1,
         'exp': 'Assim quem erra no trecho difícil não repete tudo de novo.'},
    ],
)

leitura(
    'Geração procedural: semente, labirinto e cavernas',
    'Game design: economia e balanceamento',
    'Leitura: moedas, preços e melhorias, como o custo deve crescer e por que se balanceia com números. No código, uma '
    'loja de melhorias com o gráfico da espera para cada nível.',
    'Em ▶ Testar, mexa no crescimento do custo e no ganho por nível e veja as barras ficarem laranjas. Depois mude o preço '
    'inicial, o ganho base e o limite de paciência.',
    'economia',
    [
        ['Começo mais caro', 'Troque double custoBase = 10 por 25.', r'custoBase\s*=\s*(?!10\b)\d+'],
        ['Ganho inicial maior', 'Troque double ganhoBase = 5 por 8.', r'ganhoBase\s*=\s*(?!5\b)\d+'],
        ['Paciência curta', 'No pintor Barras, troque valores[i] > 10 por valores[i] > 5.', r'valores\[i\]\s*>\s*(?!10\b)\d+'],
    ],
    [
        {'h': 'Fontes e ralos'},
        {'p': 'Todo jogo com moeda tem **fontes** (de onde os ossos vêm: fases, baús, recompensas diárias) e **ralos** (para '
              'onde vão: melhorias, roupas, vidas extras). Se a fonte for maior que o ralo por muito tempo, os ossos perdem '
              'o valor; se o ralo for maior, o jogador sente que nunca consegue nada. Balancear é ajustar os dois.'},
        {'fig': 'economia', 'legenda': 'O custo de cada nível cresce multiplicando (vermelho); o ganho cresce somando (verde). '
                                       'No começo o jogador compra rápido; com o tempo, cada nível pede mais espera.'},
        {'h': 'Curvas de custo'},
        {'p': 'O jeito mais comum é o custo **exponencial**: `custo = base * crescimento ^ nível`. Com crescimento 1,5, cada '
              'nível custa 50% a mais que o anterior. Como o ganho geralmente cresce em linha reta, a espera entre compras '
              'aumenta aos poucos: rápido no começo (o jogador se empolga) e mais lento depois (cada compra vale mais). '
              'Crescimento perto de 1 deixa tudo barato demais; perto de 2 vira um muro.'},
        {'h': 'Balancear com números'},
        {'p': 'Em vez de chutar preços, escreva a fórmula e olhe a tabela: quanto custa, quanto ganha, quanto tempo espera. A '
              'demonstração pinta de laranja as esperas acima de 10 minutos, um limite de paciência que você escolhe. '
              'Uma planilha faz o mesmo e é a ferramenta preferida de quem desenha economias de jogo.'},
        {'dica': 'Nunca venda vantagem que faça o jogador sentir que precisa pagar para continuar. Uma economia justa '
                 'recompensa quem joga, e o jogador percebe quando não é assim.', 'titulo': 'Justo com o jogador'},
    ],
    [
        {'q': 'Com custo base 10 e crescimento 2, quanto custa o nível 3 (contando do 0)?', 'ops': ['30', '60', '80', '16'], 'ok': 2,
         'exp': '10 × 2³ = 10 × 8 = 80.'},
        {'q': 'O que são os "ralos" da economia?', 'ops': ['Os bugs do jogo', 'Os lugares onde o jogador gasta a moeda', 'As fontes de moeda', 'As fases secretas'], 'ok': 1,
         'exp': 'Ralos tiram moeda do jogo: lojas, melhorias, consumíveis.'},
        {'q': 'Por que o custo exponencial combina com ganho linear?', 'ops': ['Porque deixa tudo grátis', 'Porque a espera entre compras cresce aos poucos', 'Porque o Dart exige', 'Porque o jogo acaba mais rápido'], 'ok': 1,
         'exp': 'O custo cresce mais rápido que o ganho, então cada compra pede um pouco mais de jogo.'},
        {'q': 'Qual a melhor ferramenta para balancear preços?', 'ops': ['Chutar e torcer', 'Uma tabela ou planilha com as fórmulas', 'Copiar outro jogo', 'Deixar todos iguais'], 'ok': 1,
         'exp': 'Com os números à vista, dá para ver onde a espera fica longa demais.'},
    ],
)

leitura(
    'Geração procedural: semente, labirinto e cavernas',
    'Matemática de jogos: probabilidade e sorteio',
    'Leitura: chance, sorteio com pesos e como o acaso parece injusto. No código, uma tabela de prêmios de baú e a '
    'garantia contra o azar.',
    'Em ▶ Testar, abra baús de 1 em 1 e de 100 em 100 e compare o esperado com o que saiu. Ligue a garantia. Depois deixe o '
    'dourado mais raro, a garantia mais curta e crie um prêmio novo.',
    'sorteio',
    [
        ['Dourado raríssimo', "Na tabela, troque Item('Osso dourado', 3, por Item('Osso dourado', 1,.", r"Item\('Osso dourado',\s*(?!3\b)\d+"],
        ['Garantia curta', 'Troque final int garantia = 40 por 20.', r'garantia\s*=\s*(?!40\b)\d+'],
        ['Prêmio novo', "Na tabela, acrescente Item('Petisco', 20, Color(0xFFA1887F)), antes do Osso dourado.", r"Item\(\s*'(?!Osso'|Bola'|Coleira'|Osso dourado')[^']+'\s*,\s*\d+"],
    ],
    [
        {'h': 'Chance é proporção'},
        {'p': 'Uma **probabilidade** vai de 0 (nunca) a 1 (sempre). Com 3 em 100, o osso dourado sai em média 3 vezes a '
              'cada 100 baús. Em média: em 100 baús de verdade podem sair 1, 5 ou nenhum. Quanto mais baús, mais perto dos '
              '3% fica a conta, e é isso que a demonstração mostra com o botão Abrir 100.'},
        {'fig': 'sorteio', 'legenda': 'Sorteio com pesos: os prêmios ocupam faixas de 0 a 99 do tamanho do seu peso. Sorteia-se '
                                      'um número e vê-se em que faixa ele caiu.'},
        {'h': 'Sorteio com pesos'},
        {'p': 'Em vez de porcentagens, cada prêmio recebe um **peso**. Some todos, sorteie um número de 0 até a soma e '
              'percorra a lista diminuindo o número pelo peso de cada um até achar a faixa. Assim fica fácil acrescentar '
              'um prêmio novo sem refazer todas as contas: a soma muda sozinha.'},
        {'h': 'O acaso parece injusto'},
        {'p': 'Sequências longas sem o prêmio raro acontecem mais do que as pessoas imaginam. Com 3% de chance, a chance de '
              'passar 40 baús seguidos sem nenhum dourado é de quase 30%. Por isso muitos jogos usam uma **garantia** (se '
              'passar de N tentativas, o próximo é garantido) ou um **saco de sorteio**: põe todos os resultados num saco, '
              'embaralha e tira um por um, sem repor. O jogador sente o jogo mais justo, e a média continua parecida.'},
        {'dica': 'Para testar, sorteie milhares de vezes e conte, como no botão Abrir 100. Uma tabela de prêmios com um erro '
                 'de soma aparece na hora na contagem.', 'titulo': 'Confira contando'},
    ],
    [
        {'q': 'Pesos 60, 25, 12 e 3. Qual a chance do primeiro?', 'ops': ['25%', '60%', '6%', '100%'], 'ok': 1,
         'exp': 'A soma é 100, então 60 de 100 = 60%.'},
        {'q': 'Num sorteio com pesos, o número sorteado vai...', 'ops': ['De 1 a 6', 'De 0 até a soma dos pesos', 'De 0 a 1 sempre', 'Do maior peso ao menor'], 'ok': 1,
         'exp': 'Depois se vê em que faixa de peso o número caiu.'},
        {'q': 'Para que serve a garantia contra o azar?', 'ops': ['Para dar sempre o prêmio raro', 'Para limitar a sequência máxima sem o prêmio', 'Para deixar o jogo mais difícil', 'Para economizar memória'], 'ok': 1,
         'exp': 'Depois de N tentativas sem o prêmio, o próximo é garantido.'},
        {'q': 'O que é um saco de sorteio?', 'ops': ['Um item do jogo', 'Pôr os resultados num saco e tirar sem repor', 'Sortear duas vezes', 'Um tipo de mapa'], 'ok': 1,
         'exp': 'Como tirar cartas de um baralho: todos saem antes de repetir.'},
    ],
)

leitura(
    'Multijogador em tempo real com Supabase',
    'Programação de jogos: arquitetura em camadas',
    'Leitura: como organizar um jogo que cresce, separando os dados e as regras do desenho. No código, um estado de jogo '
    'em ChangeNotifier e widgets que só mostram e mandam comandos.',
    'Em ▶ Testar, pegue ossos, leve dano e veja o registro de eventos. Depois mude as regras só no modelo: mais vidas, '
    'subir de nível mais devagar e um evento novo.',
    'arquitetura',
    [
        ['Cinco vidas', 'No EstadoJogo, troque final int vidasIniciais = 3 por 5 e int vidas = 3 por 5.', r'vidasIniciais\s*=\s*5[\s\S]*int\s+vidas\s*=\s*5'],
        ['Nível a cada 10', 'Em pegarOsso, troque if (ossos % 5 == 0) por if (ossos % 10 == 0).', r'ossos\s*%\s*(?!5\b)\d+\s*==\s*0'],
        ['Evento novo', "Em reiniciar, troque registrar('jogo novo') por registrar('jogo novo com $vidas vidas').", r"registrar\('jogo novo [^']+'\)"],
    ],
    [
        {'h': 'Quando o jogo cresce'},
        {'p': 'Num jogo pequeno, dá para deixar tudo numa classe só. Quando ele cresce, mudar uma regra quebra o desenho, e '
              'mudar o desenho quebra uma regra. A saída é separar em **camadas**: cada parte do código tem uma tarefa e '
              'conversa com as outras de um jeito combinado.'},
        {'fig': 'camadas', 'legenda': 'O visual manda comandos para o modelo (pegarOsso); o modelo muda os dados e avisa quem '
                                      'estiver ouvindo (notifyListeners). O modelo não sabe como é desenhado.'},
        {'h': 'Modelo e visual'},
        {'p': 'O **modelo** guarda os dados (vidas, ossos, nível) e as regras (a cada 5 ossos sobe de nível). Ele não importa '
              'nada visual, então dá para testar com `dart test` sem abrir o jogo. O **visual** (widgets do Flutter ou '
              'componentes do Flame) só mostra o modelo e chama os métodos dele. Com `ChangeNotifier`, o modelo avisa '
              'quando mudou, e o `ListenableBuilder` redesenha.'},
        {'p': 'Num jogo Flame, o mesmo vale: a classe do jogo guarda o estado, os componentes desenham e mandam ações, e o '
              'HUD em Flutter ouve o estado. Com o tempo, o código também se divide em arquivos e pastas: `lib/modelo/`, '
              '`lib/componentes/`, `lib/telas/`.'},
        {'h': 'Eventos'},
        {'p': 'O registro de eventos da demonstração é uma ideia poderosa: tudo que acontece vira uma mensagem ("pegou osso", '
              '"levou dano"). A partir dela dá para tocar sons, mostrar conquistas, salvar estatísticas e fazer replays, sem '
              'espalhar código pelas classes.'},
        {'dica': 'Se uma regra do jogo precisa de um BuildContext ou de um Canvas, ela provavelmente está na camada errada.',
         'titulo': 'Sinal de alerta'},
    ],
    [
        {'q': 'O que fica no modelo?', 'ops': ['Os widgets', 'Os dados e as regras do jogo', 'As imagens', 'Os sons'], 'ok': 1,
         'exp': 'O modelo guarda o estado e as regras, sem nada visual.'},
        {'q': 'Para que serve notifyListeners()?', 'ops': ['Para tocar um som', 'Para avisar quem ouve que o estado mudou', 'Para fechar o app', 'Para salvar no Hive'], 'ok': 1,
         'exp': 'Quem está ouvindo (como o ListenableBuilder) redesenha.'},
        {'q': 'Qual a vantagem de o modelo não importar nada visual?', 'ops': ['Fica mais bonito', 'Dá para testar as regras sem abrir o jogo', 'Ocupa menos memória', 'Nenhuma'], 'ok': 1,
         'exp': 'Testes rodam rápido e sem tela.'},
        {'q': 'Um registro de eventos ajuda a...', 'ops': ['Deixar o jogo mais lento', 'Ligar sons, conquistas e estatísticas sem espalhar código', 'Apagar o progresso', 'Trocar a fonte'], 'ok': 1,
         'exp': 'Cada sistema ouve os eventos que interessam a ele.'},
    ],
)

leitura(
    'Projeto · Trilha do Caramelo',
    'Game design: testar com jogadores',
    'Leitura: como observar pessoas jogando, o que medir e como transformar o que você vê em mudanças. No código, um mapa '
    'de calor de jogadores simulados mostra onde eles passam e onde morrem.',
    'Em ▶ Testar, simule jogadores e alterne entre passos e mortes. Depois deixe os jogadores mais espertos, dê menos '
    'passos a eles e tire um espinho do mapa.',
    'playtest',
    [
        ['Jogadores espertos', 'Troque double vontade = 0.6 por 0.85.', r'vontade\s*=\s*0\.(?!6\b)\d+'],
        ['Pouca paciência', 'Troque final int limitePassos = 250 por 120.', r'limitePassos\s*=\s*(?!250\b)\d+'],
        ['Menos espinhos', "No mapa fase, troque a linha '#...x.....#...#' por '#.........#...#'.", r"'#\.\.\.\.\.\.\.\.\.#\.\.\.#'"],
    ],
    [
        {'h': 'Você não é o seu jogador'},
        {'p': 'Quem fez o jogo sabe onde está cada segredo e já jogou a fase cem vezes. Por isso não consegue mais ver o jogo '
              'com olhos de novato. O **playtest** é ver outras pessoas jogarem. É o teste mais importante de um jogo, e o '
              'mais barato.'},
        {'h': 'Observar sem ajudar'},
        {'p': 'Dê o celular e fique quieto. Não explique, não aponte, não defenda o jogo. Anote onde a pessoa hesita, onde '
              'erra, onde ri, onde desiste e o que ela fala. Peça para pensar em voz alta. No fim, faça perguntas abertas: '
              '"o que foi mais difícil?", "o que você achou que era aquele bloco?".'},
        {'fig': 'calor', 'legenda': 'Um mapa de calor das mortes: as casas mais vermelhas são onde mais gente morreu. Um ponto '
                                    'muito quente pode ser um trecho injusto ou mal explicado.'},
        {'h': 'Medir'},
        {'p': 'Com muita gente, observar não basta: o jogo pode **registrar** o que acontece (onde morreu, quanto tempo levou, '
              'onde desistiu) e mostrar num mapa de calor, como na demonstração. Os números dizem **onde** está o problema; '
              'a observação diz **por quê**. Os dois juntos dizem o que mudar.'},
        {'p': 'Mude uma coisa de cada vez e teste de novo. Se mudar o pulo, a fase e os inimigos ao mesmo tempo, não dá para '
              'saber o que resolveu (ou o que piorou).'},
        {'dica': 'Pergunte antes de coletar dados e não guarde nada que identifique a pessoa. Mortes por trecho e tempo de '
                 'fase bastam para melhorar o jogo.', 'titulo': 'Dados com respeito'},
    ],
    [
        {'q': 'Por que quem fez o jogo não é um bom testador?', 'ops': ['Porque não sabe jogar', 'Porque já conhece tudo e não vê como um novato', 'Porque joga rápido demais', 'Porque é proibido'], 'ok': 1,
         'exp': 'Conhecer cada segredo esconde o que é difícil para quem chega agora.'},
        {'q': 'O que fazer enquanto a pessoa joga?', 'ops': ['Explicar cada parte', 'Observar e anotar sem ajudar', 'Jogar junto', 'Corrigir quando ela errar'], 'ok': 1,
         'exp': 'Ajudar esconde exatamente os problemas que o teste deveria achar.'},
        {'q': 'Um ponto muito quente no mapa de mortes indica...', 'ops': ['Que a fase está perfeita', 'Um trecho que talvez esteja difícil ou mal explicado', 'Um bug de desenho', 'Que ninguém passou ali'], 'ok': 1,
         'exp': 'É o lugar para observar de perto no próximo teste.'},
        {'q': 'Por que mudar uma coisa de cada vez?', 'ops': ['Para demorar mais', 'Para saber qual mudança resolveu', 'Porque o Flutter só deixa uma', 'Não precisa'], 'ok': 1,
         'exp': 'Com várias mudanças juntas, não dá para saber o efeito de cada uma.'},
    ],
)

leitura(
    'Projeto · Trilha do Caramelo',
    'Produção: publicar o jogo',
    'Leitura: o caminho do código até a loja, com nome, ícone, versão, assinatura e página do jogo. No código, uma lista '
    'de verificação que fica salva no aparelho.',
    'Em ▶ Testar, marque as etapas que você já sabe fazer. Depois troque a versão, acrescente uma etapa e mude o texto '
    'final.',
    'publicar',
    [
        ['Versão nova', "Troque const String versao = '1.0.0+1' por '1.0.1+2'.", r"versao\s*=\s*'(?!1\.0\.0\+1')[\d.]+\+\d+'"],
        ['Etapa nova', "Na lista etapas, acrescente Etapa('Qualidade', 'Pedir para 3 pessoas jogarem', 'Playtest antes de publicar.'), antes da primeira etapa da Loja.", r"Etapa\(\s*'Qualidade'\s*,\s*'(?!Testar num celular|Sem prints)"],
        ['Outra mensagem', "Troque 'Tudo pronto: pode enviar para a loja! 🎉' por uma mensagem sua.", r"Text\(\s*'(?!Tudo pronto: pode enviar para a loja! 🎉')[^']+'\s*,\s*style:\s*TextStyle\(fontSize: 18\)"],
    ],
    [
        {'h': 'Do código para o mundo'},
        {'p': 'Publicar é transformar o projeto num pacote que outras pessoas instalam. O Flutter gera pacotes para várias '
              'lojas e para a web com um comando: `flutter build appbundle` (Google Play), `flutter build ipa` (App Store, '
              'num Mac) e `flutter build web` (qualquer site, como o itch.io ou o GitHub Pages, que aceitam jogos de '
              'navegador sem taxa).'},
        {'fig': 'loja', 'legenda': 'O caminho da publicação: cada passo depende do anterior. O botão ⬇ Projeto da Oficina entrega '
                                   'o primeiro deles, o código pronto para abrir no computador.'},
        {'h': 'Identidade'},
        {'p': 'Antes do pacote: o **nome** que aparece embaixo do ícone, o **ícone** em vários tamanhos (o pacote '
              'flutter_launcher_icons gera todos a partir de uma imagem), a **tela de abertura** e o **id do pacote** '
              '(como br.edu.escola.caramelo), que nunca mais muda depois de publicado.'},
        {'h': 'Versão e assinatura'},
        {'p': 'No `pubspec.yaml`, `version: 1.0.0+1` tem duas partes: o nome da versão que o jogador vê (1.0.0) e o número '
              'do pacote (+1), que precisa crescer a cada envio para a loja. Para a Google Play, o pacote é **assinado** com '
              'uma chave sua: guarde a chave e a senha com cuidado, porque sem elas não dá para enviar atualizações.'},
        {'h': 'A página da loja'},
        {'p': 'A loja pede descrição, capturas de tela, classificação indicativa e uma **política de privacidade** (mesmo que '
              'o jogo não colete nada, diga isso). Jogos com ranking online coletam nomes: explique o que é guardado e para '
              'quê. A Google Play cobra uma taxa única de conta de desenvolvedor; a App Store, uma anual.'},
        {'dica': 'Antes de publicar para todo mundo, use os testes fechados das lojas (teste interno da Google Play, '
                 'TestFlight da Apple) com a turma. É o playtest com o jogo já instalado de verdade.', 'titulo': 'Teste fechado primeiro'},
    ],
    [
        {'q': 'Qual comando gera o pacote para a Google Play?', 'ops': ['flutter run', 'flutter build appbundle', 'flutter pub get', 'flutter clean'], 'ok': 1,
         'exp': 'O appbundle (.aab) é o formato que a Google Play pede.'},
        {'q': 'Em version: 1.2.0+7, o que precisa crescer a cada envio?', 'ops': ['O 1', 'O 2', 'O 7, número do pacote', 'Nada'], 'ok': 2,
         'exp': 'A loja recusa um pacote com número igual ou menor que o anterior.'},
        {'q': 'O que acontece se você perder a chave de assinatura?', 'ops': ['Nada', 'Não consegue mais enviar atualizações do mesmo jogo', 'O jogo some da loja', 'O ícone muda'], 'ok': 1,
         'exp': 'As atualizações precisam ser assinadas com a mesma chave.'},
        {'q': 'Onde dá para publicar um jogo Flutter web sem taxa?', 'ops': ['Só na App Store', 'Em sites como itch.io ou GitHub Pages', 'Em nenhum lugar', 'Só no Google Drive'], 'ok': 1,
         'exp': 'O flutter build web gera arquivos que qualquer hospedagem de site aceita.'},
    ],
)


# ------------------------------------------------------------------ Leituras da terceira leva
leitura(
    'Diálogos e escolhas',
    'Game design: narrativa e personagens',
    'Leitura: como contar uma história num jogo, personagens com vontade própria e o cuidado com as ramificações. No '
    'código, o mapa de uma história com escolhas conta os finais e os caminhos possíveis.',
    'Em ▶ Testar, toque nas cenas para ver aonde cada uma leva. Depois crie um final novo, ligue uma cena a outra e veja '
    'o número de caminhos mudar.',
    'narrativa',
    [
        ['Final novo', "Troque 'Sozinho': [] por 'Sozinho': ['Achou'], acrescente 'Achou': [] no mapa historia e 'Achou': 3 no mapa passo.", r"'Achou'\s*:\s*\[\]"],
        ['Mais um caminho', "Troque 'Fuga': [] por 'Fuga': ['Desculpa']: quem fugiu ainda pode voltar atrás.", r"'Fuga'\s*:\s*\['Desculpa'\]"],
        ['Começo diferente', "Troque 'Muro': ['Gentil', 'Bravo'] por 'Muro': ['Gentil', 'Bravo', 'Fuga'].", r"'Muro'\s*:\s*\['Gentil',\s*'Bravo',\s*'Fuga'\]"],
    ],
    [
        {'h': 'História que se joga'},
        {'p': 'Num livro, o leitor acompanha a história; num jogo, o jogador **faz** a história. Por isso a narrativa de jogo '
              'mostra pelo que acontece na tela mais do que conta com texto. Um cenário destruído, um gato que foge e volta, '
              'um osso escondido num lugar estranho contam coisas sem nenhuma frase. Quando houver texto, ele deve ser curto e '
              'dito por alguém.'},
        {'h': 'Personagens com vontade'},
        {'p': 'Um bom personagem quer alguma coisa e tem um jeito próprio de falar. O Mingau quer o muro dele e fala com '
              'desconfiança; o caramelo quer ossos e amigos. Quando o que o jogador quer esbarra no que o personagem quer, '
              'nasce um conflito, e o conflito move a história. Antes de escrever falas, escreva numa linha o que cada '
              'personagem quer e do que ele tem medo.'},
        {'fig': 'narrativa', 'legenda': 'Uma história com escolhas é um mapa de cenas. Cada escolha abre um galho; galhos que se '
                                        'juntam de novo evitam que a história exploda em tamanho.'},
        {'h': 'Ramificações'},
        {'p': 'Cada escolha que leva a um lugar diferente dobra o trabalho: duas escolhas seguidas de dois caminhos já dão '
              'quatro histórias para escrever, testar e desenhar. Por isso os jogos fazem os galhos **voltarem a se juntar** '
              '(como a cena Desculpa, que leva de volta ao Segredo) e guardam as consequências em variáveis, como a amizade, '
              'que mudam um detalhe depois sem criar uma história inteira nova.'},
        {'dica': 'Escreva o roteiro como dados (o mapa de falas da aula de diálogos), não como código. Assim dá para revisar, '
                 'traduzir e acrescentar cenas sem mexer na lógica do jogo.', 'titulo': 'Roteiro é dado'},
    ],
    [
        {'q': 'O que significa "mostrar em vez de contar" num jogo?', 'ops': ['Escrever textos maiores', 'Deixar o cenário e as ações contarem a história', 'Não ter história', 'Usar só vídeos'], 'ok': 1,
         'exp': 'O jogador entende o que aconteceu olhando e jogando, sem precisar de um parágrafo.'},
        {'q': 'O que move uma história?', 'ops': ['O número de fases', 'O conflito entre o que os personagens querem', 'A cor do cenário', 'A música'], 'ok': 1,
         'exp': 'Quando vontades se chocam, algo precisa acontecer.'},
        {'q': 'Duas escolhas seguidas, cada uma com dois caminhos que não se juntam, dão quantos finais?', 'ops': ['2', '3', '4', '8'], 'ok': 2,
         'exp': '2 × 2 = 4 caminhos diferentes até o fim.'},
        {'q': 'Como evitar que a história cresça demais?', 'ops': ['Tirar todas as escolhas', 'Fazer galhos se juntarem e guardar consequências em variáveis', 'Escrever só finais tristes', 'Não testar'], 'ok': 1,
         'exp': 'Galhos que voltam e variáveis que mudam detalhes mantêm o tamanho controlado.'},
    ],
    parte='Parte 8 · Mais sistemas de jogo',
)

leitura(
    'Sala de jogos (galeria)',
    'Projeto final: o seu jogo',
    'Leitura: como planejar, construir e entregar um jogo seu do começo ao fim, com o documento do jogo, as etapas por '
    'semana e a ficha de avaliação. O código é o seu caderno do projeto, guardado no aparelho.',
    'Em ▶ Testar, preencha o documento do seu jogo, marque as etapas prontas e faça a sua autoavaliação. Depois ajuste as '
    'semanas e os pesos para o calendário da turma.',
    'gdd',
    [
        ['Mais uma pergunta', "Na lista perguntas, acrescente ['publico', 'Para quem é o jogo', 'Crianças de 8 a 12 anos'], no fim.", r"\['publico',"],
        ['Prazo da entrega', "Na última etapa, troque a semana 6 por 8: ['Menu, fim de jogo e entrega (link na 🕹 Galeria)', 8].", r"entrega \(link na 🕹 Galeria\)',\s*(?!6\b)\d+\]"],
        ['Pesos da ficha', "Na ficha, troque ['O ciclo principal é divertido e claro', 3] por 4 e ['Código organizado e comentado', 1] por 0.", r"divertido e claro',\s*4\][\s\S]*comentado',\s*0\]"],
    ],
    [
        {'h': 'Do zero a um jogo seu'},
        {'p': 'O projeto final junta tudo: você escolhe o jogo, planeja, constrói, testa com colegas e entrega um link na '
              'Galeria. O segredo é **começar pequeno**: um jogo curto e terminado vale mais que um jogo enorme pela metade. '
              'Se a ideia couber em uma frase ("um caramelo que foge dos gatos pegando ossos numa praça"), ela cabe no prazo.'},
        {'h': '1. O documento do jogo'},
        {'p': 'Antes do código, escreva o **documento de design** (GDD): nome, gênero, objetivo, ciclo principal, controles, '
              'como o desafio cresce, arte e som. Uma página basta. Ele serve para você não se perder e para o professor e '
              'os colegas entenderem a ideia antes de ela existir.'},
        {'fig': 'projeto', 'legenda': 'As seis etapas do projeto, uma por semana. Cada etapa termina com algo que dá para jogar ou '
                                      'mostrar, e o teste com colegas vem antes da entrega, não depois.'},
        {'h': '2. Etapas que dá para jogar'},
        {'p': 'Construa em camadas jogáveis: primeiro um **protótipo** com quadrados e círculos (o ciclo funciona e é '
              'divertido?), depois uma fase inteira do começo ao fim, depois arte e som no lugar das formas, depois o teste '
              'com três colegas, e só então menu, fim de jogo e entrega. Em qualquer semana você tem um jogo que funciona.'},
        {'h': '3. A ficha de avaliação'},
        {'p': 'A ficha diz o que conta e quanto: o ciclo divertido e claro pesa mais que tudo, depois funcionar sem travar, a '
              'dificuldade que ensina, a arte e o som e, por fim, o código organizado. Cada critério vale de 0 a 4. Use a '
              'ficha para se autoavaliar no meio do caminho: ela mostra onde vale a pena gastar a próxima semana.'},
        {'dica': 'Guarde uma cópia do código a cada etapa (o botão ⬇ Projeto baixa o .zip). Se algo quebrar, você volta para '
                 'a última versão que funcionava.', 'titulo': 'Versões'},
    ],
    [
        {'q': 'Qual projeto tem mais chance de ficar bom no prazo?', 'ops': ['Um jogo enorme com dez fases', 'Um jogo curto, com uma ideia clara, terminado', 'Um jogo sem documento', 'Um jogo só com arte'], 'ok': 1,
         'exp': 'Terminar e polir algo pequeno vale mais que um projeto grande pela metade.'},
        {'q': 'O que vem antes da arte e do som?', 'ops': ['A entrega', 'Um protótipo com formas simples e uma fase jogável', 'O menu', 'Nada'], 'ok': 1,
         'exp': 'Primeiro garanta que o ciclo funciona e é divertido.'},
        {'q': 'Quando fazer o teste com colegas?', 'ops': ['Depois de entregar', 'Antes da entrega, para dar tempo de ajustar', 'Nunca', 'No primeiro dia'], 'ok': 1,
         'exp': 'O teste só ajuda se ainda houver tempo de mudar o jogo.'},
        {'q': 'Qual critério pesa mais na ficha?', 'ops': ['Código organizado', 'O ciclo principal divertido e claro', 'O nome do jogo', 'O tamanho do mapa'], 'ok': 1,
         'exp': 'Um jogo é, antes de tudo, a ação que o jogador repete e gosta de repetir.'},
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
