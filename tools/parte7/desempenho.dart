import 'dart:math';
import 'package:flame/components.dart';
import 'package:flame/events.dart';
import 'package:flame/game.dart';
import 'package:flame/input.dart';
import 'package:flutter/material.dart';

void main() => runApp(GameWidget(game: Chuva()));

class Chuva extends FlameGame {
  final sorteio = Random();
  late Sprite ossoSprite;
  late TextComponent painel;
  // ossos que caíram e estão guardados esperando para voltar (o "pool")
  final List<Osso> guardados = [];
  bool usarPool = true;
  int porSegundo = 60;
  double acumulado = 0;
  int criados = 0;
  int reaproveitados = 0;
  int naTela = 0;
  // últimos tempos de quadro, para a média de quadros por segundo
  final List<double> tempos = [];

  @override
  Color backgroundColor() => const Color(0xFF203040);

  @override
  Future<void> onLoad() async {
    ossoSprite = await loadSprite('osso.png', srcSize: Vector2.all(16));
    add(RectangleComponent(size: Vector2(size.x, 96), paint: Paint()..color = Colors.black87, priority: 9));
    painel = TextComponent(text: '', position: Vector2(12, 12), priority: 10, textRenderer: TextPaint(style: const TextStyle(fontSize: 15, color: Colors.white)));
    add(painel);
    add(BotaoTexto('Pool', Vector2(12, size.y - 60), () => usarPool = !usarPool));
    add(BotaoTexto('− 30', Vector2(130, size.y - 60), () => porSegundo = max(0, porSegundo - 30)));
    add(BotaoTexto('+ 30', Vector2(248, size.y - 60), () => porSegundo += 30));
  }

  Osso pegarOsso() {
    if (usarPool && guardados.isNotEmpty) {
      reaproveitados++;
      return guardados.removeLast();
    }
    criados++;
    return Osso(ossoSprite);
  }

  void soltar() {
    final o = pegarOsso();
    o.position = Vector2(sorteio.nextDouble() * size.x, -20);
    o.velocidade = 120 + sorteio.nextDouble() * 220;
    o.angle = sorteio.nextDouble() * 6;
    add(o);
    naTela++;
  }

  void caiu(Osso o) {
    o.removeFromParent();
    naTela--;
    if (usarPool) guardados.add(o);
  }

  @override
  void update(double dt) {
    super.update(dt);
    acumulado += porSegundo * dt;
    while (acumulado >= 1) {
      acumulado -= 1;
      soltar();
    }
    tempos.add(dt);
    if (tempos.length > 30) tempos.removeAt(0);
    final media = tempos.reduce((a, b) => a + b) / tempos.length;
    final fps = media > 0 ? 1 / media : 0;
    painel.text = 'FPS: ${fps.toStringAsFixed(0)}   ossos/s: $porSegundo\n'
        'na tela: $naTela   guardados: ${guardados.length}\n'
        'criados: $criados   reaproveitados: $reaproveitados\n'
        'pool: ${usarPool ? 'ligado' : 'desligado'}';
  }
}

class Osso extends SpriteComponent with HasGameReference<Chuva> {
  double velocidade = 0;
  Osso(Sprite s) : super(sprite: s, size: Vector2.all(28), anchor: Anchor.center);

  @override
  void update(double dt) {
    super.update(dt);
    position.y += velocidade * dt;
    angle += 2 * dt;
    if (position.y > game.size.y + 20) game.caiu(this);
  }
}

class BotaoTexto extends PositionComponent with TapCallbacks {
  final String rotulo;
  final void Function() acao;
  BotaoTexto(this.rotulo, Vector2 onde, this.acao) : super(position: onde, size: Vector2(104, 44), priority: 10);

  @override
  void render(Canvas canvas) {
    canvas.drawRRect(RRect.fromRectAndRadius(size.toRect(), const Radius.circular(10)), Paint()..color = const Color(0xFF41566E));
    final tp = TextPainter(text: TextSpan(text: rotulo, style: const TextStyle(fontSize: 18, color: Colors.white)), textDirection: TextDirection.ltr)..layout();
    tp.paint(canvas, Offset((size.x - tp.width) / 2, (size.y - tp.height) / 2));
  }

  @override
  void onTapDown(TapDownEvent event) {
    acao();
  }
}
