import 'dart:async';
import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(debugShowCheckedModeBanner: false, home: Memoria()));

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
      cartas = [...figuras, ...figuras]..shuffle();
      achadas.clear();
      viradas.clear();
      jogadas = 0;
    });
  }

  void tocar(int i) {
    if (esperando || achadas.contains(i) || viradas.contains(i)) return;
    setState(() => viradas.add(i));
    if (viradas.length == 2) {
      jogadas++;
      final a = viradas[0], b = viradas[1];
      if (cartas[a] == cartas[b]) {
        setState(() {
          achadas.addAll([a, b]);
          viradas.clear();
        });
      } else {
        esperando = true;
        Timer(const Duration(seconds: 1), () => setState(() {
              viradas.clear();
              esperando = false;
            }));
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final venceu = achadas.length == cartas.length;
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
