import 'dart:math';
import 'package:flame/components.dart';
import 'package:flame/game.dart';
import 'package:flame/input.dart';
import 'package:flame_audio/flame_audio.dart';
import 'package:flame_tiled/flame_tiled.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

void main() => runApp(GameWidget(game: Plataforma()));

class Plataforma extends FlameGame with HasKeyboardHandlerComponents {
  final double escala = 3;
  final List<Rect> solidos = [];
  final List<Rect> plataformas = [];
  final List<Rect> perigos = [];
  Rect chegada = Rect.zero;
  Vector2 inicio = Vector2.zero();
  late Caramelo caramelo;
  late TextComponent placar;
  int ossos = 0;
  double larguraMapa = 0;
  double alturaMapa = 0;

  @override
  Color backgroundColor() => const Color(0xFF8FD3F4);

  @override
  Future<void> onLoad() async {
    final mapa = await TiledComponent.load('fase1.tmx', Vector2.all(16 * escala));
    world.add(mapa);
    larguraMapa = mapa.width;
    alturaMapa = mapa.height;

    // camada solidos: chão (bloqueia dos quatro lados) e plataformas (só por cima)
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
      if (o.type == 'inicio') {
        inicio = onde;
      } else if (o.type == 'osso') {
        world.add(Osso(onde));
      } else if (o.type == 'perigo') {
        perigos.add(Rect.fromLTWH(o.x * escala, o.y * escala, o.width * escala, o.height * escala));
      } else if (o.type == 'fim') {
        chegada = Rect.fromLTWH(o.x * escala, o.y * escala, o.width * escala, o.height * escala);
      }
    }

    caramelo = Caramelo(inicio.clone());
    world.add(caramelo);

    placar = TextComponent(text: 'Ossos: 0', position: Vector2(16, 16));
    camera.viewport.add(placar);
    camera.viewport.add(Botao('◀', Vector2(20, size.y - 90), (apertado) => caramelo.esquerda = apertado));
    camera.viewport.add(Botao('▶', Vector2(100, size.y - 90), (apertado) => caramelo.direita = apertado));
    camera.viewport.add(Botao('⤒', Vector2(size.x - 90, size.y - 90), (apertado) {
      if (apertado) caramelo.pular();
    }));
  }

  @override
  void update(double dt) {
    super.update(dt);
    // a câmera acompanha o caramelo, mas não mostra o que fica fora do mapa
    final meio = size / 2;
    final x = caramelo.position.x.clamp(meio.x, larguraMapa - meio.x).toDouble();
    final y = (caramelo.position.y - 80).clamp(meio.y, max(meio.y, alturaMapa - meio.y)).toDouble();
    camera.viewfinder.position = Vector2(x, y);
  }

  void pegou() {
    ossos++;
    placar.text = 'Ossos: $ossos';
    FlameAudio.play('osso.wav');
  }

  void caiu() {
    FlameAudio.play('dano.wav');
    caramelo.position = inicio.clone();
    caramelo.velocidade.setZero();
  }

  void chegou() {
    FlameAudio.play('vitoria.wav');
    placar.text = 'Chegou! Ossos: $ossos';
    caramelo.position = inicio.clone();
    caramelo.velocidade.setZero();
  }
}

class Caramelo extends SpriteAnimationComponent with KeyboardHandler, HasGameReference<Plataforma> {
  Caramelo(Vector2 onde) : super(position: onde, size: Vector2.all(48), anchor: Anchor.bottomCenter);

  final Vector2 velocidade = Vector2.zero();
  double gravidade = 1400;
  double forcaPulo = 640;
  double rapidez = 220;
  bool esquerda = false;
  bool direita = false;
  bool noChao = false;
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

  // o corpo de colisão é menor que o desenho: 30 x 36, com os pés em position
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

  @override
  void update(double dt) {
    super.update(dt);
    final dir = (direita ? 1 : 0) - (esquerda ? 1 : 0);
    velocidade.x = dir * rapidez;
    velocidade.y += gravidade * dt;

    // 1) anda no eixo x e desfaz a sobra se entrou num bloco
    position.x += velocidade.x * dt;
    for (final s in game.solidos) {
      final c = corpo();
      if (c.overlaps(s)) {
        if (velocidade.x > 0) position.x = s.left - 15;
        if (velocidade.x < 0) position.x = s.right + 15;
      }
    }

    // 2) anda no eixo y: caindo, pousa em cima; subindo, bate a cabeça
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
    // plataformas finas: só seguram quem vem de cima
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

    if (game.perigos.any((p) => p.overlaps(corpo())) || position.y > 1000) game.caiu();
    if (game.chegada.overlaps(corpo())) game.chegou();
  }
}

class Osso extends SpriteAnimationComponent with HasGameReference<Plataforma> {
  Osso(Vector2 onde) : super(position: onde, size: Vector2.all(36), anchor: Anchor.center);

  @override
  Future<void> onLoad() async {
    animation = await game.loadSpriteAnimation('osso.png', SpriteAnimationData.sequenced(amount: 6, stepTime: 0.1, textureSize: Vector2.all(16)));
  }

  @override
  void update(double dt) {
    super.update(dt);
    if (game.caramelo.corpo().overlaps(toRect())) {
      removeFromParent();
      game.pegou();
    }
  }
}

// botão da tela: avisa quando aperta e quando solta
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
