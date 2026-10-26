import 'package:audioplayers/audioplayers.dart';
import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(home: Mesa()));

// Cada efeito com o seu "envelope": ataque, decaimento, sustentação e soltura (em segundos e volume)
class Envelope {
  final double ataque;
  final double decaimento;
  final double sustentacao;
  final double soltura;
  const Envelope(this.ataque, this.decaimento, this.sustentacao, this.soltura);
}

const efeitos = {
  'pulo': Envelope(0.01, 0.08, 0.5, 0.08),
  'osso': Envelope(0.01, 0.05, 0.7, 0.2),
  'latido': Envelope(0.01, 0.04, 0.6, 0.06),
  'batida': Envelope(0.0, 0.12, 0.0, 0.0),
  'explosao': Envelope(0.0, 0.3, 0.3, 0.3),
  'vitoria': Envelope(0.01, 0.1, 0.8, 0.3),
};

class Mesa extends StatefulWidget {
  const Mesa({super.key});
  @override
  State<Mesa> createState() => _MesaState();
}

class _MesaState extends State<Mesa> {
  final efeito = AudioPlayer();
  final musica = AudioPlayer();
  String escolhido = 'pulo';
  double volumeEfeitos = 1.0;
  double volumeMusica = 0.4;
  bool tocandoMusica = false;

  void tocar(String nome) {
    setState(() => escolhido = nome);
    efeito.setVolume(volumeEfeitos);
    efeito.play(AssetSource('sons/$nome.wav'));
  }

  void alternarMusica() {
    setState(() => tocandoMusica = !tocandoMusica);
    if (tocandoMusica) {
      musica.setReleaseMode(ReleaseMode.loop);
      musica.setVolume(volumeMusica);
      musica.play(AssetSource('sons/musica_aventura.mp3'));
    } else {
      musica.stop();
    }
  }

  @override
  void dispose() {
    efeito.dispose();
    musica.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Mesa de som')),
      body: ListView(padding: const EdgeInsets.all(16), children: [
        Wrap(spacing: 8, runSpacing: 8, children: [
          for (final nome in efeitos.keys)
            ElevatedButton(onPressed: () => tocar(nome), child: Text(nome)),
        ]),
        const SizedBox(height: 16),
        Text('Envelope de "$escolhido"', style: const TextStyle(fontWeight: FontWeight.bold)),
        CustomPaint(size: const Size(320, 140), painter: Desenho(efeitos[escolhido]!)),
        const SizedBox(height: 16),
        Text('Volume dos efeitos: ${(volumeEfeitos * 100).round()}%'),
        Slider(value: volumeEfeitos, onChanged: (v) => setState(() => volumeEfeitos = v)),
        Text('Volume da música: ${(volumeMusica * 100).round()}%'),
        Slider(value: volumeMusica, onChanged: (v) {
          setState(() => volumeMusica = v);
          musica.setVolume(v);
        }),
        ElevatedButton.icon(
          onPressed: alternarMusica,
          icon: Icon(tocandoMusica ? Icons.stop : Icons.play_arrow),
          label: Text(tocandoMusica ? 'Parar a música' : 'Tocar a música'),
        ),
      ]),
    );
  }
}

class Desenho extends CustomPainter {
  final Envelope e;
  Desenho(this.e);

  @override
  void paint(Canvas canvas, Size size) {
    canvas.drawRect(Rect.fromLTWH(0, 0, size.width, size.height), Paint()..color = const Color(0xFF14213D));
    const segura = 0.15;
    final total = e.ataque + e.decaimento + segura + e.soltura;
    double x(double t) => 10 + (size.width - 20) * t / total;
    double y(double v) => size.height - 10 - (size.height - 20) * v;
    final caminho = Path()
      ..moveTo(x(0), y(0))
      ..lineTo(x(e.ataque), y(1))
      ..lineTo(x(e.ataque + e.decaimento), y(e.sustentacao))
      ..lineTo(x(e.ataque + e.decaimento + segura), y(e.sustentacao))
      ..lineTo(x(total), y(0));
    canvas.drawPath(caminho, Paint()..color = Colors.amber..style = PaintingStyle.stroke..strokeWidth = 3);
  }

  @override
  bool shouldRepaint(covariant Desenho antigo) => antigo.e != e;
}
