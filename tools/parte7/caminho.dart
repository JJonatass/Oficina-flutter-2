import 'dart:async';
import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(debugShowCheckedModeBanner: false, home: Caca()));

const mapa = [
  '###############',
  '#.............#',
  '#.###.#####.#.#',
  '#.#.....#...#.#',
  '#.#.###.#.###.#',
  '#...#.....#...#',
  '###.#.###.#.###',
  '#...#...#.#...#',
  '#.#####.#.###.#',
  '#.....#.#.....#',
  '#.###.#.#####.#',
  '#...#.........#',
  '#.#.#######.#.#',
  '#.#.........#.#',
  '###############',
];
const int lado = 24;

class Celula {
  final int x;
  final int y;
  const Celula(this.x, this.y);
  @override
  bool operator ==(Object o) => o is Celula && o.x == x && o.y == y;
  @override
  int get hashCode => y * 100 + x;
}

class Busca {
  final List<Celula> caminho;
  final List<Celula> exploradas;
  Busca(this.caminho, this.exploradas);
}

// distância "de táxi": quantos passos faltariam sem paredes
int estimativa(Celula a, Celula b) => (a.x - b.x).abs() + (a.y - b.y).abs();

Busca procurar(List<List<bool>> parede, Celula inicio, Celula alvo, bool usarAEstrela) {
  final veioDe = <int, Celula>{};
  final custo = <int, int>{inicio.hashCode: 0};
  final fila = <Celula>[inicio];
  final exploradas = <Celula>[];
  while (fila.isNotEmpty) {
    // BFS pega o mais antigo da fila; A* pega o que parece mais perto do alvo
    var escolhido = 0;
    if (usarAEstrela) {
      for (int i = 1; i < fila.length; i++) {
        final a = fila[i], b = fila[escolhido];
        if (custo[a.hashCode]! + estimativa(a, alvo) < custo[b.hashCode]! + estimativa(b, alvo)) escolhido = i;
      }
    }
    final atual = fila.removeAt(escolhido);
    exploradas.add(atual);
    if (atual == alvo) break;
    for (final d in const [Celula(1, 0), Celula(-1, 0), Celula(0, 1), Celula(0, -1)]) {
      final n = Celula(atual.x + d.x, atual.y + d.y);
      if (parede[n.y][n.x]) continue;
      final novoCusto = custo[atual.hashCode]! + 1;
      if (!custo.containsKey(n.hashCode) || novoCusto < custo[n.hashCode]!) {
        custo[n.hashCode] = novoCusto;
        veioDe[n.hashCode] = atual;
        fila.add(n);
      }
    }
  }
  // volta do alvo até o início seguindo veioDe
  final caminho = <Celula>[];
  if (!veioDe.containsKey(alvo.hashCode) && alvo != inicio) return Busca(caminho, exploradas);
  var c = alvo;
  while (c != inicio) {
    caminho.insert(0, c);
    c = veioDe[c.hashCode]!;
  }
  return Busca(caminho, exploradas);
}

class Caca extends StatefulWidget {
  const Caca({super.key});

  @override
  State<Caca> createState() => _CacaState();
}

class _CacaState extends State<Caca> {
  final parede = [for (final linha in mapa) [for (final c in linha.split('')) c == '#']];
  Celula gato = const Celula(1, 1);
  Celula caramelo = const Celula(13, 13);
  bool aEstrela = false;
  bool porParede = false;
  Busca busca = Busca([], []);
  Timer? passos;
  // o gato dá um passo a cada 250 milissegundos
  final int msPorPasso = 250;

  @override
  void initState() {
    super.initState();
    recalcular();
    passos = Timer.periodic(Duration(milliseconds: msPorPasso), (t) => andar());
  }

  void recalcular() {
    busca = procurar(parede, gato, caramelo, aEstrela);
  }

  void andar() {
    if (busca.caminho.isEmpty) return;
    setState(() {
      gato = busca.caminho.first;
      recalcular();
    });
  }

  void tocar(Offset p) {
    final c = Celula(p.dx ~/ lado, p.dy ~/ lado);
    if (c.y < 1 || c.y >= mapa.length - 1 || c.x < 1 || c.x >= mapa[0].length - 1) return;
    setState(() {
      if (porParede) {
        parede[c.y][c.x] = !parede[c.y][c.x];
      } else if (!parede[c.y][c.x]) {
        caramelo = c;
      }
      recalcular();
    });
  }

  @override
  void dispose() {
    passos?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(aEstrela ? 'A*' : 'Busca em largura (BFS)')),
      body: Column(
        children: [
          Wrap(
            spacing: 8,
            children: [
              ChoiceChip(label: const Text('BFS'), selected: !aEstrela, onSelected: (_) => setState(() { aEstrela = false; recalcular(); })),
              ChoiceChip(label: const Text('A*'), selected: aEstrela, onSelected: (_) => setState(() { aEstrela = true; recalcular(); })),
              FilterChip(label: const Text('Pôr parede'), selected: porParede, onSelected: (v) => setState(() => porParede = v)),
            ],
          ),
          Text('Explorou ${busca.exploradas.length} casas · caminho de ${busca.caminho.length} passos'),
          const SizedBox(height: 8),
          GestureDetector(
            onTapDown: (d) => tocar(d.localPosition),
            child: CustomPaint(size: Size(mapa[0].length * lado * 1.0, mapa.length * lado * 1.0), painter: Labirinto(parede, busca, gato, caramelo)),
          ),
        ],
      ),
    );
  }
}

class Labirinto extends CustomPainter {
  final List<List<bool>> parede;
  final Busca busca;
  final Celula gato;
  final Celula caramelo;
  Labirinto(this.parede, this.busca, this.gato, this.caramelo);

  Rect casa(Celula c) => Rect.fromLTWH(c.x * lado * 1.0, c.y * lado * 1.0, lado * 1.0, lado * 1.0);

  @override
  void paint(Canvas canvas, Size size) {
    for (int y = 0; y < parede.length; y++) {
      for (int x = 0; x < parede[y].length; x++) {
        canvas.drawRect(casa(Celula(x, y)), Paint()..color = parede[y][x] ? const Color(0xFF3D4A5C) : const Color(0xFFF1EBDD));
      }
    }
    for (final c in busca.exploradas) {
      canvas.drawRect(casa(c).deflate(3), Paint()..color = const Color(0x553C8DFF));
    }
    for (final c in busca.caminho) {
      canvas.drawCircle(casa(c).center, 4, Paint()..color = Colors.deepOrange);
    }
    canvas.drawCircle(casa(caramelo).center, 10, Paint()..color = const Color(0xFFD98B3A));
    canvas.drawCircle(casa(gato).center, 10, Paint()..color = const Color(0xFF6B6F78));
  }

  @override
  bool shouldRepaint(Labirinto old) => true;
}
