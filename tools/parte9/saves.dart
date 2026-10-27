import 'dart:async';
import 'dart:convert';
import 'dart:math';
import 'package:flutter/material.dart';
import 'package:hive_flutter/hive_flutter.dart';

Future<void> main() async {
  await Hive.initFlutter();
  await Hive.openBox('saves');
  runApp(const MaterialApp(debugShowCheckedModeBanner: false, home: Aventura()));
}

// os espaços de save: o automático e os do jogador
const espacos = ['auto', '1', '2', '3'];
const int versaoSave = 2; // muda quando o formato do save muda
const int lado = 6; // o quintal tem 6 x 6 casas

class Aventura extends StatefulWidget {
  const Aventura({super.key});

  @override
  State<Aventura> createState() => _AventuraState();
}

class _AventuraState extends State<Aventura> {
  final caixa = Hive.box('saves');
  // o estado do jogo: tudo que precisa voltar igual ao carregar
  int x = 0;
  int y = 0;
  int passos = 0;
  int fase = 1;
  Set<int> ossos = {};
  String aviso = 'Ande com as setas e pegue os ossos.';
  Timer? automatico;
  Map<String, String> resumos = {};

  @override
  void initState() {
    super.initState();
    novaFase(1);
    atualizarResumos();
    // salvamento automático: guarda no espaço "auto" de tempos em tempos
    automatico = Timer.periodic(const Duration(seconds: 10), (t) => salvar('auto'));
  }

  @override
  void dispose() {
    automatico?.cancel();
    super.dispose();
  }

  void novaFase(int n) {
    final sorteio = Random();
    fase = n;
    ossos = {};
    while (ossos.length < 3 + n) {
      final casa = sorteio.nextInt(lado * lado);
      if (casa != y * lado + x) ossos.add(casa);
    }
  }

  void mover(int dx, int dy) {
    setState(() {
      x = (x + dx).clamp(0, lado - 1).toInt();
      y = (y + dy).clamp(0, lado - 1).toInt();
      passos++;
      if (ossos.remove(y * lado + x)) aviso = 'Osso! Faltam ${ossos.length}.';
      if (ossos.isEmpty) {
        novaFase(fase + 1);
        aviso = 'Fase $fase!';
      }
    });
  }

  // o estado vira um Map (e o Map vira texto JSON)
  Map<String, dynamic> paraJson() {
    final agora = DateTime.now();
    return {
      'versao': versaoSave,
      'x': x,
      'y': y,
      'passos': passos,
      'fase': fase,
      'ossos': ossos.toList(),
      'quando': '${agora.day}/${agora.month} ${agora.hour}:${agora.minute.toString().padLeft(2, '0')}',
    };
  }

  void salvar(String espaco) {
    caixa.put(espaco, jsonEncode(paraJson()));
    setState(() {
      atualizarResumos();
      aviso = espaco == 'auto' ? 'Salvo automaticamente.' : 'Jogo salvo no espaço $espaco.';
    });
  }

  void carregar(String espaco) {
    final texto = caixa.get(espaco);
    if (texto == null) return;
    final d = jsonDecode(texto) as Map<String, dynamic>;
    setState(() {
      x = d['x'];
      y = d['y'];
      fase = d['fase'];
      ossos = Set<int>.from(d['ossos']);
      // saves da versão 1 não tinham passos: começa do zero em vez de quebrar
      passos = (d['versao'] ?? 1) >= 2 ? d['passos'] : 0;
      aviso = 'Carregado: ${d['quando']}.';
    });
  }

  // o que aparece no cartão de cada espaço: só lê o save, sem carregar
  void atualizarResumos() {
    for (final n in espacos) {
      final texto = caixa.get(n);
      if (texto == null) {
        resumos[n] = 'vazio';
      } else {
        final d = jsonDecode(texto) as Map<String, dynamic>;
        resumos[n] = 'Fase ${d['fase']} · ${d['ossos'].length} ossos · ${d['quando']}';
      }
    }
  }

  void apagar(String espaco) {
    caixa.delete(espaco);
    setState(() => atualizarResumos());
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Fase $fase · $passos passos · ${ossos.length} ossos')),
      body: ListView(
        padding: const EdgeInsets.all(12),
        children: [
          Center(
            child: SizedBox(
            width: lado * 44.0,
            height: lado * 44.0,
            child: Wrap(
              children: [
                for (var i = 0; i < lado * lado; i++)
                  Container(
                    width: 44,
                    height: 44,
                    alignment: Alignment.center,
                    decoration: BoxDecoration(color: (i ~/ lado + i % lado).isEven ? const Color(0xFFA5D6A7) : const Color(0xFF81C784)),
                    child: Text(i == y * lado + x ? '🐶' : (ossos.contains(i) ? '🦴' : ' '), style: const TextStyle(fontSize: 26)),
                  ),
              ],
            ),
          ),
          ),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              IconButton(icon: const Icon(Icons.arrow_back), onPressed: () => mover(-1, 0)),
              IconButton(icon: const Icon(Icons.arrow_upward), onPressed: () => mover(0, -1)),
              IconButton(icon: const Icon(Icons.arrow_downward), onPressed: () => mover(0, 1)),
              IconButton(icon: const Icon(Icons.arrow_forward), onPressed: () => mover(1, 0)),
            ],
          ),
          Text(aviso, textAlign: TextAlign.center),
          const Divider(),
          for (final n in espacos)
            Card(
              child: ListTile(
                title: Text(n == 'auto' ? 'Automático' : 'Espaço $n'),
                subtitle: Text(resumos[n] ?? 'vazio'),
                trailing: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    IconButton(icon: const Icon(Icons.save), onPressed: n == 'auto' ? null : () => salvar(n)),
                    IconButton(icon: const Icon(Icons.play_arrow), onPressed: () => carregar(n)),
                    IconButton(icon: const Icon(Icons.delete_outline), onPressed: () => apagar(n)),
                  ],
                ),
              ),
            ),
        ],
      ),
    );
  }
}
