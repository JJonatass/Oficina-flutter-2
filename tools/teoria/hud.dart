import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(debugShowCheckedModeBanner: false, home: Interface()));

class Interface extends StatefulWidget {
  const Interface({super.key});

  @override
  State<Interface> createState() => _InterfaceState();
}

class _InterfaceState extends State<Interface> {
  double escalaTexto = 1.0;
  double tamanhoBotao = 56;
  bool canhoto = false;
  bool coresSeguras = false;
  bool mostrarAreas = false;
  int vidas = 2;

  // vermelho e verde se confundem para quem tem daltonismo; azul e laranja, não
  Color get corBom => coresSeguras ? const Color(0xFF1E88E5) : const Color(0xFF43A047);
  Color get corRuim => coresSeguras ? const Color(0xFFFB8C00) : const Color(0xFFE53935);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Interface do jogo')),
      body: Column(
        children: [
          // a "tela do jogo", com o HUD por cima
          Container(
            height: 330,
            color: const Color(0xFF8FD3F4),
            child: Stack(
              children: [
                Positioned(
                  left: 12,
                  top: 10,
                  child: Row(
                    children: [
                      for (int i = 0; i < 3; i++)
                        Icon(i < vidas ? Icons.favorite : Icons.favorite_border, color: Colors.red, size: 28 * escalaTexto),
                      const SizedBox(width: 12),
                      Text('Ossos: 12', style: TextStyle(fontSize: 18 * escalaTexto, color: Colors.white, fontWeight: FontWeight.bold, shadows: const [Shadow(blurRadius: 4)])),
                    ],
                  ),
                ),
                Positioned(
                  right: 12,
                  top: 56,
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.end,
                    children: [
                      // cor E símbolo: a informação não depende só da cor
                      Aviso(texto: '✓ Porta aberta', cor: corBom, escala: escalaTexto),
                      const SizedBox(height: 6),
                      Aviso(texto: '✗ Ponte quebrada', cor: corRuim, escala: escalaTexto),
                    ],
                  ),
                ),
                Positioned(
                  left: canhoto ? null : 12,
                  right: canhoto ? 12 : null,
                  bottom: 12,
                  child: Row(children: [
                    Botao(icone: Icons.arrow_back, tamanho: tamanhoBotao, areas: mostrarAreas),
                    const SizedBox(width: 12),
                    Botao(icone: Icons.arrow_forward, tamanho: tamanhoBotao, areas: mostrarAreas),
                  ]),
                ),
                Positioned(
                  left: canhoto ? 12 : null,
                  right: canhoto ? null : 12,
                  bottom: 12,
                  child: Botao(icone: Icons.arrow_upward, tamanho: tamanhoBotao * 1.2, areas: mostrarAreas),
                ),
              ],
            ),
          ),
          Expanded(
            child: ListView(
              children: [
                ListTile(title: Text('Tamanho do texto: ${(escalaTexto * 100).round()}%')),
                Slider(value: escalaTexto, min: 0.8, max: 1.6, onChanged: (v) => setState(() => escalaTexto = v)),
                ListTile(title: Text('Tamanho dos botões: ${tamanhoBotao.round()}')),
                Slider(value: tamanhoBotao, min: 32, max: 80, onChanged: (v) => setState(() => tamanhoBotao = v)),
                SwitchListTile(title: const Text('Modo canhoto'), value: canhoto, onChanged: (v) => setState(() => canhoto = v)),
                SwitchListTile(title: const Text('Cores para daltonismo'), value: coresSeguras, onChanged: (v) => setState(() => coresSeguras = v)),
                SwitchListTile(title: const Text('Mostrar área mínima de toque (48)'), value: mostrarAreas, onChanged: (v) => setState(() => mostrarAreas = v)),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class Botao extends StatelessWidget {
  final IconData icone;
  final double tamanho;
  final bool areas;
  const Botao({super.key, required this.icone, required this.tamanho, required this.areas});

  @override
  Widget build(BuildContext context) {
    // menor que 48 é difícil de acertar com o dedo
    final pequeno = tamanho < 48;
    return Container(
      width: tamanho,
      height: tamanho,
      alignment: Alignment.center,
      decoration: BoxDecoration(
        color: Colors.black38,
        shape: BoxShape.circle,
        border: areas ? Border.all(color: pequeno ? Colors.red : Colors.greenAccent, width: 3) : null,
      ),
      child: Icon(icone, color: Colors.white, size: tamanho * 0.5),
    );
  }
}

class Aviso extends StatelessWidget {
  final String texto;
  final Color cor;
  final double escala;
  const Aviso({super.key, required this.texto, required this.cor, required this.escala});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
      decoration: BoxDecoration(color: cor, borderRadius: BorderRadius.circular(8)),
      child: Text(texto, style: TextStyle(color: Colors.white, fontSize: 14 * escala, fontWeight: FontWeight.bold)),
    );
  }
}
