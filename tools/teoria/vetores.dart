import 'package:flutter/material.dart';
import 'package:flutter/scheduler.dart';

void main() => runApp(const MaterialApp(home: Vetores()));

class Vetores extends StatefulWidget {
  const Vetores({super.key});
  @override
  State<Vetores> createState() => _VetoresState();
}

class _VetoresState extends State<Vetores> with SingleTickerProviderStateMixin {
  late Ticker ticker;
  Duration anterior = Duration.zero;
  Offset caramelo = const Offset(180, 300);
  Offset alvo = const Offset(280, 160);
  double velocidade = 120;

  @override
  void initState() {
    super.initState();
    ticker = createTicker(quadro)..start();
  }

  void quadro(Duration agora) {
    final dt = (agora - anterior).inMicroseconds / 1000000;
    anterior = agora;
    if (dt <= 0 || dt > 0.1) return;
    setState(() {
      final d = alvo - caramelo;
      if (d.distance > 2) {
        final direcao = d / d.distance;
        caramelo += direcao * velocidade * dt;
      }
    });
  }

  @override
  void dispose() {
    ticker.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final d = alvo - caramelo;
    return Scaffold(
      appBar: AppBar(title: Text('d = (${d.dx.round()}, ${d.dy.round()})  |d| = ${d.distance.toStringAsFixed(0)}')),
      body: GestureDetector(
        onPanDown: (e) => setState(() => alvo = e.localPosition),
        onPanUpdate: (e) => setState(() => alvo = e.localPosition),
        child: CustomPaint(size: const Size(360, 560), painter: Plano(caramelo, alvo)),
      ),
    );
  }
}

class Plano extends CustomPainter {
  final Offset caramelo;
  final Offset alvo;
  Plano(this.caramelo, this.alvo);

  static const double escalaSeta = 60;

  void seta(Canvas canvas, Offset de, Offset ate, Color cor, double grossura) {
    final tinta = Paint()..color = cor..strokeWidth = grossura..strokeCap = StrokeCap.round;
    canvas.drawLine(de, ate, tinta);
    final d = ate - de;
    if (d.distance < 1) return;
    final u = d / d.distance;
    final lado = Offset(-u.dy, u.dx);
    canvas.drawLine(ate, ate - u * 12 + lado * 6, tinta);
    canvas.drawLine(ate, ate - u * 12 - lado * 6, tinta);
  }

  @override
  void paint(Canvas canvas, Size size) {
    canvas.drawRect(Rect.fromLTWH(0, 0, size.width, size.height), Paint()..color = const Color(0xFF14213D));
    final grade = Paint()..color = Colors.white10;
    for (double x = 0; x < size.width; x += 40) {
      canvas.drawLine(Offset(x, 0), Offset(x, size.height), grade);
    }
    for (double y = 0; y < size.height; y += 40) {
      canvas.drawLine(Offset(0, y), Offset(size.width, y), grade);
    }
    final d = alvo - caramelo;
    // componentes: quanto andar em x e quanto andar em y
    canvas.drawLine(caramelo, Offset(alvo.dx, caramelo.dy), Paint()..color = Colors.redAccent..strokeWidth = 2);
    canvas.drawLine(Offset(alvo.dx, caramelo.dy), alvo, Paint()..color = Colors.lightGreenAccent..strokeWidth = 2);
    // o vetor inteiro, do caramelo até o dedo
    seta(canvas, caramelo, alvo, Colors.white, 3);
    // o vetor unitário (tamanho 1), aumentado para aparecer
    if (d.distance > 1) seta(canvas, caramelo, caramelo + d / d.distance * escalaSeta, Colors.amber, 5);
    canvas.drawCircle(alvo, 8, Paint()..color = Colors.white);
    canvas.drawCircle(caramelo, 14, Paint()..color = const Color(0xFFD68C3E));
  }

  @override
  bool shouldRepaint(covariant Plano antigo) => true;
}
