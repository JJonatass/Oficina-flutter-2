"""Gabarito automático dos exercícios: tenta montar a troca 'antes → depois' a partir do texto
"troque A por B" e só aceita quando a troca faz a regex da etapa passar (e o código inicial não passava)."""
import re

TOK = re.compile(r"(-?[\d.]+|[\w.]+\(?[^()]*\)?|\S+)$")


def _limpa(x):
    x = x.strip().strip('`').strip()
    x = re.sub(r"^(?:o|a|os|as|um|uma)\s+", '', x)
    return x


def candidatos(d):
    for m in re.finditer(r"[Tt]roque (?:o |a |os |as |o texto |a cor |a origem )?(.+?) por (.+?)(?=(?:[.;:]\s|[.;:]?$| e (?:aumente|confira|um valor|mostre|suba|o mesmo)| \(|, | nos | no | na ))", d):
        a, b = _limpa(m.group(1)), _limpa(m.group(2))
        b = re.sub(r"^(?:um|uma) [\wçãé ]+?, como ", '', b)
        b = re.sub(r"^como ", '', b)
        yield a, b
    for m in re.finditer(r"(?:Mude a constante|use|Use|escreva|acrescente|Acrescente):?\s+([\w .=<>*/+\-'()]+?)(?=[.;]\s|[.;]?$)", d):
        yield None, m.group(1).strip()


def gabarito(code, desc, rx):
    try:
        R = re.compile(rx)
    except re.error:
        return None
    if R.search(code):
        return None
    for a, b in candidatos(desc):
        tent = []
        if a and a in code:
            tent.append((a, b))
            ta = TOK.search(a)
            if ta and ' ' not in b and len(b) < len(a):
                tent.append((a, a[:ta.start()] + b))
            # "X = 1 por Y = 2" com só o número em b
            nm = re.match(r"^(.*?)(-?[\d.]+)$", a)
            if nm and re.match(r"^-?[\d.]+$", b):
                tent.append((a, nm.group(1) + b))
            if re.match(r"^\*\s*[\d.]+$", b):
                tent.append((a, re.sub(r"\*\s*[\d.]+$", b, a)))
        elif a:
            # a é só parte (ex.: 'milliseconds: 16'): procura com espaços flexíveis
            pat = re.escape(a).replace(r'\ ', r'\s*')
            mm = re.search(pat, code)
            if mm:
                tent.append((mm.group(0), b))
        else:
            # "Mude a constante: const double chao = 400" → acha o lado esquerdo no código
            lm = re.match(r"^(.*?=)\s*(.+)$", b)
            if lm:
                left = re.escape(lm.group(1).strip()).replace(r'\ ', r'\s*')
                mm = re.search(left + r"\s*[^;,\n]+", code)
                if mm:
                    tent.append((mm.group(0), lm.group(1).strip() + ' ' + lm.group(2).strip()))
        for x, y in tent:
            if re.fullmatch(r"[a-zà-ú ]+", y) or y.count('(') != y.count(')') or x.count('(') != x.count(')'):
                continue
            if x and x in code and x != y:
                novo = code.replace(x, y, 1)
                if R.search(novo):
                    return [x, y]
    return None


# Respostas escritas à mão para as etapas que o texto não descreve como uma troca simples.
# Cada resposta é uma lista de trocas (antes, depois) aplicadas em ordem no código inicial da aula.
MANUAL = {
    ('O laço do jogo com Timer.periodic', 1): [('Timer.periodic(const Duration(milliseconds: 16)', 'Timer.periodic(const Duration(milliseconds: 100)')],
    ('O laço do jogo com Timer.periodic', 2): [('top: 200,', 'top: 400,')],
    ('O laço do jogo com Timer.periodic', 3): [('        x += 3;', '        x -= 3;'), ('        if (x > 360) {\n          x = -40;', '        if (x < -40) {\n          x = 360;')],
    ('Ticker e delta time', 1): [('      if (x > 360) {\n        x = -40;\n      }', '      if (x > 320 || x < 0) {\n        velocidade = -velocidade;\n      }')],
    ('Ticker e delta time', 2): [('  double velocidade = 120;\n', '  double velocidade = 120;\n  double dt = 0;\n'),
                                 ('      x += velocidade * dt;\n', '      x += velocidade * dt;\n      this.dt = dt;\n'),
                                 ("px/s'", "px/s  dt ${dt.toStringAsFixed(3)} s'")],
    ('Desenhando o jogo com CustomPainter', 1): [('    canvas.drawCircle(const Offset(290, 80), 36, Paint()..color = Colors.yellow);\n',
                                                  '    canvas.drawCircle(const Offset(290, 80), 36, Paint()..color = Colors.yellow);\n'
                                                  '    canvas.drawCircle(const Offset(80, 90), 22, Paint()..color = Colors.white);\n'
                                                  '    canvas.drawCircle(const Offset(105, 80), 28, Paint()..color = Colors.white);\n'
                                                  '    canvas.drawCircle(const Offset(132, 90), 22, Paint()..color = Colors.white);\n')],
    ('Toque: o personagem vai até o dedo', 2): [('  Cena(this.x, this.alvo);\n', '  Cena(this.x, this.alvo);\n\n  bool get andando => (x - alvo).abs() > 1;\n'),
                                                ('desenharCaramelo(canvas, corpo, const Color(0xFFD68C3E), 1);', 'desenharCaramelo(canvas, corpo, andando ? Colors.amber : const Color(0xFFD68C3E), 1);')],
    ('Gravidade e pulo', 2): [('  int pulos = 0;\n', '  int pulos = 0;\n  int saltosNoAr = 0;\n'),
                              ('        vy = 0;\n', '        vy = 0;\n        saltosNoAr = 0;\n'),
                              ('    if (noChao) {\n      vy = impulso;', '    if (noChao || saltosNoAr < 1) {\n      if (!noChao) saltosNoAr++;\n      vy = impulso;')],
    ('Muitos objetos: lista, sorteio e remoção', 2): [
        ('  final double altura;\n  Caixa(this.x, this.altura);\n}', '  final double altura;\n  final double largura;\n  Caixa(this.x, this.altura, this.largura);\n}'),
        ('canvas.drawRect(Rect.fromLTWH(c.x, chao - c.altura, 30, c.altura), tinta);', 'canvas.drawRect(Rect.fromLTWH(c.x, chao - c.altura, c.largura, c.altura), tinta);'),
        ('caixas.add(Caixa(largura, 30 + sorteio.nextDouble() * 60));', 'caixas.add(Caixa(largura, 30 + sorteio.nextDouble() * 60, 20 + sorteio.nextDouble() * 40));')],
    ('Colisão com retângulos (AABB)', 0): [('final jogador = Rect.fromLTWH(jogadorX, y, 40, 48).deflate(4);', 'final jogador = Rect.fromLTWH(jogadorX, y, 40, 48);')],
    ('Colisão com retângulos (AABB)', 2): [
        ('  final double altura;\n  Caixa(this.x, this.altura);\n', '  final double altura;\n  bool contada = false;\n  Caixa(this.x, this.altura);\n'),
        ('  int batidas = 0;\n', '  int batidas = 0;\n  int pontos = 0;\n'),
        ('      c.x -= 200 * dt;\n', '      c.x -= 200 * dt;\n      if (!c.contada && c.x + 30 < jogadorX) {\n        c.contada = true;\n        pontos++;\n      }\n'),
        ("Text('Batidas: $batidas')", "Text('Batidas: $batidas · Pontos: $pontos')")],
    ('Estados do jogo: pronto, jogando e fim', 0): [("'Fim de jogo!\\nToque para voltar'", "'Que pena, bateu!\\nToque para voltar'")],
    ('Estados do jogo: pronto, jogando e fim', 1): [("const Center(child: Text('Fim de jogo!\\nToque para voltar', textAlign: TextAlign.center, style: grande)),",
                                                    "Center(child: Text('Fim de jogo!\\nVocê fez $pontos pontos', textAlign: TextAlign.center, style: grande)),")],
    ('Estados do jogo: pronto, jogando e fim', 2): [('      c.x -= 200 * dt;', '      c.x -= (200 + pontos * 15) * dt;')],
    ('Projeto · Pula-Caixa', 0): [('Paint()..color = const Color(0xFF8FD3FE)', 'Paint()..color = const Color(0xFF14213D)')],
    ('Projeto · Pula-Caixa', 2): [
        ('class Cena extends CustomPainter {\n  final double y;\n  final List<Caixa> caixas;\n  final double deslocamento;\n  final bool perdeu;\n  Cena(this.y, this.caixas, this.deslocamento, this.perdeu);\n',
         'class Osso {\n  double x;\n  final double y;\n  Osso(this.x, this.y);\n\n  Rect get area => Rect.fromCircle(center: Offset(x, y), radius: 12);\n}\n\n'
         'class Cena extends CustomPainter {\n  final double y;\n  final List<Caixa> caixas;\n  final double deslocamento;\n  final bool perdeu;\n  final List<Osso> ossos;\n  Cena(this.y, this.caixas, this.deslocamento, this.perdeu, this.ossos);\n'),
        ('      canvas.drawRect(c.area.deflate(6), Paint()..color = Colors.brown.shade300);\n    }\n',
         '      canvas.drawRect(c.area.deflate(6), Paint()..color = Colors.brown.shade300);\n    }\n    for (final o in ossos) {\n      canvas.drawCircle(Offset(o.x, o.y), 12, Paint()..color = Colors.amber);\n    }\n'),
        ('  List<Caixa> caixas = [];\n  double tempoProxima = 1;\n  double tempoDePartida = 0;', '  List<Caixa> caixas = [];\n  List<Osso> ossos = [];\n  double tempoProxima = 1;\n  double tempoDePartida = 0;'),
        ('      tempoProxima = 0.9 + sorteio.nextDouble() * 1.1;\n', '      tempoProxima = 0.9 + sorteio.nextDouble() * 1.1;\n      if (sorteio.nextDouble() < 0.4) ossos.add(Osso(largura + 40, chao - 110));\n'),
        ('    caixas.removeWhere((c) => c.x < -60);\n', '    caixas.removeWhere((c) => c.x < -60);\n    for (final o in ossos) {\n      o.x -= velocidade * dt;\n    }\n    ossos.removeWhere((o) => o.x < -20);\n'),
        ('    if (caixas.any((c) => c.area.overlaps(jogador))) {\n',
         '    final pegos = ossos.where((o) => o.area.overlaps(jogador)).toList();\n    if (pegos.isNotEmpty) {\n      deslocamento += 10 * 20 * pegos.length;\n      ossos.removeWhere((o) => pegos.contains(o));\n    }\n    if (caixas.any((c) => c.area.overlaps(jogador))) {\n'),
        ('        caixas.clear();\n', '        caixas.clear();\n        ossos.clear();\n'),
        ('Cena(y, caixas, deslocamento, estado == Estado.fim)', 'Cena(y, caixas, deslocamento, estado == Estado.fim, ossos)')],
    ('Arrastar: a raquete segue o dedo', 1): [('  Offset velocidade = const Offset(160, 240);', '  Offset velocidade = const Offset(220, 320);'), ('      velocidade = const Offset(160, 240);', '      velocidade = const Offset(220, 320);')],
    ('Arrastar: a raquete segue o dedo', 2): [('      rebatidas++;\n', '      rebatidas++;\n      velocidade = velocidade * 1.05;\n')],
    ('Arremessar: a velocidade do arrasto', 0): [('pow(0.4, dt)', 'pow(0.9, dt)')],
    ('Arremessar: a velocidade do arrasto', 2): [
        ('  bool preso = false;\n', '  bool preso = false;\n  int batidas = 0;\n'),
        ('        velocidade = Offset(-velocidade.dx, velocidade.dy);\n', '        velocidade = Offset(-velocidade.dx, velocidade.dy);\n        batidas++;\n'),
        ('        velocidade = Offset(velocidade.dx, -velocidade.dy);\n', '        velocidade = Offset(velocidade.dx, -velocidade.dy);\n        batidas++;\n'),
        ("Text('${velocidade.distance.toStringAsFixed(0)} px/s')", "Text('${velocidade.distance.toStringAsFixed(0)} px/s · $batidas batidas')")],
    ('Teclado: setas e espaço', 0): [
        ('if (teclado.isLogicalKeyPressed(LogicalKeyboardKey.arrowLeft)) x -= velocidade * dt;', 'if (teclado.isLogicalKeyPressed(LogicalKeyboardKey.arrowLeft) || teclado.isLogicalKeyPressed(LogicalKeyboardKey.keyA)) x -= velocidade * dt;'),
        ('if (teclado.isLogicalKeyPressed(LogicalKeyboardKey.arrowRight)) x += velocidade * dt;', 'if (teclado.isLogicalKeyPressed(LogicalKeyboardKey.arrowRight) || teclado.isLogicalKeyPressed(LogicalKeyboardKey.keyD)) x += velocidade * dt;')],
    ('Teclado: setas e espaço', 1): [('if (event.logicalKey == LogicalKeyboardKey.space && y >= chao - 48) {', 'if ((event.logicalKey == LogicalKeyboardKey.space || event.logicalKey == LogicalKeyboardKey.arrowUp) && y >= chao - 48) {')],
    ('Teclado: setas e espaço', 2): [('    setState(() {\n      if (teclado.isLogicalKeyPressed(LogicalKeyboardKey.arrowLeft)) x -= velocidade * dt;\n      if (teclado.isLogicalKeyPressed(LogicalKeyboardKey.arrowRight)) x += velocidade * dt;',
                                     '    final rapido = teclado.isShiftPressed ? velocidade * 2 : velocidade;\n    setState(() {\n      if (teclado.isLogicalKeyPressed(LogicalKeyboardKey.arrowLeft)) x -= rapido * dt;\n      if (teclado.isLogicalKeyPressed(LogicalKeyboardKey.arrowRight)) x += rapido * dt;')],
    ('Sprites: imagens no Canvas', 0): [('canvas.drawImageRect(s.heroi, bloco,', 'canvas.drawImageRect(s.heroi, const Rect.fromLTWH(32, 0, 16, 16),')],
    ('Sprites: imagens no Canvas', 1): [('canvas.drawImageRect(s.caixa, bloco, const Rect.fromLTWH(240, chao - 48, 48, 48), tinta);', 'canvas.drawImageRect(s.caixa, bloco, const Rect.fromLTWH(240, chao - 64, 64, 64), tinta);')],
    ('Sprites: imagens no Canvas', 2): [
        ('  final ui.Image osso;\n  Sprites(this.heroi, this.grama, this.caixa, this.osso);', '  final ui.Image osso;\n  final ui.Image maca;\n  Sprites(this.heroi, this.grama, this.caixa, this.osso, this.maca);'),
        ("    final osso = await carregarImagem('assets/sprites/osso.png');\n    setState(() => sprites = Sprites(heroi, grama, caixa, osso));",
         "    final osso = await carregarImagem('assets/sprites/osso.png');\n    final maca = await carregarImagem('assets/sprites/maca.png');\n    setState(() => sprites = Sprites(heroi, grama, caixa, osso, maca));"),
        ('    canvas.drawImageRect(s.osso, bloco, const Rect.fromLTWH(252, chao - 96, 24, 24), tinta);\n',
         '    canvas.drawImageRect(s.osso, bloco, const Rect.fromLTWH(252, chao - 96, 24, 24), tinta);\n    canvas.drawImageRect(s.maca, bloco, const Rect.fromLTWH(248, chao - 132, 32, 32), tinta);\n')],
    ('Animação com folha de sprites', 1): [('final passo = 150 * dt;', 'final passo = 300 * dt;')],
    ('Som: efeitos com audioplayers', 2): [('      perdidas += ossos.where((m) => m.vida <= 0).length;\n',
                                             "      final sumiram = ossos.where((m) => m.vida <= 0).length;\n      if (sumiram > 0) somErro.play(AssetSource('sons/dano.wav'));\n      perdidas += sumiram;\n")],
    ('Texto de jogo: contorno, sombra e fonte', 1): [('offset: Offset(0, 6)', 'offset: Offset(6, 6)')],
    ('Texto de jogo: contorno, sombra e fonte', 2): [("escrever('RECORDE $recorde m', GoogleFonts.pressStart2p(fontSize: 12,", "escrever('RECORDE $recorde m', GoogleFonts.vt323(fontSize: 24,")],
    ('Efeitos visuais: degradê, brilho e sombra', 0): [('ui.Gradient.radial(luz, 140,', 'ui.Gradient.radial(luz, 200,')],
    ('Efeitos visuais: degradê, brilho e sombra', 1): [('MaskFilter.blur(BlurStyle.normal, 24)', 'MaskFilter.blur(BlurStyle.normal, 40)')],
    ('Efeitos visuais: degradê, brilho e sombra', 2): [('const Color(0xFF4B2A6B)', 'const Color(0xFFFF8A3D)')],
    ('Projeto · Pega-Maçã', 0): [('  int vidas = 3;', '  int vidas = 5;'), ('      vidas = 3;', '      vidas = 5;')],
    ('Projeto · Pega-Maçã', 1): [
        ('  final bool boa;\n  Item(this.x, this.y, this.boa);', '  final bool boa;\n  final bool dourada;\n  Item(this.x, this.y, this.boa, this.dourada);'),
        ('      itens.add(Item(sorteio.nextDouble() * (largura - 36), -36, sorteio.nextDouble() < 0.75));',
         '      final boa = sorteio.nextDouble() < 0.75;\n      itens.add(Item(sorteio.nextDouble() * (largura - 36), -36, boa, boa && sorteio.nextDouble() < 0.1));'),
        ('        canvas.drawImageRect(s.maca, bloco, item.area, tinta);\n',
         '        canvas.drawImageRect(s.maca, bloco, item.area, tinta);\n        if (item.dourada) canvas.drawCircle(item.area.center, 22, Paint()..color = Colors.amber.withOpacity(0.5));\n'),
        ('        pontos++;\n        somItem', '        pontos += item.dourada ? 5 : 1;\n        somItem')],
    ('Projeto · Pega-Maçã', 2): [('      item.y += velocidadeQueda * dt;', '      item.y += (item.boa ? velocidadeQueda : velocidadeQueda * 0.6) * dt;')],
    ('Flame: o primeiro jogo', 0): [('debugMode = false;', 'debugMode = true;')],
    ('Flame: o primeiro jogo', 1): [('    add(Bola(Vector2(220, 360), Vector2(-120, 160), Colors.pinkAccent));\n',
                                     '    add(Bola(Vector2(220, 360), Vector2(-120, 160), Colors.pinkAccent));\n    add(Bola(Vector2(160, 500), Vector2(100, -140), Colors.lightBlueAccent));\n')],
    ('Flame: sprites e animação', 2): [('    add(SpriteAnimationComponent(animation: giro, position: Vector2(262, size.y - 170), size: Vector2.all(24)));',
                                        '    for (var i = 0; i < 3; i++) {\n      add(SpriteAnimationComponent(animation: giro, position: Vector2(120 + i * 40.0, size.y - 170), size: Vector2.all(24)));\n    }')],
    ('Flame: toque e arrasto em componentes', 0): [('    position.x += event.localDelta.x;\n', '    position.x += event.localDelta.x;\n    position.y += event.localDelta.y;\n')],
    ('Flame: toque e arrasto em componentes', 2): [
        ('class Toques extends FlameGame with TapCallbacks {\n  int pontos = 0;\n', 'class Toques extends FlameGame with TapCallbacks {\n  int pontos = 0;\n  late TextComponent placar;\n'),
        ('    add(Heroi());\n  }\n', "    add(Heroi());\n    placar = TextComponent(text: 'Ossos: 0', position: Vector2(16, 16));\n    add(placar);\n  }\n\n  @override\n  void update(double dt) {\n    super.update(dt);\n    placar.text = 'Ossos: $pontos';\n  }\n")],
    ('Flame: colisões com hitboxes', 0): [('debugMode = false;', 'debugMode = true;')],
    ('Flame: teclado, mundo e câmera', 1): [('    if (keysPressed.contains(LogicalKeyboardKey.arrowRight)) heroi.direcao += 1;\n',
                                             '    if (keysPressed.contains(LogicalKeyboardKey.arrowRight)) heroi.direcao += 1;\n    if (keysPressed.contains(LogicalKeyboardKey.shiftLeft)) heroi.direcao *= 2;\n')],
    ('Flame: teclado, mundo e câmera', 2): [('    heroi = Heroi();\n    world.add(heroi);\n',
                                             "    final brilho = await loadSpriteAnimation('osso.png', SpriteAnimationData.sequenced(amount: 6, stepTime: 0.1, textureSize: Vector2.all(16)));\n"
                                             "    for (int i = 1; i < 8; i++) {\n      world.add(SpriteAnimationComponent(animation: brilho, position: Vector2(i * 200.0, 24), size: Vector2.all(24)));\n    }\n"
                                             '    heroi = Heroi();\n    world.add(heroi);\n')],
    ('Projeto · Pula-Caixa em Flame', 2): [('  int recorde = 0;\n', '  int recorde = 0;\n  bool comemorou = false;\n'),
                                            ('      distancia += velocidade * dt;\n', "      distancia += velocidade * dt;\n      if (!comemorou && metros >= 100) {\n        comemorou = true;\n        FlameAudio.play('vitoria.wav');\n      }\n")],
    ('Flame: efeitos', 0): [('EffectController(duration: 1.2, alternate: true, infinite: true, curve: Curves.easeInOut)', 'EffectController(duration: 1.2, alternate: true, infinite: true, curve: Curves.bounceOut)')],
    ('Flame: efeitos', 1): [('EffectController(duration: 0.4, alternate: true, infinite: true, curve: Curves.easeInOut)', 'EffectController(duration: 0.2, alternate: true, infinite: true, curve: Curves.easeInOut)')],
    ('Flame: efeitos', 2): [('        MoveEffect.by(Vector2(0, -40), EffectController(duration: 0.15, alternate: true)),\n',
                             '        MoveEffect.by(Vector2(0, -40), EffectController(duration: 0.15, alternate: true)),\n        OpacityEffect.fadeOut(EffectController(duration: 0.5)),\n')],
    ('Flame: partículas', 1): [('acceleration: Vector2(0, 160)', 'acceleration: Vector2(0, 400)')],
    ('Flame: partículas', 2): [('child: CircleParticle(radius: 3, paint: Paint()..color = cor)', 'child: SpriteParticle(sprite: coracao, size: Vector2.all(12))')],
    ('Flame: paralaxe', 1): [('velocityMultiplierDelta: Vector2(1.8, 1.0),', 'velocityMultiplierDelta: Vector2(2.5, 1.0),'), ('final vChao = velocidade * 1.8 * 1.8 * 1.8;', 'final vChao = velocidade * 2.5 * 2.5 * 2.5;')],
    ('Flame: paralaxe', 2): [('velocidade = velocidade == 30 ? 90 : 30;', 'velocidade = velocidade == 30 ? 150 : 30;')],
    ('Flame: overlays, pausa e música', 0): [("const Text('Coleta', style: TextStyle(fontSize: 40,", "const Text('Caça ao Osso', style: TextStyle(fontSize: 40,")],
    ('Flame: overlays, pausa e música', 2): [("    FlameAudio.play('osso.wav');\n  }\n",
                                               "    FlameAudio.play('osso.wav');\n    if (pontos >= 10) {\n      pauseEngine();\n      FlameAudio.bgm.stop();\n      overlays.remove('BotaoPausa');\n      overlays.add('Menu');\n    }\n  }\n")],
    ('Flame: obstáculos que giram e consultas', 0): [('debugMode = false;', 'debugMode = true;')],
    ('Flame: obstáculos que giram e consultas', 1): [('add(Pa(Vector2(size.x / 2, 220), 1.6));', 'add(Pa(Vector2(size.x / 2, 220), 2.4));'), ('add(Pa(Vector2(size.x / 2, 440), -2.2));', 'add(Pa(Vector2(size.x / 2, 440), -3.2));')],
    ('Flame: obstáculos que giram e consultas', 2): [('    add(Pa(Vector2(size.x / 2, 440), -2.2));\n', '    add(Pa(Vector2(size.x / 2, 440), -2.2));\n    add(Pa(Vector2(size.x / 2, 330), 1.2));\n')],
    ('Pinça: zoom com dois dedos', 1): [('const casas = 8;', 'const casas = 12;')],
    ('Pinça: zoom com dois dedos', 2): [("appBar: AppBar(title: Text('Zoom ${escala.toStringAsFixed(1)}x')),",
                                         "appBar: AppBar(title: Text('Zoom ${escala.toStringAsFixed(1)}x'), actions: [IconButton(icon: const Icon(Icons.close), onPressed: () => setState(() => aberto = false))]),")],
    ('Projeto · Céu Agitado', 0): [('  int vidas = 3;', '  int vidas = 5;'), ('    vidas = 3;', '    vidas = 5;')],
    ('Projeto · Céu Agitado', 1): [('double intervalo = 1.0;', 'double intervalo = 0.6;')],
    ('Projeto · Céu Agitado', 2): [('  int vidas = 3;\n', '  int vidas = 3;\n  int recorde = 0;\n'),
                                   ('    if (vidas <= 0) {\n      pauseEngine();', '    if (vidas <= 0) {\n      if (pontos > recorde) recorde = pontos;\n      pauseEngine();'),
                                   ("                      Text('Pontos: ${game.pontos}', style: const TextStyle(fontSize: 18)),\n",
                                    "                      Text('Pontos: ${game.pontos}', style: const TextStyle(fontSize: 18)),\n                      Text('Recorde: ${game.recorde}', style: const TextStyle(fontSize: 18)),\n")],
    ('Joystick e botões na tela', 1): [('knob: CircleComponent(radius: 22, paint: Paint()..color = Colors.white70)', 'knob: CircleComponent(radius: 22, paint: Paint()..color = Colors.amber)')],
    ('Joystick e botões na tela', 2): [("  @override\n  Color backgroundColor() => const Color(0xFF3A6B35);",
                                        "  @override\n  void update(double dt) {\n    super.update(dt);\n    placar.text = 'Ossos: $ossos  ${joystick.direction.name}';\n  }\n\n  @override\n  Color backgroundColor() => const Color(0xFF3A6B35);")],
    ('Efeitos de cor e de caminho', 2): [('MoveAlongPathEffect(volta, EffectController(duration: 4,', 'MoveAlongPathEffect(volta, EffectController(duration: 2,')],
    ('Forge2D: corpos, gravidade e quiques', 1): [('super(gravity: Vector2(0, 10),', 'super(gravity: Vector2(0, -10),')],
    ('Forge2D: impulsos e contatos', 1): [('CircleShape()..radius = 1, density: 3,', 'CircleShape()..radius = 1, density: 8,')],
    ('Forge2D: impulsos e contatos', 2): [('  bool atingido = false;\n', '  bool atingido = false;\n  bool caiu = false;\n'),
                                          ('      (game as Estilingue).acertou();\n    }\n  }\n',
                                           '      (game as Estilingue).acertou();\n    }\n    if (other is Chao && atingido && !caiu) {\n      caiu = true;\n      (game as Estilingue).acertou();\n    }\n  }\n')],
    ('Forge2D: juntas e raio', 1): [('    final def = RevoluteJointDef()..initialize(eixo, bola, eixo.position);\n    world.createJoint(RevoluteJoint(def));',
                                     '    final def = DistanceJointDef()..initialize(eixo, bola, eixo.position, bola.position);\n    world.createJoint(DistanceJoint(def));')],
    ('Forge2D: juntas e raio', 2): [('  final origem = Vector2(-16, 21.5);\n  final fim = Vector2(16, 21.5);\n  Vector2 alvo = Vector2(16, 21.5);',
                                     '  final origem = Vector2(-16, 19);\n  final fim = Vector2(16, 19);\n  Vector2 alvo = Vector2(16, 19);')],
    ('Sensores: inclinar o celular', 0): [('vx = (vx + ax * 60 * dt)', 'vx = (vx + ax * 120 * dt)'), ('vy = (vy + ay * 60 * dt)', 'vy = (vy + ay * 120 * dt)')],
    ('Sensores: inclinar o celular', 1): [('      vx = (vx + ax * 60 * dt) * 0.99;\n      vy = (vy + ay * 60 * dt) * 0.99;', '      vx = (vx + ax * 60 * dt) * 0.95;\n      vy = (vy + ay * 60 * dt) * 0.95;')],
    ('Sensores: inclinar o celular', 2): [('vx = -vx * 0.5; }\n      if (x > largura - raio) { x = largura - raio; vx = -vx * 0.5; }', 'vx = -vx * 0.8; }\n      if (x > largura - raio) { x = largura - raio; vx = -vx * 0.8; }'),
                                          ('vy = -vy * 0.5; }\n      if (y > altura - raio) { y = altura - raio; vy = -vy * 0.5; }', 'vy = -vy * 0.8; }\n      if (y > altura - raio) { y = altura - raio; vy = -vy * 0.8; }')],
    ('Tiled: mapas prontos', 1): [("    placar.text = 'Ossos: $ossos';\n    FlameAudio.play('osso.wav');", "    placar.text = 'Ossos: $ossos · faltam ${world.children.query<Osso>().length - 1}';\n    FlameAudio.play('osso.wav');")],
    ('Salvar o jogo: recorde com Hive', 1): [("      caixa.put('recorde', recorde);\n    }\n    setState(() {});", "      caixa.put('recorde', recorde);\n    }\n    final partidas = caixa.get('partidas', defaultValue: 0) + 1;\n    caixa.put('partidas', partidas);\n    setState(() {});")],
    ('Salvar o jogo: recorde com Hive', 2): [("              ElevatedButton(onPressed: comecar, child: const Text('Jogar')),\n",
                                              "              ElevatedButton(onPressed: comecar, child: const Text('Jogar')),\n              TextButton(\n                onPressed: () {\n                  caixa.delete('recorde');\n                  setState(() => recorde = 0);\n                },\n                child: const Text('Apagar recorde', style: TextStyle(color: Colors.white70)),\n              ),\n")],
    ('Ranking online com Supabase', 1): [('  Future<void> terminar() async {\n    relogio?.cancel();\n',
                                          "  Future<void> terminar() async {\n    relogio?.cancel();\n    if (nome.text.trim().isEmpty) {\n      setState(() => aviso = 'Escreva seu nome');\n      return;\n    }\n")],
    ('Ranking online com Supabase', 2): [(".stream(primaryKey: ['id']).order(", ".stream(primaryKey: ['id']).eq('nome', nome.text).order(")],
    ('Projeto · Caça-Ossos', 2): [('if (gato.position.distanceTo(heroi.position) < 170)', 'if (gato.position.distanceTo(heroi.position) < 250)')],
    ('Desenhando o jogo com CustomPainter', 0): [('Paint()..color = const Color(0xFF7EC8F2)', 'Paint()..color = Colors.indigo.shade200')],
    ('Flame: o primeiro jogo', 2): [('const Color(0xFF14213D)', 'const Color(0xFF2E1A47)')],
    ('Projeto · Pula-Caixa em Flame', 0): [('const Color(0xFF8FD3FE)', 'const Color(0xFF14213D)')],
    ('Flame: paralaxe', 0): [('baseVelocity: Vector2(velocidade, 0)', 'baseVelocity: Vector2(5, 0)')],
    ('Projeto · Caça-Ossos', 3): [('osso.dourado ? 5 : 1', 'osso.dourado ? 10 : 1')],
}


MANUAL.update({
    ('Game design: analisar um jogo (MDA)', 0): [("'Cobrinha': [3, 1, 0, 4, 0, 1, 0, 5],", "'Cobrinha': [3, 1, 0, 5, 0, 1, 0, 5],")],
    ('Game design: analisar um jogo (MDA)', 1): [("  'Multijogador': [3, 2, 0, 3, 5, 1, 1, 3],\n", "  'Multijogador': [3, 2, 0, 3, 5, 1, 1, 3],\n  'Meu jogo': [2, 4, 3, 2, 0, 5, 1, 1],\n")],
    ('Game design: ética e bem-estar do jogador', 1): [("Premio('Osso comum', '🦴', 0.70)", "Premio('Osso comum', '🦴', 0.73)"), ("Premio('Coleira dourada', '👑', 0.05)", "Premio('Coleira dourada', '👑', 0.02)")],
    ('Game design: ética e bem-estar do jogador', 2): [("Premio('Osso comum', '🦴', 0.70)", "Premio('Osso comum', '🦴', 0.60)"), ("  Premio('Coleira dourada', '👑', 0.05),", "  Premio('Petisco', '🍖', 0.10),\n  Premio('Coleira dourada', '👑', 0.05),")],
    ('Carreira: game jams, portfólio e mercado', 0): [("const nome = 'Seu Nome';", "const nome = 'Ana Lima';")],
    ('Carreira: game jams, portfólio e mercado', 1): [("'Projeto em dupla'),\n];", "'Projeto em dupla'),\n  Projeto('Meu Jogo', 'Tudo', 'O jogo do meu projeto final.', 'meusite.itch.io/meujogo', 'Projeto final'),\n];")],
})

def resposta(titulo, i, code, desc, rx):
    """Devolve a lista de trocas que resolve a etapa, ou None."""
    m = MANUAL.get((titulo, i))
    if m:
        novo = code
        for a, b in m:
            if a not in novo:
                raise ValueError(f'gabarito de "{titulo}" etapa {i + 1}: não achei {a[:50]!r}')
            novo = novo.replace(a, b, 1)
        if not re.search(rx, novo):
            raise ValueError(f'gabarito de "{titulo}" etapa {i + 1} não cumpre a etapa')
        return [list(x) for x in m]
    g = gabarito(code, desc, rx)
    return [g] if g else None

# Aulas de leitura (tools/teoria.py)
MANUAL.update({
    ('Matemática de jogos: vetores', 2): [('if (d.distance > 2) {', 'if (d.distance > 40) {')],
    ('Matemática de jogos: ângulos, seno e cosseno', 2): [('Offset(cos(tempo), sin(tempo))', 'Offset(cos(-tempo), sin(-tempo))')],
    ('Matemática de jogos: interpolação e curvas', 1): [('pow(0.02, dt)', 'pow(0.3, dt)')],
    ('Matemática de jogos: interpolação e curvas', 2): [('double freia(double t) => 1 - (1 - t) * (1 - t);', 'double freia(double t) => 1 - (1 - t) * (1 - t) * (1 - t);')],
    ('Game design: objetivo, desafio e recompensa', 1): [('pontos += combo;', 'pontos += min(combo, 5);')],
    ('Game design: objetivo, desafio e recompensa', 2): [('        combo++;\n', '        combo++;\n        tempoLimite = max(0.6, tempoLimite - 0.05);\n')],
    ('Game design: game feel e "suco"', 2): [('bool comSuco = true;', 'bool comSuco = false;')],
    ('Arte de jogos: pixel art e paletas', 0): [("  'Malhado': {'C': Color(0xFFF2EEE6), 'D': Color(0xFF6B4A2E), 'L': Color(0xFFC9A27A), 'k': Color(0xFF222034), 't': Color(0xFFEC6878)},\n",
                                               "  'Malhado': {'C': Color(0xFFF2EEE6), 'D': Color(0xFF6B4A2E), 'L': Color(0xFFC9A27A), 'k': Color(0xFF222034), 't': Color(0xFFEC6878)},\n"
                                               "  'Dourado': {'C': Color(0xFFE0A100), 'D': Color(0xFF9C6B00), 'L': Color(0xFFFFE08A), 'k': Color(0xFF222034), 't': Color(0xFFEC6878)},\n")],
    ('Arte de jogos: pixel art e paletas', 2): [("'...DC...CCCC.t..'", "'...DC...CCCC....'")],
    ('Som de jogos: efeitos e música', 2): [("  'vitoria': Envelope(0.01, 0.1, 0.8, 0.3),\n", "  'vitoria': Envelope(0.01, 0.1, 0.8, 0.3),\n  'dano': Envelope(0.0, 0.15, 0.2, 0.1),\n")],
})

# Parte 7 e leituras da segunda leva
MANUAL.update({
    ('Matemática de jogos: física e passo de tempo', 1): [('double passo = 1 / 120;', 'double passo = 1 / 240;')],
    ('Matemática de jogos: física e passo de tempo', 2): [('Offset vel = const Offset(900, -150);', 'Offset vel = const Offset(400, -150);')],
    ('Matemática de jogos: colisão em detalhes', 1): [('Size tamanho = const Size(110, 80);', 'Size tamanho = const Size(200, 40);')],
    ('Matemática de jogos: colisão em detalhes', 2): [('bool mostrarEmpurrao = true;', 'bool mostrarEmpurrao = false;')],
    ('Arte de jogos: interface e acessibilidade', 1): [('bool coresSeguras = false;', 'bool coresSeguras = true;')],
    ('Navegação: menu, fases e pausa', 2): [("child: const Text('Jogar'),", "child: const Text('Começar'),")],
    ('Game design: design de fases e ritmo', 1): [("trechos = ['ensina', 'pratica',", "trechos = ['desafio', 'pratica',")],
    ('Game design: design de fases e ritmo', 2): [("'chefe': 1.0,", "'chefe': 0.9,")],
    ('Fases e estrelas: progresso com Hive', 0): [("  Fase('Praia', 11, 10),\n", "  Fase('Praia', 11, 10),\n  Fase('Parque', 13, 10),\n")],
    ('Fases e estrelas: progresso com Hive', 1): [('if (sobra > 0.5) return 3;', 'if (sobra > 0.6) return 3;')],
    ('Matemática de jogos: probabilidade e sorteio', 0): [("Item('Osso dourado', 3,", "Item('Osso dourado', 1,")],
    ('Matemática de jogos: probabilidade e sorteio', 2): [("  Item('Osso dourado', 3, Color(0xFFFFC107)),\n", "  Item('Petisco', 20, Color(0xFFA1887F)),\n  Item('Osso dourado', 3, Color(0xFFFFC107)),\n")],
    ('Geração procedural: semente, labirinto e cavernas', 1): [('int passosSuavizar = 4;', 'int passosSuavizar = 1;')],
    ('Geração procedural: semente, labirinto e cavernas', 2): [('int semente = 42;', 'int semente = 2026;')],
    ('Caminho até o alvo: BFS e A*', 1): [('bool aEstrela = false;', 'bool aEstrela = true;')],
    ('Caminho até o alvo: BFS e A*', 2): [('int estimativa(Celula a, Celula b) => (a.x - b.x).abs() + (a.y - b.y).abs();', 'int estimativa(Celula a, Celula b) => 3 * ((a.x - b.x).abs() + (a.y - b.y).abs());')],
    ('Desempenho: medir FPS e reaproveitar objetos', 1): [('if (tempos.length > 30)', 'if (tempos.length > 60)')],
    ('Desempenho: medir FPS e reaproveitar objetos', 2): [('size: Vector2.all(28), anchor', 'size: Vector2.all(40), anchor')],
    ('Programação de jogos: arquitetura em camadas', 0): [('final int vidasIniciais = 3;', 'final int vidasIniciais = 5;'), ('  int vidas = 3;', '  int vidas = 5;')],
    ('Programação de jogos: arquitetura em camadas', 1): [('if (ossos % 5 == 0)', 'if (ossos % 10 == 0)')],
    ('Game design: testar com jogadores', 2): [("'#...x.....#...#',", "'#.........#...#',")],
    ('Produção: publicar o jogo', 0): [("const String versao = '1.0.0+1';", "const String versao = '1.0.1+2';")],
    ('Produção: publicar o jogo', 1): [("  Etapa('Loja', 'Chave de assinatura',", "  Etapa('Qualidade', 'Pedir para 3 pessoas jogarem', 'Playtest antes de publicar.'),\n  Etapa('Loja', 'Chave de assinatura',")],
    ('Produção: publicar o jogo', 2): [("'Tudo pronto: pode enviar para a loja! 🎉'", "'Agora é com você: publique e mostre para a turma!'")],
    ('Projeto · Trilha do Caramelo', 0): [('  int vidas = 3;', '  int vidas = 5;'), ("'♡' * (3 - vidas)", "'♡' * (5 - vidas)")],
    ('Projeto · Trilha do Caramelo', 3): [("  InfoFase('Feira', 'fase3.tmx'),\n", "  InfoFase('Feira', 'fase3.tmx'),\n  InfoFase('Bônus', 'fase1.tmx'),\n")],
})

# Terceira leva de leituras
MANUAL.update({
    ('Game design: narrativa e personagens', 0): [("  'Sozinho': [],\n", "  'Sozinho': ['Achou'],\n  'Achou': [],\n"), ("'Amigos': 4};", "'Amigos': 4, 'Achou': 3};")],
    ('Game design: narrativa e personagens', 1): [("  'Fuga': [],", "  'Fuga': ['Desculpa'],")],
    ('Game design: narrativa e personagens', 2): [("'Muro': ['Gentil', 'Bravo'],", "'Muro': ['Gentil', 'Bravo', 'Fuga'],")],
    ('Projeto final: o seu jogo', 0): [("  ['arte', 'Arte e som', 'Pixel art 16×16, música alegre em loop'],\n", "  ['arte', 'Arte e som', 'Pixel art 16×16, música alegre em loop'],\n  ['publico', 'Para quem é o jogo', 'Crianças de 8 a 12 anos'],\n")],
    ('Projeto final: o seu jogo', 1): [("entrega (link na 🕹 Galeria)', 6]", "entrega (link na 🕹 Galeria)', 8]")],
    ('Projeto final: o seu jogo', 2): [("divertido e claro', 3]", "divertido e claro', 4]"), ("comentado', 1]", "comentado', 0]")],
})
