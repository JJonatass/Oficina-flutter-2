import 'dart:async';
import 'package:flutter/material.dart';
import 'package:hive_flutter/hive_flutter.dart';

Future<void> main() async {
  await Hive.initFlutter();
  await Hive.openBox('conquistas');
  runApp(const MaterialApp(debugShowCheckedModeBanner: false, home: Painel()));
}

// Cada conquista olha os números do jogo e diz se já foi alcançada
class Conquista {
  final String id;
  final String titulo;
  final String descricao;
  final String icone;
  final bool Function(Map<String, int> n) alcancou;
  const Conquista(this.id, this.titulo, this.descricao, this.icone, this.alcancou);
}

final conquistas = [
  Conquista('primeiro', 'Primeiro osso', 'Pegue 1 osso', '🦴', (n) => (n['ossos'] ?? 0) >= 1),
  Conquista('colecionador', 'Colecionador', 'Pegue 20 ossos', '🏆', (n) => (n['ossos'] ?? 0) >= 20),
  Conquista('saltador', 'Perna de mola', 'Pule 10 vezes', '🦘', (n) => (n['pulos'] ?? 0) >= 10),
  Conquista('teimoso', 'Teimoso', 'Caia 5 vezes e continue jogando', '🤕', (n) => (n['quedas'] ?? 0) >= 5),
  Conquista('perfeito', 'Sem um arranhão', 'Pegue 10 ossos sem cair nenhuma vez', '✨', (n) => (n['ossos'] ?? 0) >= 10 && (n['quedas'] ?? 0) == 0),
];

class Painel extends StatefulWidget {
  const Painel({super.key});

  @override
  State<Painel> createState() => _PainelState();
}

class _PainelState extends State<Painel> {
  final caixa = Hive.box('conquistas');
  final Map<String, int> numeros = {};
  String? aviso;
  Timer? some;
  // quanto tempo o aviso de conquista fica na tela
  final int segundosAviso = 3;

  bool ganhou(Conquista c) => caixa.get(c.id, defaultValue: false);

  // todo evento do jogo passa por aqui: conta e confere as conquistas
  void evento(String nome) {
    setState(() {
      numeros[nome] = (numeros[nome] ?? 0) + 1;
      for (final c in conquistas) {
        if (!ganhou(c) && c.alcancou(numeros)) {
          caixa.put(c.id, true);
          aviso = '${c.icone} Conquista: ${c.titulo}!';
          some?.cancel();
          some = Timer(Duration(seconds: segundosAviso), () => setState(() => aviso = null));
        }
      }
    });
  }

  @override
  void dispose() {
    some?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final total = conquistas.where((c) => ganhou(c)).length;
    return Scaffold(
      appBar: AppBar(title: Text('Conquistas $total/${conquistas.length}'), actions: [
        IconButton(
          icon: const Icon(Icons.refresh),
          tooltip: 'Zerar',
          onPressed: () => setState(() {
            caixa.clear();
            numeros.clear();
          }),
        ),
      ]),
      body: Column(
        children: [
          if (aviso != null)
            Container(
              width: double.infinity,
              margin: const EdgeInsets.all(12),
              padding: const EdgeInsets.all(14),
              decoration: BoxDecoration(color: Colors.amber, borderRadius: BorderRadius.circular(12)),
              child: Text(aviso!, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            ),
          Padding(
            padding: const EdgeInsets.all(12),
            child: Text('Ossos: ${numeros['ossos'] ?? 0}   Pulos: ${numeros['pulos'] ?? 0}   Quedas: ${numeros['quedas'] ?? 0}'),
          ),
          Wrap(
            spacing: 8,
            children: [
              FilledButton(onPressed: () => evento('ossos'), child: const Text('🦴 Pegar osso')),
              OutlinedButton(onPressed: () => evento('pulos'), child: const Text('Pular')),
              OutlinedButton(onPressed: () => evento('quedas'), child: const Text('Cair')),
            ],
          ),
          Expanded(
            child: ListView(
              children: [
                for (final c in conquistas)
                  ListTile(
                    leading: Text(ganhou(c) ? c.icone : '🔒', style: const TextStyle(fontSize: 28)),
                    title: Text(c.titulo),
                    subtitle: Text(c.descricao),
                    trailing: ganhou(c) ? const Icon(Icons.check_circle, color: Colors.green) : null,
                  ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
