import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(debugShowCheckedModeBanner: false, home: Portfolio()));

class Projeto {
  final String nome;
  final String papel; // o que VOCÊ fez no projeto
  final String resumo;
  final String link;
  final String evento; // aula, game jam, projeto pessoal...
  const Projeto(this.nome, this.papel, this.resumo, this.link, this.evento);
}

const nome = 'Seu Nome';
const titulo = 'Desenvolvedora de jogos (Flutter e Flame)';
const corDestaque = Color(0xFFD68C3E);

const projetos = [
  Projeto('Trilha do Caramelo', 'Programação e fases', 'Plataforma com 3 fases, estrelas salvas e gatos que patrulham.', 'meusite.itch.io/trilha', 'Projeto da disciplina'),
  Projeto('Caramelo Voador', 'Tudo (sozinho)', 'Desvie dos canos tocando na tela. Feito em 48 horas.', 'meusite.itch.io/voador', 'Game jam da turma'),
  Projeto('Torres do Caramelo', 'Programação da IA dos gatos', 'Defenda o quintal com caramelos de guarda.', 'meusite.itch.io/torres', 'Projeto em dupla'),
];

class Portfolio extends StatelessWidget {
  const Portfolio({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          const SizedBox(height: 24),
          const Center(child: CircleAvatar(radius: 40, backgroundColor: corDestaque, child: Text('🐶', style: TextStyle(fontSize: 40)))),
          const SizedBox(height: 12),
          const Text(nome, textAlign: TextAlign.center, style: TextStyle(fontSize: 26, fontWeight: FontWeight.bold)),
          const Text(titulo, textAlign: TextAlign.center),
          const SizedBox(height: 16),
          for (final p in projetos)
            Card(
              child: Padding(
                padding: const EdgeInsets.all(12),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(p.nome, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: corDestaque)),
                    Text('${p.evento} · ${p.papel}', style: const TextStyle(fontStyle: FontStyle.italic)),
                    const SizedBox(height: 4),
                    Text(p.resumo),
                    Text('▶ ${p.link}', style: const TextStyle(color: Colors.blue)),
                  ],
                ),
              ),
            ),
        ],
      ),
    );
  }
}
