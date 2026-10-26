// Prelúdio do Flame (parte 2): efeitos, partículas, paralaxe e overlays.

class EffectController {
  double duration;
  double reverseDuration;
  bool infinite;
  int? repeatCount;
  bool alternate;
  double startDelay;
  dynamic curve;

  EffectController({double duration = 0, double? reverseDuration, bool infinite = false, int? repeatCount, bool alternate = false, double startDelay = 0, dynamic curve, double? speed})
      : duration = duration,
        reverseDuration = reverseDuration ?? (alternate ? duration : 0),
        infinite = infinite,
        repeatCount = repeatCount,
        alternate = alternate,
        startDelay = startDelay,
        curve = curve;

  double get ciclo => duration + reverseDuration;
}

class Effect extends Component {
  EffectController controller;
  dynamic onComplete;
  double tempoEfeito = 0;
  bool terminou = false;
  bool comecou = false;
  bool removeOnFinish = true;
  PositionComponent? alvoFixo;

  Effect(EffectController controller, {dynamic onComplete})
      : controller = controller,
        onComplete = onComplete;

  PositionComponent get alvo => alvoFixo ?? parent as PositionComponent;
  bool get isFinished => terminou;

  void iniciar() {}
  void aplicar(double p) {}

  void reset() {
    tempoEfeito = 0;
    terminou = false;
    comecou = false;
  }

  void avancar(double dt) {
    if (terminou) return;
    if (!comecou) {
      comecou = true;
      iniciar();
    }
    tempoEfeito += dt;
    final c = controller;
    final t = tempoEfeito - c.startDelay;
    if (t < 0) return;
    final ciclo = c.ciclo;
    double p = 1;
    if (ciclo <= 0) {
      terminou = true;
    } else {
      final n = (t / ciclo).floor();
      final limite = c.infinite ? -1 : (c.repeatCount ?? 1);
      if (limite > 0 && n >= limite) {
        p = c.reverseDuration > 0 ? 0 : 1;
        terminou = true;
      } else {
        final r = t - n * ciclo;
        p = r < c.duration ? (c.duration == 0 ? 1 : r / c.duration) : 1 - (r - c.duration) / c.reverseDuration;
      }
    }
    aplicar(__flCurve(c.curve, p));
    if (terminou) {
      final f = onComplete;
      if (f != null) {
        f();
      }
    }
  }

  @override
  void update(double dt) {
    avancar(dt);
    if (terminou && removeOnFinish) {
      removeFromParent();
    }
  }
}

class MoveEffect extends Effect {
  Vector2 destino;
  bool relativo;
  Vector2 inicio = Vector2.zero();

  MoveEffect.to(Vector2 destino, EffectController controller, {dynamic onComplete})
      : destino = destino.clone(),
        relativo = false,
        super(controller, onComplete: onComplete);

  MoveEffect.by(Vector2 deslocamento, EffectController controller, {dynamic onComplete})
      : destino = deslocamento.clone(),
        relativo = true,
        super(controller, onComplete: onComplete);

  @override
  void iniciar() {
    inicio = alvo.position.clone();
  }

  @override
  void aplicar(double p) {
    final d = relativo ? destino : destino - inicio;
    alvo.position = inicio + d * p;
  }
}

class ScaleEffect extends Effect {
  Vector2 valor;
  bool relativo;
  Vector2 inicio = Vector2.zero();

  ScaleEffect.to(Vector2 escala, EffectController controller, {dynamic onComplete})
      : valor = escala.clone(),
        relativo = false,
        super(controller, onComplete: onComplete);

  ScaleEffect.by(Vector2 fator, EffectController controller, {dynamic onComplete})
      : valor = fator.clone(),
        relativo = true,
        super(controller, onComplete: onComplete);

  @override
  void iniciar() {
    inicio = alvo.scale.clone();
  }

  @override
  void aplicar(double p) {
    final fim = relativo ? Vector2(inicio.x * valor.x, inicio.y * valor.y) : valor;
    alvo.scale = inicio + (fim - inicio) * p;
  }
}

class SizeEffect extends Effect {
  Vector2 valor;
  bool relativo;
  Vector2 inicio = Vector2.zero();

  SizeEffect.to(Vector2 tamanho, EffectController controller, {dynamic onComplete})
      : valor = tamanho.clone(),
        relativo = false,
        super(controller, onComplete: onComplete);

  SizeEffect.by(Vector2 delta, EffectController controller, {dynamic onComplete})
      : valor = delta.clone(),
        relativo = true,
        super(controller, onComplete: onComplete);

  @override
  void iniciar() {
    inicio = alvo.size.clone();
  }

  @override
  void aplicar(double p) {
    final d = relativo ? valor : valor - inicio;
    alvo.size = inicio + d * p;
  }
}

class RotateEffect extends Effect {
  double valor;
  bool relativo;
  double inicio = 0;

  RotateEffect.to(double angulo, EffectController controller, {dynamic onComplete})
      : valor = angulo,
        relativo = false,
        super(controller, onComplete: onComplete);

  RotateEffect.by(double angulo, EffectController controller, {dynamic onComplete})
      : valor = angulo,
        relativo = true,
        super(controller, onComplete: onComplete);

  @override
  void iniciar() {
    inicio = alvo.angle;
  }

  @override
  void aplicar(double p) {
    final d = relativo ? valor : valor - inicio;
    alvo.angle = inicio + d * p;
  }
}

class OpacityEffect extends Effect {
  double valor;
  double inicio = 1;

  OpacityEffect.to(double opacidade, EffectController controller, {dynamic onComplete})
      : valor = opacidade,
        super(controller, onComplete: onComplete);

  OpacityEffect.fadeOut(EffectController controller, {dynamic onComplete})
      : valor = 0,
        super(controller, onComplete: onComplete);

  OpacityEffect.fadeIn(EffectController controller, {dynamic onComplete})
      : valor = 1,
        super(controller, onComplete: onComplete);

  @override
  void iniciar() {
    inicio = alvo.opacity;
  }

  @override
  void aplicar(double p) {
    alvo.opacity = inicio + (valor - inicio) * p;
  }
}

class RemoveEffect extends Effect {
  RemoveEffect({double delay = 0, dynamic onComplete}) : super(EffectController(duration: delay), onComplete: onComplete);

  @override
  void update(double dt) {
    avancar(dt);
    if (terminou) {
      final p = parent;
      if (p != null) {
        p.removeFromParent();
      }
    }
  }
}

class SequenceEffect extends Effect {
  List<Effect> efeitos;
  int atual = 0;
  bool infinito;
  int repeticoes;
  int feitas = 0;

  SequenceEffect(List<Effect> efeitos, {bool alternate = false, bool infinite = false, int repeatCount = 1, dynamic onComplete})
      : efeitos = efeitos,
        infinito = infinite,
        repeticoes = repeatCount,
        super(EffectController(duration: 1), onComplete: onComplete);

  @override
  void update(double dt) {
    if (terminou || efeitos.isEmpty) return;
    final e = efeitos[atual];
    e.alvoFixo = alvo;
    e.removeOnFinish = false;
    e.avancar(dt);
    if (e.terminou) {
      atual++;
      if (atual >= efeitos.length) {
        feitas++;
        if (infinito || feitas < repeticoes) {
          atual = 0;
          for (final x in efeitos) {
            x.reset();
          }
        } else {
          terminou = true;
          final f = onComplete;
          if (f != null) {
            f();
          }
          if (removeOnFinish) {
            removeFromParent();
          }
        }
      }
    }
  }
}

class Particle {
  double lifespan = 1;
  double tempoVida = 0;

  Particle({double? lifespan}) {
    if (lifespan != null) {
      this.lifespan = lifespan;
    }
  }

  factory Particle.generate({int count = 10, required dynamic generator, double? lifespan}) {
    final List<Particle> filhos = [];
    for (int i = 0; i < count; i++) {
      filhos.add(generator(i));
    }
    return ComposedParticle(children: filhos, lifespan: lifespan);
  }

  double get progress => lifespan <= 0 ? 1 : (tempoVida >= lifespan ? 1 : tempoVida / lifespan);
  bool shouldRemove() => tempoVida >= lifespan;

  void setLifespan(double valor) {
    lifespan = valor;
  }

  void update(double dt) {
    tempoVida += dt;
  }

  void render(Canvas canvas) {}
}

class ComposedParticle extends Particle {
  List<Particle> children;

  ComposedParticle({required List<Particle> children, double? lifespan})
      : children = children,
        super(lifespan: lifespan) {
    if (lifespan != null) {
      for (final c in children) {
        c.setLifespan(lifespan);
      }
    }
  }

  @override
  void setLifespan(double valor) {
    lifespan = valor;
    for (final c in children) {
      c.setLifespan(valor);
    }
  }

  @override
  void update(double dt) {
    tempoVida += dt;
    for (final c in children) {
      c.update(dt);
    }
  }

  @override
  void render(Canvas canvas) {
    for (final c in children) {
      c.render(canvas);
    }
  }
}

class CircleParticle extends Particle {
  double radius;
  Paint paint;

  CircleParticle({double radius = 10, Paint? paint, double? lifespan})
      : radius = radius,
        paint = paint ?? (Paint()..color = const Color(0xFFFFFFFF)),
        super(lifespan: lifespan);

  @override
  void render(Canvas canvas) {
    canvas.drawCircle(Offset.zero, radius, paint);
  }
}

class SpriteParticle extends Particle {
  Sprite sprite;
  Vector2 size;

  SpriteParticle({required Sprite sprite, Vector2? size, double? lifespan})
      : sprite = sprite,
        size = size ?? sprite.srcSize.clone(),
        super(lifespan: lifespan);

  @override
  void render(Canvas canvas) {
    sprite.render(canvas, size: size, anchor: Anchor.center);
  }
}

class ComputedParticle extends Particle {
  dynamic renderer;

  ComputedParticle({required dynamic renderer, double? lifespan})
      : renderer = renderer,
        super(lifespan: lifespan);

  @override
  void render(Canvas canvas) {
    renderer(canvas, this);
  }
}

class AcceleratedParticle extends Particle {
  Particle child;
  Vector2 position;
  Vector2 speed;
  Vector2 acceleration;

  AcceleratedParticle({required Particle child, Vector2? position, Vector2? speed, Vector2? acceleration, double? lifespan})
      : child = child,
        position = position ?? Vector2.zero(),
        speed = speed ?? Vector2.zero(),
        acceleration = acceleration ?? Vector2.zero(),
        super(lifespan: lifespan) {
    if (lifespan != null) {
      child.setLifespan(lifespan);
    }
  }

  @override
  void setLifespan(double valor) {
    lifespan = valor;
    child.setLifespan(valor);
  }

  @override
  void update(double dt) {
    tempoVida += dt;
    speed += acceleration * dt;
    position += speed * dt;
    child.update(dt);
  }

  @override
  void render(Canvas canvas) {
    canvas.save();
    canvas.translate(position.x, position.y);
    child.render(canvas);
    canvas.restore();
  }
}

class MovingParticle extends Particle {
  Particle child;
  Vector2 from;
  Vector2 to;
  dynamic curve;

  MovingParticle({required Particle child, Vector2? from, required Vector2 to, dynamic curve, double? lifespan})
      : child = child,
        from = from ?? Vector2.zero(),
        to = to,
        curve = curve,
        super(lifespan: lifespan) {
    if (lifespan != null) {
      child.setLifespan(lifespan);
    }
  }

  @override
  void setLifespan(double valor) {
    lifespan = valor;
    child.setLifespan(valor);
  }

  @override
  void update(double dt) {
    tempoVida += dt;
    child.update(dt);
  }

  @override
  void render(Canvas canvas) {
    final p = __flCurve(curve, progress);
    canvas.save();
    canvas.translate(from.x + (to.x - from.x) * p, from.y + (to.y - from.y) * p);
    child.render(canvas);
    canvas.restore();
  }
}

class ScalingParticle extends Particle {
  Particle child;
  double to;

  ScalingParticle({required Particle child, double to = 0, double? lifespan})
      : child = child,
        to = to,
        super(lifespan: lifespan) {
    if (lifespan != null) {
      child.setLifespan(lifespan);
    }
  }

  @override
  void setLifespan(double valor) {
    lifespan = valor;
    child.setLifespan(valor);
  }

  @override
  void update(double dt) {
    tempoVida += dt;
    child.update(dt);
  }

  @override
  void render(Canvas canvas) {
    final s = 1 + (to - 1) * progress;
    canvas.save();
    canvas.scale(s, s);
    child.render(canvas);
    canvas.restore();
  }
}

class RotatingParticle extends Particle {
  Particle child;
  double from;
  double to;

  RotatingParticle({required Particle child, double from = 0, double to = 6.283185307179586, double? lifespan})
      : child = child,
        from = from,
        to = to,
        super(lifespan: lifespan) {
    if (lifespan != null) {
      child.setLifespan(lifespan);
    }
  }

  @override
  void setLifespan(double valor) {
    lifespan = valor;
    child.setLifespan(valor);
  }

  @override
  void update(double dt) {
    tempoVida += dt;
    child.update(dt);
  }

  @override
  void render(Canvas canvas) {
    canvas.save();
    canvas.rotate(from + (to - from) * progress);
    child.render(canvas);
    canvas.restore();
  }
}

class TranslatedParticle extends Particle {
  Particle child;
  Vector2 offset;

  TranslatedParticle({required Particle child, required Vector2 offset, double? lifespan})
      : child = child,
        offset = offset,
        super(lifespan: lifespan) {
    if (lifespan != null) {
      child.setLifespan(lifespan);
    }
  }

  @override
  void setLifespan(double valor) {
    lifespan = valor;
    child.setLifespan(valor);
  }

  @override
  void update(double dt) {
    tempoVida += dt;
    child.update(dt);
  }

  @override
  void render(Canvas canvas) {
    canvas.save();
    canvas.translate(offset.x, offset.y);
    child.render(canvas);
    canvas.restore();
  }
}

class ParticleSystemComponent extends PositionComponent {
  Particle particle;

  ParticleSystemComponent({required Particle particle, Vector2? position, int? priority})
      : particle = particle,
        super(position: position, priority: priority);

  @override
  void update(double dt) {
    particle.update(dt);
    if (particle.shouldRemove()) {
      removeFromParent();
    }
  }

  @override
  void render(Canvas canvas) {
    particle.render(canvas);
  }
}

enum LayerFill { height, width, none }

class ParallaxImageData {
  String caminho;
  ParallaxImageData(String caminho) : caminho = caminho;
}

class ParallaxComponent extends PositionComponent {
  List<dynamic> imagens;
  Vector2 baseVelocity;
  Vector2 velocityMultiplierDelta;
  List<double> deslocamentos = [];

  ParallaxComponent({required List<dynamic> imagens, Vector2? baseVelocity, Vector2? velocityMultiplierDelta, Vector2? position, Vector2? size, int? priority})
      : imagens = imagens,
        baseVelocity = baseVelocity ?? Vector2.zero(),
        velocityMultiplierDelta = velocityMultiplierDelta ?? Vector2.all(1),
        super(position: position, size: size, priority: priority) {
    for (int i = 0; i < imagens.length; i++) {
      deslocamentos.add(0);
    }
  }

  ParallaxComponent get parallax => this;

  @override
  void onGameResize(Vector2 tamanho) {
    if (size.x == 0 && size.y == 0) {
      size = tamanho.clone();
    }
  }

  @override
  void update(double dt) {
    double fator = 1;
    for (int i = 0; i < imagens.length; i++) {
      deslocamentos[i] = deslocamentos[i] + baseVelocity.x * fator * dt;
      fator = fator * velocityMultiplierDelta.x;
    }
  }

  @override
  void render(Canvas canvas) {
    final tinta = Paint();
    for (int i = 0; i < imagens.length; i++) {
      final img = imagens[i];
      final t = __flImgSize(img);
      final escala = size.y / t.y;
      final largura = t.x * escala;
      double x = -(deslocamentos[i] % largura);
      while (x < size.x) {
        canvas.drawImageRect(img, Rect.fromLTWH(0, 0, t.x, t.y), Rect.fromLTWH(x, 0, largura + 0.5, size.y), tinta);
        x += largura;
      }
    }
  }
}

class Overlays {
  List<String> ativos = [];

  void add(String nome) {
    if (!ativos.contains(nome)) {
      ativos.add(nome);
    }
  }

  bool remove(String nome) => ativos.remove(nome);
  bool isActive(String nome) => ativos.contains(nome);
  List<String> get activeOverlays => ativos;

  void addAll(List<String> nomes) {
    for (final n in nomes) {
      add(n);
    }
  }

  void removeAll(List<String> nomes) {
    for (final n in nomes) {
      ativos.remove(n);
    }
  }

  void clear() {
    ativos.clear();
  }

  bool toggle(String nome) {
    if (ativos.contains(nome)) {
      ativos.remove(nome);
      return false;
    }
    ativos.add(nome);
    return true;
  }
}
