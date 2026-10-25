# Aulas da Oficina Flutter 2 · trilha de jogos.
# Cada código é um app Flutter completo: roda no simulador e também num projeto real.

LESSONS = []
EXERCISES = {}


def aula(t, text, tryit, code, ex, lim=None):
    LESSONS.append({'t': t, 'text': text, 'tryit': tryit, 'code': code, 'lim': lim})
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
    lim='O simulador entrega o toque quando o clique termina (como onTap). No celular, onTapDown dispara assim que o dedo encosta.',
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

PARTS = [
    ['O laço do jogo com Timer.periodic', 'Parte 1 · Fundamentos de jogos 2D'],
    ['Projeto · Pula-Caixa', 'Projeto 1 · Pula-Caixa'],
]
