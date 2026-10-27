import 'dart:math';
import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(debugShowCheckedModeBanner: false, home: Velha()));

const caramelo = '🐶'; // você
const gato = '🐱'; // o computador

const linhasVitoria = [
  [0, 1, 2], [3, 4, 5], [6, 7, 8], // linhas
  [0, 3, 6], [1, 4, 7], [2, 5, 8], // colunas
  [0, 4, 8], [2, 4, 6], // diagonais
];

// quem venceu: caramelo, gato, 'empate' ou '' (o jogo continua)
String vencedor(List<String> t) {
  for (final l in linhasVitoria) {
    if (t[l[0]] != '' && t[l[0]] == t[l[1]] && t[l[1]] == t[l[2]]) return t[l[0]];
  }
  if (!t.contains('')) return 'empate';
  return '';
}

int analisadas = 0;

// Minimax com poda alfa-beta. O gato quer o MAIOR valor, o caramelo quer o MENOR.
// Vencer cedo vale mais que vencer tarde (por isso o "- profundidade").
int minimax(List<String> t, bool vezDoGato, int profundidade, int limite, int alfa, int beta) {
  analisadas++;
  final v = vencedor(t);
  if (v == gato) return 10 - profundidade;
  if (v == caramelo) return profundidade - 10;
  if (v == 'empate' || profundidade >= limite) return 0; // chegou no fim ou não enxerga mais longe
  var melhor = vezDoGato ? -100 : 100;
  for (var i = 0; i < 9; i++) {
    if (t[i] != '') continue;
    t[i] = vezDoGato ? gato : caramelo; // experimenta a jogada...
    final valor = minimax(t, !vezDoGato, profundidade + 1, limite, alfa, beta);
    t[i] = ''; // ...e desfaz
    if (vezDoGato) {
      melhor = max(melhor, valor);
      alfa = max(alfa, valor);
    } else {
      melhor = min(melhor, valor);
      beta = min(beta, valor);
    }
    if (beta <= alfa) break; // poda: o outro jogador nunca deixaria chegar aqui
  }
  return melhor;
}

class Velha extends StatefulWidget {
  const Velha({super.key});

  @override
  State<Velha> createState() => _VelhaState();
}

class _VelhaState extends State<Velha> {
  final sorteio = Random();
  List<String> tabuleiro = List.filled(9, '');
  int olharFrente = 9; // quantas jogadas o gato imagina à frente
  final double chanceDeErro = 0.0; // de 0 (nunca erra) a 1 (sempre joga ao acaso)
  String aviso = 'Você é o 🐶. Toque numa casa.';
  int vitorias = 0;
  int derrotas = 0;
  int empates = 0;

  void jogar(int i) {
    if (tabuleiro[i] != '' || vencedor(tabuleiro) != '') return;
    setState(() {
      tabuleiro[i] = caramelo;
      if (vencedor(tabuleiro) == '') vezDoGato();
      conferirFim();
    });
  }

  void vezDoGato() {
    final List<int> livres = [];
    for (var i = 0; i < 9; i++) {
      if (tabuleiro[i] == '') livres.add(i);
    }
    if (sorteio.nextDouble() < chanceDeErro) {
      tabuleiro[livres[sorteio.nextInt(livres.length)]] = gato;
      aviso = 'O gato se distraiu e jogou ao acaso.';
      return;
    }
    analisadas = 0;
    var melhorValor = -100;
    List<int> melhores = [];
    for (final i in livres) {
      tabuleiro[i] = gato;
      final valor = minimax(tabuleiro, false, 1, olharFrente, -100, 100);
      tabuleiro[i] = '';
      if (valor > melhorValor) {
        melhorValor = valor;
        melhores = [i];
      } else if (valor == melhorValor) {
        melhores.add(i);
      }
    }
    // empate entre as melhores casas: sorteia uma delas
    tabuleiro[melhores[sorteio.nextInt(melhores.length)]] = gato;
    aviso = 'O gato pensou em $analisadas posições (nota da jogada: $melhorValor).';
  }

  void conferirFim() {
    final v = vencedor(tabuleiro);
    if (v == caramelo) {
      vitorias++;
      aviso = 'Você venceu! 🎉';
    } else if (v == gato) {
      derrotas++;
      aviso = 'O gato venceu.';
    } else if (v == 'empate') {
      empates++;
      aviso = 'Empate: ninguém erra, ninguém ganha.';
    }
  }

  void novaPartida(bool gatoComeca) {
    setState(() {
      tabuleiro = List.filled(9, '');
      aviso = 'Sua vez.';
      if (gatoComeca) {
        tabuleiro[sorteio.nextInt(9)] = gato; // primeira jogada sorteada: o tabuleiro vazio tem posições demais
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('🐶 $vitorias  ×  $derrotas 🐱   ·   $empates empates')),
      body: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          children: [
            SizedBox(
              width: 318,
              height: 318,
              child: Wrap(
                spacing: 6,
                runSpacing: 6,
                children: [
                  for (var i = 0; i < 9; i++)
                    GestureDetector(
                      onTap: () => jogar(i),
                      child: Container(
                        width: 100,
                        height: 100,
                        alignment: Alignment.center,
                        decoration: BoxDecoration(color: const Color(0xFFF6E7CF), borderRadius: BorderRadius.circular(12)),
                        child: Text(tabuleiro[i], style: const TextStyle(fontSize: 54)),
                      ),
                    ),
                ],
              ),
            ),
            const SizedBox(height: 12),
            Text(aviso, textAlign: TextAlign.center, style: const TextStyle(fontSize: 16)),
            const SizedBox(height: 8),
            Text('O gato imagina $olharFrente jogadas à frente'),
            Slider(value: olharFrente.toDouble(), min: 1, max: 9, divisions: 8, onChanged: (v) => setState(() => olharFrente = v.round())),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                FilledButton(onPressed: () => novaPartida(false), child: const Text('Eu começo')),
                const SizedBox(width: 12),
                OutlinedButton(onPressed: () => novaPartida(true), child: const Text('O gato começa')),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
