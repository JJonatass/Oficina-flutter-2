import 'dart:math';
import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(debugShowCheckedModeBanner: false, home: Radar()));

// As oito "estéticas" do MDA: os tipos de diversão que um jogo pode dar
const esteticas = ['Sensação', 'Fantasia', 'Narrativa', 'Desafio', 'Companhia', 'Descoberta', 'Expressão', 'Passatempo'];

// quanto cada jogo da Oficina oferece de cada estética (0 a 5)
const jogos = {
  'Cobrinha': [3, 1, 0, 4, 0, 1, 0, 5],
  'Trilha do Caramelo': [4, 3, 2, 4, 0, 3, 0, 2],
  'Diálogos': [1, 4, 5, 1, 0, 3, 2, 1],
  'Multijogador': [3, 2, 0, 3, 5, 1, 1, 3],
};

class Radar extends StatefulWidget {
  const Radar({super.key});

  @override
  State<Radar> createState() => _RadarState();
}

class _RadarState extends State<Radar> {
  String escolhido = 'Cobrinha';
  List<double> valores = [];
  final Color corRadar = const Color(0xFFD68C3E);

  @override
  void initState() {
    super.initState();
    escolher('Cobrinha');
  }

  void escolher(String nome) {
    setState(() {
      escolhido = nome;
      valores = jogos[nome]!.map((v) => v.toDouble()).toList();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Diversão de: $escolhido')),
      body: ListView(
        padding: const EdgeInsets.all(12),
        children: [
          Wrap(
            spacing: 6,
            children: [
              for (final nome in jogos.keys)
                ChoiceChip(label: Text(nome), selected: nome == escolhido, onSelected: (_) => escolher(nome)),
            ],
          ),
          Center(child: CustomPaint(size: const Size(320, 300), painter: Teia(valores, corRadar))),
          for (var i = 0; i < 8; i++)
            Row(
              children: [
                SizedBox(width: 100, child: Text(esteticas[i])),
                Expanded(
                  child: Slider(value: valores[i], min: 0, max: 5, divisions: 5, onChanged: (v) => setState(() => valores[i] = v)),
                ),
              ],
            ),
        ],
      ),
    );
  }
}

// gráfico de radar: um eixo por estética, o polígono mostra o "formato" da diversão
class Teia extends CustomPainter {
  final List<double> valores;
  final Color cor;
  Teia(this.valores, this.cor);

  @override
  void paint(Canvas canvas, Size size) {
    final centro = Offset(size.width / 2, size.height / 2);
    const raio = 110.0;
    final linha = Paint()
      ..color = Colors.black26
      ..style = PaintingStyle.stroke;
    for (var anel = 1; anel <= 5; anel++) {
      canvas.drawCircle(centro, raio * anel / 5, linha);
    }
    final forma = Path();
    for (var i = 0; i < 8; i++) {
      final ang = -pi / 2 + i * 2 * pi / 8;
      final ponta = centro + Offset(cos(ang), sin(ang)) * raio;
      canvas.drawLine(centro, ponta, linha);
      final tp = TextPainter(text: TextSpan(text: esteticas[i], style: const TextStyle(fontSize: 11, color: Colors.black87)), textDirection: TextDirection.ltr)..layout();
      final rotulo = centro + Offset(cos(ang), sin(ang)) * (raio + 18);
      tp.paint(canvas, rotulo - Offset(tp.width / 2, tp.height / 2));
      final p = centro + Offset(cos(ang), sin(ang)) * (raio * valores[i] / 5);
      if (i == 0) {
        forma.moveTo(p.dx, p.dy);
      } else {
        forma.lineTo(p.dx, p.dy);
      }
    }
    forma.close();
    canvas.drawPath(forma, Paint()..color = cor.withOpacity(0.45));
    canvas.drawPath(
      forma,
      Paint()
        ..color = cor
        ..style = PaintingStyle.stroke
        ..strokeWidth = 2,
    );
  }

  @override
  bool shouldRepaint(Teia old) => true;
}
