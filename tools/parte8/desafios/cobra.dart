import 'dart:async';
import 'dart:math';
import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(debugShowCheckedModeBanner: false, home: Cobrinha()));

const int colunas = 15;
const int linhas = 20;
const double lado = 22;

class Cobrinha extends StatefulWidget {
  const Cobrinha({super.key});

  @override
  State<Cobrinha> createState() => _CobrinhaState();
}

class _CobrinhaState extends State<Cobrinha> {
  final sorteio = Random();
  List<Offset> corpo = [];
  Offset direcao = const Offset(1, 0);
  Offset proxima = const Offset(1, 0);
  Offset osso = const Offset(10, 10);
  int pontos = 0;
  bool perdeu = false;
  Timer? relogio;

  @override
  void initState() {
    super.initState();
    comecar();
  }

  void comecar() {
    relogio?.cancel();
    setState(() {
      corpo = [const Offset(5, 10), const Offset(4, 10), const Offset(3, 10)];
      direcao = const Offset(1, 0);
      proxima = direcao;
      pontos = 0;
      perdeu = false;
      novoOsso();
    });
    relogio = Timer.periodic(const Duration(milliseconds: 200), (t) => andar());
  }

  void novoOsso() {
    do {
      osso = Offset(sorteio.nextInt(colunas).toDouble(), sorteio.nextInt(linhas).toDouble());
    } while (corpo.contains(osso));
  }

  // não deixa virar 180 graus de uma vez
  void virar(Offset nova) {
    if (nova + direcao != Offset.zero) proxima = nova;
  }

  void andar() {
    setState(() {
      direcao = proxima;
      final cabeca = corpo.first + direcao;
      final fora = cabeca.dx < 0 || cabeca.dy < 0 || cabeca.dx >= colunas || cabeca.dy >= linhas;
      if (fora || corpo.contains(cabeca)) {
        perdeu = true;
        relogio?.cancel();
        return;
      }
      corpo.insert(0, cabeca);
      if (cabeca == osso) {
        pontos++;
        novoOsso();
      } else {
        corpo.removeLast();
      }
    });
  }

  @override
  void dispose() {
    relogio?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(perdeu ? 'Fim! Pontos: $pontos' : 'Pontos: $pontos')),
      body: Column(
        children: [
          GestureDetector(
            onPanEnd: (d) {
              final v = d.velocity.pixelsPerSecond;
              if (v.dx.abs() > v.dy.abs()) {
                virar(Offset(v.dx > 0 ? 1 : -1, 0));
              } else {
                virar(Offset(0, v.dy > 0 ? 1 : -1));
              }
            },
            child: CustomPaint(size: const Size(colunas * lado, linhas * lado), painter: Grade(corpo, osso)),
          ),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              IconButton(icon: const Icon(Icons.arrow_back), onPressed: () => virar(const Offset(-1, 0))),
              IconButton(icon: const Icon(Icons.arrow_upward), onPressed: () => virar(const Offset(0, -1))),
              IconButton(icon: const Icon(Icons.arrow_downward), onPressed: () => virar(const Offset(0, 1))),
              IconButton(icon: const Icon(Icons.arrow_forward), onPressed: () => virar(const Offset(1, 0))),
              if (perdeu) FilledButton(onPressed: comecar, child: const Text('De novo')),
            ],
          ),
        ],
      ),
    );
  }
}

class Grade extends CustomPainter {
  final List<Offset> corpo;
  final Offset osso;
  Grade(this.corpo, this.osso);

  @override
  void paint(Canvas canvas, Size size) {
    canvas.drawRect(Rect.fromLTWH(0, 0, size.width, size.height), Paint()..color = const Color(0xFF9ED67A));
    canvas.drawCircle(Offset(osso.dx * lado + lado / 2, osso.dy * lado + lado / 2), lado / 2 - 2, Paint()..color = const Color(0xFFF2EEE6));
    for (int i = 0; i < corpo.length; i++) {
      final c = corpo[i];
      canvas.drawRRect(
        RRect.fromRectAndRadius(Rect.fromLTWH(c.dx * lado + 1, c.dy * lado + 1, lado - 2, lado - 2), const Radius.circular(5)),
        Paint()..color = i == 0 ? const Color(0xFF9C5A22) : const Color(0xFFD68C3E),
      );
    }
  }

  @override
  bool shouldRepaint(Grade old) => true;
}
