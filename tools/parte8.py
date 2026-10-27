# Partes 8 e 9 da Oficina Flutter 2: mais sistemas de jogo (diálogos, inventário, conquistas, bando,
# conta do jogador, tradução) e desafios abertos com o projeto final e a sala de jogos da turma.
import pathlib
import solucoes

PASTA = pathlib.Path(__file__).resolve().parent / 'parte8'


def ler(nome):
    c = (PASTA / (nome + '.dart')).read_text(encoding='utf-8')
    assert "'''" not in c
    return c


def codigo(nome):
    return '\n' + ler(nome)


SETUP_HIVE = 'No terminal do projeto:\n  flutter pub add hive_flutter\n\nNo simulador as caixas do Hive ficam guardadas neste navegador (↺ Reiniciar apaga).'


def desafio(aula, t, text, tryit, nome, ex, lim=None, setup=None):
    ini, sol = ler('desafios/' + nome + '_ini'), ler('desafios/' + nome)
    aula(t, text, tryit, '\n' + ini, ex, lim=lim, setup=setup)
    for i in range(len(ex)):
        solucoes.MANUAL[(t, i)] = [(ini.strip('\n'), sol.strip('\n'))]


def adicionar(aula, PARTS, SETUP_FLAME):
    aula(
        'Diálogos e escolhas',
        'Personagens que conversam dão vida ao jogo. O jeito mais simples de montar uma conversa com escolhas é guardar o '
        'roteiro como dados: um Map em que cada fala tem um nome, quem fala, o texto e uma lista de escolhas, e cada escolha '
        'aponta para o nome da próxima fala. Assim o roteiro inteiro fica num lugar só, e acrescentar um caminho novo é '
        'acrescentar uma linha, sem mexer no código que mostra a conversa. As escolhas também mudam variáveis do jogo '
        '(amizade e ossos), que podem abrir ou fechar caminhos mais tarde. O texto aparece letra por letra com um '
        'Timer.periodic (o efeito de máquina de escrever), e tocar no balão mostra tudo de uma vez, porque quem lê rápido '
        'não quer esperar. As escolhas só aparecem quando a fala termina.',
        'Em ▶ Testar, converse com o Mingau por caminhos diferentes. Depois deixe o texto mais rápido, crie uma escolha nova '
        'e aumente a recompensa do segredo.',
        codigo('dialogos'),
        [
            ['Escrever mais rápido', 'Troque final int msPorLetra = 35 por 15.', r'msPorLetra\s*=\s*(?!35\b)\d+'],
            ['Uma escolha nova', "Na fala 'inicio', acrescente Escolha('Oferecer um osso', 'segredo', amizade: 2), depois das outras duas escolhas.", r"Escolha\('(?!Desculpa, só|O muro é|Quero!|Prefiro|Late bem|Pede desculpas|Combinado|Recomeçar)[^']+'"],
            ['Segredo valioso', "Na escolha 'Combinado, amigo!', troque ossos: 1 por ossos: 3.", r"'Combinado, amigo!',\s*'fim',\s*amizade:\s*1,\s*ossos:\s*(?!1\b)\d+"],
        ],
    )
    PARTS.append(['Diálogos e escolhas', 'Parte 8 · Mais sistemas de jogo'])

    aula(
        'Inventário e itens salvos em JSON',
        'Uma mochila separa duas ideias: o tipo do item (o que ele é: nome, ícone, quanto empilha, o efeito), que fica num '
        'catálogo fixo, e a pilha (qual item e quantos), que muda durante o jogo. Guardar um item primeiro procura uma pilha '
        'do mesmo tipo que ainda caiba; se não houver, ocupa uma casa nova, se sobrar espaço. Usar um item aplica o efeito e '
        'diminui a pilha; a coleira não some, ela é equipada. Para salvar uma lista de objetos, cada objeto vira um Map com '
        'toJson, a lista vira texto com jsonEncode e o texto vai para o Hive. Para carregar, o caminho é o contrário: '
        'jsonDecode e Pilha.fromJson. Esse mesmo formato JSON serve para salvar em arquivo, mandar para o Supabase ou '
        'exportar o progresso.',
        'Em ▶ Testar, explore até encher a mochila, use os itens e equipe a coleira. Reinicie e veja que tudo continua lá. '
        'Depois aumente a mochila, deixe empilhar mais ossos e crie um item novo.',
        codigo('inventario'),
        [
            ['Mochila maior', 'Troque final int capacidade = 8 por 12.', r'capacidade\s*=\s*(?!8\b)\d+'],
            ['Pilha de ossos', "No catálogo, troque TipoItem('osso', 'Osso', '🦴', 10, por TipoItem('osso', 'Osso', '🦴', 20,.", r"TipoItem\('osso',\s*'Osso',\s*'🦴',\s*(?!10\b)\d+"],
            ['Item novo', "No catálogo, acrescente 'petisco': TipoItem('petisco', 'Petisco', '🍖', 5, 'Recupera 2 vidas'), no fim.", r"'(?!osso'|bola'|coleira'|mapa')\w+'\s*:\s*TipoItem\("],
        ],
        setup=SETUP_HIVE,
    )

    aula(
        'Conquistas',
        'Conquistas são metas extras que recompensam jeitos diferentes de jogar: pegar muitos ossos, pular muito, insistir '
        'depois de cair, terminar sem dano. Cada Conquista guarda o id, o título, a descrição, o ícone e uma função que '
        'olha os números do jogo e diz se ela foi alcançada. Todo evento do jogo passa por um só lugar (o método evento), '
        'que soma o contador e confere as conquistas que ainda não foram ganhas. Quando uma é alcançada, fica salva no Hive '
        'e aparece um aviso que some sozinho depois de alguns segundos. É a mesma ideia do registro de eventos da aula de '
        'arquitetura: o jogo só avisa o que aconteceu, e o sistema de conquistas decide o que fazer com isso.',
        'Em ▶ Testar, pegue ossos, pule e caia para ganhar as conquistas. Depois deixe o aviso mais tempo na tela, faça o '
        'colecionador pedir mais ossos e crie uma conquista sua.',
        codigo('conquistas'),
        [
            ['Aviso mais longo', 'Troque final int segundosAviso = 3 por 5.', r'segundosAviso\s*=\s*(?!3\b)\d+'],
            ['Colecionador de verdade', "Na conquista 'colecionador', troque >= 20 por >= 50 e a descrição 'Pegue 20 ossos' por 'Pegue 50 ossos'.", r"\(n\['ossos'\]\s*\?\?\s*0\)\s*>=\s*50"],
            ['Conquista nova', "Acrescente na lista: Conquista('atleta', 'Atleta', 'Pule 30 vezes', '🏅', (n) => (n['pulos'] ?? 0) >= 30),", r"Conquista\(\s*'(?!primeiro'|colecionador'|saltador'|teimoso'|perfeito')\w+'"],
        ],
        setup=SETUP_HIVE,
    )

    aula(
        'Bando: comportamento de grupo',
        'Um bando de pombos parece complicado, mas cada pombo segue só três regras olhando os vizinhos próximos: separação '
        '(não chegar perto demais), alinhamento (voar para o mesmo lado que os vizinhos) e coesão (ir para o meio do grupo). '
        'Cada regra vira um vetor de força; somados com pesos, mudam a velocidade, que tem um limite máximo e um mínimo (o '
        'pombo nunca para no ar). É o algoritmo boids, criado em 1986 e usado em filmes e jogos para cardumes, rebanhos e '
        'multidões. Uma quarta regra deixa tudo mais vivo: fugir do caramelo quando ele chega perto. Os mesmos vetores da '
        'Parte 2 (subtrair, normalizar, limitar) fazem todo o trabalho.',
        'Em ▶ Testar, arraste o dedo para assustar o bando e mexa nos três pesos. Depois aumente a visão, o número de pombos '
        'e comece com mais separação.',
        codigo('bando'),
        [
            ['Visão maior', 'Troque final double raioVisao = 70 por 100.', r'raioVisao\s*=\s*(?!70\b)\d+'],
            ['Bando grande', 'Troque final int quantos = 24 por 36.', r'quantos\s*=\s*(?!24\b)\d+'],
            ['Mais espaço', 'Troque double separacao = 1.5 por 3.0.', r'double\s+separacao\s*=\s*(?!1\.5\b)[\d.]+'],
        ],
        lim='No simulador cada pombo confere todos os outros a cada quadro; com muitos pombos o desenho fica lento. No celular, o Dart compilado aguenta centenas.',
    )

    aula(
        'Conta do jogador e progresso na nuvem',
        'Com uma conta, o progresso segue o jogador para outro celular. O Supabase Auth cria contas com e-mail e senha: '
        'auth.signUp cria, auth.signInWithPassword entra, auth.signOut sai, e auth.currentUser diz quem está jogando (ou '
        'null). Erros como senha errada chegam como AuthException, com a mensagem em e.message. O progresso fica numa '
        'tabela com uma linha por jogador, marcada com o user_id: carregar é select().eq(\'user_id\', id).maybeSingle() (que '
        'devolve null se ainda não houver linha), e salvar é upsert com onConflict: \'user_id\'. No Supabase de verdade, '
        'as regras de segurança (RLS) garantem que cada jogador só lê e escreve a própria linha. Antes de chamar o '
        'servidor, o app confere o tamanho da senha: validar no aparelho evita espera e mensagens confusas.',
        'Em ▶ Testar, crie a conta, pegue ossos, salve, saia e entre de novo para ver o progresso voltar. Depois exija uma '
        'senha maior, dê 2 ossos por toque e troque o e-mail que já vem escrito.',
        codigo('conta'),
        [
            ['Senha maior', 'Troque final int senhaMinima = 6 por 8 (a senha de exemplo osso1234 tem 8).', r'senhaMinima\s*=\s*(?!6\b)\d+'],
            ['Dois ossos', 'No botão Pegar osso, troque setState(() => ossos++) por setState(() => ossos += 2).', r'ossos\s*\+=\s*2'],
            ['Outro e-mail', "Troque text: 'caramelo@escola.br' pelo seu e-mail de teste, como 'eu@escola.br'.", r"TextEditingController\(text:\s*'(?!caramelo@escola\.br')[^']+@[^']+'\)"],
        ],
        lim='No simulador o Supabase é de mentira: as contas e a tabela progresso ficam neste navegador e ↺ Reiniciar apaga. Não há e-mail de confirmação.',
        setup='No terminal do projeto:\n  flutter pub add supabase_flutter\n\nNo SQL Editor do Supabase:\n'
              '  create table progresso (user_id uuid primary key references auth.users, ossos int default 0, fase int default 1);\n'
              '  alter table progresso enable row level security;\n'
              '  create policy "dono" on progresso for all using (auth.uid() = user_id) with check (auth.uid() = user_id);\n'
              'Em Authentication > Providers, deixe Email ligado. Troque SEU-PROJETO e SUA-CHAVE-ANON pelos do seu projeto.',
    )

    aula(
        'Tradução: o jogo em vários idiomas',
        'Para o jogo falar outros idiomas, nenhum texto fica solto pelo código: todos ficam num mapa por idioma, com uma '
        'chave para cada frase, e a função t(\'chave\') busca a frase no idioma escolhido (ou em português, se faltar). '
        'Frases com partes que mudam usam marcadores, como \'Olá, {nome}!\', trocados na hora com replaceAll. O plural '
        'merece cuidado: "1 osso" e "2 ossos" são frases diferentes, e cada idioma tem as suas regras, por isso há uma '
        'chave para zero, uma para um e uma para muitos. Este jeito é ótimo para aprender e para jogos pequenos. Em apps '
        'maiores, o Flutter tem o gen-l10n: os textos ficam em arquivos .arb (um por idioma) e o Flutter gera o código, '
        'com plural e formatação de números e datas prontos.',
        'Em ▶ Testar, troque o idioma e jogue para ver o plural mudar. Depois acrescente o espanhol, um texto novo e a '
        'bandeira do novo idioma.',
        codigo('traducao'),
        [
            ['Espanhol', "No mapa textos, acrescente 'es': {'titulo': 'Caramelo y los Huesos', 'jogar': 'Jugar', 'ossos': '{n} huesos', 'osso1': '1 hueso', 'ossos0': 'Ningún hueso todavía', 'ola': '¡Hola, {nome}!', 'idioma': 'Idioma'},", r"'es'\s*:\s*\{"],
            ['Bandeira nova', "No mapa bandeiras, acrescente 'es': '🇪🇸 Español'.", r"'es'\s*:\s*'"],
            ['Frase nova', "Acrescente a chave 'recorde' em pt ('Recorde: {n}') e em en ('Best: {n}') e mostre Text(t('recorde', {'n': ossos})) embaixo dos ossos.", r"'recorde'\s*:[\s\S]*'recorde'\s*:[\s\S]*t\('recorde'"],
        ],
    )

    # ---------------------------------------------------------------- Parte 9: desafios abertos
    desafio(aula,
        'Desafio · Relógio de reação',
        'Desafio: o código já traz a tela, as cores e os textos, e marca com FAÇA o que falta. A pessoa toca para começar, espera '
        'um tempo sorteado e toca assim que a tela ficar verde; o jogo mostra o tempo em milissegundos e guarda o recorde. '
        'Planeje antes de programar: quais estados a tela tem (pronto, esperando, agora, resultado, cedo demais) e o que um '
        'toque faz em cada um. As etapas abaixo conferem as partes principais. Quer mais desafio? Apague tudo e faça do zero.',
        'Procure os comentários FAÇA no código e complete na ordem. Teste em ▶ Testar a cada parte que ficar pronta.',
        'reacao',
        [
            ['Tempo sorteado', 'Crie um Timer com uma Duration sorteada (Random().nextInt) para a tela ficar verde.', r'Timer\([\s\S]*nextInt|nextInt[\s\S]*Timer\('],
            ['Medir a reação', 'Guarde DateTime.now() quando ficar verde e calcule a diferença em inMilliseconds no toque.', r'difference\(\s*\w+!?\s*\)\.inMilliseconds|Stopwatch\(\)'],
            ['Recorde', 'Guarde o menor tempo numa variável recorde e mostre na tela.', r'recorde\s*=[^=]'],
        ],
    )
    PARTS.append(['Desafio · Relógio de reação', 'Parte 9 · Desafios e projeto final'])

    desafio(aula,
        'Desafio · Cobrinha do caramelo',
        'Desafio: a clássica cobrinha numa grade. A grade, os botões e o desenho já estão prontos; faltam o laço, o osso e a batida (os comentários FAÇA). O corpo é uma lista de casas; a cada passo, uma cabeça nova entra '
        'na frente e o rabo sai, a não ser que o caramelo tenha comido um osso (aí ele cresce). Pense em como guardar a '
        'direção e em como impedir que ele vire para trás de uma vez. Use as aulas de Timer.periodic, de CustomPainter e '
        'de colisão.',
        'Procure os comentários FAÇA e complete na ordem: o movimento, depois o osso e por fim a batida no corpo.',
        'cobra',
        [
            ['O laço', 'Crie um Timer.periodic(const Duration(milliseconds: 200), ...) que move o caramelo uma casa.', r'Timer\.periodic\(\s*(?:const\s+)?Duration\('],
            ['Corpo e comida', 'Guarde o corpo numa List<Offset> e sorteie a casa do osso com nextInt.', r'List<Offset>[\s\S]*nextInt'],
            ['Bater em si mesmo', 'Use corpo.contains(cabeca) para saber se o caramelo bateu no próprio corpo.', r'\.contains\(\s*\w+\s*\)'],
        ],
    )

    desafio(aula,
        'Desafio · Caramelo voador',
        'Desafio em Flame: um caramelo que cai com a gravidade e sobe a cada toque, passando entre canos. É o mesmo '
        'pulo da Parte 1 com o salto no lugar do chão, e os canos nascem com um TimerComponent como os obstáculos da Parte '
        '4. Decida o tamanho do vão, a velocidade dos canos e a força do impulso jogando várias vezes: esses números são o '
        'game feel do jogo. O caramelo animado, o toque e a criação dos canos já estão prontos; faltam a gravidade, o relógio dos canos e a batida (os comentários FAÇA).',
        'Procure os comentários FAÇA e complete na ordem. Teste o pulo antes de pôr os canos.',
        'voo',
        [
            ['Gravidade e impulso', 'No update do caramelo, some a gravidade à velocidade (velocidade += gravidade * dt); no toque, dê uma velocidade negativa.', r'velocidade\s*\+=\s*gravidade'],
            ['Canos', 'Use add(TimerComponent(period: 1.5, repeat: true, onTick: ...)) para criar os canos.', r'add\(\s*TimerComponent\('],
            ['Pontos e batida', 'Conte 1 ponto ao passar por um par de canos (pontos++) e termine ao encostar (overlaps).', r'overlaps\([\s\S]*pontos\+\+|pontos\+\+[\s\S]*overlaps\('],
        ],
        setup=SETUP_FLAME,
    )

    desafio(aula,
        'Desafio · Quebra-blocos',
        'Desafio: raquete, bola e uma parede de blocos. O desenho, os blocos, os quiques e as vidas já estão prontos; faltam a raquete, o Ticker e a quebra (os comentários FAÇA). A bola anda com velocidade em x e em y e inverte uma delas ao '
        'bater numa parede; na raquete, o ponto em que bate muda o ângulo, o que dá controle ao jogador. Os blocos são uma '
        'lista de Rect, e o que a bola tocar sai da lista. Use a aula de Ticker e delta time, a de arrastar e a de colisão '
        'AABB.',
        'Procure os comentários FAÇA e complete na ordem: a raquete, depois a bola andando e por fim os blocos quebrando.',
        'blocos',
        [
            ['Raquete', 'Mova a raquete com GestureDetector(onPanUpdate: ...).', r'onPanUpdate'],
            ['Bola', 'Anime a bola com createTicker e o dt de cada quadro.', r'createTicker'],
            ['Quebrar blocos', 'Tire da lista o bloco que a bola tocou (blocos.removeAt ou blocos.remove).', r'blocos\.removeAt\(|blocos\.remove\('],
        ],
    )

    desafio(aula,
        'Desafio · Jogo da memória',
        'Desafio: 12 cartas, 6 pares. As cartas e o toque já estão prontos; faltam embaralhar, comparar e o fim de jogo (os comentários FAÇA). O jogo precisa lembrar quais cartas estão viradas agora (no máximo duas) e '
        'quais pares já foram achados. Quando duas cartas diferentes ficam viradas, o jogo espera um segundo antes de '
        'desvirar, e nesse tempo não deixa virar outra. Use listas, Set e Timer, e pense em como embaralhar.',
        'Procure os comentários FAÇA e complete na ordem.',
        'memoria',
        [
            ['Embaralhar', 'Monte a lista com cada figura duas vezes e embaralhe com .shuffle().', r'\.\.shuffle\(\)|\.shuffle\(\)'],
            ['Duas viradas', 'Quando houver duas cartas viradas (length == 2), compare as figuras.', r'length\s*==\s*2'],
            ['Fim de jogo', 'Termine quando achadas.length == cartas.length e mostre as jogadas.', r'achadas\.length\s*==\s*cartas\.length'],
        ],
    )

    aula(
        'Sala de jogos (galeria)',
        'Esta é a sala de jogos da turma. Os jogos que chegam por link (botão 🔗 Compartilhar de quem fez) aparecem na 🕹 '
        'Galeria, e o botão ▶ Jogar abre o jogo aqui, nesta aula, sem apagar o código das outras aulas. Os jogos e as '
        'estrelas que você der ficam guardados neste navegador. Para mandar o seu jogo: abra a aula em que ele está, toque '
        'em 🔗 Compartilhar, dê um nome e envie o link (por e-mail, na plataforma da turma ou num grupo). Os sprites e mapas '
        'que você fez no 🎨 Desenhar e no 🗺 Mapa vão junto no link.',
        'Abra a 🕹 Galeria, cole o link de um colega e jogue. Depois troque o texto de boas-vindas da sala.',
        codigo('sala'),
        [
            ['Boas-vindas', "Troque 'Sala de jogos da turma' por um nome para a sala da sua turma.", r"Text\('(?!Sala de jogos da turma')[^']+',\s*style:\s*TextStyle\(fontSize:\s*26"],
        ],
        lim='A galeria não tem servidor: cada jogo chega por link e fica guardado só no navegador de quem abriu. Links muito longos (com muitas imagens) podem ser cortados por alguns aplicativos de mensagem.',
    )
    solucoes.MANUAL[('Inventário e itens salvos em JSON', 1)] = [("TipoItem('osso', 'Osso', '🦴', 10,", "TipoItem('osso', 'Osso', '🦴', 20,")]
    solucoes.MANUAL[('Diálogos e escolhas', 1)] = [("    Escolha('O muro é de todo mundo!', 'bravo', amizade: -1),\n",
                                                     "    Escolha('O muro é de todo mundo!', 'bravo', amizade: -1),\n    Escolha('Oferecer um osso', 'segredo', amizade: 2),\n")]
    solucoes.MANUAL[('Diálogos e escolhas', 2)] = [("Escolha('Combinado, amigo!', 'fim', amizade: 1, ossos: 1)", "Escolha('Combinado, amigo!', 'fim', amizade: 1, ossos: 3)")]
    solucoes.MANUAL[('Inventário e itens salvos em JSON', 2)] = [("  'mapa': TipoItem('mapa', 'Mapa do bairro', '🗺️', 1, 'Mostra os segredos'),\n",
                                                                   "  'mapa': TipoItem('mapa', 'Mapa do bairro', '🗺️', 1, 'Mostra os segredos'),\n  'petisco': TipoItem('petisco', 'Petisco', '🍖', 5, 'Recupera 2 vidas'),\n")]
    solucoes.MANUAL[('Conquistas', 1)] = [("Conquista('colecionador', 'Colecionador', 'Pegue 20 ossos', '🏆', (n) => (n['ossos'] ?? 0) >= 20)",
                                           "Conquista('colecionador', 'Colecionador', 'Pegue 50 ossos', '🏆', (n) => (n['ossos'] ?? 0) >= 50)")]
    solucoes.MANUAL[('Conquistas', 2)] = [("];\n\nclass Painel", "  Conquista('atleta', 'Atleta', 'Pule 30 vezes', '🏅', (n) => (n['pulos'] ?? 0) >= 30),\n];\n\nclass Painel")]
    solucoes.MANUAL[('Conta do jogador e progresso na nuvem', 1)] = [('setState(() => ossos++)', 'setState(() => ossos += 2)')]
    solucoes.MANUAL[('Conta do jogador e progresso na nuvem', 2)] = [("TextEditingController(text: 'caramelo@escola.br')", "TextEditingController(text: 'eu@escola.br')")]
    solucoes.MANUAL[('Tradução: o jogo em vários idiomas', 0)] = [("    'idioma': 'Language',\n  },\n};", "    'idioma': 'Language',\n  },\n  'es': {\n    'titulo': 'Caramelo y los Huesos',\n    'jogar': 'Jugar',\n    'ossos': '{n} huesos',\n    'osso1': '1 hueso',\n    'ossos0': 'Ningún hueso todavía',\n    'ola': '¡Hola, {nome}!',\n    'idioma': 'Idioma',\n  },\n};")]
    solucoes.MANUAL[('Tradução: o jogo em vários idiomas', 1)] = [("const bandeiras = {'pt': '🇧🇷 Português', 'en': '🇺🇸 English'};", "const bandeiras = {'pt': '🇧🇷 Português', 'en': '🇺🇸 English', 'es': '🇪🇸 Español'};")]
    solucoes.MANUAL[('Tradução: o jogo em vários idiomas', 2)] = [("    'idioma': 'Idioma',\n  },", "    'idioma': 'Idioma',\n    'recorde': 'Recorde: {n}',\n  },"),
                                                                ("    'idioma': 'Language',\n  },", "    'idioma': 'Language',\n    'recorde': 'Best: {n}',\n  },"),
                                                                ("            Text(contarOssos(ossos), style: const TextStyle(fontSize: 20)),\n", "            Text(contarOssos(ossos), style: const TextStyle(fontSize: 20)),\n            Text(t('recorde', {'n': ossos})),\n")]
    solucoes.MANUAL[('Sala de jogos (galeria)', 0)] = [("Text('Sala de jogos da turma',", "Text('Fliperama da turma A',")]
    PARTS.append(['Sala de jogos (galeria)', 'Sala de jogos'])
