import 'dart:math';
import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(debugShowCheckedModeBanner: false, home: Loja()));

class Loja extends StatefulWidget {
  const Loja({super.key});

  @override
  State<Loja> createState() => _LojaState();
}

// O caramelo ganha ossos por minuto e compra melhorias de faro.
// Cada nível de faro aumenta o ganho; cada nível custa mais que o anterior.
class _LojaState extends State<Loja> {
  double custoBase = 10;
  double crescimentoCusto = 1.5; // cada nível custa 50% a mais
  double ganhoBase = 5; // ossos por minuto no nível 0
  double ganhoPorNivel = 3; // ossos por minuto a mais por nível

  double custo(int nivel) => custoBase * pow(crescimentoCusto, nivel).toDouble();
  double ganho(int nivel) => ganhoBase + ganhoPorNivel * nivel;

  // quantos minutos o jogador espera para comprar o próximo nível
  double espera(int nivel) => custo(nivel) / ganho(nivel);

  @override
  Widget build(BuildContext context) {
    final niveis = List.generate(15, (n) => n);
    final total = niveis.fold(0.0, (s, n) => s + espera(n));
    return Scaffold(
      appBar: AppBar(title: Text('15 níveis em ${total.toStringAsFixed(0)} minutos')),
      body: ListView(
        padding: const EdgeInsets.all(12),
        children: [
          const Text('Minutos de espera para comprar cada nível de faro:'),
          const SizedBox(height: 8),
          CustomPaint(size: const Size(336, 220), painter: Barras([for (final n in niveis) espera(n)])),
          const SizedBox(height: 8),
          Text('Crescimento do custo: ${crescimentoCusto.toStringAsFixed(2)}×'),
          Slider(value: crescimentoCusto, min: 1.05, max: 2.0, onChanged: (v) => setState(() => crescimentoCusto = v)),
          Text('Ossos a mais por nível: ${ganhoPorNivel.toStringAsFixed(1)}'),
          Slider(value: ganhoPorNivel, min: 0, max: 10, onChanged: (v) => setState(() => ganhoPorNivel = v)),
          const Divider(),
          for (final n in [0, 4, 9, 14])
            Text('Nível ${n + 1}: custa ${custo(n).toStringAsFixed(0)} ossos, ganho ${ganho(n).toStringAsFixed(0)}/min, espera ${espera(n).toStringAsFixed(1)} min'),
        ],
      ),
    );
  }
}

class Barras extends CustomPainter {
  final List<double> valores;
  Barras(this.valores);

  @override
  void paint(Canvas canvas, Size size) {
    final maior = valores.reduce((a, b) => a > b ? a : b);
    final w = size.width / valores.length;
    for (int i = 0; i < valores.length; i++) {
      final h = maior == 0 ? 0.0 : valores[i] / maior * (size.height - 10);
      // laranja quando a espera passa de 10 minutos: o jogador pode desistir
      final cor = valores[i] > 10 ? const Color(0xFFFF8A65) : const Color(0xFF81C784);
      canvas.drawRect(Rect.fromLTWH(i * w + 2, size.height - h, w - 4, h), Paint()..color = cor);
    }
    canvas.drawLine(Offset(0, size.height), Offset(size.width, size.height), Paint()..color = Colors.black54);
  }

  @override
  bool shouldRepaint(Barras old) => true;
}
