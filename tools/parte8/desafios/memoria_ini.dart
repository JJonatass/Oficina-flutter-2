import 'dart:async';
import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(debugShowCheckedModeBanner: false, home: Memoria()));

// DESAFIO · JOGO DA MEMÓRIA
// 1. 12 cartas viradas para baixo, com 6 pares de figuras, embaralhadas.
// 2. Tocar numa carta vira ela. Com duas viradas: se forem iguais, ficam abertas; se não, desviram depois de 1 segundo.
// 3. Conte as jogadas (cada par tentado é uma jogada).
// 4. Quando todos os pares estiverem abertos, mostre "Você venceu em N jogadas!" e um botão para jogar de novo.
// As cartas, o toque e o desenho já estão prontos. Complete as partes marcadas com FAÇA.

const figuras = ['🦴', '🐱', '🎾', '🐾', '🍖', '🏠'];

class Memoria extends StatefulWidget {
  const Memoria({super.key});

  @override
  State<Memoria> createState() => _MemoriaState();
}

class _MemoriaState extends State<Memoria> {
  List<String> cartas = [];
  final Set<int> achadas = {};
  final List<int> viradas = [];
  int jogadas = 0;
  bool esperando = false;

  @override
  void initState() {
    super.initState();
    embaralhar();
  }

  void embaralhar() {
    setState(() {
      // FAÇA 1: as cartas estão sempre na mesma ordem. Embaralhe a lista (o método de List que mistura os itens).
      cartas = [...figuras, ...figuras];
      achadas.clear();
      viradas.clear();
      jogadas = 0;
    });
  }

  void tocar(int i) {
    if (esperando || achadas.contains(i) || viradas.contains(i)) return;
    setState(() => viradas.add(i));
    // FAÇA 2: quando houver duas cartas viradas:
    //   - conte uma jogada;
    //   - se as figuras forem iguais (cartas[a] == cartas[b]), ponha as duas em achadas e limpe viradas;
    //   - se não, marque esperando = true e, depois de 1 segundo (Timer), limpe viradas e volte esperando para false.
  }

  @override
  Widget build(BuildContext context) {
    // FAÇA 3: venceu quando o número de cartas achadas for igual ao número de cartas.
    final venceu = false;
    return Scaffold(
      appBar: AppBar(title: Text(venceu ? 'Você venceu em $jogadas jogadas!' : 'Jogadas: $jogadas')),
      body: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          children: [
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: [
                for (int i = 0; i < cartas.length; i++)
                  GestureDetector(
                    onTap: () => tocar(i),
                    child: Container(
                      width: 100,
                      height: 100,
                      alignment: Alignment.center,
                      decoration: BoxDecoration(
                        color: achadas.contains(i) ? Colors.green.shade100 : (viradas.contains(i) ? Colors.white : const Color(0xFFD68C3E)),
                        borderRadius: BorderRadius.circular(12),
                        border: Border.all(color: Colors.brown, width: 2),
                      ),
                      child: Text(achadas.contains(i) || viradas.contains(i) ? cartas[i] : '?', style: const TextStyle(fontSize: 40)),
                    ),
                  ),
              ],
            ),
            const SizedBox(height: 16),
            if (venceu) FilledButton(onPressed: embaralhar, child: const Text('Jogar de novo')),
          ],
        ),
      ),
    );
  }
}
