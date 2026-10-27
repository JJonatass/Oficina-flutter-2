import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(debugShowCheckedModeBanner: false, home: Sala()));

// Esta aula é a sala de jogos da turma: os jogos que chegam por link abrem aqui.
// Para jogar, use o botão 🕹 Galeria. Para mandar o seu, abra a aula do seu jogo e use 🔗 Compartilhar.
class Sala extends StatelessWidget {
  const Sala({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF1E2A3A),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: const [
              Text('🕹', style: TextStyle(fontSize: 64)),
              SizedBox(height: 12),
              Text('Sala de jogos da turma', style: TextStyle(fontSize: 26, color: Colors.amber, fontWeight: FontWeight.bold)),
              SizedBox(height: 12),
              Text('Abra a 🕹 Galeria e escolha um jogo para jogar aqui.', textAlign: TextAlign.center, style: TextStyle(fontSize: 18, color: Colors.white70)),
            ],
          ),
        ),
      ),
    );
  }
}
