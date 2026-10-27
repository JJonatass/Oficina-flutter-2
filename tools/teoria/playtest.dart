import 'dart:math';
import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(debugShowCheckedModeBanner: false, home: Teste()));

// I início, F fim, # parede, x espinhos
const fase = [
  '###############',
  '#I....#.......#',
  '#.###.#.#####.#',
  '#...#...#...#.#',
  '###.#####.#.#.#',
  '#...x.....#...#',
  '#.#######.###.#',
  '#.......#.....#',
  '#####.#.#####.#',
  '#.....#..x....#',
  '#.#########.###',
  '#.....x.......#',
  '#.###.#####.#.#',
  '#...#.....#..F#',
  '###############',
];
const int lado = 24;

class Teste extends StatefulWidget {
  const Teste({super.key});

  @override
  State<Teste> createState() => _TesteState();
}

class _TesteState extends State<Teste> {
  final sorteio = Random(7);
  // quantas vezes alguém passou por cada casa e quantos morreram nela
  final Map<int, int> passos = {};
  final Map<int, int> mortes = {};
  int jogadores = 0;
  int chegaram = 0;
  bool verMortes = false;
  // 0 = anda à toa; 1 = sempre vai na direção do fim
  double vontade = 0.6;
  final int limitePassos = 250;

  bool parede(int x, int y) => fase[y][x] == '#';

  void simular(int quantos) {
    setState(() {
      for (int j = 0; j < quantos; j++) {
        var x = 1, y = 1;
        for (int p = 0; p < limitePassos; p++) {
          final chave = y * 100 + x;
          passos[chave] = (passos[chave] ?? 0) + 1;
          if (fase[y][x] == 'F') {
            chegaram++;
            break;
          }
          if (fase[y][x] == 'x') {
            mortes[chave] = (mortes[chave] ?? 0) + 1;
            break;
          }
          final opcoes = <List<int>>[];
          for (final d in const [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
            if (!parede(x + d[0], y + d[1])) opcoes.add(d);
          }
          // com chance "vontade", prefere o passo que mais aproxima do fim (13, 13)
          opcoes.sort((a, b) => ((13 - x - a[0]).abs() + (13 - y - a[1]).abs()).compareTo((13 - x - b[0]).abs() + (13 - y - b[1]).abs()));
          final d = sorteio.nextDouble() < vontade ? opcoes.first : opcoes[sorteio.nextInt(opcoes.length)];
          x += d[0];
          y += d[1];
        }
        jogadores++;
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    final totalMortes = mortes.values.fold(0, (a, b) => a + b);
    return Scaffold(
      appBar: AppBar(title: Text('Teste com $jogadores jogadores')),
      body: Column(
        children: [
          CustomPaint(size: Size(fase[0].length * lado * 1.0, fase.length * lado * 1.0), painter: Calor(passos, mortes, verMortes)),
          Padding(
            padding: const EdgeInsets.all(8),
            child: Text(jogadores == 0
                ? 'Simule alguns jogadores para ver onde eles passam e onde morrem.'
                : 'Chegaram ao fim: ${(chegaram * 100 / jogadores).toStringAsFixed(0)}%   Mortes: $totalMortes'),
          ),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              ChoiceChip(label: const Text('Passos'), selected: !verMortes, onSelected: (_) => setState(() => verMortes = false)),
              const SizedBox(width: 8),
              ChoiceChip(label: const Text('Mortes'), selected: verMortes, onSelected: (_) => setState(() => verMortes = true)),
            ],
          ),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              FilledButton(onPressed: () => simular(20), child: const Text('Simular 20')),
              OutlinedButton(
                onPressed: () => setState(() {
                  passos.clear();
                  mortes.clear();
                  jogadores = 0;
                  chegaram = 0;
                }),
                child: const Text('Limpar'),
              ),
            ],
          ),
        ],
      ),
    );
  }
}

class Calor extends CustomPainter {
  final Map<int, int> passos;
  final Map<int, int> mortes;
  final bool verMortes;
  Calor(this.passos, this.mortes, this.verMortes);

  @override
  void paint(Canvas canvas, Size size) {
    final dados = verMortes ? mortes : passos;
    final maior = dados.values.fold(1, (a, b) => a > b ? a : b);
    for (int y = 0; y < fase.length; y++) {
      for (int x = 0; x < fase[y].length; x++) {
        final c = fase[y][x];
        final r = Rect.fromLTWH(x * lado * 1.0, y * lado * 1.0, lado * 1.0, lado * 1.0);
        canvas.drawRect(r, Paint()..color = c == '#' ? const Color(0xFF3D4A5C) : const Color(0xFFF1EBDD));
        final v = dados[y * 100 + x] ?? 0;
        if (v > 0) {
          final forca = v / maior;
          final cor = verMortes ? Color.fromRGBO(229, 57, 53, 0.25 + 0.75 * forca) : Color.fromRGBO(255, 152, 0, 0.1 + 0.8 * forca);
          canvas.drawRect(r.deflate(1), Paint()..color = cor);
        }
        if (c == 'x') canvas.drawCircle(r.center, 5, Paint()..color = Colors.black);
        if (c == 'F') canvas.drawRect(r.deflate(5), Paint()..color = Colors.green);
      }
    }
  }

  @override
  bool shouldRepaint(Calor old) => true;
}
