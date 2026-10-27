import 'dart:math';
import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(debugShowCheckedModeBanner: false, home: Combina()));

const pecas = ['🦴', '🐾', '⚽', '🍖', '🧶'];
const int colunas = 7;
const int linhas = 8;

class Combina extends StatefulWidget {
  const Combina({super.key});

  @override
  State<Combina> createState() => _CombinaState();
}

class _CombinaState extends State<Combina> {
  final sorteio = Random();
  final int tamanhoMinimo = 3;
  final int jogadasPorPartida = 20;
  List<String> grade = [];
  Set<int> brilhando = {};
  int? escolhida;
  int pontos = 0;
  int combo = 0;
  int jogadas = 0;
  bool ocupado = false;
  String aviso = 'Toque em duas peças vizinhas para trocar.';

  @override
  void initState() {
    super.initState();
    novaPartida();
  }

  String sortear() => pecas[sorteio.nextInt(pecas.length)];

  void novaPartida() {
    grade = List.generate(colunas * linhas, (_) => sortear());
    // a grade começa sem combinações prontas
    var prontas = combinacoes();
    while (prontas.isNotEmpty) {
      for (final i in prontas) {
        grade[i] = sortear();
      }
      prontas = combinacoes();
    }
    pontos = 0;
    jogadas = jogadasPorPartida;
    escolhida = null;
  }

  // todas as casas que fazem parte de uma fileira de 3 ou mais peças iguais
  Set<int> combinacoes() {
    final Set<int> achadas = {};
    // nas linhas
    for (var l = 0; l < linhas; l++) {
      var inicio = 0;
      for (var c = 1; c <= colunas; c++) {
        if (c == colunas || grade[l * colunas + c] != grade[l * colunas + inicio]) {
          if (c - inicio >= tamanhoMinimo && grade[l * colunas + inicio] != '') {
            for (var k = inicio; k < c; k++) {
              achadas.add(l * colunas + k);
            }
          }
          inicio = c;
        }
      }
    }
    // nas colunas
    for (var c = 0; c < colunas; c++) {
      var inicio = 0;
      for (var l = 1; l <= linhas; l++) {
        if (l == linhas || grade[l * colunas + c] != grade[inicio * colunas + c]) {
          if (l - inicio >= tamanhoMinimo && grade[inicio * colunas + c] != '') {
            for (var k = inicio; k < l; k++) {
              achadas.add(k * colunas + c);
            }
          }
          inicio = l;
        }
      }
    }
    return achadas;
  }

  // as peças caem para ocupar os buracos, e peças novas entram por cima
  void cair() {
    for (var c = 0; c < colunas; c++) {
      final List<String> restantes = [];
      for (var l = linhas - 1; l >= 0; l--) {
        if (grade[l * colunas + c] != '') restantes.add(grade[l * colunas + c]);
      }
      for (var l = linhas - 1; l >= 0; l--) {
        final k = linhas - 1 - l;
        grade[l * colunas + c] = k < restantes.length ? restantes[k] : sortear();
      }
    }
  }

  bool vizinhas(int a, int b) {
    final d = (a - b).abs();
    return d == colunas || (d == 1 && a ~/ colunas == b ~/ colunas);
  }

  void tocar(int i) {
    if (ocupado || jogadas == 0) return;
    final e = escolhida;
    if (e == null || !vizinhas(e, i)) {
      setState(() => escolhida = i);
      return;
    }
    escolhida = null;
    trocar(e, i);
    if (combinacoes().isEmpty) {
      trocar(e, i); // não combinou: desfaz a troca
      setState(() => aviso = 'Essa troca não forma 3 iguais.');
      return;
    }
    jogadas--;
    combo = 0;
    resolver();
  }

  void trocar(int a, int b) {
    final t = grade[a];
    grade[a] = grade[b];
    grade[b] = t;
  }

  // cascata: some, cai e confere de novo. Cada rodada a mais é um combo.
  Future<void> resolver() async {
    final achadas = combinacoes();
    if (achadas.isEmpty) {
      setState(() {
        ocupado = false;
        if (jogadas == 0) aviso = 'Fim de jogo! $pontos pontos.';
      });
      return;
    }
    ocupado = true;
    combo++;
    setState(() => brilhando = achadas);
    await Future.delayed(const Duration(milliseconds: 300));
    setState(() {
      pontos += achadas.length * 10 * combo;
      for (final i in achadas) {
        grade[i] = '';
      }
      brilhando = {};
      aviso = combo > 1 ? 'Combo x$combo!' : '+${achadas.length * 10} pontos';
    });
    await Future.delayed(const Duration(milliseconds: 200));
    setState(() => cair());
    await Future.delayed(const Duration(milliseconds: 250));
    resolver(); // confere a grade nova: as peças que caíram podem formar outra fileira
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Pontos: $pontos   Jogadas: $jogadas')),
      body: Padding(
        padding: const EdgeInsets.all(8),
        child: Column(
          children: [
            SizedBox(
              width: 346,
              height: 396,
              child: Wrap(
                spacing: 4,
                runSpacing: 4,
                children: [
                  for (var i = 0; i < colunas * linhas; i++)
                    GestureDetector(
                      onTap: () => tocar(i),
                      child: Container(
                        width: 46,
                        height: 46,
                        alignment: Alignment.center,
                        decoration: BoxDecoration(
                          color: brilhando.contains(i) ? Colors.white : (escolhida == i ? Colors.amber : const Color(0xFFF6E7CF)),
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: Text(grade[i], style: const TextStyle(fontSize: 28)),
                      ),
                    ),
                ],
              ),
            ),
            const SizedBox(height: 10),
            Text(aviso, style: const TextStyle(fontSize: 18)),
            if (jogadas == 0) FilledButton(onPressed: () => setState(() => novaPartida()), child: const Text('Jogar de novo')),
          ],
        ),
      ),
    );
  }
}
