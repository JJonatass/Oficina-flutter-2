import 'package:flutter/material.dart';
import 'package:hive_flutter/hive_flutter.dart';

Future<void> main() async {
  await Hive.initFlutter();
  await Hive.openBox('meu_jogo');
  runApp(const MaterialApp(debugShowCheckedModeBanner: false, home: Documento()));
}

// As perguntas do documento de design do jogo (GDD)
const perguntas = [
  ['nome', 'Nome do jogo', 'Caramelo e o Mistério da Praça'],
  ['genero', 'Gênero', 'Plataforma, quebra-cabeça, corrida...'],
  ['objetivo', 'Objetivo do jogador', 'Achar os 3 ossos dourados da praça'],
  ['ciclo', 'Ciclo principal (o que o jogador faz o tempo todo)', 'Correr, pular e pegar ossos fugindo dos gatos'],
  ['controles', 'Controles', 'Botões ◀ ▶ e ⤒ na tela'],
  ['desafio', 'Desafio e como ele cresce', 'Mais gatos e menos chão a cada fase'],
  ['arte', 'Arte e som', 'Pixel art 16×16, música alegre em loop'],
];

// As etapas do projeto, com a semana em que cada uma deve ficar pronta
const etapas = [
  ['Documento do jogo preenchido', 1],
  ['Protótipo com formas simples (o ciclo funciona)', 2],
  ['Uma fase jogável do começo ao fim', 3],
  ['Arte e som no lugar das formas', 4],
  ['Teste com 3 colegas e ajustes', 5],
  ['Menu, fim de jogo e entrega (link na 🕹 Galeria)', 6],
];

// A ficha de avaliação: critério e peso (os pesos somam 10)
const ficha = [
  ['O ciclo principal é divertido e claro', 3],
  ['O jogo funciona do começo ao fim, sem travar', 2],
  ['A dificuldade cresce e ensina', 2],
  ['Arte, som e retorno visual', 2],
  ['Código organizado e comentado', 1],
];

class Documento extends StatefulWidget {
  const Documento({super.key});

  @override
  State<Documento> createState() => _DocumentoState();
}

class _DocumentoState extends State<Documento> {
  final caixa = Hive.box('meu_jogo');
  final Map<String, TextEditingController> campos = {};

  @override
  void initState() {
    super.initState();
    for (final p in perguntas) {
      campos[p[0]] = TextEditingController(text: caixa.get(p[0], defaultValue: ''));
    }
  }

  int get prontas => etapas.where((e) => caixa.get('etapa_${e[0]}', defaultValue: false) == true).length;

  double get nota {
    var total = 0.0;
    for (final f in ficha) {
      total += (caixa.get('nota_${f[0]}', defaultValue: 0) as int) / 4 * (f[1] as int);
    }
    return total;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Meu jogo · etapas $prontas/${etapas.length} · nota ${nota.toStringAsFixed(1)}')),
      body: ListView(
        padding: const EdgeInsets.all(12),
        children: [
          const Text('1. Documento do jogo', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          for (final p in perguntas)
            TextField(
              controller: campos[p[0]],
              decoration: InputDecoration(labelText: p[1], hintText: p[2]),
              onChanged: (v) => caixa.put(p[0], v),
            ),
          const SizedBox(height: 16),
          const Text('2. Etapas', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          for (final e in etapas)
            CheckboxListTile(
              value: caixa.get('etapa_${e[0]}', defaultValue: false),
              title: Text('${e[0]}'),
              subtitle: Text('até a semana ${e[1]}'),
              onChanged: (v) => setState(() {
                caixa.put('etapa_${e[0]}', v);
              }),
            ),
          const SizedBox(height: 16),
          const Text('3. Ficha de avaliação (0 a 4 em cada critério)', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          for (final f in ficha)
            ListTile(
              title: Text('${f[0]} (peso ${f[1]})'),
              subtitle: Slider(
                value: (caixa.get('nota_${f[0]}', defaultValue: 0) as int).toDouble(),
                min: 0,
                max: 4,
                divisions: 4,
                onChanged: (v) => setState(() {
                  caixa.put('nota_${f[0]}', v.round());
                }),
              ),
            ),
        ],
      ),
    );
  }
}
