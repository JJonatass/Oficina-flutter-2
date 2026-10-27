import 'package:audioplayers/audioplayers.dart';
import 'package:flutter/material.dart';
import 'package:flutter/scheduler.dart';

void main() => runApp(const MaterialApp(debugShowCheckedModeBanner: false, home: Ritmo()));

// a música: em que batida cada nota cai e em qual das 3 pistas
const partitura = [
  [4, 0], [5, 1], [6, 2], [7, 1],
  [8, 0], [8.5, 0], [9, 2], [10, 1],
  [11, 0], [11.5, 1], [12, 2], [13, 2],
  [14, 1], [14.5, 0], [15, 1],
];
const cores = [Color(0xFFEF5350), Color(0xFF66BB6A), Color(0xFF42A5F5)];

class Nota {
  final double batida;
  final int pista;
  String resultado = ''; // '', perfeito, bom ou errou
  Nota(this.batida, this.pista);
}

class Ritmo extends StatefulWidget {
  const Ritmo({super.key});

  @override
  State<Ritmo> createState() => _RitmoState();
}

class _RitmoState extends State<Ritmo> with SingleTickerProviderStateMixin {
  late Ticker ticker;
  final metronomo = AudioPlayer();
  final somAcerto = AudioPlayer();
  final double bpm = 100; // batidas por minuto
  final double janelaPerfeito = 0.06; // segundos de folga para "perfeito"
  final double janelaBom = 0.14;
  final double velocidade = 300; // pixels por segundo que as notas descem
  final double linhaAlvo = 300; // onde a nota deve ser tocada
  List<Nota> notas = [];
  double tempo = 0; // segundos desde o começo da música
  int batidaTocada = -1;
  bool tocando = false;
  int pontos = 0;
  int combo = 0;
  String aviso = 'Acerte as notas na linha branca.';

  double get segundosPorBatida => 60 / bpm;

  @override
  void initState() {
    super.initState();
    // o tempo da música vem do relógio do Ticker (agora), não de somar dt:
    // somar dt acumula pequenos erros e a música sai do ritmo
    ticker = createTicker((agora) {
      setState(() => passo(agora.inMicroseconds / 1000000));
    });
  }

  void comecar() {
    ticker.stop();
    setState(() {
      notas = [];
      for (final n in partitura) {
        notas.add(Nota(n[0].toDouble(), n[1].toInt()));
      }
      tempo = 0;
      batidaTocada = -1;
      pontos = 0;
      combo = 0;
      tocando = true;
      aviso = '';
    });
    ticker.start();
  }

  void passo(double t) {
    tempo = t;
    // metrônomo: um som a cada batida
    final batida = (tempo / segundosPorBatida).floor();
    if (batida > batidaTocada) {
      batidaTocada = batida;
      metronomo.play(AssetSource('sons/batida.wav'));
    }
    // nota que passou da linha sem ser tocada
    for (final n in notas) {
      if (n.resultado == '' && tempo - n.batida * segundosPorBatida > janelaBom) {
        n.resultado = 'errou';
        combo = 0;
        aviso = 'Errou!';
      }
    }
    if (tempo > (partitura.last[0] + 2) * segundosPorBatida) {
      tocando = false;
      ticker.stop();
      aviso = 'Fim! $pontos pontos.';
    }
  }

  void tocar(int pista) {
    if (!tocando) return;
    // a nota da pista mais perto do tempo de agora
    Nota? alvo;
    var menor = 999.0;
    for (final n in notas) {
      final diferenca = (tempo - n.batida * segundosPorBatida).abs();
      if (n.pista == pista && n.resultado == '' && diferenca < menor) {
        menor = diferenca;
        alvo = n;
      }
    }
    final a = alvo;
    if (a == null || menor > janelaBom) return; // longe demais: ignora o toque
    setState(() {
      combo++;
      if (menor <= janelaPerfeito) {
        a.resultado = 'perfeito';
        pontos += 100 * combo;
        aviso = 'Perfeito! x$combo';
      } else {
        a.resultado = 'bom';
        pontos += 50 * combo;
        aviso = 'Bom x$combo';
      }
    });
    somAcerto.play(AssetSource('sons/clique.wav'));
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
      body: Column(
        children: [
          CustomPaint(size: const Size(360, 340), painter: Pistas(notas, tempo, segundosPorBatida, velocidade, linhaAlvo)),
          SizedBox(height: 34, child: Text(aviso, style: const TextStyle(fontSize: 20))),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              for (var p = 0; p < 3; p++)
                GestureDetector(
                  onTapDown: (d) => tocar(p),
                  child: Container(
                    width: 100,
                    height: 60,
                    margin: const EdgeInsets.all(6),
                    decoration: BoxDecoration(color: cores[p], borderRadius: BorderRadius.circular(14)),
                  ),
                ),
            ],
          ),
          if (!tocando) FilledButton(onPressed: comecar, child: const Text('Começar')),
        ],
      ),
    );
  }
}

class Pistas extends CustomPainter {
  final List<Nota> notas;
  final double tempo;
  final double spb;
  final double velocidade;
  final double linhaAlvo;
  Pistas(this.notas, this.tempo, this.spb, this.velocidade, this.linhaAlvo);

  @override
  void paint(Canvas canvas, Size size) {
    canvas.drawRect(Rect.fromLTWH(0, 0, size.width, size.height), Paint()..color = const Color(0xFF1E2A3A));
    for (var p = 0; p < 3; p++) {
      canvas.drawRect(Rect.fromLTWH(18 + p * 112.0, 0, 100, size.height), Paint()..color = const Color(0xFF26364A));
    }
    canvas.drawRect(Rect.fromLTWH(0, linhaAlvo - 3, size.width, 6), Paint()..color = Colors.white70);
    for (final n in notas) {
      // quanto falta para a nota chegar na linha vira distância acima da linha
      final y = linhaAlvo - (n.batida * spb - tempo) * velocidade;
      if (y < -30 || y > size.height + 30) continue;
      final cor = n.resultado == 'perfeito'
          ? Colors.amber
          : (n.resultado == 'bom' ? Colors.white : (n.resultado == 'errou' ? Colors.black38 : cores[n.pista]));
      canvas.drawRRect(RRect.fromRectAndRadius(Rect.fromCenter(center: Offset(68 + n.pista * 112.0, y), width: 90, height: 26), const Radius.circular(10)), Paint()..color = cor);
    }
  }

  @override
  bool shouldRepaint(Pistas old) => true;
}
