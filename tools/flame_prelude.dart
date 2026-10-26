// Prelúdio do Flame simplificado da Oficina Flutter 2.
// Estas classes são acrescentadas ao programa quando ele importa package:flame.
// O ciclo de vida, a árvore de componentes, as colisões e os eventos ficam no motor em JS (funções __fl*).

enum CollisionType { active, passive, inactive }

class Anchor {
  final double x;
  final double y;
  const Anchor(this.x, this.y);
  static const Anchor topLeft = Anchor(0, 0);
  static const Anchor topCenter = Anchor(0.5, 0);
  static const Anchor topRight = Anchor(1, 0);
  static const Anchor centerLeft = Anchor(0, 0.5);
  static const Anchor center = Anchor(0.5, 0.5);
  static const Anchor centerRight = Anchor(1, 0.5);
  static const Anchor bottomLeft = Anchor(0, 1);
  static const Anchor bottomCenter = Anchor(0.5, 1);
  static const Anchor bottomRight = Anchor(1, 1);
}

class Component {
  List<Component> children = [];
  Component? parent;
  int priority = 0;
  bool debugMode = false;

  Component({List<Component>? children, int? priority}) {
    if (priority != null) {
      this.priority = priority;
    }
    if (children != null) {
      for (final c in children) {
        __flAdd(this, c);
      }
    }
  }

  Future<void> onLoad() async {}
  void onMount() {}
  void onRemove() {}
  void onGameResize(Vector2 size) {}
  void update(double dt) {}
  void render(Canvas canvas) {}

  void add(Component c) {
    __flAdd(this, c);
  }

  void addAll(List<Component> lista) {
    for (final c in lista) {
      __flAdd(this, c);
    }
  }

  void remove(Component c) {
    __flRemove(c);
  }

  void removeAll(List<Component> lista) {
    for (final c in lista) {
      __flRemove(c);
    }
  }

  void removeFromParent() {
    __flRemove(this);
  }

  bool get isMounted => __flMounted(this);
  bool get isRemoved => __flRemoved(this);
  bool get isLoaded => __flMounted(this);
  FlameGame get game => __flRoot(this);
  FlameGame get gameRef => __flRoot(this);
  FlameGame? findGame() => __flRoot(this);

  Future<Sprite> loadSprite(String caminho, {Vector2? srcPosition, Vector2? srcSize}) async {
    return Sprite(__flImage(caminho), srcPosition: srcPosition, srcSize: srcSize);
  }

  Future<SpriteAnimation> loadSpriteAnimation(String caminho, SpriteAnimationData dados) async {
    return SpriteAnimation.fromFrameData(__flImage(caminho), dados);
  }
}

class PositionComponent extends Component {
  Vector2 position;
  Vector2 size;
  Vector2 scale;
  double angle;
  Anchor anchor;
  double opacity = 1;

  PositionComponent({Vector2? position, Vector2? size, Vector2? scale, double? angle, Anchor? anchor, List<Component>? children, int? priority})
      : position = position ?? Vector2.zero(),
        size = size ?? Vector2.zero(),
        scale = scale ?? Vector2.all(1),
        angle = angle ?? 0,
        anchor = anchor ?? Anchor.topLeft,
        super(children: children, priority: priority);

  double get x => position.x;
  set x(double v) {
    position.x = v;
  }

  double get y => position.y;
  set y(double v) {
    position.y = v;
  }

  double get width => size.x;
  set width(double v) {
    size.x = v;
  }

  double get height => size.y;
  set height(double v) {
    size.y = v;
  }

  Vector2 get center => __flCenter(this);
  Vector2 get absolutePosition => __flAbsPos(this);
  Vector2 get absoluteCenter => __flCenter(this);
  Vector2 get topLeftPosition => __flTopLeft(this);
  Rect toRect() => __flRect(this);
  Rect toAbsoluteRect() => __flRect(this);
  bool containsPoint(Vector2 ponto) => __flRect(this).contains(ponto.toOffset());
  bool containsLocalPoint(Vector2 ponto) => ponto.x >= 0 && ponto.y >= 0 && ponto.x < size.x && ponto.y < size.y;
  double distance(PositionComponent outro) => position.distanceTo(outro.position);
  bool get isFlippedHorizontally => scale.x < 0;
  bool get isFlippedVertically => scale.y < 0;

  void flipHorizontally() {
    scale.x = -scale.x;
  }

  void flipVertically() {
    scale.y = -scale.y;
  }

  void flipHorizontallyAroundCenter() {
    scale.x = -scale.x;
  }

  void flipVerticallyAroundCenter() {
    scale.y = -scale.y;
  }

  void lookAt(Vector2 alvo) {
    angle = __flAngleTo(this, alvo);
  }
}

class RectangleComponent extends PositionComponent {
  Paint paint;

  RectangleComponent({Vector2? position, Vector2? size, Vector2? scale, double? angle, Anchor? anchor, int? priority, Paint? paint, List<Component>? children})
      : paint = paint ?? (Paint()..color = const Color(0xFFFFFFFF)),
        super(position: position, size: size, scale: scale, angle: angle, anchor: anchor, priority: priority, children: children);

  @override
  void render(Canvas canvas) {
    canvas.drawRect(Rect.fromLTWH(0, 0, size.x, size.y), paint);
  }
}

class CircleComponent extends PositionComponent {
  Paint paint;

  CircleComponent({double? radius, Vector2? position, Vector2? scale, double? angle, Anchor? anchor, int? priority, Paint? paint, List<Component>? children})
      : paint = paint ?? (Paint()..color = const Color(0xFFFFFFFF)),
        super(position: position, size: Vector2.all((radius ?? 10) * 2), scale: scale, angle: angle, anchor: anchor, priority: priority, children: children);

  double get radius => size.x / 2;
  set radius(double r) {
    size = Vector2.all(r * 2);
  }

  @override
  void render(Canvas canvas) {
    canvas.drawCircle(Offset(size.x / 2, size.y / 2), size.x / 2, paint);
  }
}

class ShapeHitbox extends PositionComponent {
  bool circulo = false;
  bool tamanhoDoDono = true;
  CollisionType collisionType = CollisionType.active;
  bool isSolid = false;

  ShapeHitbox({Vector2? position, Vector2? size, Anchor? anchor, CollisionType? collisionType})
      : super(position: position, size: size, anchor: anchor) {
    if (collisionType != null) {
      this.collisionType = collisionType;
    }
    if (size != null) {
      tamanhoDoDono = false;
    }
  }
}

class RectangleHitbox extends ShapeHitbox {
  RectangleHitbox({Vector2? position, Vector2? size, Anchor? anchor, CollisionType? collisionType, bool isSolid = false})
      : super(position: position, size: size, anchor: anchor, collisionType: collisionType);
}

class CircleHitbox extends ShapeHitbox {
  CircleHitbox({double? radius, Vector2? position, Anchor? anchor, CollisionType? collisionType, bool isSolid = false})
      : super(position: position, size: radius == null ? null : Vector2.all(radius * 2), anchor: anchor, collisionType: collisionType) {
    circulo = true;
  }
}

mixin HasCollisionDetection on FlameGame {}

mixin CollisionCallbacks on Component {
  void onCollisionStart(Set<Vector2> intersectionPoints, PositionComponent other) {}
  void onCollision(Set<Vector2> intersectionPoints, PositionComponent other) {}
  void onCollisionEnd(PositionComponent other) {}
}

mixin TapCallbacks on Component {
  void onTapDown(TapDownEvent event) {}
  void onTapUp(TapUpEvent event) {}
  void onTapCancel(TapCancelEvent event) {}
  void onLongTapDown(TapDownEvent event) {}
}

mixin DragCallbacks on Component {
  void onDragStart(DragStartEvent event) {}
  void onDragUpdate(DragUpdateEvent event) {}
  void onDragEnd(DragEndEvent event) {}
  void onDragCancel(DragCancelEvent event) {}
}

mixin KeyboardEvents on FlameGame {
  KeyEventResult onKeyEvent(KeyEvent event, Set<LogicalKeyboardKey> keysPressed) => KeyEventResult.ignored;
}

mixin HasKeyboardHandlerComponents on FlameGame {}

mixin KeyboardHandler on Component {
  bool onKeyEvent(KeyEvent event, Set<LogicalKeyboardKey> keysPressed) => true;
}

mixin HasGameRef<T> on Component {}
mixin HasGameReference<T> on Component {}
mixin HasPaint on Component {}
mixin HasVisibility on Component {}

class Sprite {
  dynamic image;
  Vector2 srcPosition;
  Vector2 srcSize;
  Paint paint = Paint();

  Sprite(dynamic imagem, {Vector2? srcPosition, Vector2? srcSize})
      : image = imagem,
        srcPosition = srcPosition ?? Vector2.zero(),
        srcSize = srcSize ?? __flImgSize(imagem);

  static Future<Sprite> load(String caminho, {Vector2? srcPosition, Vector2? srcSize}) async {
    return Sprite(__flImage(caminho), srcPosition: srcPosition, srcSize: srcSize);
  }

  Vector2 get originalSize => srcSize;

  void render(Canvas canvas, {Vector2? position, Vector2? size, Anchor? anchor, Paint? overridePaint}) {
    final p = position ?? Vector2.zero();
    final s = size ?? srcSize;
    final a = anchor ?? Anchor.topLeft;
    canvas.drawImageRect(image, Rect.fromLTWH(srcPosition.x, srcPosition.y, srcSize.x, srcSize.y),
        Rect.fromLTWH(p.x - a.x * s.x, p.y - a.y * s.y, s.x, s.y), overridePaint ?? paint);
  }
}

class SpriteAnimationData {
  int amount = 1;
  double stepTime = 0.1;
  Vector2 textureSize = Vector2.zero();
  bool loop = true;
  Vector2 texturePosition = Vector2.zero();
  int amountPerRow = 0;

  SpriteAnimationData.sequenced({required int amount, required double stepTime, required Vector2 textureSize, bool loop = true, Vector2? texturePosition, int? amountPerRow}) {
    this.amount = amount;
    this.stepTime = stepTime;
    this.textureSize = textureSize;
    this.loop = loop;
    if (texturePosition != null) {
      this.texturePosition = texturePosition;
    }
    this.amountPerRow = amountPerRow ?? amount;
  }
}

class SpriteAnimation {
  List<Sprite> sprites;
  double stepTime;
  bool loop;

  SpriteAnimation(this.sprites, {this.stepTime = 0.1, this.loop = true});

  factory SpriteAnimation.spriteList(List<Sprite> sprites, {required double stepTime, bool loop = true}) {
    return SpriteAnimation(sprites, stepTime: stepTime, loop: loop);
  }

  factory SpriteAnimation.fromFrameData(dynamic imagem, SpriteAnimationData dados) {
    final List<Sprite> lista = [];
    for (int i = 0; i < dados.amount; i++) {
      final coluna = i % dados.amountPerRow;
      final linha = (i / dados.amountPerRow).floor();
      lista.add(Sprite(imagem,
          srcPosition: Vector2(dados.texturePosition.x + coluna * dados.textureSize.x, dados.texturePosition.y + linha * dados.textureSize.y),
          srcSize: dados.textureSize.clone()));
    }
    return SpriteAnimation(lista, stepTime: dados.stepTime, loop: dados.loop);
  }

  static Future<SpriteAnimation> load(String caminho, SpriteAnimationData dados) async {
    return SpriteAnimation.fromFrameData(__flImage(caminho), dados);
  }
}

class SpriteSheet {
  dynamic image;
  Vector2 srcSize;

  SpriteSheet({required dynamic image, required Vector2 srcSize})
      : image = image,
        srcSize = srcSize;

  int get columns => (__flImgSize(image).x / srcSize.x).floor();
  int get rows => (__flImgSize(image).y / srcSize.y).floor();

  Sprite getSprite(int row, int column) {
    return Sprite(image, srcPosition: Vector2(column * srcSize.x, row * srcSize.y), srcSize: srcSize.clone());
  }

  SpriteAnimation createAnimation({required int row, required double stepTime, bool loop = true, int from = 0, int? to}) {
    final fim = to ?? columns;
    final List<Sprite> lista = [];
    for (int i = from; i < fim; i++) {
      lista.add(getSprite(row, i));
    }
    return SpriteAnimation(lista, stepTime: stepTime, loop: loop);
  }
}

class SpriteComponent extends PositionComponent {
  Sprite? sprite;
  Paint paint = Paint();

  SpriteComponent({Sprite? sprite, Vector2? position, Vector2? size, Vector2? scale, double? angle, Anchor? anchor, int? priority, Paint? paint, List<Component>? children})
      : sprite = sprite,
        super(position: position, size: size, scale: scale, angle: angle, anchor: anchor, priority: priority, children: children) {
    if (paint != null) {
      this.paint = paint;
    }
  }

  @override
  void onMount() {
    final s = sprite;
    if (s != null && size.x == 0 && size.y == 0) {
      size = s.srcSize.clone();
    }
  }

  @override
  void render(Canvas canvas) {
    final s = sprite;
    if (s == null) return;
    if (size.x == 0 && size.y == 0) {
      size = s.srcSize.clone();
    }
    s.render(canvas, size: size, overridePaint: paint);
  }
}

class SpriteAnimationComponent extends PositionComponent {
  SpriteAnimation? animation;
  bool playing = true;
  bool removeOnFinish = false;
  double tempoAnimacao = 0;
  int quadroAtual = 0;
  bool terminou = false;
  Paint paint = Paint();

  SpriteAnimationComponent({SpriteAnimation? animation, Vector2? position, Vector2? size, Vector2? scale, double? angle, Anchor? anchor, int? priority, bool? playing, bool? removeOnFinish, Paint? paint, List<Component>? children})
      : animation = animation,
        super(position: position, size: size, scale: scale, angle: angle, anchor: anchor, priority: priority, children: children) {
    if (playing != null) {
      this.playing = playing;
    }
    if (removeOnFinish != null) {
      this.removeOnFinish = removeOnFinish;
    }
    if (paint != null) {
      this.paint = paint;
    }
  }

  @override
  void update(double dt) {
    final a = animation;
    if (a == null || a.sprites.isEmpty) return;
    if (size.x == 0 && size.y == 0) {
      size = a.sprites[0].srcSize.clone();
    }
    if (!playing || terminou) return;
    tempoAnimacao += dt;
    final total = (tempoAnimacao / a.stepTime).floor();
    if (a.loop) {
      quadroAtual = total % a.sprites.length;
    } else if (total >= a.sprites.length) {
      quadroAtual = a.sprites.length - 1;
      terminou = true;
      if (removeOnFinish) {
        removeFromParent();
      }
    } else {
      quadroAtual = total;
    }
  }

  @override
  void render(Canvas canvas) {
    final a = animation;
    if (a == null || a.sprites.isEmpty) return;
    if (size.x == 0 && size.y == 0) {
      size = a.sprites[0].srcSize.clone();
    }
    final i = quadroAtual < a.sprites.length ? quadroAtual : 0;
    a.sprites[i].render(canvas, size: size, overridePaint: paint);
  }
}

class TextPaint {
  dynamic style;
  TextPaint({dynamic style}) : style = style ?? const TextStyle(color: Color(0xFFFFFFFF), fontSize: 24);
}

class TextComponent extends PositionComponent {
  String text;
  TextPaint textRenderer;

  TextComponent({String? text, TextPaint? textRenderer, Vector2? position, Vector2? size, Vector2? scale, double? angle, Anchor? anchor, int? priority, List<Component>? children})
      : text = text ?? '',
        textRenderer = textRenderer ?? TextPaint(),
        super(position: position, size: size, scale: scale, angle: angle, anchor: anchor, priority: priority, children: children);

  TextPainter medir() {
    final tp = TextPainter(text: TextSpan(text: text, style: textRenderer.style), textDirection: TextDirection.ltr)..layout();
    size = Vector2(tp.width, tp.height);
    return tp;
  }

  @override
  void onMount() {
    medir();
  }

  @override
  void update(double dt) {
    medir();
  }

  @override
  void render(Canvas canvas) {
    medir().paint(canvas, Offset.zero);
  }
}

class FlTimer {
  double limit;
  bool repeat;
  dynamic onTick;
  double current = 0;
  bool isRunning = true;

  FlTimer(double limite, {bool repeat = false, dynamic onTick, bool autoStart = true})
      : limit = limite,
        repeat = repeat,
        onTick = onTick {
    isRunning = autoStart;
  }

  bool get finished => !repeat && current >= limit;
  double get progress => limit == 0 ? 1 : current / limit;

  void update(double dt) {
    if (!isRunning) return;
    current += dt;
    if (current >= limit) {
      final f = onTick;
      if (repeat) {
        current -= limit;
      } else {
        current = limit;
        isRunning = false;
      }
      if (f != null) {
        f();
      }
    }
  }

  void start() {
    current = 0;
    isRunning = true;
  }

  void stop() {
    current = 0;
    isRunning = false;
  }

  void pause() {
    isRunning = false;
  }

  void resume() {
    isRunning = true;
  }

  void reset() {
    current = 0;
  }
}

class TimerComponent extends Component {
  FlTimer timer;
  bool removeOnFinish;

  TimerComponent({required double period, bool repeat = false, bool autoStart = true, bool removeOnFinish = false, dynamic onTick})
      : timer = FlTimer(period, repeat: repeat, onTick: onTick, autoStart: autoStart),
        removeOnFinish = removeOnFinish;

  @override
  void update(double dt) {
    timer.update(dt);
    if (removeOnFinish && timer.finished) {
      removeFromParent();
    }
  }
}

class World extends Component {
  World({List<Component>? children}) : super(children: children);
}

class Viewfinder extends PositionComponent {
  double zoom = 1;
  Viewfinder() : super(anchor: Anchor.center);
}

class Viewport extends Component {}

class CameraComponent extends Component {
  Viewfinder viewfinder = Viewfinder();
  Viewport viewport = Viewport();
  World? world;
  PositionComponent? seguindo;

  CameraComponent({World? world}) : world = world;

  void follow(PositionComponent alvo, {double? maxSpeed, bool snap = false}) {
    seguindo = alvo;
  }

  void stop() {
    seguindo = null;
  }

  void moveTo(Vector2 ponto, {double? speed}) {
    seguindo = null;
    viewfinder.position = ponto.clone();
  }

  Rect get visibleWorldRect => __flVisible(this);
}

class Images {
  String prefix = 'assets/images/';
  Future<dynamic> load(String caminho) async => __flImage(caminho);
  Future<List<dynamic>> loadAll(List<String> nomes) async => nomes.map((n) => __flImage(n)).toList();
  dynamic fromCache(String caminho) => __flImage(caminho);
}

class FlameGame extends Component {
  Vector2 size = Vector2.zero();
  World world;
  CameraComponent camera;
  bool paused = false;
  Images images = Images();
  Overlays overlays = Overlays();

  FlameGame({World? world, CameraComponent? camera, List<Component>? children})
      : world = world ?? World(),
        camera = camera ?? CameraComponent(),
        super(children: children);

  Vector2 get canvasSize => size;

  void pauseEngine() {
    paused = true;
  }

  void resumeEngine() {
    paused = false;
  }

  Color backgroundColor() => const Color(0xFF000000);

  Future<ParallaxComponent> loadParallaxComponent(List<ParallaxImageData> dados, {Vector2? baseVelocity, Vector2? velocityMultiplierDelta, dynamic repeat, dynamic fill, Vector2? size, Vector2? position, int? priority}) async {
    final List<dynamic> imagens = [];
    for (final d in dados) {
      imagens.add(__flImage(d.caminho));
    }
    return ParallaxComponent(imagens: imagens, baseVelocity: baseVelocity, velocityMultiplierDelta: velocityMultiplierDelta, size: size ?? this.size.clone(), position: position, priority: priority);
  }
}
