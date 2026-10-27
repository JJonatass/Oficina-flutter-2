import 'dart:convert';
import 'dart:math';
import 'package:flutter/material.dart';
import 'package:hive_flutter/hive_flutter.dart';

Future<void> main() async {
  await Hive.initFlutter();
  await Hive.openBox('mochila');
  runApp(const MaterialApp(debugShowCheckedModeBanner: false, home: Mochila()));
}

// O tipo do item: o que ele é e como funciona (não muda durante o jogo)
class TipoItem {
  final String id;
  final String nome;
  final String icone;
  final int pilhaMax;
  final String efeito;
  const TipoItem(this.id, this.nome, this.icone, this.pilhaMax, this.efeito);
}

const catalogo = {
  'osso': TipoItem('osso', 'Osso', '🦴', 10, 'Recupera 1 vida'),
  'bola': TipoItem('bola', 'Bola', '🎾', 3, 'Distrai um gato'),
  'coleira': TipoItem('coleira', 'Coleira azul', '📿', 1, 'Equipar: +1 de velocidade'),
  'mapa': TipoItem('mapa', 'Mapa do bairro', '🗺️', 1, 'Mostra os segredos'),
};

// Uma casa da mochila: qual item e quantos
class Pilha {
  final String id;
  int quantidade;
  Pilha(this.id, this.quantidade);

  // para salvar: objeto -> Map -> texto JSON
  Map<String, dynamic> toJson() => {'id': id, 'q': quantidade};
  // para carregar: texto JSON -> Map -> objeto
  factory Pilha.fromJson(Map<String, dynamic> m) => Pilha(m['id'], m['q']);
}

class Mochila extends StatefulWidget {
  const Mochila({super.key});

  @override
  State<Mochila> createState() => _MochilaState();
}

class _MochilaState extends State<Mochila> {
  final int capacidade = 8;
  final sorteio = Random();
  List<Pilha> casas = [];
  int vidas = 2;
  String? equipado;
  String aviso = 'Explore o bairro para achar coisas.';

  @override
  void initState() {
    super.initState();
    carregar();
  }

  void carregar() {
    final texto = Hive.box('mochila').get('itens', defaultValue: '[]');
    final lista = jsonDecode(texto) as List;
    casas = lista.map((m) => Pilha.fromJson(m)).toList();
    equipado = Hive.box('mochila').get('equipado');
  }

  void salvar() {
    Hive.box('mochila').put('itens', jsonEncode(casas.map((p) => p.toJson()).toList()));
    Hive.box('mochila').put('equipado', equipado);
  }

  // guarda um item: completa uma pilha que já existe ou ocupa uma casa nova
  bool guardar(String id) {
    final tipo = catalogo[id]!;
    for (final p in casas) {
      if (p.id == id && p.quantidade < tipo.pilhaMax) {
        p.quantidade++;
        return true;
      }
    }
    if (casas.length >= capacidade) return false;
    casas.add(Pilha(id, 1));
    return true;
  }

  void explorar() {
    final ids = catalogo.keys.toList();
    final id = ids[sorteio.nextInt(ids.length)];
    setState(() {
      aviso = guardar(id) ? 'Achou: ${catalogo[id]!.icone} ${catalogo[id]!.nome}' : 'Mochila cheia! Use ou largue alguma coisa.';
      salvar();
    });
  }

  void usar(Pilha p) {
    final tipo = catalogo[p.id]!;
    setState(() {
      if (p.id == 'coleira') {
        equipado = equipado == 'coleira' ? null : 'coleira';
        aviso = equipado == null ? 'Tirou a coleira.' : 'Equipou a coleira: mais rápido!';
      } else {
        if (p.id == 'osso') vidas = min(3, vidas + 1);
        aviso = 'Usou ${tipo.nome}: ${tipo.efeito}.';
        p.quantidade--;
        if (p.quantidade == 0) casas.remove(p);
      }
      salvar();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Mochila ${casas.length}/$capacidade   ${'♥' * vidas}'), actions: [
        IconButton(icon: const Icon(Icons.delete_outline), onPressed: () => setState(() {
              casas.clear();
              equipado = null;
              salvar();
            })),
      ]),
      body: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Text(aviso, style: const TextStyle(fontSize: 16)),
            const SizedBox(height: 12),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: [
                for (int i = 0; i < capacidade; i++)
                  GestureDetector(
                    onTap: i < casas.length ? () => usar(casas[i]) : null,
                    child: Container(
                      width: 76,
                      height: 76,
                      alignment: Alignment.center,
                      decoration: BoxDecoration(
                        color: i < casas.length && casas[i].id == equipado ? Colors.amber.shade200 : Colors.brown.shade100,
                        borderRadius: BorderRadius.circular(10),
                        border: Border.all(color: Colors.brown, width: 2),
                      ),
                      child: i < casas.length
                          ? Text('${catalogo[casas[i].id]!.icone}\n${casas[i].quantidade > 1 ? '×${casas[i].quantidade}' : ''}', textAlign: TextAlign.center, style: const TextStyle(fontSize: 26))
                          : const Text(''),
                    ),
                  ),
              ],
            ),
            const SizedBox(height: 12),
            const Text('Toque num item para usar (a coleira equipa e desequipa).'),
            const Spacer(),
            FilledButton(onPressed: explorar, child: const Text('Explorar o bairro')),
          ],
        ),
      ),
    );
  }
}
