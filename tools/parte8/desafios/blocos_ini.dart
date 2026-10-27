import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(debugShowCheckedModeBanner: false, home: QuebraBlocos()));

// DESAFIO · QUEBRA-BLOCOS
// 1. Uma raquete embaixo segue o dedo (arrastar na horizontal).
// 2. Uma bola anda sozinha (Ticker + dt) e quica nas paredes, no teto e na raquete.
// 3. No alto, 5 fileiras de 6 blocos. A bola quebra o bloco em que bate e volta.
// 4. Cada bloco vale 10 pontos. Sem blocos: vitória. Se a bola cair embaixo da raquete: perde uma vida (3 vidas).
// Dicas: List<Rect> para os blocos, Rect.overlaps ou contains, removeAt, e desenhe tudo num CustomPainter.

class QuebraBlocos extends StatefulWidget {
  const QuebraBlocos({super.key});

  @override
  State<QuebraBlocos> createState() => _QuebraBlocosState();
}

class _QuebraBlocosState extends State<QuebraBlocos> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Pontos: 0   ♥♥♥')),
      body: const Center(child: Text('Comece pela raquete')),
    );
  }
}
