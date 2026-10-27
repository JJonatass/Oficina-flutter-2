import 'dart:async';
import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(debugShowCheckedModeBanner: false, home: Conversa()));

class Escolha {
  final String texto;
  final String proxima;
  final int amizade;
  final int ossos;
  const Escolha(this.texto, this.proxima, {this.amizade = 0, this.ossos = 0});
}

class Fala {
  final String quem;
  final String texto;
  final List<Escolha> escolhas;
  const Fala(this.quem, this.texto, this.escolhas);
}

// O roteiro: cada fala tem um nome e aponta para as próximas.
const roteiro = {
  'inicio': Fala('Mingau', 'Ei, caramelo! Você está no MEU muro.', [
    Escolha('Desculpa, só estou de passagem.', 'gentil', amizade: 1),
    Escolha('O muro é de todo mundo!', 'bravo', amizade: -1),
  ]),
  'gentil': Fala('Mingau', 'Hum... educado. Quer saber onde tem um osso escondido?', [
    Escolha('Quero!', 'segredo', amizade: 1),
    Escolha('Prefiro achar sozinho.', 'fim', amizade: 0),
  ]),
  'bravo': Fala('Mingau', 'Então suba se tiver coragem. Fffff!', [
    Escolha('Late bem alto', 'fuga', amizade: -1),
    Escolha('Pede desculpas', 'gentil', amizade: 2),
  ]),
  'segredo': Fala('Mingau', 'Atrás da lixeira da praça. Mas divide comigo, hein?', [
    Escolha('Combinado, amigo!', 'fim', amizade: 1, ossos: 1),
  ]),
  'fuga': Fala('Narrador', 'O gato pula do muro e some. Ninguém ganhou nada hoje.', [
    Escolha('Recomeçar', 'inicio'),
  ]),
  'fim': Fala('Narrador', 'O dia segue no bairro.', [
    Escolha('Recomeçar', 'inicio'),
  ]),
};

class Conversa extends StatefulWidget {
  const Conversa({super.key});

  @override
  State<Conversa> createState() => _ConversaState();
}

class _ConversaState extends State<Conversa> {
  String atual = 'inicio';
  int letras = 0;
  int amizade = 0;
  int ossos = 0;
  Timer? digitando;
  // milissegundos para cada letra aparecer
  final int msPorLetra = 35;

  Fala get fala => roteiro[atual]!;
  bool get terminou => letras >= fala.texto.length;

  @override
  void initState() {
    super.initState();
    comecar('inicio');
  }

  // efeito de máquina de escrever: uma letra de cada vez
  void comecar(String nome) {
    digitando?.cancel();
    setState(() {
      atual = nome;
      letras = 0;
    });
    digitando = Timer.periodic(Duration(milliseconds: msPorLetra), (t) {
      setState(() => letras++);
      if (terminou) t.cancel();
    });
  }

  // tocar no balão mostra o texto inteiro de uma vez
  void pular() {
    digitando?.cancel();
    setState(() => letras = fala.texto.length);
  }

  void escolher(Escolha e) {
    setState(() {
      if (e.proxima == 'inicio') {
        amizade = 0;
        ossos = 0;
      } else {
        amizade += e.amizade;
        ossos += e.ossos;
      }
    });
    comecar(e.proxima);
  }

  @override
  void dispose() {
    digitando?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final f = roteiro[atual]!;
    return Scaffold(
      backgroundColor: const Color(0xFF8FD3F4),
      appBar: AppBar(title: Text('Amizade: $amizade   Ossos: $ossos')),
      body: Column(
        children: [
          const Expanded(
            child: Center(
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [Text('🐶', style: TextStyle(fontSize: 72)), Text('🐱', style: TextStyle(fontSize: 72))],
              ),
            ),
          ),
          GestureDetector(
            onTap: pular,
            child: Container(
              width: double.infinity,
              margin: const EdgeInsets.all(12),
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(16), border: Border.all(color: Colors.black87, width: 3)),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(f.quem, style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.deepOrange)),
                  const SizedBox(height: 6),
                  Text(f.texto.substring(0, letras.clamp(0, f.texto.length)), style: const TextStyle(fontSize: 18)),
                ],
              ),
            ),
          ),
          if (terminou)
            Padding(
              padding: const EdgeInsets.fromLTRB(12, 0, 12, 16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  for (final e in f.escolhas)
                    Padding(
                      padding: const EdgeInsets.only(top: 6),
                      child: FilledButton(onPressed: () => escolher(e), child: Text(e.texto)),
                    ),
                ],
              ),
            ),
        ],
      ),
    );
  }
}
