# Aplica ao simulador original (tools/upstream.html) os recursos de jogo da Oficina Flutter 2.
# Cada trecho-âncora precisa aparecer exatamente uma vez; se o original mudar, o script avisa.

def sub1(src, old, new, label):
    n = src.count(old)
    if n != 1:
        raise SystemExit(f'[patch_engine] âncora "{label}" encontrada {n} vezes')
    return src.replace(old, new, 1)


HELPERS = r"""/* ===== Oficina 2: laço de jogo (Ticker e Timer) ===== */
function methodOf(cn,nm){var seen=0;while(cn&&seen++<20){var dc=ST.dataClasses[cn];if(!dc)return null;if(dc.methods[nm])return dc.methods[nm];var w=(dc.withs||[]).slice().reverse();for(var i=0;i<w.length;i++){var wc=ST.dataClasses[w[i]];if(wc&&wc.methods[nm])return wc.methods[nm]}cn=dc.ext}return null}
function cbArg(ast,env){
  if(ast&&ast.t==='id'){var nm=ast.name;
    if(!(env.params&&hasOwn(env.params,nm))&&!(env.locals&&hasOwn(env.locals,nm))){
      var sf=env.self||curThis(env),mm=sf&&sf.cls?methodOf(sf.cls,nm):null;
      /* o método é procurado na hora da chamada: editar o código com o jogo rodando usa a versão nova (como o hot reload) */
      if(mm)return{lam:true,src:nm,pn:[],call:function(args){return runMethod(methodOf(sf.cls,nm)||mm,args,sf)}};
      if(ST.methods[nm])return{lam:true,src:nm,pn:[],call:function(args){var m=ST.methods[nm];if(!m)throw new Error('método '+nm+' não existe mais');return runMethod(m,args,null)}}}}
  return ev(ast,env)}
function mkTicker(cb){return{nat:'Ticker',f:{},tk:{cb:cb,on:false,t0:0},src:'Ticker()'}}
function mkTimer(ms,cb,per){var t={nat:'Timer',f:{},tm:{ms:Math.max(per?16:0,ms||0),cb:cb,per:per,next:ST.now()+Math.max(per?16:0,ms||0),on:true,n:0},src:'Timer()'};ST.anims.push(t);return t}
function animDrop(v){var ix=ST.anims.indexOf(v);if(ix>=0)ST.anims.splice(ix,1)}
function gameStep(v,now){
  if(v.nat==='Ticker'){
    if(!v.tk.on){animDrop(v);return false}
    steps=0;try{callLam(v.tk.cb,[{raw:'Duration(microseconds: '+Math.round((now-v.tk.t0)*1000)+')'}])}
    catch(e){v.tk.on=false;animDrop(v);ST.tickErr={msg:e.message,exc:!!e.dartExc,src:'Ticker'}}
    return true}
  var tm=v.tm;
  if(!tm.on){animDrop(v);return false}
  if(now<tm.next)return false;
  steps=0;tm.n++;
  if(tm.per){tm.next+=tm.ms;if(tm.next<now)tm.next=now+tm.ms}else{tm.on=false;animDrop(v)}
  try{callLam(tm.cb,tm.per?[v]:[])}
  catch(e){tm.on=false;animDrop(v);ST.tickErr={msg:e.message,exc:!!e.dartExc,src:'Timer'}}
  return true}
"""

NAT_MEMBERS = r"""  if(v.nat==='Ticker'){
    switch(name){
      case 'start':if(!v.tk.on){v.tk.on=true;v.tk.t0=ST.now();if(ST.anims.indexOf(v)<0)ST.anims.push(v)}return null;
      case 'stop':case 'dispose':v.tk.on=false;animDrop(v);return null;
      case 'isActive':case 'isTicking':return v.tk.on;
      case 'muted':return false}}
  if(v.nat==='Timer'){
    switch(name){
      case 'cancel':v.tm.on=false;animDrop(v);return null;
      case 'isActive':return v.tm.on;
      case 'tick':return v.tm.n}}
"""

CANVAS_FN = r"""/* ===== Oficina 2: CustomPaint desenhado num <canvas> (bem mais rápido que SVG a cada quadro) ===== */
var P2D={};var P2Dn=0;
function p2d(d){var p=P2D[d];if(!p){if(++P2Dn>600){P2D={};P2Dn=0}p=P2D[d]=new Path2D(d)}return p}
function paintCanvas(res,w,h){
  var dpr=Math.min(2,window.devicePixelRatio||1),cv=document.createElement('canvas');
  cv.width=Math.max(1,Math.round(w*dpr));cv.height=Math.max(1,Math.round(h*dpr));
  cv.style.width=w+'px';cv.style.height=h+'px';cv.style.display='block';
  var g=cv.getContext('2d');if(!g)return cv;
  var cache={};function css(c){return cache[c]||(cache[c]=pcssColor(c))}
  res.ops.forEach(function(o){
    var p=o.p||{color:'#000',style:'fill',sw:0,cap:'butt',join:'miter'},col=css(p.color),m=o.m,stroke=p.style==='stroke'&&!o.pt;
    g.save();
    if(o.clip>=0&&res.clips[o.clip]){var c=res.clips[o.clip];g.setTransform(dpr,0,0,dpr,0,0);g.transform(c.m[0],c.m[1],c.m[2],c.m[3],c.m[4],c.m[5]);g.clip(p2d(c.d))}
    g.setTransform(dpr,0,0,dpr,0,0);g.transform(m[0],m[1],m[2],m[3],m[4],m[5]);
    g.fillStyle=col;g.strokeStyle=col;g.lineWidth=p.sw||1;g.lineCap=p.cap||'butt';g.lineJoin=p.join||'miter';
    function paint(){if(stroke)g.stroke();else g.fill()}
    switch(o.k){
      case 'circle':g.beginPath();g.arc(o.cx,o.cy,Math.max(0,o.r),0,Math.PI*2);paint();break;
      case 'line':g.beginPath();g.moveTo(o.x1,o.y1);g.lineTo(o.x2,o.y2);g.stroke();break;
      case 'rect':if(stroke)g.strokeRect(o.x,o.y,o.w,o.h);else g.fillRect(o.x,o.y,o.w,o.h);break;
      case 'rrect':{g.beginPath();var r=Math.max(0,Math.min(o.r||0,Math.abs(o.w)/2,Math.abs(o.h)/2));if(g.roundRect)g.roundRect(o.x,o.y,o.w,o.h,r);else g.rect(o.x,o.y,o.w,o.h);paint();break}
      case 'oval':g.beginPath();g.ellipse(o.cx,o.cy,Math.max(0,o.rx),Math.max(0,o.ry),0,0,Math.PI*2);paint();break;
      case 'path':if(o.d){if(stroke)g.stroke(p2d(o.d));else g.fill(p2d(o.d))}break;
      case 'color':g.fillRect(-5000,-5000,10000,10000);break;
      case 'text':{g.fillStyle=css(o.color);g.font=(o.bold?'700 ':'')+o.size+'px Roboto,Arial,sans-serif';g.textBaseline='top';
        String(o.text).split('\n').forEach(function(t,i){g.fillText(t,o.x,o.y+i*o.size*1.2)});break}}
    g.restore()});
  return cv}
"""


def patch(src):
    # createTicker(callback) dentro de um State com SingleTickerProviderStateMixin
    src = sub1(src,
        "    case 'fn':{\n      var av=a.args.map(",
        "    case 'fn':{\n      if(a.name==='createTicker'&&a.args.length&&a.args[0].ast!==undefined)return mkTicker(cbArg(a.args[0].ast,env));\n      var av=a.args.map(",
        'fn createTicker')
    # Timer.periodic(duração, (t) {...}) e Timer(duração, () {...})
    src = sub1(src,
        "      if(a.args&&NATCTOR[a.name])return natCtor(a.name,evalArgs(a,env));",
        "      if(a.args&&(a.name==='Timer.periodic'||a.name==='Timer')){var tpa=a.args.filter(function(x){return !x.name});if(tpa.length<2||tpa[0].ast===undefined||tpa[1].ast===undefined)throw new Error(a.name+' precisa de uma Duration e de uma função');var tdu=durMs(ev(tpa[0].ast,env));return mkTimer(tdu==null?0:tdu,cbArg(tpa[1].ast,env),a.name==='Timer.periodic')}\n"
        "      if(a.args&&NATCTOR[a.name])return natCtor(a.name,evalArgs(a,env));",
        'ctor Timer')
    src = sub1(src, "function mkDur(ms){", HELPERS + "function mkDur(ms){", 'helpers')
    src = sub1(src,
        "  list.forEach(function(v){\n    var c=v.c,t=(now-c.t0)/c.span;changed=true;",
        "  list.forEach(function(v){\n    if(v.nat==='Ticker'||v.nat==='Timer'){if(gameStep(v,now))changed=true;return}\n    var c=v.c,t=(now-c.t0)/c.span;changed=true;",
        'ST.tick')
    src = sub1(src, "  if(v.nat==='Random'){\n", NAT_MEMBERS + "  if(v.nat==='Random'){\n", 'natMember')
    # Rect: overlaps, intersect e translate (colisões AABB)
    src = sub1(src,
        "        case 'outerRect':",
        "        case 'overlaps':{var o2=args[0].f;return nn(f.left)<nn(o2.right)&&nn(o2.left)<nn(f.right)&&nn(f.top)<nn(o2.bottom)&&nn(o2.top)<nn(f.bottom)}\n"
        "        case 'intersect':{var o3=args[0].f,il=Math.max(nn(f.left),nn(o3.left)),it=Math.max(nn(f.top),nn(o3.top)),ir=Math.min(nn(f.right),nn(o3.right)),ib=Math.min(nn(f.bottom),nn(o3.bottom));return mkRect(il,it,ir-il,ib-it)}\n"
        "        case 'translate':return mkRect(nn(f.left)+P(0),nn(f.top)+P(1),nn(f.width),nn(f.height));\n"
        "        case 'outerRect':",
        'Rect')
    # erro dentro do laço de jogo vira aviso na tela, em vez de sumir em silêncio
    src = sub1(src,
        "  var ch=false;try{ch=ST.tick(ST.now())}catch(e){}\n  if(ch)try{patchRender()}catch(e2){}",
        "  var ch=false;try{ch=ST.tick(ST.now())}catch(e){}\n"
        "  if(ST.tickErr){var te=ST.tickErr;ST.tickErr=null;toast((te.exc?'Exceção no ':'Erro no ')+te.src+' (o laço parou): '+te.msg)}\n"
        "  if(ch)try{patchRender()}catch(e2){}",
        'animStep')
    # CustomPaint(size: const Size(largura, altura)) com constantes: avalia a expressão
    src = sub1(src,
        "      if(csz){cw=+csz[1];chh=+(csz[2]||csz[1])}\n",
        "      if(csz){cw=+csz[1];chh=+(csz[2]||csz[1])}\n"
        "      else if(/Size\\b/.test(szr)){try{var szv=OF.ST.value(szr.trim().replace(/^const\\s+/,'')),unw=function(q){return q&&q.v!==undefined?q.v:q};if(szv&&szv.nat==='Size'&&isFinite(unw(szv.f.width))&&isFinite(unw(szv.f.height))){cw=+unw(szv.f.width);chh=+unw(szv.f.height)}}catch(e){}}\n",
        'CustomPaint size')
    # Center e Align soltos dentro de um Stack ocupam o Stack inteiro (como no Flutter)
    src = sub1(src,
        "  if(pt==='Stack'&&n.type!=='Positioned'&&n.type!=='AnimatedPositioned')d.style.gridArea='1 / 1';\n",
        "  if(pt==='Stack'&&n.type!=='Positioned'&&n.type!=='AnimatedPositioned')d.style.gridArea='1 / 1';\n"
        "  if(pt==='Stack'&&(n.type==='Center'||n.type==='Align')){d.style.justifySelf='stretch';d.style.alignSelf='stretch'}\n",
        'Stack Center')
    # getters do State (int get pontos => ...) visíveis no build e nos métodos
    src = sub1(src,
        "    var ci2=pickS.ci;info.stateOf=pickS.of;info.fields=ci2.fields;\n",
        "    var ci2=pickS.ci;info.stateOf=pickS.of;info.fields=ci2.fields;info.sgetters=ci2.getters||{};\n",
        'state getters info')
    src = sub1(src,
        "  info.methods.forEach(function(m){ST.methods[m.name]=m});\n",
        "  info.methods.forEach(function(m){ST.methods[m.name]=m});\n  ST.sgetters=info.sgetters||{};\n",
        'state getters load')
    src = sub1(src,
        "  if(ST.fields[n])return ST.fields[n].value;\n  if(n==='widget')return WIDGETOBJ;\n",
        "  if(ST.fields[n])return ST.fields[n].value;\n"
        "  if(ST.sgetters&&hasOwn(ST.sgetters,n)&&!ST.methods[n]){var sgt=ST.sgetters[n],sge=mkEnv({});if(sgt.arrow)return ev(pTern(new Ps(sgt.body)),sge);stmt(new Ps(sgt.body),sge,true);return sge.ret}\n"
        "  if(n==='widget')return WIDGETOBJ;\n",
        'state getters lookup')
    # em ▶ Testar o rótulo "CustomPaint" some de cima do desenho do jogo
    src = sub1(src,
        "      var cpl=document.createElement('span');cpl.className='cpl';cpl.textContent='CustomPaint';d.appendChild(cpl);\n",
        "      if(!(R_opts.run&&d.classList.contains('cpd'))){var cpl=document.createElement('span');cpl.className='cpl';cpl.textContent='CustomPaint';d.appendChild(cpl)}\n",
        'CustomPaint label')
    # com o laço de jogo rodando, mudar um campo fora do setState é normal: o próximo quadro redesenha
    src = sub1(src,
        "  else if(r.mutated)toast('A variável mudou, mas sem setState() a tela não é redesenhada.');\n",
        "  else if(r.mutated&&!(ST.anims||[]).some(function(v){return v.nat==='Ticker'||v.nat==='Timer'}))toast('A variável mudou, mas sem setState() a tela não é redesenhada.');\n",
        'mutated toast')
    # Limites: o que a trilha de jogos usa e o que ainda não existe
    src = sub1(src,
        "OF.LIMITS=[\n",
        "OF.LIMITS=[\n"
        "{h:'Jogos: o que o simulador já roda',\n"
        " p:'O laço de jogo roda de verdade em ▶ Testar, no ritmo do navegador (em geral 60 quadros por segundo). Ao sair de ▶ Testar ou mudar o código, o laço para e recomeça do initState.',\n"
        " li:[\n"
        " 'Funcionam: Ticker com createTicker (SingleTickerProviderStateMixin), start, stop e dispose; Timer.periodic e Timer, com cancel e isActive; Random; CustomPainter com save, restore, translate, rotate e scale; Rect com overlaps, intersect, deflate, inflate, shift e contains; getters do State.',\n"
        " 'Toque e arrasto: GestureDetector com onTapDown (assim que o dedo encosta), onTapUp, onPanDown, onPanStart, onPanUpdate, onPanEnd e os arrastos horizontal e vertical. Os detalhes trazem localPosition, globalPosition, delta, primaryDelta e velocity.pixelsPerSecond.',\n"
        " 'Teclado: Focus e KeyboardListener com onKeyEvent (KeyDownEvent, KeyUpEvent, KeyRepeatEvent e event.logicalKey) e HardwareKeyboard.instance.isLogicalKeyPressed no laço. Clique no celular antes de usar as teclas.',\n"
        " 'Imagens: rootBundle.load + decodeImageFromList (ou ui.instantiateImageCodec), canvas.drawImage e drawImageRect, e Image.asset. Os sprites prontos ficam em assets/sprites/ (heroi, moeda, slime, nave, explosao, tiro, caixa, coracao, maca, grama, nuvem, ceu, montanhas e colinas, todos .png). Pelo botão 🖼 Sprites você acrescenta imagens suas, que ficam guardadas neste navegador.',\n"
        " 'Som: AudioPlayer com play(AssetSource(...)), setVolume, setReleaseMode(ReleaseMode.loop), pause, resume, stop e dispose (pacote audioplayers) e SystemSound.play. Os sons são sintetizados pelo navegador: sons/pulo.wav, moeda, batida, explosao, tiro, vitoria, derrota, clique, dano e poder. As músicas em loop são musica_aventura, musica_espaco e musica_menu (.mp3). O botão 🔊 Som liga e desliga.',\n"
        " 'Texto no Canvas: TextPainter com cor, tamanho, negrito, itálico, letterSpacing, sombra, contorno (foreground: Paint com stroke) e fonte, incluindo GoogleFonts.pressStart2p, silkscreen, vt323 e bungee. tp.width e tp.height são medidos de verdade.',\n"
        " 'Pinça: GestureDetector com onScaleStart, onScaleUpdate (scale, rotation, focalPoint) e onScaleEnd, com dois dedos na tela de toque ou Ctrl + roda do mouse no computador.',\n"
        " 'build com vários return: if (condição) return TelaA(); antes do return final funciona. Em ✎ Editar aparece a tela do último return; em ▶ Testar, a que vale para o estado atual.',\n"
        " 'Flame (simplificado): FlameGame, GameWidget (com overlayBuilderMap e initialActiveOverlays), Component, PositionComponent, SpriteComponent, SpriteAnimationComponent, TextComponent, RectangleComponent, CircleComponent, TimerComponent e Timer, SpriteSheet, Vector2, Anchor, world e camera (follow, zoom, viewport), debugMode, pauseEngine e resumeEngine, RectangleHitbox e CircleHitbox com HasCollisionDetection e CollisionCallbacks (a rotação conta), TapCallbacks e DragCallbacks com vários dedos, KeyboardEvents, KeyboardHandler, FlameAudio.play, FlameAudio.loop e FlameAudio.bgm.',\n"
        " 'Flame, efeitos e outros: MoveEffect, ScaleEffect, SizeEffect, RotateEffect, OpacityEffect, RemoveEffect e SequenceEffect com EffectController (duration, curve, alternate, reverseDuration, infinite, repeatCount, startDelay); partículas (Particle.generate, CircleParticle, SpriteParticle, AcceleratedParticle, MovingParticle, ComputedParticle e outras) em ParticleSystemComponent; loadParallaxComponent e ParallaxImageData; children.query, whereType, firstChild e componentsAtPoint.',\n"
        " 'Do Flame não existem: Forge2D (física), tiled (mapas do Tiled), joystick e efeitos de cor ou de caminho (ColorEffect, MoveAlongPathEffect).',\n"
        " ]},\n",
        'LIMITS')
    # editar o código com o jogo rodando: o Ticker e o Timer continuam (estado preservado, como no hot reload);
    # se algum campo mudou e o initState roda de novo, os antigos são descartados para não haver dois laços
    src = sub1(src,
        "ST.load=function(info){\n  ST.anims=[];\n",
        "ST.load=function(info){\n  var keepG=(ST.anims||[]).filter(function(v){return v.nat==='Ticker'||v.nat==='Timer'});\n  ST.anims=[];\n",
        'load keep game loop')
    src = sub1(src,
        "  if(fresh&&ST.initState)ST.runInit()};\n",
        "  if(!fresh)keepG.forEach(function(v){if(ST.anims.indexOf(v)<0)ST.anims.push(v)});\n"
        "  else if(keepG.length)ST.order.forEach(function(n){var f=ST.fields[n];f.value=initOf(f)});\n"
        "  if(fresh&&ST.initState)ST.runInit()};\n",
        'load restore game loop')
    # canvas no lugar do SVG
    src = sub1(src, "function paintSvg(res,w,h){", CANVAS_FN + "function paintSvg(res,w,h){", 'paintCanvas fn')
    src = sub1(src,
        "        if(res)lay.innerHTML=paintSvg(res,cw||0,chh||0);return lay}",
        "        if(res){if(OF.useSvg)lay.innerHTML=paintSvg(res,cw||0,chh||0);else lay.appendChild(paintCanvas(res,cw||0,chh||0))}return lay}",
        'paintLayer canvas')
    src = sub1(src,
        "if(res)lay0.innerHTML=paintSvg(res,w,chh)});",
        "if(res){if(OF.useSvg)lay0.innerHTML=paintSvg(res,w,chh);else{lay0.innerHTML='';lay0.appendChild(paintCanvas(res,w,chh))}}});",
        'post canvas')
    # patchRender: o canvas novo é copiado para o que já está na tela (atributos não carregam pixels)
    src = sub1(src,
        "  if(a.tagName==='INPUT'&&document.activeElement!==a&&a.value!==b.value)a.value=b.value;\n  patchKids(a,b)}",
        "  if(a.tagName==='INPUT'&&document.activeElement!==a&&a.value!==b.value)a.value=b.value;\n"
        "  if(a.tagName==='CANVAS'){var gc=a.getContext('2d');if(gc){gc.setTransform(1,0,0,1,0,0);gc.clearRect(0,0,a.width,a.height);gc.drawImage(b,0,0)}if(OF.popSched)OF.popSched();return}\n"
        "  patchKids(a,b)}",
        'patchEl canvas')
    # janela separada (⤢ Janela): copiar também os pixels dos canvas
    src = sub1(src,
        "function popSched(){if(!popRaf)popRaf=requestAnimationFrame(popSync)}\n",
        "function popSched(){if(!popRaf)popRaf=requestAnimationFrame(popSync)}\nOF.popSched=function(){if(popW)popSched()};\n",
        'popSched expose')
    src = sub1(src,
        "  m.innerHTML=screen.innerHTML;\n",
        "  m.innerHTML=screen.innerHTML;\n"
        "  (function(){var ca=screen.querySelectorAll('canvas'),cb=m.querySelectorAll('canvas');for(var k=0;k<ca.length&&k<cb.length;k++){try{cb[k].width=ca[k].width;cb[k].height=ca[k].height;cb[k].getContext('2d').drawImage(ca[k],0,0)}catch(e){}}})();\n",
        'popSync canvas')
    # analisador: o mesmo trecho de código não é tokenizado de novo a cada quadro
    src = sub1(src,
        "function Ps(src){src=provSub(src);this.src=src;this.t=lex(src);this.i=0}",
        "var LEXC=new Map();\nfunction lexC(src){var t=LEXC.get(src);if(!t){if(LEXC.size>4000)LEXC.clear();t=lex(src);LEXC.set(src,t)}return t}\n"
        "function Ps(src){src=provSub(src);this.src=src;this.t=lexC(src);this.i=0}",
        'lex cache')
    # expressões: a árvore de uma expressão é guardada por (tokens, posição); o laço não reanalisa a cada quadro
    src = sub1(src,
        "function pTern(p){var c=pBin(p,0);",
        "var PTC=new WeakMap();\n"
        "function pTern(p){var mt=PTC.get(p.t);if(!mt){mt=new Map();PTC.set(p.t,mt)}var key=p.i*4+(p.noCasc?1:0)+(p.hn?2:0),hit=p.hn?null:mt.get(key);if(hit){p.i=hit.e;return hit.a}var at=pTern0(p);if(!p.hn)mt.set(key,{a:at,e:p.i});return at}\n"
        "function pTern0(p){var c=pBin(p,0);",
        'pTern memo')
    # limite de comandos de desenho por quadro: o canvas aguenta bem mais que o SVG
    src = sub1(src,
        "if(cv.ops.length>4000)throw exc('muitos comandos de desenho (limite 4000)')",
        "if(cv.ops.length>20000)throw exc('muitos comandos de desenho (limite 20000 por quadro)')",
        'ops limit')
    return src
