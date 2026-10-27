import 'dart:math';
import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(debugShowCheckedModeBanner: false, home: Fractal()));

class Fractal extends StatefulWidget {
  const Fractal({super.key});

  @override
  State<Fractal> createState() => _FractalState();
}

class _FractalState extends State<Fractal> {
  double profundidade = 6;
  double abertura = 0.45; // ângulo entre os dois galhos, em radianos
  final double encolhe = 0.72; // cada galho filho tem 72% do tamanho do pai

  @override
  Widget build(BuildContext context) {
    final niveis = profundidade.round();
    // 1 + 2 + 4 + ... : cada chamada faz mais duas
    final galhos = pow(2, niveis + 1).toInt() - 1;
    return Scaffold(
      appBar: AppBar(title: Text('$niveis níveis · $galhos galhos')),
      body: Column(
        children: [
          CustomPaint(size: const Size(360, 380), painter: Arvore(niveis, abertura, encolhe)),
          Row(children: [
            const SizedBox(width: 110, child: Text('Profundidade')),
            Expanded(child: Slider(value: profundidade, min: 0, max: 10, divisions: 10, onChanged: (v) => setState(() => profundidade = v))),
          ]),
          Row(children: [
            const SizedBox(width: 110, child: Text('Abertura')),
            Expanded(child: Slider(value: abertura, min: 0.1, max: 1.2, onChanged: (v) => setState(() => abertura = v))),
          ]),
        ],
      ),
    );
  }
}

class Arvore extends CustomPainter {
  final int niveis;
  final double abertura;
  final double encolhe;
  Arvore(this.niveis, this.abertura, this.encolhe);

  // RECURSÃO: galho desenha um traço e chama a si mesma duas vezes, com galhos menores.
  // O caso base (resta == 0) é o que faz a repetição parar.
  void galho(Canvas canvas, Offset base, double tamanho, double angulo, int resta) {
    final ponta = base + Offset(cos(angulo), sin(angulo)) * tamanho;
    canvas.drawLine(
      base,
      ponta,
      Paint()
        ..color = resta <= 1 ? const Color(0xFF66BB6A) : const Color(0xFF7B4F2C)
        ..strokeWidth = resta + 1.0,
    );
    if (resta == 0) return; // caso base: folha, sem mais galhos
    galho(canvas, ponta, tamanho * encolhe, angulo - abertura, resta - 1);
    galho(canvas, ponta, tamanho * encolhe, angulo + abertura, resta - 1);
  }

  @override
  void paint(Canvas canvas, Size size) {
    canvas.drawRect(Rect.fromLTWH(0, 0, size.width, size.height), Paint()..color = const Color(0xFFE3F2FD));
    galho(canvas, Offset(size.width / 2, size.height), 95, -pi / 2, niveis);
  }

  @override
  bool shouldRepaint(Arvore old) => true;
}
