import 'dart:math';
import 'package:flame/components.dart';
import 'package:flame/events.dart';
import 'package:flame/game.dart';
import 'package:flame/input.dart';
import 'package:flame_audio/flame_audio.dart';
import 'package:flame_tiled/flame_tiled.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:hive_flutter/hive_flutter.dart';

Future<void> main() async {
  await Hive.initFlutter();
  await Hive.openBox('trilha');
  runApp(const MaterialApp(debugShowCheckedModeBanner: false, home: Menu()));
}

class InfoFase {
  final String nome;
  final String arquivo;
  const InfoFase(this.nome, this.arquivo);
}

const fases = [
  InfoFase('Quintal', 'fase1.tmx'),
  InfoFase('Praça', 'fase2.tmx'),
  InfoFase('Feira', 'fase3.tmx'),
];

int estrelasDe(int i) => Hive.box('trilha').get('estrelas$i', defaultValue: 0);
bool liberada(int i) => i == 0 || estrelasDe(i - 1) > 0;

// ------------------------------------------------------------ telas do Flutter
class Menu extends StatelessWidget {
  const Menu({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF8FD3F4),
      body: Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Text('Trilha do', style: TextStyle(fontSize: 22, color: Colors.white)),
            const Text('Caramelo', style: TextStyle(fontSize: 48, fontWeight: FontWeight.bold, color: Color(0xFF8A4B12))),
            const SizedBox(height: 32),
            FilledButton(
              onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (context) => const Mapa())),
              child: const Text('Jogar'),
            ),
            const SizedBox(height: 16),
            const Text('◀ ▶ para andar, ⤒ para pular.\nPule na cabeça dos gatos!', textAlign: TextAlign.center),
          ],
        ),
      ),
    );
  }
}

class Mapa extends StatefulWidget {
  const Mapa({super.key});

  @override
  State<Mapa> createState() => _MapaState();
}

class _MapaState extends State<Mapa> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Escolha a fase')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          for (int i = 0; i < fases.length; i++)
            Card(
              child: ListTile(
                leading: CircleAvatar(child: liberada(i) ? Text('${i + 1}') : const Icon(Icons.lock)),
                title: Text(fases[i].nome),
                subtitle: Text(liberada(i) ? '★ chegar   ★ todos os ossos   ★ sem dano' : 'Complete a fase anterior'),
                trailing: Text('★' * estrelasDe(i) + '☆' * (3 - estrelasDe(i)), style: const TextStyle(fontSize: 22, color: Colors.amber)),
                onTap: liberada(i)
                    ? () => Navigator.push(context, MaterialPageRoute(builder: (context) => TelaFase(indice: i))).then((_) => setState(() {}))
                    : null,
              ),
            ),
        ],
      ),
    );
  }
}

class TelaFase extends StatelessWidget {
  final int indice;
  const TelaFase({super.key, required this.indice});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: GameWidget(
        game: Trilha(indice),
        overlayBuilderMap: {
          'pausa': (context, Trilha jogo) => Janela(titulo: 'Pausa', filhos: [
                FilledButton(onPressed: jogo.continuar, child: const Text('Continuar')),
                OutlinedButton(onPressed: () => Navigator.pop(context), child: const Text('Sair da fase')),
              ]),
          'fim': (context, Trilha jogo) => Janela(titulo: jogo.estrelas > 0 ? 'Chegou!' : 'Fim das vidas', filhos: [
                Text('★' * jogo.estrelas + '☆' * (3 - jogo.estrelas), style: const TextStyle(fontSize: 40, color: Colors.amber)),
                Text('Ossos: ${jogo.ossos} de ${jogo.totalOssos}'),
                if (jogo.estrelas > 0 && indice < fases.length - 1)
                  FilledButton(
                    onPressed: () => Navigator.pushReplacement(context, MaterialPageRoute(builder: (context) => TelaFase(indice: indice + 1))),
                    child: const Text('Próxima fase'),
                  ),
                OutlinedButton(
                  onPressed: () => Navigator.pushReplacement(context, MaterialPageRoute(builder: (context) => TelaFase(indice: indice))),
                  child: const Text('Jogar de novo'),
                ),
                TextButton(onPressed: () => Navigator.pop(context), child: const Text('Escolher fase')),
              ]),
        },
      ),
    );
  }
}

class Janela extends StatelessWidget {
  final String titulo;
  final List<Widget> filhos;
  const Janela({super.key, required this.titulo, required this.filhos});

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Card(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Text(titulo, style: const TextStyle(fontSize: 26, fontWeight: FontWeight.bold)),
              for (final f in filhos) Padding(padding: const EdgeInsets.only(top: 10), child: f),
            ],
          ),
        ),
      ),
    );
  }
}

// ------------------------------------------------------------ o jogo
class Trilha extends FlameGame with HasKeyboardHandlerComponents {
  final int indice;
  Trilha(this.indice);

  final double escala = 3;
  final List<Rect> solidos = [];
  final List<Rect> plataformas = [];
  final List<Rect> perigos = [];
  Rect chegada = Rect.zero;
  Vector2 inicio = Vector2.zero();
  double larguraMapa = 0;
  double alturaMapa = 0;
  late Caramelo caramelo;
  late TextComponent hud;
  int vidas = 3;
  int ossos = 0;
  int totalOssos = 0;
  bool levouDano = false;
  bool acabou = false;
  int estrelas = 0;

  @override
  Color backgroundColor() => const Color(0xFF8FD3F4);

  @override
  Future<void> onLoad() async {
    final mapa = await TiledComponent.load(fases[indice].arquivo, Vector2.all(16 * escala));
    world.add(mapa);
    larguraMapa = mapa.width;
    alturaMapa = mapa.height;

    for (final o in mapa.tileMap.getLayer<ObjectGroup>('solidos')!.objects) {
      final r = Rect.fromLTWH(o.x * escala, o.y * escala, o.width * escala, o.height * escala);
      if (o.type == 'plataforma') {
        plataformas.add(r);
      } else {
        solidos.add(r);
      }
    }
    for (final o in mapa.tileMap.getLayer<ObjectGroup>('objetos')!.objects) {
      final onde = Vector2(o.x * escala, o.y * escala);
      final area = Rect.fromLTWH(o.x * escala, o.y * escala, o.width * escala, o.height * escala);
      switch (o.type) {
        case 'inicio':
          inicio = onde;
        case 'osso':
          world.add(Osso(onde, dourado: false));
          totalOssos++;
        case 'dourado':
          world.add(Osso(onde, dourado: true));
          totalOssos++;
        case 'inimigo':
          world.add(Gato(onde));
        case 'perigo':
          perigos.add(area);
        case 'fim':
          chegada = area;
      }
    }
    caramelo = Caramelo(inicio.clone());
    world.add(caramelo);

    hud = TextComponent(text: '', position: Vector2(16, 16), textRenderer: TextPaint(style: const TextStyle(fontSize: 22, color: Colors.white, shadows: [Shadow(blurRadius: 3)])));
    camera.viewport.add(hud);
    camera.viewport.add(BotaoPausa());
    camera.viewport.add(Botao('◀', Vector2(16, size.y - 90), (a) => caramelo.esquerda = a));
    camera.viewport.add(Botao('▶', Vector2(96, size.y - 90), (a) => caramelo.direita = a));
    camera.viewport.add(Botao('⤒', Vector2(size.x - 90, size.y - 90), (a) {
      if (a) caramelo.pular();
    }));
    FlameAudio.bgm.play('musica_aventura.mp3', volume: 0.3);
  }

  bool temChao(double x, double y) =>
      solidos.any((s) => s.contains(Offset(x, y))) || plataformas.any((p) => p.contains(Offset(x, y)));

  @override
  void update(double dt) {
    super.update(dt);
    final meio = size / 2;
    final x = caramelo.position.x.clamp(meio.x, larguraMapa - meio.x).toDouble();
    final y = (caramelo.position.y - 80).clamp(meio.y, max(meio.y, alturaMapa - meio.y)).toDouble();
    camera.viewfinder.position = Vector2(x, y);
    hud.text = '${'♥' * vidas}${'♡' * (3 - vidas)}   🦴 $ossos/$totalOssos';
  }

  void pegou(Osso o) {
    ossos++;
    FlameAudio.play(o.dourado ? 'poder.wav' : 'osso.wav');
  }

  void dano() {
    levouDano = true;
    vidas--;
    FlameAudio.play('dano.wav');
    if (vidas <= 0) terminar(false);
  }

  void caiu() {
    dano();
    caramelo.position = inicio.clone();
    caramelo.velocidade.setZero();
  }

  void terminar(bool chegou) {
    if (acabou) return;
    acabou = true;
    estrelas = chegou ? 1 + (ossos == totalOssos ? 1 : 0) + (levouDano ? 0 : 1) : 0;
    final caixa = Hive.box('trilha');
    if (estrelas > estrelasDe(indice)) caixa.put('estrelas$indice', estrelas);
    FlameAudio.bgm.stop();
    FlameAudio.play(chegou ? 'vitoria.wav' : 'derrota.wav');
    pauseEngine();
    overlays.add('fim');
  }

  void pausar() {
    pauseEngine();
    overlays.add('pausa');
  }

  void continuar() {
    overlays.remove('pausa');
    resumeEngine();
  }

  @override
  void onRemove() {
    FlameAudio.bgm.stop();
    super.onRemove();
  }
}

class Caramelo extends SpriteAnimationComponent with KeyboardHandler, HasGameReference<Trilha> {
  Caramelo(Vector2 onde) : super(position: onde, size: Vector2.all(48), anchor: Anchor.bottomCenter);

  final Vector2 velocidade = Vector2.zero();
  double gravidade = 1400;
  double forcaPulo = 700;
  double rapidez = 230;
  bool esquerda = false;
  bool direita = false;
  bool noChao = false;
  double invencivel = 0;
  late SpriteAnimation correndo;
  late SpriteAnimation pulando;
  late SpriteAnimation sentado;

  @override
  Future<void> onLoad() async {
    correndo = await game.loadSpriteAnimation('heroi.png', SpriteAnimationData.sequenced(amount: 4, stepTime: 0.1, textureSize: Vector2.all(16)));
    pulando = await game.loadSpriteAnimation('caramelo_pulo.png', SpriteAnimationData.sequenced(amount: 1, stepTime: 1, textureSize: Vector2.all(16)));
    sentado = await game.loadSpriteAnimation('caramelo_sentado.png', SpriteAnimationData.sequenced(amount: 2, stepTime: 0.4, textureSize: Vector2.all(16)));
    animation = sentado;
  }

  Rect corpo() => Rect.fromLTWH(position.x - 15, position.y - 36, 30, 36);

  void pular() {
    if (noChao) {
      velocidade.y = -forcaPulo;
      noChao = false;
      FlameAudio.play('pulo.wav');
    }
  }

  @override
  bool onKeyEvent(KeyEvent event, Set<LogicalKeyboardKey> keysPressed) {
    esquerda = keysPressed.contains(LogicalKeyboardKey.arrowLeft);
    direita = keysPressed.contains(LogicalKeyboardKey.arrowRight);
    if (event is KeyDownEvent && (event.logicalKey == LogicalKeyboardKey.space || event.logicalKey == LogicalKeyboardKey.arrowUp)) {
      pular();
    }
    return true;
  }

  void machucar(double deOndeX) {
    if (invencivel > 0) return;
    invencivel = 1.5;
    velocidade.y = -350;
    position.x += position.x < deOndeX ? -24 : 24;
    game.dano();
  }

  @override
  void update(double dt) {
    super.update(dt);
    final dir = (direita ? 1 : 0) - (esquerda ? 1 : 0);
    velocidade.x = dir * rapidez;
    velocidade.y += gravidade * dt;

    position.x += velocidade.x * dt;
    position.x = position.x.clamp(15, game.larguraMapa - 15).toDouble();
    for (final s in game.solidos) {
      if (corpo().overlaps(s)) {
        if (velocidade.x > 0) position.x = s.left - 15;
        if (velocidade.x < 0) position.x = s.right + 15;
      }
    }

    final pesAntes = position.y;
    position.y += velocidade.y * dt;
    noChao = false;
    for (final s in game.solidos) {
      if (corpo().overlaps(s)) {
        if (velocidade.y > 0) {
          position.y = s.top;
          noChao = true;
        } else {
          position.y = s.bottom + 36;
        }
        velocidade.y = 0;
      }
    }
    for (final p in game.plataformas) {
      if (velocidade.y >= 0 && pesAntes <= p.top && corpo().overlaps(p)) {
        position.y = p.top;
        velocidade.y = 0;
        noChao = true;
      }
    }

    if (dir < 0 && scale.x > 0) flipHorizontally();
    if (dir > 0 && scale.x < 0) flipHorizontally();
    animation = !noChao ? pulando : (dir == 0 ? sentado : correndo);

    // piscando enquanto está invencível
    if (invencivel > 0) {
      invencivel -= dt;
      opacity = (invencivel * 10).floor() % 2 == 0 ? 0.3 : 1;
    } else {
      opacity = 1;
    }

    if (game.perigos.any((p) => p.overlaps(corpo())) || position.y > game.alturaMapa + 100) game.caiu();
    if (game.chegada.overlaps(corpo())) game.terminar(true);
  }
}

class Gato extends SpriteAnimationComponent with HasGameReference<Trilha> {
  Gato(Vector2 onde) : super(position: onde, size: Vector2.all(44), anchor: Anchor.bottomCenter);

  double velocidade = 60;
  int direcao = -1;

  @override
  Future<void> onLoad() async {
    animation = await game.loadSpriteAnimation('gato.png', SpriteAnimationData.sequenced(amount: 2, stepTime: 0.25, textureSize: Vector2.all(16)));
  }

  Rect corpo() => Rect.fromLTWH(position.x - 16, position.y - 30, 32, 30);

  @override
  void update(double dt) {
    super.update(dt);
    position.x += direcao * velocidade * dt;
    // patrulha: vira ao achar parede ou a beira do chão
    final frente = position.x + direcao * 18;
    final parede = game.solidos.any((s) => s.contains(Offset(frente, position.y - 10)));
    final semChao = !game.temChao(frente, position.y + 4);
    if (parede || semChao) {
      direcao = -direcao;
      flipHorizontally();
    }

    final c = game.caramelo;
    if (c.corpo().overlaps(corpo())) {
      // caindo por cima: derruba o gato e quica
      if (c.velocidade.y > 0 && c.position.y < position.y - 16) {
        removeFromParent();
        c.velocidade.y = -450;
        FlameAudio.play('batida.wav');
      } else {
        c.machucar(position.x);
      }
    }
  }
}

class Osso extends SpriteAnimationComponent with HasGameReference<Trilha> {
  final bool dourado;
  Osso(Vector2 onde, {required this.dourado}) : super(position: onde, size: Vector2.all(dourado ? 44 : 36), anchor: Anchor.center);

  @override
  Future<void> onLoad() async {
    animation = await game.loadSpriteAnimation(dourado ? 'osso_dourado.png' : 'osso.png', SpriteAnimationData.sequenced(amount: 6, stepTime: 0.1, textureSize: Vector2.all(16)));
  }

  @override
  void update(double dt) {
    super.update(dt);
    if (game.caramelo.corpo().overlaps(toRect())) {
      removeFromParent();
      game.pegou(this);
    }
  }
}

class BotaoPausa extends PositionComponent with TapCallbacks, HasGameReference<Trilha> {
  BotaoPausa() : super(size: Vector2.all(44));

  @override
  Future<void> onLoad() async {
    position = Vector2(game.size.x - 56, 10);
  }

  @override
  void render(Canvas canvas) {
    canvas.drawRRect(RRect.fromRectAndRadius(size.toRect(), const Radius.circular(10)), Paint()..color = Colors.black26);
    canvas.drawRect(const Rect.fromLTWH(14, 12, 6, 20), Paint()..color = Colors.white);
    canvas.drawRect(const Rect.fromLTWH(24, 12, 6, 20), Paint()..color = Colors.white);
  }

  @override
  void onTapDown(TapDownEvent event) {
    game.pausar();
  }
}

class Botao extends ButtonComponent {
  Botao(String simbolo, Vector2 onde, void Function(bool) aviso)
      : super(
          position: onde,
          size: Vector2.all(70),
          button: Tecla(simbolo, Colors.black26),
          buttonDown: Tecla(simbolo, Colors.black54),
          onPressed: () => aviso(true),
          onReleased: () => aviso(false),
          onCancelled: () => aviso(false),
        );
}

class Tecla extends PositionComponent {
  final String simbolo;
  final Color cor;
  Tecla(this.simbolo, this.cor) : super(size: Vector2.all(70));

  @override
  void render(Canvas canvas) {
    canvas.drawCircle(const Offset(35, 35), 35, Paint()..color = cor);
    final tp = TextPainter(text: TextSpan(text: simbolo, style: const TextStyle(fontSize: 30, color: Colors.white)), textDirection: TextDirection.ltr)..layout();
    tp.paint(canvas, Offset(35 - tp.width / 2, 35 - tp.height / 2));
  }
}
