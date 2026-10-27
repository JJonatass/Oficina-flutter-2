import 'package:flutter/material.dart';
import 'package:flutter/scheduler.dart';

void main() => runApp(const MaterialApp(debugShowCheckedModeBanner: false, home: QuebraBlocos()));

// DESAFIO · QUEBRA-BLOCOS
// 1. Uma raquete embaixo segue o dedo (arrastar na horizontal).
// 2. Uma bola anda sozinha (Ticker + dt) e quica nas paredes, no teto e na raquete.
// 3. No alto, 5 fileiras de 6 blocos. A bola quebra o bloco em que bate e volta.
// 4. Cada bloco vale 10 pontos. Sem blocos: vitória. Se a bola cair embaixo da raquete: perde uma vida (3 vidas).
// Os blocos, o desenho, os quiques e as vidas já estão prontos. Complete as partes marcadas com FAÇA.

const double largura = 360;
const double altura = 520;

class QuebraBlocos extends StatefulWidget {
  const QuebraBlocos({super.key});

  @override
  State<QuebraBlocos> createState() => _QuebraBlocosState();
}

class _QuebraBlocosState extends State<QuebraBlocos> with SingleTickerProviderStateMixin {
  Ticker? ticker;
  Duration anterior = Duration.zero;
  double raqueteX = 180;
  Offset bola = const Offset(180, 400);
  Offset vel = const Offset(150, -260);
  List<Rect> blocos = [];
  int pontos = 0;
  int vidas = 3;

  @override
  void initState() {
    super.initState();
    montar();
    // FAÇA 2: crie o Ticker do State (como na aula 2, Ticker e delta time) e guarde em ticker.
    // A cada quadro: dt = (agora - anterior).inMicroseconds / 1000000; anterior = agora;
    // ignore dt <= 0 ou dt > 0.05; e chame setState(() => mover(dt)). Depois, ticker!.start().
  }

  void montar() {
    blocos = [];
    for (int l = 0; l < 5; l++) {
      for (int c = 0; c < 6; c++) {
        blocos.add(Rect.fromLTWH(12 + c * 57.0, 40 + l * 26.0, 52, 20));
      }
    }
  }

  Rect get raquete => Rect.fromCenter(center: Offset(raqueteX, altura - 30), width: 80, height: 14);

  void mover(double dt) {
    if (vidas == 0 || blocos.isEmpty) return;
    bola += vel * dt;
    if (bola.dx < 8 || bola.dx > largura - 8) vel = Offset(-vel.dx, vel.dy);
    if (bola.dy < 8) vel = Offset(vel.dx, vel.dy.abs());
    final r = Rect.fromCircle(center: bola, radius: 8);
    if (vel.dy > 0 && r.overlaps(raquete)) {
      // onde bateu na raquete muda o ângulo
      final desvio = (bola.dx - raqueteX) / 40;
      vel = Offset(desvio * 220, -vel.dy.abs());
    }
    for (int i = 0; i < blocos.length; i++) {
      if (r.overlaps(blocos[i])) {
        // FAÇA 3: tire da lista o bloco i, some 10 pontos e inverta vel.dy.
        break;
      }
    }
    if (bola.dy > altura) {
      vidas--;
      bola = Offset(raqueteX, altura - 60);
      vel = const Offset(150, -260);
    }
  }

  @override
  void dispose() {
    ticker?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final titulo = vidas == 0 ? 'Fim! $pontos pontos' : (blocos.isEmpty ? 'Venceu! $pontos pontos' : 'Pontos: $pontos   ${'♥' * vidas}');
    return Scaffold(
      appBar: AppBar(title: Text(titulo), actions: [
        IconButton(
          icon: const Icon(Icons.refresh),
          onPressed: () => setState(() {
            montar();
            pontos = 0;
            vidas = 3;
            bola = const Offset(180, 400);
            vel = const Offset(150, -260);
          }),
        ),
      ]),
      // FAÇA 1: envolva o CustomPaint num GestureDetector que, ao arrastar,
      // muda raqueteX para d.localPosition.dx (limitado entre 40 e largura - 40 com clamp).
      body: CustomPaint(size: const Size(largura, altura), painter: Quadra(blocos, bola, raquete)),
    );
  }
}

class Quadra extends CustomPainter {
  final List<Rect> blocos;
  final Offset bola;
  final Rect raquete;
  Quadra(this.blocos, this.bola, this.raquete);

  @override
  void paint(Canvas canvas, Size size) {
    canvas.drawRect(Rect.fromLTWH(0, 0, size.width, size.height), Paint()..color = const Color(0xFF1E2A3A));
    for (final b in blocos) {
      final cor = Color.lerp(const Color(0xFFFF8A65), const Color(0xFF64B5F6), (b.top - 40) / 110)!;
      canvas.drawRRect(RRect.fromRectAndRadius(b, const Radius.circular(4)), Paint()..color = cor);
    }
    canvas.drawRRect(RRect.fromRectAndRadius(raquete, const Radius.circular(7)), Paint()..color = const Color(0xFFD68C3E));
    canvas.drawCircle(bola, 8, Paint()..color = Colors.white);
  }

  @override
  bool shouldRepaint(Quadra old) => true;
}
