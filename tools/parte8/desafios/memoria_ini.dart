import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(debugShowCheckedModeBanner: false, home: Memoria()));

// DESAFIO · JOGO DA MEMÓRIA
// 1. 12 cartas viradas para baixo, com 6 pares de figuras (por exemplo 🦴 🐱 🎾 🐾 🍖 🏠), embaralhadas.
// 2. Tocar numa carta vira ela. Com duas viradas: se forem iguais, ficam abertas; se não, desviram depois de 1 segundo.
// 3. Conte as jogadas (cada par tentado é uma jogada).
// 4. Quando todos os pares estiverem abertos, mostre "Você venceu em N jogadas!" e um botão para jogar de novo.
// Dicas: List<String> com shuffle(), um Set<int> com as abertas, Future.delayed ou Timer para desvirar.

class Memoria extends StatefulWidget {
  const Memoria({super.key});

  @override
  State<Memoria> createState() => _MemoriaState();
}

class _MemoriaState extends State<Memoria> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Jogadas: 0')),
      body: const Center(child: Text('Comece embaralhando as cartas')),
    );
  }
}
