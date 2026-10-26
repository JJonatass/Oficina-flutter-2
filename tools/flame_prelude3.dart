// Prelúdio 3 do Flame simplificado: joystick e botões na tela, ColorEffect, MoveAlongPathEffect,
// Forge2D simplificado (flame_forge2d) e mapas do Tiled (flame_tiled).

// ---------------------------------------------------------------- joystick e botões
enum JoystickDirection { up, upLeft, upRight, right, down, downRight, downLeft, left, idle }

class JoystickComponent extends PositionComponent with DragCallbacks {
  PositionComponent? knob;
  PositionComponent? background;
  dynamic margin;
  double knobRadius = 0;
  double raioPedido = 0;
  Vector2 delta = Vector2.zero();
  Vector2 relativeDelta = Vector2.zero();
  Vector2 centro = Vector2.zero();

  JoystickComponent({PositionComponent? knob, PositionComponent? background, dynamic margin, Vector2? position, double? size, double? knobRadius, Anchor? anchor, int? priority})
      : knob = knob,
        background = background,
        margin = margin,
        super(position: position, size: Vector2.all(size ?? 0), anchor: anchor ?? Anchor.center, priority: priority ?? 100) {
    raioPedido = knobRadius ?? 0;
  }

  bool get isDragged => !delta.isZero();
  bool get isIdle => delta.isZero();

  @override
  Future<void> onLoad() async {
    final fundo = background;
    if (size.x == 0) {
      if (fundo != null) {
        size = fundo.size.clone();
      } else {
        size = Vector2.all(100);
      }
    }
    centro = Vector2(size.x / 2, size.y / 2);
    knobRadius = raioPedido > 0 ? raioPedido : size.x / 2;
    if (fundo != null) {
      fundo.anchor = Anchor.center;
      fundo.position = centro.clone();
      add(fundo);
    }
    final bolinha = knob;
    if (bolinha != null) {
      bolinha.anchor = Anchor.center;
      bolinha.position = centro.clone();
      add(bolinha);
    }
    if (margin != null) {
      position = __flMargem(margin, game.size, this);
    }
  }

  @override
  void onGameResize(Vector2 tamanho) {
    if (margin != null) {
      position = __flMargem(margin, tamanho, this);
    }
  }

  void mover(Vector2 local) {
    Vector2 d = local - centro;
    final l = d.length;
    if (l > knobRadius && l > 0) {
      d = d * (knobRadius / l);
    }
    delta = d;
    relativeDelta = knobRadius > 0 ? d * (1 / knobRadius) : Vector2.zero();
    final bolinha = knob;
    if (bolinha != null) {
      bolinha.position = centro + d;
    }
  }

  void soltar() {
    delta = Vector2.zero();
    relativeDelta = Vector2.zero();
    final bolinha = knob;
    if (bolinha != null) {
      bolinha.position = centro.clone();
    }
  }

  @override
  void onDragStart(DragStartEvent event) {
    mover(event.localPosition);
  }

  @override
  void onDragUpdate(DragUpdateEvent event) {
    mover(event.localEndPosition);
  }

  @override
  void onDragEnd(DragEndEvent event) {
    soltar();
  }

  @override
  void onDragCancel(DragCancelEvent event) {
    soltar();
  }

  JoystickDirection get direction {
    final i = __flDirecao(delta);
    if (i == 0) return JoystickDirection.up;
    if (i == 1) return JoystickDirection.upLeft;
    if (i == 2) return JoystickDirection.upRight;
    if (i == 3) return JoystickDirection.right;
    if (i == 4) return JoystickDirection.down;
    if (i == 5) return JoystickDirection.downRight;
    if (i == 6) return JoystickDirection.downLeft;
    if (i == 7) return JoystickDirection.left;
    return JoystickDirection.idle;
  }
}

class ButtonComponent extends PositionComponent with TapCallbacks {
  PositionComponent? button;
  PositionComponent? buttonDown;
  dynamic onPressed;
  dynamic onReleased;
  dynamic onCancelled;
  bool apertado = false;

  ButtonComponent({PositionComponent? button, PositionComponent? buttonDown, dynamic onPressed, dynamic onReleased, dynamic onCancelled, Vector2? position, Vector2? size, Anchor? anchor, int? priority})
      : button = button,
        buttonDown = buttonDown,
        onPressed = onPressed,
        onReleased = onReleased,
        onCancelled = onCancelled,
        super(position: position, size: size, anchor: anchor, priority: priority ?? 100);

  @override
  Future<void> onLoad() async {
    final b = button;
    if (b != null) {
      if (size.x == 0) {
        size = b.size.clone();
      }
      add(b);
    }
    final bd = buttonDown;
    if (bd != null) {
      bd.opacity = 0;
      add(bd);
    }
    posicionar();
  }

  void posicionar() {}

  void trocar(bool baixo) {
    apertado = baixo;
    final bd = buttonDown;
    final b = button;
    if (bd != null && b != null) {
      b.opacity = baixo ? 0 : 1;
      bd.opacity = baixo ? 1 : 0;
    }
  }

  @override
  void onTapDown(TapDownEvent event) {
    trocar(true);
    final f = onPressed;
    if (f != null) {
      f();
    }
  }

  @override
  void onTapUp(TapUpEvent event) {
    trocar(false);
    final f = onReleased;
    if (f != null) {
      f();
    }
  }

  @override
  void onTapCancel(TapCancelEvent event) {
    trocar(false);
    final f = onCancelled;
    if (f != null) {
      f();
    }
  }
}

class HudButtonComponent extends ButtonComponent {
  dynamic margin;

  HudButtonComponent({PositionComponent? button, PositionComponent? buttonDown, dynamic margin, dynamic onPressed, dynamic onReleased, dynamic onCancelled, Vector2? position, Vector2? size, Anchor? anchor, int? priority})
      : margin = margin,
        super(button: button, buttonDown: buttonDown, onPressed: onPressed, onReleased: onReleased, onCancelled: onCancelled, position: position, size: size, anchor: anchor, priority: priority);

  @override
  void posicionar() {
    if (margin != null) {
      position = __flMargem(margin, game.size, this);
    }
  }

  @override
  void onGameResize(Vector2 tamanho) {
    if (margin != null) {
      if (size.x == 0) {
        final b = button;
        if (b != null) {
          size = b.size.clone();
        }
      }
      position = __flMargem(margin, tamanho, this);
    }
  }
}

// ---------------------------------------------------------------- efeitos de cor e de caminho
class ColorEffect extends Effect {
  Color cor;
  double de;
  double ate;

  ColorEffect(Color color, EffectController controller, {double opacityFrom = 0, double opacityTo = 1, dynamic onComplete})
      : cor = color,
        de = opacityFrom,
        ate = opacityTo,
        super(controller, onComplete: onComplete);

  @override
  void aplicar(double p) {
    alvo.tintColor = cor;
    alvo.tintAmount = de + (ate - de) * p;
  }
}

class MoveAlongPathEffect extends Effect {
  dynamic caminho;
  bool absoluto;
  bool orientado;
  Vector2 inicio = Vector2.zero();

  MoveAlongPathEffect(dynamic path, EffectController controller, {bool absolute = false, bool oriented = false, dynamic onComplete})
      : caminho = path,
        absoluto = absolute,
        orientado = oriented,
        super(controller, onComplete: onComplete);

  @override
  void iniciar() {
    inicio = alvo.position.clone();
  }

  @override
  void aplicar(double p) {
    final ponto = __flPathAt(caminho, p);
    alvo.position = absoluto ? ponto : inicio + ponto;
    if (orientado) {
      alvo.angle = __flPathAngle(caminho, p);
    }
  }
}

// ---------------------------------------------------------------- Forge2D simplificado
class Filter {
  int categoryBits = 1;
  int maskBits = 65535;
  int groupIndex = 0;
}

class CircleShape {
  double radius;
  Vector2 position;

  CircleShape({double radius = 0, Vector2? position})
      : radius = radius,
        position = position ?? Vector2.zero();
}

class PolygonShape {
  List<Vector2> vertices = [];

  PolygonShape();

  void setAsBoxXY(double hx, double hy) {
    vertices = [Vector2(-hx, -hy), Vector2(hx, -hy), Vector2(hx, hy), Vector2(-hx, hy)];
  }

  void setAsBox(double hx, double hy, Vector2 center, double angle) {
    vertices = __b2Caixa(hx, hy, center, angle);
  }

  void set(List<Vector2> pontos) {
    vertices = pontos.map((p) => p.clone()).toList();
  }
}

class EdgeShape {
  Vector2 vertex1 = Vector2.zero();
  Vector2 vertex2 = Vector2.zero();

  EdgeShape();

  void set(Vector2 a, Vector2 b) {
    vertex1 = a.clone();
    vertex2 = b.clone();
  }
}

class ChainShape {
  List<Vector2> pontos = [];
  bool fechada = false;

  ChainShape();

  void createChain(List<Vector2> v) {
    pontos = v.map((p) => p.clone()).toList();
    fechada = false;
  }

  void createLoop(List<Vector2> v) {
    pontos = v.map((p) => p.clone()).toList();
    fechada = true;
  }
}

class FixtureDef {
  dynamic shape;
  double density;
  double friction;
  double restitution;
  bool isSensor;
  dynamic userData;
  Filter filter;

  FixtureDef(dynamic shape, {double density = 0, double friction = 0.2, double restitution = 0, bool isSensor = false, dynamic userData, Filter? filter})
      : shape = shape,
        density = density,
        friction = friction,
        restitution = restitution,
        isSensor = isSensor,
        userData = userData,
        filter = filter ?? Filter();
}

class Fixture {
  Body body;
  dynamic shape;
  double density;
  double friction;
  double restitution;
  bool isSensor;
  dynamic userData;
  Filter filter;

  Fixture(Body dono, FixtureDef d)
      : body = dono,
        shape = d.shape,
        density = d.density,
        friction = d.friction,
        restitution = d.restitution,
        isSensor = d.isSensor,
        userData = d.userData,
        filter = d.filter;

  bool testPoint(Vector2 ponto) => __b2TestPoint(this, ponto);
}

class BodyDef {
  dynamic type;
  Vector2 position;
  double angle;
  Vector2 linearVelocity;
  double angularVelocity;
  double linearDamping;
  double angularDamping;
  bool fixedRotation;
  bool bullet;
  dynamic userData;
  double gravityScale;

  BodyDef({dynamic type, Vector2? position, double angle = 0, Vector2? linearVelocity, double angularVelocity = 0, double linearDamping = 0, double angularDamping = 0, bool fixedRotation = false, bool bullet = false, dynamic userData, bool allowSleep = true, bool awake = true, dynamic gravityScale})
      : type = type ?? BodyType.static,
        position = position ?? Vector2.zero(),
        angle = angle,
        linearVelocity = linearVelocity ?? Vector2.zero(),
        angularVelocity = angularVelocity,
        linearDamping = linearDamping,
        angularDamping = angularDamping,
        fixedRotation = fixedRotation,
        bullet = bullet,
        userData = userData,
        gravityScale = gravityScale == null ? 1.0 : __b2Escala(gravityScale);
}

class Body {
  Forge2DWorld world;
  dynamic bodyType;
  Vector2 position;
  double angle;
  Vector2 linearVelocity;
  double angularVelocity;
  double linearDamping;
  double angularDamping;
  bool fixedRotation;
  bool isBullet;
  dynamic userData;
  double gravityScale;
  List<Fixture> fixtures = [];
  double mass = 0;
  double inertia = 0;
  Vector2 localCenter = Vector2.zero();
  Vector2 forca = Vector2.zero();
  double torque = 0;
  bool destruido = false;
  bool isAwake = true;
  dynamic componente;

  Body(BodyDef d, Forge2DWorld mundo)
      : world = mundo,
        bodyType = d.type,
        position = d.position.clone(),
        angle = d.angle,
        linearVelocity = d.linearVelocity.clone(),
        angularVelocity = d.angularVelocity,
        linearDamping = d.linearDamping,
        angularDamping = d.angularDamping,
        fixedRotation = d.fixedRotation,
        isBullet = d.bullet,
        userData = d.userData,
        gravityScale = d.gravityScale;

  Fixture createFixture(FixtureDef d) {
    final f = Fixture(this, d);
    fixtures.add(f);
    __b2Massa(this);
    return f;
  }

  Fixture createFixtureFromShape(dynamic shape, [double density = 0]) => createFixture(FixtureDef(shape, density: density));

  void destroyFixture(Fixture f) {
    fixtures.remove(f);
    __b2Massa(this);
  }

  void applyLinearImpulse(Vector2 impulse, {Vector2? point, bool wake = true}) {
    __b2Impulso(this, impulse, point);
  }

  void applyForce(Vector2 force, {Vector2? point}) {
    __b2Forca(this, force, point);
  }

  void applyAngularImpulse(double impulse) {
    __b2ImpulsoAngular(this, impulse);
  }

  void applyTorque(double t) {
    torque += t;
  }

  void setTransform(Vector2 p, double a) {
    position.x = p.x;
    position.y = p.y;
    angle = a;
  }

  void setType(dynamic t) {
    bodyType = t;
    __b2Massa(this);
  }

  void setFixedRotation(bool v) {
    fixedRotation = v;
    __b2Massa(this);
  }

  void setAwake(bool v) {
    isAwake = v;
  }

  void setGravityScale(dynamic g) {
    gravityScale = __b2Escala(g);
  }

  double getMass() => mass;
  dynamic getUserData() => userData;
  dynamic get type => bodyType;
  Vector2 get worldCenter => __b2Centro(this);
  Vector2 worldPoint(Vector2 local) => __b2PontoMundo(this, local);
  Vector2 localPoint(Vector2 ponto) => __b2PontoLocal(this, ponto);
  Vector2 worldVector(Vector2 local) => __b2VetorMundo(this, local);
  Vector2 localVector(Vector2 v) => __b2VetorLocal(this, v);
  List<Joint> get joints => world.joints.where((j) => j.def.bodyA == this || j.def.bodyB == this).toList();
}

class Forge2DWorld extends World {
  Vector2 gravity;
  List<Body> bodies = [];

  Forge2DWorld({Vector2? gravity, List<Component>? children})
      : gravity = gravity ?? Vector2(0, 10),
        super(children: children);

  List<Joint> joints = [];

  Forge2DWorld get physicsWorld => this;

  Joint createJoint(Joint j) {
    joints.add(j);
    return j;
  }

  void destroyJoint(Joint j) {
    j.destruido = true;
    joints.remove(j);
  }

  void raycast(dynamic callback, Vector2 inicio, Vector2 fim) {
    __b2Raio(this, callback, inicio, fim);
  }

  void setGravity(Vector2 g) {
    gravity = g.clone();
  }

  Body createBody(BodyDef def) {
    final b = Body(def, this);
    bodies.add(b);
    return b;
  }

  void destroyBody(Body b) {
    b.destruido = true;
    bodies.remove(b);
    joints.removeWhere((j) => j.def.bodyA == b || j.def.bodyB == b);
  }

  @override
  void update(double dt) {
    __b2Passo(this, dt);
  }
}

class Forge2DGame extends FlameGame {
  Forge2DGame({Vector2? gravity, double zoom = 10, CameraComponent? camera, Forge2DWorld? world, List<Component>? children})
      : super(world: world ?? Forge2DWorld(gravity: gravity), camera: camera, children: children) {
    this.camera.viewfinder.zoom = zoom;
  }

  Vector2 screenToWorld(Vector2 p) => __flTelaParaMundo(this, p);
  Vector2 worldToScreen(Vector2 p) => __flMundoParaTela(this, p);
}

// ---- juntas
class JointDef {
  Body? bodyA;
  Body? bodyB;
  Vector2 localAnchorA = Vector2.zero();
  Vector2 localAnchorB = Vector2.zero();
  bool collideConnected = false;
  dynamic userData;
}

class RevoluteJointDef extends JointDef {
  double referenceAngle = 0;
  bool enableLimit = false;
  double lowerAngle = 0;
  double upperAngle = 0;
  bool enableMotor = false;
  double motorSpeed = 0;
  double maxMotorTorque = 0;

  void initialize(Body a, Body b, Vector2 ancora) {
    bodyA = a;
    bodyB = b;
    localAnchorA = a.localPoint(ancora);
    localAnchorB = b.localPoint(ancora);
    referenceAngle = b.angle - a.angle;
  }
}

class WeldJointDef extends JointDef {
  double referenceAngle = 0;
  double frequencyHz = 0;
  double dampingRatio = 0;

  void initialize(Body a, Body b, Vector2 ancora) {
    bodyA = a;
    bodyB = b;
    localAnchorA = a.localPoint(ancora);
    localAnchorB = b.localPoint(ancora);
    referenceAngle = b.angle - a.angle;
  }
}

class DistanceJointDef extends JointDef {
  double length = 1;
  double frequencyHz = 0;
  double dampingRatio = 0;

  void initialize(Body a, Body b, Vector2 ancoraA, Vector2 ancoraB) {
    bodyA = a;
    bodyB = b;
    localAnchorA = a.localPoint(ancoraA);
    localAnchorB = b.localPoint(ancoraB);
    length = ancoraA.distanceTo(ancoraB);
  }
}

class RopeJointDef extends JointDef {
  double maxLength = 1;
}

class PrismaticJointDef extends JointDef {
  Vector2 localAxisA = Vector2(1, 0);
  double referenceAngle = 0;
  bool enableLimit = false;
  double lowerTranslation = 0;
  double upperTranslation = 0;
  bool enableMotor = false;
  double motorSpeed = 0;
  double maxMotorForce = 0;

  void initialize(Body a, Body b, Vector2 ancora, Vector2 eixo) {
    bodyA = a;
    bodyB = b;
    localAnchorA = a.localPoint(ancora);
    localAnchorB = b.localPoint(ancora);
    localAxisA = a.localVector(eixo).normalized();
    referenceAngle = b.angle - a.angle;
  }
}

class MouseJointDef extends JointDef {
  Vector2 target = Vector2.zero();
  double maxForce = 0;
  double frequencyHz = 5;
  double dampingRatio = 0.7;
}

class Joint {
  dynamic def;
  String tipo;
  bool destruido = false;

  Joint(this.def, this.tipo);

  Body get bodyA => def.bodyA;
  Body get bodyB => def.bodyB;
  Vector2 get anchorA => tipo == 'mouse' ? def.target.clone() : bodyA.worldPoint(def.localAnchorA);
  Vector2 get anchorB => bodyB.worldPoint(def.localAnchorB);
  dynamic get userData => def.userData;
  double get jointAngle => bodyB.angle - bodyA.angle - def.referenceAngle;
  double get jointSpeed => bodyB.angularVelocity - bodyA.angularVelocity;
  double get motorSpeed => def.motorSpeed;
  bool get isMotorEnabled => def.enableMotor;
  bool get isLimitEnabled => def.enableLimit;
  double get length => def.length;
  Vector2 get target => def.target;

  void setMotorSpeed(double v) {
    def.motorSpeed = v;
  }

  void enableMotor(bool v) {
    def.enableMotor = v;
  }

  void enableLimit(bool v) {
    def.enableLimit = v;
  }

  void setLimits(double inferior, double superior) {
    if (tipo == 'prismatic') {
      def.lowerTranslation = inferior;
      def.upperTranslation = superior;
    } else {
      def.lowerAngle = inferior;
      def.upperAngle = superior;
    }
  }

  void setMaxMotorTorque(double v) {
    def.maxMotorTorque = v;
  }

  void setMaxMotorForce(double v) {
    def.maxMotorForce = v;
  }

  void setTarget(Vector2 alvo) {
    def.target = alvo.clone();
  }

  void setLength(double v) {
    def.length = v;
  }
}

class RevoluteJoint extends Joint {
  RevoluteJoint(RevoluteJointDef d) : super(d, 'revolute');
}

class WeldJoint extends Joint {
  WeldJoint(WeldJointDef d) : super(d, 'weld');
}

class DistanceJoint extends Joint {
  DistanceJoint(DistanceJointDef d) : super(d, 'distance');
}

class RopeJoint extends Joint {
  RopeJoint(RopeJointDef d) : super(d, 'rope');
}

class PrismaticJoint extends Joint {
  PrismaticJoint(PrismaticJointDef d) : super(d, 'prismatic');
}

class MouseJoint extends Joint {
  MouseJoint(MouseJointDef d) : super(d, 'mouse');
}

abstract class RayCastCallback {
  double reportFixture(Fixture fixture, Vector2 point, Vector2 normal, double fraction);
}

mixin ContactCallbacks {
  void beginContact(Object other, dynamic contact) {}
  void endContact(Object other, dynamic contact) {}
}

class BodyComponent extends PositionComponent {
  late Body body;
  Paint paint;
  bool renderBody = true;
  BodyDef? bodyDef;
  List<FixtureDef>? fixtureDefs;

  BodyComponent({Paint? paint, List<Component>? children, int? priority, bool? renderBody, BodyDef? bodyDef, List<FixtureDef>? fixtureDefs})
      : paint = paint ?? (Paint()..color = const Color(0xFFFFFFFF)),
        renderBody = renderBody ?? true,
        bodyDef = bodyDef,
        fixtureDefs = fixtureDefs,
        super(children: children, priority: priority);

  Forge2DWorld get world => __b2Mundo(this);
  CameraComponent get camera => game.camera;
  Vector2 get center => body.worldCenter;

  Body createBody() {
    final b = world.createBody(bodyDef ?? BodyDef());
    final defs = fixtureDefs;
    if (defs != null) {
      for (final f in defs) {
        b.createFixture(f);
      }
    }
    return b;
  }

  @override
  Future<void> onLoad() async {
    body = createBody();
    body.componente = this;
    if (body.userData == null) {
      body.userData = this;
    }
    position = body.position;
    angle = body.angle;
  }

  @override
  void onRemove() {
    world.destroyBody(body);
  }

  @override
  void render(Canvas canvas) {
    if (renderBody) {
      __b2Desenhar(this, canvas);
    }
  }
}

// ---------------------------------------------------------------- Tiled
class TiledObject {
  int id;
  String name;
  String type;
  double x;
  double y;
  double width;
  double height;
  double rotation;
  int gid;
  Map<String, dynamic> properties;

  TiledObject(List<dynamic> d)
      : id = d[0],
        name = d[1],
        type = d[2],
        x = d[3],
        y = d[4],
        width = d[5],
        height = d[6],
        rotation = d[7],
        gid = d[8],
        properties = __tlProps(d[9]);

  String get className => type;
  String get class_ => type;
  bool get isRectangle => gid == 0;
  bool get isPoint => width == 0 && height == 0;
  Vector2 get position => Vector2(x, y);
  Vector2 get size => Vector2(width, height);
}

class ObjectGroup {
  String name;
  bool visible = true;
  List<TiledObject> objects = [];

  ObjectGroup(this.name, List<dynamic> lista) {
    for (final o in lista) {
      objects.add(TiledObject(o));
    }
  }
}

class TileLayer {
  String name;
  bool visible = true;
  int width;
  int height;
  List<int> data;

  TileLayer(this.name, this.width, this.height, this.data);

  int tileAt(int x, int y) => data[y * width + x];
}

class TiledMap {
  int width;
  int height;
  int tileWidth;
  int tileHeight;
  List<dynamic> layers = [];

  TiledMap(this.width, this.height, this.tileWidth, this.tileHeight);

  dynamic layerByName(String nome) {
    for (final l in layers) {
      if (l.name == nome) return l;
    }
    return null;
  }
}

class RenderableTiledMap {
  TiledMap map;
  Vector2 destTileSize;
  dynamic dados;

  RenderableTiledMap(this.map, this.destTileSize, this.dados);

  dynamic getLayer(String nome) => map.layerByName(nome);
  bool get isometric => __tlIso(this);
}

class TiledComponent extends PositionComponent {
  RenderableTiledMap tileMap;

  TiledComponent(RenderableTiledMap mapa, {Vector2? position, int? priority})
      : tileMap = mapa,
        super(position: position, size: __tlTamanho(mapa), priority: priority);

  static Future<TiledComponent> load(String arquivo, Vector2 destTileSize, {int? priority, String? prefix}) async {
    final d = __tlCarregar(arquivo);
    final mapa = TiledMap(d[0], d[1], d[2], d[3]);
    for (final c in d[4]) {
      if (c[0] == 'tiles') {
        mapa.layers.add(TileLayer(c[1], d[0], d[1], c[2]));
      } else {
        mapa.layers.add(ObjectGroup(c[1], c[2]));
      }
    }
    return TiledComponent(RenderableTiledMap(mapa, destTileSize.clone(), d[5]), priority: priority);
  }

  double get width => size.x;
  double get height => size.y;

  @override
  void render(Canvas canvas) {
    __tlDesenhar(this, canvas);
  }
}
