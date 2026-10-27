import 'dart:math';
import 'package:flame/components.dart';
import 'package:flame/events.dart';
import 'package:flame/game.dart';
import 'package:flutter/material.dart';

void main() => runApp(GameWidget(game: Voo()));

class Voo extends FlameGame with TapCallbacks {
  final sorteio = Random();
  late Caramelo caramelo;
  late TextComponent placar;
  int pontos = 0;
  bool jogando = false;
  final double vao = 190;

  @override
  Color backgroundColor() => const Color(0xFF8FD3F4);

  @override
  Future<void> onLoad() async {
    caramelo = Caramelo();
    add(caramelo);
    placar = TextComponent(text: 'Toque para voar', position: Vector2(16, 16), priority: 10);
    add(placar);
    add(TimerComponent(period: 1.5, repeat: true, onTick: novosCanos));
  }

  void novosCanos() {
    if (!jogando) return;
    final topo = 80 + sorteio.nextDouble() * (size.y - vao - 160);
    add(Cano(Vector2(size.x, 0), Vector2(60, topo), true));
    add(Cano(Vector2(size.x, topo + vao), Vector2(60, size.y - topo - vao), false));
  }

  @override
  void onTapDown(TapDownEvent event) {
    if (!jogando) {
      jogando = true;
      pontos = 0;
      placar.text = 'Pontos: 0';
      children.whereType<Cano>().toList().forEach((c) => c.removeFromParent());
      caramelo.position = Vector2(100, size.y / 2);
      caramelo.velocidade = 0;
    }
    caramelo.velocidade = -360;
  }

  void marcou() {
    pontos++;
    placar.text = 'Pontos: $pontos';
  }

  void perdeu() {
    jogando = false;
    placar.text = 'Fim! $pontos pontos. Toque para recomeçar.';
  }
}

class Caramelo extends SpriteAnimationComponent with HasGameReference<Voo> {
  Caramelo() : super(size: Vector2.all(48), anchor: Anchor.center);
  double velocidade = 0;
  final double gravidade = 900;

  @override
  Future<void> onLoad() async {
    position = Vector2(100, game.size.y / 2);
    animation = await game.loadSpriteAnimation('heroi.png', SpriteAnimationData.sequenced(amount: 4, stepTime: 0.1, textureSize: Vector2.all(16)));
  }

  @override
  void update(double dt) {
    super.update(dt);
    if (!game.jogando) return;
    velocidade += gravidade * dt;
    position.y += velocidade * dt;
    angle = (velocidade / 900).clamp(-0.5, 0.8).toDouble();
    if (position.y < 0 || position.y > game.size.y) game.perdeu();
  }
}

class Cano extends RectangleComponent with HasGameReference<Voo> {
  final bool deCima;
  bool contou = false;
  Cano(Vector2 onde, Vector2 tamanho, this.deCima) : super(position: onde, size: tamanho, paint: Paint()..color = const Color(0xFF3FA34D));

  @override
  void update(double dt) {
    super.update(dt);
    if (!game.jogando) return;
    position.x -= 160 * dt;
    if (position.x + size.x < 0) removeFromParent();
    final corpo = game.caramelo.toRect().deflate(10);
    if (corpo.overlaps(toRect())) game.perdeu();
    if (deCima && !contou && position.x + size.x < game.caramelo.position.x) {
      contou = true;
      game.marcou();
    }
  }
}
