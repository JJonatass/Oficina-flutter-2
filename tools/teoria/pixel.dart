import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(home: PixelArt()));

// O desenho do caramelo: cada letra é um pixel, e a paleta diz a cor de cada letra.
const desenho = [
  '................',
  '................',
  '..........DD....',
  '..D.......DCCC..',
  '..D......CCkCC..',
  '..D......CCCCLLk',
  '...D.....CCCLLL.',
  '...DC...CCCC.t..',
  '....CCCCCCCC....',
  '...CCCCCCCCCC...',
  '...CCCCCCCCCC...',
  '...CLLLLLLLLC...',
  '...C.C....C.C...',
  '...C.C....C.C...',
  '...D.D....D.D...',
  '................',
];

const paletas = {
  'Caramelo': {'C': Color(0xFFD68C3E), 'D': Color(0xFFA0602A), 'L': Color(0xFFF6CE96), 'k': Color(0xFF222034), 't': Color(0xFFEC6878)},
  'Pretinho': {'C': Color(0xFF2B2B33), 'D': Color(0xFF15151A), 'L': Color(0xFFD9D4C7), 'k': Color(0xFFFFFFFF), 't': Color(0xFFEC6878)},
  'Malhado': {'C': Color(0xFFF2EEE6), 'D': Color(0xFF6B4A2E), 'L': Color(0xFFC9A27A), 'k': Color(0xFF222034), 't': Color(0xFFEC6878)},
};

class PixelArt extends StatefulWidget {
  const PixelArt({super.key});
  @override
  State<PixelArt> createState() => _PixelArtState();
}

class _PixelArtState extends State<PixelArt> {
  String paleta = 'Caramelo';
  bool grade = true;
  double tamanhoPixel = 18;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Pixel art: 16 × 16')),
      body: Column(children: [
        Wrap(spacing: 8, children: [
          for (final nome in paletas.keys)
            ChoiceChip(label: Text(nome), selected: paleta == nome, onSelected: (_) => setState(() => paleta = nome)),
        ]),
        SwitchListTile(title: const Text('Mostrar a grade'), value: grade, onChanged: (v) => setState(() => grade = v)),
        CustomPaint(size: Size(16 * tamanhoPixel, 16 * tamanhoPixel), painter: Pixels(paletas[paleta]!, grade, tamanhoPixel)),
        const SizedBox(height: 12),
        Row(mainAxisAlignment: MainAxisAlignment.center, children: [
          const Text('Tamanho real: '),
          CustomPaint(size: const Size(32, 32), painter: Pixels(paletas[paleta]!, false, 2)),
        ]),
      ]),
    );
  }
}

class Pixels extends CustomPainter {
  final Map<String, Color> cores;
  final bool grade;
  final double lado;
  Pixels(this.cores, this.grade, this.lado);

  @override
  void paint(Canvas canvas, Size size) {
    for (var y = 0; y < desenho.length; y++) {
      for (var x = 0; x < desenho[y].length; x++) {
        final letra = desenho[y][x];
        final cor = cores[letra];
        if (cor != null) {
          canvas.drawRect(Rect.fromLTWH(x * lado, y * lado, lado, lado), Paint()..color = cor);
        }
        if (grade) {
          canvas.drawRect(Rect.fromLTWH(x * lado, y * lado, lado, lado), Paint()..color = Colors.black12..style = PaintingStyle.stroke);
        }
      }
    }
  }

  @override
  bool shouldRepaint(covariant Pixels antigo) => true;
}
