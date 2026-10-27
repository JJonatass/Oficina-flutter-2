import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(debugShowCheckedModeBanner: false, home: Reacao()));

// DESAFIO · RELÓGIO DE REAÇÃO
// 1. A tela começa cinza, com "Toque para começar".
// 2. Ao tocar, espera um tempo sorteado (de 1 a 3 segundos) e fica verde com "TOQUE AGORA!".
// 3. Ao tocar no verde, mostre quantos milissegundos a pessoa levou.
// 4. Guarde o melhor tempo (recorde) e mostre embaixo.
// 5. Se tocar antes de ficar verde, avise "Cedo demais!" e deixe tentar de novo.
// Dicas: Timer (dart:async), Random (dart:math), DateTime.now() e difference(...).inMilliseconds.

class Reacao extends StatefulWidget {
  const Reacao({super.key});

  @override
  State<Reacao> createState() => _ReacaoState();
}

class _ReacaoState extends State<Reacao> {
  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      body: Center(child: Text('Toque para começar', style: TextStyle(fontSize: 26))),
    );
  }
}
