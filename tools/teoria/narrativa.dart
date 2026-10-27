import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(debugShowCheckedModeBanner: false, home: Arvore()));

// Cada cena da história e as cenas que podem vir depois dela.
// Uma cena sem saídas é um final.
const historia = {
  'Muro': ['Gentil', 'Bravo'],
  'Gentil': ['Segredo', 'Sozinho'],
  'Bravo': ['Fuga', 'Desculpa'],
  'Desculpa': ['Segredo'],
  'Segredo': ['Amigos'],
  'Sozinho': [],
  'Fuga': [],
  'Amigos': [],
};
// em que coluna (passo da história) cada cena aparece
const passo = {'Muro': 0, 'Gentil': 1, 'Bravo': 1, 'Sozinho': 2, 'Desculpa': 2, 'Fuga': 2, 'Segredo': 3, 'Amigos': 4};

// conta quantos caminhos diferentes vão do começo até algum final
int caminhos(String cena) {
  final saidas = historia[cena] ?? [];
  if (saidas.isEmpty) return 1;
  var total = 0;
  for (final s in saidas) {
    total += caminhos(s);
  }
  return total;
}

class Arvore extends StatefulWidget {
  const Arvore({super.key});

  @override
  State<Arvore> createState() => _ArvoreState();
}

class _ArvoreState extends State<Arvore> {
  String? marcada;

  @override
  Widget build(BuildContext context) {
    final finais = historia.keys.where((c) => historia[c]!.isEmpty).length;
    return Scaffold(
      appBar: AppBar(title: Text('${historia.length} cenas · $finais finais · ${caminhos('Muro')} caminhos')),
      body: Column(
        children: [
          GestureDetector(
            onTapDown: (d) => setState(() => marcada = Mapa.cenaEm(d.localPosition)),
            child: CustomPaint(size: const Size(360, 420), painter: Mapa(marcada)),
          ),
          Padding(
            padding: const EdgeInsets.all(12),
            child: Text(marcada == null
                ? 'Toque numa cena para ver de onde se chega nela.'
                : '$marcada: ${historia[marcada]!.isEmpty ? 'é um final' : 'leva a ${historia[marcada]!.join(' ou ')}'}'),
          ),
        ],
      ),
    );
  }
}

class Mapa extends CustomPainter {
  final String? marcada;
  Mapa(this.marcada);

  static Offset centro(String cena) {
    final col = passo[cena]!;
    final mesmas = passo.keys.where((c) => passo[c] == col).toList();
    final i = mesmas.indexOf(cena);
    return Offset(40.0 + col * 70, 420 * (i + 1) / (mesmas.length + 1));
  }

  static String? cenaEm(Offset p) {
    for (final c in historia.keys) {
      if ((centro(c) - p).distance < 34) return c;
    }
    return null;
  }

  @override
  void paint(Canvas canvas, Size size) {
    final linha = Paint()..color = Colors.black45..strokeWidth = 2;
    for (final c in historia.keys) {
      for (final s in historia[c]!) {
        canvas.drawLine(centro(c), centro(s), linha);
      }
    }
    for (final c in historia.keys) {
      final fim = historia[c]!.isEmpty;
      final cor = c == marcada ? Colors.amber : (fim ? const Color(0xFFFF8A65) : const Color(0xFF81C784));
      canvas.drawRRect(RRect.fromRectAndRadius(Rect.fromCenter(center: centro(c), width: 66, height: 30), const Radius.circular(10)), Paint()..color = cor);
      final tp = TextPainter(text: TextSpan(text: c, style: const TextStyle(fontSize: 11, color: Colors.black)), textDirection: TextDirection.ltr)..layout();
      tp.paint(canvas, centro(c) - Offset(tp.width / 2, tp.height / 2));
    }
  }

  @override
  bool shouldRepaint(Mapa old) => true;
}
