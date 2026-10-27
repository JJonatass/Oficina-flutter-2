import 'dart:math';
import 'package:flame/components.dart';
import 'package:flame/events.dart';
import 'package:flame/game.dart';
import 'package:flutter/material.dart';

void main() => runApp(GameWidget(game: Voo()));

// DESAFIO · CARAMELO VOADOR (Flame)
// 1. O caramelo cai com gravidade; cada toque na tela dá um impulso para cima.
// 2. A cada 1,5 segundo nascem dois canos (um em cima, um embaixo) com um vão sorteado entre eles.
// 3. Os canos andam para a esquerda e saem do jogo quando passam da borda.
// 4. Passar por um par de canos vale 1 ponto (mostre num TextComponent).
// 5. Encostar num cano ou sair da tela termina o jogo; tocar de novo recomeça.
// O caramelo animado, o toque, o placar e a criação dos canos já estão prontos.
// Complete as partes marcadas com FAÇA.

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
    // FAÇA 2: acrescente ao jogo um TimerComponent com period: 1.5 e repeat: true
    // que chama novosCanos a cada tique (onTick: novosCanos).
  }

  // cria um par de canos com um vão sorteado entre eles
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
    // FAÇA 3 (parte 1): some 1 aos pontos e mostre no placar: placar.text = 'Pontos: $pontos'.
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
    // FAÇA 1: a gravidade aumenta a velocidade a cada quadro (some gravidade * dt à velocidade).
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
    // FAÇA 3 (parte 2): se o retângulo do caramelo (game.caramelo.toRect(), um pouco encolhido com deflate(10))
    // encostar no retângulo deste cano (toRect()), chame game.perdeu().
    if (deCima && !contou && position.x + size.x < game.caramelo.position.x) {
      contou = true;
      game.marcou();
    }
  }
}
