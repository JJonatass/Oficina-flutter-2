import 'dart:async';
import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(debugShowCheckedModeBanner: false, home: Nevoa()));

const mapa = [
  '###############',
  '#.....#.......#',
  '#.###.#.#####.#',
  '#.#...#.....#.#',
  '#.#.#####.#.#.#',
  '#...#.....#...#',
  '###.#.###.###.#',
  '#...#...#.....#',
  '#.#####.#####.#',
  '#.....#.....#.#',
  '#.###.#####.#.#',
  '#.#.........#.#',
  '#.#.#######.#.#',
  '#...#.........#',
  '###############',
];
const double lado = 24;
const corLembrada = Color(0x99000000); // casa já vista, mas fora da visão agora
const corNunca = Color(0xFF000000); // casa nunca vista
const rondaGato = [[13, 7], [13, 13], [5, 13], [13, 13], [13, 7], [9, 7], [9, 3], [11, 3], [11, 5], [13, 5], [13, 1]];

bool parede(int x, int y) => mapa[y][x] == '#';

// A linha reta entre duas casas (algoritmo de Bresenham). Se ela passa por uma parede, não dá para ver.
bool enxerga(int x0, int y0, int x1, int y1) {
  var x = x0;
  var y = y0;
  final dx = (x1 - x0).abs();
  final dy = -(y1 - y0).abs();
  final sx = x0 < x1 ? 1 : -1;
  final sy = y0 < y1 ? 1 : -1;
  var erro = dx + dy;
  while (x != x1 || y != y1) {
    if ((x != x0 || y != y0) && parede(x, y)) return false;
    final e2 = 2 * erro;
    if (e2 >= dy) {
      erro += dy;
      x += sx;
    }
    if (e2 <= dx) {
      erro += dx;
      y += sy;
    }
  }
  return true;
}

class Nevoa extends StatefulWidget {
  const Nevoa({super.key});

  @override
  State<Nevoa> createState() => _NevoaState();
}

class _NevoaState extends State<Nevoa> {
  final int raioVisao = 5; // até quantas casas o caramelo enxerga
  final int raioGato = 4;
  int cx = 1;
  int cy = 1;
  int gx = 13;
  int gy = 1;
  int ronda = 0;
  bool nevoaLigada = true;
  Set<int> visiveis = {};
  Set<int> vistas = {};
  String aviso = 'Explore o labirinto sem o gato ver você.';
  Timer? relogio;

  @override
  void initState() {
    super.initState();
    calcularVisao();
    relogio = Timer.periodic(const Duration(milliseconds: 400), (t) => setState(() => andarGato()));
  }

  @override
  void dispose() {
    relogio?.cancel();
    super.dispose();
  }

  // quais casas o caramelo vê agora: perto o bastante e com a linha livre
  void calcularVisao() {
    visiveis = {};
    for (var y = 0; y < mapa.length; y++) {
      for (var x = 0; x < mapa[0].length; x++) {
        final perto = (x - cx) * (x - cx) + (y - cy) * (y - cy) <= raioVisao * raioVisao;
        if (perto && enxerga(cx, cy, x, y)) visiveis.add(y * 15 + x);
      }
    }
    vistas.addAll(visiveis); // o que já foi visto fica no mapa (a memória)
  }

  void mover(int dx, int dy) {
    if (parede(cx + dx, cy + dy)) return;
    setState(() {
      cx += dx;
      cy += dy;
      calcularVisao();
    });
  }

  // o gato anda de ponto em ponto da ronda, uma casa por vez
  void andarGato() {
    final alvo = rondaGato[ronda];
    if (gx == alvo[0] && gy == alvo[1]) {
      ronda = (ronda + 1) % rondaGato.length;
      return;
    }
    if (gx != alvo[0]) {
      gx += gx < alvo[0] ? 1 : -1;
    } else {
      gy += gy < alvo[1] ? 1 : -1;
    }
    // a mesma função de visão serve para o inimigo
    final pertoGato = (gx - cx) * (gx - cx) + (gy - cy) * (gy - cy) <= raioGato * raioGato;
    aviso = pertoGato && enxerga(gx, gy, cx, cy) ? '😾 O gato viu você!' : 'Explore o labirinto sem o gato ver você.';
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Visto: ${vistas.length} casas')),
      body: Column(
        children: [
          CustomPaint(size: const Size(360, 360), painter: Labirinto(cx, cy, gx, gy, visiveis, vistas, nevoaLigada)),
          const SizedBox(height: 6),
          Text(aviso, style: const TextStyle(fontSize: 18)),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              IconButton.filled(icon: const Icon(Icons.arrow_back), onPressed: () => mover(-1, 0)),
              IconButton.filled(icon: const Icon(Icons.arrow_upward), onPressed: () => mover(0, -1)),
              IconButton.filled(icon: const Icon(Icons.arrow_downward), onPressed: () => mover(0, 1)),
              IconButton.filled(icon: const Icon(Icons.arrow_forward), onPressed: () => mover(1, 0)),
            ],
          ),
          SwitchListTile(title: const Text('Névoa de guerra'), value: nevoaLigada, onChanged: (v) => setState(() => nevoaLigada = v)),
        ],
      ),
    );
  }
}

class Labirinto extends CustomPainter {
  final int cx, cy, gx, gy;
  final Set<int> visiveis;
  final Set<int> vistas;
  final bool nevoa;
  Labirinto(this.cx, this.cy, this.gx, this.gy, this.visiveis, this.vistas, this.nevoa);

  @override
  void paint(Canvas canvas, Size size) {
    for (var y = 0; y < mapa.length; y++) {
      for (var x = 0; x < mapa[0].length; x++) {
        final r = Rect.fromLTWH(x * lado, y * lado, lado, lado);
        canvas.drawRect(r, Paint()..color = parede(x, y) ? const Color(0xFF5D4037) : const Color(0xFFD7CCC8));
        final i = y * 15 + x;
        if (nevoa && !visiveis.contains(i)) {
          canvas.drawRect(r, Paint()..color = vistas.contains(i) ? corLembrada : corNunca);
        }
      }
    }
    // o gato só aparece se estiver numa casa visível (ou sem névoa)
    if (!nevoa || visiveis.contains(gy * 15 + gx)) {
      canvas.drawCircle(Offset(gx * lado + lado / 2, gy * lado + lado / 2), 10, Paint()..color = const Color(0xFF9E9E9E));
    }
    canvas.drawCircle(Offset(cx * lado + lado / 2, cy * lado + lado / 2), 10, Paint()..color = const Color(0xFFD68C3E));
  }

  @override
  bool shouldRepaint(Labirinto old) => true;
}
