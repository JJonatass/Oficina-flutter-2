import 'dart:async';
import 'dart:math';
import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(debugShowCheckedModeBanner: false, home: Cobrinha()));

// DESAFIO · COBRINHA DO CARAMELO
// 1. Uma grade de 15 x 20 casas. O caramelo é uma fila de casas (a cabeça e o rabo).
// 2. A cada 200 ms ele anda uma casa na direção atual (Timer.periodic).
// 3. Botões ◀ ▲ ▼ ▶ (ou arrastar o dedo) mudam a direção, mas não deixam voltar para trás.
// 4. Um osso aparece numa casa sorteada. Ao comer, o caramelo cresce e ganha 1 ponto.
// 5. Bater na borda ou no próprio corpo termina o jogo; um botão recomeça.
// A grade, os botões, o desenho e o andar já estão prontos. Complete as partes marcadas com FAÇA.

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
    // FAÇA 1: o laço do jogo. Guarde em relogio um Timer que repete a cada 200 ms
    // e chama andar() (o Timer periódico da aula 1).
  }

  void novoOsso() {
    // FAÇA 2: sorteie uma casa para o osso: uma coluna de 0 a colunas - 1 e uma linha de 0 a linhas - 1
    // (com o sorteio), e guarde em osso como Offset(coluna, linha) com toDouble().
    // Extra: sorteie de novo enquanto a casa cair em cima do corpo.
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
      // FAÇA 3: também perde se a cabeça cair numa casa do próprio corpo (pergunte à lista corpo se ela contém a cabeça).
      if (fora) {
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
