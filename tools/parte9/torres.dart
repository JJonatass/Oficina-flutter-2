import 'package:flame/components.dart';
import 'package:flame/events.dart';
import 'package:flame/game.dart';
import 'package:flame/input.dart';
import 'package:flame_audio/flame_audio.dart';
import 'package:flutter/material.dart';

void main() => runApp(GameWidget(game: Torres()));

const int colunas = 9;
const int linhas = 11;
const double lado = 40;
const double topo = 44; // o quintal começa abaixo do placar
const entrada = [4, 0]; // coluna e linha por onde os gatos entram
const saida = [4, 10]; // por onde eles fogem com a comida
const vizinhos4 = [[1, 0], [-1, 0], [0, 1], [0, -1]];
const int ossosIniciais = 30;

class Torres extends FlameGame with TapCallbacks {
  List<List<bool>> bloqueado = [];
  List<List<int>> distancia = [];
  final List<Tiro> tiros = []; // a reserva de tiros: são reaproveitados, nunca destruídos
  final int custoTorre = 10;
  int vidas = 10;
  int ossos = ossosIniciais;
  int onda = 0;
  int faltamNascer = 0;
  double relogio = 0;
  bool ondaAtiva = false;
  bool fim = false;
  late TextComponent placar;
  late TextComponent aviso;

  @override
  Color backgroundColor() => const Color(0xFF2E3B2C);

  @override
  Future<void> onLoad() async {
    add(Quintal());
    placar = TextComponent(text: '', position: Vector2(10, 12), priority: 10, textRenderer: TextPaint(style: const TextStyle(fontSize: 17, color: Colors.white)));
    add(placar);
    aviso = TextComponent(text: 'Toque no quintal para pôr um caramelo (10 🦴).', position: Vector2(10, topo + linhas * lado + 12), priority: 10, textRenderer: TextPaint(style: const TextStyle(fontSize: 14, color: Colors.white)));
    add(aviso);
    add(Botao('▶', Vector2(size.x - 80, topo + linhas * lado + 40), proximaOnda));
    reiniciar();
  }

  void reiniciar() {
    children.whereType<Torre>().toList().forEach((t) => t.removeFromParent());
    children.whereType<Gato>().toList().forEach((g) => g.removeFromParent());
    bloqueado = List.generate(linhas, (_) => List.filled(colunas, false));
    calcularDistancias();
    vidas = 10;
    ossos = ossosIniciais;
    onda = 0;
    ondaAtiva = false;
    fim = false;
  }

  // BFS a partir da saída: cada casa guarda quantos passos faltam até a saída.
  // Os gatos só precisam ir sempre para o vizinho com número menor (um "mapa de fluxo").
  bool calcularDistancias() {
    final d = List.generate(linhas, (_) => List.filled(colunas, -1));
    final List<List<int>> fila = [saida];
    d[saida[1]][saida[0]] = 0;
    var i = 0;
    while (i < fila.length) {
      final c = fila[i];
      i++;
      for (final v in vizinhos4) {
        final nx = c[0] + v[0];
        final ny = c[1] + v[1];
        if (nx < 0 || ny < 0 || nx >= colunas || ny >= linhas) continue;
        if (bloqueado[ny][nx] || d[ny][nx] >= 0) continue;
        d[ny][nx] = d[c[1]][c[0]] + 1;
        fila.add([nx, ny]);
      }
    }
    if (d[entrada[1]][entrada[0]] < 0) return false; // as torres fecharam o caminho
    distancia = d;
    return true;
  }

  @override
  void onTapDown(TapDownEvent event) {
    if (fim) return;
    final p = event.canvasPosition;
    final c = (p.x / lado).floor();
    final l = ((p.y - topo) / lado).floor();
    if (c < 0 || l < 0 || c >= colunas || l >= linhas || bloqueado[l][c]) return;
    if ((c == entrada[0] && l == entrada[1]) || (c == saida[0] && l == saida[1])) return;
    if (ossos < custoTorre) {
      aviso.text = 'Faltam ossos: cada caramelo custa $custoTorre.';
      return;
    }
    for (final g in children.whereType<Gato>()) {
      if (g.coluna == c && g.linha == l) return; // tem um gato nessa casa
    }
    bloqueado[l][c] = true;
    if (!calcularDistancias()) {
      bloqueado[l][c] = false; // desfaz: o caminho precisa continuar existindo
      aviso.text = 'Não dá para fechar o caminho dos gatos!';
      return;
    }
    ossos -= custoTorre;
    add(Torre(c, l));
    aviso.text = 'Caramelo de guarda posto.';
  }

  void proximaOnda() {
    if (fim) {
      reiniciar();
      aviso.text = 'Novo jogo. Monte a defesa!';
      return;
    }
    if (ondaAtiva) return;
    onda++;
    faltamNascer = 5 + onda * 2;
    relogio = 0;
    ondaAtiva = true;
    aviso.text = 'Onda $onda: lá vêm os gatos!';
  }

  // pega um tiro parado da reserva; só cria um novo se todos estiverem em uso
  Tiro pegarTiro() {
    for (final t in tiros) {
      if (!t.ativo) return t;
    }
    final novo = Tiro();
    tiros.add(novo);
    add(novo);
    return novo;
  }

  void gatoFugiu(Gato g) {
    g.removeFromParent();
    vidas--;
    FlameAudio.play('dano.wav');
    if (vidas <= 0) {
      fim = true;
      ondaAtiva = false;
      aviso.text = 'Os gatos levaram a comida! Onda $onda. ▶ recomeça.';
    }
  }

  void gatoDerrotado(Gato g) {
    g.removeFromParent();
    ossos += 2;
    FlameAudio.play('osso.wav');
  }

  @override
  void update(double dt) {
    super.update(dt);
    if (ondaAtiva && !fim) {
      relogio += dt;
      if (faltamNascer > 0 && relogio >= 0.8) {
        relogio = 0;
        faltamNascer--;
        add(Gato(2 + onda));
      }
      if (faltamNascer == 0 && children.whereType<Gato>().isEmpty) {
        ondaAtiva = false;
        ossos += 5;
        aviso.text = 'Onda $onda vencida! +5 🦴. Toque ▶ para a próxima.';
      }
    }
    placar.text = 'Onda $onda   ❤ $vidas   🦴 $ossos   tiros criados: ${tiros.length}';
  }
}

class Gato extends SpriteAnimationComponent with HasGameReference<Torres> {
  int vida;
  late int vidaMax;
  final double velocidade = 50;
  int coluna = entrada[0];
  int linha = entrada[1];
  Vector2? alvo;

  Gato(this.vida) : super(size: Vector2.all(32), anchor: Anchor.center) {
    vidaMax = vida;
    position = Vector2(entrada[0] * lado + lado / 2, topo + entrada[1] * lado + lado / 2);
  }

  @override
  Future<void> onLoad() async {
    animation = await game.loadSpriteAnimation('gato.png', SpriteAnimationData.sequenced(amount: 2, stepTime: 0.25, textureSize: Vector2.all(16)));
  }

  // passos que faltam até a saída: quem tem menos está mais adiantado
  int get faltam => game.distancia[linha][coluna];

  @override
  void update(double dt) {
    super.update(dt);
    final a = alvo;
    if (a == null || position.distanceTo(a) < 2) {
      if (a != null) position = a.clone();
      coluna = (position.x / lado).floor();
      linha = ((position.y - topo) / lado).floor();
      if (coluna == saida[0] && linha == saida[1]) {
        game.gatoFugiu(this);
        return;
      }
      // vai para o vizinho mais perto da saída
      var melhor = game.distancia[linha][coluna];
      var proximo = [coluna, linha];
      for (final v in vizinhos4) {
        final nx = coluna + v[0];
        final ny = linha + v[1];
        if (nx < 0 || ny < 0 || nx >= colunas || ny >= linhas) continue;
        final d = game.distancia[ny][nx];
        if (d >= 0 && (melhor < 0 || d < melhor)) {
          melhor = d;
          proximo = [nx, ny];
        }
      }
      alvo = Vector2(proximo[0] * lado + lado / 2, topo + proximo[1] * lado + lado / 2);
      return;
    }
    final passo = velocidade * dt;
    final falta = a - position;
    position += falta.length <= passo ? falta : falta.normalized() * passo;
  }

  void levarTiro() {
    vida--;
    if (vida <= 0) game.gatoDerrotado(this);
  }

  @override
  void render(Canvas canvas) {
    super.render(canvas);
    canvas.drawRect(const Rect.fromLTWH(2, -6, 28, 4), Paint()..color = Colors.black54);
    canvas.drawRect(Rect.fromLTWH(2, -6, 28 * vida / vidaMax, 4), Paint()..color = Colors.lightGreenAccent);
  }
}

class Torre extends SpriteAnimationComponent with HasGameReference<Torres> {
  final double alcance = 90;
  final double intervalo = 0.6; // segundos entre um tiro e outro
  double recarga = 0;

  Torre(int c, int l) : super(position: Vector2(c * lado + lado / 2, topo + l * lado + lado / 2), size: Vector2.all(36), anchor: Anchor.center);

  @override
  Future<void> onLoad() async {
    animation = await game.loadSpriteAnimation('caramelo_sentado.png', SpriteAnimationData.sequenced(amount: 2, stepTime: 0.4, textureSize: Vector2.all(16)));
  }

  @override
  void update(double dt) {
    super.update(dt);
    recarga -= dt;
    if (recarga > 0) return;
    // mira no gato ao alcance que está mais perto de fugir
    Gato? escolhido;
    for (final g in game.children.whereType<Gato>()) {
      if (g.position.distanceTo(position) > alcance) continue;
      if (escolhido == null || g.faltam < escolhido.faltam) escolhido = g;
    }
    final e = escolhido;
    if (e == null) return;
    game.pegarTiro().lancar(position, e);
    recarga = intervalo;
  }
}

class Tiro extends PositionComponent {
  bool ativo = false;
  Gato? alvo;
  final double velocidade = 320;

  Tiro() : super(size: Vector2.all(10), anchor: Anchor.center, priority: 5);

  void lancar(Vector2 de, Gato g) {
    position = de.clone();
    alvo = g;
    ativo = true;
  }

  @override
  void update(double dt) {
    super.update(dt);
    final g = alvo;
    if (!ativo || g == null) return;
    if (!g.isMounted) {
      ativo = false; // o gato já foi embora: o tiro volta para a reserva
      return;
    }
    final falta = g.position - position;
    if (falta.length < 10) {
      ativo = false;
      g.levarTiro();
      return;
    }
    position += falta.normalized() * velocidade * dt;
  }

  @override
  void render(Canvas canvas) {
    if (!ativo) return;
    canvas.drawCircle(const Offset(5, 5), 5, Paint()..color = const Color(0xFFFFF3E0));
  }
}

// o chão quadriculado, a entrada e a saída
class Quintal extends PositionComponent with HasGameReference<Torres> {
  @override
  void render(Canvas canvas) {
    for (var l = 0; l < linhas; l++) {
      for (var c = 0; c < colunas; c++) {
        final r = Rect.fromLTWH(c * lado, topo + l * lado, lado, lado);
        canvas.drawRect(r, Paint()..color = (c + l).isEven ? const Color(0xFF7CB342) : const Color(0xFF8BC34A));
      }
    }
    canvas.drawRect(Rect.fromLTWH(entrada[0] * lado, topo + entrada[1] * lado, lado, lado), Paint()..color = const Color(0x88E53935));
    canvas.drawRect(Rect.fromLTWH(saida[0] * lado, topo + saida[1] * lado, lado, lado), Paint()..color = const Color(0x88FFD54F));
  }
}

class Botao extends ButtonComponent {
  Botao(String simbolo, Vector2 onde, void Function() acao)
      : super(
          position: onde,
          size: Vector2.all(64),
          button: Tecla(simbolo, Colors.black38),
          buttonDown: Tecla(simbolo, Colors.black54),
          onPressed: acao,
        );
}

class Tecla extends PositionComponent {
  final String simbolo;
  final Color cor;
  Tecla(this.simbolo, this.cor) : super(size: Vector2.all(64));

  @override
  void render(Canvas canvas) {
    canvas.drawCircle(const Offset(32, 32), 32, Paint()..color = cor);
    final tp = TextPainter(text: TextSpan(text: simbolo, style: const TextStyle(fontSize: 28, color: Colors.white)), textDirection: TextDirection.ltr)..layout();
    tp.paint(canvas, Offset(32 - tp.width / 2, 32 - tp.height / 2));
  }
}
