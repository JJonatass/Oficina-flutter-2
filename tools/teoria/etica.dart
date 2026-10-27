import 'dart:math';
import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(debugShowCheckedModeBanner: false, home: Bau()));

class Premio {
  final String nome;
  final String icone;
  final double chance; // de 0 a 1; todas juntas somam 1
  const Premio(this.nome, this.icone, this.chance);
}

// as chances ficam à vista do jogador: nada de sorteio escondido
const premios = [
  Premio('Osso comum', '🦴', 0.70),
  Premio('Bola nova', '⚽', 0.25),
  Premio('Coleira dourada', '👑', 0.05),
];

class Bau extends StatefulWidget {
  const Bau({super.key});

  @override
  State<Bau> createState() => _BauState();
}

class _BauState extends State<Bau> {
  final sorteio = Random();
  final int pausaACada = 10; // depois de tantos baús, o jogo sugere uma pausa
  int abertos = 0;
  Map<String, int> ganhos = {};
  String ultimo = '';
  bool sugerirPausa = false;

  Premio sortear() {
    var r = sorteio.nextDouble();
    for (final p in premios) {
      if (r < p.chance) return p;
      r -= p.chance;
    }
    return premios.last;
  }

  void abrir() {
    final p = sortear();
    setState(() {
      abertos++;
      ganhos[p.nome] = (ganhos[p.nome] ?? 0) + 1;
      ultimo = '${p.icone} ${p.nome}';
      sugerirPausa = abertos % pausaACada == 0;
    });
  }

  @override
  Widget build(BuildContext context) {
    // em média, quantos baús até o prêmio raro: 1 / chance
    final media = (1 / premios.last.chance).round();
    return Scaffold(
      appBar: AppBar(title: Text('Baús abertos: $abertos')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Text(ultimo.isEmpty ? 'Toque para abrir um baú' : ultimo, textAlign: TextAlign.center, style: const TextStyle(fontSize: 30)),
          const SizedBox(height: 12),
          FilledButton(onPressed: abrir, child: const Text('🎁 Abrir baú')),
          const SizedBox(height: 16),
          const Text('Chances de cada prêmio', style: TextStyle(fontWeight: FontWeight.bold)),
          for (final p in premios)
            ListTile(
              leading: Text(p.icone, style: const TextStyle(fontSize: 26)),
              title: Text(p.nome),
              subtitle: Text('${(p.chance * 100).toStringAsFixed(0)}% · você ganhou ${ganhos[p.nome] ?? 0}'),
            ),
          Text('Em média, a coleira dourada sai 1 vez a cada $media baús.'),
          if (sugerirPausa)
            Card(
              color: Colors.amber.shade100,
              child: const Padding(
                padding: EdgeInsets.all(12),
                child: Text('Você já abriu vários baús. Que tal uma pausa? Os prêmios continuam aqui depois.'),
              ),
            ),
        ],
      ),
    );
  }
}
