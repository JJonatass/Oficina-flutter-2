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
// Dicas: TapCallbacks no jogo, TimerComponent(period: 1.5, repeat: true, onTick: ...), toRect().overlaps(...).

class Voo extends FlameGame with TapCallbacks {
  @override
  Color backgroundColor() => const Color(0xFF8FD3F4);

  @override
  Future<void> onLoad() async {
    add(TextComponent(text: 'Toque para voar', position: size / 2, anchor: Anchor.center));
  }
}
