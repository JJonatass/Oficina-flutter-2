import 'dart:async';
import 'dart:math';
import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(debugShowCheckedModeBanner: false, home: Reacao()));

// DESAFIO · RELÓGIO DE REAÇÃO
// 1. A tela começa cinza, com "Toque para começar".
// 2. Ao tocar, espera um tempo sorteado (de 1 a 3 segundos) e fica verde com "TOQUE AGORA!".
// 3. Ao tocar no verde, mostre quantos milissegundos a pessoa levou.
// 4. Guarde o melhor tempo (recorde) e mostre embaixo.
// 5. Se tocar antes de ficar verde, avise "Cedo demais!" e deixe tentar de novo.
// A tela, as cores e os textos já estão prontos. Complete as partes marcadas com FAÇA.

class Reacao extends StatefulWidget {
  const Reacao({super.key});

  @override
  State<Reacao> createState() => _ReacaoState();
}

class _ReacaoState extends State<Reacao> {
  final sorteio = Random();
  String estado = 'pronto'; // pronto, esperando, agora, resultado ou cedo
  DateTime? inicio;
  Timer? espera;
  int? ultimo;
  int? recorde;

  void tocar() {
    if (estado == 'esperando') {
      // FAÇA 4: tocou antes do verde. Cancele a espera (espera?.cancel())
      // e mude o estado para 'cedo' dentro de um setState.
    } else if (estado == 'agora') {
      // FAÇA 2: calcule quantos milissegundos passaram desde inicio
      // (DateTime.now(), o método difference e o campo inMilliseconds),
      // guarde em ultimo e mude o estado para 'resultado'.
      // FAÇA 3: se esse tempo for menor que o recorde (ou se ainda não houver recorde), troque o recorde.
    } else {
      setState(() => estado = 'esperando');
      // FAÇA 1: guarde em espera um Timer que dispara depois de 1 a 3 segundos
      // (use o sorteio para escolher os milissegundos). Quando ele disparar,
      // dentro de um setState: estado = 'agora' e inicio = DateTime.now().
    }
  }

  @override
  void dispose() {
    espera?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final cor = estado == 'agora' ? Colors.green : (estado == 'cedo' ? Colors.red : Colors.blueGrey);
    final texto = estado == 'esperando'
        ? 'Espere o verde...'
        : estado == 'agora'
            ? 'TOQUE AGORA!'
            : estado == 'cedo'
                ? 'Cedo demais! Toque para tentar de novo.'
                : estado == 'resultado'
                    ? '$ultimo ms! Toque para jogar de novo.'
                    : 'Toque para começar';
    return Scaffold(
      backgroundColor: cor,
      body: GestureDetector(
        onTap: tocar,
        child: Container(
          color: cor,
          width: double.infinity,
          height: double.infinity,
          alignment: Alignment.center,
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(texto, textAlign: TextAlign.center, style: const TextStyle(fontSize: 28, color: Colors.white)),
              const SizedBox(height: 24),
              Text(recorde == null ? 'Sem recorde ainda' : 'Recorde: $recorde ms', style: const TextStyle(fontSize: 18, color: Colors.white70)),
            ],
          ),
        ),
      ),
    );
  }
}
