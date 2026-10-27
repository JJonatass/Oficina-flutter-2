import 'dart:math';
import 'package:flame/components.dart';
import 'package:flame/game.dart';
import 'package:flame/input.dart';
import 'package:flutter/material.dart';

void main() => runApp(GameWidget(game: Passeio()));

const modos = ['direto', 'suave', 'olhar à frente', 'zona morta'];

class Passeio extends FlameGame {
  final double larguraMundo = 2400;
  final double alturaMundo = 1080;
  final double chao = 780;
  final sorteio = Random(7);
  late Caramelo caramelo;
  late TextComponent placar;
  int modo = 1;
  final double suavidade = 4; // quanto maior, mais depressa a câmera alcança o alvo
  final double zonaMorta = 80; // meia largura do retângulo em que o caramelo anda sem mexer a câmera
  double tremor = 0; // de 0 a 1, diminui sozinho
  Vector2 foco = Vector2.zero(); // para onde a câmera olha, sem o tremor

  @override
  Color backgroundColor() => const Color(0xFF8FD3F4);

  @override
  Future<void> onLoad() async {
    world.add(RectangleComponent(position: Vector2(0, chao), size: Vector2(larguraMundo, alturaMundo - chao), paint: Paint()..color = const Color(0xFF6DBE45)));
    // árvores e marcos de distância: sem referência no cenário, não dá para perceber a câmera andando
    for (var i = 0; i < 24; i++) {
      world.add(Arvore(Vector2(sorteio.nextDouble() * larguraMundo, chao)));
    }
    for (var x = 0; x <= 2400; x += 200) {
      world.add(TextComponent(text: '${x ~/ 100} m', position: Vector2(x.toDouble() + 4, chao + 12)));
    }
    world.add(RectangleComponent(position: Vector2(700, chao - 160), size: Vector2(220, 24), paint: Paint()..color = const Color(0xFF8D6E63)));
    world.add(RectangleComponent(position: Vector2(1300, chao - 260), size: Vector2(220, 24), paint: Paint()..color = const Color(0xFF8D6E63)));
    caramelo = Caramelo(Vector2(200, chao));
    world.add(caramelo);
    foco = caramelo.position.clone();

    placar = TextComponent(text: '', position: Vector2(16, 16));
    camera.viewport.add(Moldura());
    camera.viewport.add(placar);
    camera.viewport.add(Botao('◀', Vector2(16, size.y - 86), (a) => caramelo.esquerda = a));
    camera.viewport.add(Botao('▶', Vector2(96, size.y - 86), (a) => caramelo.direita = a));
    camera.viewport.add(Botao('⤒', Vector2(size.x - 86, size.y - 86), (a) {
      if (a) caramelo.pular();
    }));
    camera.viewport.add(Botao('💥', Vector2(size.x - 86, size.y - 166), (a) {
      if (a) tremer(0.7);
    }));
    camera.viewport.add(Botao('🎥', Vector2(size.x - 86, 16), (a) {
      if (a) modo = (modo + 1) % modos.length;
    }));
  }

  void tremer(double quanto) {
    tremor = min(1.0, tremor + quanto);
  }

  @override
  void update(double dt) {
    super.update(dt);
    final alvo = caramelo.position.clone();
    alvo.y -= 100; // mostra mais do que está acima do caramelo
    if (modo == 0) {
      foco = alvo; // direto: gruda no caramelo (e treme junto com cada passo)
    } else if (modo == 1) {
      foco += (alvo - foco) * min(1.0, suavidade * dt); // suave: anda uma fração do caminho a cada quadro
    } else if (modo == 2) {
      alvo.x += caramelo.direcao * 140; // olha para onde o caramelo está indo
      foco += (alvo - foco) * min(1.0, suavidade * dt);
    } else {
      // zona morta: a câmera só anda quando o caramelo sai do retângulo do meio
      if (alvo.x - foco.x > zonaMorta) foco.x = alvo.x - zonaMorta;
      if (alvo.x - foco.x < -zonaMorta) foco.x = alvo.x + zonaMorta;
      if (alvo.y - foco.y > 60) foco.y = alvo.y - 60;
      if (alvo.y - foco.y < -60) foco.y = alvo.y + 60;
    }
    // limites do mundo: a câmera nunca mostra o que fica fora do mapa
    final meio = size / 2;
    foco.x = foco.x.clamp(meio.x, larguraMundo - meio.x).toDouble();
    foco.y = foco.y.clamp(meio.y, alturaMundo - meio.y).toDouble();
    // tremor: um empurrão aleatório que fica mais fraco a cada quadro
    var empurrao = Vector2.zero();
    if (tremor > 0) {
      final forca = tremor * tremor * 18;
      empurrao = Vector2((sorteio.nextDouble() * 2 - 1) * forca, (sorteio.nextDouble() * 2 - 1) * forca);
      tremor = max(0.0, tremor - dt * 1.5);
    }
    camera.viewfinder.position = foco + empurrao;
    placar.text = 'Câmera: ${modos[modo]}';
  }
}

class Caramelo extends SpriteAnimationComponent with HasGameReference<Passeio> {
  Caramelo(Vector2 onde) : super(position: onde, size: Vector2.all(64), anchor: Anchor.bottomCenter);
  bool esquerda = false;
  bool direita = false;
  double direcao = 1;
  double vy = 0;
  bool noChao = true;

  @override
  Future<void> onLoad() async {
    animation = await game.loadSpriteAnimation('heroi.png', SpriteAnimationData.sequenced(amount: 4, stepTime: 0.1, textureSize: Vector2.all(16)));
  }

  void pular() {
    if (noChao) {
      vy = -620;
      noChao = false;
    }
  }

  @override
  void update(double dt) {
    super.update(dt);
    final andar = (direita ? 1 : 0) - (esquerda ? 1 : 0);
    if (andar != 0) {
      direcao = andar.toDouble();
      scale.x = direcao;
    }
    position.x = (position.x + andar * 280 * dt).clamp(20, game.larguraMundo - 20).toDouble();
    vy += 1500 * dt;
    position.y += vy * dt;
    // chão e as duas tábuas
    var apoio = game.chao;
    if (position.x > 700 && position.x < 920 && position.y - vy * dt <= game.chao - 160) apoio = game.chao - 160;
    if (position.x > 1300 && position.x < 1520 && position.y - vy * dt <= game.chao - 260) apoio = game.chao - 260;
    if (vy > 0 && position.y >= apoio) {
      if (!noChao && vy > 900) game.tremer(0.35); // aterrissagem forte sacode a tela
      position.y = apoio;
      vy = 0;
      noChao = true;
    }
  }
}

class Arvore extends PositionComponent {
  Arvore(Vector2 base) : super(position: base, size: Vector2(60, 150), anchor: Anchor.bottomCenter);

  @override
  void render(Canvas canvas) {
    canvas.drawRect(const Rect.fromLTWH(24, 70, 12, 80), Paint()..color = const Color(0xFF7B4F2C));
    canvas.drawCircle(const Offset(30, 50), 40, Paint()..color = const Color(0xFF2E7D32));
  }
}

// mostra o retângulo da zona morta quando esse modo está ligado
class Moldura extends PositionComponent with HasGameReference<Passeio> {
  @override
  void render(Canvas canvas) {
    if (game.modo != 3) return;
    final c = game.size / 2;
    canvas.drawRect(
      Rect.fromCenter(center: Offset(c.x, c.y + 68), width: game.zonaMorta * 2 + 64, height: 184),
      Paint()
        ..color = Colors.white70
        ..style = PaintingStyle.stroke
        ..strokeWidth = 2,
    );
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
