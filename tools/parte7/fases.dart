import 'dart:math';
import 'package:flame/components.dart';
import 'package:flame/events.dart';
import 'package:flame/game.dart';
import 'package:flutter/material.dart';
import 'package:hive_flutter/hive_flutter.dart';

Future<void> main() async {
  await Hive.initFlutter();
  await Hive.openBox('progresso');
  runApp(const MaterialApp(debugShowCheckedModeBanner: false, home: Mapa()));
}

// Cada fase: quantos ossos pegar e em quanto tempo
class Fase {
  final String nome;
  final int ossos;
  final double tempo;
  const Fase(this.nome, this.ossos, this.tempo);
}

const fases = [
  Fase('Quintal', 5, 10),
  Fase('Praça', 7, 10),
  Fase('Feira', 9, 10),
  Fase('Praia', 11, 10),
];

// estrelas guardadas no aparelho: 'fase0' -> 0 a 3
int estrelasDe(int i) => Hive.box('progresso').get('fase$i', defaultValue: 0);

// a fase abre quando a anterior tem pelo menos 1 estrela
bool liberada(int i) => i == 0 || estrelasDe(i - 1) > 0;

class Mapa extends StatefulWidget {
  const Mapa({super.key});

  @override
  State<Mapa> createState() => _MapaState();
}

class _MapaState extends State<Mapa> {
  int get total {
    var soma = 0;
    for (int i = 0; i < fases.length; i++) {
      soma += estrelasDe(i);
    }
    return soma;
  }

  void jogar(int i) {
    Navigator.push(context, MaterialPageRoute(builder: (context) => TelaFase(indice: i))).then((_) => setState(() {}));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Fases'),
        actions: [
          Center(child: Text('⭐ $total / ${fases.length * 3}   ')),
          IconButton(
            icon: const Icon(Icons.delete_outline),
            tooltip: 'Apagar progresso',
            onPressed: () => setState(() {
              Hive.box('progresso').clear();
            }),
          ),
        ],
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          for (int i = 0; i < fases.length; i++)
            Card(
              child: ListTile(
                enabled: liberada(i),
                leading: CircleAvatar(child: liberada(i) ? Text('${i + 1}') : const Icon(Icons.lock)),
                title: Text(fases[i].nome),
                subtitle: Text(liberada(i) ? '${fases[i].ossos} ossos em ${fases[i].tempo.toStringAsFixed(0)} s' : 'Ganhe 1 estrela na fase anterior'),
                trailing: Text('★' * estrelasDe(i) + '☆' * (3 - estrelasDe(i)), style: const TextStyle(fontSize: 22, color: Colors.amber)),
                onTap: liberada(i) ? () => jogar(i) : null,
              ),
            ),
        ],
      ),
    );
  }
}

class TelaFase extends StatelessWidget {
  final int indice;
  const TelaFase({super.key, required this.indice});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: GameWidget(
        game: Corrida(indice),
        overlayBuilderMap: {
          'fim': (context, Corrida jogo) => Center(
                child: Card(
                  child: Padding(
                    padding: const EdgeInsets.all(24),
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Text(jogo.estrelas > 0 ? 'Fase completa!' : 'Não deu desta vez', style: const TextStyle(fontSize: 24)),
                        Text('★' * jogo.estrelas + '☆' * (3 - jogo.estrelas), style: const TextStyle(fontSize: 40, color: Colors.amber)),
                        if (jogo.recorde) const Text('Novo recorde da fase!'),
                        const SizedBox(height: 12),
                        FilledButton(onPressed: () => Navigator.pop(context), child: const Text('Voltar ao mapa')),
                      ],
                    ),
                  ),
                ),
              ),
        },
      ),
    );
  }
}

class Corrida extends FlameGame {
  final int indice;
  Corrida(this.indice);

  late Fase fase;
  late double tempo;
  late int faltam;
  late TextComponent placar;
  int estrelas = 0;
  bool recorde = false;
  bool acabou = false;
  final sorteio = Random();

  @override
  Color backgroundColor() => const Color(0xFF9ED67A);

  @override
  Future<void> onLoad() async {
    fase = fases[indice];
    tempo = fase.tempo;
    faltam = fase.ossos;
    placar = TextComponent(text: '', position: Vector2(16, 16));
    add(placar);
    novoOsso();
  }

  void novoOsso() {
    add(Osso(Vector2(40 + sorteio.nextDouble() * (size.x - 80), 90 + sorteio.nextDouble() * (size.y - 160))));
  }

  void pegou() {
    faltam--;
    if (faltam == 0) {
      terminar();
    } else {
      novoOsso();
    }
  }

  // estrelas pelo tempo que sobrou: mais da metade = 3, mais de um quarto = 2, terminou = 1
  int contarEstrelas() {
    if (faltam > 0) return 0;
    final sobra = tempo / fase.tempo;
    if (sobra > 0.5) return 3;
    if (sobra > 0.25) return 2;
    return 1;
  }

  void terminar() {
    acabou = true;
    estrelas = contarEstrelas();
    final caixa = Hive.box('progresso');
    final antes = caixa.get('fase$indice', defaultValue: 0);
    if (estrelas > antes) {
      caixa.put('fase$indice', estrelas);
      recorde = antes > 0;
    }
    pauseEngine();
    overlays.add('fim');
  }

  @override
  void update(double dt) {
    super.update(dt);
    if (acabou) return;
    tempo -= dt;
    placar.text = '${fase.nome}   Ossos: $faltam   Tempo: ${max(0, tempo).toStringAsFixed(1)}';
    if (tempo <= 0) {
      tempo = 0;
      terminar();
    }
  }
}

class Osso extends SpriteAnimationComponent with TapCallbacks, HasGameReference<Corrida> {
  Osso(Vector2 onde) : super(position: onde, size: Vector2.all(52), anchor: Anchor.center);

  @override
  Future<void> onLoad() async {
    animation = await game.loadSpriteAnimation('osso.png', SpriteAnimationData.sequenced(amount: 6, stepTime: 0.1, textureSize: Vector2.all(16)));
  }

  @override
  void onTapDown(TapDownEvent event) {
    removeFromParent();
    game.pegou();
  }
}
