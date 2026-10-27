import 'package:flutter/material.dart';
import 'package:flutter/scheduler.dart';

void main() => runApp(const MaterialApp(debugShowCheckedModeBanner: false, home: Passos()));

// a bola sai da esquerda, rápida, em direção a uma parede fina
const double paredeX = 260;
const double paredeLargura = 6;
const double gravidade = 600;

class Bola {
  Offset pos = const Offset(20, 120);
  Offset vel = const Offset(900, -150);
  bool bateu = false;
  final List<Offset> rastro = [];
}

class Passos extends StatefulWidget {
  const Passos({super.key});

  @override
  State<Passos> createState() => _PassosState();
}

class _PassosState extends State<Passos> with SingleTickerProviderStateMixin {
  late Ticker ticker;
  Duration anterior = Duration.zero;
  // quantos quadros por segundo o aparelho consegue desenhar (simulado)
  int fps = 60;
  bool passoFixo = false;
  // tamanho de cada passo da física quando passoFixo está ligado
  double passo = 1 / 120;
  double sobra = 0;
  double relogioQuadro = 0;
  Bola bola = Bola();

  @override
  void initState() {
    super.initState();
    ticker = createTicker((agora) {
      final dt = (agora - anterior).inMicroseconds / 1000000;
      anterior = agora;
      if (dt <= 0 || dt > 0.1) return;
      // um aparelho lento só entrega um quadro a cada 1/fps segundos
      relogioQuadro += dt;
      if (relogioQuadro < 1 / fps) return;
      final dtQuadro = relogioQuadro;
      relogioQuadro = 0;
      setState(() {
        if (passoFixo) {
          // vários passos pequenos e iguais por quadro
          sobra += dtQuadro;
          while (sobra >= passo) {
            fisica(passo);
            sobra -= passo;
          }
        } else {
          // um passo do tamanho do quadro (pode ser enorme)
          fisica(dtQuadro);
        }
        if (bola.pos.dy > 560 || bola.pos.dx > 400) bola = Bola();
      });
    });
    ticker.start();
  }

  // Euler semi-implícito: primeiro a velocidade, depois a posição
  void fisica(double dt) {
    bola.vel = Offset(bola.vel.dx, bola.vel.dy + gravidade * dt);
    final antes = bola.pos;
    bola.pos = bola.pos + bola.vel * dt;
    // a parede só é vista se a bola estiver DENTRO dela neste passo
    if (!bola.bateu && bola.pos.dx >= paredeX && bola.pos.dx <= paredeX + paredeLargura && bola.pos.dy > 60) {
      bola.bateu = true;
      bola.vel = Offset(-bola.vel.dx * 0.5, bola.vel.dy);
      bola.pos = Offset(paredeX - 1, bola.pos.dy);
    }
    if (antes != bola.pos) bola.rastro.add(bola.pos);
  }

  @override
  void dispose() {
    ticker.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(bola.bateu ? 'Bateu na parede' : 'Bola voando')),
      body: Column(
        children: [
          Wrap(
            spacing: 6,
            children: [
              for (final f in [60, 20, 8])
                ChoiceChip(label: Text('$f fps'), selected: fps == f, onSelected: (_) => setState(() => fps = f)),
            ],
          ),
          SwitchListTile(title: const Text('Passo fixo (vários passos pequenos)'), value: passoFixo, onChanged: (v) => setState(() => passoFixo = v)),
          CustomPaint(size: const Size(360, 440), painter: Cena(bola)),
        ],
      ),
    );
  }
}

class Cena extends CustomPainter {
  final Bola bola;
  Cena(this.bola);

  @override
  void paint(Canvas canvas, Size size) {
    canvas.drawRect(Rect.fromLTWH(0, 0, size.width, size.height), Paint()..color = const Color(0xFFEFF4FA));
    canvas.drawRect(const Rect.fromLTWH(paredeX, 60, paredeLargura, 380), Paint()..color = const Color(0xFF3D4A5C));
    for (final p in bola.rastro) {
      canvas.drawCircle(p, 3, Paint()..color = const Color(0x88D98B3A));
    }
    canvas.drawCircle(bola.pos, 10, Paint()..color = const Color(0xFFD98B3A));
  }

  @override
  bool shouldRepaint(Cena old) => true;
}
