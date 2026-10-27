import 'dart:async';
import 'dart:math';
import 'package:flutter/material.dart';
import 'package:supabase_flutter/supabase_flutter.dart';

Future<void> main() async {
  await Supabase.initialize(url: 'https://SEU-PROJETO.supabase.co', anonKey: 'SUA-CHAVE-ANON');
  runApp(const MaterialApp(debugShowCheckedModeBanner: false, home: Sala()));
}

final supabase = Supabase.instance.client;
final sorteio = Random();

const cores = [Colors.orange, Colors.blue, Colors.pink, Colors.green, Colors.purple];

class Sala extends StatefulWidget {
  const Sala({super.key});

  @override
  State<Sala> createState() => _SalaState();
}

class _SalaState extends State<Sala> {
  // cada aparelho escolhe um id e uma cor ao abrir
  final String meuId = 'j${sorteio.nextInt(99999)}';
  final int minhaCor = sorteio.nextInt(cores.length);
  Offset eu = const Offset(180, 300);
  DateTime ultimoEnvio = DateTime(2000);
  Timer? bot;
  Timer? pulso;
  double anguloBot = 0;
  // não mostra quem ficou parado por mais de 15 segundos
  final int segundosAusente = 15;

  @override
  void initState() {
    super.initState();
    enviar(eu, forcar: true);
    // sinal de vida: mesmo parado, avisa a cada 5 segundos que continua na sala
    pulso = Timer.periodic(const Duration(seconds: 5), (t) => enviar(eu, forcar: true));
  }

  // grava a posição na tabela; no máximo 10 vezes por segundo
  Future<void> enviar(Offset p, {bool forcar = false}) async {
    final agora = DateTime.now();
    if (!forcar && agora.difference(ultimoEnvio).inMilliseconds < 100) return;
    ultimoEnvio = agora;
    await supabase.from('jogadores').upsert({
      'id': meuId,
      'cor': minhaCor,
      'x': p.dx,
      'y': p.dy,
      'visto': agora.millisecondsSinceEpoch,
    });
  }

  // apaga a linha do jogador (o pacote só manda o pedido quando há await ou then)
  Future<void> sair(String id) async {
    await supabase.from('jogadores').delete().eq('id', id);
  }

  // um jogador de mentira que anda em círculo, para testar sozinho
  void ligarBot() {
    if (bot != null) {
      bot!.cancel();
      setState(() => bot = null);
      sair('bot');
      return;
    }
    setState(() {
      bot = Timer.periodic(const Duration(milliseconds: 200), (t) async {
        anguloBot += 0.15;
        await supabase.from('jogadores').upsert({
          'id': 'bot',
          'cor': 1,
          'x': 180 + cos(anguloBot) * 110,
          'y': 300 + sin(anguloBot) * 110,
          'visto': DateTime.now().millisecondsSinceEpoch,
        });
        setState(() {});
      });
    });
  }

  @override
  void dispose() {
    bot?.cancel();
    pulso?.cancel();
    sair(meuId);
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFDDEFD2),
      appBar: AppBar(
        title: const Text('Sala online'),
        actions: [
          TextButton(onPressed: ligarBot, child: Text(bot == null ? 'Ligar bot' : 'Desligar bot')),
        ],
      ),
      body: GestureDetector(
        onPanUpdate: (d) {
          setState(() => eu = d.localPosition);
          enviar(eu);
        },
        // ao soltar, manda a posição final (o limite de envios pode ter pulado a última)
        onPanEnd: (d) => enviar(eu, forcar: true),
        onTapDown: (d) {
          setState(() => eu = d.localPosition);
          enviar(eu, forcar: true);
        },
        child: StreamBuilder<List<Map<String, dynamic>>>(
          stream: supabase.from('jogadores').stream(primaryKey: ['id']),
          builder: (context, snapshot) {
            final agora = DateTime.now().millisecondsSinceEpoch;
            final todos = (snapshot.data ?? []).where((j) => agora - (j['visto'] as int) < segundosAusente * 1000).toList();
            return Stack(
              children: [
                Positioned(left: 12, top: 12, child: Text('${todos.length} na sala · arraste para andar')),
                for (final j in todos)
                  if (j['id'] != meuId)
                    Positioned(
                      left: (j['x'] as num).toDouble() - 20,
                      top: (j['y'] as num).toDouble() - 20,
                      child: Bolinha(cor: cores[j['cor'] as int], nome: j['id'] == 'bot' ? 'bot' : 'outro'),
                    ),
                // eu mesmo: desenhado com a posição local, sem esperar o servidor
                Positioned(left: eu.dx - 20, top: eu.dy - 20, child: Bolinha(cor: cores[minhaCor], nome: 'você')),
              ],
            );
          },
        ),
      ),
    );
  }
}

class Bolinha extends StatelessWidget {
  final Color cor;
  final String nome;
  const Bolinha({super.key, required this.cor, required this.nome});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Container(width: 40, height: 40, decoration: BoxDecoration(color: cor, shape: BoxShape.circle, border: Border.all(color: Colors.white, width: 3))),
        Text(nome, style: const TextStyle(fontSize: 12)),
      ],
    );
  }
}
