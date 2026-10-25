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
        " 'Toque: GestureDetector com onTapDown e onTapUp entrega details.localPosition. O simulador entrega o toque quando o clique termina; no celular, onTapDown dispara assim que o dedo encosta.',\n"
        " 'Ainda não existem: arrastar (onPanUpdate), teclado (KeyboardListener, Focus com onKeyEvent), vários dedos ao mesmo tempo, imagens desenhadas no Canvas (drawImage, sprites) e som.',\n"
        " 'O pacote Flame ainda não é simulado: os jogos desta trilha usam só Flutter puro, que é a base do Flame.',\n"
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
    return src
