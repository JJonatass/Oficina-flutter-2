import 'dart:math';
import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(debugShowCheckedModeBanner: false, home: Bau()));

class Item {
  final String nome;
  final int peso;
  final Color cor;
  const Item(this.nome, this.peso, this.cor);
}

// a tabela de prêmios: quanto maior o peso, mais fácil de sair
const tabela = [
  Item('Osso', 60, Color(0xFFE9D8A6)),
  Item('Bola', 25, Color(0xFF64B5F6)),
  Item('Coleira', 12, Color(0xFFBA68C8)),
  Item('Osso dourado', 3, Color(0xFFFFC107)),
];

final sorteio = Random();

// sorteio com pesos: escolhe um número de 0 até a soma e vê em que faixa ele caiu
Item sortearComPeso() {
  final total = tabela.fold(0, (soma, i) => soma + i.peso);
  var n = sorteio.nextInt(total);
  for (final item in tabela) {
    if (n < item.peso) return item;
    n -= item.peso;
  }
  return tabela.last;
}

class Bau extends StatefulWidget {
  const Bau({super.key});

  @override
  State<Bau> createState() => _BauState();
}

class _BauState extends State<Bau> {
  final Map<String, int> contagem = {};
  int abertos = 0;
  String ultimo = '';
  // garantia: depois de tantas aberturas sem dourado, o próximo é dourado
  int semDourado = 0;
  final int garantia = 40;
  bool usarGarantia = false;

  void abrir(int vezes) {
    setState(() {
      for (int i = 0; i < vezes; i++) {
        var item = sortearComPeso();
        if (usarGarantia && semDourado >= garantia - 1) item = tabela.last;
        semDourado = item.nome == 'Osso dourado' ? 0 : semDourado + 1;
        contagem[item.nome] = (contagem[item.nome] ?? 0) + 1;
        abertos++;
        ultimo = item.nome;
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    final total = tabela.fold(0, (soma, i) => soma + i.peso);
    return Scaffold(
      appBar: AppBar(title: Text('Baús abertos: $abertos')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Text(ultimo.isEmpty ? 'Abra um baú!' : 'Saiu: $ultimo', style: const TextStyle(fontSize: 22), textAlign: TextAlign.center),
            const SizedBox(height: 12),
            for (final item in tabela)
              Padding(
                padding: const EdgeInsets.symmetric(vertical: 6),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text('${item.nome}: esperado ${(item.peso * 100 / total).toStringAsFixed(0)}%, saiu '
                        '${abertos == 0 ? 0 : ((contagem[item.nome] ?? 0) * 100 / abertos).toStringAsFixed(1)}% (${contagem[item.nome] ?? 0})'),
                    const SizedBox(height: 4),
                    LinearProgressIndicator(
                      value: abertos == 0 ? 0 : (contagem[item.nome] ?? 0) / abertos,
                      minHeight: 14,
                      color: item.cor,
                      backgroundColor: Colors.black12,
                    ),
                  ],
                ),
              ),
            Text('Aberturas seguidas sem dourado: $semDourado'),
            SwitchListTile(
              title: Text('Garantia: dourado em no máximo $garantia'),
              value: usarGarantia,
              onChanged: (v) => setState(() => usarGarantia = v),
            ),
            const Spacer(),
            Row(
              children: [
                Expanded(child: FilledButton(onPressed: () => abrir(1), child: const Text('Abrir 1'))),
                const SizedBox(width: 8),
                Expanded(child: OutlinedButton(onPressed: () => abrir(100), child: const Text('Abrir 100'))),
                const SizedBox(width: 8),
                IconButton(
                  onPressed: () => setState(() {
                    contagem.clear();
                    abertos = 0;
                    semDourado = 0;
                    ultimo = '';
                  }),
                  icon: const Icon(Icons.refresh),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
