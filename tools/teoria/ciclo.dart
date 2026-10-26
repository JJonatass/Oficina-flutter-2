import 'dart:math';
import 'package:flutter/material.dart';
import 'package:flutter/scheduler.dart';

void main() => runApp(const MaterialApp(home: Ciclo()));

class Ciclo extends StatefulWidget {
  const Ciclo({super.key});
  @override
  State<Ciclo> createState() => _CicloState();
}

class _CicloState extends State<Ciclo> with SingleTickerProviderStateMixin {
  final sorteio = Random();
  late Ticker ticker;
  Duration anterior = Duration.zero;

  // objetivo: pegar o osso antes que ele suma
  Offset osso = const Offset(180, 300);
  // desafio: o tempo para pegar cada osso
  double tempoLimite = 1.5;
  double restante = 1.5;
  // recompensa: pontos, e mais pontos para quem acerta em sequência
  int pontos = 0;
  int combo = 0;
  String aviso = 'Toque no osso!';

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
      restante -= dt;
      if (restante <= 0) {
        combo = 0;
        aviso = 'Escapou! O combo zerou.';
        novoOsso();
      }
    });
  }

  void novoOsso() {
    osso = Offset(40 + sorteio.nextDouble() * 280, 120 + sorteio.nextDouble() * 360);
    restante = tempoLimite;
  }

  void tocar(Offset p) {
    setState(() {
      if ((p - osso).distance < 36) {
        combo++;
        pontos += combo;
        aviso = combo > 1 ? 'Combo x$combo! +$combo' : '+1';
        novoOsso();
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
    return Scaffold(
      appBar: AppBar(title: Text('Pontos: $pontos   Combo: $combo')),
      body: GestureDetector(
        onTapDown: (e) => tocar(e.localPosition),
        child: CustomPaint(size: const Size(360, 560), painter: Tela(osso, restante / tempoLimite, aviso)),
      ),
    );
  }
}

class Tela extends CustomPainter {
  final Offset osso;
  final double fracao;
  final String aviso;
  Tela(this.osso, this.fracao, this.aviso);

  @override
  void paint(Canvas canvas, Size size) {
    canvas.drawRect(Rect.fromLTWH(0, 0, size.width, size.height), Paint()..color = const Color(0xFF3E6B3A));
    // a barra de tempo mostra o desafio: quanto falta para o osso sumir
    canvas.drawRect(Rect.fromLTWH(20, 20, 320, 14), Paint()..color = Colors.black26);
    canvas.drawRect(Rect.fromLTWH(20, 20, 320 * fracao.clamp(0, 1), 14), Paint()..color = fracao > 0.3 ? Colors.amber : Colors.redAccent);
    canvas.drawCircle(osso, 30, Paint()..color = Colors.white24);
    canvas.drawRRect(RRect.fromRectAndRadius(Rect.fromCenter(center: osso, width: 40, height: 10), const Radius.circular(5)), Paint()..color = const Color(0xFFFAF4E2));
    for (final dx in [-20.0, 20.0]) {
      for (final dy in [-5.0, 5.0]) {
        canvas.drawCircle(osso + Offset(dx, dy), 7, Paint()..color = const Color(0xFFFAF4E2));
      }
    }
    final texto = TextPainter(
      text: TextSpan(text: aviso, style: const TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold)),
      textDirection: TextDirection.ltr,
    )..layout();
    texto.paint(canvas, Offset((size.width - texto.width) / 2, size.height - 60));
  }

  @override
  bool shouldRepaint(covariant Tela antiga) => true;
}
