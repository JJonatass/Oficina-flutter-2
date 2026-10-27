import 'package:flutter/material.dart';
import 'package:flutter/scheduler.dart';

void main() => runApp(const MaterialApp(debugShowCheckedModeBanner: false, home: Corrida()));

// passo fixo: o jogo sempre anda 1/60 de segundo por vez, em qualquer aparelho.
// Com o mesmo começo e as mesmas entradas, o resultado é sempre o mesmo.
const double passoFixo = 1 / 60;
const bandeiras = [Offset(300, 70), Offset(60, 180), Offset(290, 300), Offset(80, 380)];
const inicio = Offset(60, 60);
const corFantasma = Color(0x6690A4AE);

class Corredor {
  Offset pos = inicio;
  Offset vel = Offset.zero;
  int proxima = 0; // próxima bandeira a pegar

  // um passo da simulação: só depende do estado e da entrada (o dedo)
  void passo(Offset? dedo) {
    if (dedo != null) {
      final d = dedo - pos;
      if (d.distance > 1) vel += d / d.distance * 900 * passoFixo;
    }
    vel = vel * 0.94; // atrito
    pos += vel * passoFixo;
    if (proxima < bandeiras.length && (pos - bandeiras[proxima]).distance < 22) proxima++;
  }
}

class Corrida extends StatefulWidget {
  const Corrida({super.key});

  @override
  State<Corrida> createState() => _CorridaState();
}

class _CorridaState extends State<Corrida> with SingleTickerProviderStateMixin {
  late Ticker ticker;
  Duration anterior = Duration.zero;
  double acumulado = 0;
  String modo = 'pronto'; // pronto, correndo ou replay
  Corredor jogador = Corredor();
  Corredor fantasma = Corredor();
  Offset? dedo;
  int passos = 0;
  List<Offset?> entradas = []; // a gravação: o dedo em cada passo
  List<Offset?> ultima = [];
  List<Offset?> melhor = [];

  @override
  void initState() {
    super.initState();
    ticker = createTicker((agora) {
      final dt = (agora - anterior).inMicroseconds / 1000000;
      anterior = agora;
      if (dt <= 0 || dt > 0.1) return;
      setState(() {
        acumulado += dt;
        while (acumulado >= passoFixo) {
          acumulado -= passoFixo;
          passoDoJogo();
        }
      });
    });
    ticker.start();
  }

  void comecar(String novoModo) {
    setState(() {
      modo = novoModo;
      jogador = Corredor();
      fantasma = Corredor();
      passos = 0;
      entradas = [];
    });
  }

  void passoDoJogo() {
    if (modo == 'pronto') return;
    Offset? entrada;
    if (modo == 'correndo') {
      entrada = dedo;
      entradas.add(entrada); // grava o que o jogador fez neste passo
    } else {
      if (passos >= ultima.length) {
        modo = 'pronto';
        return;
      }
      entrada = ultima[passos]; // replay: repete o que foi gravado
    }
    jogador.passo(entrada);
    if (passos < melhor.length) fantasma.passo(melhor[passos]); // o fantasma repete a melhor corrida
    passos++;
    if (modo == 'correndo' && jogador.proxima == bandeiras.length) {
      modo = 'pronto';
      ultima = entradas;
      if (melhor.isEmpty || entradas.length < melhor.length) melhor = entradas;
    }
  }

  String segundos(int n) => (n * passoFixo).toStringAsFixed(2);

  @override
  void dispose() {
    ticker.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final tempo = segundos(passos);
    final recorde = melhor.isEmpty ? '--' : segundos(melhor.length);
    return Scaffold(
      appBar: AppBar(title: Text('Tempo $tempo s · recorde $recorde s')),
      body: Column(
        children: [
          GestureDetector(
            onPanStart: (d) => dedo = d.localPosition,
            onPanUpdate: (d) => dedo = d.localPosition,
            onPanEnd: (d) => dedo = null,
            child: CustomPaint(size: const Size(360, 440), painter: Pista(jogador, fantasma, melhor.isNotEmpty, modo == 'replay')),
          ),
          const SizedBox(height: 8),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              FilledButton(onPressed: () => comecar('correndo'), child: const Text('🏁 Correr')),
              const SizedBox(width: 12),
              OutlinedButton(onPressed: ultima.isEmpty ? null : () => comecar('replay'), child: const Text('▶ Ver replay')),
            ],
          ),
          Text('Gravação: ${entradas.length} entradas'),
        ],
      ),
    );
  }
}

class Pista extends CustomPainter {
  final Corredor jogador;
  final Corredor fantasma;
  final bool temFantasma;
  final bool replay;
  Pista(this.jogador, this.fantasma, this.temFantasma, this.replay);

  @override
  void paint(Canvas canvas, Size size) {
    canvas.drawRect(Rect.fromLTWH(0, 0, size.width, size.height), Paint()..color = const Color(0xFFDCEFD0));
    for (var i = 0; i < bandeiras.length; i++) {
      final pega = i < jogador.proxima;
      canvas.drawCircle(bandeiras[i], 22, Paint()..color = pega ? const Color(0xFF9CCC65) : const Color(0xFFFFB74D));
      final tp = TextPainter(text: TextSpan(text: '${i + 1}', style: const TextStyle(fontSize: 18, color: Colors.black)), textDirection: TextDirection.ltr)..layout();
      tp.paint(canvas, bandeiras[i] - Offset(tp.width / 2, tp.height / 2));
    }
    if (temFantasma) canvas.drawCircle(fantasma.pos, 16, Paint()..color = corFantasma);
    canvas.drawCircle(jogador.pos, 16, Paint()..color = replay ? const Color(0xFF64B5F6) : const Color(0xFFD68C3E));
  }

  @override
  bool shouldRepaint(Pista old) => true;
}
