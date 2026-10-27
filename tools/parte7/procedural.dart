import 'dart:math';
import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(debugShowCheckedModeBanner: false, home: Gerador()));

const int colunas = 21;
const int linhas = 29;

// true = parede, false = chão
typedef Grade = List<List<bool>>;

class Celula {
  final int x;
  final int y;
  const Celula(this.x, this.y);
}

Grade cheia(bool valor) => List.generate(linhas, (_) => List.filled(colunas, valor));

// Labirinto: começa tudo parede e cava caminhos com uma pilha (busca em profundidade)
Grade labirinto(Random r) {
  final g = cheia(true);
  final pilha = <Celula>[const Celula(1, 1)];
  g[1][1] = false;
  while (pilha.isNotEmpty) {
    final atual = pilha.last;
    final vizinhos = <Celula>[];
    for (final d in const [Celula(0, -2), Celula(2, 0), Celula(0, 2), Celula(-2, 0)]) {
      final n = Celula(atual.x + d.x, atual.y + d.y);
      if (n.x > 0 && n.y > 0 && n.x < colunas - 1 && n.y < linhas - 1 && g[n.y][n.x]) vizinhos.add(n);
    }
    if (vizinhos.isEmpty) {
      pilha.removeLast();
    } else {
      final n = vizinhos[r.nextInt(vizinhos.length)];
      g[(atual.y + n.y) ~/ 2][(atual.x + n.x) ~/ 2] = false; // derruba a parede do meio
      g[n.y][n.x] = false;
      pilha.add(n);
    }
  }
  return g;
}

// Cavernas: sorteia paredes e depois suaviza com a regra dos vizinhos (autômato celular)
double chanceParede = 0.45;
int passosSuavizar = 4;

Grade cavernas(Random r) {
  var g = List.generate(linhas, (y) => List.generate(colunas, (x) => r.nextDouble() < chanceParede));
  for (int passo = 0; passo < passosSuavizar; passo++) {
    final nova = cheia(false);
    for (int y = 0; y < linhas; y++) {
      for (int x = 0; x < colunas; x++) {
        var paredes = 0;
        for (int dy = -1; dy <= 1; dy++) {
          for (int dx = -1; dx <= 1; dx++) {
            final nx = x + dx, ny = y + dy;
            if (nx < 0 || ny < 0 || nx >= colunas || ny >= linhas || g[ny][nx]) paredes++;
          }
        }
        nova[y][x] = paredes >= 5;
      }
    }
    g = nova;
  }
  return g;
}

class Gerador extends StatefulWidget {
  const Gerador({super.key});

  @override
  State<Gerador> createState() => _GeradorState();
}

class _GeradorState extends State<Gerador> {
  int semente = 42;
  String modo = 'Labirinto';
  late Grade grade;

  @override
  void initState() {
    super.initState();
    gerar();
  }

  // mesma semente = mesma sequência de sorteios = mesmo mapa
  void gerar() {
    final r = Random(semente);
    grade = modo == 'Labirinto' ? labirinto(r) : cavernas(r);
  }

  void trocar(int nova) {
    setState(() {
      semente = nova;
      gerar();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('$modo · semente $semente')),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(8),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                for (final m in ['Labirinto', 'Cavernas'])
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 4),
                    child: ChoiceChip(
                      label: Text(m),
                      selected: modo == m,
                      onSelected: (_) => setState(() {
                        modo = m;
                        gerar();
                      }),
                    ),
                  ),
              ],
            ),
          ),
          CustomPaint(size: const Size(360, 480), painter: Desenho(grade)),
          const Spacer(),
          Padding(
            padding: const EdgeInsets.all(8),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                OutlinedButton(onPressed: () => trocar(semente - 1), child: const Text('◀ anterior')),
                FilledButton(onPressed: () => trocar(Random().nextInt(100000)), child: const Text('Sortear')),
                OutlinedButton(onPressed: () => trocar(semente + 1), child: const Text('próxima ▶')),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class Desenho extends CustomPainter {
  final Grade grade;
  Desenho(this.grade);

  @override
  void paint(Canvas canvas, Size size) {
    final lado = min(size.width / colunas, size.height / linhas);
    final ox = (size.width - lado * colunas) / 2;
    final parede = Paint()..color = const Color(0xFF5B4636);
    final chao = Paint()..color = const Color(0xFFE9D8A6);
    for (int y = 0; y < linhas; y++) {
      for (int x = 0; x < colunas; x++) {
        canvas.drawRect(Rect.fromLTWH(ox + x * lado, y * lado, lado + 0.5, lado + 0.5), grade[y][x] ? parede : chao);
      }
    }
  }

  @override
  bool shouldRepaint(Desenho old) => true;
}
