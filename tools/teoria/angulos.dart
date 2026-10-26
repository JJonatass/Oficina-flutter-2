import 'dart:math';
import 'package:flutter/material.dart';
import 'package:flutter/scheduler.dart';

void main() => runApp(const MaterialApp(home: Angulos()));

class Tiro {
  Offset posicao;
  final Offset velocidade;
  Tiro(this.posicao, this.velocidade);
}

class Angulos extends StatefulWidget {
  const Angulos({super.key});
  @override
  State<Angulos> createState() => _AngulosState();
}

class _AngulosState extends State<Angulos> with SingleTickerProviderStateMixin {
  late Ticker ticker;
  Duration anterior = Duration.zero;
  double tempo = 0;
  Offset dedo = const Offset(260, 200);
  final tiros = <Tiro>[];

  static const canhao = Offset(180, 520);
  double raioOrbita = 80;
  double velocidadeTiro = 300;

  double get angulo => atan2(dedo.dy - canhao.dy, dedo.dx - canhao.dx);

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
      for (final t in tiros) {
        t.posicao += t.velocidade * dt;
      }
      tiros.removeWhere((t) => t.posicao.dy < -20 || t.posicao.dx < -20 || t.posicao.dx > 380);
    });
  }

  void atirar() {
    final direcao = Offset(cos(angulo), sin(angulo));
    tiros.add(Tiro(canhao + direcao * 40, direcao * velocidadeTiro));
  }

  @override
  void dispose() {
    ticker.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final graus = angulo * 180 / pi;
    return Scaffold(
      appBar: AppBar(title: Text('ângulo: ${graus.toStringAsFixed(0)}°  (${angulo.toStringAsFixed(2)} rad)')),
      body: GestureDetector(
        onPanUpdate: (e) => setState(() => dedo = e.localPosition),
        onTapDown: (e) => setState(() {
          dedo = e.localPosition;
          atirar();
        }),
        child: CustomPaint(size: const Size(360, 560), painter: Cena(tempo, angulo, raioOrbita, tiros, dedo)),
      ),
    );
  }
}

class Cena extends CustomPainter {
  final double tempo;
  final double angulo;
  final double raioOrbita;
  final List<Tiro> tiros;
  final Offset dedo;
  Cena(this.tempo, this.angulo, this.raioOrbita, this.tiros, this.dedo);

  @override
  void paint(Canvas canvas, Size size) {
    canvas.drawRect(Rect.fromLTWH(0, 0, size.width, size.height), Paint()..color = const Color(0xFF0B1026));
    // órbita: x = centro + cos(t) * raio, y = centro + sin(t) * raio
    const sol = Offset(100, 130);
    canvas.drawCircle(sol, raioOrbita, Paint()..color = Colors.white24..style = PaintingStyle.stroke);
    canvas.drawCircle(sol, 22, Paint()..color = Colors.amber);
    final lua = sol + Offset(cos(tempo), sin(tempo)) * raioOrbita;
    canvas.drawLine(sol, lua, Paint()..color = Colors.white30);
    canvas.drawLine(sol, Offset(lua.dx, sol.dy), Paint()..color = Colors.redAccent..strokeWidth = 2);
    canvas.drawLine(Offset(lua.dx, sol.dy), lua, Paint()..color = Colors.lightGreenAccent..strokeWidth = 2);
    canvas.drawCircle(lua, 10, Paint()..color = Colors.white);

    // canhão que mira o dedo: rotate gira tudo o que vem depois
    const canhao = Offset(180, 520);
    canvas.save();
    canvas.translate(canhao.dx, canhao.dy);
    canvas.rotate(angulo);
    canvas.drawRRect(RRect.fromRectAndRadius(const Rect.fromLTWH(0, -8, 44, 16), const Radius.circular(4)), Paint()..color = Colors.blueGrey.shade200);
    canvas.restore();
    canvas.drawCircle(canhao, 18, Paint()..color = const Color(0xFFD68C3E));
    canvas.drawLine(canhao, dedo, Paint()..color = Colors.white12);
    for (final t in tiros) {
      canvas.drawCircle(t.posicao, 6, Paint()..color = const Color(0xFFFAF4E2));
    }
  }

  @override
  bool shouldRepaint(covariant Cena antiga) => true;
}
