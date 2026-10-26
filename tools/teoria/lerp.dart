import 'dart:math';
import 'dart:ui' as ui;
import 'package:flutter/material.dart';
import 'package:flutter/scheduler.dart';

void main() => runApp(const MaterialApp(home: Suave()));

double linear(double t) => t;
double acelera(double t) => t * t;
double freia(double t) => 1 - (1 - t) * (1 - t);
double suave(double t) => t * t * (3 - 2 * t);

class Suave extends StatefulWidget {
  const Suave({super.key});
  @override
  State<Suave> createState() => _SuaveState();
}

class _SuaveState extends State<Suave> with SingleTickerProviderStateMixin {
  late Ticker ticker;
  Duration anterior = Duration.zero;
  double tempo = 0;
  double duracao = 2;
  Offset alvo = const Offset(180, 460);
  Offset seguidor = const Offset(180, 460);

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
      tempo += dt;
      // a cada quadro, anda uma fração do que falta: rápido longe, devagar perto
      final fracao = 1 - pow(0.02, dt).toDouble();
      seguidor = Offset.lerp(seguidor, alvo, fracao)!;
    });
  }

  @override
  void dispose() {
    ticker.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final t = (tempo % duracao) / duracao;
    return Scaffold(
      appBar: AppBar(title: Text('t = ${t.toStringAsFixed(2)}')),
      body: GestureDetector(
        onPanDown: (e) => setState(() => alvo = e.localPosition),
        onPanUpdate: (e) => setState(() => alvo = e.localPosition),
        child: CustomPaint(size: const Size(360, 560), painter: Curvas(t, alvo, seguidor)),
      ),
    );
  }
}

class Curvas extends CustomPainter {
  final double t;
  final Offset alvo;
  final Offset seguidor;
  Curvas(this.t, this.alvo, this.seguidor);

  @override
  void paint(Canvas canvas, Size size) {
    canvas.drawRect(Rect.fromLTWH(0, 0, size.width, size.height), Paint()..color = const Color(0xFF1D1B33));
    const inicio = 40.0;
    const fim = 320.0;
    final curvas = [linear, acelera, freia, suave];
    final nomes = ['linear', 'acelera (t²)', 'freia', 'suave'];
    final cores = [Colors.white, Colors.redAccent, Colors.lightGreenAccent, Colors.amber];
    for (var i = 0; i < 4; i++) {
      final y = 50.0 + i * 70;
      canvas.drawLine(Offset(inicio, y), Offset(fim, y), Paint()..color = Colors.white12..strokeWidth = 2);
      // lerp: começo + (fim - começo) * curva(t)
      final x = ui.lerpDouble(inicio, fim, curvas[i](t))!;
      canvas.drawCircle(Offset(x, y), 12, Paint()..color = cores[i]);
      final nome = TextPainter(
        text: TextSpan(text: nomes[i], style: TextStyle(color: cores[i], fontSize: 13)),
        textDirection: TextDirection.ltr,
      )..layout();
      nome.paint(canvas, Offset(inicio, y + 14));
    }
    canvas.drawCircle(alvo, 8, Paint()..color = Colors.white38);
    canvas.drawCircle(seguidor, 16, Paint()..color = const Color(0xFFD68C3E));
  }

  @override
  bool shouldRepaint(covariant Curvas antiga) => true;
}
