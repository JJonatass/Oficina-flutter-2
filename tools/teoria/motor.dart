import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(debugShowCheckedModeBanner: false, home: Escolha()));

class Pergunta {
  final String texto;
  final int peso; // positivo puxa para o Flame, negativo puxa para o Flutter puro
  const Pergunta(this.texto, this.peso);
}

// perguntas sobre o SEU jogo: marque as que valem para ele
const perguntas = [
  Pergunta('Muitos objetos se mexendo ao mesmo tempo (inimigos, tiros, partículas)', 2),
  Pergunta('O mundo é maior que a tela e precisa de câmera', 2),
  Pergunta('Colisões entre muitas formas diferentes', 2),
  Pergunta('Física de verdade (quicar, empurrar, juntas)', 2),
  Pergunta('Mapas feitos no Tiled', 2),
  Pergunta('O jogo é feito de botões, cartas ou casas de um tabuleiro', -2),
  Pergunta('Joga por turnos: nada acontece enquanto o jogador pensa', -2),
  Pergunta('Muitas telas de menu, listas e formulários', -1),
  Pergunta('Só um ou dois objetos animados na tela', -1),
];

class Escolha extends StatefulWidget {
  const Escolha({super.key});

  @override
  State<Escolha> createState() => _EscolhaState();
}

class _EscolhaState extends State<Escolha> {
  final Set<int> marcadas = {};
  final int limite = 2; // a partir de quantos pontos vale a pena o Flame

  int get pontos {
    var total = 0;
    for (final i in marcadas) {
      total += perguntas[i].peso;
    }
    return total;
  }

  @override
  Widget build(BuildContext context) {
    final p = pontos;
    final conselho = marcadas.isEmpty
        ? 'Marque o que vale para o seu jogo.'
        : (p >= limite
            ? '🔥 Flame: o laço, a câmera e as colisões já vêm prontos.'
            : (p <= -limite ? '🧩 Flutter puro: widgets e setState dão conta.' : '🤝 Os dois servem: comece simples, com Flutter puro.'));
    return Scaffold(
      appBar: AppBar(title: Text('Pontos: $p')),
      body: ListView(
        children: [
          Padding(
            padding: const EdgeInsets.all(16),
            child: Text(conselho, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          ),
          for (var i = 0; i < perguntas.length; i++)
            CheckboxListTile(
              value: marcadas.contains(i),
              title: Text(perguntas[i].texto),
              subtitle: Text(perguntas[i].peso > 0 ? 'puxa para o Flame (+${perguntas[i].peso})' : 'puxa para o Flutter puro (${perguntas[i].peso})'),
              onChanged: (v) => setState(() {
                if (v == true) {
                  marcadas.add(i);
                } else {
                  marcadas.remove(i);
                }
              }),
            ),
        ],
      ),
    );
  }
}
