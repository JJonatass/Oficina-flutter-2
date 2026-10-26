import 'dart:math';
import 'package:flutter/material.dart';
import 'package:flutter/scheduler.dart';
import 'package:audioplayers/audioplayers.dart';

void main() => runApp(const MaterialApp(home: Suco()));

class Faisca {
  Offset posicao;
  Offset velocidade;
  double vida = 0.6;
  Faisca(this.posicao, this.velocidade);
}

class Suco extends StatefulWidget {
  const Suco({super.key});
  @override
  State<Suco> createState() => _SucoState();
}

class _SucoState extends State<Suco> with SingleTickerProviderStateMixin {
  final sorteio = Random();
  final som = AudioPlayer();
  late Ticker ticker;
  Duration anterior = Duration.zero;
  bool comSuco = true;

  double tremida = 0;
  double esmaga = 0;
  double flash = 0;
  final faiscas = <Faisca>[];
  int toques = 0;

  double forcaTremida = 10;

  @override
  void initState() {
    super.initState();
    ticker = createTicker(quadro)..start();
  }

  void quadro(Duration agora) {
    final dt = (agora - anterior).inMicroseconds / 1000000;
    anterior = agora;
    if (dt <= 0 || dt > 0.1) return;
    setState(() {
      // tudo o que o toque provocou vai voltando ao normal aos poucos
      tremida = max(0, tremida - dt * 2.5);
      esmaga = max(0, esmaga - dt * 3);
      flash = max(0, flash - dt * 4);
      for (final f in faiscas) {
        f.posicao += f.velocidade * dt;
        f.velocidade += const Offset(0, 600) * dt;
        f.vida -= dt;
      }
      faiscas.removeWhere((f) => f.vida <= 0);
    });
  }

  void bater() {
    setState(() {
      toques++;
      if (!comSuco) return;
      tremida = 1;
      esmaga = 1;
      flash = 1;
      som.play(AssetSource('sons/batida.wav'));
      for (var i = 0; i < 14; i++) {
        final a = sorteio.nextDouble() * 2 * pi;
        final v = 120 + sorteio.nextDouble() * 220;
        faiscas.add(Faisca(const Offset(180, 330), Offset(cos(a), sin(a) - 0.8) * v));
      }
    });
  }

  @override
  void dispose() {
    ticker.dispose();
    som.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final deslocamento = Offset((sorteio.nextDouble() - 0.5), (sorteio.nextDouble() - 0.5)) * forcaTremida * tremida * 2;
    return Scaffold(
      appBar: AppBar(title: Text('Toques: $toques')),
      body: Column(children: [
        SwitchListTile(title: const Text('Com suco (tremida, esmagar, faíscas, flash e som)'), value: comSuco, onChanged: (v) => setState(() => comSuco = v)),
        GestureDetector(
          onTapDown: (_) => bater(),
          child: CustomPaint(size: const Size(360, 480), painter: Palco(deslocamento, esmaga, flash, faiscas)),
        ),
      ]),
    );
  }
}

class Palco extends CustomPainter {
  final Offset deslocamento;
  final double esmaga;
  final double flash;
  final List<Faisca> faiscas;
  Palco(this.deslocamento, this.esmaga, this.flash, this.faiscas);

  @override
  void paint(Canvas canvas, Size size) {
    canvas.drawRect(Rect.fromLTWH(0, 0, size.width, size.height), Paint()..color = const Color(0xFF1D1B33));
    canvas.save();
    canvas.translate(deslocamento.dx, deslocamento.dy);
    canvas.drawRect(const Rect.fromLTWH(0, 380, 360, 100), Paint()..color = const Color(0xFF3E6B3A));
    // esmagar e esticar: mais largo e mais baixo no impacto, mantendo a base no chão
    final largura = 90 * (1 + 0.35 * esmaga);
    final altura = 90 * (1 - 0.3 * esmaga);
    final caixa = Rect.fromLTWH(180 - largura / 2, 380 - altura, largura, altura);
    canvas.drawRRect(RRect.fromRectAndRadius(caixa, const Radius.circular(10)), Paint()..color = Color.lerp(const Color(0xFFD68C3E), Colors.white, flash * 0.8)!);
    for (final f in faiscas) {
      canvas.drawCircle(f.posicao, 4 * f.vida / 0.6 + 1, Paint()..color = Colors.amber);
    }
    canvas.restore();
    final dica = TextPainter(
      text: const TextSpan(text: 'Toque na tela', style: TextStyle(color: Colors.white54, fontSize: 16)),
      textDirection: TextDirection.ltr,
    )..layout();
    dica.paint(canvas, Offset((size.width - dica.width) / 2, 40));
  }

  @override
  bool shouldRepaint(covariant Palco antigo) => true;
}
