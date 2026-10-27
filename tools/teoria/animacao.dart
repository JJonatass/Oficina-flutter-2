import 'dart:math';
import 'package:flutter/material.dart';
import 'package:flutter/scheduler.dart';

void main() => runApp(const MaterialApp(home: Quique()));

class Quique extends StatefulWidget {
  const Quique({super.key});
  @override
  State<Quique> createState() => _QuiqueState();
}

class _QuiqueState extends State<Quique> with SingleTickerProviderStateMixin {
  late Ticker ticker;
  Duration anterior = Duration.zero;
  double tempo = 0;
  double exagero = 0.6;
  double periodo = 1.2;
  bool rastro = true;

  @override
  void initState() {
    super.initState();
    ticker = createTicker(quadro)..start();
  }

  void quadro(Duration agora) {
    final dt = (agora - anterior).inMicroseconds / 1000000;
    anterior = agora;
    if (dt <= 0 || dt > 0.1) return;
    setState(() => tempo += dt);
  }

  @override
  void dispose() {
    ticker.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Exagero: ${(exagero * 100).round()}%')),
      body: Column(children: [
        Slider(value: exagero, onChanged: (v) => setState(() => exagero = v)),
        SwitchListTile(title: const Text('Mostrar o rastro dos quadros'), value: rastro, onChanged: (v) => setState(() => rastro = v)),
        CustomPaint(size: const Size(360, 420), painter: Bola(tempo, periodo, exagero, rastro)),
      ]),
    );
  }
}

// Onde a bola está e como está deformada num instante t (de 0 a 1 no ciclo do pulo)
class Pose {
  final double altura;
  final double largura;
  final double alta;
  Pose(this.altura, this.largura, this.alta);
}

Pose pose(double t, double exagero) {
  // parábola: no chão em t = 0 e t = 1, no alto em t = 0.5
  final altura = 4 * t * (1 - t);
  // perto do chão, a bola esmaga (mais larga e mais baixa); no ar, estica na direção do movimento
  final chao = max(0.0, 1 - min(t, 1 - t) / 0.08);
  final rapidez = (1 - 2 * t).abs();
  final estica = 1 + exagero * 0.35 * rapidez * (1 - chao);
  final esmaga = 1 - exagero * 0.45 * chao;
  return Pose(altura, 1 / (estica * esmaga), estica * esmaga);
}

class Bola extends CustomPainter {
  final double tempo;
  final double periodo;
  final double exagero;
  final bool rastro;
  Bola(this.tempo, this.periodo, this.exagero, this.rastro);

  void desenhar(Canvas canvas, double t, double x, Color cor) {
    final p = pose(t, exagero);
    const raio = 30.0;
    const chao = 380.0;
    final w = raio * 2 * p.largura;
    final h = raio * 2 * p.alta;
    final centro = Offset(x, chao - h / 2 - p.altura * 260);
    canvas.drawOval(Rect.fromCenter(center: centro, width: w, height: h), Paint()..color = cor);
  }

  // a bola também vai e volta na horizontal, para o rastro mostrar o arco
  double lado(double t) => 180 + 120 * sin(2 * pi * t / (periodo * 3));

  @override
  void paint(Canvas canvas, Size size) {
    canvas.drawRect(Rect.fromLTWH(0, 0, size.width, size.height), Paint()..color = const Color(0xFF1D1B33));
    canvas.drawRect(const Rect.fromLTWH(0, 380, 360, 40), Paint()..color = const Color(0xFF3E6B3A));
    final t = (tempo % periodo) / periodo;
    if (rastro) {
      // os quadros anteriores, cada vez mais apagados: mostram o espaçamento entre as poses
      for (var k = 1; k <= 6; k++) {
        final antes = tempo - k * 0.05;
        desenhar(canvas, (antes % periodo) / periodo, lado(antes), Colors.white.withOpacity(0.08 * (7 - k)));
      }
    }
    desenhar(canvas, t, lado(tempo), const Color(0xFFD68C3E));
  }

  @override
  bool shouldRepaint(covariant Bola antiga) => true;
}
