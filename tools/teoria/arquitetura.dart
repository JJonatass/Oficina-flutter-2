import 'package:flutter/material.dart';

// =============================================================
// Camada 1 · MODELO: os dados e as regras do jogo, sem desenho.
// Não importa nada visual; dá para testar com dart test.
// =============================================================
class EstadoJogo extends ChangeNotifier {
  final int vidasIniciais = 3;
  int vidas = 3;
  int ossos = 0;
  int nivel = 1;
  final List<String> eventos = [];

  bool get acabou => vidas <= 0;

  void pegarOsso() {
    if (acabou) return;
    ossos++;
    // regra: a cada 5 ossos, sobe de nível
    if (ossos % 5 == 0) {
      nivel++;
      registrar('subiu para o nível $nivel');
    } else {
      registrar('pegou osso ($ossos)');
    }
  }

  void levarDano() {
    if (acabou) return;
    vidas--;
    registrar(acabou ? 'fim de jogo' : 'levou dano, restam $vidas');
  }

  void reiniciar() {
    vidas = vidasIniciais;
    ossos = 0;
    nivel = 1;
    eventos.clear();
    registrar('jogo novo');
  }

  void registrar(String e) {
    eventos.insert(0, e);
    notifyListeners(); // avisa quem estiver ouvindo que algo mudou
  }
}

// =============================================================
// Camada 2 · VISUAL: widgets que só MOSTRAM o estado e
// MANDAM COMANDOS para ele. Nenhuma regra mora aqui.
// =============================================================
void main() => runApp(const MaterialApp(debugShowCheckedModeBanner: false, home: TelaJogo()));

class TelaJogo extends StatefulWidget {
  const TelaJogo({super.key});

  @override
  State<TelaJogo> createState() => _TelaJogoState();
}

class _TelaJogoState extends State<TelaJogo> {
  final estado = EstadoJogo();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Camadas do jogo')),
      body: ListenableBuilder(
        listenable: estado,
        builder: (context, _) => Column(
          children: [
            Placar(estado: estado),
            Controles(estado: estado),
            const Divider(),
            const Text('Registro de eventos'),
            Expanded(
              child: ListView(
                children: [for (final e in estado.eventos) ListTile(dense: true, title: Text(e))],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class Placar extends StatelessWidget {
  final EstadoJogo estado;
  const Placar({super.key, required this.estado});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(16),
      color: estado.acabou ? Colors.red.shade100 : Colors.amber.shade100,
      child: Text(
        '${'♥' * estado.vidas}${'♡' * (estado.vidasIniciais - estado.vidas)}   Ossos: ${estado.ossos}   Nível: ${estado.nivel}',
        style: const TextStyle(fontSize: 20),
      ),
    );
  }
}

class Controles extends StatelessWidget {
  final EstadoJogo estado;
  const Controles({super.key, required this.estado});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(8),
      child: Wrap(
        spacing: 8,
        children: [
          FilledButton(onPressed: estado.pegarOsso, child: const Text('Pegar osso')),
          OutlinedButton(onPressed: estado.levarDano, child: const Text('Levar dano')),
          TextButton(onPressed: estado.reiniciar, child: const Text('Reiniciar')),
        ],
      ),
    );
  }
}
