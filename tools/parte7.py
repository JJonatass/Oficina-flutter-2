# Parte 7 da Oficina Flutter 2: do jogo de uma tela ao jogo completo (telas, fases, mapas, conteúdo gerado,
# inteligência de caminho, desempenho, multijogador) e o Projeto 6.
import pathlib

PASTA = pathlib.Path(__file__).resolve().parent / 'parte7'


def codigo(nome):
    c = (PASTA / (nome + '.dart')).read_text(encoding='utf-8')
    assert "'''" not in c
    return '\n' + c


SETUP_HIVE = '\n\nProgresso salvo: flutter pub add hive_flutter.'


def adicionar(aula, PARTS, SETUP_FLAME, SETUP_TILED):
    aula(
        'Navegação: menu, fases e pausa',
        'Um jogo de verdade tem várias telas: menu, escolha de fase, créditos e o jogo. As telas são widgets do Flutter, '
        'e o Navigator troca entre elas como numa pilha. Navigator.push(context, MaterialPageRoute(builder: ...)) põe uma '
        'tela por cima; Navigator.pop(context) tira a de cima e volta para a anterior; Navigator.pushReplacement troca a '
        'tela de cima por outra, sem empilhar (é assim que "Próxima fase" e "Tentar de novo" funcionam: a fase velha sai '
        'e a nova entra, e o pop continua voltando para a escolha de fases). Só a tela TelaJogo tem um GameWidget, e cada '
        'vez que ela é criada nasce um jogo novo (PegaOssos(fase)). A pausa e o fim são overlays do GameWidget: o jogo '
        'chama pauseEngine() e overlays.add(\'pausa\'), e o botão Continuar chama jogo.continuar, que tira o overlay e chama '
        'resumeEngine(). O Flame também tem um RouterComponent para trocar telas dentro do próprio jogo; aqui as telas '
        'ficam no Flutter, que já sabe fazer listas, botões e textos.',
        'Em ▶ Testar, vá do menu à escolha de fases, jogue, pause e use os botões das janelas. Acrescente uma quarta fase, '
        'deixe o tempo mais curto e troque o texto do botão de jogar.',
        codigo('navegacao'),
        [
            ['Quarta fase', 'Troque const int totalFases = 3 por 4: a lista ganha a Fase 4, com mais ossos e menos tempo.', r'totalFases\s*=\s*(?!3\b)\d+'],
            ['Menos tempo', 'No onLoad do PegaOssos, troque tempo = 12.0 - fase por tempo = 10.0 - fase.', r'tempo\s*=\s*(?!12\.0\b)[\d.]+\s*-\s*fase'],
            ['Outro texto', "No menu, troque child: const Text('Jogar') por child: const Text('Começar').", r"child:\s*const\s+Text\(\s*'(?!Jogar')[^']+'\s*\),\s*\),\s*const SizedBox\(height: 12\)"],
        ],
        lim='No simulador as telas do Navigator aparecem uma de cada vez, como no celular. O botão voltar do Android não existe aqui: use os botões de cada tela.',
        setup=SETUP_FLAME,
    )
    PARTS.append(['Navegação: menu, fases e pausa', 'Parte 7 · Jogo completo'])

    aula(
        'Plataforma: gravidade e colisão com o mapa',
        'No jogo de plataforma o caramelo cai, pousa no chão, bate a cabeça e para nas paredes. O mapa do Tiled traz a '
        'camada solidos com retângulos: chao bloqueia dos quatro lados e plataforma (as tábuas) só segura quem vem de '
        'cima. A física tem dois passos por quadro, um eixo de cada vez. Primeiro o x: anda, e se o corpo entrou num '
        'bloco, encosta na borda dele (left - 15 andando para a direita, right + 15 para a esquerda). Depois o y: cai, '
        'e se entrou num bloco descendo, os pés ficam no topo do bloco (noChao = true); subindo, a cabeça fica embaixo '
        'dele. Separar os eixos evita o caramelo "grudar" na parede ou atravessar o canto. A tábua usa a posição dos pés '
        'antes do passo: só segura se antes ele estava acima dela. O anchor bottomCenter deixa position nos pés, o que '
        'simplifica as contas. A câmera acompanha o caramelo, mas com clamp para não mostrar o que fica fora do mapa. '
        'Os botões da tela usam ButtonComponent, que avisa quando aperta e quando solta.',
        'Em ▶ Testar, ande com ◀ ▶ (ou as setas) e pule com ⤒ (ou espaço). Suba nas tábuas, pegue os ossos e chegue na '
        'porta. Depois mude o pulo, a gravidade e a velocidade e sinta a diferença.',
        codigo('plataforma'),
        [
            ['Pulo mais alto', 'Na classe Caramelo, troque double forcaPulo = 640 por 760.', r'forcaPulo\s*=\s*(?!640\b)\d+'],
            ['Gravidade de lua', 'Troque double gravidade = 1400 por 700: o pulo fica alto e lento.', r'gravidade\s*=\s*(?!1400\b)\d+'],
            ['Mais rápido', 'Troque double rapidez = 220 por 300.', r'rapidez\s*=\s*(?!220\b)\d+'],
        ],
        lim='No simulador o mapa fase1.tmx já existe. O caramelo volta ao início quando cai na água ou nos espinhos e quando chega na porta.',
        setup=SETUP_TILED,
    )

    aula(
        'Fases e estrelas: progresso com Hive',
        'Fases dão ao jogador um caminho: cada uma é um pouco mais difícil, e terminar uma abre a próxima. As fases ficam '
        'numa lista de objetos Fase (nome, quantos ossos, quanto tempo), e o jogo recebe o número da fase. O resultado '
        'vira estrelas pelo tempo que sobrou: mais da metade dá 3, mais de um quarto dá 2, só terminar dá 1. O progresso '
        'fica guardado com o Hive na caixa progresso, com uma chave por fase (fase0, fase1...). Só se grava se a nota '
        'nova for maior que a antiga, para o jogador não perder estrelas jogando pior. A fase n abre quando a fase n - 1 '
        'tem pelo menos uma estrela. A tela do mapa é um StatefulWidget e usa Navigator.push(...).then((_) => setState(() '
        '{})): quando a fase fecha e o jogador volta, ela redesenha com as estrelas novas.',
        'Em ▶ Testar, jogue o Quintal, veja as estrelas e a Praça abrir. Acrescente uma fase, deixe 3 estrelas mais '
        'difíceis e mude a regra que abre as fases.',
        codigo('fases'),
        [
            ['Mais uma fase', "Na lista fases, acrescente Fase('Parque', 13, 10), depois da Praia.", r"Fase\(\s*'(?!Quintal'|Praça'|Feira'|Praia')[^']+'\s*,\s*\d+"],
            ['3 estrelas difíceis', 'Em contarEstrelas, troque if (sobra > 0.5) return 3 por if (sobra > 0.6) return 3.', r'sobra\s*>\s*0\.(?!5\b)\d+\)\s*return\s*3'],
            ['Abrir com 2 estrelas', 'Troque estrelasDe(i - 1) > 0 por estrelasDe(i - 1) > 1: a próxima fase só abre com 2 estrelas.', r'estrelasDe\(i\s*-\s*1\)\s*>\s*(?!0\b)\d'],
        ],
        lim='No simulador a caixa do Hive fica guardada neste navegador. O botão da lixeira apaga o progresso, e ↺ Reiniciar também.',
        setup=SETUP_FLAME + SETUP_HIVE,
    )

    aula(
        'Geração procedural: semente, labirinto e cavernas',
        'Em vez de desenhar cada fase, o jogo pode criar a fase com uma receita: é a geração procedural. Toda receita usa '
        'sorteios, e o Random(semente) do dart:math sempre devolve a mesma sequência para a mesma semente. Por isso a '
        'semente 42 sempre gera o mesmo labirinto: dá para repetir a fase, compartilhar uma fase com um amigo ou ter um '
        '"desafio do dia" igual para todo mundo. O labirinto começa todo parede e cava caminhos com uma pilha: escolhe um '
        'vizinho ainda fechado (pulando de dois em dois), derruba a parede do meio e empilha; sem vizinhos, desempilha e '
        'volta. As cavernas fazem o contrário: sorteiam paredes com uma chance e depois suavizam várias vezes com a regra '
        'dos vizinhos (uma casa vira parede se tiver 5 ou mais paredes em volta, contando ela mesma). Poucas linhas de '
        'código geram mapas que parecem feitos à mão.',
        'Em ▶ Testar, troque de semente e de modo e compare. Mude a chance de parede e os passos de suavização das '
        'cavernas e deixe a semente inicial ser a sua.',
        codigo('procedural'),
        [
            ['Cavernas mais abertas', 'Troque double chanceParede = 0.45 por 0.40.', r'chanceParede\s*=\s*0\.(?!45\b)\d+'],
            ['Menos suavização', 'Troque int passosSuavizar = 4 por 1 e veja as cavernas com cara de ruído.', r'passosSuavizar\s*=\s*(?!4\b)\d+'],
            ['Sua semente', 'Troque int semente = 42 por outro número, como o dia do seu aniversário.', r'int\s+semente\s*=\s*(?!42\b)\d+'],
        ],
        lim='O Random do simulador também repete a sequência para a mesma semente, mas não é o mesmo algoritmo do Dart: no celular a semente 42 gera um labirinto diferente deste (e sempre o mesmo).',
    )

    aula(
        'Caminho até o alvo: BFS e A*',
        'O gato da aula de estados corre em linha reta e bate nas paredes. Para contornar o labirinto, ele precisa de uma '
        'busca de caminho. O mapa vira uma grade de casas, e cada casa livre tem até quatro vizinhos. A busca em largura '
        '(BFS) usa uma fila: tira a casa mais antiga, olha os vizinhos novos, anota de onde veio cada um (veioDe) e põe '
        'na fila. Ela explora em ondas e sempre acha o caminho mais curto. O A* (A estrela) usa a mesma fila, mas tira '
        'a casa com o menor custo até ali + estimativa até o alvo; a estimativa é a distância "de táxi" (quantos passos '
        'faltariam sem paredes). Assim ele explora bem menos casas e acha o mesmo caminho. Achado o alvo, o caminho é '
        'montado de trás para frente seguindo veioDe. Este gato refaz a busca a cada passo, então muda de rota quando o '
        'caramelo muda de lugar. A Celula tem operator == e hashCode para poder ser comparada e usada como chave.',
        'Em ▶ Testar, toque numa casa para mudar o caramelo de lugar e compare BFS e A* no número de casas exploradas. '
        'Ligue Pôr parede e feche passagens. Depois deixe o gato mais rápido e troque a estimativa.',
        codigo('caminho'),
        [
            ['Gato mais rápido', 'Troque final int msPorPasso = 250 por 120.', r'msPorPasso\s*=\s*(?!250\b)\d+'],
            ['A* desde o início', 'Troque bool aEstrela = false por true.', r'bool\s+aEstrela\s*=\s*true'],
            ['Estimativa exagerada', 'Na função estimativa, multiplique tudo por 3: => 3 * ((a.x - b.x).abs() + (a.y - b.y).abs()). Ele explora menos, mas nem sempre acha o menor caminho.', r'=>\s*3\s*\*'],
        ],
    )

    aula(
        'Desempenho: medir FPS e reaproveitar objetos',
        'Um jogo precisa desenhar 60 quadros por segundo (FPS). Quando cada quadro demora mais que 16 milissegundos, a '
        'animação engasga. Para saber, meça: a média dos últimos dt dá o FPS (1 / média). O Flame também tem o '
        'FpsTextComponent pronto. A chuva de ossos cria muitos componentes. Criar e jogar fora objetos o tempo todo dá '
        'trabalho ao coletor de lixo do Dart, que de vez em quando para tudo para limpar a memória. O pool (piscina de '
        'objetos) evita isso: o osso que caiu sai do jogo (removeFromParent) mas fica guardado numa lista; quando precisa '
        'de um osso novo, o jogo pega um guardado e só muda posição e velocidade. Com o pool ligado, os "criados" param '
        'de subir e os "reaproveitados" sobem. Outras dicas: carregar a imagem uma vez só (aqui, ossoSprite no onLoad), '
        'não criar Paint e TextPainter dentro do render quando dá para guardar, e tirar do jogo o que saiu da tela.',
        'Em ▶ Testar, observe o painel, aumente a chuva com + 30 e desligue o pool para ver os criados dispararem. Depois '
        'comece com mais ossos, use uma média mais longa e deixe os ossos maiores.',
        codigo('desempenho'),
        [
            ['Chuva forte', 'Troque int porSegundo = 60 por 150.', r'porSegundo\s*=\s*(?!60\b)\d+;'],
            ['Média mais longa', 'Troque if (tempos.length > 30) por if (tempos.length > 60): o FPS fica mais estável.', r'tempos\.length\s*>\s*(?!30\b)\d+'],
            ['Ossos maiores', 'Na classe Osso, troque size: Vector2.all(28) por size: Vector2.all(40).', r'size:\s*Vector2\.all\(\s*(?!28\b)\d+\s*\),\s*anchor'],
        ],
        lim='No simulador o FPS depende do navegador e do computador, e o interpretador é bem mais lento que o Dart compilado: no celular a mesma chuva aguenta muito mais ossos.',
        setup=SETUP_FLAME,
    )

    aula(
        'Multijogador em tempo real com Supabase',
        'No multijogador, cada aparelho conta para o servidor onde está o seu jogador e recebe a posição dos outros. '
        'Com o Supabase, a tabela jogadores tem uma linha por jogador (id, cor, x, y e visto, a hora do último aviso). '
        'Cada aparelho faz upsert da própria linha ao andar (cria se não existe, atualiza se existe) e ouve a tabela '
        'inteira com stream(primaryKey: [\'id\']): a cada mudança, o StreamBuilder redesenha todo mundo. Três cuidados '
        'de jogo online aparecem aqui. Limite de envios: no máximo 10 por segundo, para não sobrecarregar o servidor; ao '
        'soltar o dedo, a posição final vai de qualquer jeito. Sinal de vida: a cada 5 segundos o aparelho avisa que '
        'continua na sala, e quem ficou mais de 15 segundos sem avisar some da tela. Previsão local: o seu próprio '
        'jogador é desenhado na hora com a posição local, sem esperar a volta do servidor. Para jogos rápidos, o Supabase '
        'também tem canais de broadcast (supabase.channel), que mandam mensagens sem gravar no banco.',
        'Em ▶ Testar, ligue o bot e arraste o seu jogador. Abra esta mesma aula em outra aba do navegador e veja os dois '
        'jogadores se mexendo nas duas. Depois mude o limite de envios e o tempo de ausência.',
        codigo('online'),
        [
            ['Ausência curta', 'Troque final int segundosAusente = 15 por 8.', r'segundosAusente\s*=\s*(?!15\b)\d+'],
            ['Menos envios', 'Em enviar, troque inMilliseconds < 100 por inMilliseconds < 250: no máximo 4 envios por segundo.', r'inMilliseconds\s*<\s*(?!100\b)\d+'],
            ['Bot mais rápido', 'Em ligarBot, troque anguloBot += 0.15 por anguloBot += 0.3.', r'anguloBot\s*\+=\s*0\.(?!15\b)\d+'],
        ],
        lim='No simulador o Supabase é de mentira e fica guardado neste navegador. Outra aba aberta na mesma aula vê as mudanças na hora, como dois celulares. Abrir a aula de novo limpa a tabela.',
        setup='No terminal do projeto:\n  flutter pub add supabase_flutter\n\nNo painel do Supabase, rode no SQL Editor:\n'
              '  create table jogadores (id text primary key, cor int, x float8, y float8, visto int8);\n'
              '  alter table jogadores enable row level security;\n'
              '  create policy "todos" on jogadores for all using (true) with check (true);\n'
              'e ligue o Realtime da tabela (Database > Replication). Troque SEU-PROJETO e SUA-CHAVE-ANON pelos do seu projeto.',
    )

    aula(
        'Projeto · Trilha do Caramelo',
        'O último projeto junta a Parte 7 num jogo de plataforma completo. O menu e a escolha de fases são telas do '
        'Flutter; cada fase é um mapa do Tiled (fase1, fase2 e fase3.tmx), com chão, tábuas, água, espinhos, ossos, um '
        'osso dourado, gatos e a porta de chegada. O caramelo tem a física da aula de plataforma, três vidas e fica '
        'piscando e invencível por um instante depois de levar dano. Os gatos patrulham: andam até achar uma parede ou a '
        'beira do chão e viram. Cair em cima de um gato derruba ele (e o caramelo quica); encostar de lado machuca. Cada '
        'fase vale até 3 estrelas: chegar, pegar todos os ossos e chegar sem levar dano. As estrelas ficam no Hive, e a '
        'fase seguinte abre com pelo menos uma. A pausa e a janela de fim são overlays, e Próxima fase e Jogar de novo '
        'usam pushReplacement.',
        'Em ▶ Testar, jogue as três fases. Depois deixe o jogo com 5 vidas, gatos mais rápidos, um pulo mais forte e uma '
        'fase nova na lista.',
        codigo('projeto6'),
        [
            ['Cinco vidas', 'No Trilha, troque int vidas = 3 por 5, e no hud troque (3 - vidas) por (5 - vidas).', r'int\s+vidas\s*=\s*5[\s\S]*\(\s*5\s*-\s*vidas\s*\)'],
            ['Gatos ligeiros', 'Na classe Gato, troque double velocidade = 60 por 110.', r'double\s+velocidade\s*=\s*(?!60\b)\d+'],
            ['Pulo forte', 'No Caramelo, troque double forcaPulo = 700 por 820.', r'forcaPulo\s*=\s*(?!700\b)\d+'],
            ['Fase bônus', "Na lista fases, acrescente InfoFase('Bônus', 'fase1.tmx'), no fim: uma quarta fase que repete o mapa do Quintal.", r"InfoFase\(\s*'(?!Quintal'|Praça'|Feira')[^']+'\s*,\s*'\w+\.tmx'\s*\)"],
        ],
        lim='No simulador os mapas fase1, fase2 e fase3.tmx já existem, a música é sintetizada e só toca depois do primeiro toque, e as estrelas ficam guardadas neste navegador (↺ Reiniciar apaga).',
        setup=SETUP_TILED + SETUP_HIVE,
    )
    PARTS.append(['Projeto · Trilha do Caramelo', 'Projeto 6 · Trilha do Caramelo'])
