import 'dart:math';
import 'package:flutter/material.dart';
import 'package:flutter/scheduler.dart';

void main() => runApp(const MaterialApp(home: Jogo()));

const int quantidade = __N__;

class Bola {
  double x;
  double y;
  double vx;
  double vy;
  Bola(this.x, this.y, this.vx, this.vy);
}

class Cena extends CustomPainter {
  final List<Bola> bolas;
  Cena(this.bolas);

  @override
  void paint(Canvas canvas, Size size) {
    canvas.drawRect(Rect.fromLTWH(0, 0, size.width, size.height), Paint()..color = Colors.black);
    final tinta = Paint()..color = Colors.amber;
    for (final b in bolas) {
      canvas.drawCircle(Offset(b.x, b.y), 5, tinta);
    }
  }

  @override
  bool shouldRepaint(covariant Cena antiga) => true;
}

class Jogo extends StatefulWidget {
  const Jogo({super.key});

  @override
  State<Jogo> createState() => _JogoState();
}

class _JogoState extends State<Jogo> with SingleTickerProviderStateMixin {
  late Ticker ticker;
  final sorteio = Random();
  List<Bola> bolas = [];
  double ultimo = 0;
  int quadros = 0;
  double janela = 0;
  int fps = 0;

  @override
  void initState() {
    super.initState();
    for (int i = 0; i < quantidade; i++) {
      bolas.add(Bola(sorteio.nextDouble() * 360, sorteio.nextDouble() * 500, sorteio.nextDouble() * 200 - 100, sorteio.nextDouble() * 200 - 100));
    }
    ticker = createTicker(quadro);
    ticker.start();
  }

  void quadro(Duration tempo) {
    final agora = tempo.inMicroseconds / 1000000;
    final dt = agora - ultimo;
    ultimo = agora;
    quadros++;
    janela += dt;
    if (janela >= 1) {
      fps = quadros;
      quadros = 0;
      janela = 0;
    }
    setState(() {
      for (final b in bolas) {
        b.x += b.vx * dt;
        b.y += b.vy * dt;
        if (b.x < 0 || b.x > 360) b.vx = -b.vx;
        if (b.y < 0 || b.y > 500) b.vy = -b.vy;
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('$fps fps · $quantidade bolas')),
      body: Center(
        child: CustomPaint(size: const Size(360, 500), painter: Cena(bolas)),
      ),
    );
  }
}
