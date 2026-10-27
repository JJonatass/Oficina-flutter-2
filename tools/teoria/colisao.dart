import 'dart:math';
import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(debugShowCheckedModeBanner: false, home: Testes()));

// Círculo contra círculo: a distância entre os centros é menor que a soma dos raios?
bool circulos(Offset a, double ra, Offset b, double rb) => (a - b).distance < ra + rb;

// Retângulo contra retângulo (AABB): separados se um está todo de um lado do outro
bool retangulos(Rect a, Rect b) => a.left < b.right && a.right > b.left && a.top < b.bottom && a.bottom > b.top;

// Círculo contra retângulo: o ponto do retângulo mais perto do centro está dentro do círculo?
Offset maisPerto(Rect r, Offset c) => Offset(c.dx.clamp(r.left, r.right).toDouble(), c.dy.clamp(r.top, r.bottom).toDouble());
bool circuloRetangulo(Offset c, double raio, Rect r) => (c - maisPerto(r, c)).distance < raio;

// Resolver: quanto empurrar A para sair de B pelo lado mais curto
Offset empurrao(Rect a, Rect b) {
  final dx1 = b.right - a.left, dx2 = a.right - b.left;
  final dy1 = b.bottom - a.top, dy2 = a.bottom - b.top;
  final dx = dx1 < dx2 ? dx1 : -dx2;
  final dy = dy1 < dy2 ? dy1 : -dy2;
  return dx.abs() < dy.abs() ? Offset(dx, 0) : Offset(0, dy);
}

class Testes extends StatefulWidget {
  const Testes({super.key});

  @override
  State<Testes> createState() => _TestesState();
}

class _TestesState extends State<Testes> {
  String modo = 'Círculos';
  Offset a = const Offset(120, 200);
  Offset b = const Offset(220, 260);
  double raio = 50;
  Size tamanho = const Size(110, 80);
  bool mostrarEmpurrao = true;

  Rect retA() => Rect.fromCenter(center: a, width: tamanho.width, height: tamanho.height);
  Rect retB() => Rect.fromCenter(center: b, width: 140, height: 100);

  bool colidindo() {
    if (modo == 'Círculos') return circulos(a, raio, b, raio);
    if (modo == 'Retângulos') return retangulos(retA(), retB());
    return circuloRetangulo(a, raio, retB());
  }

  @override
  Widget build(BuildContext context) {
    final bate = colidindo();
    return Scaffold(
      appBar: AppBar(title: Text(bate ? 'Colidindo!' : 'Separados'), backgroundColor: bate ? Colors.red.shade100 : null),
      body: Column(
        children: [
          Wrap(
            spacing: 6,
            children: [
              for (final m in ['Círculos', 'Retângulos', 'Círculo e retângulo'])
                ChoiceChip(label: Text(m), selected: modo == m, onSelected: (_) => setState(() => modo = m)),
            ],
          ),
          const Text('Arraste a forma laranja'),
          GestureDetector(
            onPanUpdate: (d) => setState(() => a = d.localPosition),
            child: CustomPaint(
              size: const Size(360, 480),
              painter: Formas(modo, a, b, raio, retA(), retB(), bate, mostrarEmpurrao && modo == 'Retângulos' && bate ? empurrao(retA(), retB()) : null),
            ),
          ),
        ],
      ),
    );
  }
}

class Formas extends CustomPainter {
  final String modo;
  final Offset a, b;
  final double raio;
  final Rect ra, rb;
  final bool bate;
  final Offset? empurra;
  Formas(this.modo, this.a, this.b, this.raio, this.ra, this.rb, this.bate, this.empurra);

  @override
  void paint(Canvas canvas, Size size) {
    final cinza = Paint()..color = bate ? const Color(0xAAE53935) : const Color(0xAA7A8AA0);
    final laranja = Paint()..color = const Color(0xCCD98B3A);
    if (modo == 'Círculos') {
      canvas.drawCircle(b, raio, cinza);
      canvas.drawCircle(a, raio, laranja);
      canvas.drawLine(a, b, Paint()..color = Colors.black54..strokeWidth = 2);
    } else if (modo == 'Retângulos') {
      canvas.drawRect(rb, cinza);
      canvas.drawRect(ra, laranja);
      final e = empurra;
      if (e != null) {
        canvas.drawRect(ra.shift(e), Paint()..color = Colors.green..style = PaintingStyle.stroke..strokeWidth = 2);
        canvas.drawLine(a, a + e, Paint()..color = Colors.green..strokeWidth = 4);
      }
    } else {
      canvas.drawRect(rb, cinza);
      canvas.drawCircle(a, raio, laranja);
      final p = Offset(a.dx.clamp(rb.left, rb.right).toDouble(), a.dy.clamp(rb.top, rb.bottom).toDouble());
      canvas.drawLine(a, p, Paint()..color = Colors.black54..strokeWidth = 2);
      canvas.drawCircle(p, 5, Paint()..color = Colors.black);
    }
  }

  @override
  bool shouldRepaint(Formas old) => true;
}
