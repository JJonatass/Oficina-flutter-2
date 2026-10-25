# Aulas da Oficina Flutter 2 · trilha de jogos.
# Cada código é um app Flutter completo: roda no simulador e também num projeto real.

LESSONS = []
EXERCISES = {}


def aula(t, text, tryit, code, ex, lim=None, setup=None):
    LESSONS.append({'t': t, 'text': text, 'tryit': tryit, 'code': code, 'lim': lim, 'setup': setup})
    EXERCISES[t] = ex


# ---------------------------------------------------------------- Parte 1
aula(
    'O laço do jogo com Timer.periodic',
    'Todo jogo é um laço que se repete muitas vezes por segundo: atualizar o mundo (mover, testar, contar) e '
    'desenhar de novo. O jeito mais simples de montar esse laço em Flutter é um Timer.periodic, do pacote '
    'dart:async. A cada 16 milissegundos (cerca de 60 vezes por segundo) a função recebe o timer, muda a '
    'posição x dentro do setState e o build desenha o quadrado no lugar novo, com um Positioned dentro de um '
    'Stack. Quando o quadrado passa da borda direita, ele volta pela esquerda. O botão chama cancel() para '
    'pausar e cria um Timer novo para continuar. Em dispose() o timer é cancelado, senão ele continua rodando '
    'depois que a tela fecha.',
    'Em ▶ Testar, veja o quadrado atravessar a tela e use o botão para pausar. Mude o passo de 3 para 8, troque '
    'o intervalo de 16 para 100 milissegundos e compare: o movimento fica rápido, depois aos saltos.',
    r'''
import 'dart:async';
import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(home: Jogo()));

class Jogo extends StatefulWidget {
  const Jogo({super.key});

  @override
  State<Jogo> createState() => _JogoState();
}

class _JogoState extends State<Jogo> {
  double x = 0;
  Timer? timer;
  bool rodando = false;

  @override
  void initState() {
    super.initState();
    iniciar();
  }

  void iniciar() {
    rodando = true;
    timer = Timer.periodic(const Duration(milliseconds: 16), (t) {
      setState(() {
        x += 3;
        if (x > 360) {
          x = -40;
        }
      });
    });
  }

  void alternar() {
    setState(() {
      if (rodando) {
        timer?.cancel();
        rodando = false;
      } else {
        iniciar();
      }
    });
  }

  @override
  void dispose() {
    timer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.indigo.shade900,
      appBar: AppBar(title: const Text('O laço do jogo')),
      body: Stack(
        children: [
          Positioned(
            left: x,
            top: 200,
            child: Container(width: 40, height: 40, color: Colors.amber),
          ),
          Positioned(
            left: 16,
            bottom: 16,
            child: Text('x = ${x.toStringAsFixed(0)}', style: const TextStyle(color: Colors.white, fontSize: 18)),
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: alternar,
        child: Icon(rodando ? Icons.pause : Icons.play_arrow),
      ),
    );
  }
}
''',
    [
        ['Passo de 8 pixels', 'Dentro do setState, troque x += 3 por x += 8.', r'x\s*\+=\s*8\b'],
        ['Intervalo de 100 ms', 'No Timer.periodic, troque milliseconds: 16 por milliseconds: 100.', r'Timer\.periodic\(\s*const\s+Duration\(\s*milliseconds:\s*100\s*\)'],
        ['Quadrado mais baixo (top: 400)', 'No primeiro Positioned, troque top: 200 por top: 400.', r'left:\s*x,\s*top:\s*400'],
        ['Andar para a esquerda', 'Use x -= 3 e faça o quadrado voltar pela direita: if (x < -40) x = 360.', r'x\s*-=\s*\d[\s\S]*x\s*<\s*-40'],
    ],
)

aula(
    'Ticker e delta time',
    'O Timer não acompanha a tela: ele pode disparar fora de hora e o movimento treme. O Ticker é o relógio '
    'que o próprio Flutter usa nas animações: ele chama a sua função uma vez a cada quadro desenhado, com o '
    'tempo que passou desde o start(). Para ter um, o State usa o mixin SingleTickerProviderStateMixin e chama '
    'createTicker(quadro). Dentro de quadro, o delta time (dt) é o tempo entre este quadro e o anterior, em '
    'segundos. Com ele a velocidade passa a ser em pixels por segundo: x += velocidade * dt. Assim o jogo anda '
    'igual num celular de 60 Hz e num de 120 Hz, porque o de 120 Hz dá passos menores, mas o dobro deles. O '
    'texto de cima mostra quantos quadros por segundo (fps) estão sendo desenhados.',
    'Em ▶ Testar, confira o fps. Mude a velocidade de 120 para 300 e veja que o tempo para cruzar a tela cai '
    'pela metade (ou mais), sem mexer no laço. Depois faça o quadrado quicar nas bordas trocando o sinal da '
    'velocidade.',
    r'''
import 'package:flutter/material.dart';
import 'package:flutter/scheduler.dart';

void main() => runApp(const MaterialApp(home: Jogo()));

class Jogo extends StatefulWidget {
  const Jogo({super.key});

  @override
  State<Jogo> createState() => _JogoState();
}

class _JogoState extends State<Jogo> with SingleTickerProviderStateMixin {
  late Ticker ticker;
  double x = 0;
  double velocidade = 120;
  double ultimo = 0;
  double fps = 0;

  @override
  void initState() {
    super.initState();
    ticker = createTicker(quadro);
    ticker.start();
  }

  void quadro(Duration tempo) {
    final agora = tempo.inMicroseconds / 1000000;
    final dt = agora - ultimo;
    ultimo = agora;
    setState(() {
      x += velocidade * dt;
      if (x > 360) {
        x = -40;
      }
      if (dt > 0) {
        fps = 1 / dt;
      }
    });
  }

  @override
  void dispose() {
    ticker.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.indigo.shade900,
      appBar: AppBar(title: Text('${fps.toStringAsFixed(0)} fps')),
      body: Stack(
        children: [
          Positioned(
            left: x,
            top: 200,
            child: Container(width: 40, height: 40, color: Colors.lightGreenAccent),
          ),
          Positioned(
            left: 16,
            bottom: 16,
            child: Text('${velocidade.toStringAsFixed(0)} px/s', style: const TextStyle(color: Colors.white, fontSize: 18)),
          ),
        ],
      ),
    );
  }
}
''',
    [
        ['Velocidade de 300 px/s', 'Troque double velocidade = 120 por 300.', r'double velocidade\s*=\s*300\b'],
        ['Quicar na borda direita', 'Quando x passar de 320, inverta a velocidade: velocidade = -velocidade.', r'velocidade\s*=\s*-\s*velocidade'],
        ['Mostrar o dt na tela', "Guarde o dt num campo e mostre com dt.toStringAsFixed(3) em um Text.", r'dt\.toStringAsFixed\(\s*3\s*\)'],
    ],
    lim='O simulador desenha no ritmo do navegador, em geral 60 quadros por segundo. O fps varia um pouco a cada quadro, como num aparelho real.',
)

aula(
    'Desenhando o jogo com CustomPainter',
    'Com muitos objetos, montar o jogo com Container e Positioned fica pesado e difícil de ler. Jogos 2D '
    'costumam desenhar tudo num Canvas: o CustomPaint dá a área e o CustomPainter desenha nela. A cena recebe o '
    'estado do jogo pelo construtor (aqui, x e direcao) e o método paint pinta, de trás para a frente: céu, '
    'sol, chão e personagem. O que é pintado depois fica por cima. O tamanho do mundo fica em constantes '
    '(largura, altura e chao), assim o desenho e as regras usam os mesmos números. O shouldRepaint compara a '
    'cena antiga com a nova e só redesenha quando algo mudou. O olho segue a direcao: +1 olha para a direita, '
    '-1 para a esquerda.',
    'Em ▶ Testar, veja o personagem ir e voltar. Troque a cor do céu, desenhe uma nuvem (três drawCircle '
    'brancos juntos) e mude a altura do chão para 400.',
    r'''
import 'package:flutter/material.dart';
import 'package:flutter/scheduler.dart';

void main() => runApp(const MaterialApp(home: Jogo()));

const double largura = 360;
const double altura = 520;
const double chao = 440;

class Cena extends CustomPainter {
  final double x;
  final double direcao;
  Cena(this.x, this.direcao);

  @override
  void paint(Canvas canvas, Size size) {
    canvas.drawRect(Rect.fromLTWH(0, 0, size.width, size.height), Paint()..color = const Color(0xFF7EC8F2));
    canvas.drawCircle(const Offset(290, 80), 36, Paint()..color = Colors.yellow);
    canvas.drawRect(Rect.fromLTWH(0, chao, size.width, size.height - chao), Paint()..color = Colors.green.shade700);

    final corpo = Rect.fromLTWH(x, chao - 48, 40, 48);
    canvas.drawRRect(RRect.fromRectAndRadius(corpo, const Radius.circular(8)), Paint()..color = Colors.deepOrange);
    final olho = Offset(x + 20 + direcao * 8, chao - 34);
    canvas.drawCircle(olho, 6, Paint()..color = Colors.white);
    canvas.drawCircle(olho + Offset(direcao * 2, 0), 3, Paint()..color = Colors.black);
  }

  @override
  bool shouldRepaint(covariant Cena antiga) => antiga.x != x || antiga.direcao != direcao;
}

class Jogo extends StatefulWidget {
  const Jogo({super.key});

  @override
  State<Jogo> createState() => _JogoState();
}

class _JogoState extends State<Jogo> with SingleTickerProviderStateMixin {
  late Ticker ticker;
  double ultimo = 0;
  double x = 20;
  double direcao = 1;
  double velocidade = 140;

  @override
  void initState() {
    super.initState();
    ticker = createTicker(quadro);
    ticker.start();
  }

  void quadro(Duration tempo) {
    final agora = tempo.inMicroseconds / 1000000;
    final dt = agora - ultimo;
    ultimo = agora;
    setState(() {
      x += velocidade * direcao * dt;
      if (x > largura - 40) {
        x = largura - 40;
        direcao = -1;
      }
      if (x < 0) {
        x = 0;
        direcao = 1;
      }
    });
  }

  @override
  void dispose() {
    ticker.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: Center(
        child: CustomPaint(
          size: const Size(largura, altura),
          painter: Cena(x, direcao),
        ),
      ),
    );
  }
}
''',
    [
        ['Céu de outra cor', 'No primeiro drawRect, troque Color(0xFF7EC8F2) por outra cor, como Colors.indigo.shade200.', r'^(?![\s\S]*0xFF7EC8F2)'],
        ['Uma nuvem com três círculos', 'Depois do sol, acrescente três canvas.drawCircle brancos, um ao lado do outro.', r'(?:drawCircle\([^;]*Colors\.white[\s\S]*?){3}'],
        ['Chão mais alto (chao = 400)', 'Mude a constante: const double chao = 400.', r'const double chao\s*=\s*400\b'],
    ],
)

aula(
    'Toque: o personagem vai até o dedo',
    'Jogo precisa de entrada. No celular, a mais comum é o toque. O GestureDetector em volta do CustomPaint '
    'chama onTapDown com TapDownDetails, e details.localPosition diz onde o dedo tocou, medido a partir do canto '
    'de cima à esquerda da área do jogo. O toque não move o personagem na hora: ele só guarda um alvo. Quem '
    'anda é o laço, a cada quadro, no máximo velocidade * dt pixels na direção do alvo. Se faltar menos que um '
    'passo, o personagem para em cima do alvo. Repare que tocar não chama setState: o Ticker já chama setState '
    'a cada quadro, então o alvo novo aparece no próximo desenho. Separar a entrada (o que o jogador quer) da '
    'atualização (o que acontece no mundo) é a base de qualquer jogo.',
    'Em ▶ Testar, toque em vários pontos do chão e veja o personagem caminhar até a marca. Aumente a velocidade, '
    'troque a cor da marca e faça o personagem também mudar de cor enquanto está andando.',
    r'''
import 'package:flutter/material.dart';
import 'package:flutter/scheduler.dart';

void main() => runApp(const MaterialApp(home: Jogo()));

const double largura = 360;
const double altura = 520;
const double chao = 440;

class Cena extends CustomPainter {
  final double x;
  final double alvo;
  Cena(this.x, this.alvo);

  @override
  void paint(Canvas canvas, Size size) {
    canvas.drawRect(Rect.fromLTWH(0, 0, size.width, size.height), Paint()..color = const Color(0xFF7EC8F2));
    canvas.drawRect(Rect.fromLTWH(0, chao, size.width, size.height - chao), Paint()..color = Colors.green.shade700);

    final marca = Paint()
      ..color = Colors.white
      ..style = PaintingStyle.stroke
      ..strokeWidth = 3;
    canvas.drawCircle(Offset(alvo + 20, chao + 12), 8, marca);

    final corpo = Rect.fromLTWH(x, chao - 48, 40, 48);
    canvas.drawRRect(RRect.fromRectAndRadius(corpo, const Radius.circular(8)), Paint()..color = Colors.deepOrange);
  }

  @override
  bool shouldRepaint(covariant Cena antiga) => antiga.x != x || antiga.alvo != alvo;
}

class Jogo extends StatefulWidget {
  const Jogo({super.key});

  @override
  State<Jogo> createState() => _JogoState();
}

class _JogoState extends State<Jogo> with SingleTickerProviderStateMixin {
  late Ticker ticker;
  double ultimo = 0;
  double x = 160;
  double alvo = 160;
  double velocidade = 180;

  @override
  void initState() {
    super.initState();
    ticker = createTicker(quadro);
    ticker.start();
  }

  void quadro(Duration tempo) {
    final agora = tempo.inMicroseconds / 1000000;
    final dt = agora - ultimo;
    ultimo = agora;
    setState(() {
      final distancia = alvo - x;
      final passo = velocidade * dt;
      if (distancia.abs() <= passo) {
        x = alvo;
      } else if (distancia > 0) {
        x += passo;
      } else {
        x -= passo;
      }
    });
  }

  void tocar(TapDownDetails details) {
    var novo = details.localPosition.dx - 20;
    if (novo < 0) novo = 0;
    if (novo > largura - 40) novo = largura - 40;
    alvo = novo;
  }

  @override
  void dispose() {
    ticker.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: Center(
        child: GestureDetector(
          onTapDown: tocar,
          child: CustomPaint(
            size: const Size(largura, altura),
            painter: Cena(x, alvo),
          ),
        ),
      ),
    );
  }
}
''',
    [
        ['Velocidade de 400 px/s', 'Troque double velocidade = 180 por 400.', r'double velocidade\s*=\s*400\b'],
        ['Marca amarela', 'No Paint da marca, troque Colors.white por Colors.yellow.', r'marca\s*=\s*Paint\(\)\s*\.\.color\s*=\s*Colors\.yellow'],
        ['Cor diferente enquanto anda', 'Passe para a Cena se x != alvo e use um operador ternário na cor do corpo.', r'\?\s*Colors\.\w+[\s\S]{0,40}:\s*Colors\.deepOrange|\?\s*Colors\.deepOrange[\s\S]{0,40}:\s*Colors\.\w+'],
    ],
)

aula(
    'Gravidade e pulo',
    'Pular é física simples, quadro a quadro. O personagem tem uma posição y e uma velocidade vertical vy. A '
    'gravidade aumenta vy um pouco a cada quadro (vy += gravidade * dt), e a velocidade muda a posição '
    '(y += vy * dt). No Canvas o y cresce para baixo, então gravidade é positiva e o impulso do pulo é negativo. '
    'Quando o pé passa do chão, o laço corrige a posição e zera vy: é a colisão mais simples que existe. O pulo '
    'só vale com o pé no chão (noChao), senão o jogador voaria tocando sem parar. A sombra encolhe com a altura '
    'e ajuda a perceber o salto.',
    'Em ▶ Testar, toque para pular. Aumente o impulso para -800, reduza a gravidade para 600 (pulo na Lua) e '
    'depois permita um pulo duplo: um segundo pulo no ar, mas só um.',
    r'''
import 'package:flutter/material.dart';
import 'package:flutter/scheduler.dart';

void main() => runApp(const MaterialApp(home: Jogo()));

const double largura = 360;
const double altura = 520;
const double chao = 440;
const double gravidade = 1500;
const double impulso = -620;

class Cena extends CustomPainter {
  final double y;
  Cena(this.y);

  @override
  void paint(Canvas canvas, Size size) {
    canvas.drawRect(Rect.fromLTWH(0, 0, size.width, size.height), Paint()..color = const Color(0xFF7EC8F2));
    canvas.drawRect(Rect.fromLTWH(0, chao, size.width, size.height - chao), Paint()..color = Colors.green.shade700);

    final alturaDoPulo = chao - (y + 48);
    final sombra = 40 - alturaDoPulo / 10;
    canvas.drawOval(
      Rect.fromCenter(center: Offset(160, chao + 4), width: sombra < 10 ? 10.0 : sombra, height: 8),
      Paint()..color = Colors.black26,
    );
    final corpo = Rect.fromLTWH(140, y, 40, 48);
    canvas.drawRRect(RRect.fromRectAndRadius(corpo, const Radius.circular(8)), Paint()..color = Colors.deepOrange);
  }

  @override
  bool shouldRepaint(covariant Cena antiga) => antiga.y != y;
}

class Jogo extends StatefulWidget {
  const Jogo({super.key});

  @override
  State<Jogo> createState() => _JogoState();
}

class _JogoState extends State<Jogo> with SingleTickerProviderStateMixin {
  late Ticker ticker;
  double ultimo = 0;
  double y = chao - 48;
  double vy = 0;
  int pulos = 0;

  bool get noChao => y >= chao - 48;

  @override
  void initState() {
    super.initState();
    ticker = createTicker(quadro);
    ticker.start();
  }

  void quadro(Duration tempo) {
    final agora = tempo.inMicroseconds / 1000000;
    final dt = agora - ultimo;
    ultimo = agora;
    setState(() {
      vy += gravidade * dt;
      y += vy * dt;
      if (y > chao - 48) {
        y = chao - 48;
        vy = 0;
      }
    });
  }

  void pular() {
    if (noChao) {
      vy = impulso;
      pulos++;
    }
  }

  @override
  void dispose() {
    ticker.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(title: Text('Pulos: $pulos')),
      body: Center(
        child: GestureDetector(
          onTapDown: (_) => pular(),
          child: CustomPaint(
            size: const Size(largura, altura),
            painter: Cena(y),
          ),
        ),
      ),
    );
  }
}
''',
    [
        ['Impulso de -800', 'Troque const double impulso = -620 por -800.', r'const double impulso\s*=\s*-800\b'],
        ['Gravidade da Lua (600)', 'Troque const double gravidade = 1500 por 600.', r'const double gravidade\s*=\s*600\b'],
        ['Pulo duplo', 'Guarde quantos pulos foram dados no ar (zere ao tocar o chão) e aceite o pulo se noChao ou se ainda não usou o segundo.', r'noChao\s*\|\||\|\|\s*noChao'],
    ],
)

aula(
    'Muitos objetos: lista, sorteio e remoção',
    'Um jogo tem vários objetos iguais: inimigos, moedas, caixas. Cada um vira uma instância de uma classe '
    '(aqui, Caixa, com x e altura) e todos ficam numa List. O laço faz três coisas com a lista. Criar (spawn): '
    'um contador regressivo, tempoProxima, diz quando nasce a próxima caixa, e Random sorteia a altura e o '
    'intervalo, para o jogo não ficar previsível. Mover: um for passa por todas e diminui o x. Remover: '
    'removeWhere tira as que saíram pela esquerda. Sem a remoção, a lista cresceria para sempre e o jogo '
    'ficaria cada vez mais lento. O texto no topo mostra quantas caixas existem agora e quantas já nasceram.',
    'Em ▶ Testar, confira que o número de caixas na tela fica pequeno, mesmo com o total crescendo. Faça as '
    'caixas nascerem mais seguido, sorteie também a largura e apague o removeWhere para ver a lista crescer.',
    r'''
import 'dart:math';
import 'package:flutter/material.dart';
import 'package:flutter/scheduler.dart';

void main() => runApp(const MaterialApp(home: Jogo()));

const double largura = 360;
const double altura = 520;
const double chao = 440;

class Caixa {
  double x;
  final double altura;
  Caixa(this.x, this.altura);
}

class Cena extends CustomPainter {
  final List<Caixa> caixas;
  Cena(this.caixas);

  @override
  void paint(Canvas canvas, Size size) {
    canvas.drawRect(Rect.fromLTWH(0, 0, size.width, size.height), Paint()..color = const Color(0xFF7EC8F2));
    canvas.drawRect(Rect.fromLTWH(0, chao, size.width, size.height - chao), Paint()..color = Colors.green.shade700);
    final tinta = Paint()..color = Colors.brown;
    for (final c in caixas) {
      canvas.drawRect(Rect.fromLTWH(c.x, chao - c.altura, 30, c.altura), tinta);
    }
  }

  @override
  bool shouldRepaint(covariant Cena antiga) => true;
}

class Jogo extends StatefulWidget {
  const Jogo({super.key});

  @override
  State<Jogo> createState() => _JogoState();
}

class _JogoState extends State<Jogo> with SingleTickerProviderStateMixin {
  late Ticker ticker;
  double ultimo = 0;
  final sorteio = Random();
  List<Caixa> caixas = [];
  double tempoProxima = 0;
  double velocidade = 200;
  int nascidas = 0;

  @override
  void initState() {
    super.initState();
    ticker = createTicker(quadro);
    ticker.start();
  }

  void quadro(Duration tempo) {
    final agora = tempo.inMicroseconds / 1000000;
    final dt = agora - ultimo;
    ultimo = agora;
    setState(() {
      tempoProxima -= dt;
      if (tempoProxima <= 0) {
        caixas.add(Caixa(largura, 30 + sorteio.nextDouble() * 60));
        nascidas++;
        tempoProxima = 0.8 + sorteio.nextDouble() * 1.2;
      }
      for (final c in caixas) {
        c.x -= velocidade * dt;
      }
      caixas.removeWhere((c) => c.x < -30);
    });
  }

  @override
  void dispose() {
    ticker.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(title: Text('Na tela: ${caixas.length} · nascidas: $nascidas')),
      body: Center(
        child: CustomPaint(
          size: const Size(largura, altura),
          painter: Cena(caixas),
        ),
      ),
    );
  }
}
''',
    [
        ['Intervalo menor (0.4)', 'Na linha do tempoProxima sorteado, troque 0.8 por 0.4.', r'tempoProxima\s*=\s*0\.4\b'],
        ['Caixas cinza', 'Na Cena, troque Colors.brown por Colors.blueGrey.', r'tinta\s*=\s*Paint\(\)\s*\.\.color\s*=\s*Colors\.blueGrey'],
        ['Largura sorteada', 'Acrescente um campo largura na Caixa, sorteie no add e use c.largura no drawRect.', r'c\.largura'],
    ],
)

aula(
    'Colisão com retângulos (AABB)',
    'Para saber se o personagem bateu numa caixa, o jeito mais usado em jogos 2D é comparar retângulos alinhados '
    'aos eixos (AABB, axis-aligned bounding box). Cada objeto ganha um Rect com a sua área, e rect.overlaps(outro) '
    'diz se os dois se cruzam: isso acontece quando um começa antes de o outro terminar, na horizontal e na '
    'vertical ao mesmo tempo. Aqui o personagem pula sobre as caixas da aula anterior. Se bater, a caixa some, '
    'batidas aumenta e o personagem fica vermelho por 0,3 segundo (tempoVermelho conta para baixo no laço). '
    'Repare no retângulo do jogador um pouco menor que o desenho (deflate): deixa a colisão mais justa para '
    'quem joga.',
    'Em ▶ Testar, pule as caixas e deixe algumas baterem. Tire o deflate e sinta a diferença. Depois faça o '
    'personagem ganhar 1 ponto por caixa que passar sem bater.',
    r'''
import 'dart:math';
import 'package:flutter/material.dart';
import 'package:flutter/scheduler.dart';

void main() => runApp(const MaterialApp(home: Jogo()));

const double largura = 360;
const double altura = 520;
const double chao = 440;
const double gravidade = 1500;
const double impulso = -620;
const double jogadorX = 60;

class Caixa {
  double x;
  final double altura;
  Caixa(this.x, this.altura);

  Rect get area => Rect.fromLTWH(x, chao - altura, 30, altura);
}

class Cena extends CustomPainter {
  final double y;
  final List<Caixa> caixas;
  final bool vermelho;
  Cena(this.y, this.caixas, this.vermelho);

  @override
  void paint(Canvas canvas, Size size) {
    canvas.drawRect(Rect.fromLTWH(0, 0, size.width, size.height), Paint()..color = const Color(0xFF7EC8F2));
    canvas.drawRect(Rect.fromLTWH(0, chao, size.width, size.height - chao), Paint()..color = Colors.green.shade700);
    for (final c in caixas) {
      canvas.drawRect(c.area, Paint()..color = Colors.brown);
    }
    final corpo = Rect.fromLTWH(jogadorX, y, 40, 48);
    canvas.drawRRect(
      RRect.fromRectAndRadius(corpo, const Radius.circular(8)),
      Paint()..color = vermelho ? Colors.red : Colors.deepOrange,
    );
  }

  @override
  bool shouldRepaint(covariant Cena antiga) => true;
}

class Jogo extends StatefulWidget {
  const Jogo({super.key});

  @override
  State<Jogo> createState() => _JogoState();
}

class _JogoState extends State<Jogo> with SingleTickerProviderStateMixin {
  late Ticker ticker;
  double ultimo = 0;
  final sorteio = Random();
  double y = chao - 48;
  double vy = 0;
  List<Caixa> caixas = [];
  double tempoProxima = 1;
  double tempoVermelho = 0;
  int batidas = 0;

  @override
  void initState() {
    super.initState();
    ticker = createTicker(quadro);
    ticker.start();
  }

  void quadro(Duration tempo) {
    final agora = tempo.inMicroseconds / 1000000;
    final dt = agora - ultimo;
    ultimo = agora;
    setState(() => atualizar(dt));
  }

  void atualizar(double dt) {
    vy += gravidade * dt;
    y += vy * dt;
    if (y > chao - 48) {
      y = chao - 48;
      vy = 0;
    }

    tempoProxima -= dt;
    if (tempoProxima <= 0) {
      caixas.add(Caixa(largura, 30 + sorteio.nextDouble() * 40));
      tempoProxima = 1 + sorteio.nextDouble() * 1.2;
    }
    for (final c in caixas) {
      c.x -= 200 * dt;
    }
    caixas.removeWhere((c) => c.x < -30);

    final jogador = Rect.fromLTWH(jogadorX, y, 40, 48).deflate(4);
    final atingidas = caixas.where((c) => c.area.overlaps(jogador)).toList();
    if (atingidas.isNotEmpty) {
      batidas += atingidas.length;
      tempoVermelho = 0.3;
      caixas.removeWhere((c) => atingidas.contains(c));
    }
    if (tempoVermelho > 0) {
      tempoVermelho -= dt;
    }
  }

  void pular() {
    if (y >= chao - 48) {
      vy = impulso;
    }
  }

  @override
  void dispose() {
    ticker.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(title: Text('Batidas: $batidas')),
      body: Center(
        child: GestureDetector(
          onTapDown: (_) => pular(),
          child: CustomPaint(
            size: const Size(largura, altura),
            painter: Cena(y, caixas, tempoVermelho > 0),
          ),
        ),
      ),
    );
  }
}
''',
    [
        ['Colisão sem folga', 'Apague o .deflate(4) do retângulo do jogador.', r'final jogador\s*=\s*Rect\.fromLTWH\(\s*jogadorX,\s*y,\s*40,\s*48\s*\);'],
        ['Piscar por meio segundo', 'Troque tempoVermelho = 0.3 por 0.5.', r'tempoVermelho\s*=\s*0\.5\b'],
        ['Ponto por caixa pulada', 'Crie int pontos e some 1 quando uma caixa passar do jogador sem bater (dica: um campo bool contada na Caixa).', r'pontos\s*(?:\+\+|\+=\s*1)'],
    ],
)

aula(
    'Estados do jogo: pronto, jogando e fim',
    'Um jogo completo tem fases: a tela de início, a partida e o game over. Um enum deixa isso claro: Estado.pronto, '
    'Estado.jogando e Estado.fim. O laço continua rodando sempre (para o dt não dar um salto), mas só atualiza o '
    'mundo quando o estado é jogando. O mesmo toque faz coisas diferentes em cada estado: começar, pular ou '
    'reiniciar. As mensagens e a pontuação ficam em widgets por cima do CustomPaint, num Stack: é o HUD '
    '(heads-up display). O if dentro da lista de children mostra cada mensagem só no estado certo. Agora bater '
    'numa caixa termina a partida, e cada caixa que passa pelo jogador vale um ponto (o campo contada impede de '
    'contar a mesma caixa duas vezes).',
    'Em ▶ Testar, toque para começar, pule algumas caixas e perca de propósito. Mude a mensagem de game over, '
    'mostre a pontuação também na tela de fim e faça a velocidade das caixas aumentar a cada ponto.',
    r'''
import 'dart:math';
import 'package:flutter/material.dart';
import 'package:flutter/scheduler.dart';

void main() => runApp(const MaterialApp(home: Jogo()));

const double largura = 360;
const double altura = 520;
const double chao = 440;
const double gravidade = 1500;
const double impulso = -620;
const double jogadorX = 60;

enum Estado { pronto, jogando, fim }

class Caixa {
  double x;
  final double altura;
  bool contada = false;
  Caixa(this.x, this.altura);

  Rect get area => Rect.fromLTWH(x, chao - altura, 30, altura);
}

class Cena extends CustomPainter {
  final double y;
  final List<Caixa> caixas;
  Cena(this.y, this.caixas);

  @override
  void paint(Canvas canvas, Size size) {
    canvas.drawRect(Rect.fromLTWH(0, 0, size.width, size.height), Paint()..color = const Color(0xFF7EC8F2));
    canvas.drawRect(Rect.fromLTWH(0, chao, size.width, size.height - chao), Paint()..color = Colors.green.shade700);
    for (final c in caixas) {
      canvas.drawRect(c.area, Paint()..color = Colors.brown);
    }
    final corpo = Rect.fromLTWH(jogadorX, y, 40, 48);
    canvas.drawRRect(RRect.fromRectAndRadius(corpo, const Radius.circular(8)), Paint()..color = Colors.deepOrange);
  }

  @override
  bool shouldRepaint(covariant Cena antiga) => true;
}

class Jogo extends StatefulWidget {
  const Jogo({super.key});

  @override
  State<Jogo> createState() => _JogoState();
}

class _JogoState extends State<Jogo> with SingleTickerProviderStateMixin {
  late Ticker ticker;
  double ultimo = 0;
  final sorteio = Random();
  Estado estado = Estado.pronto;
  double y = chao - 48;
  double vy = 0;
  List<Caixa> caixas = [];
  double tempoProxima = 1;
  int pontos = 0;

  @override
  void initState() {
    super.initState();
    ticker = createTicker(quadro);
    ticker.start();
  }

  void quadro(Duration tempo) {
    final agora = tempo.inMicroseconds / 1000000;
    final dt = agora - ultimo;
    ultimo = agora;
    if (estado != Estado.jogando) return;
    setState(() => atualizar(dt));
  }

  void atualizar(double dt) {
    vy += gravidade * dt;
    y += vy * dt;
    if (y > chao - 48) {
      y = chao - 48;
      vy = 0;
    }

    tempoProxima -= dt;
    if (tempoProxima <= 0) {
      caixas.add(Caixa(largura, 30 + sorteio.nextDouble() * 40));
      tempoProxima = 1 + sorteio.nextDouble() * 1.2;
    }
    for (final c in caixas) {
      c.x -= 200 * dt;
      if (!c.contada && c.x + 30 < jogadorX) {
        c.contada = true;
        pontos++;
      }
    }
    caixas.removeWhere((c) => c.x < -30);

    final jogador = Rect.fromLTWH(jogadorX, y, 40, 48).deflate(4);
    if (caixas.any((c) => c.area.overlaps(jogador))) {
      estado = Estado.fim;
    }
  }

  void tocar() {
    setState(() {
      if (estado == Estado.pronto) {
        estado = Estado.jogando;
      } else if (estado == Estado.jogando) {
        if (y >= chao - 48) vy = impulso;
      } else {
        caixas.clear();
        pontos = 0;
        y = chao - 48;
        vy = 0;
        tempoProxima = 1;
        estado = Estado.pronto;
      }
    });
  }

  @override
  void dispose() {
    ticker.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    const grande = TextStyle(color: Colors.white, fontSize: 28, fontWeight: FontWeight.bold);
    return Scaffold(
      backgroundColor: Colors.black,
      body: Center(
        child: GestureDetector(
          onTapDown: (_) => tocar(),
          child: SizedBox(
            width: largura,
            height: altura,
            child: Stack(
              children: [
                CustomPaint(size: const Size(largura, altura), painter: Cena(y, caixas)),
                Positioned(
                  top: 16,
                  left: 16,
                  child: Text('Pontos: $pontos', style: const TextStyle(color: Colors.white, fontSize: 20)),
                ),
                if (estado == Estado.pronto)
                  const Center(child: Text('Toque para começar', style: grande)),
                if (estado == Estado.fim)
                  const Center(child: Text('Fim de jogo!\nToque para voltar', textAlign: TextAlign.center, style: grande)),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
''',
    [
        ['Nova mensagem de game over', 'Troque o texto Fim de jogo! por outra frase.', r'^(?![\s\S]*Fim de jogo!)'],
        ['Pontuação na tela de fim', "Tire o const do Center do fim e use interpolação: Text('Você fez $pontos pontos').", r"estado\s*==\s*Estado\.fim\)[\s\S]{0,200}\$pontos"],
        ['Velocidade que cresce', 'Troque o 200 fixo por uma conta com os pontos, como 200 + pontos * 15.', r'c\.x\s*-=\s*\(\s*200\s*\+\s*pontos\s*\*'],
    ],
)

aula(
    'Projeto · Pula-Caixa',
    'Agora é juntar tudo num jogo de verdade, no estilo corredor infinito. Tudo o que você viu está aqui: o laço '
    'com Ticker e dt, o desenho no CustomPainter, o toque, a gravidade, a lista de caixas com sorteio, a colisão '
    'AABB e os estados com HUD. O que é novo: a velocidade cresce com o tempo de partida (o jogo fica mais '
    'difícil sozinho), o recorde guarda a melhor pontuação da sessão e o cenário tem duas camadas que andam em '
    'velocidades diferentes, o paralaxe. As nuvens, longe, andam a 20% da velocidade; as listras do chão, perto, '
    'andam junto com as caixas. O operador % (resto da divisão) faz o desenho se repetir sem fim. A distância '
    'percorrida vira a pontuação, em metros.',
    'Em ▶ Testar, jogue algumas partidas e tente bater o recorde. Depois mude o jogo: troque as cores para um '
    'cenário noturno, deixe a aceleração mais forte e acrescente uma moeda que vale 10 metros.',
    r'''
import 'dart:math';
import 'package:flutter/material.dart';
import 'package:flutter/scheduler.dart';

void main() => runApp(const MaterialApp(home: PulaCaixa()));

const double largura = 360;
const double altura = 520;
const double chao = 440;
const double gravidade = 1700;
const double impulso = -680;
const double jogadorX = 60;

enum Estado { pronto, jogando, fim }

class Caixa {
  double x;
  final double largura;
  final double altura;
  Caixa(this.x, this.largura, this.altura);

  Rect get area => Rect.fromLTWH(x, chao - altura, largura, altura);
}

class Cena extends CustomPainter {
  final double y;
  final List<Caixa> caixas;
  final double deslocamento;
  final bool perdeu;
  Cena(this.y, this.caixas, this.deslocamento, this.perdeu);

  @override
  void paint(Canvas canvas, Size size) {
    canvas.drawRect(Rect.fromLTWH(0, 0, size.width, size.height), Paint()..color = const Color(0xFF8FD3FE));

    final nuvem = Paint()..color = Colors.white;
    for (int i = 0; i < 3; i++) {
      final x = (i * 160 - deslocamento * 0.2) % (largura + 120) - 60;
      final alto = 70.0 + i * 45;
      canvas.drawCircle(Offset(x, alto), 18, nuvem);
      canvas.drawCircle(Offset(x + 20, alto - 8), 22, nuvem);
      canvas.drawCircle(Offset(x + 42, alto), 16, nuvem);
    }

    canvas.drawRect(Rect.fromLTWH(0, chao, size.width, size.height - chao), Paint()..color = Colors.green.shade700);
    final listra = Paint()..color = Colors.green.shade900;
    for (int i = 0; i < 10; i++) {
      final x = (i * 40 - deslocamento) % (largura + 40) - 40;
      canvas.drawRect(Rect.fromLTWH(x, chao + 14, 20, 6), listra);
    }

    for (final c in caixas) {
      canvas.drawRRect(RRect.fromRectAndRadius(c.area, const Radius.circular(4)), Paint()..color = Colors.brown);
      canvas.drawRect(c.area.deflate(6), Paint()..color = Colors.brown.shade300);
    }

    final corpo = Rect.fromLTWH(jogadorX, y, 40, 48);
    canvas.drawRRect(
      RRect.fromRectAndRadius(corpo, const Radius.circular(8)),
      Paint()..color = perdeu ? Colors.red : Colors.deepOrange,
    );
    canvas.drawCircle(Offset(jogadorX + 28, y + 14), 6, Paint()..color = Colors.white);
    canvas.drawCircle(Offset(jogadorX + 30, y + 14), 3, Paint()..color = Colors.black);
  }

  @override
  bool shouldRepaint(covariant Cena antiga) => true;
}

class PulaCaixa extends StatefulWidget {
  const PulaCaixa({super.key});

  @override
  State<PulaCaixa> createState() => _PulaCaixaState();
}

class _PulaCaixaState extends State<PulaCaixa> with SingleTickerProviderStateMixin {
  late Ticker ticker;
  double ultimo = 0;
  final sorteio = Random();
  Estado estado = Estado.pronto;
  double y = chao - 48;
  double vy = 0;
  List<Caixa> caixas = [];
  double tempoProxima = 1;
  double tempoDePartida = 0;
  double deslocamento = 0;
  int recorde = 0;

  double get velocidade => 220 + tempoDePartida * 8;
  int get metros => (deslocamento / 20).floor();

  @override
  void initState() {
    super.initState();
    ticker = createTicker(quadro);
    ticker.start();
  }

  void quadro(Duration tempo) {
    final agora = tempo.inMicroseconds / 1000000;
    final dt = agora - ultimo;
    ultimo = agora;
    if (estado != Estado.jogando) return;
    setState(() => atualizar(dt));
  }

  void atualizar(double dt) {
    tempoDePartida += dt;
    deslocamento += velocidade * dt;

    vy += gravidade * dt;
    y += vy * dt;
    if (y > chao - 48) {
      y = chao - 48;
      vy = 0;
    }

    tempoProxima -= dt;
    if (tempoProxima <= 0) {
      caixas.add(Caixa(largura, 24 + sorteio.nextDouble() * 24, 30 + sorteio.nextDouble() * 40));
      tempoProxima = 0.9 + sorteio.nextDouble() * 1.1;
    }
    for (final c in caixas) {
      c.x -= velocidade * dt;
    }
    caixas.removeWhere((c) => c.x < -60);

    final jogador = Rect.fromLTWH(jogadorX, y, 40, 48).deflate(4);
    if (caixas.any((c) => c.area.overlaps(jogador))) {
      estado = Estado.fim;
      if (metros > recorde) recorde = metros;
    }
  }

  void tocar() {
    setState(() {
      if (estado == Estado.pronto) {
        estado = Estado.jogando;
      } else if (estado == Estado.jogando) {
        if (y >= chao - 48) vy = impulso;
      } else {
        caixas.clear();
        y = chao - 48;
        vy = 0;
        tempoProxima = 1;
        tempoDePartida = 0;
        deslocamento = 0;
        estado = Estado.pronto;
      }
    });
  }

  @override
  void dispose() {
    ticker.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    const grande = TextStyle(color: Colors.white, fontSize: 28, fontWeight: FontWeight.bold);
    const hud = TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.w600);
    return Scaffold(
      backgroundColor: Colors.black,
      body: Center(
        child: GestureDetector(
          onTapDown: (_) => tocar(),
          child: SizedBox(
            width: largura,
            height: altura,
            child: Stack(
              children: [
                CustomPaint(
                  size: const Size(largura, altura),
                  painter: Cena(y, caixas, deslocamento, estado == Estado.fim),
                ),
                Positioned(top: 16, left: 16, child: Text('$metros m', style: hud)),
                Positioned(top: 16, right: 16, child: Text('Recorde: $recorde m', style: hud)),
                if (estado == Estado.pronto)
                  const Center(child: Text('Pula-Caixa\nToque para começar', textAlign: TextAlign.center, style: grande)),
                if (estado == Estado.fim)
                  Center(
                    child: Text('Fim! $metros m\nToque para jogar de novo', textAlign: TextAlign.center, style: grande),
                  ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
''',
    [
        ['Cenário noturno', 'Troque a cor do céu (0xFF8FD3FE) por um azul escuro, como Color(0xFF14213D).', r'^(?![\s\S]*0xFF8FD3FE)'],
        ['Aceleração mais forte', 'No getter velocidade, troque tempoDePartida * 8 por * 15.', r'tempoDePartida\s*\*\s*15\b'],
        ['Uma moeda que vale 10 metros', 'Crie uma classe Moeda com x e y, uma lista moedas, desenhe com drawCircle amarelo e some 10 * 20 ao deslocamento quando o jogador encostar.', r'class\s+Moeda\b[\s\S]*Colors\.(?:yellow|amber)'],
    ],
)

# ---------------------------------------------------------------- Parte 2
aula(
    'Arrastar: a raquete segue o dedo',
    'Tocar serve para ações (pular, atirar). Para controlar uma posição de forma contínua, o gesto certo é '
    'arrastar. O GestureDetector chama onPanUpdate várias vezes enquanto o dedo desliza, e DragUpdateDetails '
    'traz details.delta: quanto o dedo andou desde a última chamada. Somar o delta.dx ao x da raquete faz ela '
    'acompanhar o dedo, de onde quer que o arrasto comece. Os dois if logo depois seguram a raquete dentro da '
    'tela. A bola usa um Offset para a posição e outro para a velocidade: bola += velocidade * dt anda nos dois '
    'eixos de uma vez. Quando bate numa parede, só o sinal do eixo daquela parede muda. Na raquete, a bola só '
    'rebate se estiver descendo (velocidade.dy > 0), senão ela poderia ficar presa vibrando dentro dela.',
    'Em ▶ Testar, arraste em qualquer lugar da área do jogo para mover a raquete e rebata a bola. Diminua a '
    'raquete para 50, acelere a bola e faça a bola ir um pouco mais rápido a cada rebatida.',
    r'''
import 'package:flutter/material.dart';
import 'package:flutter/scheduler.dart';

void main() => runApp(const MaterialApp(home: Jogo()));

const double largura = 360;
const double altura = 520;
const double raqueteY = 470;
const double raqueteLargura = 80;
const double raio = 8;

class Cena extends CustomPainter {
  final double raqueteX;
  final Offset bola;
  Cena(this.raqueteX, this.bola);

  @override
  void paint(Canvas canvas, Size size) {
    canvas.drawRect(Rect.fromLTWH(0, 0, size.width, size.height), Paint()..color = const Color(0xFF14213D));
    canvas.drawCircle(bola, raio, Paint()..color = Colors.white);
    final raquete = Rect.fromLTWH(raqueteX, raqueteY, raqueteLargura, 12);
    canvas.drawRRect(RRect.fromRectAndRadius(raquete, const Radius.circular(6)), Paint()..color = Colors.cyanAccent);
  }

  @override
  bool shouldRepaint(covariant Cena antiga) => true;
}

class Jogo extends StatefulWidget {
  const Jogo({super.key});

  @override
  State<Jogo> createState() => _JogoState();
}

class _JogoState extends State<Jogo> with SingleTickerProviderStateMixin {
  late Ticker ticker;
  double ultimo = 0;
  double raqueteX = 140;
  Offset bola = const Offset(180, 120);
  Offset velocidade = const Offset(160, 240);
  int rebatidas = 0;
  int perdidas = 0;

  @override
  void initState() {
    super.initState();
    ticker = createTicker(quadro);
    ticker.start();
  }

  void quadro(Duration tempo) {
    final agora = tempo.inMicroseconds / 1000000;
    final dt = agora - ultimo;
    ultimo = agora;
    setState(() => atualizar(dt));
  }

  void atualizar(double dt) {
    bola += velocidade * dt;

    if (bola.dx < raio) {
      bola = Offset(raio, bola.dy);
      velocidade = Offset(velocidade.dx.abs(), velocidade.dy);
    }
    if (bola.dx > largura - raio) {
      bola = Offset(largura - raio, bola.dy);
      velocidade = Offset(-velocidade.dx.abs(), velocidade.dy);
    }
    if (bola.dy < raio) {
      bola = Offset(bola.dx, raio);
      velocidade = Offset(velocidade.dx, velocidade.dy.abs());
    }

    final raquete = Rect.fromLTWH(raqueteX, raqueteY, raqueteLargura, 12);
    if (velocidade.dy > 0 && raquete.contains(bola + const Offset(0, raio))) {
      velocidade = Offset(velocidade.dx, -velocidade.dy);
      rebatidas++;
    }

    if (bola.dy > altura + raio) {
      perdidas++;
      bola = const Offset(180, 120);
      velocidade = const Offset(160, 240);
    }
  }

  void arrastar(DragUpdateDetails details) {
    raqueteX += details.delta.dx;
    if (raqueteX < 0) raqueteX = 0;
    if (raqueteX > largura - raqueteLargura) raqueteX = largura - raqueteLargura;
  }

  @override
  void dispose() {
    ticker.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(title: Text('Rebatidas: $rebatidas · Perdidas: $perdidas')),
      body: Center(
        child: GestureDetector(
          onPanUpdate: arrastar,
          child: CustomPaint(
            size: const Size(largura, altura),
            painter: Cena(raqueteX, bola),
          ),
        ),
      ),
    );
  }
}
''',
    [
        ['Raquete menor (50)', 'Troque const double raqueteLargura = 80 por 50.', r'const double raqueteLargura\s*=\s*50\b'],
        ['Bola mais rápida', 'Aumente os dois números da velocidade inicial, por exemplo Offset(220, 320), nos dois lugares em que ela aparece.', r'velocidade\s*=\s*const\s+Offset\(\s*(?:2[2-9]\d|[3-9]\d\d)'],
        ['Acelerar a cada rebatida', 'Logo depois de rebatidas++, multiplique a velocidade: velocidade = velocidade * 1.05.', r'velocidade\s*=\s*velocidade\s*\*\s*1\.\d+'],
    ],
    lim='O arrasto funciona com mouse e com o dedo. O simulador não junta dois dedos ao mesmo tempo (multitoque).',
)

aula(
    'Arremessar: a velocidade do arrasto',
    'O fim do arrasto também traz informação. onPanStart avisa que o dedo começou a arrastar, onPanUpdate dá a '
    'posição a cada movimento (details.localPosition) e onPanEnd traz details.velocity.pixelsPerSecond: a '
    'velocidade do dedo no instante em que ele soltou, em pixels por segundo. Aqui o disco só pode ser pego se o '
    'arrasto começar em cima dele (a distância até o centro menor que o raio). Enquanto está preso, o disco '
    'segue o dedo e o laço não o move. Ao soltar, a velocidade do dedo vira a velocidade do disco. O atrito usa '
    'pow(0.4, dt): a cada segundo sobram 40% da velocidade, e o resultado é o mesmo com qualquer taxa de '
    'quadros, porque a potência junta os pedaços de tempo do jeito certo.',
    'Em ▶ Testar, pegue o disco e arremesse contra as paredes. Troque 0.4 por 0.9 (mesa de gelo) e por 0.05 '
    '(areia). Depois conte quantas vezes o disco bate nas paredes.',
    r'''
import 'dart:math';
import 'package:flutter/material.dart';
import 'package:flutter/scheduler.dart';

void main() => runApp(const MaterialApp(home: Jogo()));

const double largura = 360;
const double altura = 520;
const double raio = 26;

class Cena extends CustomPainter {
  final Offset disco;
  final bool preso;
  Cena(this.disco, this.preso);

  @override
  void paint(Canvas canvas, Size size) {
    canvas.drawRect(Rect.fromLTWH(0, 0, size.width, size.height), Paint()..color = const Color(0xFF1B4332));
    final linha = Paint()
      ..color = Colors.white24
      ..style = PaintingStyle.stroke
      ..strokeWidth = 3;
    canvas.drawLine(Offset(0, size.height / 2), Offset(size.width, size.height / 2), linha);
    canvas.drawCircle(Offset(size.width / 2, size.height / 2), 50, linha);
    canvas.drawCircle(disco, raio, Paint()..color = preso ? Colors.orangeAccent : Colors.redAccent);
    canvas.drawCircle(disco, raio - 8, Paint()..color = Colors.black26);
  }

  @override
  bool shouldRepaint(covariant Cena antiga) => true;
}

class Jogo extends StatefulWidget {
  const Jogo({super.key});

  @override
  State<Jogo> createState() => _JogoState();
}

class _JogoState extends State<Jogo> with SingleTickerProviderStateMixin {
  late Ticker ticker;
  double ultimo = 0;
  Offset disco = const Offset(180, 380);
  Offset velocidade = Offset.zero;
  bool preso = false;

  @override
  void initState() {
    super.initState();
    ticker = createTicker(quadro);
    ticker.start();
  }

  void quadro(Duration tempo) {
    final agora = tempo.inMicroseconds / 1000000;
    final dt = agora - ultimo;
    ultimo = agora;
    if (preso) return;
    setState(() {
      disco += velocidade * dt;
      velocidade = velocidade * pow(0.4, dt).toDouble();
      if (disco.dx < raio || disco.dx > largura - raio) {
        velocidade = Offset(-velocidade.dx, velocidade.dy);
        disco = Offset(disco.dx < raio ? raio : largura - raio, disco.dy);
      }
      if (disco.dy < raio || disco.dy > altura - raio) {
        velocidade = Offset(velocidade.dx, -velocidade.dy);
        disco = Offset(disco.dx, disco.dy < raio ? raio : altura - raio);
      }
    });
  }

  void comecar(DragStartDetails details) {
    if ((details.localPosition - disco).distance <= raio) {
      setState(() {
        preso = true;
        velocidade = Offset.zero;
      });
    }
  }

  void mover(DragUpdateDetails details) {
    if (preso) setState(() => disco = details.localPosition);
  }

  void soltar(DragEndDetails details) {
    if (preso) {
      setState(() {
        preso = false;
        velocidade = details.velocity.pixelsPerSecond;
      });
    }
  }

  @override
  void dispose() {
    ticker.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(title: Text('${velocidade.distance.toStringAsFixed(0)} px/s')),
      body: Center(
        child: GestureDetector(
          onPanStart: comecar,
          onPanUpdate: mover,
          onPanEnd: soltar,
          child: CustomPaint(
            size: const Size(largura, altura),
            painter: Cena(disco, preso),
          ),
        ),
      ),
    );
  }
}
''',
    [
        ['Mesa de gelo (0.9)', 'No atrito, troque pow(0.4, dt) por pow(0.9, dt).', r'pow\(\s*0\.9\s*,\s*dt\s*\)'],
        ['Disco menor (raio 18)', 'Troque const double raio = 26 por 18.', r'const double raio\s*=\s*18\b'],
        ['Contar as batidas nas paredes', 'Crie int batidas = 0, some 1 dentro dos dois if das paredes e mostre no título da AppBar.', r'batidas\s*(?:\+\+|\+=\s*1)[\s\S]*batidas\s*(?:\+\+|\+=\s*1)[\s\S]*\$batidas'],
    ],
)

aula(
    'Teclado: setas e espaço',
    'No computador e no Flutter Web, o jogador espera usar o teclado. Há dois jeitos de ler teclas, e jogos '
    'usam os dois. Para ações de um toque só, como pular, o widget Focus com autofocus: true recebe cada tecla '
    'em onKeyEvent: event is KeyDownEvent diz que a tecla acabou de descer, e event.logicalKey diz qual foi '
    '(LogicalKeyboardKey.space). A função devolve KeyEventResult.handled quando usou a tecla. Para movimento '
    'contínuo, enquanto a tecla está apertada, o laço pergunta a cada quadro: '
    'HardwareKeyboard.instance.isLogicalKeyPressed(LogicalKeyboardKey.arrowLeft). Assim o personagem anda '
    'macio, sem depender da repetição automática do teclado. Tudo isso vem de package:flutter/services.dart.',
    'Em ▶ Testar, clique uma vez no celular e use ← → para andar e espaço para pular. Acrescente as teclas A e D '
    'como alternativa às setas e faça a seta para cima também pular.',
    r'''
import 'package:flutter/material.dart';
import 'package:flutter/scheduler.dart';
import 'package:flutter/services.dart';

void main() => runApp(const MaterialApp(home: Jogo()));

const double largura = 360;
const double altura = 520;
const double chao = 440;
const double gravidade = 1500;
const double impulso = -620;

class Cena extends CustomPainter {
  final double x;
  final double y;
  Cena(this.x, this.y);

  @override
  void paint(Canvas canvas, Size size) {
    canvas.drawRect(Rect.fromLTWH(0, 0, size.width, size.height), Paint()..color = const Color(0xFF7EC8F2));
    canvas.drawRect(Rect.fromLTWH(0, chao, size.width, size.height - chao), Paint()..color = Colors.green.shade700);
    final corpo = Rect.fromLTWH(x, y, 40, 48);
    canvas.drawRRect(RRect.fromRectAndRadius(corpo, const Radius.circular(8)), Paint()..color = Colors.deepOrange);
  }

  @override
  bool shouldRepaint(covariant Cena antiga) => true;
}

class Jogo extends StatefulWidget {
  const Jogo({super.key});

  @override
  State<Jogo> createState() => _JogoState();
}

class _JogoState extends State<Jogo> with SingleTickerProviderStateMixin {
  late Ticker ticker;
  double ultimo = 0;
  double x = 160;
  double y = chao - 48;
  double vy = 0;
  double velocidade = 220;
  String ultimaTecla = 'nenhuma';

  @override
  void initState() {
    super.initState();
    ticker = createTicker(quadro);
    ticker.start();
  }

  void quadro(Duration tempo) {
    final agora = tempo.inMicroseconds / 1000000;
    final dt = agora - ultimo;
    ultimo = agora;
    final teclado = HardwareKeyboard.instance;
    setState(() {
      if (teclado.isLogicalKeyPressed(LogicalKeyboardKey.arrowLeft)) x -= velocidade * dt;
      if (teclado.isLogicalKeyPressed(LogicalKeyboardKey.arrowRight)) x += velocidade * dt;
      if (x < 0) x = 0;
      if (x > largura - 40) x = largura - 40;

      vy += gravidade * dt;
      y += vy * dt;
      if (y > chao - 48) {
        y = chao - 48;
        vy = 0;
      }
    });
  }

  KeyEventResult tecla(FocusNode node, KeyEvent event) {
    if (event is KeyDownEvent) {
      ultimaTecla = event.logicalKey == LogicalKeyboardKey.space ? 'espaço' : 'outra';
      if (event.logicalKey == LogicalKeyboardKey.space && y >= chao - 48) {
        vy = impulso;
      }
      return KeyEventResult.handled;
    }
    return KeyEventResult.ignored;
  }

  @override
  void dispose() {
    ticker.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(title: Text('← → andar · espaço pular · $ultimaTecla')),
      body: Center(
        child: Focus(
          autofocus: true,
          onKeyEvent: tecla,
          child: CustomPaint(
            size: const Size(largura, altura),
            painter: Cena(x, y),
          ),
        ),
      ),
    );
  }
}
''',
    [
        ['Andar com A e D', 'Nos dois if de movimento, acrescente || teclado.isLogicalKeyPressed(LogicalKeyboardKey.keyA) e o mesmo com keyD.', r'LogicalKeyboardKey\.keyA[\s\S]*LogicalKeyboardKey\.keyD|LogicalKeyboardKey\.keyD[\s\S]*LogicalKeyboardKey\.keyA'],
        ['Seta para cima também pula', 'Na condição do pulo, aceite LogicalKeyboardKey.arrowUp além do espaço.', r'LogicalKeyboardKey\.arrowUp'],
        ['Correr segurando Shift', 'No quadro, use uma velocidade maior quando teclado.isShiftPressed for verdadeiro.', r'isShiftPressed'],
    ],
    lim='Clique no celular antes de usar as teclas: com o cursor no editor de código, as teclas vão para o código. No celular de verdade não há teclado físico, então jogos para celular também precisam de controles por toque.',
)

PARTS = [
    ['O laço do jogo com Timer.periodic', 'Parte 1 · Fundamentos de jogos 2D'],
    ['Projeto · Pula-Caixa', 'Projeto 1 · Pula-Caixa'],
    ['Arrastar: a raquete segue o dedo', 'Parte 2 · Entrada: arrastar e teclado'],
]


# ---------------------------------------------------------------- Parte 3
SETUP_SPRITES = (
    'pubspec.yaml (dentro de flutter:):\n'
    '  assets:\n'
    '    - assets/sprites/\n\n'
    'Coloque os arquivos PNG em assets/sprites/ na raiz do projeto. O simulador já tem estes sprites prontos, '
    'desenhados para a Oficina: heroi.png (4 quadros de 16×16), moeda.png (6), slime.png (2), nave.png (2), '
    'explosao.png (5), tiro.png (8×8), caixa.png, coracao.png, maca.png, grama.png (16×16) e nuvem.png (32×16). '
    'Os arquivos estão na pasta tools/sprites do repositório da Oficina Flutter 2.'
)

aula(
    'Sprites: imagens no Canvas',
    'Sprite é uma imagem pequena que representa um personagem ou objeto do jogo. Em Flutter, para desenhar uma '
    'imagem no Canvas ela precisa virar um ui.Image (do pacote dart:ui): rootBundle.load lê os bytes do arquivo '
    'de assets e decodeImageFromList transforma os bytes em imagem. Como ler arquivo leva tempo, a função é '
    'async e o State começa sem imagens: o body mostra um CircularProgressIndicator até tudo carregar, e o '
    'setState troca pela cena. Com a imagem pronta, canvas.drawImage desenha ela inteira no tamanho original, e '
    'canvas.drawImageRect(imagem, origem, destino, paint) recorta um pedaço (origem) e estica para outro '
    'retângulo (destino). É assim que um sprite de 16×16 vira 64×64 na tela. O Paint padrão usa '
    'FilterQuality.none, que amplia sem borrar: o pixel art continua nítido. O herói pequeno lá em cima é a '
    'folha inteira, com os quatro quadros lado a lado.',
    'Em ▶ Testar, compare a folha pequena com o herói ampliado. Troque o quadro do herói (o x da origem vai de 0 '
    'a 48, de 16 em 16), aumente a caixa para 64×64 e desenhe uma maçã em cima dela.',
    r'''
import 'dart:ui' as ui;
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

void main() => runApp(const MaterialApp(home: Vitrine()));

const double largura = 360;
const double altura = 520;
const double chao = 440;

Future<ui.Image> carregarImagem(String caminho) async {
  final dados = await rootBundle.load(caminho);
  return decodeImageFromList(dados.buffer.asUint8List());
}

class Sprites {
  final ui.Image heroi;
  final ui.Image grama;
  final ui.Image caixa;
  final ui.Image moeda;
  Sprites(this.heroi, this.grama, this.caixa, this.moeda);
}

class Cena extends CustomPainter {
  final Sprites s;
  Cena(this.s);

  @override
  void paint(Canvas canvas, Size size) {
    canvas.drawRect(Rect.fromLTWH(0, 0, size.width, size.height), Paint()..color = const Color(0xFF7EC8F2));
    canvas.drawRect(Rect.fromLTWH(0, chao + 32, size.width, size.height - chao - 32), Paint()..color = const Color(0xFF8B5A2B));

    final tinta = Paint();
    const bloco = Rect.fromLTWH(0, 0, 16, 16);
    for (int i = 0; i < 12; i++) {
      canvas.drawImageRect(s.grama, bloco, Rect.fromLTWH(i * 32.0, chao, 32, 32), tinta);
    }
    canvas.drawImageRect(s.caixa, bloco, const Rect.fromLTWH(240, chao - 48, 48, 48), tinta);
    canvas.drawImageRect(s.moeda, bloco, const Rect.fromLTWH(252, chao - 96, 24, 24), tinta);
    canvas.drawImageRect(s.heroi, bloco, const Rect.fromLTWH(80, chao - 64, 64, 64), tinta);

    canvas.drawImage(s.heroi, const Offset(16, 16), tinta);
  }

  @override
  bool shouldRepaint(covariant Cena antiga) => antiga.s != s;
}

class Vitrine extends StatefulWidget {
  const Vitrine({super.key});

  @override
  State<Vitrine> createState() => _VitrineState();
}

class _VitrineState extends State<Vitrine> {
  Sprites? sprites;

  @override
  void initState() {
    super.initState();
    carregar();
  }

  Future<void> carregar() async {
    final heroi = await carregarImagem('assets/sprites/heroi.png');
    final grama = await carregarImagem('assets/sprites/grama.png');
    final caixa = await carregarImagem('assets/sprites/caixa.png');
    final moeda = await carregarImagem('assets/sprites/moeda.png');
    setState(() => sprites = Sprites(heroi, grama, caixa, moeda));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: sprites == null
          ? const Center(child: CircularProgressIndicator())
          : Center(
              child: CustomPaint(
                size: const Size(largura, altura),
                painter: Cena(sprites!),
              ),
            ),
    );
  }
}
''',
    [
        ['Outro quadro do herói', 'No drawImageRect do herói ampliado, troque a origem bloco por Rect.fromLTWH(32, 0, 16, 16).', r'drawImageRect\(\s*s\.heroi\s*,\s*(?:const\s+)?Rect\.fromLTWH\(\s*(?:16|32|48)\b'],
        ['Caixa de 64×64', 'No destino da caixa, use largura e altura 64 (e suba o top para chao - 64).', r'drawImageRect\(\s*s\.caixa[^;]*Rect\.fromLTWH\([^;]*,\s*64\s*,\s*64\s*\)'],
        ['Uma maçã em cima da caixa', "Carregue 'assets/sprites/maca.png' como as outras (um campo novo em Sprites) e desenhe acima da caixa.", r"assets/sprites/maca\.png[\s\S]*drawImageRect\(\s*s\.maca"],
    ],
    lim='O simulador desenha a tela a partir do primeiro return do build. Para mostrar algo enquanto carrega, use um if/? dentro do Scaffold (como aqui), não dois return. No simulador, rootBundle só lê os sprites e sons prontos.',
    setup=SETUP_SPRITES,
)

aula(
    'Animação com folha de sprites',
    'Uma folha de sprites (sprite sheet) guarda os quadros de uma animação lado a lado, todos do mesmo tamanho. '
    'Animar é escolher qual pedaço recortar em cada momento: o quadro i começa em x = i * 16. O tempo decide o '
    'quadro: (tempo * 10).floor() % 4 troca de quadro 10 vezes por segundo e volta ao primeiro depois do quarto. '
    'O herói só conta o tempo de caminhada enquanto anda; parado, ele mostra o quadro 0. A moeda tem o seu '
    'próprio relógio (12 quadros por segundo, 6 quadros), porque cada animação tem o seu ritmo. Para virar o '
    'herói para a esquerda não é preciso outra imagem: canvas.save, translate até o centro do sprite, scale(-1, 1) '
    'espelha tudo o que vier depois, e canvas.restore desfaz a transformação para o resto da cena.',
    'Em ▶ Testar, toque em pontos à esquerda e à direita e veja o herói andar e virar. Mude a velocidade da '
    'animação de 10 para 4 e para 20 quadros por segundo. Depois faça a moeda girar mais devagar.',
    r'''
import 'dart:ui' as ui;
import 'package:flutter/material.dart';
import 'package:flutter/scheduler.dart';
import 'package:flutter/services.dart';

void main() => runApp(const MaterialApp(home: Jogo()));

const double largura = 360;
const double altura = 520;
const double chao = 440;

Future<ui.Image> carregarImagem(String caminho) async {
  final dados = await rootBundle.load(caminho);
  return decodeImageFromList(dados.buffer.asUint8List());
}

class Cena extends CustomPainter {
  final ui.Image heroi;
  final ui.Image moeda;
  final ui.Image grama;
  final double x;
  final double direcao;
  final int quadroHeroi;
  final int quadroMoeda;
  Cena(this.heroi, this.moeda, this.grama, this.x, this.direcao, this.quadroHeroi, this.quadroMoeda);

  @override
  void paint(Canvas canvas, Size size) {
    canvas.drawRect(Rect.fromLTWH(0, 0, size.width, size.height), Paint()..color = const Color(0xFF7EC8F2));
    canvas.drawRect(Rect.fromLTWH(0, chao + 32, size.width, size.height - chao - 32), Paint()..color = const Color(0xFF8B5A2B));
    final tinta = Paint();
    for (int i = 0; i < 12; i++) {
      canvas.drawImageRect(grama, const Rect.fromLTWH(0, 0, 16, 16), Rect.fromLTWH(i * 32.0, chao, 32, 32), tinta);
    }

    final origemMoeda = Rect.fromLTWH(quadroMoeda * 16.0, 0, 16, 16);
    canvas.drawImageRect(moeda, origemMoeda, const Rect.fromLTWH(300, 24, 40, 40), tinta);

    final origemHeroi = Rect.fromLTWH(quadroHeroi * 16.0, 0, 16, 16);
    canvas.save();
    canvas.translate(x + 32, chao - 64);
    canvas.scale(direcao, 1);
    canvas.drawImageRect(heroi, origemHeroi, const Rect.fromLTWH(-32, 0, 64, 64), tinta);
    canvas.restore();
  }

  @override
  bool shouldRepaint(covariant Cena antiga) => true;
}

class Jogo extends StatefulWidget {
  const Jogo({super.key});

  @override
  State<Jogo> createState() => _JogoState();
}

class _JogoState extends State<Jogo> with SingleTickerProviderStateMixin {
  late Ticker ticker;
  double ultimo = 0;
  ui.Image? heroi;
  ui.Image? moeda;
  ui.Image? grama;
  double x = 148;
  double alvo = 148;
  double direcao = 1;
  bool andando = false;
  double tempoAndando = 0;
  double tempoTotal = 0;

  @override
  void initState() {
    super.initState();
    carregar();
    ticker = createTicker(quadro);
    ticker.start();
  }

  Future<void> carregar() async {
    final h = await carregarImagem('assets/sprites/heroi.png');
    final m = await carregarImagem('assets/sprites/moeda.png');
    final g = await carregarImagem('assets/sprites/grama.png');
    setState(() {
      heroi = h;
      moeda = m;
      grama = g;
    });
  }

  void quadro(Duration tempo) {
    final agora = tempo.inMicroseconds / 1000000;
    final dt = agora - ultimo;
    ultimo = agora;
    setState(() {
      tempoTotal += dt;
      final distancia = alvo - x;
      final passo = 150 * dt;
      andando = distancia.abs() > passo;
      if (andando) {
        direcao = distancia > 0 ? 1.0 : -1.0;
        x += passo * direcao;
        tempoAndando += dt;
      } else {
        x = alvo;
        tempoAndando = 0;
      }
    });
  }

  void tocar(TapDownDetails details) {
    var novo = details.localPosition.dx - 32;
    if (novo < 0) novo = 0;
    if (novo > largura - 64) novo = largura - 64;
    alvo = novo;
  }

  @override
  void dispose() {
    ticker.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final quadroHeroi = andando ? (tempoAndando * 10).floor() % 4 : 0;
    final quadroMoeda = (tempoTotal * 12).floor() % 6;
    return Scaffold(
      backgroundColor: Colors.black,
      body: heroi == null || moeda == null || grama == null
          ? const Center(child: CircularProgressIndicator())
          : Center(
              child: GestureDetector(
                onTapDown: tocar,
                child: CustomPaint(
                  size: const Size(largura, altura),
                  painter: Cena(heroi!, moeda!, grama!, x, direcao, quadroHeroi, quadroMoeda),
                ),
              ),
            ),
    );
  }
}
''',
    [
        ['Animação a 4 quadros por segundo', 'No build, troque (tempoAndando * 10) por (tempoAndando * 4).', r'tempoAndando\s*\*\s*4\s*\)'],
        ['Herói mais rápido', 'No quadro, troque o passo 150 * dt por 300 * dt e confira se a animação ainda combina.', r'passo\s*=\s*300\s*\*\s*dt'],
        ['Moeda mais devagar', 'Troque (tempoTotal * 12) por (tempoTotal * 6).', r'tempoTotal\s*\*\s*6\s*\)'],
    ],
    setup=SETUP_SPRITES,
)

aula(
    'Som: efeitos com audioplayers',
    'Som é metade da sensação de um jogo: o jogador percebe o acerto antes de olhar o placar. O pacote '
    'audioplayers toca arquivos de áudio. Um AudioPlayer é um tocador; play(AssetSource(\'sons/moeda.wav\')) toca '
    'um arquivo da pasta assets/sons (o AssetSource já começa em assets/). Aqui há dois tocadores, um para cada '
    'tipo de efeito, para que um som não corte o outro. O jogo é pegar moedas: elas aparecem em lugares sorteados, '
    'giram e somem depois de 2 segundos. Tocar numa moeda (a distância entre o dedo e o centro menor que 28) dá '
    'ponto e toca moeda.wav; errar toca clique.wav; a cada 10 pontos toca poder.wav. A moeda que está para sumir '
    'fica transparente: o alfa da cor do Paint também vale para imagens.',
    'Em ▶ Testar, pegue moedas e ouça os efeitos (o botão 🔊 Som no topo liga e desliga). Troque o som do erro por '
    'batida.wav, deixe as moedas durarem menos e faça o fim de cada moeda perdida tocar dano.wav.',
    r'''
import 'dart:math';
import 'dart:ui' as ui;
import 'package:audioplayers/audioplayers.dart';
import 'package:flutter/material.dart';
import 'package:flutter/scheduler.dart';
import 'package:flutter/services.dart';

void main() => runApp(const MaterialApp(home: Jogo()));

const double largura = 360;
const double altura = 520;

Future<ui.Image> carregarImagem(String caminho) async {
  final dados = await rootBundle.load(caminho);
  return decodeImageFromList(dados.buffer.asUint8List());
}

class Moeda {
  final Offset centro;
  double vida = 2;
  Moeda(this.centro);
}

class Cena extends CustomPainter {
  final ui.Image folha;
  final List<Moeda> moedas;
  final int quadro;
  Cena(this.folha, this.moedas, this.quadro);

  @override
  void paint(Canvas canvas, Size size) {
    canvas.drawRect(Rect.fromLTWH(0, 0, size.width, size.height), Paint()..color = const Color(0xFF1D1B33));
    final origem = Rect.fromLTWH(quadro * 16.0, 0, 16, 16);
    for (final m in moedas) {
      final opacidade = m.vida < 0.5 ? m.vida * 2 : 1.0;
      final tinta = Paint()..color = Colors.white.withOpacity(opacidade);
      canvas.drawImageRect(folha, origem, Rect.fromCenter(center: m.centro, width: 40, height: 40), tinta);
    }
  }

  @override
  bool shouldRepaint(covariant Cena antiga) => true;
}

class Jogo extends StatefulWidget {
  const Jogo({super.key});

  @override
  State<Jogo> createState() => _JogoState();
}

class _JogoState extends State<Jogo> with SingleTickerProviderStateMixin {
  late Ticker ticker;
  double ultimo = 0;
  ui.Image? folha;
  final sorteio = Random();
  final somAcerto = AudioPlayer();
  final somErro = AudioPlayer();
  List<Moeda> moedas = [];
  double tempoProxima = 0;
  double tempoTotal = 0;
  int pontos = 0;
  int perdidas = 0;

  @override
  void initState() {
    super.initState();
    carregar();
    ticker = createTicker(quadro);
    ticker.start();
  }

  Future<void> carregar() async {
    final f = await carregarImagem('assets/sprites/moeda.png');
    setState(() => folha = f);
  }

  void quadro(Duration tempo) {
    final agora = tempo.inMicroseconds / 1000000;
    final dt = agora - ultimo;
    ultimo = agora;
    if (folha == null) return;
    setState(() {
      tempoTotal += dt;
      tempoProxima -= dt;
      if (tempoProxima <= 0) {
        moedas.add(Moeda(Offset(30 + sorteio.nextDouble() * 300, 60 + sorteio.nextDouble() * 420)));
        tempoProxima = 0.7;
      }
      for (final m in moedas) {
        m.vida -= dt;
      }
      perdidas += moedas.where((m) => m.vida <= 0).length;
      moedas.removeWhere((m) => m.vida <= 0);
    });
  }

  void tocar(TapDownDetails details) {
    Moeda? pega;
    for (final m in moedas) {
      if ((m.centro - details.localPosition).distance < 28) {
        pega = m;
        break;
      }
    }
    setState(() {
      if (pega != null) {
        moedas.remove(pega);
        pontos++;
        if (pontos % 10 == 0) {
          somAcerto.play(AssetSource('sons/poder.wav'));
        } else {
          somAcerto.play(AssetSource('sons/moeda.wav'));
        }
      } else {
        somErro.play(AssetSource('sons/clique.wav'));
      }
    });
  }

  @override
  void dispose() {
    ticker.dispose();
    somAcerto.dispose();
    somErro.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(title: Text('Moedas: $pontos · perdidas: $perdidas')),
      body: folha == null
          ? const Center(child: CircularProgressIndicator())
          : Center(
              child: GestureDetector(
                onTapDown: tocar,
                child: CustomPaint(
                  size: const Size(largura, altura),
                  painter: Cena(folha!, moedas, (tempoTotal * 12).floor() % 6),
                ),
              ),
            ),
    );
  }
}
''',
    [
        ['Erro com batida.wav', "No somErro, troque 'sons/clique.wav' por 'sons/batida.wav'.", r"somErro\.play\(\s*AssetSource\(\s*'sons/batida\.wav'"],
        ['Moedas que duram menos', 'Na classe Moeda, troque double vida = 2 por 1.2.', r'double vida\s*=\s*1\.2\b'],
        ['Som quando uma moeda some', "Quando perdidas aumentar, toque AssetSource('sons/dano.wav') no somErro.", r"sons/dano\.wav"],
    ],
    lim="No simulador os sons são sintetizados pelo navegador, com timbre de videogame antigo. Os nomes disponíveis são pulo, moeda, batida, explosao, tiro, vitoria, derrota, clique, dano e poder (em sons/NOME.wav). O navegador só libera som depois do primeiro toque ou tecla.",
    setup='No terminal do projeto:\n  flutter pub add audioplayers\n\npubspec.yaml (dentro de flutter:):\n  assets:\n    - assets/sprites/\n    - assets/sons/\n\nColoque seus arquivos .wav ou .mp3 em assets/sons/. Sites como freesound.org e opengameart.org têm efeitos livres (confira a licença de cada um).',
)

aula(
    'Texto de jogo: contorno, sombra e fonte',
    'Texto dentro do Canvas usa TextPainter: ele recebe um TextSpan com o texto e o estilo, layout() calcula o '
    'tamanho e paint(canvas, posição) desenha. Depois do layout, tp.width diz a largura real do texto, e '
    '(size.width - tp.width) / 2 centraliza. O título de jogo clássico tem contorno: o mesmo texto é desenhado '
    'duas vezes no mesmo lugar, primeiro com foreground: Paint() com style stroke (só a borda, grossa) e depois '
    'preenchido por cima. A sombra vem de shadows: [Shadow(...)]. A fonte pixelada vem do pacote google_fonts '
    '(GoogleFonts.pressStart2p), que baixa a fonte na primeira vez. O título balança com sin(tempo), e o convite '
    'pisca porque só é desenhado quando (tempo * 2).floor() é par.',
    'Em ▶ Testar, veja o título balançar e o convite piscar; cada toque troca a cor. Engrosse o contorno para 10, '
    'mude a sombra para baixo e à direita e troque a fonte do recorde por GoogleFonts.vt323.',
    r'''
import 'dart:math';
import 'package:flutter/material.dart';
import 'package:flutter/scheduler.dart';
import 'package:google_fonts/google_fonts.dart';

void main() => runApp(const MaterialApp(home: Abertura()));

const double largura = 360;
const double altura = 520;

TextPainter escrever(String texto, TextStyle estilo) {
  return TextPainter(
    text: TextSpan(text: texto, style: estilo),
    textDirection: TextDirection.ltr,
  )..layout();
}

class Titulo extends CustomPainter {
  final double tempo;
  final Color cor;
  final int recorde;
  Titulo(this.tempo, this.cor, this.recorde);

  @override
  void paint(Canvas canvas, Size size) {
    canvas.drawRect(Rect.fromLTWH(0, 0, size.width, size.height), Paint()..color = const Color(0xFF241B4B));
    final estrela = Paint()..color = Colors.white70;
    for (int i = 0; i < 40; i++) {
      canvas.drawCircle(Offset((i * 97) % largura, (i * 53) % altura), i % 3 == 0 ? 2.0 : 1.0, estrela);
    }

    final y = 140 + sin(tempo * 2) * 6;
    final borda = escrever('PULA\nCAIXA', TextStyle(
      fontSize: 64,
      fontWeight: FontWeight.w900,
      foreground: Paint()
        ..style = PaintingStyle.stroke
        ..strokeWidth = 8
        ..color = Colors.black,
    ));
    final cheio = escrever('PULA\nCAIXA', TextStyle(
      fontSize: 64,
      fontWeight: FontWeight.w900,
      color: cor,
      shadows: const [Shadow(color: Colors.black54, offset: Offset(0, 6), blurRadius: 6)],
    ));
    final x = (size.width - cheio.width) / 2;
    borda.paint(canvas, Offset(x, y));
    cheio.paint(canvas, Offset(x, y));

    if ((tempo * 2).floor() % 2 == 0) {
      final convite = escrever('TOQUE PARA COMEÇAR', GoogleFonts.pressStart2p(fontSize: 14, color: Colors.white));
      convite.paint(canvas, Offset((size.width - convite.width) / 2, 380));
    }
    final placar = escrever('RECORDE $recorde m', GoogleFonts.pressStart2p(fontSize: 12, color: Colors.amberAccent));
    placar.paint(canvas, Offset((size.width - placar.width) / 2, 440));
  }

  @override
  bool shouldRepaint(covariant Titulo antiga) => true;
}

class Abertura extends StatefulWidget {
  const Abertura({super.key});

  @override
  State<Abertura> createState() => _AberturaState();
}

class _AberturaState extends State<Abertura> with SingleTickerProviderStateMixin {
  late Ticker ticker;
  double tempo = 0;
  int indiceCor = 0;
  final cores = [Colors.amber, Colors.lightGreenAccent, Colors.cyanAccent, Colors.pinkAccent];

  @override
  void initState() {
    super.initState();
    ticker = createTicker((t) => setState(() => tempo = t.inMicroseconds / 1000000));
    ticker.start();
  }

  @override
  void dispose() {
    ticker.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: Center(
        child: GestureDetector(
          onTapDown: (_) => setState(() => indiceCor = (indiceCor + 1) % cores.length),
          child: CustomPaint(
            size: const Size(largura, altura),
            painter: Titulo(tempo, cores[indiceCor], 128),
          ),
        ),
      ),
    );
  }
}
''',
    [
        ['Contorno mais grosso (10)', 'No Paint da borda, troque strokeWidth = 8 por 10.', r'strokeWidth\s*=\s*10\b'],
        ['Sombra para baixo e à direita', 'No Shadow do título, troque Offset(0, 6) por Offset(6, 6).', r'Shadow\([^)]*offset:\s*Offset\(\s*[1-9]\d*\s*,\s*[1-9]'],
        ['Recorde com VT323', 'No placar, troque GoogleFonts.pressStart2p por GoogleFonts.vt323 (e aumente o fontSize para 24).', r"placar\s*=\s*escrever\([^;]*GoogleFonts\.vt323"],
    ],
    lim='No simulador, as fontes do google_fonts que já vêm prontas são pressStart2p, silkscreen, vt323 e bungee. Sem internet, o texto aparece numa fonte parecida.',
    setup='No terminal do projeto:\n  flutter pub add google_fonts\n\nO google_fonts baixa a fonte na primeira execução. Para o jogo funcionar sem internet, baixe o arquivo .ttf, ponha em assets/fontes/ e declare em fonts: no pubspec.yaml.',
)

PARTS.append(['Sprites: imagens no Canvas', 'Parte 3 · Sprites, animação, som e texto'])

aula(
    'Projeto · Pega-Maçã',
    'O segundo projeto junta as Partes 1, 2 e 3. Maçãs e slimes caem do céu; o herói anda pelo chão, arrastando o '
    'dedo ou com as setas, e precisa pegar as maçãs e fugir dos slimes. Cada maçã vale um ponto e toca moeda.wav. '
    'Cada slime tira um coração, toca dano.wav e deixa o herói piscando e invencível por 1 segundo (tempoInvencivel). '
    'Sem corações, a partida acaba, toca derrota.wav e o recorde é atualizado. Os itens caem cada vez mais rápido e '
    'mais seguido, porque a velocidade e o intervalo dependem do tempo de partida. A classe Item guarda o que é '
    'comum às maçãs e aos slimes; o campo boa diz qual é qual. O HUD (corações e pontos) e as telas de começo e '
    'fim são desenhados no próprio Canvas, com sprites e TextPainter.',
    'Em ▶ Testar, jogue algumas partidas com o dedo (arrastando) e com as setas do teclado. Depois mude o jogo: '
    'comece com 5 corações, faça uma maçã dourada (rara) valer 5 pontos e deixe os slimes mais lentos que as maçãs.',
    r'''
import 'dart:math';
import 'dart:ui' as ui;
import 'package:audioplayers/audioplayers.dart';
import 'package:flutter/material.dart';
import 'package:flutter/scheduler.dart';
import 'package:flutter/services.dart';
import 'package:google_fonts/google_fonts.dart';

void main() => runApp(const MaterialApp(home: PegaMaca()));

const double largura = 360;
const double altura = 520;
const double chao = 448;
const double tamanhoHeroi = 56;

enum Estado { pronto, jogando, fim }

Future<ui.Image> carregarImagem(String caminho) async {
  final dados = await rootBundle.load(caminho);
  return decodeImageFromList(dados.buffer.asUint8List());
}

TextPainter escrever(String texto, TextStyle estilo) {
  return TextPainter(text: TextSpan(text: texto, style: estilo), textDirection: TextDirection.ltr)..layout();
}

class Sprites {
  final ui.Image heroi;
  final ui.Image maca;
  final ui.Image slime;
  final ui.Image coracao;
  final ui.Image grama;
  Sprites(this.heroi, this.maca, this.slime, this.coracao, this.grama);
}

class Item {
  double x;
  double y;
  final bool boa;
  Item(this.x, this.y, this.boa);

  Rect get area => Rect.fromLTWH(x, y, 36, 36);
}

class Cena extends CustomPainter {
  final Sprites s;
  final _PegaMacaState jogo;
  Cena(this.s, this.jogo);

  @override
  void paint(Canvas canvas, Size size) {
    canvas.drawRect(Rect.fromLTWH(0, 0, size.width, size.height), Paint()..color = const Color(0xFF9AD8F5));
    final tinta = Paint();
    const bloco = Rect.fromLTWH(0, 0, 16, 16);
    for (int i = 0; i < 12; i++) {
      canvas.drawImageRect(s.grama, bloco, Rect.fromLTWH(i * 32.0, chao, 32, 32), tinta);
    }
    canvas.drawRect(Rect.fromLTWH(0, chao + 32, size.width, size.height - chao - 32), Paint()..color = const Color(0xFF8B5A2B));

    final quadroSlime = (jogo.tempoTotal * 4).floor() % 2;
    for (final item in jogo.itens) {
      if (item.boa) {
        canvas.drawImageRect(s.maca, bloco, item.area, tinta);
      } else {
        canvas.drawImageRect(s.slime, Rect.fromLTWH(quadroSlime * 16.0, 0, 16, 16), item.area, tinta);
      }
    }

    final piscando = jogo.tempoInvencivel > 0 && (jogo.tempoInvencivel * 10).floor() % 2 == 0;
    if (!piscando) {
      final quadro = jogo.andando ? (jogo.tempoAndando * 10).floor() % 4 : 0;
      canvas.save();
      canvas.translate(jogo.x + tamanhoHeroi / 2, chao - tamanhoHeroi);
      canvas.scale(jogo.direcao, 1);
      canvas.drawImageRect(s.heroi, Rect.fromLTWH(quadro * 16.0, 0, 16, 16), const Rect.fromLTWH(-tamanhoHeroi / 2, 0, tamanhoHeroi, tamanhoHeroi), tinta);
      canvas.restore();
    }

    for (int i = 0; i < jogo.vidas; i++) {
      canvas.drawImageRect(s.coracao, bloco, Rect.fromLTWH(12 + i * 28.0, 12, 24, 24), tinta);
    }
    final placar = escrever('${jogo.pontos}', GoogleFonts.pressStart2p(fontSize: 18, color: Colors.white, shadows: const [Shadow(color: Colors.black, offset: Offset(2, 2))]));
    placar.paint(canvas, Offset(size.width - placar.width - 14, 16));

    if (jogo.estado != Estado.jogando) {
      canvas.drawRect(Rect.fromLTWH(0, 0, size.width, size.height), Paint()..color = Colors.black45);
      final texto = jogo.estado == Estado.pronto ? 'PEGA\nMAÇÃ' : 'FIM!';
      final borda = escrever(texto, TextStyle(fontSize: 56, fontWeight: FontWeight.w900, foreground: Paint()..style = PaintingStyle.stroke..strokeWidth = 8..color = Colors.black));
      final cheio = escrever(texto, const TextStyle(fontSize: 56, fontWeight: FontWeight.w900, color: Colors.redAccent));
      final x = (size.width - cheio.width) / 2;
      borda.paint(canvas, Offset(x, 110));
      cheio.paint(canvas, Offset(x, 110));
      final dica = escrever(jogo.estado == Estado.pronto ? 'TOQUE OU ESPAÇO' : 'RECORDE ${jogo.recorde}', GoogleFonts.pressStart2p(fontSize: 13, color: Colors.white));
      dica.paint(canvas, Offset((size.width - dica.width) / 2, 300));
    }
  }

  @override
  bool shouldRepaint(covariant Cena antiga) => true;
}

class PegaMaca extends StatefulWidget {
  const PegaMaca({super.key});

  @override
  State<PegaMaca> createState() => _PegaMacaState();
}

class _PegaMacaState extends State<PegaMaca> with SingleTickerProviderStateMixin {
  late Ticker ticker;
  double ultimo = 0;
  Sprites? sprites;
  final sorteio = Random();
  final somItem = AudioPlayer();
  final somFim = AudioPlayer();

  Estado estado = Estado.pronto;
  List<Item> itens = [];
  double x = (largura - tamanhoHeroi) / 2;
  double direcao = 1;
  bool andando = false;
  double tempoAndando = 0;
  double ultimoMovimento = -1;
  double tempoTotal = 0;
  double tempoDePartida = 0;
  double tempoProximo = 0;
  double tempoInvencivel = 0;
  int vidas = 3;
  int pontos = 0;
  int recorde = 0;

  double get velocidadeQueda => 140 + tempoDePartida * 6;
  double get intervalo => max(0.35, 1.1 - tempoDePartida * 0.02);

  @override
  void initState() {
    super.initState();
    carregar();
    ticker = createTicker(quadro);
    ticker.start();
  }

  Future<void> carregar() async {
    final heroi = await carregarImagem('assets/sprites/heroi.png');
    final maca = await carregarImagem('assets/sprites/maca.png');
    final slime = await carregarImagem('assets/sprites/slime.png');
    final coracao = await carregarImagem('assets/sprites/coracao.png');
    final grama = await carregarImagem('assets/sprites/grama.png');
    setState(() => sprites = Sprites(heroi, maca, slime, coracao, grama));
  }

  void quadro(Duration tempo) {
    final agora = tempo.inMicroseconds / 1000000;
    final dt = agora - ultimo;
    ultimo = agora;
    setState(() {
      tempoTotal += dt;
      if (estado == Estado.jogando) atualizar(dt);
    });
  }

  void atualizar(double dt) {
    tempoDePartida += dt;
    if (tempoInvencivel > 0) tempoInvencivel -= dt;

    final teclado = HardwareKeyboard.instance;
    double movimento = 0;
    if (teclado.isLogicalKeyPressed(LogicalKeyboardKey.arrowLeft)) movimento -= 260 * dt;
    if (teclado.isLogicalKeyPressed(LogicalKeyboardKey.arrowRight)) movimento += 260 * dt;
    if (movimento != 0) mover(movimento);
    andando = tempoTotal - ultimoMovimento < 0.12;
    tempoAndando = andando ? tempoAndando + dt : 0;

    tempoProximo -= dt;
    if (tempoProximo <= 0) {
      itens.add(Item(sorteio.nextDouble() * (largura - 36), -36, sorteio.nextDouble() < 0.75));
      tempoProximo = intervalo;
    }
    for (final item in itens) {
      item.y += velocidadeQueda * dt;
    }

    final heroi = Rect.fromLTWH(x, chao - tamanhoHeroi, tamanhoHeroi, tamanhoHeroi).deflate(8);
    final pegos = itens.where((item) => item.area.overlaps(heroi)).toList();
    for (final item in pegos) {
      if (item.boa) {
        pontos++;
        somItem.play(AssetSource('sons/moeda.wav'));
      } else if (tempoInvencivel <= 0) {
        vidas--;
        tempoInvencivel = 1;
        somItem.play(AssetSource('sons/dano.wav'));
      }
    }
    itens.removeWhere((item) => pegos.contains(item) || item.y > chao);

    if (vidas <= 0) {
      estado = Estado.fim;
      if (pontos > recorde) recorde = pontos;
      somFim.play(AssetSource('sons/derrota.wav'));
    }
  }

  void mover(double dx) {
    x += dx;
    if (x < 0) x = 0;
    if (x > largura - tamanhoHeroi) x = largura - tamanhoHeroi;
    if (dx != 0) {
      direcao = dx > 0 ? 1.0 : -1.0;
      ultimoMovimento = tempoTotal;
    }
  }

  void comecar() {
    setState(() {
      if (estado == Estado.jogando) return;
      itens.clear();
      vidas = 3;
      pontos = 0;
      tempoDePartida = 0;
      tempoProximo = 0.5;
      tempoInvencivel = 0;
      estado = Estado.jogando;
      somFim.play(AssetSource('sons/poder.wav'));
    });
  }

  KeyEventResult tecla(FocusNode node, KeyEvent event) {
    if (event is KeyDownEvent && event.logicalKey == LogicalKeyboardKey.space) {
      comecar();
      return KeyEventResult.handled;
    }
    return KeyEventResult.ignored;
  }

  @override
  void dispose() {
    ticker.dispose();
    somItem.dispose();
    somFim.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: sprites == null
          ? const Center(child: CircularProgressIndicator())
          : Center(
              child: Focus(
                autofocus: true,
                onKeyEvent: tecla,
                child: GestureDetector(
                  onTapDown: (_) => comecar(),
                  onPanUpdate: (details) => mover(details.delta.dx),
                  child: CustomPaint(
                    size: const Size(largura, altura),
                    painter: Cena(sprites!, this),
                  ),
                ),
              ),
            ),
    );
  }
}
''',
    [
        ['Começar com 5 corações', 'Em comecar() e na declaração, troque vidas = 3 por 5.', r'int vidas\s*=\s*5\b[\s\S]*vidas\s*=\s*5\s*;|vidas\s*=\s*5\s*;[\s\S]*int vidas\s*=\s*5\b'],
        ['Maçã dourada que vale 5', 'Acrescente um campo dourada no Item (sorteado raramente), some 5 pontos quando pegar e pinte com Colors.amber por cima (Paint com colorFilter) ou desenhe um círculo dourado.', r'dourada'],
        ['Slimes mais lentos', "No laço que faz os itens caírem, use velocidadeQueda * 0.6 quando o item não for boa.", r'boa\s*\?\s*velocidadeQueda\s*:\s*velocidadeQueda\s*\*|!\s*item\.boa[\s\S]{0,80}\*\s*0\.\d'],
    ],
    lim="O painter recebe o próprio State (Cena(sprites!, this)) para ler os campos do jogo: é um atalho comum em protótipos. Em projetos maiores, separe o estado do jogo numa classe própria, como o Flame faz.",
    setup=SETUP_SPRITES + '\n\nSons: flutter pub add audioplayers e assets/sons/ (moeda.wav, dano.wav, derrota.wav, poder.wav).\nFonte: flutter pub add google_fonts.',
)

PARTS.append(['Projeto · Pega-Maçã', 'Projeto 2 · Pega-Maçã'])
