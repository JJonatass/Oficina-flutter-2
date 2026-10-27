import 'dart:math';
import 'package:flutter/material.dart';
import 'package:flutter/scheduler.dart';

void main() => runApp(const MaterialApp(home: Dificuldade()));

// quantos inimigos por segundo, em função do tempo de partida (em segundos)
double reta(double t) => 0.5 + t * 0.05;
double degraus(double t) => 0.5 + (t / 15).floor() * 0.6;
double ondas(double t) => 0.5 + t * 0.04 + 0.5 * sin(t * 0.6);

class Dificuldade extends StatefulWidget {
  const Dificuldade({super.key});
  @override
  State<Dificuldade> createState() => _DificuldadeState();
}

class _DificuldadeState extends State<Dificuldade> with SingleTickerProviderStateMixin {
  final sorteio = Random();
  late Ticker ticker;
  Duration anterior = Duration.zero;
  double tempo = 0;
  double acumulado = 0;
  int escolhida = 2;
  double duracaoPartida = 60;
  final gotas = <Offset>[];

  final curvas = [reta, degraus, ondas];

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
      tempo = (tempo + dt) % duracaoPartida;
      final curva = curvas[escolhida];
      acumulado += curva(tempo) * dt;
      while (acumulado >= 1) {
        acumulado -= 1;
        gotas.add(Offset(20 + sorteio.nextDouble() * 320, 300));
      }
      for (var i = 0; i < gotas.length; i++) {
        gotas[i] = gotas[i] + Offset(0, 160 * dt);
      }
      gotas.removeWhere((g) => g.dy > 560);
    });
  }

  @override
  void dispose() {
    ticker.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final nomes = ['Reta', 'Degraus', 'Ondas'];
    final curva = curvas[escolhida];
    return Scaffold(
      appBar: AppBar(title: Text('${nomes[escolhida]}: ${curva(tempo).toStringAsFixed(1)} por segundo')),
      body: Column(children: [
        Row(mainAxisAlignment: MainAxisAlignment.spaceEvenly, children: [
          for (var i = 0; i < 3; i++)
            ChoiceChip(label: Text(nomes[i]), selected: escolhida == i, onSelected: (_) => setState(() => escolhida = i)),
        ]),
        CustomPaint(size: const Size(360, 500), painter: Grafico(tempo, duracaoPartida, escolhida, gotas)),
      ]),
    );
  }
}

class Grafico extends CustomPainter {
  final double tempo;
  final double duracao;
  final int escolhida;
  final List<Offset> gotas;
  Grafico(this.tempo, this.duracao, this.escolhida, this.gotas);

  @override
  void paint(Canvas canvas, Size size) {
    canvas.drawRect(Rect.fromLTWH(0, 0, size.width, size.height), Paint()..color = const Color(0xFF14213D));
    const area = Rect.fromLTWH(30, 20, 310, 220);
    canvas.drawRect(area, Paint()..color = Colors.white10);
    final cores = [Colors.white, Colors.lightBlueAccent, Colors.amber];
    final funcoes = [reta, degraus, ondas];
    for (var c = 0; c < 3; c++) {
      final caminho = Path();
      for (var i = 0; i <= 120; i++) {
        final t = duracao * i / 120;
        final x = area.left + area.width * i / 120;
        final y = area.bottom - area.height * (funcoes[c](t) / 4).clamp(0.0, 1.0);
        if (i == 0) {
          caminho.moveTo(x, y);
        } else {
          caminho.lineTo(x, y);
        }
      }
      canvas.drawPath(caminho, Paint()
        ..color = c == escolhida ? cores[c] : cores[c].withOpacity(0.25)
        ..style = PaintingStyle.stroke
        ..strokeWidth = c == escolhida ? 3 : 1.5);
    }
    final xAgora = area.left + area.width * tempo / duracao;
    canvas.drawLine(Offset(xAgora, area.top), Offset(xAgora, area.bottom), Paint()..color = Colors.redAccent..strokeWidth = 2);
    for (final g in gotas) {
      canvas.drawRect(Rect.fromCenter(center: g, width: 14, height: 14), Paint()..color = Colors.brown.shade300);
    }
  }

  @override
  bool shouldRepaint(covariant Grafico antigo) => true;
}
