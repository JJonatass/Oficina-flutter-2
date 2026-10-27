import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(debugShowCheckedModeBanner: false, home: Caixas()));

// # parede   . tapete   C caixa   * caixa já no tapete   @ caramelo
const fases = [
  [
    '#######',
    '#     #',
    '# @C .#',
    '#     #',
    '#######',
  ],
  [
    '#######',
    '#.    #',
    '# CC  #',
    '#  @ .#',
    '#######',
  ],
  [
    '########',
    '#  .   #',
    '# #C#  #',
    '#  C C #',
    '#. @ . #',
    '########',
  ],
];

const caixa = '📦';
const double lado = 42;

// uma "foto" do jogo: onde estão o caramelo e as caixas
class Estado {
  final int caramelo;
  final Set<int> caixas;
  Estado(this.caramelo, this.caixas);
}

class Caixas extends StatefulWidget {
  const Caixas({super.key});

  @override
  State<Caixas> createState() => _CaixasState();
}

class _CaixasState extends State<Caixas> {
  final int limiteDesfazer = 999;
  int fase = 0;
  List<String> mapa = [];
  int largura = 0;
  Set<int> alvos = {};
  Set<int> caixas = {};
  int caramelo = 0;
  int movimentos = 0;
  // a pilha de desfazer: cada movimento guarda a foto de antes dele
  final List<Estado> historico = [];

  @override
  void initState() {
    super.initState();
    carregar(0);
  }

  void carregar(int n) {
    fase = n;
    mapa = fases[n];
    largura = mapa[0].length;
    alvos = {};
    caixas = {};
    historico.clear();
    movimentos = 0;
    for (var y = 0; y < mapa.length; y++) {
      for (var x = 0; x < largura; x++) {
        final ch = mapa[y][x];
        final i = y * largura + x;
        if (ch == '.' || ch == '*') alvos.add(i);
        if (ch == 'C' || ch == '*') caixas.add(i);
        if (ch == '@') caramelo = i;
      }
    }
  }

  bool parede(int i) => mapa[i ~/ largura][i % largura] == '#';

  bool get venceu => caixas.every((c) => alvos.contains(c));

  void mover(int dx, int dy) {
    if (venceu) return;
    final passo = dy * largura + dx;
    final destino = caramelo + passo;
    if (parede(destino)) return;
    if (caixas.contains(destino)) {
      final alem = destino + passo;
      if (parede(alem) || caixas.contains(alem)) return; // a caixa está presa: nada acontece
      guardar();
      caixas.remove(destino);
      caixas.add(alem);
    } else {
      guardar();
    }
    setState(() {
      caramelo = destino;
      movimentos++;
    });
  }

  // empilha a foto de agora (uma cópia, para não mudar junto com o jogo)
  void guardar() {
    historico.add(Estado(caramelo, Set<int>.from(caixas)));
    if (historico.length > limiteDesfazer) historico.removeAt(0);
  }

  // desempilha a última foto e volta para ela
  void desfazer() {
    if (historico.isEmpty) return;
    final antes = historico.removeLast();
    setState(() {
      caramelo = antes.caramelo;
      caixas = antes.caixas;
      movimentos--;
    });
  }

  @override
  Widget build(BuildContext context) {
    final titulo = venceu ? 'Fase ${fase + 1} completa em $movimentos!' : 'Fase ${fase + 1} · $movimentos movimentos';
    return Scaffold(
      appBar: AppBar(title: Text(titulo)),
      body: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          children: [
            GestureDetector(
              onPanEnd: (d) {
                final v = d.velocity.pixelsPerSecond;
                if (v.dx.abs() > v.dy.abs()) {
                  mover(v.dx > 0 ? 1 : -1, 0);
                } else {
                  mover(0, v.dy > 0 ? 1 : -1);
                }
              },
              child: SizedBox(
                width: largura * lado,
                height: mapa.length * lado,
                child: Wrap(
                  children: [
                    for (var i = 0; i < mapa.length * largura; i++)
                      Container(
                        width: lado,
                        height: lado,
                        alignment: Alignment.center,
                        decoration: BoxDecoration(
                          color: parede(i)
                              ? const Color(0xFF8D6E63)
                              : (alvos.contains(i) ? (caixas.contains(i) ? const Color(0xFF9CCC65) : const Color(0xFFFFE082)) : const Color(0xFFF6E7CF)),
                          border: Border.all(color: const Color(0x22000000)),
                        ),
                        child: Text(caramelo == i ? '🐶' : (caixas.contains(i) ? caixa : (alvos.contains(i) ? '·' : ' ')), style: const TextStyle(fontSize: 26)),
                      ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 16),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                IconButton.filled(icon: const Icon(Icons.arrow_back), onPressed: () => mover(-1, 0)),
                IconButton.filled(icon: const Icon(Icons.arrow_upward), onPressed: () => mover(0, -1)),
                IconButton.filled(icon: const Icon(Icons.arrow_downward), onPressed: () => mover(0, 1)),
                IconButton.filled(icon: const Icon(Icons.arrow_forward), onPressed: () => mover(1, 0)),
              ],
            ),
            const SizedBox(height: 8),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                OutlinedButton(onPressed: historico.isEmpty ? null : desfazer, child: Text('↶ Desfazer (${historico.length})')),
                const SizedBox(width: 8),
                OutlinedButton(onPressed: () => setState(() => carregar(fase)), child: const Text('↺ Reiniciar')),
              ],
            ),
            const SizedBox(height: 8),
            if (venceu && fase < fases.length - 1) FilledButton(onPressed: () => setState(() => carregar(fase + 1)), child: const Text('Próxima fase')),
            if (venceu && fase == fases.length - 1) const Text('Você terminou todas as fases! 🎉', style: TextStyle(fontSize: 18)),
          ],
        ),
      ),
    );
  }
}
