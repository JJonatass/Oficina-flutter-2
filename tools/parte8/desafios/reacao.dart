import 'dart:async';
import 'dart:math';
import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(debugShowCheckedModeBanner: false, home: Reacao()));

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
      espera?.cancel();
      setState(() => estado = 'cedo');
    } else if (estado == 'agora') {
      final ms = DateTime.now().difference(inicio!).inMilliseconds;
      setState(() {
        ultimo = ms;
        if (recorde == null || ms < recorde!) recorde = ms;
        estado = 'resultado';
      });
    } else {
      setState(() => estado = 'esperando');
      espera = Timer(Duration(milliseconds: 1000 + sorteio.nextInt(2000)), () {
        setState(() {
          estado = 'agora';
          inicio = DateTime.now();
        });
      });
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
