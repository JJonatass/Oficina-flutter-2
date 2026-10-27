import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(debugShowCheckedModeBanner: false, home: Roteiro()));

// tipos de trecho de uma fase e o quanto cada um aperta o jogador (0 a 1)
const tipos = {
  'ensina': 0.2,
  'pratica': 0.45,
  'desafio': 0.8,
  'descanso': 0.1,
  'chefe': 1.0,
};
const cores = {
  'ensina': Color(0xFF64B5F6),
  'pratica': Color(0xFF81C784),
  'desafio': Color(0xFFFF8A65),
  'descanso': Color(0xFFB0BEC5),
  'chefe': Color(0xFFE53935),
};

class Roteiro extends StatefulWidget {
  const Roteiro({super.key});

  @override
  State<Roteiro> createState() => _RoteiroState();
}

class _RoteiroState extends State<Roteiro> {
  // a fase, trecho por trecho
  final List<String> trechos = ['ensina', 'pratica', 'desafio', 'descanso', 'ensina', 'pratica', 'desafio', 'desafio', 'descanso', 'chefe'];
  // quantos trechos difíceis seguidos o jogador aguenta sem respiro
  final int limiteSeguidos = 2;

  void trocar(int i) {
    final nomes = tipos.keys.toList();
    setState(() => trechos[i] = nomes[(nomes.indexOf(trechos[i]) + 1) % nomes.length]);
  }

  List<String> avisos() {
    final lista = <String>[];
    if (trechos.first != 'ensina') lista.add('A fase não começa ensinando.');
    var seguidos = 0;
    for (int i = 0; i < trechos.length; i++) {
      if (tipos[trechos[i]]! >= 0.8) {
        seguidos++;
        if (seguidos > limiteSeguidos) lista.add('Trecho ${i + 1}: difícil demais em sequência, falta um descanso.');
      } else {
        seguidos = 0;
      }
      if (trechos[i] == 'desafio' && !trechos.sublist(0, i).contains('pratica')) {
        lista.add('Trecho ${i + 1}: desafio antes de qualquer prática.');
      }
    }
    if (tipos[trechos.last]! < 0.8) lista.add('O fim não tem um momento forte (desafio ou chefe).');
    return lista;
  }

  @override
  Widget build(BuildContext context) {
    final av = avisos();
    return Scaffold(
      appBar: AppBar(title: const Text('Ritmo da fase')),
      body: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Text('Toque num trecho para trocar o tipo.'),
            const SizedBox(height: 8),
            GestureDetector(
              onTapDown: (d) => trocar((d.localPosition.dx / (336 / trechos.length)).floor().clamp(0, trechos.length - 1)),
              child: CustomPaint(size: const Size(336, 220), painter: Grafico(trechos)),
            ),
            const SizedBox(height: 8),
            Wrap(
              spacing: 12,
              children: [
                for (final t in tipos.keys)
                  Row(mainAxisSize: MainAxisSize.min, children: [
                    Container(width: 14, height: 14, color: cores[t]),
                    const SizedBox(width: 4),
                    Text(t),
                  ]),
              ],
            ),
            const SizedBox(height: 8),
            if (av.isEmpty) const Text('✓ Ritmo equilibrado', style: TextStyle(color: Colors.green, fontSize: 18)),
            for (final a in av) Text('⚠ $a', style: const TextStyle(color: Colors.deepOrange)),
          ],
        ),
      ),
    );
  }
}

class Grafico extends CustomPainter {
  final List<String> trechos;
  Grafico(this.trechos);

  @override
  void paint(Canvas canvas, Size size) {
    final w = size.width / trechos.length;
    final caminho = Path();
    for (int i = 0; i < trechos.length; i++) {
      final v = tipos[trechos[i]]!;
      final h = v * (size.height - 20);
      canvas.drawRect(Rect.fromLTWH(i * w + 2, size.height - h, w - 4, h), Paint()..color = cores[trechos[i]]!);
      final p = Offset(i * w + w / 2, size.height - h);
      if (i == 0) {
        caminho.moveTo(p.dx, p.dy);
      } else {
        caminho.lineTo(p.dx, p.dy);
      }
    }
    canvas.drawPath(caminho, Paint()..color = Colors.black87..style = PaintingStyle.stroke..strokeWidth = 2);
  }

  @override
  bool shouldRepaint(Grafico old) => true;
}
