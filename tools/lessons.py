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
    'cena antiga com a nova e só redesenha quando algo mudou. O personagem é o vira-lata caramelo, montado com '
    'retângulos e círculos na função desenharCaramelo, no fim do arquivo: translate leva o desenho até o lugar dele '
    'e scale(direcao, 1) espelha o cachorro, então +1 olha para a direita e -1 para a esquerda.',
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
    desenharCaramelo(canvas, corpo, const Color(0xFFD68C3E), direcao);
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

/// O vira-lata caramelo desenhado com retângulos e círculos, dentro do retângulo r (40 × 48).
/// direcao 1 olha para a direita e -1 para a esquerda.
void desenharCaramelo(Canvas canvas, Rect r, Color pelo, double direcao) {
  canvas.save();
  canvas.translate(r.center.dx, r.center.dy);
  canvas.scale(direcao * r.width / 40, r.height / 48);
  final cor = Paint()..color = pelo;
  final escuro = Paint()..color = const Color(0xFF9C5E28);
  final claro = Paint()..color = const Color(0xFFF6CE96);
  final preto = Paint()..color = Colors.black;
  canvas.drawLine(const Offset(-14, 0), const Offset(-19, -12), Paint()..color = const Color(0xFF9C5E28)..strokeWidth = 4..strokeCap = StrokeCap.round);
  canvas.drawRect(const Rect.fromLTWH(-14, 14, 6, 10), cor);
  canvas.drawRect(const Rect.fromLTWH(-5, 14, 6, 10), cor);
  canvas.drawRect(const Rect.fromLTWH(6, 14, 6, 10), cor);
  canvas.drawRRect(RRect.fromRectAndRadius(const Rect.fromLTWH(-17, -2, 31, 18), const Radius.circular(6)), cor);
  canvas.drawRect(const Rect.fromLTWH(-12, 11, 22, 4), claro);
  canvas.drawRRect(RRect.fromRectAndRadius(const Rect.fromLTWH(1, -22, 18, 20), const Radius.circular(6)), cor);
  canvas.drawRect(const Rect.fromLTWH(3, -26, 6, 9), escuro);
  canvas.drawRRect(RRect.fromRectAndRadius(const Rect.fromLTWH(13, -12, 8, 7), const Radius.circular(3)), claro);
  canvas.drawCircle(const Offset(20, -11), 2, preto);
  canvas.drawCircle(const Offset(10, -15), 2.5, preto);
  canvas.restore();
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
    desenharCaramelo(canvas, corpo, const Color(0xFFD68C3E), 1);
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

/// O vira-lata caramelo desenhado com retângulos e círculos, dentro do retângulo r (40 × 48).
/// direcao 1 olha para a direita e -1 para a esquerda.
void desenharCaramelo(Canvas canvas, Rect r, Color pelo, double direcao) {
  canvas.save();
  canvas.translate(r.center.dx, r.center.dy);
  canvas.scale(direcao * r.width / 40, r.height / 48);
  final cor = Paint()..color = pelo;
  final escuro = Paint()..color = const Color(0xFF9C5E28);
  final claro = Paint()..color = const Color(0xFFF6CE96);
  final preto = Paint()..color = Colors.black;
  canvas.drawLine(const Offset(-14, 0), const Offset(-19, -12), Paint()..color = const Color(0xFF9C5E28)..strokeWidth = 4..strokeCap = StrokeCap.round);
  canvas.drawRect(const Rect.fromLTWH(-14, 14, 6, 10), cor);
  canvas.drawRect(const Rect.fromLTWH(-5, 14, 6, 10), cor);
  canvas.drawRect(const Rect.fromLTWH(6, 14, 6, 10), cor);
  canvas.drawRRect(RRect.fromRectAndRadius(const Rect.fromLTWH(-17, -2, 31, 18), const Radius.circular(6)), cor);
  canvas.drawRect(const Rect.fromLTWH(-12, 11, 22, 4), claro);
  canvas.drawRRect(RRect.fromRectAndRadius(const Rect.fromLTWH(1, -22, 18, 20), const Radius.circular(6)), cor);
  canvas.drawRect(const Rect.fromLTWH(3, -26, 6, 9), escuro);
  canvas.drawRRect(RRect.fromRectAndRadius(const Rect.fromLTWH(13, -12, 8, 7), const Radius.circular(3)), claro);
  canvas.drawCircle(const Offset(20, -11), 2, preto);
  canvas.drawCircle(const Offset(10, -15), 2.5, preto);
  canvas.restore();
}
''',
    [
        ['Velocidade de 400 px/s', 'Troque double velocidade = 180 por 400.', r'double velocidade\s*=\s*400\b'],
        ['Marca amarela', 'No Paint da marca, troque Colors.white por Colors.yellow.', r'marca\s*=\s*Paint\(\)\s*\.\.color\s*=\s*Colors\.yellow'],
        ['Cor diferente enquanto anda', 'Passe para a Cena se x != alvo e use um operador ternário na cor que vai para o desenharCaramelo, como andando ? Colors.amber : const Color(0xFFD68C3E).', r'desenharCaramelo\(\s*canvas\s*,\s*corpo\s*,\s*\w+\s*\?'],
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
    desenharCaramelo(canvas, corpo, const Color(0xFFD68C3E), 1);
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

/// O vira-lata caramelo desenhado com retângulos e círculos, dentro do retângulo r (40 × 48).
/// direcao 1 olha para a direita e -1 para a esquerda.
void desenharCaramelo(Canvas canvas, Rect r, Color pelo, double direcao) {
  canvas.save();
  canvas.translate(r.center.dx, r.center.dy);
  canvas.scale(direcao * r.width / 40, r.height / 48);
  final cor = Paint()..color = pelo;
  final escuro = Paint()..color = const Color(0xFF9C5E28);
  final claro = Paint()..color = const Color(0xFFF6CE96);
  final preto = Paint()..color = Colors.black;
  canvas.drawLine(const Offset(-14, 0), const Offset(-19, -12), Paint()..color = const Color(0xFF9C5E28)..strokeWidth = 4..strokeCap = StrokeCap.round);
  canvas.drawRect(const Rect.fromLTWH(-14, 14, 6, 10), cor);
  canvas.drawRect(const Rect.fromLTWH(-5, 14, 6, 10), cor);
  canvas.drawRect(const Rect.fromLTWH(6, 14, 6, 10), cor);
  canvas.drawRRect(RRect.fromRectAndRadius(const Rect.fromLTWH(-17, -2, 31, 18), const Radius.circular(6)), cor);
  canvas.drawRect(const Rect.fromLTWH(-12, 11, 22, 4), claro);
  canvas.drawRRect(RRect.fromRectAndRadius(const Rect.fromLTWH(1, -22, 18, 20), const Radius.circular(6)), cor);
  canvas.drawRect(const Rect.fromLTWH(3, -26, 6, 9), escuro);
  canvas.drawRRect(RRect.fromRectAndRadius(const Rect.fromLTWH(13, -12, 8, 7), const Radius.circular(3)), claro);
  canvas.drawCircle(const Offset(20, -11), 2, preto);
  canvas.drawCircle(const Offset(10, -15), 2.5, preto);
  canvas.restore();
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
    'Um jogo tem vários objetos iguais: inimigos, ossos, caixas. Cada um vira uma instância de uma classe '
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
    desenharCaramelo(canvas, corpo, vermelho ? Colors.red : const Color(0xFFD68C3E), 1);
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

/// O vira-lata caramelo desenhado com retângulos e círculos, dentro do retângulo r (40 × 48).
/// direcao 1 olha para a direita e -1 para a esquerda.
void desenharCaramelo(Canvas canvas, Rect r, Color pelo, double direcao) {
  canvas.save();
  canvas.translate(r.center.dx, r.center.dy);
  canvas.scale(direcao * r.width / 40, r.height / 48);
  final cor = Paint()..color = pelo;
  final escuro = Paint()..color = const Color(0xFF9C5E28);
  final claro = Paint()..color = const Color(0xFFF6CE96);
  final preto = Paint()..color = Colors.black;
  canvas.drawLine(const Offset(-14, 0), const Offset(-19, -12), Paint()..color = const Color(0xFF9C5E28)..strokeWidth = 4..strokeCap = StrokeCap.round);
  canvas.drawRect(const Rect.fromLTWH(-14, 14, 6, 10), cor);
  canvas.drawRect(const Rect.fromLTWH(-5, 14, 6, 10), cor);
  canvas.drawRect(const Rect.fromLTWH(6, 14, 6, 10), cor);
  canvas.drawRRect(RRect.fromRectAndRadius(const Rect.fromLTWH(-17, -2, 31, 18), const Radius.circular(6)), cor);
  canvas.drawRect(const Rect.fromLTWH(-12, 11, 22, 4), claro);
  canvas.drawRRect(RRect.fromRectAndRadius(const Rect.fromLTWH(1, -22, 18, 20), const Radius.circular(6)), cor);
  canvas.drawRect(const Rect.fromLTWH(3, -26, 6, 9), escuro);
  canvas.drawRRect(RRect.fromRectAndRadius(const Rect.fromLTWH(13, -12, 8, 7), const Radius.circular(3)), claro);
  canvas.drawCircle(const Offset(20, -11), 2, preto);
  canvas.drawCircle(const Offset(10, -15), 2.5, preto);
  canvas.restore();
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
    desenharCaramelo(canvas, corpo, const Color(0xFFD68C3E), 1);
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

/// O vira-lata caramelo desenhado com retângulos e círculos, dentro do retângulo r (40 × 48).
/// direcao 1 olha para a direita e -1 para a esquerda.
void desenharCaramelo(Canvas canvas, Rect r, Color pelo, double direcao) {
  canvas.save();
  canvas.translate(r.center.dx, r.center.dy);
  canvas.scale(direcao * r.width / 40, r.height / 48);
  final cor = Paint()..color = pelo;
  final escuro = Paint()..color = const Color(0xFF9C5E28);
  final claro = Paint()..color = const Color(0xFFF6CE96);
  final preto = Paint()..color = Colors.black;
  canvas.drawLine(const Offset(-14, 0), const Offset(-19, -12), Paint()..color = const Color(0xFF9C5E28)..strokeWidth = 4..strokeCap = StrokeCap.round);
  canvas.drawRect(const Rect.fromLTWH(-14, 14, 6, 10), cor);
  canvas.drawRect(const Rect.fromLTWH(-5, 14, 6, 10), cor);
  canvas.drawRect(const Rect.fromLTWH(6, 14, 6, 10), cor);
  canvas.drawRRect(RRect.fromRectAndRadius(const Rect.fromLTWH(-17, -2, 31, 18), const Radius.circular(6)), cor);
  canvas.drawRect(const Rect.fromLTWH(-12, 11, 22, 4), claro);
  canvas.drawRRect(RRect.fromRectAndRadius(const Rect.fromLTWH(1, -22, 18, 20), const Radius.circular(6)), cor);
  canvas.drawRect(const Rect.fromLTWH(3, -26, 6, 9), escuro);
  canvas.drawRRect(RRect.fromRectAndRadius(const Rect.fromLTWH(13, -12, 8, 7), const Radius.circular(3)), claro);
  canvas.drawCircle(const Offset(20, -11), 2, preto);
  canvas.drawCircle(const Offset(10, -15), 2.5, preto);
  canvas.restore();
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
    'cenário noturno, deixe a aceleração mais forte e acrescente um osso que vale 10 metros.',
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
    desenharCaramelo(canvas, corpo, perdeu ? Colors.red : const Color(0xFFD68C3E), 1);
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

/// O vira-lata caramelo desenhado com retângulos e círculos, dentro do retângulo r (40 × 48).
/// direcao 1 olha para a direita e -1 para a esquerda.
void desenharCaramelo(Canvas canvas, Rect r, Color pelo, double direcao) {
  canvas.save();
  canvas.translate(r.center.dx, r.center.dy);
  canvas.scale(direcao * r.width / 40, r.height / 48);
  final cor = Paint()..color = pelo;
  final escuro = Paint()..color = const Color(0xFF9C5E28);
  final claro = Paint()..color = const Color(0xFFF6CE96);
  final preto = Paint()..color = Colors.black;
  canvas.drawLine(const Offset(-14, 0), const Offset(-19, -12), Paint()..color = const Color(0xFF9C5E28)..strokeWidth = 4..strokeCap = StrokeCap.round);
  canvas.drawRect(const Rect.fromLTWH(-14, 14, 6, 10), cor);
  canvas.drawRect(const Rect.fromLTWH(-5, 14, 6, 10), cor);
  canvas.drawRect(const Rect.fromLTWH(6, 14, 6, 10), cor);
  canvas.drawRRect(RRect.fromRectAndRadius(const Rect.fromLTWH(-17, -2, 31, 18), const Radius.circular(6)), cor);
  canvas.drawRect(const Rect.fromLTWH(-12, 11, 22, 4), claro);
  canvas.drawRRect(RRect.fromRectAndRadius(const Rect.fromLTWH(1, -22, 18, 20), const Radius.circular(6)), cor);
  canvas.drawRect(const Rect.fromLTWH(3, -26, 6, 9), escuro);
  canvas.drawRRect(RRect.fromRectAndRadius(const Rect.fromLTWH(13, -12, 8, 7), const Radius.circular(3)), claro);
  canvas.drawCircle(const Offset(20, -11), 2, preto);
  canvas.drawCircle(const Offset(10, -15), 2.5, preto);
  canvas.restore();
}
''',
    [
        ['Cenário noturno', 'Troque a cor do céu (0xFF8FD3FE) por um azul escuro, como Color(0xFF14213D).', r'^(?![\s\S]*0xFF8FD3FE)'],
        ['Aceleração mais forte', 'No getter velocidade, troque tempoDePartida * 8 por * 15.', r'tempoDePartida\s*\*\s*15\b'],
        ['Um osso que vale 10 metros', 'Crie uma classe Osso com x e y, uma lista ossos, desenhe com drawCircle amarelo e some 10 * 20 ao deslocamento quando o jogador encostar.', r'class\s+Osso\b[\s\S]*Colors\.(?:yellow|amber)'],
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
    lim='O arrasto funciona com mouse e com o dedo. Para gestos com dois dedos (pinça), veja a aula de zoom na Parte 5.',
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
    desenharCaramelo(canvas, corpo, const Color(0xFFD68C3E), 1);
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

/// O vira-lata caramelo desenhado com retângulos e círculos, dentro do retângulo r (40 × 48).
/// direcao 1 olha para a direita e -1 para a esquerda.
void desenharCaramelo(Canvas canvas, Rect r, Color pelo, double direcao) {
  canvas.save();
  canvas.translate(r.center.dx, r.center.dy);
  canvas.scale(direcao * r.width / 40, r.height / 48);
  final cor = Paint()..color = pelo;
  final escuro = Paint()..color = const Color(0xFF9C5E28);
  final claro = Paint()..color = const Color(0xFFF6CE96);
  final preto = Paint()..color = Colors.black;
  canvas.drawLine(const Offset(-14, 0), const Offset(-19, -12), Paint()..color = const Color(0xFF9C5E28)..strokeWidth = 4..strokeCap = StrokeCap.round);
  canvas.drawRect(const Rect.fromLTWH(-14, 14, 6, 10), cor);
  canvas.drawRect(const Rect.fromLTWH(-5, 14, 6, 10), cor);
  canvas.drawRect(const Rect.fromLTWH(6, 14, 6, 10), cor);
  canvas.drawRRect(RRect.fromRectAndRadius(const Rect.fromLTWH(-17, -2, 31, 18), const Radius.circular(6)), cor);
  canvas.drawRect(const Rect.fromLTWH(-12, 11, 22, 4), claro);
  canvas.drawRRect(RRect.fromRectAndRadius(const Rect.fromLTWH(1, -22, 18, 20), const Radius.circular(6)), cor);
  canvas.drawRect(const Rect.fromLTWH(3, -26, 6, 9), escuro);
  canvas.drawRRect(RRect.fromRectAndRadius(const Rect.fromLTWH(13, -12, 8, 7), const Radius.circular(3)), claro);
  canvas.drawCircle(const Offset(20, -11), 2, preto);
  canvas.drawCircle(const Offset(10, -15), 2.5, preto);
  canvas.restore();
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
    'desenhados para a Oficina: heroi.png (o vira-lata caramelo, 4 quadros de 16×16), osso.png (6), osso_dourado.png (6), gato.png (2), pombo.png (2), caramelo_sentado.png (2), caramelo_pulo.png, caramelo_latindo.png (2), nave.png (2), '
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
  final ui.Image osso;
  Sprites(this.heroi, this.grama, this.caixa, this.osso);
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
    canvas.drawImageRect(s.osso, bloco, const Rect.fromLTWH(252, chao - 96, 24, 24), tinta);
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
    final osso = await carregarImagem('assets/sprites/osso.png');
    setState(() => sprites = Sprites(heroi, grama, caixa, osso));
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
        ['Uma maçã em cima da caixa', "Carregue 'assets/sprites/maca.png' como as outras (um campo novo em Sprites) e desenhe acima da caixa.", r"^(?=[\s\S]*assets/sprites/maca\.png)(?=[\s\S]*drawImageRect\(\s*s\.maca)"],
    ],
    lim='Aqui a escolha fica dentro do Scaffold, com ?:. Um if (...) return antes do return final também funciona no simulador. rootBundle lê os sprites prontos e as imagens que você acrescentar no botão 🖼 Sprites.',
    setup=SETUP_SPRITES,
)

aula(
    'Animação com folha de sprites',
    'Uma folha de sprites (sprite sheet) guarda os quadros de uma animação lado a lado, todos do mesmo tamanho. '
    'Animar é escolher qual pedaço recortar em cada momento: o quadro i começa em x = i * 16. O tempo decide o '
    'quadro: (tempo * 10).floor() % 4 troca de quadro 10 vezes por segundo e volta ao primeiro depois do quarto. '
    'O herói só conta o tempo de caminhada enquanto anda; parado, ele mostra o quadro 0. O osso tem o seu '
    'próprio relógio (12 quadros por segundo, 6 quadros), porque cada animação tem o seu ritmo. Para virar o '
    'herói para a esquerda não é preciso outra imagem: canvas.save, translate até o centro do sprite, scale(-1, 1) '
    'espelha tudo o que vier depois, e canvas.restore desfaz a transformação para o resto da cena.',
    'Em ▶ Testar, toque em pontos à esquerda e à direita e veja o herói andar e virar. Mude a velocidade da '
    'animação de 10 para 4 e para 20 quadros por segundo. Depois faça o osso brilhar mais devagar.',
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
  final ui.Image osso;
  final ui.Image grama;
  final double x;
  final double direcao;
  final int quadroHeroi;
  final int quadroOsso;
  Cena(this.heroi, this.osso, this.grama, this.x, this.direcao, this.quadroHeroi, this.quadroOsso);

  @override
  void paint(Canvas canvas, Size size) {
    canvas.drawRect(Rect.fromLTWH(0, 0, size.width, size.height), Paint()..color = const Color(0xFF7EC8F2));
    canvas.drawRect(Rect.fromLTWH(0, chao + 32, size.width, size.height - chao - 32), Paint()..color = const Color(0xFF8B5A2B));
    final tinta = Paint();
    for (int i = 0; i < 12; i++) {
      canvas.drawImageRect(grama, const Rect.fromLTWH(0, 0, 16, 16), Rect.fromLTWH(i * 32.0, chao, 32, 32), tinta);
    }

    final origemOsso = Rect.fromLTWH(quadroOsso * 16.0, 0, 16, 16);
    canvas.drawImageRect(osso, origemOsso, const Rect.fromLTWH(300, 24, 40, 40), tinta);

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
  ui.Image? osso;
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
    final m = await carregarImagem('assets/sprites/osso.png');
    final g = await carregarImagem('assets/sprites/grama.png');
    setState(() {
      heroi = h;
      osso = m;
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
    final quadroOsso = (tempoTotal * 12).floor() % 6;
    return Scaffold(
      backgroundColor: Colors.black,
      body: heroi == null || osso == null || grama == null
          ? const Center(child: CircularProgressIndicator())
          : Center(
              child: GestureDetector(
                onTapDown: tocar,
                child: CustomPaint(
                  size: const Size(largura, altura),
                  painter: Cena(heroi!, osso!, grama!, x, direcao, quadroHeroi, quadroOsso),
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
        ['Osso mais devagar', 'Troque (tempoTotal * 12) por (tempoTotal * 6).', r'tempoTotal\s*\*\s*6\s*\)'],
    ],
    setup=SETUP_SPRITES,
)

aula(
    'Som: efeitos com audioplayers',
    'Som é metade da sensação de um jogo: o jogador percebe o acerto antes de olhar o placar. O pacote '
    'audioplayers toca arquivos de áudio. Um AudioPlayer é um tocador; play(AssetSource(\'sons/osso.wav\')) toca '
    'um arquivo da pasta assets/sons (o AssetSource já começa em assets/). Aqui há dois tocadores, um para cada '
    'tipo de efeito, para que um som não corte o outro. O jogo é pegar ossos: eles aparecem em lugares sorteados, '
    'brilham e somem depois de 2 segundos. Tocar num osso (a distância entre o dedo e o centro menor que 28) dá '
    'ponto e toca osso.wav; errar toca clique.wav; a cada 10 pontos toca poder.wav. O osso que está para sumir '
    'fica transparente: o alfa da cor do Paint também vale para imagens.',
    'Em ▶ Testar, pegue ossos e ouça os efeitos (o botão 🔊 Som no topo liga e desliga). Troque o som do erro por '
    'batida.wav, deixe os ossos durarem menos e faça o fim de cada osso perdido tocar dano.wav.',
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

class Osso {
  final Offset centro;
  double vida = 2;
  Osso(this.centro);
}

class Cena extends CustomPainter {
  final ui.Image folha;
  final List<Osso> ossos;
  final int quadro;
  Cena(this.folha, this.ossos, this.quadro);

  @override
  void paint(Canvas canvas, Size size) {
    canvas.drawRect(Rect.fromLTWH(0, 0, size.width, size.height), Paint()..color = const Color(0xFF1D1B33));
    final origem = Rect.fromLTWH(quadro * 16.0, 0, 16, 16);
    for (final m in ossos) {
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
  List<Osso> ossos = [];
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
    final f = await carregarImagem('assets/sprites/osso.png');
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
        ossos.add(Osso(Offset(30 + sorteio.nextDouble() * 300, 60 + sorteio.nextDouble() * 420)));
        tempoProxima = 0.7;
      }
      for (final m in ossos) {
        m.vida -= dt;
      }
      perdidas += ossos.where((m) => m.vida <= 0).length;
      ossos.removeWhere((m) => m.vida <= 0);
    });
  }

  void tocar(TapDownDetails details) {
    Osso? pega;
    for (final m in ossos) {
      if ((m.centro - details.localPosition).distance < 28) {
        pega = m;
        break;
      }
    }
    setState(() {
      if (pega != null) {
        ossos.remove(pega);
        pontos++;
        if (pontos % 10 == 0) {
          somAcerto.play(AssetSource('sons/poder.wav'));
        } else {
          somAcerto.play(AssetSource('sons/osso.wav'));
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
      appBar: AppBar(title: Text('Ossos: $pontos · perdidas: $perdidas')),
      body: folha == null
          ? const Center(child: CircularProgressIndicator())
          : Center(
              child: GestureDetector(
                onTapDown: tocar,
                child: CustomPaint(
                  size: const Size(largura, altura),
                  painter: Cena(folha!, ossos, (tempoTotal * 12).floor() % 6),
                ),
              ),
            ),
    );
  }
}
''',
    [
        ['Erro com batida.wav', "No somErro, troque 'sons/clique.wav' por 'sons/batida.wav'.", r"somErro\.play\(\s*AssetSource\(\s*'sons/batida\.wav'"],
        ['Ossos que duram menos', 'Na classe Osso, troque double vida = 2 por 1.2.', r'double vida\s*=\s*1\.2\b'],
        ['Som quando um osso some', "Quando perdidas aumentar, toque AssetSource('sons/dano.wav') no somErro.", r"sons/dano\.wav"],
    ],
    lim="No simulador os sons são sintetizados pelo navegador, com timbre de videogame antigo. Os nomes disponíveis são pulo, osso, latido, batida, explosao, tiro, vitoria, derrota, clique, dano e poder (em sons/NOME.wav). O navegador só libera som depois do primeiro toque ou tecla.",
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
    'Efeitos visuais: degradê, brilho e sombra',
    'Três truques do Paint deixam a cena muito mais bonita. O degradê é um shader: ui.Gradient.linear(de, até, cores) '
    'pinta o céu indo do azul-escuro ao roxo, e ui.Gradient.radial(centro, raio, cores, paradas) faz um círculo que '
    'vai mudando de cor do centro para fora. O brilho é desfoque: maskFilter = MaskFilter.blur(BlurStyle.normal, 24) '
    'espalha a cor do círculo atrás da lua, e blendMode = BlendMode.plus soma a luz do osso com o que já está '
    'embaixo, em vez de cobrir. A sombra vem de canvas.drawShadow(caminho, cor, elevação, false), que desenha a sombra '
    'de um Path como se ele estivesse flutuando. A escuridão da noite é um degradê radial em cima de tudo: '
    'transparente perto do dedo e quase preto nas bordas, como uma lanterna. A ordem importa: a lua e o brilho do osso '
    'são pintados depois da escuridão, por isso aparecem mesmo no escuro.',
    'Em ▶ Testar, arraste o dedo para mover a lanterna e encoste a luz no osso que brilha. Aumente o raio da luz, '
    'deixe o brilho da lua mais espalhado e troque o céu por um pôr do sol.',
    r'''
import 'dart:math';
import 'dart:ui' as ui;
import 'package:flutter/material.dart';
import 'package:flutter/scheduler.dart';

void main() => runApp(const MaterialApp(home: Lanterna()));

const double largura = 360;
const double altura = 600;

class Lanterna extends StatefulWidget {
  const Lanterna({super.key});
  @override
  State<Lanterna> createState() => _LanternaState();
}

class _LanternaState extends State<Lanterna> with SingleTickerProviderStateMixin {
  final sorteio = Random();
  late Ticker ticker;
  double tempo = 0;
  Offset luz = const Offset(180, 300);
  Offset osso = const Offset(90, 420);
  int achados = 0;

  @override
  void initState() {
    super.initState();
    ticker = createTicker((t) => setState(() => tempo = t.inMilliseconds / 1000))..start();
  }

  @override
  void dispose() {
    ticker.dispose();
    super.dispose();
  }

  void mover(Offset p) {
    setState(() {
      luz = p;
      if ((luz - osso).distance < 30) {
        achados++;
        osso = Offset(40 + sorteio.nextDouble() * (largura - 80), 300 + sorteio.nextDouble() * (altura - 340));
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: GestureDetector(
        onPanDown: (d) => mover(d.localPosition),
        onPanUpdate: (d) => mover(d.localPosition),
        child: CustomPaint(
          size: const Size(largura, altura),
          painter: Noite(tempo, luz, osso, achados),
        ),
      ),
    );
  }
}

class Noite extends CustomPainter {
  final double tempo;
  final Offset luz;
  final Offset osso;
  final int achados;
  Noite(this.tempo, this.luz, this.osso, this.achados);

  @override
  void paint(Canvas canvas, Size size) {
    // céu com degradê: do azul-escuro ao roxo
    final ceu = Paint()
      ..shader = ui.Gradient.linear(Offset.zero, Offset(0, size.height * 0.6), [const Color(0xFF0B1026), const Color(0xFF4B2A6B)]);
    canvas.drawRect(Rect.fromLTWH(0, 0, size.width, size.height), ceu);

    // chão
    canvas.drawRect(Rect.fromLTWH(0, 280, size.width, size.height - 280), Paint()..color = const Color(0xFF1F3B22));

    // osso com sombra
    final forma = Path()
      ..addRRect(RRect.fromRectAndRadius(Rect.fromCenter(center: osso, width: 34, height: 8), const Radius.circular(4)))
      ..addOval(Rect.fromCircle(center: osso + const Offset(-17, -4), radius: 6))
      ..addOval(Rect.fromCircle(center: osso + const Offset(-17, 4), radius: 6))
      ..addOval(Rect.fromCircle(center: osso + const Offset(17, -4), radius: 6))
      ..addOval(Rect.fromCircle(center: osso + const Offset(17, 4), radius: 6));
    canvas.drawShadow(forma, Colors.black, 6, false);
    canvas.drawPath(forma, Paint()..color = const Color(0xFFFAF4E2));

    // a escuridão: um degradê radial transparente no centro da luz e preto nas bordas
    final escuro = Paint()
      ..shader = ui.Gradient.radial(luz, 140, [Colors.transparent, Colors.black.withOpacity(0.92)], [0.45, 1]);
    canvas.drawRect(Rect.fromLTWH(0, 0, size.width, size.height), escuro);

    // a lua vem depois da escuridão, então ela fica sempre acesa; o brilho é um círculo desfocado
    const lua = Offset(280, 90);
    canvas.drawCircle(lua, 46, Paint()
      ..color = const Color(0x88FFF4C2)
      ..maskFilter = const MaskFilter.blur(BlurStyle.normal, 24));
    canvas.drawCircle(lua, 30, Paint()..color = const Color(0xFFFFF4C2));

    // o brilho do osso também vem depois: com BlendMode.plus ele soma luz ao que está embaixo
    final pulso = 0.5 + 0.5 * sin(tempo * 4);
    canvas.drawCircle(osso, 22 + 6 * pulso, Paint()
      ..color = Colors.amber.withOpacity(0.35)
      ..maskFilter = const MaskFilter.blur(BlurStyle.normal, 12)
      ..blendMode = BlendMode.plus);
    final texto = TextPainter(
      text: TextSpan(text: 'Ossos achados: $achados', style: const TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold)),
      textDirection: TextDirection.ltr,
    )..layout();
    texto.paint(canvas, const Offset(16, 16));
  }

  @override
  bool shouldRepaint(covariant Noite antiga) => true;
}
''',
    [
        ['Lanterna maior', 'No Paint escuro, troque o raio 140 do ui.Gradient.radial por 200.', r'ui\.Gradient\.radial\(\s*luz\s*,\s*(?!140\b)\d+'],
        ['Lua mais brilhante', 'No círculo desfocado da lua, troque MaskFilter.blur(BlurStyle.normal, 24) por 40.', r'BlurStyle\.normal,\s*(?!24\b|12\b)\d+'],
        ['Pôr do sol', 'No degradê do céu, troque a cor de baixo (0xFF4B2A6B) por um laranja, como const Color(0xFFFF8A3D).', r'^(?![\s\S]*0xFF4B2A6B)'],
    ],
    lim='No simulador o desfoque usa o filtro do navegador, então o raio pode parecer um pouco diferente do celular. BlendMode tem os modos mais comuns (plus, multiply, screen, overlay, darken, lighten, difference e outros).',
)

aula(
    'Projeto · Pega-Maçã',
    'O segundo projeto junta as Partes 1, 2 e 3. Maçãs e gatos caem do céu; o herói anda pelo chão, arrastando o '
    'dedo ou com as setas, e precisa pegar as maçãs e fugir dos gatos. Cada maçã vale um ponto e toca osso.wav. '
    'Cada gato tira um coração, toca dano.wav e deixa o herói piscando e invencível por 1 segundo (tempoInvencivel). '
    'Sem corações, a partida acaba, toca derrota.wav e o recorde é atualizado. Os itens caem cada vez mais rápido e '
    'mais seguido, porque a velocidade e o intervalo dependem do tempo de partida. A classe Item guarda o que é '
    'comum às maçãs e aos gatos; o campo boa diz qual é qual. O HUD (corações e pontos) e as telas de começo e '
    'fim são desenhados no próprio Canvas, com sprites e TextPainter.',
    'Em ▶ Testar, jogue algumas partidas com o dedo (arrastando) e com as setas do teclado. Depois mude o jogo: '
    'comece com 5 corações, faça uma maçã dourada (rara) valer 5 pontos e deixe os gatos mais lentos que as maçãs.',
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
  final ui.Image gato;
  final ui.Image coracao;
  final ui.Image grama;
  Sprites(this.heroi, this.maca, this.gato, this.coracao, this.grama);
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

    final quadroGato = (jogo.tempoTotal * 4).floor() % 2;
    for (final item in jogo.itens) {
      if (item.boa) {
        canvas.drawImageRect(s.maca, bloco, item.area, tinta);
      } else {
        canvas.drawImageRect(s.gato, Rect.fromLTWH(quadroGato * 16.0, 0, 16, 16), item.area, tinta);
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
    final gato = await carregarImagem('assets/sprites/gato.png');
    final coracao = await carregarImagem('assets/sprites/coracao.png');
    final grama = await carregarImagem('assets/sprites/grama.png');
    setState(() => sprites = Sprites(heroi, maca, gato, coracao, grama));
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
        somItem.play(AssetSource('sons/osso.wav'));
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
        ['Gatos mais lentos', "No laço que faz os itens caírem, use velocidadeQueda * 0.6 quando o item não for boa.", r'boa\s*\?\s*velocidadeQueda\s*:\s*velocidadeQueda\s*\*|!\s*item\.boa[\s\S]{0,80}\*\s*0\.\d'],
    ],
    lim="O painter recebe o próprio State (Cena(sprites!, this)) para ler os campos do jogo: é um atalho comum em protótipos. Em projetos maiores, separe o estado do jogo numa classe própria, como o Flame faz.",
    setup=SETUP_SPRITES + '\n\nSons: flutter pub add audioplayers e assets/sons/ (osso.wav, dano.wav, derrota.wav, poder.wav).\nFonte: flutter pub add google_fonts.',
)

PARTS.append(['Projeto · Pega-Maçã', 'Projeto 2 · Pega-Maçã'])


# ---------------------------------------------------------------- Parte 4 · Flame
SETUP_FLAME = (
    'No terminal do projeto:\n'
    '  flutter pub add flame\n\n'
    'O Flame procura imagens em assets/images/ e sons em assets/audio/. No pubspec.yaml (dentro de flutter:):\n'
    '  assets:\n'
    '    - assets/images/\n'
    '    - assets/audio/\n\n'
    'No simulador, os sprites prontos (heroi.png, osso.png, gato.png, pombo.png, nave.png, explosao.png, tiro.png, caixa.png, '
    'coracao.png, maca.png, grama.png, nuvem.png, ceu.png, montanhas.png, colinas.png), os sons (pulo.wav, osso.wav, latido.wav, '
    'batida.wav, explosao.wav, tiro.wav, vitoria.wav, derrota.wav, clique.wav, dano.wav, poder.wav) e as músicas '
    '(musica_aventura.mp3, musica_espaco.mp3, musica_menu.mp3) já existem com esses nomes. Imagens suas entram pelo botão 🖼 Sprites.'
)

aula(
    'Flame: o primeiro jogo',
    'Flame é o motor de jogos 2D mais usado com Flutter. Ele traz pronto o que você montou à mão nas Partes 1 a 3: o '
    'laço com dt, o desenho no Canvas e a lista de objetos. O jogo é uma classe que estende FlameGame e aparece na '
    'tela com GameWidget(game: MeuJogo()). Tudo dentro dele é um componente: o onLoad do jogo cria as bolas e chama '
    'add() para colocá-las no jogo. Cada Bola estende PositionComponent, que já tem position, size, angle e anchor. '
    'O Flame chama update(dt) de todos os componentes a cada quadro e depois render(canvas), com o canvas já '
    'deslocado para a posição do componente: por isso a bola desenha o círculo em relação ao próprio canto, sem '
    'somar position. Com anchor: Anchor.center, a position passa a ser o centro da bola. game.size é o tamanho da '
    'tela do jogo. Ligue o debugMode para ver o contorno e a posição de cada componente.',
    'Em ▶ Testar, veja as bolas quicarem. Mude debugMode para true, acrescente uma terceira bola no onLoad e troque a '
    'cor de fundo em backgroundColor.',
    r'''
import 'package:flame/components.dart';
import 'package:flame/game.dart';
import 'package:flutter/material.dart';

void main() => runApp(GameWidget(game: MeuJogo()));

class MeuJogo extends FlameGame {
  @override
  Future<void> onLoad() async {
    debugMode = false;
    add(Bola(Vector2(80, 120), Vector2(150, 110), Colors.amber));
    add(Bola(Vector2(220, 360), Vector2(-120, 160), Colors.pinkAccent));
  }

  @override
  Color backgroundColor() => const Color(0xFF14213D);
}

class Bola extends PositionComponent with HasGameReference<MeuJogo> {
  Vector2 velocidade;
  final Color cor;

  Bola(Vector2 inicio, this.velocidade, this.cor)
      : super(position: inicio, size: Vector2.all(40), anchor: Anchor.center);

  @override
  void update(double dt) {
    super.update(dt);
    position += velocidade * dt;
    if (position.x < 20 || position.x > game.size.x - 20) {
      velocidade.x = -velocidade.x;
    }
    if (position.y < 20 || position.y > game.size.y - 20) {
      velocidade.y = -velocidade.y;
    }
  }

  @override
  void render(Canvas canvas) {
    canvas.drawCircle(Offset(size.x / 2, size.y / 2), size.x / 2, Paint()..color = cor);
  }
}
''',
    [
        ['Ligar o debugMode', 'No onLoad do jogo, troque debugMode = false por true.', r'debugMode\s*=\s*true'],
        ['Terceira bola', 'Acrescente mais um add(Bola(...)) no onLoad, com outra posição, velocidade e cor.', r'(?:add\(\s*Bola\([\s\S]*?){3}'],
        ['Outro fundo', 'Em backgroundColor, troque Color(0xFF14213D) por outra cor.', r'^(?![\s\S]*0xFF14213D)'],
    ],
    lim='O Flame do simulador é uma versão simplificada: tem os componentes, eventos, colisões, efeitos, partículas, paralaxe, overlays, joystick, física do Forge2D e mapas do Tiled mais usados. O botão ⚠ Limites lista o que existe.',
    setup=SETUP_FLAME,
)

aula(
    'Flame: sprites e animação',
    'No Flame, desenhar imagem não precisa de CustomPainter: SpriteComponent mostra um Sprite e SpriteAnimationComponent '
    'mostra uma animação. game.loadSprite(\'caixa.png\') carrega a imagem da pasta assets/images e devolve o Sprite. '
    'Para animar uma folha de sprites, game.loadSpriteAnimation recebe a imagem e um SpriteAnimationData.sequenced: '
    'quantos quadros (amount), quanto tempo cada um fica na tela (stepTime) e o tamanho de cada quadro na folha '
    '(textureSize). O componente troca de quadro sozinho no update. O herói aqui anda de um lado a outro; ao chegar na '
    'borda ele inverte a direção e chama flipHorizontallyAroundCenter(), que espelha o desenho sem mudar a posição. O '
    'osso brilha com 6 quadros, cada um por 0,08 segundo.',
    'Em ▶ Testar, veja o herói andar e virar nas bordas. Deixe a animação mais lenta (stepTime 0.25), troque a caixa '
    'pela maçã e coloque três ossos em fila.',
    r'''
import 'package:flame/components.dart';
import 'package:flame/game.dart';
import 'package:flutter/material.dart';

void main() => runApp(GameWidget(game: Vitrine()));

class Vitrine extends FlameGame {
  @override
  Future<void> onLoad() async {
    add(RectangleComponent(position: Vector2(0, size.y - 32), size: Vector2(size.x, 32), paint: Paint()..color = const Color(0xFF8B5A2B)));
    final grama = await loadSprite('grama.png');
    for (int i = 0; i < 12; i++) {
      add(SpriteComponent(sprite: grama, position: Vector2(i * 32.0, size.y - 64), size: Vector2.all(32)));
    }
    add(SpriteComponent(sprite: await loadSprite('caixa.png'), position: Vector2(250, size.y - 112), size: Vector2.all(48)));

    final giro = await loadSpriteAnimation(
      'osso.png',
      SpriteAnimationData.sequenced(amount: 6, stepTime: 0.08, textureSize: Vector2.all(16)),
    );
    add(SpriteAnimationComponent(animation: giro, position: Vector2(262, size.y - 170), size: Vector2.all(24)));

    add(Heroi());
  }

  @override
  Color backgroundColor() => const Color(0xFF7EC8F2);
}

class Heroi extends SpriteAnimationComponent with HasGameReference<Vitrine> {
  double direcao = 1;

  Heroi() : super(size: Vector2.all(64), anchor: Anchor.bottomCenter);

  @override
  Future<void> onLoad() async {
    animation = await game.loadSpriteAnimation(
      'heroi.png',
      SpriteAnimationData.sequenced(amount: 4, stepTime: 0.1, textureSize: Vector2.all(16)),
    );
    position = Vector2(80, game.size.y - 64);
  }

  @override
  void update(double dt) {
    super.update(dt);
    position.x += 120 * direcao * dt;
    if ((direcao > 0 && position.x > game.size.x - 32) || (direcao < 0 && position.x < 32)) {
      direcao = -direcao;
      flipHorizontallyAroundCenter();
    }
  }
}
''',
    [
        ['Animação mais lenta', 'No SpriteAnimationData do herói, troque stepTime: 0.1 por 0.25.', r"heroi\.png[\s\S]{0,140}stepTime:\s*0\.25"],
        ['Maçã no lugar da caixa', "Troque loadSprite('caixa.png') por loadSprite('maca.png').", r"loadSprite\(\s*'maca\.png'\s*\)"],
        ['Três ossos', 'Crie os ossos num for com i de 0 a 2, mudando o x de cada um (todos podem usar a mesma animação giro).', r'for\s*\([^)]*\)\s*\{[\s\S]{0,200}SpriteAnimationComponent\(\s*animation:\s*giro'],
    ],
    setup=SETUP_FLAME,
)

aula(
    'Flame: toque e arrasto em componentes',
    'No Flame, quem recebe o toque é o componente. Basta acrescentar o mixin TapCallbacks e escrever onTapDown: o Flame '
    'só chama o método se o dedo cair dentro do retângulo daquele componente, e event.localPosition diz onde, a partir '
    'do canto dele. Aqui cada osso some quando tocado e toca um som com FlameAudio.play(\'osso.wav\') (os sons ficam '
    'em assets/audio). Para arrastar, o mixin é DragCallbacks: onDragUpdate recebe event.localDelta, quanto o dedo andou '
    'desde a última vez. O herói só anda na horizontal, então soma só o x. O próprio jogo também pode ter '
    'TapCallbacks: ele recebe os toques que não caíram em nenhum componente; aqui um toque no vazio cria um osso novo.',
    'Em ▶ Testar, pegue os ossos tocando neles, arraste o herói e toque no céu vazio para criar ossos. Faça o herói '
    'arrastar também na vertical e conte os pontos no título com um TextComponent.',
    r'''
import 'package:flame/components.dart';
import 'package:flame/events.dart';
import 'package:flame/game.dart';
import 'package:flame_audio/flame_audio.dart';
import 'package:flutter/material.dart';

void main() => runApp(GameWidget(game: Toques()));

class Toques extends FlameGame with TapCallbacks {
  int pontos = 0;

  @override
  Future<void> onLoad() async {
    for (int i = 0; i < 4; i++) {
      add(Osso(Vector2(60 + i * 80.0, 160)));
    }
    add(Heroi());
  }

  @override
  void onTapDown(TapDownEvent event) {
    add(Osso(event.canvasPosition));
  }

  @override
  Color backgroundColor() => const Color(0xFF1D1B33);
}

class Osso extends SpriteAnimationComponent with TapCallbacks, HasGameReference<Toques> {
  Osso(Vector2 posicao) : super(position: posicao, size: Vector2.all(40), anchor: Anchor.center);

  @override
  Future<void> onLoad() async {
    animation = await game.loadSpriteAnimation(
      'osso.png',
      SpriteAnimationData.sequenced(amount: 6, stepTime: 0.08, textureSize: Vector2.all(16)),
    );
  }

  @override
  void onTapDown(TapDownEvent event) {
    game.pontos++;
    FlameAudio.play('osso.wav');
    removeFromParent();
  }
}

class Heroi extends SpriteAnimationComponent with DragCallbacks, HasGameReference<Toques> {
  Heroi() : super(size: Vector2.all(72), anchor: Anchor.center);

  @override
  Future<void> onLoad() async {
    animation = await game.loadSpriteAnimation(
      'heroi.png',
      SpriteAnimationData.sequenced(amount: 4, stepTime: 0.12, textureSize: Vector2.all(16)),
    );
    position = Vector2(game.size.x / 2, game.size.y - 120);
  }

  @override
  void onDragUpdate(DragUpdateEvent event) {
    position.x += event.localDelta.x;
  }
}
''',
    [
        ['Arrastar na vertical também', 'No onDragUpdate, some também event.localDelta.y ao position.y (ou use position += event.localDelta).', r'position\.y\s*\+=\s*event\.localDelta\.y|position\s*\+=\s*event\.localDelta'],
        ['Ossos maiores', 'No construtor do Osso, troque Vector2.all(40) por Vector2.all(56).', r'Vector2\.all\(\s*56\s*\)'],
        ['Placar com TextComponent', "Crie um TextComponent no onLoad do jogo, guarde num campo late TextComponent placar e atualize placar.text no update do jogo.", r'placar\.text\s*='],
    ],
    setup=SETUP_FLAME,
)

aula(
    'Flame: colisões com hitboxes',
    'Para o Flame testar colisões, o jogo usa o mixin HasCollisionDetection e cada componente que colide ganha um '
    'hitbox como filho: RectangleHitbox ou CircleHitbox, que por padrão ocupam o tamanho do componente. O componente '
    'que quer saber da colisão usa CollisionCallbacks e escreve onCollisionStart(pontos, outro): o Flame chama uma vez, '
    'no primeiro quadro em que os dois se tocam, e "outro" é o componente do outro lado. Com is dá para saber o tipo '
    '(if (other is Pombo)). Aqui a nave atira sozinha a cada 0,3 segundo (TimerComponent), os pombos descem e, quando '
    'um tiro acerta um pombo, os dois somem e nasce uma explosão: uma SpriteAnimationComponent com loop: false e '
    'removeOnFinish: true, que se apaga sozinha no último quadro. Ligue o debugMode para ver os hitboxes em amarelo.',
    'Em ▶ Testar, arraste a nave e acerte os pombos. Ligue debugMode, troque o CircleHitbox do pombo por um '
    'RectangleHitbox e faça a nave atirar mais rápido.',
    r'''
import 'dart:math';
import 'package:flame/collisions.dart';
import 'package:flame/components.dart';
import 'package:flame/events.dart';
import 'package:flame/game.dart';
import 'package:flame_audio/flame_audio.dart';
import 'package:flutter/material.dart';

void main() => runApp(GameWidget(game: Espaco()));

class Espaco extends FlameGame with HasCollisionDetection {
  final sorteio = Random();
  late Nave nave;

  @override
  Future<void> onLoad() async {
    debugMode = false;
    nave = Nave();
    add(nave);
    add(TimerComponent(period: 0.3, repeat: true, onTick: () => add(Tiro(nave.position.clone()))));
    add(TimerComponent(period: 0.9, repeat: true, onTick: () => add(Pombo(Vector2(30 + sorteio.nextDouble() * (size.x - 60), -30)))));
  }

  @override
  Color backgroundColor() => const Color(0xFF0B0F2A);
}

class Nave extends SpriteAnimationComponent with DragCallbacks, HasGameReference<Espaco> {
  Nave() : super(size: Vector2.all(56), anchor: Anchor.center);

  @override
  Future<void> onLoad() async {
    animation = await game.loadSpriteAnimation(
      'nave.png',
      SpriteAnimationData.sequenced(amount: 2, stepTime: 0.1, textureSize: Vector2.all(16)),
    );
    position = Vector2(game.size.x / 2, game.size.y - 90);
  }

  @override
  void onDragUpdate(DragUpdateEvent event) {
    position.x += event.localDelta.x;
  }
}

class Tiro extends SpriteComponent with HasGameReference<Espaco> {
  Tiro(Vector2 inicio) : super(position: inicio, size: Vector2(12, 24), anchor: Anchor.center);

  @override
  Future<void> onLoad() async {
    sprite = await game.loadSprite('tiro.png');
    add(RectangleHitbox());
  }

  @override
  void update(double dt) {
    super.update(dt);
    position.y -= 420 * dt;
    if (position.y < -20) removeFromParent();
  }
}

class Pombo extends SpriteAnimationComponent with CollisionCallbacks, HasGameReference<Espaco> {
  Pombo(Vector2 inicio) : super(position: inicio, size: Vector2.all(48), anchor: Anchor.center);

  @override
  Future<void> onLoad() async {
    animation = await game.loadSpriteAnimation(
      'pombo.png',
      SpriteAnimationData.sequenced(amount: 2, stepTime: 0.3, textureSize: Vector2.all(16)),
    );
    add(CircleHitbox());
  }

  @override
  void update(double dt) {
    super.update(dt);
    position.y += 90 * dt;
    if (position.y > game.size.y + 30) removeFromParent();
  }

  @override
  void onCollisionStart(Set<Vector2> intersectionPoints, PositionComponent other) {
    super.onCollisionStart(intersectionPoints, other);
    if (other is Tiro) {
      other.removeFromParent();
      removeFromParent();
      game.add(Explosao(position.clone()));
      FlameAudio.play('explosao.wav');
    }
  }
}

class Explosao extends SpriteAnimationComponent with HasGameReference<Espaco> {
  Explosao(Vector2 onde) : super(position: onde, size: Vector2.all(64), anchor: Anchor.center, removeOnFinish: true);

  @override
  Future<void> onLoad() async {
    animation = await game.loadSpriteAnimation(
      'explosao.png',
      SpriteAnimationData.sequenced(amount: 5, stepTime: 0.07, textureSize: Vector2.all(16), loop: false),
    );
  }
}
''',
    [
        ['Ver os hitboxes', 'No onLoad do jogo, troque debugMode = false por true.', r'debugMode\s*=\s*true'],
        ['Pombo com RectangleHitbox', 'No onLoad do Pombo, troque CircleHitbox() por RectangleHitbox().', r'class Pombo[\s\S]*add\(\s*RectangleHitbox\(\s*\)\s*\)[\s\S]*class Explosao'],
        ['Tiro mais rápido', 'No primeiro TimerComponent, troque period: 0.3 por 0.15.', r'period:\s*0\.15\b'],
    ],
    setup=SETUP_FLAME,
)

aula(
    'Flame: teclado, mundo e câmera',
    'Jogos maiores que a tela usam mundo e câmera. Tudo o que é colocado com world.add fica no mundo, um espaço sem '
    'bordas; a câmera mostra só um pedaço dele. Por padrão o centro da tela é o ponto (0, 0) do mundo, e '
    'camera.follow(heroi) faz a câmera andar junto com o herói. O que deve ficar parado na tela, como o placar, vai '
    'para camera.viewport.add: é o HUD. O jogo recebe o teclado com o mixin KeyboardEvents: onKeyEvent ganha o evento '
    'e keysPressed, o conjunto de teclas apertadas neste momento. Guardar a direção num campo e usá-la no update do '
    'herói deixa o movimento contínuo enquanto a tecla está apertada. O chão é uma fila de 60 blocos de grama, muito '
    'mais larga que a tela, e as nuvens ajudam a perceber que a câmera está andando.',
    'Em ▶ Testar, clique no celular e ande com ← e →. Veja o placar mostrar o x do herói. Mude o zoom da câmera para '
    '1.5, faça o herói correr segurando Shift e acrescente ossos pelo caminho.',
    r'''
import 'package:flame/components.dart';
import 'package:flame/events.dart';
import 'package:flame/game.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

void main() => runApp(GameWidget(game: Caminhada()));

class Caminhada extends FlameGame with KeyboardEvents {
  late Heroi heroi;
  late TextComponent placar;

  @override
  Future<void> onLoad() async {
    world.add(RectangleComponent(position: Vector2(-960, 96), size: Vector2(1920, 600), paint: Paint()..color = const Color(0xFF8B5A2B)));
    final grama = await loadSprite('grama.png');
    for (int i = -30; i < 30; i++) {
      world.add(SpriteComponent(sprite: grama, position: Vector2(i * 32.0, 64), size: Vector2.all(32)));
    }
    final nuvem = await loadSprite('nuvem.png');
    for (int i = -6; i < 6; i++) {
      world.add(SpriteComponent(sprite: nuvem, position: Vector2(i * 170.0, -180.0 + (i % 3) * 40), size: Vector2(96, 48)));
    }
    heroi = Heroi();
    world.add(heroi);
    camera.follow(heroi);
    camera.viewfinder.zoom = 1;

    placar = TextComponent(
      text: '',
      position: Vector2(12, 12),
      textRenderer: TextPaint(style: const TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
    );
    camera.viewport.add(placar);
  }

  @override
  void update(double dt) {
    super.update(dt);
    placar.text = 'x = ${heroi.position.x.toStringAsFixed(0)}';
  }

  @override
  KeyEventResult onKeyEvent(KeyEvent event, Set<LogicalKeyboardKey> keysPressed) {
    heroi.direcao = 0;
    if (keysPressed.contains(LogicalKeyboardKey.arrowLeft)) heroi.direcao -= 1;
    if (keysPressed.contains(LogicalKeyboardKey.arrowRight)) heroi.direcao += 1;
    return KeyEventResult.handled;
  }

  @override
  Color backgroundColor() => const Color(0xFF7EC8F2);
}

class Heroi extends SpriteAnimationComponent with HasGameReference<Caminhada> {
  double direcao = 0;
  bool olhandoDireita = true;

  Heroi() : super(position: Vector2(0, 64), size: Vector2.all(64), anchor: Anchor.bottomCenter);

  @override
  Future<void> onLoad() async {
    animation = await game.loadSpriteAnimation(
      'heroi.png',
      SpriteAnimationData.sequenced(amount: 4, stepTime: 0.1, textureSize: Vector2.all(16)),
    );
  }

  @override
  void update(double dt) {
    super.update(dt);
    playing = direcao != 0;
    position.x += direcao * 180 * dt;
    if ((direcao < 0 && olhandoDireita) || (direcao > 0 && !olhandoDireita)) {
      olhandoDireita = !olhandoDireita;
      flipHorizontallyAroundCenter();
    }
  }
}
''',
    [
        ['Zoom de 1.5', 'Troque camera.viewfinder.zoom = 1 por 1.5.', r'camera\.viewfinder\.zoom\s*=\s*1\.5'],
        ['Correr com Shift', 'No onKeyEvent, se keysPressed tiver LogicalKeyboardKey.shiftLeft, multiplique a direção por 2.', r'LogicalKeyboardKey\.shiftLeft'],
        ['Ossos no caminho', "Crie ossos com world.add num for, usando game.loadSpriteAnimation('osso.png', ...) ou loadSprite.", r"world\.add\([\s\S]{0,200}osso|osso\.png[\s\S]*world\.add"],
    ],
    lim='Clique no celular antes de usar as teclas. Em celulares de verdade não há teclado: jogos para celular também precisam de controles de toque.',
    setup=SETUP_FLAME,
)

PARTS.append(['Flame: o primeiro jogo', 'Parte 4 · Flame'])

aula(
    'Projeto · Pula-Caixa em Flame',
    'O Pula-Caixa do Projeto 1 refeito com Flame, para comparar os dois jeitos de fazer o mesmo jogo. Antes havia um '
    'State com listas, um CustomPainter e a colisão AABB escrita à mão. Agora cada coisa é um componente com a sua '
    'própria lógica: o Jogador cuida da gravidade e do pulo, cada Caixa anda para a esquerda e se remove quando sai da '
    'tela, as Nuvens se repetem devagar (paralaxe) e o jogo só coordena: cria caixas, conta a distância e troca de '
    'estado. A colisão vem do Flame: o hitbox do jogador é um pouco menor que o desenho (RectangleHitbox com position '
    'e size), e onCollisionStart com uma Caixa termina a partida. O placar e o aviso são TextComponents. O jogo aceita '
    'toque (TapCallbacks) e teclado (espaço ou seta para cima, com KeyboardEvents) e toca pulo.wav e derrota.wav. '
    'O caramelo tem três animações e troca a cada quadro: sentado antes de começar, correndo no chão e '
    'pulando no ar (animation = noChao ? correndo : pulando).',
    'Em ▶ Testar, jogue tocando ou com o espaço. Compare este código com o do Projeto 1. Depois: deixe o céu noturno, '
    'aumente a aceleração e toque vitoria.wav quando o jogador passar de 100 m.',
    r'''
import 'dart:math';
import 'package:flame/collisions.dart';
import 'package:flame/components.dart';
import 'package:flame/events.dart';
import 'package:flame/game.dart';
import 'package:flame_audio/flame_audio.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

void main() => runApp(GameWidget(game: PulaCaixa()));

const double gravidade = 1700;
const double impulso = -680;

enum Estado { pronto, jogando, fim }

class PulaCaixa extends FlameGame with HasCollisionDetection, TapCallbacks, KeyboardEvents {
  final sorteio = Random();
  late Jogador jogador;
  late TextComponent placar;
  late TextComponent aviso;
  List<Caixa> caixas = [];
  Estado estado = Estado.pronto;
  double tempoDePartida = 0;
  double distancia = 0;
  double proximaCaixa = 1;
  int recorde = 0;

  double get chao => size.y - 96;
  double get velocidade => 220 + tempoDePartida * 8;
  int get metros => (distancia / 20).floor();

  @override
  Future<void> onLoad() async {
    add(RectangleComponent(
      position: Vector2(0, chao + 32),
      size: Vector2(size.x, size.y - chao - 32),
      paint: Paint()..color = const Color(0xFF8B5A2B),
    ));
    final grama = await loadSprite('grama.png');
    for (int i = 0; i < 12; i++) {
      add(SpriteComponent(sprite: grama, position: Vector2(i * 32.0, chao), size: Vector2.all(32)));
    }
    for (int i = 0; i < 3; i++) {
      add(Nuvem(Vector2(i * 150.0, 80.0 + i * 50)));
    }
    jogador = Jogador();
    add(jogador);

    const estilo = TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold);
    placar = TextComponent(position: Vector2(16, 16), textRenderer: TextPaint(style: estilo));
    aviso = TextComponent(
      text: 'Toque para começar',
      position: size / 2,
      anchor: Anchor.center,
      textRenderer: TextPaint(style: const TextStyle(color: Colors.white, fontSize: 26, fontWeight: FontWeight.bold)),
    );
    add(placar);
    add(aviso);
  }

  @override
  void update(double dt) {
    super.update(dt);
    if (estado == Estado.jogando) {
      tempoDePartida += dt;
      distancia += velocidade * dt;
      proximaCaixa -= dt;
      if (proximaCaixa <= 0) {
        final caixa = Caixa(Vector2(size.x + 30, chao), 30 + sorteio.nextDouble() * 30);
        caixas.add(caixa);
        add(caixa);
        proximaCaixa = 0.9 + sorteio.nextDouble() * 1.1;
      }
    }
    placar.text = '$metros m    recorde $recorde m';
  }

  void acao() {
    if (estado == Estado.pronto) {
      estado = Estado.jogando;
      aviso.text = '';
    } else if (estado == Estado.jogando) {
      jogador.pular();
    } else {
      for (final c in caixas) {
        c.removeFromParent();
      }
      caixas.clear();
      tempoDePartida = 0;
      distancia = 0;
      proximaCaixa = 1;
      jogador.position.y = chao;
      jogador.vy = 0;
      estado = Estado.pronto;
      aviso.text = 'Toque para começar';
    }
  }

  void perder() {
    estado = Estado.fim;
    if (metros > recorde) recorde = metros;
    aviso.text = 'Fim! $metros m';
    FlameAudio.play('derrota.wav');
  }

  @override
  void onTapDown(TapDownEvent event) => acao();

  @override
  KeyEventResult onKeyEvent(KeyEvent event, Set<LogicalKeyboardKey> keysPressed) {
    if (event is KeyDownEvent &&
        (event.logicalKey == LogicalKeyboardKey.space || event.logicalKey == LogicalKeyboardKey.arrowUp)) {
      acao();
      return KeyEventResult.handled;
    }
    return KeyEventResult.ignored;
  }

  @override
  Color backgroundColor() => const Color(0xFF8FD3FE);
}

class Jogador extends SpriteAnimationComponent with CollisionCallbacks, HasGameReference<PulaCaixa> {
  double vy = 0;
  late SpriteAnimation correndo;
  late SpriteAnimation pulando;
  late SpriteAnimation sentado;

  Jogador() : super(size: Vector2.all(56), anchor: Anchor.bottomLeft);

  bool get noChao => position.y >= game.chao;

  @override
  Future<void> onLoad() async {
    correndo = await game.loadSpriteAnimation(
      'heroi.png',
      SpriteAnimationData.sequenced(amount: 4, stepTime: 0.1, textureSize: Vector2.all(16)),
    );
    pulando = await game.loadSpriteAnimation(
      'caramelo_pulo.png',
      SpriteAnimationData.sequenced(amount: 1, stepTime: 1, textureSize: Vector2.all(16)),
    );
    sentado = await game.loadSpriteAnimation(
      'caramelo_sentado.png',
      SpriteAnimationData.sequenced(amount: 2, stepTime: 0.4, textureSize: Vector2.all(16)),
    );
    animation = sentado;
    position = Vector2(60, game.chao);
    add(RectangleHitbox(position: Vector2(10, 8), size: Vector2(36, 48)));
  }

  void pular() {
    if (noChao) {
      vy = impulso;
      FlameAudio.play('pulo.wav');
    }
  }

  @override
  void update(double dt) {
    super.update(dt);
    if (game.estado != Estado.jogando) {
      animation = sentado;
      return;
    }
    animation = noChao ? correndo : pulando;
    vy += gravidade * dt;
    position.y += vy * dt;
    if (position.y > game.chao) {
      position.y = game.chao;
      vy = 0;
    }
  }

  @override
  void onCollisionStart(Set<Vector2> intersectionPoints, PositionComponent other) {
    super.onCollisionStart(intersectionPoints, other);
    if (other is Caixa && game.estado == Estado.jogando) {
      game.perder();
    }
  }
}

class Caixa extends SpriteComponent with HasGameReference<PulaCaixa> {
  Caixa(Vector2 posicao, double lado) : super(position: posicao, size: Vector2.all(lado), anchor: Anchor.bottomLeft);

  @override
  Future<void> onLoad() async {
    sprite = await game.loadSprite('caixa.png');
    add(RectangleHitbox());
  }

  @override
  void update(double dt) {
    super.update(dt);
    if (game.estado == Estado.jogando) {
      position.x -= game.velocidade * dt;
    }
    if (position.x < -size.x) {
      removeFromParent();
      game.caixas.remove(this);
    }
  }
}

class Nuvem extends SpriteComponent with HasGameReference<PulaCaixa> {
  Nuvem(Vector2 posicao) : super(position: posicao, size: Vector2(96, 48));

  @override
  Future<void> onLoad() async {
    sprite = await game.loadSprite('nuvem.png');
  }

  @override
  void update(double dt) {
    super.update(dt);
    if (game.estado == Estado.jogando) {
      position.x -= game.velocidade * 0.2 * dt;
    }
    if (position.x < -100) {
      position.x = game.size.x + 20;
    }
  }
}
''',
    [
        ['Céu noturno', 'Em backgroundColor, troque Color(0xFF8FD3FE) por um azul escuro, como Color(0xFF14213D).', r'^(?![\s\S]*0xFF8FD3FE)'],
        ['Aceleração mais forte', 'No getter velocidade, troque tempoDePartida * 8 por * 15.', r'tempoDePartida\s*\*\s*15\b'],
        ['Som ao passar de 100 m', "Guarde um bool comemorou e, no update, quando metros passar de 100 pela primeira vez, toque FlameAudio.play('vitoria.wav').", r"vitoria\.wav"],
    ],
    setup=SETUP_FLAME,
)

PARTS.append(['Projeto · Pula-Caixa em Flame', 'Projeto 3 · Pula-Caixa em Flame'])


# ---------------------------------------------------------------- Parte 5 · Flame: efeitos, telas e toques
aula(
    'Flame: efeitos',
    'Muita coisa que dá vida a um jogo é movimento que começa, dura um tempo e termina: o osso que pula, o coração '
    'que pulsa, a caixa que gira quando é tocada. No Flame isso é um efeito, um componente que se coloca dentro de '
    'outro com add(). MoveEffect muda a posição, ScaleEffect a escala, RotateEffect o ângulo e OpacityEffect a '
    'transparência; .to vai até um valor e .by soma ao valor atual. Quem diz quanto tempo o efeito dura é o '
    'EffectController: duration em segundos, curve para acelerar ou frear (Curves.easeInOut, Curves.bounceOut), '
    'alternate: true para voltar ao ponto de partida e infinite: true para repetir para sempre. SequenceEffect '
    'roda uma lista de efeitos um depois do outro e chama onComplete no fim. Aqui o coração pulsa, a maçã vai e '
    'volta, e cada toque na caixa faz ela girar 90 graus e dar um pulinho.',
    'Em ▶ Testar, toque na caixa algumas vezes. Troque a curva da maçã por Curves.bounceOut, deixe o coração mais '
    'rápido e faça a caixa sumir aos poucos no fim da sequência.',
    r'''
import 'dart:math';
import 'package:flame/components.dart';
import 'package:flame/effects.dart';
import 'package:flame/events.dart';
import 'package:flame/game.dart';
import 'package:flutter/material.dart';

void main() => runApp(GameWidget(game: Vitrine()));

class Vitrine extends FlameGame {
  @override
  Future<void> onLoad() async {
    final coracao = SpriteComponent(
      sprite: await loadSprite('coracao.png'),
      size: Vector2.all(64),
      position: Vector2(size.x / 2, 130),
      anchor: Anchor.center,
    );
    add(coracao);
    coracao.add(ScaleEffect.to(
      Vector2.all(1.3),
      EffectController(duration: 0.4, alternate: true, infinite: true, curve: Curves.easeInOut),
    ));

    final maca = SpriteComponent(
      sprite: await loadSprite('maca.png'),
      size: Vector2.all(48),
      position: Vector2(70, 290),
      anchor: Anchor.center,
    );
    add(maca);
    maca.add(MoveEffect.by(
      Vector2(size.x - 140, 0),
      EffectController(duration: 1.2, alternate: true, infinite: true, curve: Curves.easeInOut),
    ));

    add(Caixa(Vector2(size.x / 2, 470)));
  }

  @override
  Color backgroundColor() => const Color(0xFF1B2A41);
}

class Caixa extends SpriteComponent with TapCallbacks, HasGameReference<Vitrine> {
  bool ocupada = false;

  Caixa(Vector2 onde) : super(position: onde, size: Vector2.all(80), anchor: Anchor.center);

  @override
  Future<void> onLoad() async {
    sprite = await game.loadSprite('caixa.png');
  }

  @override
  void onTapDown(TapDownEvent event) {
    if (ocupada) return;
    ocupada = true;
    add(SequenceEffect(
      [
        RotateEffect.by(pi / 2, EffectController(duration: 0.3, curve: Curves.easeOut)),
        MoveEffect.by(Vector2(0, -40), EffectController(duration: 0.15, alternate: true)),
      ],
      onComplete: () => ocupada = false,
    ));
  }
}
''',
    [
        ['Outra curva', 'Na maçã, troque Curves.easeInOut por Curves.bounceOut (ou outra curva).', r'MoveEffect\.by\([^;]*?curve:\s*Curves\.(?!easeInOut\b)\w+'],
        ['Coração mais rápido', 'No ScaleEffect do coração, troque duration: 0.4 por um valor menor, como 0.2.', r'ScaleEffect\.to\([^;]*?duration:\s*0?\.[0-3]\d*\s*,'],
        ['Sumir aos poucos', 'Acrescente OpacityEffect.fadeOut(EffectController(duration: 0.5)) como último item da lista do SequenceEffect. A caixa some e o próximo toque não acha mais nada.', r'OpacityEffect\.(?:fadeOut|to)\('],
    ],
    setup=SETUP_FLAME,
)

aula(
    'Flame: partículas',
    'Explosões, faíscas, poeira e fogos de artifício são feitos de muitas peças pequenas que nascem juntas, se '
    'espalham e somem. Criar um componente para cada uma seria trabalhoso; o Flame tem partículas para isso. '
    'Particle.generate cria count partículas chamando generator(i) para cada uma, e todas vivem lifespan segundos. '
    'CircleParticle desenha um círculo; AcceleratedParticle dá a ele uma velocidade inicial (speed) e uma '
    'aceleração (acceleration), que aqui faz as faíscas caírem como se houvesse gravidade. O conjunto entra no jogo '
    'dentro de um ParticleSystemComponent, que se remove sozinho quando todas as partículas acabam. Para espalhar '
    'em círculo, cada faísca sorteia um ângulo e vai na direção (cos, sin) desse ângulo.',
    'Em ▶ Testar, toque em vários pontos da tela. Dobre o número de faíscas, mude a gravidade e troque as bolinhas '
    'por coraçõezinhos com SpriteParticle.',
    r'''
import 'dart:math';
import 'package:flame/components.dart';
import 'package:flame/events.dart';
import 'package:flame/game.dart';
import 'package:flame/particles.dart';
import 'package:flame_audio/flame_audio.dart';
import 'package:flutter/material.dart';

void main() => runApp(GameWidget(game: Fogos()));

class Fogos extends FlameGame with TapCallbacks {
  final sorteio = Random();
  final cores = [Colors.amber, Colors.pinkAccent, Colors.cyanAccent, Colors.lightGreenAccent];
  late Sprite coracao;

  @override
  Future<void> onLoad() async {
    coracao = await loadSprite('coracao.png');
    add(TextComponent(text: 'Toque para soltar fogos', position: Vector2(size.x / 2, size.y - 50), anchor: Anchor.center));
    add(TimerComponent(
      period: 1.4,
      repeat: true,
      onTick: () => explodir(Vector2(40 + sorteio.nextDouble() * (size.x - 80), 100 + sorteio.nextDouble() * 220)),
    ));
  }

  @override
  void onTapDown(TapDownEvent event) {
    explodir(event.localPosition);
  }

  void explodir(Vector2 onde) {
    final cor = cores[sorteio.nextInt(cores.length)];
    add(ParticleSystemComponent(
      position: onde,
      particle: Particle.generate(
        count: 30,
        lifespan: 1.2,
        generator: (i) {
          final angulo = sorteio.nextDouble() * 2 * pi;
          final forca = 60 + sorteio.nextDouble() * 140;
          return AcceleratedParticle(
            speed: Vector2(cos(angulo), sin(angulo)) * forca,
            acceleration: Vector2(0, 160),
            child: CircleParticle(radius: 3, paint: Paint()..color = cor),
          );
        },
      ),
    ));
    FlameAudio.play('explosao.wav', volume: 0.4);
  }

  @override
  Color backgroundColor() => const Color(0xFF0B0F2A);
}
''',
    [
        ['Mais faíscas', 'Em Particle.generate, troque count: 30 por 60.', r'count:\s*(?!30\b)\d{2,}'],
        ['Outra gravidade', 'Mude a aceleração Vector2(0, 160): 0 deixa as faíscas flutuando, 400 faz cair rápido.', r'acceleration:\s*Vector2\(\s*[-\d.]+\s*,\s*(?!160\b)[-\d.]+\s*\)'],
        ['Corações', 'Troque o child por SpriteParticle(sprite: coracao, size: Vector2.all(12)). O sprite já foi carregado no onLoad.', r'SpriteParticle\(\s*sprite:\s*coracao'],
    ],
    setup=SETUP_FLAME,
)

aula(
    'Flame: paralaxe',
    'Quando você olha pela janela de um carro, as montanhas lá longe quase não se mexem e os postes perto passam '
    'voando. Repetir isso no jogo dá profundidade a um cenário 2D: é o efeito de paralaxe. loadParallaxComponent '
    'recebe as camadas da mais distante para a mais próxima (cada uma um ParallaxImageData com o nome da imagem), '
    'e cada camada se repete na horizontal para cobrir a tela. baseVelocity é a velocidade da primeira camada, em '
    'pixels por segundo, e velocityMultiplierDelta multiplica essa velocidade de uma camada para a seguinte: com '
    '1.8, as montanhas andam 1,8 vez mais rápido que o céu e as colinas 1,8 vez mais rápido que as montanhas. O chão '
    'de grama é a camada mais próxima de todas: os blocos andam no update e, ao sair pela esquerda, voltam pela '
    'direita. Cada toque troca entre andar e correr, mudando parallax.baseVelocity.',
    'Em ▶ Testar, toque na tela para o herói correr. Deixe o céu parado com baseVelocity menor, aumente a diferença '
    'entre as camadas e faça o herói correr mais rápido.',
    r'''
import 'package:flame/components.dart';
import 'package:flame/events.dart';
import 'package:flame/game.dart';
import 'package:flame/parallax.dart';
import 'package:flutter/material.dart';

void main() => runApp(GameWidget(game: Paisagem()));

class Paisagem extends FlameGame with TapCallbacks {
  late ParallaxComponent fundo;
  final List<SpriteComponent> chao = [];
  double velocidade = 30;
  final double bloco = 48;

  @override
  Future<void> onLoad() async {
    fundo = await loadParallaxComponent(
      [ParallaxImageData('ceu.png'), ParallaxImageData('montanhas.png'), ParallaxImageData('colinas.png')],
      baseVelocity: Vector2(velocidade, 0),
      velocityMultiplierDelta: Vector2(1.8, 1.0),
      size: Vector2(size.x, size.y - bloco),
    );
    add(fundo);

    final grama = await loadSprite('grama.png');
    for (int i = 0; i < size.x / bloco + 2; i++) {
      final b = SpriteComponent(sprite: grama, position: Vector2(i * bloco, size.y - bloco), size: Vector2.all(bloco));
      chao.add(b);
      add(b);
    }

    add(SpriteAnimationComponent(
      animation: await loadSpriteAnimation(
        'heroi.png',
        SpriteAnimationData.sequenced(amount: 4, stepTime: 0.12, textureSize: Vector2.all(16)),
      ),
      position: Vector2(90, size.y - bloco),
      size: Vector2.all(64),
      anchor: Anchor.bottomCenter,
    ));
  }

  @override
  void update(double dt) {
    super.update(dt);
    final vChao = velocidade * 1.8 * 1.8 * 1.8;
    for (final b in chao) {
      b.position.x -= vChao * dt;
      if (b.position.x < -bloco) {
        b.position.x += chao.length * bloco;
      }
    }
  }

  @override
  void onTapDown(TapDownEvent event) {
    velocidade = velocidade == 30 ? 90 : 30;
    fundo.parallax!.baseVelocity = Vector2(velocidade, 0);
  }
}
''',
    [
        ['Céu quase parado', 'Em loadParallaxComponent, troque baseVelocity: Vector2(velocidade, 0) por Vector2(5, 0). Repare que o toque volta a usar velocidade.', r'baseVelocity:\s*Vector2\(\s*[\d.]+\s*,'],
        ['Mais profundidade', 'Mude velocityMultiplierDelta para Vector2(2.5, 1.0). Ajuste o vChao para continuar acompanhando as colinas.', r'velocityMultiplierDelta:\s*Vector2\(\s*(?!1\.8\b)[\d.]+'],
        ['Correr mais', 'No onTapDown, troque o 90 por 150.', r'velocidade\s*==\s*30\s*\?\s*(?!90\b)\d+'],
    ],
    setup=SETUP_FLAME,
)

aula(
    'Flame: overlays, pausa e música',
    'Menus, botão de pausa e tela de fim de jogo costumam ser widgets do Flutter por cima do jogo, não componentes: '
    'eles ganham botões, textos e layout prontos. O GameWidget recebe overlayBuilderMap, um mapa de nome para uma '
    'função (context, game) que monta o widget; initialActiveOverlays diz quais aparecem no começo. Dentro do jogo, '
    'overlays.add(\'Pausa\') mostra um overlay e overlays.remove(\'Pausa\') esconde. pauseEngine() congela o update '
    'de todos os componentes e resumeEngine() volta. A música de fundo vem do FlameAudio.bgm: play começa a tocar '
    'em loop, pause e resume acompanham a pausa. O jogo em si é simples: ossos aparecem e cada toque num deles vale '
    'um ponto.',
    'Em ▶ Testar, toque em Jogar, pegue alguns ossos e use o botão de pausa. Mude o título do menu, troque a música '
    'por musica_espaco.mp3 e faça o jogo voltar ao menu quando chegar a 10 ossos.',
    r'''
import 'dart:math';
import 'package:flame/components.dart';
import 'package:flame/events.dart';
import 'package:flame/game.dart';
import 'package:flame_audio/flame_audio.dart';
import 'package:flutter/material.dart';

void main() => runApp(GameWidget(
      game: Coleta(),
      overlayBuilderMap: {
        'Menu': (BuildContext context, Coleta game) => Center(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Text('Coleta', style: TextStyle(fontSize: 40, color: Colors.white, fontWeight: FontWeight.bold)),
                  const SizedBox(height: 24),
                  ElevatedButton(onPressed: () => game.comecar(), child: const Text('Jogar')),
                ],
              ),
            ),
        'BotaoPausa': (BuildContext context, Coleta game) => Align(
              alignment: Alignment.topRight,
              child: Padding(
                padding: const EdgeInsets.all(12),
                child: ElevatedButton(onPressed: () => game.pausar(), child: const Text('Pausa')),
              ),
            ),
        'Pausa': (BuildContext context, Coleta game) => Center(
              child: Card(
                child: Padding(
                  padding: const EdgeInsets.all(24),
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      const Text('Pausado', style: TextStyle(fontSize: 24)),
                      const SizedBox(height: 16),
                      ElevatedButton(onPressed: () => game.continuar(), child: const Text('Continuar')),
                    ],
                  ),
                ),
              ),
            ),
      },
      initialActiveOverlays: const ['Menu'],
    ));

class Coleta extends FlameGame {
  final sorteio = Random();
  late TextComponent placar;
  int pontos = 0;

  @override
  Future<void> onLoad() async {
    placar = TextComponent(text: 'Ossos: 0', position: Vector2(16, 20));
    add(placar);
    add(TimerComponent(period: 0.8, repeat: true, onTick: () => add(Osso(Vector2(
      40 + sorteio.nextDouble() * (size.x - 80),
      100 + sorteio.nextDouble() * (size.y - 200),
    )))));
    pauseEngine();
  }

  void comecar() {
    overlays.remove('Menu');
    overlays.add('BotaoPausa');
    pontos = 0;
    placar.text = 'Ossos: 0';
    FlameAudio.bgm.play('musica_aventura.mp3', volume: 0.5);
    resumeEngine();
  }

  void pausar() {
    pauseEngine();
    FlameAudio.bgm.pause();
    overlays.add('Pausa');
  }

  void continuar() {
    overlays.remove('Pausa');
    FlameAudio.bgm.resume();
    resumeEngine();
  }

  void pegou() {
    pontos++;
    placar.text = 'Ossos: $pontos';
    FlameAudio.play('osso.wav');
  }

  @override
  Color backgroundColor() => const Color(0xFF2B3A67);
}

class Osso extends SpriteAnimationComponent with TapCallbacks, HasGameReference<Coleta> {
  double vida = 2.5;

  Osso(Vector2 onde) : super(position: onde, size: Vector2.all(48), anchor: Anchor.center);

  @override
  Future<void> onLoad() async {
    animation = await game.loadSpriteAnimation(
      'osso.png',
      SpriteAnimationData.sequenced(amount: 6, stepTime: 0.1, textureSize: Vector2.all(16)),
    );
  }

  @override
  void update(double dt) {
    super.update(dt);
    vida -= dt;
    if (vida <= 0) removeFromParent();
  }

  @override
  void onTapDown(TapDownEvent event) {
    game.pegou();
    removeFromParent();
  }
}
''',
    [
        ['Outro título', 'No overlay Menu, troque o texto Coleta pelo nome do seu jogo.', r"Text\(\s*'(?!Coleta')[^']+',\s*style:\s*TextStyle\(fontSize:\s*40"],
        ['Outra música', "Troque musica_aventura.mp3 por musica_espaco.mp3 (ou musica_menu.mp3).", r"bgm\.play\(\s*'musica_(?:espaco|menu)\.mp3'"],
        ['Fim aos 10', "No pegou, quando pontos chegar a 10: pauseEngine(), FlameAudio.bgm.stop(), overlays.remove('BotaoPausa') e overlays.add('Menu').", r"if\s*\(\s*pontos\s*>?=+\s*10\s*\)[\s\S]*?overlays\.add\(\s*'Menu'\s*\)"],
    ],
    lim='No simulador a música é sintetizada pelo navegador, e só começa depois do primeiro toque. As músicas prontas são musica_aventura, musica_espaco e musica_menu (.mp3).',
    setup=SETUP_FLAME,
)

aula(
    'Flame: obstáculos que giram e consultas',
    'Uma hélice girando só é um obstáculo justo se a colisão acompanhar o giro: a caixa que contorna um retângulo '
    'inclinado é bem maior que ele. No Flame, o RectangleHitbox gira junto com o componente, e a colisão é calculada '
    'com o retângulo girado de verdade. Aqui cada pá é um RectangleComponent com hitbox, e o update soma ao angle a '
    'cada quadro. Arraste a bola até a estrela do outro lado sem encostar nas pás; com debugMode ligado dá para ver '
    'os contornos girando. Para saber quantos ossos faltam, o jogo pergunta aos próprios filhos: '
    'children.query<Osso>() devolve a lista dos componentes daquele tipo (whereType<Osso>() também serve). Quando '
    'a lista fica vazia, a fase acabou.',
    'Em ▶ Testar, arraste a bola e pegue os três ossos sem bater. Ligue o debugMode, deixe as pás mais rápidas e '
    'acrescente uma terceira pá.',
    r'''
import 'dart:math';
import 'package:flame/collisions.dart';
import 'package:flame/components.dart';
import 'package:flame/events.dart';
import 'package:flame/game.dart';
import 'package:flame_audio/flame_audio.dart';
import 'package:flutter/material.dart';

void main() => runApp(GameWidget(game: Helices()));

class Helices extends FlameGame with HasCollisionDetection {
  late TextComponent aviso;

  @override
  Future<void> onLoad() async {
    debugMode = false;
    add(Pa(Vector2(size.x / 2, 220), 1.6));
    add(Pa(Vector2(size.x / 2, 440), -2.2));
    add(Osso(Vector2(60, 220)));
    add(Osso(Vector2(size.x - 60, 330)));
    add(Osso(Vector2(60, 440)));
    add(Bola(Vector2(size.x / 2, size.y - 60)));
    aviso = TextComponent(text: 'Faltam 3 ossos', position: Vector2(16, 20));
    add(aviso);
  }

  void contar() {
    final faltam = children.query<Osso>().length;
    aviso.text = faltam == 0 ? 'Você pegou todos!' : 'Faltam $faltam ossos';
    if (faltam == 0) FlameAudio.play('vitoria.wav');
  }

  @override
  Color backgroundColor() => const Color(0xFF203040);
}

class Pa extends RectangleComponent with CollisionCallbacks {
  final double giro;

  Pa(Vector2 centro, this.giro)
      : super(position: centro, size: Vector2(220, 18), anchor: Anchor.center, paint: Paint()..color = Colors.orangeAccent);

  @override
  Future<void> onLoad() async {
    add(RectangleHitbox());
  }

  @override
  void update(double dt) {
    super.update(dt);
    angle += giro * dt;
  }
}

class Osso extends CircleComponent with CollisionCallbacks, HasGameReference<Helices> {
  Osso(Vector2 onde) : super(position: onde, radius: 14, anchor: Anchor.center, paint: Paint()..color = Colors.amber);

  @override
  Future<void> onLoad() async {
    add(CircleHitbox());
  }

  @override
  void onRemove() {
    super.onRemove();
    game.contar();
  }
}

class Bola extends CircleComponent with DragCallbacks, CollisionCallbacks, HasGameReference<Helices> {
  final Vector2 inicio;

  Bola(Vector2 onde)
      : inicio = onde.clone(),
        super(position: onde, radius: 16, anchor: Anchor.center, paint: Paint()..color = Colors.lightBlueAccent);

  @override
  Future<void> onLoad() async {
    add(CircleHitbox());
  }

  @override
  void onDragUpdate(DragUpdateEvent event) {
    position += event.localDelta;
  }

  @override
  void onCollisionStart(Set<Vector2> pontos, PositionComponent other) {
    super.onCollisionStart(pontos, other);
    if (other is Pa) {
      position = inicio.clone();
      FlameAudio.play('dano.wav');
    }
    if (other is Osso) {
      other.removeFromParent();
      FlameAudio.play('osso.wav');
    }
  }
}
''',
    [
        ['Ver os contornos', 'No onLoad, troque debugMode = false por true e veja os hitboxes girando com as pás.', r'debugMode\s*=\s*true'],
        ['Pás mais rápidas', 'Aumente os giros 1.6 e -2.2 (em radianos por segundo).', r'Pa\([^;]*,\s*(?!1\.6\b)[\d.]+\)\)'],
        ['Terceira pá', 'Acrescente add(Pa(...)) com outra posição e outro giro.', r'(?:add\(\s*Pa\([\s\S]*?){3}'],
    ],
    setup=SETUP_FLAME,
)

aula(
    'Pinça: zoom com dois dedos',
    'Mapas e tabuleiros pedem zoom com dois dedos. O GestureDetector entende esse gesto pelos callbacks de escala: '
    'onScaleStart avisa que os dedos encostaram, onScaleUpdate traz details.scale (1 no começo, 2 quando a distância '
    'entre os dedos dobrou) e details.focalPointDelta (quanto o ponto entre os dedos andou), e onScaleEnd avisa que '
    'soltaram. Como scale é relativo ao começo do gesto, guardamos a escala em onScaleStart e multiplicamos. Com um '
    'dedo só, o mesmo gesto arrasta o mapa. Repare também no build: ele tem dois return. Enquanto o jogador não toca '
    'em Abrir mapa, o if devolve a tela inicial; depois, o build segue até o return do mapa. No computador, a pinça '
    'é Ctrl + roda do mouse.',
    'Em ▶ Testar, toque em Abrir mapa, arraste e use Ctrl + roda (ou dois dedos na tela de toque). Limite o zoom '
    'máximo a 3, mude o tamanho do mapa e acrescente um botão para voltar à tela inicial.',
    r'''
import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(debugShowCheckedModeBanner: false, home: Mapa()));

class Mapa extends StatefulWidget {
  const Mapa({super.key});

  @override
  State<Mapa> createState() => _MapaState();
}

class _MapaState extends State<Mapa> {
  bool aberto = false;
  double escala = 1;
  double escalaInicio = 1;
  Offset desloc = Offset.zero;

  @override
  Widget build(BuildContext context) {
    if (!aberto) {
      return Scaffold(
        backgroundColor: const Color(0xFF14213D),
        body: Center(
          child: ElevatedButton(
            onPressed: () => setState(() => aberto = true),
            child: const Text('Abrir mapa'),
          ),
        ),
      );
    }
    return Scaffold(
      appBar: AppBar(title: Text('Zoom ${escala.toStringAsFixed(1)}x')),
      body: GestureDetector(
        onScaleStart: (details) => escalaInicio = escala,
        onScaleUpdate: (details) => setState(() {
          escala = (escalaInicio * details.scale).clamp(0.5, 5.0);
          desloc += details.focalPointDelta;
        }),
        child: CustomPaint(
          size: Size.infinite,
          painter: Quadriculado(escala, desloc),
        ),
      ),
    );
  }
}

class Quadriculado extends CustomPainter {
  final double escala;
  final Offset desloc;
  Quadriculado(this.escala, this.desloc);

  @override
  void paint(Canvas canvas, Size size) {
    canvas.drawRect(Offset.zero & size, Paint()..color = const Color(0xFF7EC8F2));
    canvas.save();
    canvas.translate(size.width / 2 + desloc.dx, size.height / 2 + desloc.dy);
    canvas.scale(escala);
    const casas = 8;
    const lado = 40.0;
    for (int i = 0; i < casas; i++) {
      for (int j = 0; j < casas; j++) {
        final cor = (i + j) % 2 == 0 ? const Color(0xFF5DBB63) : const Color(0xFF3E8E41);
        canvas.drawRect(
          Rect.fromLTWH((i - casas / 2) * lado, (j - casas / 2) * lado, lado, lado),
          Paint()..color = cor,
        );
      }
    }
    canvas.drawCircle(Offset.zero, 10, Paint()..color = Colors.redAccent);
    canvas.restore();
  }

  @override
  bool shouldRepaint(Quadriculado old) => true;
}
''',
    [
        ['Zoom até 3', 'No clamp, troque 5.0 por 3.0.', r'clamp\(\s*[\d.]+\s*,\s*3(?:\.0)?\s*\)'],
        ['Mapa maior', 'Mude const casas = 8 para 12.', r'const\s+casas\s*=\s*(?!8\b)\d+'],
        ['Voltar', "Acrescente actions: [IconButton(icon: const Icon(Icons.close), onPressed: () => setState(() => aberto = false))] na AppBar.", r'setState\(\s*\(\)\s*(?:=>|\{)\s*aberto\s*=\s*false'],
    ],
    lim='No simulador, a pinça funciona com dois dedos numa tela de toque ou com Ctrl + roda do mouse. O mapa recomeça do zero quando você muda o código.',
)

PARTS.append(['Flame: efeitos', 'Parte 5 · Efeitos, telas e gestos'])

aula(
    'Projeto · Céu Agitado',
    'O último projeto junta tudo da Parte 5 num jogo de nave com rolagem lateral. O céu, as montanhas e as colinas '
    'são um fundo em paralaxe. A nave é o sprite nave.png girado 90 graus (angle = pi / 2) para apontar para a '
    'direita; como ela está girada, o arrasto usa event.canvasDelta, que vem nas coordenadas da tela, e não '
    'localDelta. Ela atira sozinha, e os inimigos chegam pela direita: pombos e caixas que giram, todos da mesma '
    'classe Inimigo, e o hitbox da caixa gira junto com ela. Tiro em inimigo vira explosão de partículas e ponto; '
    'inimigo na nave tira uma vida e a nave pisca com um OpacityEffect. O menu inicial e a tela de fim são overlays, '
    'a música é do FlameAudio.bgm e, para recomeçar, o jogo usa children.query para remover os inimigos e tiros que '
    'sobraram.',
    'Em ▶ Testar, toque em Jogar e arraste a nave para cima e para baixo. Comece com 5 vidas, faça os inimigos '
    'chegarem mais rápido e guarde o recorde para mostrar na tela de fim.',
    r'''
import 'dart:math';
import 'package:flame/collisions.dart';
import 'package:flame/components.dart';
import 'package:flame/effects.dart';
import 'package:flame/events.dart';
import 'package:flame/game.dart';
import 'package:flame/parallax.dart';
import 'package:flame/particles.dart';
import 'package:flame_audio/flame_audio.dart';
import 'package:flutter/material.dart';

void main() => runApp(GameWidget(
      game: CeuAgitado(),
      overlayBuilderMap: {
        'Menu': (BuildContext context, CeuAgitado game) => Center(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Text('Céu Agitado', style: TextStyle(fontSize: 36, color: Colors.white, fontWeight: FontWeight.bold)),
                  const SizedBox(height: 8),
                  const Text('Arraste a nave para cima e para baixo', style: TextStyle(color: Colors.white)),
                  const SizedBox(height: 24),
                  ElevatedButton(onPressed: () => game.comecar(), child: const Text('Jogar')),
                ],
              ),
            ),
        'Fim': (BuildContext context, CeuAgitado game) => Center(
              child: Card(
                child: Padding(
                  padding: const EdgeInsets.all(24),
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      const Text('Fim de jogo', style: TextStyle(fontSize: 26, fontWeight: FontWeight.bold)),
                      const SizedBox(height: 8),
                      Text('Pontos: ${game.pontos}', style: const TextStyle(fontSize: 18)),
                      const SizedBox(height: 16),
                      ElevatedButton(onPressed: () => game.comecar(), child: const Text('Jogar de novo')),
                    ],
                  ),
                ),
              ),
            ),
      },
      initialActiveOverlays: const ['Menu'],
    ));

class CeuAgitado extends FlameGame with HasCollisionDetection {
  final sorteio = Random();
  late Nave nave;
  late TextComponent placar;
  int pontos = 0;
  int vidas = 3;
  double intervalo = 1.0;
  double relogio = 0;

  @override
  Future<void> onLoad() async {
    add(await loadParallaxComponent(
      [ParallaxImageData('ceu.png'), ParallaxImageData('montanhas.png'), ParallaxImageData('colinas.png')],
      baseVelocity: Vector2(15, 0),
      velocityMultiplierDelta: Vector2(2.0, 1.0),
    ));
    nave = Nave();
    add(nave);
    placar = TextComponent(text: '', position: Vector2(16, 16), priority: 10);
    add(placar);
    add(TimerComponent(period: 0.35, repeat: true, onTick: () => add(Tiro(nave.position.clone()))));
    atualizarPlacar();
    pauseEngine();
  }

  @override
  void update(double dt) {
    super.update(dt);
    relogio += dt;
    if (relogio >= intervalo) {
      relogio = 0;
      final y = 60 + sorteio.nextDouble() * (size.y - 120);
      if (sorteio.nextBool()) {
        add(Inimigo('pombo.png', 2, 0, Vector2(size.x + 30, y)));
      } else {
        add(Inimigo('caixa.png', 1, 2.5, Vector2(size.x + 30, y)));
      }
    }
  }

  void atualizarPlacar() {
    placar.text = 'Pontos: $pontos   Vidas: $vidas';
  }

  void comecar() {
    for (final c in children.query<Inimigo>()) {
      c.removeFromParent();
    }
    for (final c in children.query<Tiro>()) {
      c.removeFromParent();
    }
    pontos = 0;
    vidas = 3;
    relogio = 0;
    nave.position = Vector2(70, size.y / 2);
    atualizarPlacar();
    overlays.remove('Menu');
    overlays.remove('Fim');
    FlameAudio.bgm.play('musica_espaco.mp3', volume: 0.4);
    resumeEngine();
  }

  void acertou(Inimigo inimigo) {
    pontos++;
    atualizarPlacar();
    explodir(inimigo.position.clone());
    FlameAudio.play('explosao.wav', volume: 0.5);
  }

  void bateu() {
    vidas--;
    atualizarPlacar();
    FlameAudio.play('dano.wav');
    nave.add(OpacityEffect.to(0.2, EffectController(duration: 0.1, alternate: true, repeatCount: 3)));
    if (vidas <= 0) {
      pauseEngine();
      FlameAudio.bgm.stop();
      FlameAudio.play('derrota.wav');
      overlays.add('Fim');
    }
  }

  void explodir(Vector2 onde) {
    add(ParticleSystemComponent(
      position: onde,
      particle: Particle.generate(
        count: 18,
        lifespan: 0.6,
        generator: (i) {
          final angulo = sorteio.nextDouble() * 2 * pi;
          return AcceleratedParticle(
            speed: Vector2(cos(angulo), sin(angulo)) * (40 + sorteio.nextDouble() * 120),
            acceleration: Vector2(0, 100),
            child: CircleParticle(radius: 2.5, paint: Paint()..color = Colors.orangeAccent),
          );
        },
      ),
    ));
  }
}

class Nave extends SpriteAnimationComponent with DragCallbacks, CollisionCallbacks, HasGameReference<CeuAgitado> {
  Nave() : super(size: Vector2.all(56), anchor: Anchor.center, angle: pi / 2, priority: 5);

  @override
  Future<void> onLoad() async {
    animation = await game.loadSpriteAnimation(
      'nave.png',
      SpriteAnimationData.sequenced(amount: 2, stepTime: 0.1, textureSize: Vector2.all(16)),
    );
    position = Vector2(70, game.size.y / 2);
    add(CircleHitbox());
  }

  @override
  void onDragUpdate(DragUpdateEvent event) {
    position.y = (position.y + event.canvasDelta.y).clamp(30.0, game.size.y - 30);
  }

  @override
  void onCollisionStart(Set<Vector2> pontos, PositionComponent other) {
    super.onCollisionStart(pontos, other);
    if (other is Inimigo) {
      other.removeFromParent();
      game.bateu();
    }
  }
}

class Tiro extends SpriteComponent with CollisionCallbacks, HasGameReference<CeuAgitado> {
  Tiro(Vector2 inicio) : super(position: inicio, size: Vector2(12, 24), anchor: Anchor.center, angle: pi / 2);

  @override
  Future<void> onLoad() async {
    sprite = await game.loadSprite('tiro.png');
    add(RectangleHitbox());
  }

  @override
  void update(double dt) {
    super.update(dt);
    position.x += 420 * dt;
    if (position.x > game.size.x + 20) removeFromParent();
  }

  @override
  void onCollisionStart(Set<Vector2> pontos, PositionComponent other) {
    super.onCollisionStart(pontos, other);
    if (other is Inimigo) {
      other.removeFromParent();
      removeFromParent();
      game.acertou(other);
    }
  }
}

class Inimigo extends SpriteAnimationComponent with CollisionCallbacks, HasGameReference<CeuAgitado> {
  final String imagem;
  final int quadros;
  final double giro;
  double velocidade = 140;

  Inimigo(this.imagem, this.quadros, this.giro, Vector2 inicio)
      : super(position: inicio, size: Vector2.all(44), anchor: Anchor.center);

  @override
  Future<void> onLoad() async {
    animation = await game.loadSpriteAnimation(
      imagem,
      SpriteAnimationData.sequenced(amount: quadros, stepTime: 0.3, textureSize: Vector2.all(16)),
    );
    if (giro == 0) {
      add(CircleHitbox());
    } else {
      add(RectangleHitbox());
    }
  }

  @override
  void update(double dt) {
    super.update(dt);
    position.x -= velocidade * dt;
    angle += giro * dt;
    if (position.x < -40) removeFromParent();
  }
}
''',
    [
        ['Cinco vidas', 'No comecar, troque vidas = 3 por vidas = 5 (e o valor inicial do campo também).', r'void\s+comecar\(\)\s*\{[\s\S]*?vidas\s*=\s*5\s*;'],
        ['Mais rápido', 'Diminua o intervalo entre inimigos (1.0) ou aumente a velocidade deles (140).', r'(?:double\s+intervalo\s*=\s*0?\.\d+\s*;|double\s+velocidade\s*=\s*(?!140\b)\d+)'],
        ['Recorde', "Crie int recorde = 0; no jogo, atualize no bateu quando pontos > recorde e mostre Text('Recorde: ${game.recorde}') no overlay Fim.", r'game\.recorde'],
    ],
    lim='No simulador, a música e os sons são sintetizados pelo navegador e só começam depois do primeiro toque. Use ▶ Testar para jogar: em ✎ Editar o jogo fica parado no menu.',
    setup=SETUP_FLAME,
)

PARTS.append(['Projeto · Céu Agitado', 'Projeto 4 · Céu Agitado'])


# ---------------------------------------------------------------- Parte 6 · Celular, física e mapas
SETUP_FORGE2D = (
    'No terminal do projeto:\n'
    '  flutter pub add flame flame_forge2d\n\n'
    'flame_forge2d já traz o Flame junto. As medidas do Forge2D são em metros: com zoom 10, cada metro vira 10 pixels '
    'na tela, e o ponto (0, 0) do mundo fica no centro.'
)
SETUP_TILED = (
    'No terminal do projeto:\n'
    '  flutter pub add flame flame_tiled\n\n'
    'O flame_tiled procura os mapas em assets/tiles/ e as imagens dos blocos em assets/images/. No pubspec.yaml:\n'
    '  assets:\n'
    '    - assets/images/\n'
    '    - assets/tiles/\n\n'
    'No simulador já existem os mapas arena.tmx (vista de cima) e fase1.tmx (plataforma), com o tileset tiles.png '
    'incorporado. Para usar um mapa seu, salve no Tiled com as camadas em CSV e o tileset incorporado, e acrescente o '
    '.tmx e a imagem dos blocos pelo botão 🖼 Sprites.'
)

aula(
    'Joystick e botões na tela',
    'Celular não tem teclado: jogos de ação usam um joystick desenhado na tela. No Flame ele é o JoystickComponent, '
    'feito de dois componentes: background, o círculo de fundo, e knob, a bolinha que segue o dedo. margin prende o '
    'joystick a um canto da tela, como um widget com Padding. A cada quadro, joystick.relativeDelta diz para onde o '
    'dedo está puxando, de -1 a 1 em cada eixo, e joystick.direction resume isso em oito direções. Multiplicar '
    'relativeDelta pela velocidade e por dt faz o herói andar mais rápido quanto mais longe do centro estiver o dedo. '
    'O HudButtonComponent é um botão de jogo: button é o desenho normal, buttonDown o desenho enquanto está apertado, '
    'e onPressed e onReleased avisam quando o dedo encosta e quando solta. Joystick e botão funcionam ao mesmo tempo, '
    'cada um com um dedo.',
    'Em ▶ Testar, arraste a bolinha do joystick com o mouse ou o dedo e pegue os ossos. Segure o botão laranja para '
    'correr. Mude a velocidade, troque as cores do joystick e mostre a direção no placar.',
    r'''
import 'dart:math';
import 'package:flame/components.dart';
import 'package:flame/game.dart';
import 'package:flame/input.dart';
import 'package:flame_audio/flame_audio.dart';
import 'package:flutter/material.dart';

void main() => runApp(GameWidget(game: Passeio()));

class Passeio extends FlameGame {
  final sorteio = Random();
  late JoystickComponent joystick;
  late Heroi heroi;
  late TextComponent placar;
  int ossos = 0;
  bool turbo = false;

  @override
  Future<void> onLoad() async {
    heroi = Heroi();
    add(heroi);
    joystick = JoystickComponent(
      knob: CircleComponent(radius: 22, paint: Paint()..color = Colors.white70),
      background: CircleComponent(radius: 60, paint: Paint()..color = Colors.white24),
      margin: const EdgeInsets.only(left: 30, bottom: 40),
    );
    add(joystick);
    add(HudButtonComponent(
      button: CircleComponent(radius: 32, paint: Paint()..color = Colors.orange),
      buttonDown: CircleComponent(radius: 32, paint: Paint()..color = Colors.deepOrange),
      margin: const EdgeInsets.only(right: 30, bottom: 64),
      onPressed: () => turbo = true,
      onReleased: () => turbo = false,
    ));
    placar = TextComponent(text: 'Ossos: 0', position: Vector2(16, 16));
    add(placar);
    novoOsso();
  }

  void novoOsso() {
    add(Osso(Vector2(40 + sorteio.nextDouble() * (size.x - 80), 80 + sorteio.nextDouble() * (size.y - 280))));
  }

  void pegou() {
    ossos++;
    placar.text = 'Ossos: $ossos';
    FlameAudio.play('osso.wav');
    novoOsso();
  }

  @override
  Color backgroundColor() => const Color(0xFF3A6B35);
}

class Heroi extends SpriteAnimationComponent with HasGameReference<Passeio> {
  Heroi() : super(size: Vector2.all(64), anchor: Anchor.center);

  @override
  Future<void> onLoad() async {
    animation = await game.loadSpriteAnimation(
      'heroi.png',
      SpriteAnimationData.sequenced(amount: 4, stepTime: 0.12, textureSize: Vector2.all(16)),
    );
    position = Vector2(game.size.x / 2, game.size.y / 2);
  }

  @override
  void update(double dt) {
    super.update(dt);
    final j = game.joystick;
    playing = !j.isIdle;
    if (j.isIdle) return;
    final velocidade = game.turbo ? 260.0 : 140.0;
    position.add(j.relativeDelta * velocidade * dt);
    position.clamp(Vector2.all(32), game.size - Vector2.all(32));
    if (j.relativeDelta.x < 0 && scale.x > 0) flipHorizontally();
    if (j.relativeDelta.x > 0 && scale.x < 0) flipHorizontally();
  }
}

class Osso extends SpriteAnimationComponent with HasGameReference<Passeio> {
  Osso(Vector2 onde) : super(position: onde, size: Vector2.all(36), anchor: Anchor.center);

  @override
  Future<void> onLoad() async {
    animation = await game.loadSpriteAnimation(
      'osso.png',
      SpriteAnimationData.sequenced(amount: 6, stepTime: 0.1, textureSize: Vector2.all(16)),
    );
  }

  @override
  void update(double dt) {
    super.update(dt);
    if (position.distanceTo(game.heroi.position) < 40) {
      removeFromParent();
      game.pegou();
    }
  }
}
''',
    [
        ['Mais rápido', 'No update do herói, troque 140.0 por 200.0.', r'turbo\s*\?\s*[\d.]+\s*:\s*(?!140(?:\.0)?\b)[\d.]+'],
        ['Outras cores', 'Troque Colors.white70 do knob por outra cor, como Colors.amber.', r'knob:\s*CircleComponent\([^\n]*Colors\.(?!white70\b)\w+'],
        ['Mostrar a direção', "No update do jogo (override void update(double dt)), escreva placar.text = 'Ossos: $ossos  ${joystick.direction.name}';", r'joystick\.direction'],
    ],
    lim='No computador, o joystick funciona arrastando com o mouse; numa tela de toque, dá para usar o joystick e o botão ao mesmo tempo, com dois dedos.',
    setup=SETUP_FLAME,
)

aula(
    'Efeitos de cor e de caminho',
    'Dois efeitos completam a caixa de ferramentas da Parte 5. ColorEffect pinta o componente com uma cor por cima '
    'do desenho: opacityTo diz quanto da cor entra (1 é tudo), e com alternate: true a cor vai e volta, o jeito '
    'clássico de mostrar que o inimigo levou um golpe. MoveAlongPathEffect move o componente ao longo de um Path, o '
    'mesmo Path do CustomPainter: moveTo, lineTo, quadraticBezierTo e addOval desenham a trilha, e o efeito anda por '
    'ela do começo ao fim no tempo do EffectController. Sem absolute: true, o caminho é somado à posição em que o '
    'componente estava. Com oriented: true, o componente gira para apontar na direção em que está andando. Aqui o '
    'gato patrulha um caminho em forma de onda e a nave dá voltas num círculo. O desenho da nave aponta para cima, e '
    'oriented gira o componente para a direção do eixo x; por isso o sprite fica dentro de um PositionComponent, já '
    'girado 90 graus.',
    'Em ▶ Testar, toque no gato para ver o efeito de cor. Troque a cor do golpe, aumente a onda do caminho e deixe a '
    'nave mais rápida.',
    r'''
import 'dart:math';
import 'package:flame/components.dart';
import 'package:flame/effects.dart';
import 'package:flame/events.dart';
import 'package:flame/game.dart';
import 'package:flutter/material.dart';

void main() => runApp(GameWidget(game: Patrulha()));

class Patrulha extends FlameGame {
  late TextComponent placar;
  int golpes = 0;

  @override
  Future<void> onLoad() async {
    placar = TextComponent(text: 'Golpes: 0', position: Vector2(16, 16));
    add(placar);

    final gato = Gato(Vector2(40, 260));
    add(gato);
    final onda = Path()
      ..moveTo(0, 0)
      ..quadraticBezierTo(70, -80, 140, 0)
      ..quadraticBezierTo(210, 80, 280, 0);
    gato.add(MoveAlongPathEffect(onda, EffectController(duration: 3, alternate: true, infinite: true)));

    final nave = PositionComponent(size: Vector2.all(48), anchor: Anchor.center);
    nave.add(SpriteAnimationComponent(
      animation: await loadSpriteAnimation(
        'nave.png',
        SpriteAnimationData.sequenced(amount: 2, stepTime: 0.1, textureSize: Vector2.all(16)),
      ),
      size: Vector2.all(48),
      position: Vector2.all(24),
      anchor: Anchor.center,
      angle: pi / 2,
    ));
    add(nave);
    final volta = Path()..addOval(Rect.fromCircle(center: Offset(size.x / 2, 470), radius: 100));
    nave.add(MoveAlongPathEffect(volta, EffectController(duration: 4, infinite: true), absolute: true, oriented: true));
  }

  @override
  Color backgroundColor() => const Color(0xFF1B2A41);
}

class Gato extends SpriteAnimationComponent with TapCallbacks, HasGameReference<Patrulha> {
  Gato(Vector2 inicio) : super(position: inicio, size: Vector2.all(56), anchor: Anchor.center);

  @override
  Future<void> onLoad() async {
    animation = await game.loadSpriteAnimation(
      'gato.png',
      SpriteAnimationData.sequenced(amount: 2, stepTime: 0.3, textureSize: Vector2.all(16)),
    );
  }

  @override
  void onTapDown(TapDownEvent event) {
    game.golpes++;
    game.placar.text = 'Golpes: ${game.golpes}';
    add(ColorEffect(Colors.red, EffectController(duration: 0.12, alternate: true, repeatCount: 2), opacityTo: 0.8));
  }
}
''',
    [
        ['Outra cor de golpe', 'No ColorEffect, troque Colors.red por Colors.white (ou outra cor).', r'ColorEffect\(\s*Colors\.(?!red\b)\w+'],
        ['Onda maior', 'No primeiro quadraticBezierTo, troque -80 por -140.', r'quadraticBezierTo\(\s*70\s*,\s*-(?!80\b)\d+'],
        ['Nave mais rápida', 'No EffectController da volta, troque duration: 4 por duration: 2.', r'MoveAlongPathEffect\(\s*volta\s*,\s*EffectController\(\s*duration:\s*(?!4\b)[\d.]+'],
    ],
    setup=SETUP_FLAME,
)

aula(
    'Forge2D: corpos, gravidade e quiques',
    'Até aqui o próprio jogo calculava a queda e a batida. Um motor de física faz isso sozinho e com mais realismo: '
    'objetos empilham, rolam, giram e quicam. O Forge2D é o Box2D, o motor de física 2D mais usado em jogos, escrito '
    'em Dart. Cada objeto é um BodyComponent, e o método createBody monta seu corpo em três partes: o BodyDef diz onde '
    'o corpo começa e de que tipo ele é (BodyType.dynamic cai e se mexe, static fica parado, como o chão); a forma '
    '(CircleShape, PolygonShape ou EdgeShape, uma linha) diz o contorno; e o FixtureDef liga a forma ao corpo com '
    'density (peso), friction (atrito) e restitution (quanto quica, de 0 a 1). As medidas são em metros, e o '
    'Forge2DGame mostra 10 pixels por metro. camera.visibleWorldRect diz quais metros cabem na tela, o que serve para '
    'pôr as paredes nas bordas. Cada toque solta uma bola nova onde o dedo encostou, convertida com screenToWorld.',
    'Em ▶ Testar, toque na tela várias vezes e veja as bolas derrubarem a torre. Deixe as bolas mais saltitantes, '
    'inverta a gravidade e faça a torre mais alta.',
    r'''
import 'dart:math';
import 'package:flame/components.dart';
import 'package:flame/events.dart';
import 'package:flame_forge2d/flame_forge2d.dart';
import 'package:flutter/material.dart';

void main() => runApp(GameWidget(game: Fisica()));

class Fisica extends Forge2DGame with TapCallbacks {
  Fisica() : super(gravity: Vector2(0, 10), zoom: 10);

  final sorteio = Random();

  @override
  Future<void> onLoad() async {
    await super.onLoad();
    final r = camera.visibleWorldRect;
    world.add(Parede(Vector2(r.left, r.bottom - 1), Vector2(r.right, r.bottom - 1)));
    world.add(Parede(Vector2(r.left + 0.5, r.top), Vector2(r.left + 0.5, r.bottom)));
    world.add(Parede(Vector2(r.right - 0.5, r.top), Vector2(r.right - 0.5, r.bottom)));
    for (int i = 0; i < 6; i++) {
      world.add(Caixa(Vector2(4, r.bottom - 2 - i * 2)));
    }
  }

  @override
  void onTapDown(TapDownEvent event) {
    world.add(Bola(screenToWorld(event.localPosition), 0.8 + sorteio.nextDouble()));
  }
}

class Parede extends BodyComponent {
  final Vector2 inicio;
  final Vector2 fim;

  Parede(this.inicio, this.fim);

  @override
  Body createBody() {
    final forma = EdgeShape()..set(inicio, fim);
    final corpo = world.createBody(BodyDef(type: BodyType.static));
    corpo.createFixture(FixtureDef(forma, friction: 0.6));
    return corpo;
  }
}

class Caixa extends BodyComponent {
  final Vector2 inicio;

  Caixa(this.inicio) : super(paint: Paint()..color = Colors.orange);

  @override
  Body createBody() {
    final forma = PolygonShape()..setAsBoxXY(1, 1);
    final corpo = world.createBody(BodyDef(position: inicio, type: BodyType.dynamic));
    corpo.createFixture(FixtureDef(forma, density: 1, friction: 0.5));
    return corpo;
  }
}

class Bola extends BodyComponent {
  final Vector2 inicio;
  final double raio;

  Bola(this.inicio, this.raio) : super(paint: Paint()..color = Colors.lightBlueAccent);

  @override
  Body createBody() {
    final forma = CircleShape()..radius = raio;
    final corpo = world.createBody(BodyDef(position: inicio, type: BodyType.dynamic));
    corpo.createFixture(FixtureDef(forma, density: 2, restitution: 0.5, friction: 0.4));
    return corpo;
  }
}
''',
    [
        ['Bolas saltitantes', 'No FixtureDef da bola, troque restitution: 0.5 por 0.9.', r'restitution:\s*0?\.(?!5\b)\d+'],
        ['Gravidade ao contrário', 'No construtor do jogo, troque Vector2(0, 10) por Vector2(0, -10). Toque e veja as bolas caírem para cima.', r'gravity:\s*Vector2\(\s*[-\d.]+\s*,\s*-\s*\d'],
        ['Torre mais alta', 'No for das caixas, troque i < 6 por i < 10.', r'i\s*<\s*(?!6\b)\d+\s*;'],
    ],
    lim='O Forge2D do simulador é uma versão simplificada do Box2D: tem corpos estáticos, dinâmicos e cinemáticos, círculos, polígonos convexos, arestas e correntes, atrito, quique, impulsos, forças e contatos, e as juntas da próxima aula, mas não tem corpos dormindo nem CCD (corpos muito rápidos podem atravessar paredes finas).',
    setup=SETUP_FORGE2D,
)

aula(
    'Forge2D: impulsos e contatos',
    'Para lançar um corpo, o Forge2D usa impulso: body.applyLinearImpulse(Vector2(...)) dá um empurrão de uma vez, '
    'como um chute, e quanto mais pesado o corpo, menos ele acelera. Aqui é um estilingue: arraste a partir da bola '
    'para trás, como quem estica um elástico, e solte. A linha mostra a mira, e o impulso é proporcional ao quanto '
    'você puxou, na direção oposta. Para saber quando um corpo bate em outro, o componente usa o mixin '
    'ContactCallbacks: beginContact(other, contact) é chamado quando os contornos se tocam, e other é o userData do '
    'outro corpo, que aqui é o próprio componente (userData: this no BodyDef). Cada alvo atingido pela bola fica '
    'verde e soma um ponto. Repare que os alvos também são dinâmicos: a batida derruba a pilha de verdade.',
    'Em ▶ Testar, puxe a bola azul para trás e solte. Aumente a força do lançamento, deixe a bola mais pesada e faça '
    'um alvo valer 2 pontos quando cair no chão.',
    r'''
import 'package:flame/components.dart';
import 'package:flame/events.dart';
import 'package:flame_forge2d/flame_forge2d.dart';
import 'package:flutter/material.dart';

void main() => runApp(GameWidget(game: Estilingue()));

class Estilingue extends Forge2DGame with DragCallbacks {
  Estilingue() : super(gravity: Vector2(0, 10), zoom: 14);

  late Bola bola;
  late TextComponent placar;
  late Vector2 base;
  Vector2 puxao = Vector2.zero();
  bool mirando = false;
  int pontos = 0;

  @override
  Future<void> onLoad() async {
    await super.onLoad();
    final r = camera.visibleWorldRect;
    final chao = r.bottom - 4;
    world.add(Chao(Vector2(r.left, chao), Vector2(r.right, chao)));
    world.add(Chao(Vector2(r.left, r.top), Vector2(r.left, chao)));
    world.add(Chao(Vector2(r.right, r.top), Vector2(r.right, chao)));
    for (int i = 0; i < 4; i++) {
      world.add(Alvo(Vector2(6, chao - 1 - i * 2.2)));
    }
    world.add(Alvo(Vector2(9.5, chao - 1)));
    base = Vector2(r.left + 4, chao - 8);
    bola = Bola(base.clone());
    world.add(bola);
    placar = TextComponent(text: 'Pontos: 0', position: Vector2(16, 16));
    camera.viewport.add(placar);
  }

  @override
  void onDragStart(DragStartEvent event) {
    super.onDragStart(event);
    mirando = true;
    puxao = Vector2.zero();
  }

  @override
  void onDragUpdate(DragUpdateEvent event) {
    puxao += event.localDelta / 10;
    if (puxao.length > 6) {
      puxao = puxao.normalized() * 6;
    }
  }

  @override
  void onDragEnd(DragEndEvent event) {
    super.onDragEnd(event);
    mirando = false;
    bola.lancar(-puxao * 30);
    puxao = Vector2.zero();
  }

  void acertou() {
    pontos++;
    placar.text = 'Pontos: $pontos';
  }

  @override
  void render(Canvas canvas) {
    super.render(canvas);
    if (mirando) {
      final inicio = worldToScreen(base);
      final fim = worldToScreen(base + puxao);
      canvas.drawLine(inicio.toOffset(), fim.toOffset(), Paint()
        ..color = Colors.white
        ..strokeWidth = 3);
    }
  }
}

class Chao extends BodyComponent {
  final Vector2 a;
  final Vector2 b;

  Chao(this.a, this.b);

  @override
  Body createBody() {
    final corpo = world.createBody(BodyDef());
    corpo.createFixture(FixtureDef(EdgeShape()..set(a, b), friction: 0.8));
    return corpo;
  }
}

class Bola extends BodyComponent {
  final Vector2 inicio;

  Bola(this.inicio) : super(paint: Paint()..color = Colors.lightBlueAccent);

  @override
  Body createBody() {
    final corpo = world.createBody(BodyDef(position: inicio, type: BodyType.static, userData: this));
    corpo.createFixture(FixtureDef(CircleShape()..radius = 1, density: 3, restitution: 0.3, friction: 0.5));
    return corpo;
  }

  void lancar(Vector2 impulso) {
    body.setType(BodyType.dynamic);
    body.applyLinearImpulse(impulso);
  }
}

class Alvo extends BodyComponent with ContactCallbacks {
  final Vector2 inicio;
  bool atingido = false;

  Alvo(this.inicio) : super(paint: Paint()..color = Colors.orange);

  @override
  Body createBody() {
    final corpo = world.createBody(BodyDef(position: inicio, type: BodyType.dynamic, userData: this));
    corpo.createFixture(FixtureDef(PolygonShape()..setAsBoxXY(1, 1), density: 1, friction: 0.6));
    return corpo;
  }

  @override
  void beginContact(Object other, Contact contact) {
    if (other is Bola && !atingido) {
      atingido = true;
      paint = Paint()..color = Colors.greenAccent;
      (game as Estilingue).acertou();
    }
  }
}
''',
    [
        ['Mais força', 'Em onDragEnd, troque -puxao * 30 por -puxao * 45.', r'lancar\(\s*-\s*puxao\s*\*\s*(?!30\b)[\d.]+'],
        ['Bola pesada', 'No FixtureDef da bola, troque density: 3 por density: 8.', r'radius\s*=\s*1\s*,\s*density:\s*(?!3\b)[\d.]+'],
        ['Ponto extra', 'No beginContact do alvo, se other for Chao, some mais um ponto com (game as Estilingue).acertou().', r'other\s+is\s+Chao'],
    ],
    setup=SETUP_FORGE2D,
)

aula(
    'Forge2D: juntas e raio',
    'Juntas (joints) prendem dois corpos um ao outro. A RevoluteJoint é um pino: os corpos giram em volta de um ponto '
    'comum, como o pêndulo, que fica pendurado num eixo estático. Com enableMotor, motorSpeed (em radianos por segundo) '
    'e maxMotorTorque, o pino vira um motor, e o catavento gira sozinho e empurra o que encontrar. A junta nasce de um '
    'JointDef: initialize(corpoA, corpoB, ponto) calcula as posições, e world.createJoint(RevoluteJoint(def)) cria a '
    'junta no mundo. Repare que o eixo é um corpo criado dentro do createBody, só para segurar a outra ponta. A '
    'MouseJoint é a junta do arrasto: ela puxa um corpo até target com uma força limitada por maxForce, e setTarget '
    'muda o alvo enquanto o dedo anda. O raio (raycast) responde à pergunta "o que existe nessa linha?": '
    'world.raycast(callback, de, até) chama reportFixture para cada contorno atravessado, com o ponto, a normal e a '
    'fração do caminho; devolver fraction faz o raio parar no mais próximo. O laser usa isso a cada quadro.',
    'Em ▶ Testar, arraste as caixas laranja com o mouse ou o dedo e jogue uma no catavento. Tire as caixas da frente do '
    'laser e veja o ponto vermelho andar. Acelere o motor, troque o pino do pêndulo por uma corda e suba o laser.',
    r'''import 'package:flame/components.dart';
import 'package:flame/events.dart';
import 'package:flame_forge2d/flame_forge2d.dart';
import 'package:flutter/material.dart';

void main() => runApp(GameWidget(game: Parque()));

class Parque extends Forge2DGame with DragCallbacks {
  Parque() : super(gravity: Vector2(0, 20), zoom: 12);

  late Chao chao;
  final caixas = <Caixa>[];
  MouseJoint? puxador;

  @override
  Future<void> onLoad() async {
    await super.onLoad();
    chao = Chao();
    await world.add(chao);
    final pendulo = Pendulo();
    await world.add(pendulo);
    await world.add(Corda(pendulo));
    await world.add(Catavento());
    for (var i = 0; i < 4; i++) {
      final caixa = Caixa(Vector2(-10 + i * 2.5, 18));
      caixas.add(caixa);
      await world.add(caixa);
    }
    await world.add(Laser());
  }

  @override
  void onDragStart(DragStartEvent event) {
    super.onDragStart(event);
    final ponto = screenToWorld(event.localPosition);
    for (final caixa in caixas) {
      if (caixa.body.position.distanceTo(ponto) < 2) {
        final def = MouseJointDef()
          ..bodyA = chao.body
          ..bodyB = caixa.body
          ..maxForce = 2000 * caixa.body.mass
          ..target.setFrom(ponto);
        puxador = MouseJoint(def);
        world.createJoint(puxador!);
        break;
      }
    }
  }

  @override
  void onDragUpdate(DragUpdateEvent event) {
    puxador?.setTarget(screenToWorld(event.canvasEndPosition));
  }

  @override
  void onDragEnd(DragEndEvent event) {
    super.onDragEnd(event);
    if (puxador != null) world.destroyJoint(puxador!);
    puxador = null;
  }
}

class Chao extends BodyComponent {
  Chao() : super(paint: Paint()..color = Colors.brown);

  @override
  Body createBody() {
    final corpo = world.createBody(BodyDef(position: Vector2(0, 24)));
    corpo.createFixture(FixtureDef(PolygonShape()..setAsBoxXY(16, 1), friction: 0.6));
    return corpo;
  }
}

class Pendulo extends BodyComponent {
  Pendulo() : super(paint: Paint()..color = Colors.indigo);

  @override
  Body createBody() {
    final eixo = world.createBody(BodyDef(position: Vector2(-8, -20)));
    final bola = world.createBody(BodyDef(position: Vector2(0, -20), type: BodyType.dynamic));
    bola.createFixture(FixtureDef(CircleShape()..radius = 1.5, density: 4));
    final def = RevoluteJointDef()..initialize(eixo, bola, eixo.position);
    world.createJoint(RevoluteJoint(def));
    return bola;
  }
}

class Corda extends Component {
  final Pendulo pendulo;
  Corda(this.pendulo);

  @override
  void render(Canvas canvas) {
    final eixo = Vector2(-8, -20);
    canvas.drawLine(eixo.toOffset(), pendulo.body.position.toOffset(), Paint()..color = Colors.white70..strokeWidth = 0.15);
    canvas.drawCircle(eixo.toOffset(), 0.4, Paint()..color = Colors.white);
  }
}

class Catavento extends BodyComponent {
  Catavento() : super(paint: Paint()..color = Colors.teal);

  @override
  Body createBody() {
    final eixo = world.createBody(BodyDef(position: Vector2(8, 6)));
    final pa = world.createBody(BodyDef(position: Vector2(8, 6), type: BodyType.dynamic));
    pa.createFixture(FixtureDef(PolygonShape()..setAsBoxXY(6, 0.5), density: 1));
    final def = RevoluteJointDef()..initialize(eixo, pa, eixo.position);
    def.enableMotor = true;
    def.motorSpeed = 2;
    def.maxMotorTorque = 3000;
    world.createJoint(RevoluteJoint(def));
    return pa;
  }
}

class Caixa extends BodyComponent {
  final Vector2 inicio;
  Caixa(this.inicio) : super(paint: Paint()..color = Colors.orange);

  @override
  Body createBody() {
    final corpo = world.createBody(BodyDef(position: inicio, type: BodyType.dynamic));
    corpo.createFixture(FixtureDef(PolygonShape()..setAsBoxXY(1, 1), density: 1, friction: 0.5));
    return corpo;
  }
}

class Mira extends RayCastCallback {
  Vector2? ponto;

  @override
  double reportFixture(Fixture fixture, Vector2 point, Vector2 normal, double fraction) {
    ponto = point.clone();
    return fraction;
  }
}

class Laser extends Component with HasGameReference<Parque> {
  final origem = Vector2(-16, 21.5);
  final fim = Vector2(16, 21.5);
  Vector2 alvo = Vector2(16, 21.5);

  @override
  void update(double dt) {
    final mira = Mira();
    game.world.raycast(mira, origem, fim);
    alvo = mira.ponto ?? fim;
  }

  @override
  void render(Canvas canvas) {
    canvas.drawLine(origem.toOffset(), alvo.toOffset(), Paint()..color = Colors.red..strokeWidth = 0.25);
    canvas.drawCircle(alvo.toOffset(), 0.5, Paint()..color = Colors.redAccent);
  }
}
''',
    [
        ['Motor mais rápido', 'No Catavento, troque def.motorSpeed = 2 por 5 (e um valor negativo gira ao contrário).', r'motorSpeed\s*=\s*(?!2\s*;)-?[\d.]+'],
        ['Pêndulo de corda', 'No Pendulo, troque a RevoluteJoint por uma DistanceJoint: final def = DistanceJointDef()..initialize(eixo, bola, eixo.position, bola.position); e world.createJoint(DistanceJoint(def)). A distância entre o eixo e a bola fica fixa, mas a bola pode girar sobre si mesma.', r'DistanceJoint\('],
        ['Laser mais alto', 'No Laser, troque o y de origem, fim e alvo de 21.5 para 19: o raio passa por cima das caixas paradas e só acerta as que você levantar.', r'origem\s*=\s*Vector2\(\s*-16\s*,\s*(?!21\.5\b)[\d.]+'],
    ],
    lim='No simulador as juntas são resolvidas por uma versão simplificada do Box2D: RevoluteJoint, WeldJoint, DistanceJoint, RopeJoint, PrismaticJoint e MouseJoint. GearJoint, PulleyJoint, WheelJoint e FrictionJoint não existem.',
    setup=SETUP_FORGE2D,
)

aula(
    'Sensores: inclinar o celular',
    'O celular sabe para que lado está inclinado graças ao acelerômetro, que mede a gravidade em cada eixo, em m/s². '
    'Deitado na mesa, ele marca x 0, y 0 e z 9,8; inclinado para a direita, x fica negativo, e com o topo para baixo, y '
    'fica negativo. O pacote sensors_plus entrega essas leituras num Stream: accelerometerEventStream(samplingPeriod: '
    'SensorInterval.gameInterval).listen(...) recebe um AccelerometerEvent com x, y e z umas 50 vezes por segundo. '
    'Aqui o listen só guarda a inclinação em ax e ay; quem move a bola é o Ticker, como na Parte 1: a inclinação '
    'vira aceleração, a aceleração muda a velocidade, e a velocidade muda a posição. Multiplicar a velocidade por 0.99 '
    'a cada quadro é o atrito, e inverter a velocidade pela metade nas bordas faz a bola quicar. Guarde a assinatura '
    '(StreamSubscription) e cancele no dispose, senão o sensor continua ligado depois que a tela fecha.',
    'Em ▶ Testar no computador, arraste a bolinha do painel 📐 Inclinar o celular e leve a bola branca até o anel. '
    'Abra o app no celular pelo endereço do site e incline o aparelho de verdade. Depois deixe a bola mais pesada, '
    'aumente o atrito e o quique.',
    r'''import 'dart:async';
import 'dart:math';
import 'package:flutter/material.dart';
import 'package:flutter/scheduler.dart';
import 'package:sensors_plus/sensors_plus.dart';

void main() => runApp(const MaterialApp(home: Inclina()));

class Inclina extends StatefulWidget {
  const Inclina({super.key});
  @override
  State<Inclina> createState() => _InclinaState();
}

class _InclinaState extends State<Inclina> with SingleTickerProviderStateMixin {
  final sorteio = Random();
  late Ticker ticker;
  StreamSubscription<AccelerometerEvent>? sensor;
  Duration anterior = Duration.zero;

  double ax = 0, ay = 0;
  double x = 160, y = 300, vx = 0, vy = 0;
  double alvoX = 80, alvoY = 120;
  int pontos = 0;

  static const raio = 18.0;
  static const largura = 360.0;
  static const altura = 600.0;

  @override
  void initState() {
    super.initState();
    sensor = accelerometerEventStream(samplingPeriod: SensorInterval.gameInterval).listen((AccelerometerEvent e) {
      ax = -e.x;
      ay = e.y;
    });
    ticker = createTicker(passo)..start();
  }

  void passo(Duration agora) {
    final dt = (agora - anterior).inMicroseconds / 1000000;
    anterior = agora;
    if (dt <= 0 || dt > 0.1) return;
    setState(() {
      vx = (vx + ax * 60 * dt) * 0.99;
      vy = (vy + ay * 60 * dt) * 0.99;
      x += vx * dt;
      y += vy * dt;
      if (x < raio) { x = raio; vx = -vx * 0.5; }
      if (x > largura - raio) { x = largura - raio; vx = -vx * 0.5; }
      if (y < raio) { y = raio; vy = -vy * 0.5; }
      if (y > altura - raio) { y = altura - raio; vy = -vy * 0.5; }
      final dx = x - alvoX, dy = y - alvoY;
      if (sqrt(dx * dx + dy * dy) < 30) {
        pontos++;
        alvoX = 40 + sorteio.nextDouble() * (largura - 80);
        alvoY = 60 + sorteio.nextDouble() * (altura - 120);
      }
    });
  }

  @override
  void dispose() {
    sensor?.cancel();
    ticker.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF14213D),
      body: Stack(children: [
        Positioned(
          left: alvoX - 30,
          top: alvoY - 30,
          child: Container(width: 60, height: 60, decoration: BoxDecoration(shape: BoxShape.circle, border: Border.all(color: Colors.amber, width: 4))),
        ),
        Positioned(
          left: x - raio,
          top: y - raio,
          child: Container(width: raio * 2, height: raio * 2, decoration: const BoxDecoration(color: Colors.white, shape: BoxShape.circle)),
        ),
        Positioned(
          left: 16,
          top: 16,
          child: Text('Pontos: $pontos   inclinação ${ax.toStringAsFixed(1)}, ${ay.toStringAsFixed(1)}', style: const TextStyle(color: Colors.white, fontSize: 16)),
        ),
      ]),
    );
  }
}
''',
    [
        ['Bola mais ágil', 'Em passo, troque ax * 60 e ay * 60 por ax * 120 e ay * 120: a mesma inclinação acelera o dobro.', r'ax\s*\*\s*(?!60\b)\d+'],
        ['Mais atrito', 'Troque os dois * 0.99 por * 0.95: a bola perde velocidade mais depressa.', r'\)\s*\*\s*(?!0\.99\b)0\.\d+\s*;'],
        ['Quique maior', 'Nas bordas, troque -vx * 0.5 e -vy * 0.5 por -vx * 0.8 e -vy * 0.8.', r'vx\s*=\s*-vx\s*\*\s*(?!0\.5\b)[\d.]+'],
    ],
    lim='No computador, o painel 📐 Inclinar o celular faz o papel do acelerômetro: arraste a bolinha ou toque em Nivelar. No celular, aberto pelo endereço do site, o simulador usa o sensor de verdade; no iPhone, toque na tela uma vez para permitir o acesso aos sensores de movimento.',
    setup='No terminal do projeto:\n  flutter pub add sensors_plus\n\nNo iPhone, acrescente NSMotionUsageDescription ao ios/Runner/Info.plist com uma frase explicando por que o jogo usa o movimento do aparelho.',
)

aula(
    'Tiled: mapas prontos',
    'Montar fase bloco por bloco no código é trabalhoso. O Tiled é um editor de mapas gratuito: você pinta os blocos '
    'numa grade, separa em camadas (chão, paredes, decoração) e marca objetos, como o ponto de partida e os ossos, '
    'numa camada de objetos. O flame_tiled lê o arquivo .tmx: TiledComponent.load(\'arena.tmx\', Vector2.all(32)) '
    'monta o mapa com cada bloco de 16 pixels desenhado com 32. Depois, mapa.tileMap.getLayer<ObjectGroup>(\'objetos\') '
    'devolve uma camada de objetos, e cada objeto tem x, y, width, height, name, type e properties, em pixels do mapa '
    '(por isso multiplicamos por 2). As paredes vêm da camada solidos: cada retângulo vira um Rect, e o herói desfaz '
    'o passo se entrar num deles. O mapa é maior que a tela, e a câmera segue o herói.',
    'Em ▶ Testar, ande pela arena com o joystick e pegue os ossos. Troque a escala dos blocos para 24, conte os ossos '
    'que faltam e troque o mapa por fase1.tmx para ver como ele é.',
    r'''
import 'package:flame/components.dart';
import 'package:flame/game.dart';
import 'package:flame/input.dart';
import 'package:flame_audio/flame_audio.dart';
import 'package:flame_tiled/flame_tiled.dart';
import 'package:flutter/material.dart';

void main() => runApp(GameWidget(game: Arena()));

class Arena extends FlameGame {
  late JoystickComponent joystick;
  late Heroi heroi;
  late TextComponent placar;
  final List<Rect> paredes = [];
  final double escala = 2;
  int ossos = 0;

  @override
  Future<void> onLoad() async {
    final mapa = await TiledComponent.load('arena.tmx', Vector2.all(16 * escala));
    world.add(mapa);

    final solidos = mapa.tileMap.getLayer<ObjectGroup>('solidos');
    for (final o in solidos!.objects) {
      paredes.add(Rect.fromLTWH(o.x * escala, o.y * escala, o.width * escala, o.height * escala));
    }
    final objetos = mapa.tileMap.getLayer<ObjectGroup>('objetos');
    for (final o in objetos!.objects) {
      final onde = Vector2(o.x * escala, o.y * escala);
      if (o.type == 'osso') {
        world.add(Osso(onde));
      } else if (o.type == 'inicio') {
        heroi = Heroi(onde);
        world.add(heroi);
      }
    }
    camera.follow(heroi);

    joystick = JoystickComponent(
      knob: CircleComponent(radius: 20, paint: Paint()..color = Colors.white70),
      background: CircleComponent(radius: 55, paint: Paint()..color = Colors.black26),
      margin: const EdgeInsets.only(left: 30, bottom: 40),
    );
    camera.viewport.add(joystick);
    placar = TextComponent(text: 'Ossos: 0', position: Vector2(16, 16));
    camera.viewport.add(placar);
  }

  bool bateu(Rect r) => paredes.any((p) => p.overlaps(r));

  @override
  Color backgroundColor() => const Color(0xFF4A5060);

  void pegou() {
    ossos++;
    placar.text = 'Ossos: $ossos';
    FlameAudio.play('osso.wav');
  }
}

class Heroi extends SpriteAnimationComponent with HasGameReference<Arena> {
  Heroi(Vector2 inicio) : super(position: inicio, size: Vector2.all(40), anchor: Anchor.center);

  @override
  Future<void> onLoad() async {
    animation = await game.loadSpriteAnimation(
      'heroi.png',
      SpriteAnimationData.sequenced(amount: 4, stepTime: 0.12, textureSize: Vector2.all(16)),
    );
  }

  Rect corpo() => Rect.fromCenter(center: position.toOffset(), width: 24, height: 28);

  @override
  void update(double dt) {
    super.update(dt);
    final j = game.joystick;
    playing = !j.isIdle;
    if (j.isIdle) return;
    final passo = j.relativeDelta * 150 * dt;
    position.x += passo.x;
    if (game.bateu(corpo())) position.x -= passo.x;
    position.y += passo.y;
    if (game.bateu(corpo())) position.y -= passo.y;
    if (passo.x < 0 && scale.x > 0) flipHorizontally();
    if (passo.x > 0 && scale.x < 0) flipHorizontally();
  }
}

class Osso extends SpriteAnimationComponent with HasGameReference<Arena> {
  Osso(Vector2 onde) : super(position: onde, size: Vector2.all(24), anchor: Anchor.center);

  @override
  Future<void> onLoad() async {
    animation = await game.loadSpriteAnimation(
      'osso.png',
      SpriteAnimationData.sequenced(amount: 6, stepTime: 0.1, textureSize: Vector2.all(16)),
    );
  }

  @override
  void update(double dt) {
    super.update(dt);
    if (position.distanceTo(game.heroi.position) < 24) {
      removeFromParent();
      game.pegou();
    }
  }
}
''',
    [
        ['Blocos menores', 'Troque final double escala = 2 por 1.5: o mapa inteiro encolhe, inclusive as paredes e os ossos.', r'double\s+escala\s*=\s*(?!2\b)[\d.]+'],
        ['Quantos faltam', "No pegou, mostre também quantos faltam: world.children.query<Osso>().length - 1 (o osso que acabou de ser pego ainda está saindo).", r'children\.query<\s*Osso\s*>\(\)'],
        ['Outro mapa', "Troque 'arena.tmx' por 'fase1.tmx', a fase de plataforma vista de lado. O herói começa no objeto inicio dela, mas anda solto pelo ar: este código não tem gravidade. As paredes da camada solidos continuam valendo.", r"TiledComponent\.load\(\s*'(?!arena\.tmx')[\w.-]+\.tmx'"],
    ],
    lim='O simulador lê mapas ortogonais e isométricos com as camadas em CSV ou base64 sem compressão e o tileset incorporado no .tmx, incluindo camadas de imagem e blocos animados. Mapas infinitos e tilesets externos (.tsx) não são lidos.',
    setup=SETUP_TILED,
)

PARTS.append(['Joystick e botões na tela', 'Parte 6 · Celular, física e mapas'])

aula(
    'Inimigos que pensam: estados',
    'Um inimigo interessante não faz sempre a mesma coisa: ele dorme, percebe o jogador, corre atrás e desiste. Cada '
    'jeito de agir é um estado, e o jeito mais claro de organizar isso é uma máquina de estados: um enum com os '
    'estados possíveis (dormindo, alerta, perseguindo, voltando), um campo com o estado atual e um switch no update '
    'que decide o que fazer em cada um e quando trocar. O gato dormindo só olha a distância; quando o caramelo chega '
    'perto, ele fica em alerta (o balão mostra !) e espera um pouco, contando o tempo em relogio. Depois persegue e, '
    'se arranhar ou se o caramelo fugir para longe, volta para casa e dorme de novo. O método mudar troca o estado, '
    'zera o relógio e atualiza o balão, que é um TextComponent filho do gato e por isso anda junto com ele. No '
    'switch do Dart 3, cada case termina sozinho, sem break.',
    'Em ▶ Testar, ande com o joystick perto dos gatos e veja os balões: Zzz, !, perseguição e ? na volta. Deixe o sono '
    'mais leve, encurte o susto e faça o gato desistir mais cedo.',
    r'''
import 'package:flame/components.dart';
import 'package:flame/effects.dart';
import 'package:flame/game.dart';
import 'package:flutter/material.dart';

void main() => runApp(GameWidget(game: Quintal()));

enum EstadoGato { dormindo, alerta, perseguindo, voltando }

class Quintal extends FlameGame {
  late JoystickComponent joystick;
  late Heroi heroi;
  late TextComponent placar;
  int arranhoes = 0;

  @override
  Future<void> onLoad() async {
    joystick = JoystickComponent(
      knob: CircleComponent(radius: 20, paint: Paint()..color = Colors.white70),
      background: CircleComponent(radius: 55, paint: Paint()..color = Colors.black26),
      margin: const EdgeInsets.only(left: 30, bottom: 40),
    );
    camera.viewport.add(joystick);
    placar = TextComponent(
      text: 'Arranhões: 0',
      position: Vector2(12, 12),
      textRenderer: TextPaint(style: const TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
    );
    camera.viewport.add(placar);
    heroi = Heroi(Vector2(0, 160));
    world.add(heroi);
    world.add(Gato(Vector2(-110, -150)));
    world.add(Gato(Vector2(110, -40)));
    world.add(Gato(Vector2(-90, 60)));
  }

  void arranhado() {
    arranhoes++;
    placar.text = 'Arranhões: $arranhoes';
  }

  @override
  Color backgroundColor() => const Color(0xFF3E6B3A);
}

class Heroi extends SpriteAnimationComponent with HasGameReference<Quintal> {
  Heroi(Vector2 inicio) : super(position: inicio, size: Vector2.all(40), anchor: Anchor.center, priority: 2);

  @override
  Future<void> onLoad() async {
    animation = await game.loadSpriteAnimation(
      'heroi.png',
      SpriteAnimationData.sequenced(amount: 4, stepTime: 0.12, textureSize: Vector2.all(16)),
    );
  }

  @override
  void update(double dt) {
    super.update(dt);
    final j = game.joystick;
    playing = !j.isIdle;
    if (j.isIdle) return;
    position += j.relativeDelta * 150 * dt;
    if (j.relativeDelta.x < -0.1 && scale.x > 0) flipHorizontally();
    if (j.relativeDelta.x > 0.1 && scale.x < 0) flipHorizontally();
  }
}

class Gato extends SpriteAnimationComponent with HasGameReference<Quintal> {
  final Vector2 casa;
  EstadoGato estado = EstadoGato.dormindo;
  double relogio = 0;
  late TextComponent balao;

  Gato(Vector2 onde)
      : casa = onde.clone(),
        super(position: onde, size: Vector2.all(36), anchor: Anchor.center);

  @override
  Future<void> onLoad() async {
    animation = await game.loadSpriteAnimation(
      'gato.png',
      SpriteAnimationData.sequenced(amount: 2, stepTime: 0.4, textureSize: Vector2.all(16)),
    );
    balao = TextComponent(
      text: 'Zzz',
      position: Vector2(18, -4),
      anchor: Anchor.bottomCenter,
      textRenderer: TextPaint(style: const TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold)),
    );
    add(balao);
  }

  void mudar(EstadoGato novo) {
    estado = novo;
    relogio = 0;
    switch (novo) {
      case EstadoGato.dormindo:
        balao.text = 'Zzz';
      case EstadoGato.alerta:
        balao.text = '!';
      case EstadoGato.perseguindo:
        balao.text = '';
      case EstadoGato.voltando:
        balao.text = '?';
    }
  }

  void irPara(Vector2 alvo, double velocidade, double dt) {
    final rumo = alvo - position;
    if (rumo.length < 2) return;
    rumo.normalize();
    position += rumo * velocidade * dt;
  }

  @override
  void update(double dt) {
    super.update(dt);
    relogio += dt;
    final distancia = position.distanceTo(game.heroi.position);
    switch (estado) {
      case EstadoGato.dormindo:
        if (distancia < 120) mudar(EstadoGato.alerta);
      case EstadoGato.alerta:
        if (relogio > 0.6) mudar(EstadoGato.perseguindo);
      case EstadoGato.perseguindo:
        irPara(game.heroi.position, 95, dt);
        if (distancia < 28) {
          game.arranhado();
          game.heroi.add(ColorEffect(Colors.red, EffectController(duration: 0.1, alternate: true, repeatCount: 3), opacityTo: 0.8));
          mudar(EstadoGato.voltando);
        } else if (distancia > 240) {
          mudar(EstadoGato.voltando);
        }
      case EstadoGato.voltando:
        irPara(casa, 60, dt);
        if (position.distanceTo(casa) < 3) mudar(EstadoGato.dormindo);
    }
  }
}
''',
    [
        ['Sono mais leve', 'No estado dormindo, troque distancia < 120 por 180: o gato acorda de mais longe.', r'distancia\s*<\s*(?!120\b)\d+\)\s*mudar\(\s*EstadoGato\.alerta'],
        ['Susto mais curto', 'No estado alerta, troque relogio > 0.6 por 0.2.', r'relogio\s*>\s*(?!0\.6\b)[\d.]+'],
        ['Gato que desiste', 'No estado perseguindo, troque distancia > 240 por 160.', r'distancia\s*>\s*(?!240\b)\d+'],
    ],
)

aula(
    'Salvar o jogo: recorde com Hive',
    'Quando o app fecha, as variáveis somem. Para guardar o recorde, o jogo precisa gravar no aparelho. O Hive é um '
    'banco simples de chave e valor: Hive.initFlutter() prepara o armazenamento, Hive.openBox(\'jogo\') abre (ou '
    'cria) uma caixa, e depois Hive.box(\'jogo\') devolve a mesma caixa em qualquer lugar. caixa.get(\'recorde\', '
    'defaultValue: 0) lê o valor, com 0 quando ainda não existe, e caixa.put(\'recorde\', recorde) grava. O jogo é '
    'rápido: em 10 segundos, toque no maior número de ossos. No initState o recorde é lido da caixa; no fim da '
    'partida, se os pontos passaram do recorde, ele é gravado. Feche e abra o app, ou mude de aula e volte: o '
    'recorde continua lá.',
    'Em ▶ Testar, jogue duas partidas e veja o recorde ficar guardado. Deixe a partida com 15 segundos, conte quantas '
    'partidas já foram jogadas e crie um botão que apaga o recorde.',
    r'''
import 'dart:async';
import 'dart:math';
import 'package:flutter/material.dart';
import 'package:hive_flutter/hive_flutter.dart';

Future<void> main() async {
  await Hive.initFlutter();
  await Hive.openBox('jogo');
  runApp(const MaterialApp(home: Relampago()));
}

class Relampago extends StatefulWidget {
  const Relampago({super.key});
  @override
  State<Relampago> createState() => _RelampagoState();
}

class _RelampagoState extends State<Relampago> {
  final caixa = Hive.box('jogo');
  final sorteio = Random();
  Timer? relogio;
  int pontos = 0;
  int restante = 0;
  int recorde = 0;
  bool novoRecorde = false;
  Offset osso = const Offset(150, 300);

  @override
  void initState() {
    super.initState();
    recorde = caixa.get('recorde', defaultValue: 0);
  }

  void comecar() {
    setState(() {
      pontos = 0;
      restante = 10;
      novoRecorde = false;
      sortear();
    });
    relogio = Timer.periodic(const Duration(seconds: 1), (t) {
      setState(() => restante--);
      if (restante == 0) terminar();
    });
  }

  void sortear() {
    osso = Offset(20 + sorteio.nextDouble() * 280, 120 + sorteio.nextDouble() * 380);
  }

  void pegou() {
    if (restante == 0) return;
    setState(() {
      pontos++;
      sortear();
    });
  }

  void terminar() {
    relogio?.cancel();
    if (pontos > recorde) {
      recorde = pontos;
      novoRecorde = true;
      caixa.put('recorde', recorde);
    }
    setState(() {});
  }

  @override
  void dispose() {
    relogio?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final jogando = restante > 0;
    return Scaffold(
      backgroundColor: const Color(0xFF3E6B3A),
      body: Stack(children: [
        Positioned(
          left: 16,
          top: 16,
          child: Text('Pontos: $pontos   Tempo: $restante   Recorde: $recorde',
              style: const TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
        ),
        if (jogando)
          Positioned(
            left: osso.dx,
            top: osso.dy,
            child: GestureDetector(
              onTapDown: (_) => pegou(),
              child: const Text('🦴', style: TextStyle(fontSize: 44)),
            ),
          ),
        if (!jogando)
          Center(
            child: Column(mainAxisSize: MainAxisSize.min, children: [
              Text(novoRecorde ? 'Novo recorde: $recorde!' : 'Recorde: $recorde',
                  style: const TextStyle(color: Colors.white, fontSize: 28, fontWeight: FontWeight.bold)),
              const SizedBox(height: 16),
              ElevatedButton(onPressed: comecar, child: const Text('Jogar')),
            ]),
          ),
      ]),
    );
  }
}
''',
    [
        ['Partida de 15 segundos', 'No comecar, troque restante = 10 por 15.', r'pontos\s*=\s*0;\s*restante\s*=\s*(?!10\b)\d+\s*;'],
        ['Contar partidas', "No terminar, leia caixa.get('partidas', defaultValue: 0), some 1 e grave com caixa.put('partidas', ...).", r"caixa\.put\(\s*'partidas'"],
        ['Apagar o recorde', "Crie um TextButton que chama caixa.delete('recorde') e zera recorde dentro do setState.", r"caixa\.delete\(\s*'recorde'\s*\)"],
    ],
    setup='No terminal do projeto:\n  flutter pub add hive_flutter\n\nO Hive guarda os dados num arquivo do próprio celular, sem servidor. No simulador as caixas ficam guardadas neste navegador, e ↺ Reiniciar apaga tudo.',
)

aula(
    'Ranking online com Supabase',
    'O Hive guarda o recorde só no aparelho. Para comparar com os colegas, os pontos precisam ir para um servidor. O '
    'Supabase é um banco Postgres na nuvem com um pacote para Flutter: Supabase.initialize liga o app ao projeto, e '
    'supabase.from(\'placar\') aponta para a tabela. insert({...}) grava uma linha nova, com o nome e os pontos; '
    'como pode falhar (sem internet, por exemplo), ele fica num try com on PostgrestException. O ranking usa '
    'stream(primaryKey: [\'id\']): é um Stream que manda a lista inteira de novo sempre que a tabela muda, então o '
    'StreamBuilder redesenha sozinho quando alguém joga. order(\'pontos\', ascending: false) deixa os maiores primeiro '
    'e limit(5) pega só os cinco melhores.',
    'Em ▶ Testar, escreva seu nome, jogue algumas partidas e veja o ranking mudar. Mostre os dez melhores, impeça '
    'enviar sem nome e crie um filtro que mostra só as suas partidas.',
    r'''
import 'dart:async';
import 'dart:math';
import 'package:flutter/material.dart';
import 'package:supabase_flutter/supabase_flutter.dart';

Future<void> main() async {
  await Supabase.initialize(url: 'https://SEU-PROJETO.supabase.co', anonKey: 'SUA-CHAVE-ANON');
  runApp(const MaterialApp(home: Ranking()));
}

final supabase = Supabase.instance.client;

class Ranking extends StatefulWidget {
  const Ranking({super.key});
  @override
  State<Ranking> createState() => _RankingState();
}

class _RankingState extends State<Ranking> {
  final sorteio = Random();
  final nome = TextEditingController(text: 'Caramelo');
  Timer? relogio;
  int pontos = 0;
  int restante = 0;
  String aviso = '';
  Offset osso = const Offset(150, 300);

  void comecar() {
    setState(() {
      pontos = 0;
      restante = 10;
      aviso = '';
      sortear();
    });
    relogio = Timer.periodic(const Duration(seconds: 1), (t) {
      setState(() => restante--);
      if (restante == 0) terminar();
    });
  }

  void sortear() {
    osso = Offset(20 + sorteio.nextDouble() * 280, 160 + sorteio.nextDouble() * 300);
  }

  void pegou() {
    if (restante == 0) return;
    setState(() {
      pontos++;
      sortear();
    });
  }

  Future<void> terminar() async {
    relogio?.cancel();
    try {
      await supabase.from('placar').insert({'nome': nome.text, 'pontos': pontos});
      setState(() => aviso = 'Enviado: $pontos pontos');
    } on PostgrestException catch (e) {
      setState(() => aviso = 'Erro: ${e.message}');
    }
  }

  @override
  void dispose() {
    relogio?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final jogando = restante > 0;
    return Scaffold(
      backgroundColor: const Color(0xFF14213D),
      body: Stack(children: [
        Positioned(
          left: 16,
          top: 16,
          child: Text('Pontos: $pontos   Tempo: $restante', style: const TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
        ),
        if (jogando)
          Positioned(
            left: osso.dx,
            top: osso.dy,
            child: GestureDetector(onTapDown: (_) => pegou(), child: const Text('🦴', style: TextStyle(fontSize: 44))),
          ),
        if (!jogando)
          Positioned(
            left: 24,
            right: 24,
            top: 60,
            child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
              TextField(controller: nome, style: const TextStyle(color: Colors.white), decoration: const InputDecoration(labelText: 'Seu nome', labelStyle: TextStyle(color: Colors.white70))),
              const SizedBox(height: 12),
              ElevatedButton(onPressed: comecar, child: const Text('Jogar')),
              const SizedBox(height: 8),
              Text(aviso, style: const TextStyle(color: Colors.amber)),
              const SizedBox(height: 16),
              const Text('Ranking', style: TextStyle(color: Colors.white, fontSize: 22, fontWeight: FontWeight.bold)),
              StreamBuilder<List<Map<String, dynamic>>>(
                stream: supabase.from('placar').stream(primaryKey: ['id']).order('pontos', ascending: false).limit(5),
                builder: (context, snapshot) {
                  if (!snapshot.hasData) return const Text('Carregando...', style: TextStyle(color: Colors.white70));
                  final linhas = snapshot.data!;
                  if (linhas.isEmpty) return const Text('Ninguém jogou ainda.', style: TextStyle(color: Colors.white70));
                  return Column(children: [
                    for (final linha in linhas)
                      ListTile(
                        leading: Text('${linhas.indexOf(linha) + 1}º', style: const TextStyle(color: Colors.amber, fontSize: 18)),
                        title: Text('${linha['nome']}', style: const TextStyle(color: Colors.white)),
                        trailing: Text('${linha['pontos']}', style: const TextStyle(color: Colors.white, fontSize: 18)),
                      ),
                  ]);
                },
              ),
            ]),
          ),
      ]),
    );
  }
}
''',
    [
        ['Top 10', 'No stream do ranking, troque limit(5) por limit(10).', r'\.limit\(\s*(?!5\b)\d+\s*\)'],
        ['Nome obrigatório', "No terminar, se nome.text.trim().isEmpty, mostre o aviso 'Escreva seu nome' e não envie.", r'nome\.text\.trim\(\)\.isEmpty'],
        ['Só as suas partidas', "No stream, acrescente .eq('nome', nome.text) logo depois de stream(primaryKey: ['id']).", r"\.eq\(\s*'nome'"],
    ],
    lim='No simulador o Supabase é de mentira: a tabela placar fica guardada neste navegador e o stream só mostra as partidas jogadas aqui. Com o pacote de verdade e o seu projeto do Supabase, o ranking é o mesmo para todo mundo.',
    setup='No terminal do projeto:\n  flutter pub add supabase_flutter\n\nNo painel do Supabase (supabase.com), crie um projeto e rode no SQL Editor:\n  create table placar (id bigint generated always as identity primary key, nome text, pontos int, created_at timestamptz default now());\n  alter table placar enable row level security;\n  create policy "todos leem" on placar for select using (true);\n  create policy "todos gravam" on placar for insert with check (true);\n  alter publication supabase_realtime add table placar;\n\nDepois troque url e anonKey no main pelos do seu projeto (Project Settings > API). No simulador o Supabase é de mentira: a tabela fica neste navegador e já funciona sem configurar nada.',
)

aula(
    'Projeto · Caça-Ossos',
    'O último projeto junta a Parte 6 num jogo completo para celular. O caramelo anda pela arena com o joystick e '
    'precisa pegar todos os ossos de duas fases, arena.tmx e arena2.tmx, que vêm do Tiled: as paredes saem da camada '
    'solidos, e os ossos, o ponto de partida e os gatos saem da camada objetos. Cada osso vale 1 ponto e devolve uma '
    'vida (até maxVidas); o osso dourado vale 5 e enche todas as vidas. Quando faltam chega a zero, proximaFase limpa '
    'o mundo e monta o próximo mapa. Os gatos são uma máquina de estados (enum EstadoGato): descansando, patrulhando '
    'de parede em parede, perseguindo quando o caramelo chega a menos de 150 pixels (o rumo é alvo - position com '
    'normalize) e assustados. Parado, o caramelo senta e abana o rabo (a animação troca para sentado). O botão do cachorro latindo é um HudButtonComponent: latir assusta os gatos a menos de '
    '170 pixels, que fogem por 2,5 segundos, e depois espera 3 segundos para latir de novo. Encostar num gato tira '
    'uma vida e pinta o caramelo de vermelho. O placar é um overlay com ValueListenableBuilder, e o recorde fica '
    'guardado com Hive: no fim, se os pontos passaram do recorde, caixa.put grava o valor novo.',
    'Em ▶ Testar, pegue todos os ossos das duas fases. Use o latido quando um gato chegar perto. Dê 5 vidas ao '
    'caramelo, deixe os gatos mais rápidos, aumente o alcance do latido e faça o osso dourado valer 10.',
    r'''
import 'package:flame/components.dart';
import 'package:flame/effects.dart';
import 'package:flame/game.dart';
import 'package:flame/input.dart';
import 'package:flame_audio/flame_audio.dart';
import 'package:flame_tiled/flame_tiled.dart';
import 'package:flutter/material.dart';
import 'package:hive_flutter/hive_flutter.dart';

Future<void> main() async {
  await Hive.initFlutter();
  await Hive.openBox('caca_ossos');
  runApp(GameWidget(
    game: CacaOssos(),
    overlayBuilderMap: {
      'Placar': (BuildContext context, CacaOssos game) => Align(
            alignment: Alignment.topLeft,
            child: Padding(
              padding: const EdgeInsets.all(12),
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  ValueListenableBuilder<int>(
                    valueListenable: game.pontos,
                    builder: (context, valor, child) => Text('Pontos: $valor', style: const TextStyle(color: Colors.white, fontSize: 18)),
                  ),
                  const SizedBox(width: 12),
                  ValueListenableBuilder<int>(
                    valueListenable: game.vidas,
                    builder: (context, valor, child) => Text('Vidas: $valor', style: const TextStyle(color: Colors.white, fontSize: 18)),
                  ),
                  const SizedBox(width: 12),
                  ValueListenableBuilder<int>(
                    valueListenable: game.fase,
                    builder: (context, valor, child) => Text('Fase: $valor', style: const TextStyle(color: Colors.white, fontSize: 18)),
                  ),
                ],
              ),
            ),
          ),
      'Fim': (BuildContext context, CacaOssos game) => Center(
            child: Card(
              child: Padding(
                padding: const EdgeInsets.all(24),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Text(game.mensagem, textAlign: TextAlign.center, style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
                    const SizedBox(height: 16),
                    ElevatedButton(onPressed: () => game.recomecar(), child: const Text('Jogar de novo')),
                  ],
                ),
              ),
            ),
          ),
    },
    initialActiveOverlays: const ['Placar'],
  ));
}

class CacaOssos extends FlameGame {
  final caixa = Hive.box('caca_ossos');
  final pontos = ValueNotifier<int>(0);
  final vidas = ValueNotifier<int>(3);
  final fase = ValueNotifier<int>(1);
  final mapas = ['arena.tmx', 'arena2.tmx'];
  final List<Rect> paredes = [];
  final double escala = 2;
  int maxVidas = 3;
  int recorde = 0;
  int faltam = 0;
  double esperaLatido = 0;
  String mensagem = '';
  late JoystickComponent joystick;
  late Heroi heroi;

  @override
  Future<void> onLoad() async {
    recorde = caixa.get('recorde', defaultValue: 0);
    joystick = JoystickComponent(
      knob: CircleComponent(radius: 20, paint: Paint()..color = Colors.white70),
      background: CircleComponent(radius: 55, paint: Paint()..color = Colors.black26),
      margin: const EdgeInsets.only(left: 30, bottom: 40),
    );
    camera.viewport.add(joystick);
    final icone = await loadSprite('caramelo_latindo.png', srcPosition: Vector2(16, 0), srcSize: Vector2.all(16));
    camera.viewport.add(HudButtonComponent(
      button: SpriteComponent(sprite: icone, size: Vector2.all(64)),
      buttonDown: SpriteComponent(sprite: icone, size: Vector2.all(56)),
      margin: const EdgeInsets.only(right: 30, bottom: 50),
      onPressed: latir,
    ));
    vidas.value = maxVidas;
    await montar();
    FlameAudio.bgm.play('musica_aventura.mp3', volume: 0.4);
  }

  Future<void> montar() async {
    paredes.clear();
    faltam = 0;
    final mapa = await TiledComponent.load(mapas[fase.value - 1], Vector2.all(16 * escala));
    world.add(mapa);
    for (final o in mapa.tileMap.getLayer<ObjectGroup>('solidos')!.objects) {
      paredes.add(Rect.fromLTWH(o.x * escala, o.y * escala, o.width * escala, o.height * escala));
    }
    for (final o in mapa.tileMap.getLayer<ObjectGroup>('objetos')!.objects) {
      final onde = Vector2(o.x * escala, o.y * escala);
      if (o.type == 'osso' || o.type == 'dourado') {
        world.add(Osso(onde, o.type == 'dourado'));
        faltam++;
      } else if (o.type == 'inimigo') {
        world.add(Gato(onde));
      } else if (o.type == 'inicio') {
        heroi = Heroi(onde);
        world.add(heroi);
      }
    }
    camera.follow(heroi);
  }

  bool bateu(Rect r) => paredes.any((p) => p.overlaps(r));

  void latir() {
    if (esperaLatido > 0) return;
    esperaLatido = 3;
    heroi.latir();
    FlameAudio.play('latido.wav');
    for (final gato in world.children.query<Gato>()) {
      if (gato.position.distanceTo(heroi.position) < 170) gato.mudar(EstadoGato.assustado);
    }
  }

  void pegou(Osso osso) {
    pontos.value += osso.dourado ? 5 : 1;
    if (osso.dourado) {
      vidas.value = maxVidas;
      heroi.curar();
      FlameAudio.play('poder.wav');
    } else if (vidas.value < maxVidas) {
      vidas.value++;
      heroi.curar();
      FlameAudio.play('poder.wav');
    } else {
      FlameAudio.play('osso.wav');
    }
    faltam--;
    if (faltam == 0) proximaFase();
  }

  Future<void> proximaFase() async {
    if (fase.value == mapas.length) {
      terminar('Você venceu!', 'vitoria.wav');
      return;
    }
    FlameAudio.play('vitoria.wav');
    fase.value++;
    world.removeAll(world.children.toList());
    await montar();
  }

  void ferido() {
    vidas.value--;
    FlameAudio.play('dano.wav');
    if (vidas.value <= 0) terminar('Fim de jogo', 'derrota.wav');
  }

  void terminar(String texto, String som) {
    if (pontos.value > recorde) {
      recorde = pontos.value;
      caixa.put('recorde', recorde);
      texto = '$texto\nNovo recorde!';
    }
    mensagem = '$texto\nPontos: ${pontos.value}   Recorde: $recorde';
    FlameAudio.play(som);
    pauseEngine();
    overlays.add('Fim');
  }

  Future<void> recomecar() async {
    overlays.remove('Fim');
    pontos.value = 0;
    vidas.value = maxVidas;
    fase.value = 1;
    world.removeAll(world.children.toList());
    await montar();
    resumeEngine();
  }

  @override
  void update(double dt) {
    super.update(dt);
    if (esperaLatido > 0) esperaLatido -= dt;
  }

  @override
  Color backgroundColor() => const Color(0xFF4A5060);
}

class Heroi extends SpriteAnimationComponent with HasGameReference<CacaOssos> {
  double protegido = 0;
  double latindo = 0;
  late SpriteAnimation andando;
  late SpriteAnimation latido;
  late SpriteAnimation sentado;

  Heroi(Vector2 inicio) : super(position: inicio, size: Vector2.all(40), anchor: Anchor.center, priority: 2);

  @override
  Future<void> onLoad() async {
    andando = await game.loadSpriteAnimation(
      'heroi.png',
      SpriteAnimationData.sequenced(amount: 4, stepTime: 0.12, textureSize: Vector2.all(16)),
    );
    latido = await game.loadSpriteAnimation(
      'caramelo_latindo.png',
      SpriteAnimationData.sequenced(amount: 2, stepTime: 0.1, textureSize: Vector2.all(16)),
    );
    sentado = await game.loadSpriteAnimation(
      'caramelo_sentado.png',
      SpriteAnimationData.sequenced(amount: 2, stepTime: 0.4, textureSize: Vector2.all(16)),
    );
    animation = sentado;
  }

  Rect corpo() => Rect.fromCenter(center: position.toOffset(), width: 24, height: 28);

  void latir() {
    latindo = 0.5;
    animation = latido;
  }

  void levarDano() {
    if (protegido > 0) return;
    protegido = 1;
    add(ColorEffect(Colors.red, EffectController(duration: 0.1, alternate: true, repeatCount: 4), opacityTo: 0.8));
    game.ferido();
  }

  void curar() {
    add(ColorEffect(Colors.lightGreenAccent, EffectController(duration: 0.15, alternate: true, repeatCount: 2), opacityTo: 0.7));
  }

  @override
  void update(double dt) {
    super.update(dt);
    if (protegido > 0) protegido -= dt;
    if (latindo > 0) latindo -= dt;
    final j = game.joystick;
    if (latindo <= 0) animation = j.isIdle ? sentado : andando;
    if (j.isIdle) return;
    final passo = j.relativeDelta * 150 * dt;
    position.x += passo.x;
    if (game.bateu(corpo())) position.x -= passo.x;
    position.y += passo.y;
    if (game.bateu(corpo())) position.y -= passo.y;
    if (passo.x < -0.1 && scale.x > 0) flipHorizontally();
    if (passo.x > 0.1 && scale.x < 0) flipHorizontally();
  }
}

class Osso extends SpriteAnimationComponent with HasGameReference<CacaOssos> {
  final bool dourado;
  Osso(Vector2 onde, this.dourado) : super(position: onde, size: Vector2.all(24), anchor: Anchor.center);

  @override
  Future<void> onLoad() async {
    animation = await game.loadSpriteAnimation(
      dourado ? 'osso_dourado.png' : 'osso.png',
      SpriteAnimationData.sequenced(amount: 6, stepTime: 0.1, textureSize: Vector2.all(16)),
    );
  }

  @override
  void update(double dt) {
    super.update(dt);
    if (position.distanceTo(game.heroi.position) < 24) {
      removeFromParent();
      game.pegou(this);
    }
  }
}

enum EstadoGato { descansando, patrulhando, perseguindo, assustado }

class Gato extends SpriteAnimationComponent with HasGameReference<CacaOssos> {
  double velocidade = 90;
  double visao = 150;
  double direcao = 1;
  EstadoGato estado = EstadoGato.descansando;
  double relogio = 0;
  late TextComponent balao;

  Gato(Vector2 onde) : super(position: onde, size: Vector2.all(36), anchor: Anchor.center);

  @override
  Future<void> onLoad() async {
    animation = await game.loadSpriteAnimation(
      'gato.png',
      SpriteAnimationData.sequenced(amount: 2, stepTime: 0.3, textureSize: Vector2.all(16)),
    );
    balao = TextComponent(
      text: 'Zzz',
      position: Vector2(18, -2),
      anchor: Anchor.bottomCenter,
      textRenderer: TextPaint(style: const TextStyle(color: Colors.white, fontSize: 14, fontWeight: FontWeight.bold)),
    );
    add(balao);
  }

  Rect corpo() => Rect.fromCenter(center: position.toOffset(), width: 24, height: 24);

  void mudar(EstadoGato novo) {
    estado = novo;
    relogio = 0;
    switch (novo) {
      case EstadoGato.descansando:
        balao.text = 'Zzz';
      case EstadoGato.patrulhando:
        balao.text = '';
      case EstadoGato.perseguindo:
        balao.text = '!';
      case EstadoGato.assustado:
        balao.text = 'Fsss!';
    }
  }

  void andar(Vector2 passo) {
    position.x += passo.x;
    if (game.bateu(corpo())) {
      position.x -= passo.x;
      direcao = -direcao;
    }
    position.y += passo.y;
    if (game.bateu(corpo())) position.y -= passo.y;
  }

  @override
  void update(double dt) {
    super.update(dt);
    relogio += dt;
    final alvo = game.heroi.position;
    final distancia = position.distanceTo(alvo);
    switch (estado) {
      case EstadoGato.descansando:
        if (relogio > 2) mudar(EstadoGato.patrulhando);
      case EstadoGato.patrulhando:
        andar(Vector2(direcao * velocidade * 0.6 * dt, 0));
        if (distancia < visao) mudar(EstadoGato.perseguindo);
      case EstadoGato.perseguindo:
        final rumo = (alvo - position)..normalize();
        andar(rumo * velocidade * dt);
        if (distancia > visao * 1.6) mudar(EstadoGato.patrulhando);
        if (distancia < 30) {
          game.heroi.levarDano();
          mudar(EstadoGato.descansando);
        }
      case EstadoGato.assustado:
        final fuga = (position - alvo)..normalize();
        andar(fuga * velocidade * 1.3 * dt);
        if (relogio > 2.5) mudar(EstadoGato.patrulhando);
    }
  }
}
''',
    [
        ['Cinco vidas', 'No CacaOssos, troque int maxVidas = 3 por 5: o jogo começa com 5 vidas e cada osso recupera até 5.', r'int\s+maxVidas\s*=\s*(?!3\b)\d+\s*;'],
        ['Gatos mais rápidos', 'Na classe Gato, troque double velocidade = 90 por 120: quase a velocidade do caramelo.', r'double\s+velocidade\s*=\s*(?!90\b)[\d.]+'],
        ['Latido mais forte', 'No latir, troque o alcance 170 por 250.', r'distanceTo\(\s*heroi\.position\s*\)\s*<\s*(?!170\b)\d+'],
        ['Dourado vale 10', 'No pegou, troque osso.dourado ? 5 : 1 por osso.dourado ? 10 : 1.', r'osso\.dourado\s*\?\s*(?!5\b)\d+'],
    ],
    lim='No simulador a música e o latido são sintetizados pelo navegador e só tocam depois do primeiro toque. O joystick e o botão funcionam com o mouse ou com o dedo, ao mesmo tempo no celular. O recorde fica guardado neste navegador (↺ Reiniciar apaga).',
    setup=SETUP_TILED + '\n\nRecorde: flutter pub add hive_flutter.',
)

PARTS.append(['Projeto · Caça-Ossos', 'Projeto 5 · Caça-Ossos'])
