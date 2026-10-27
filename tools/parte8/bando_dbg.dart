import 'dart:math';
import 'package:flutter/material.dart';
import 'package:flutter/scheduler.dart';

void main() => runApp(const MaterialApp(debugShowCheckedModeBanner: false, home: Bando()));

class Pombo {
  Offset pos;
  Offset vel;
  Pombo(this.pos, this.vel);
}

// limita o tamanho de um vetor
Offset limitar(Offset v, double maximo) => v.distance > maximo ? v / v.distance * maximo : v;

class Bando extends StatefulWidget {
  const Bando({super.key});

  @override
  State<Bando> createState() => _BandoState();
}

class _BandoState extends State<Bando> with SingleTickerProviderStateMixin {
  final sorteio = Random(3);
  late Ticker ticker;
  Duration anterior = Duration.zero;
  List<Pombo> pombos = [];
  Offset? caramelo;
  // os três pesos do bando
  double separacao = 1.5;
  double alinhamento = 1.0;
  double coesao = 1.0;
  final double raioVisao = 70;
  int quadros = 0;
  final double velocidadeMax = 120;
  final int quantos = 24;

  @override
  void initState() {
    super.initState();
    pombos = List.generate(quantos, (_) => Pombo(Offset(sorteio.nextDouble() * 340 + 10, sorteio.nextDouble() * 380 + 10), Offset(sorteio.nextDouble() * 80 - 40, sorteio.nextDouble() * 80 - 40)));
    ticker = createTicker((agora) {
      final dt = (agora - anterior).inMicroseconds / 1000000;
      anterior = agora;
      if (dt <= 0 || dt > 0.1) return;
      setState(() {
        quadros++;
        passo(dt);
      });
    });
    ticker.start();
  }

  void passo(double dt) {
    for (final p in pombos) {
      var afasta = Offset.zero, direcao = Offset.zero, centro = Offset.zero;
      var vizinhos = 0;
      for (final o in pombos) {
        if (identical(o, p)) continue;
        final d = p.pos - o.pos;
        final dist = d.distance;
        if (dist < raioVisao && dist > 0) {
          vizinhos++;
          if (dist < 25) afasta += d / dist; // separação: só os muito perto
          direcao += o.vel; // alinhamento: voar para onde os vizinhos voam
          centro += o.pos; // coesão: ir para o meio do grupo
        }
      }
      var forca = Offset.zero;
      if (vizinhos > 0) {
        forca += afasta * 80 * separacao;
        forca += (direcao / vizinhos.toDouble() - p.vel) * alinhamento;
        forca += (centro / vizinhos.toDouble() - p.pos) * 0.8 * coesao;
      }
      // fugir do caramelo quando ele está perto
      final c = caramelo;
      if (c != null && (p.pos - c).distance < 110) {
        forca += (p.pos - c) / (p.pos - c).distance * 300;
      }
      // voltar quando chega perto da borda
      if (p.pos.dx < 20) forca += const Offset(200, 0);
      if (p.pos.dx > 340) forca += const Offset(-200, 0);
      if (p.pos.dy < 20) forca += const Offset(0, 200);
      if (p.pos.dy > 400) forca += const Offset(0, -200);
      p.vel = limitar(p.vel + forca * dt, velocidadeMax);
      // nunca para no ar: velocidade mínima
      if (p.vel.distance < 50) p.vel = p.vel.distance > 0 ? p.vel / p.vel.distance * 50 : const Offset(50, 0);
    }
    for (final p in pombos) {
      p.pos += p.vel * dt;
    }
  }

  @override
  void dispose() {
    ticker.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Bando de pombos $quadros')),
      body: Column(
        children: [
          GestureDetector(
            onPanUpdate: (d) => setState(() => caramelo = d.localPosition),
            onPanEnd: (d) => setState(() => caramelo = null),
            onTapDown: (d) => setState(() => caramelo = d.localPosition),
            child: CustomPaint(size: const Size(360, 420), painter: Ceu(pombos, caramelo)),
          ),
          Row(children: [
            SizedBox(width: 110, child: Text('Separação ${separacao.toStringAsFixed(1)}')),
            Expanded(child: Slider(value: separacao, min: 0, max: 3, onChanged: (v) => setState(() => separacao = v))),
          ]),
          Row(children: [
            SizedBox(width: 110, child: Text('Alinhamento ${alinhamento.toStringAsFixed(1)}')),
            Expanded(child: Slider(value: alinhamento, min: 0, max: 3, onChanged: (v) => setState(() => alinhamento = v))),
          ]),
          Row(children: [
            SizedBox(width: 110, child: Text('Coesão ${coesao.toStringAsFixed(1)}')),
            Expanded(child: Slider(value: coesao, min: 0, max: 3, onChanged: (v) => setState(() => coesao = v))),
          ]),
        ],
      ),
    );
  }
}

class Ceu extends CustomPainter {
  final List<Pombo> pombos;
  final Offset? caramelo;
  Ceu(this.pombos, this.caramelo);

  @override
  void paint(Canvas canvas, Size size) {
    canvas.drawRect(Rect.fromLTWH(0, 0, size.width, size.height), Paint()..color = const Color(0xFFBFE6F7));
    final tinta = Paint()..color = const Color(0xFF6B6F78);
    for (final p in pombos) {
      final frente = p.vel.distance > 0 ? p.vel / p.vel.distance : const Offset(1, 0);
      final lado = Offset(-frente.dy, frente.dx);
      final corpo = Path()
        ..moveTo(p.pos.dx + frente.dx * 9, p.pos.dy + frente.dy * 9)
        ..lineTo(p.pos.dx - frente.dx * 6 + lado.dx * 5, p.pos.dy - frente.dy * 6 + lado.dy * 5)
        ..lineTo(p.pos.dx - frente.dx * 6 - lado.dx * 5, p.pos.dy - frente.dy * 6 - lado.dy * 5)
        ..close();
      canvas.drawPath(corpo, tinta);
    }
    final c = caramelo;
    if (c != null) {
      canvas.drawCircle(c, 110, Paint()..color = const Color(0x22D98B3A));
      canvas.drawCircle(c, 14, Paint()..color = const Color(0xFFD98B3A));
    }
  }

  @override
  bool shouldRepaint(Ceu old) => true;
}
