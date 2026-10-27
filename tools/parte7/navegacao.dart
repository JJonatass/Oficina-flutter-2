import 'dart:math';
import 'package:flame/components.dart';
import 'package:flame/events.dart';
import 'package:flame/game.dart';
import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(debugShowCheckedModeBanner: false, home: Menu()));

const int totalFases = 3;

// Tela 1: o menu principal
class Menu extends StatelessWidget {
  const Menu({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF1E2A3A),
      body: Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Text('Caramelo', style: TextStyle(fontSize: 40, color: Colors.amber, fontWeight: FontWeight.bold)),
            const Text('pega-ossos', style: TextStyle(fontSize: 18, color: Colors.white70)),
            const SizedBox(height: 32),
            FilledButton(
              onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (context) => const Fases())),
              child: const Text('Jogar'),
            ),
            const SizedBox(height: 12),
            OutlinedButton(
              onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (context) => const Creditos())),
              child: const Text('Créditos'),
            ),
          ],
        ),
      ),
    );
  }
}

// Tela 2: escolher a fase
class Fases extends StatelessWidget {
  const Fases({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Escolha a fase')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            for (int n = 1; n <= totalFases; n++)
              Card(
                child: ListTile(
                  leading: CircleAvatar(child: Text('$n')),
                  title: Text('Fase $n'),
                  subtitle: Text('${4 + n * 2} ossos em ${12 - n} segundos'),
                  trailing: const Icon(Icons.play_arrow),
                  onTap: () => Navigator.push(context, MaterialPageRoute(builder: (context) => TelaJogo(fase: n))),
                ),
              ),
          ],
        ),
      ),
    );
  }
}

// Tela 3: créditos
class Creditos extends StatelessWidget {
  const Creditos({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Créditos')),
      body: const Padding(
        padding: EdgeInsets.all(24),
        child: Text('Programação: você\nArte: Oficina Flutter 2\nSons: sintetizados no navegador\n\nObrigado por jogar!', style: TextStyle(fontSize: 18)),
      ),
    );
  }
}

// Tela 4: o jogo, com as janelas de pausa e de fim por cima
class TelaJogo extends StatelessWidget {
  final int fase;
  const TelaJogo({super.key, required this.fase});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: GameWidget(
        game: PegaOssos(fase),
        overlayBuilderMap: {
          'pausa': (context, PegaOssos jogo) => Janela(
                titulo: 'Pausa',
                botoes: [
                  FilledButton(onPressed: jogo.continuar, child: const Text('Continuar')),
                  OutlinedButton(onPressed: () => Navigator.pop(context), child: const Text('Sair da fase')),
                ],
              ),
          'fim': (context, PegaOssos jogo) => Janela(
                titulo: jogo.venceu ? 'Fase $fase completa!' : 'O tempo acabou',
                botoes: [
                  if (jogo.venceu && fase < totalFases)
                    FilledButton(
                      onPressed: () => Navigator.pushReplacement(context, MaterialPageRoute(builder: (context) => TelaJogo(fase: fase + 1))),
                      child: const Text('Próxima fase'),
                    ),
                  if (!jogo.venceu)
                    FilledButton(
                      onPressed: () => Navigator.pushReplacement(context, MaterialPageRoute(builder: (context) => TelaJogo(fase: fase))),
                      child: const Text('Tentar de novo'),
                    ),
                  OutlinedButton(onPressed: () => Navigator.pop(context), child: const Text('Escolher fase')),
                ],
              ),
        },
      ),
    );
  }
}

class Janela extends StatelessWidget {
  final String titulo;
  final List<Widget> botoes;
  const Janela({super.key, required this.titulo, required this.botoes});

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Card(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Text(titulo, style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
              const SizedBox(height: 16),
              for (final b in botoes) Padding(padding: const EdgeInsets.only(top: 8), child: b),
            ],
          ),
        ),
      ),
    );
  }
}

class PegaOssos extends FlameGame {
  final int fase;
  PegaOssos(this.fase);

  late TextComponent placar;
  late double tempo;
  late int faltam;
  bool venceu = false;
  final sorteio = Random();

  @override
  Color backgroundColor() => const Color(0xFF7EC8E3);

  @override
  Future<void> onLoad() async {
    tempo = 12.0 - fase;
    faltam = 4 + fase * 2;
    placar = TextComponent(text: '', position: Vector2(16, 16), textRenderer: TextPaint(style: const TextStyle(fontSize: 18, color: Colors.white)));
    add(placar);
    add(BotaoPausa());
    novoOsso();
  }

  void novoOsso() {
    add(Osso(Vector2(40 + sorteio.nextDouble() * (size.x - 80), 90 + sorteio.nextDouble() * (size.y - 160))));
  }

  void pegou() {
    faltam--;
    if (faltam == 0) {
      terminar(true);
    } else {
      novoOsso();
    }
  }

  void terminar(bool ganhou) {
    venceu = ganhou;
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
  void update(double dt) {
    super.update(dt);
    tempo -= dt;
    placar.text = 'Fase $fase   Ossos: $faltam   Tempo: ${max(0, tempo).toStringAsFixed(1)}';
    if (tempo <= 0) terminar(false);
  }
}

class Osso extends SpriteAnimationComponent with TapCallbacks, HasGameReference<PegaOssos> {
  Osso(Vector2 onde) : super(position: onde, size: Vector2.all(48), anchor: Anchor.center);

  @override
  Future<void> onLoad() async {
    animation = await game.loadSpriteAnimation(
      'osso.png',
      SpriteAnimationData.sequenced(amount: 6, stepTime: 0.1, textureSize: Vector2.all(16)),
    );
  }

  @override
  void onTapDown(TapDownEvent event) {
    removeFromParent();
    game.pegou();
  }
}

class BotaoPausa extends PositionComponent with TapCallbacks, HasGameReference<PegaOssos> {
  BotaoPausa() : super(size: Vector2.all(44));

  @override
  Future<void> onLoad() async {
    position = Vector2(game.size.x - 56, 8);
  }

  @override
  void render(Canvas canvas) {
    final tinta = Paint()..color = Colors.white;
    canvas.drawRRect(RRect.fromRectAndRadius(size.toRect(), const Radius.circular(10)), Paint()..color = Colors.black26);
    canvas.drawRect(const Rect.fromLTWH(14, 12, 6, 20), tinta);
    canvas.drawRect(const Rect.fromLTWH(24, 12, 6, 20), tinta);
  }

  @override
  void onTapDown(TapDownEvent event) {
    game.pausar();
  }
}
