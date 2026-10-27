import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(debugShowCheckedModeBanner: false, home: Cobrinha()));

// DESAFIO · COBRINHA DO CARAMELO
// 1. Uma grade de 15 x 20 casas. O caramelo é uma fila de casas (a cabeça e o rabo).
// 2. A cada 200 ms ele anda uma casa na direção atual (Timer.periodic).
// 3. Botões ◀ ▲ ▼ ▶ (ou arrastar o dedo) mudam a direção, mas não deixam voltar para trás.
// 4. Um osso aparece numa casa sorteada. Ao comer, o caramelo cresce e ganha 1 ponto.
// 5. Bater na borda ou no próprio corpo termina o jogo; um botão recomeça.
// Dicas: List<Offset> para o corpo, insert(0, novaCabeca) e removeLast(), contains(...).

class Cobrinha extends StatefulWidget {
  const Cobrinha({super.key});

  @override
  State<Cobrinha> createState() => _CobrinhaState();
}

class _CobrinhaState extends State<Cobrinha> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Pontos: 0')),
      body: const Center(child: Text('Comece pelo Timer.periodic')),
    );
  }
}
