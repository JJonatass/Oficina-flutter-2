# Frente 2 da Oficina Flutter 2: entrada para jogos.
# - toque instantâneo (onTapDown no pointerdown) e arrastar (onPan*, onHorizontalDrag*, onVerticalDrag*)
# - teclado: Focus e KeyboardListener com onKeyEvent, HardwareKeyboard.instance no laço
from patch_engine import sub1

# ---------------------------------------------------------------- interpretador
ENGINE = r"""/* ===== Oficina 2: detalhes de gestos e eventos de teclado ===== */
ST.keys=new Set();
function gOff(p){return p?mkOffset(p[0],p[1]):null}
ST.mkGest=function(o){var f={};
  if(o.lp)f.localPosition=gOff(o.lp);if(o.gp)f.globalPosition=gOff(o.gp);
  if(o.d){f.delta=gOff(o.d);f.primaryDelta=o.axis==='h'?new Dbl(o.d[0]):o.axis==='v'?new Dbl(o.d[1]):null}
  if(o.v){f.velocity={nat:'GDetails',f:{pixelsPerSecond:gOff(o.v)},src:'Velocity'};f.primaryVelocity=o.axis==='h'?new Dbl(o.v[0]):o.axis==='v'?new Dbl(o.v[1]):null}
  f.kind={raw:'PointerDeviceKind.touch'};
  return{nat:'GDetails',f:f,src:o.src||'DragUpdateDetails'}};
ST.mkKey=function(kind,code,ch){return{nat:'KeyEvt',kind:kind,code:code,ch:ch,f:{},src:kind+'(LogicalKeyboardKey.'+code+')'}};
var HWKB={nat:'HwKb',f:{},src:'HardwareKeyboard.instance'};
function keyName(k){var r=isRaw(k)?k.raw:(typeof k==='string'?k:'');var m=/(?:LogicalKeyboardKey|PhysicalKeyboardKey)\.(\w+)/.exec(r);return m?m[1]:null}
function hwHas(n){return ST.keys.has(n)}
"""

NAT = r"""  if(v.nat==='GDetails'){if(hasOwn(v.f,name))return v.f[name];if(name==='sourceTimeStamp')return null}
  if(v.nat==='KeyEvt'){
    switch(name){
      case 'logicalKey':return{raw:'LogicalKeyboardKey.'+v.code};
      case 'physicalKey':return{raw:'PhysicalKeyboardKey.'+v.code};
      case 'character':return v.kind==='KeyUpEvent'?null:v.ch;
      case 'timeStamp':return{raw:'Duration(milliseconds: '+Math.round(ST.now())+')'};
      case 'synthesized':return false;
      case 'runtimeType':return v.kind;
      case 'toString':return v.src}}
  if(v.nat==='HwKb'){
    switch(name){
      case 'isLogicalKeyPressed':case 'isPhysicalKeyPressed':return hwHas(keyName(args[0]));
      case 'isShiftPressed':return hwHas('shiftLeft')||hwHas('shiftRight');
      case 'isControlPressed':return hwHas('controlLeft')||hwHas('controlRight');
      case 'isAltPressed':return hwHas('altLeft')||hwHas('altRight');
      case 'isMetaPressed':return hwHas('metaLeft')||hwHas('metaRight');
      case 'addHandler':case 'removeHandler':return null}}
"""

# ---------------------------------------------------------------- interface (eventos do navegador)
UI = r"""/* ===== Oficina 2: toque instantâneo, arrastar e teclado ===== */
var G_TAP=['onTapDown','onTapUp'],G_PAN=['onPanDown','onPanStart','onPanUpdate','onPanEnd'],
  G_H=['onHorizontalDragStart','onHorizontalDragUpdate','onHorizontalDragEnd'],G_V=['onVerticalDragStart','onVerticalDragUpdate','onVerticalDragEnd'];
function gRaw(el,name){var r=el&&el._n&&M.rawProp(el._n,name);return r&&r.trim()!=='null'?r:null}
function gHas(el,names){for(var i=0;i<names.length;i++)if(gRaw(el,names[i]))return true;return false}
function gFind(start,names){for(var el=start&&start.closest&&start.closest('.hh');el;el=el.parentElement&&el.parentElement.closest('.hh'))if(gHas(el,names))return el;return null}
function gLive(el){if(el.isConnected)return el;var p=el.dataset.path;return (p&&screen.querySelector('.hh[data-path="'+p.replace(/"/g,'')+'"]'))||el}
function gPos(el,e){var sr=screen.getBoundingClientRect(),k=sr.width/360||1,rc=gLive(el).getBoundingClientRect();return{l:[(e.clientX-rc.left)/k,(e.clientY-rc.top)/k],g:[(e.clientX-sr.left)/k,(e.clientY-sr.top)/k],k:k}}
function gLoop(){return (ST.anims||[]).some(function(v){return v.nat==='Ticker'||v.nat==='Timer'})}
/* com o laço do jogo rodando, o próximo quadro já redesenha: não precisa desenhar a tela de novo a cada evento */
function gRun(el,raw,args){var r=runAt(el,raw,args);if(r.err||(r.fx&&r.fx.length)||!gLoop())afterRun(r);else if(r.dirty&&typeof animKick==='function')animKick();return r}
var gDrag=null,gTapEl=null,gSup=false;
screen.addEventListener('pointerdown',function(e){
  if(!(S.run&&ST.active))return;
  if(e.button!==undefined&&e.button>0)return;
  gTapEl=gFind(e.target,G_TAP);
  if(gTapEl){var rd=gRaw(gTapEl,'onTapDown');if(rd){var p0=gPos(gTapEl,e);gRun(gTapEl,rd,[ST.mkTap(p0.l[0],p0.l[1],p0.g[0],p0.g[1])])}}
  var de=gFind(e.target,G_PAN.concat(G_H,G_V));
  if(de){var p1=gPos(de,e);gDrag={el:de,id:e.pointerId,start:p1,last:p1,started:false,axis:gHas(de,G_PAN)?'p':gHas(de,G_H)?'h':'v',hist:[[performance.now(),p1.g]]};
    try{screen.setPointerCapture(e.pointerId)}catch(x){}
    var pd=gRaw(de,'onPanDown');if(pd)gRun(de,pd,[ST.mkGest({lp:p1.l,gp:p1.g,src:'DragDownDetails'})])}
});
screen.addEventListener('pointermove',function(e){
  var d=gDrag;if(!d||e.pointerId!==d.id||!(S.run&&ST.active))return;
  var p=gPos(d.el,e),dx=p.g[0]-d.last.g[0],dy=p.g[1]-d.last.g[1];
  if(!d.started){var tx=p.g[0]-d.start.g[0],ty=p.g[1]-d.start.g[1],slop=e.pointerType==='mouse'?2:8;
    var go=d.axis==='p'?Math.hypot(tx,ty)>=slop:d.axis==='h'?Math.abs(tx)>=slop&&Math.abs(tx)>=Math.abs(ty):Math.abs(ty)>=slop&&Math.abs(ty)>=Math.abs(tx);
    if(!go)return;
    d.started=true;gSup=true;
    var sn=d.axis==='p'?'onPanStart':d.axis==='h'?'onHorizontalDragStart':'onVerticalDragStart',sr=gRaw(d.el,sn);
    if(sr)gRun(d.el,sr,[ST.mkGest({lp:d.start.l,gp:d.start.g,src:'DragStartDetails'})]);
    dx=p.g[0]-d.start.g[0];dy=p.g[1]-d.start.g[1]}
  if(d.axis==='h')dy=0;if(d.axis==='v')dx=0;
  d.last=p;d.hist.push([performance.now(),p.g]);if(d.hist.length>8)d.hist.shift();
  var un=d.axis==='p'?'onPanUpdate':d.axis==='h'?'onHorizontalDragUpdate':'onVerticalDragUpdate',ur=gRaw(d.el,un);
  if(ur&&(dx||dy))gRun(d.el,ur,[ST.mkGest({lp:p.l,gp:p.g,d:[dx,dy],axis:d.axis,src:'DragUpdateDetails'})]);
});
function gEnd(e,cancel){
  var d=gDrag;
  if(d&&e.pointerId===d.id){gDrag=null;
    if(d.started&&S.run&&ST.active){
      var h=d.hist,now=performance.now(),a=h[0];for(var i=0;i<h.length;i++)if(now-h[i][0]<=100){a=h[i];break}
      var b=h[h.length-1],dt=Math.max(1,b[0]-a[0])/1000,vx=(b[1][0]-a[1][0])/dt,vy=(b[1][1]-a[1][1])/dt;
      if(d.axis==='h')vy=0;if(d.axis==='v')vx=0;
      var en=d.axis==='p'?'onPanEnd':d.axis==='h'?'onHorizontalDragEnd':'onVerticalDragEnd',er=gRaw(d.el,en);
      if(er)gRun(d.el,er,[ST.mkGest({v:[vx,vy],axis:d.axis,src:'DragEndDetails'})]);
      gTapEl=null;return}}
  var t=gTapEl;gTapEl=null;
  if(t&&!cancel&&S.run&&ST.active){var ru=gRaw(t,'onTapUp');if(ru){var p=gPos(t,e);gRun(t,ru,[ST.mkTap(p.l[0],p.l[1],p.g[0],p.g[1])])}}
}
screen.addEventListener('pointerup',function(e){gEnd(e,false)});
screen.addEventListener('pointercancel',function(e){gEnd(e,true)});
/* depois de um arrasto, o clique que o navegador dispara não vira onTap */
screen.addEventListener('click',function(e){if(gSup){gSup=false;e.stopPropagation();e.preventDefault()}},true);

/* teclado: Focus(onKeyEvent) e KeyboardListener(onKeyEvent) recebem as teclas quando o foco não está no editor */
function kName(e){var c=e.code||'';if(!c){if(e.key===' ')return 'space';c=e.key||''}return c.charAt(0).toLowerCase()+c.slice(1)}
function kTarget(){var a=document.activeElement;return !(a&&(a.tagName==='TEXTAREA'||a.tagName==='INPUT'||a.tagName==='SELECT'||a.isContentEditable))}
function kDispatch(kind,e){
  if(!(S.run&&ST.active))return false;
  var els=[].slice.call(screen.querySelectorAll('.kbd')).reverse(),done=false,code=kName(e);
  els.forEach(function(el){var raw=gRaw(el,'onKeyEvent');if(!raw)return;done=true;
    var ev=ST.mkKey(kind,code,e.key&&e.key.length===1?e.key:null);
    gRun(el,raw,el._n.type==='Focus'?[{nat:'#focusNode',f:{},src:'FocusNode()'},ev]:[ev])});
  return done}
window.addEventListener('keydown',function(e){
  if(!(S.run&&ST.active)||!kTarget())return;
  var n=kName(e);ST.keys.add(n);
  var used=kDispatch(e.repeat?'KeyRepeatEvent':'KeyDownEvent',e);
  if((used||gLoop())&&/^(arrow\w+|space)$/.test(n))e.preventDefault()});
window.addEventListener('keyup',function(e){
  var n=kName(e);ST.keys.delete(n);
  if(!(S.run&&ST.active)||!kTarget())return;
  kDispatch('KeyUpEvent',e)});
window.addEventListener('blur',function(){ST.keys.clear()});
"""


def patch(src):
    src = sub1(src, "function mkDur(ms){", ENGINE + "function mkDur(ms){", 'input engine helpers')
    src = sub1(src, "  if(v.nat==='Random'){\n", NAT + "  if(v.nat==='Random'){\n", 'input natMember')
    # event is KeyDownEvent / KeyUpEvent / KeyRepeatEvent / KeyEvent
    src = sub1(src,
        "    case 'Set':return !!v.isSet}\n  return !!v.cls&&isSub(v.cls,ty)}",
        "    case 'Set':return !!v.isSet}\n"
        "  if(v.nat==='KeyEvt')return ty==='KeyEvent'||ty===v.kind||(ty==='RawKeyEvent')||(ty==='RawKeyDownEvent'&&v.kind!=='KeyUpEvent')||(ty==='RawKeyUpEvent'&&v.kind==='KeyUpEvent');\n"
        "  return !!v.cls&&isSub(v.cls,ty)}",
        'isType KeyEvt')
    # HardwareKeyboard.instance(.isLogicalKeyPressed(...))
    src = sub1(src,
        "      if(a.args&&(a.name==='Timer.periodic'||a.name==='Timer')){",
        "      if(!a.args&&(a.name==='Offset.zero'||a.name==='Size.zero'))return a.name==='Offset.zero'?mkOffset(0,0):mkSize(0,0);\n"
        "      if(a.name.indexOf('HardwareKeyboard.instance')===0){var hwr=a.name.split('.').slice(2);if(!hwr.length&&!a.args)return HWKB;if(hwr.length===1)return natMember(HWKB,hwr[0],a.args?evalArgs(a,env).map(function(x){return x.val}):[])}\n"
        "      if(a.args&&(a.name==='Timer.periodic'||a.name==='Timer')){",
        'HardwareKeyboard ctor')
    src = sub1(src,
        "ST.reset=function(){\n",
        "ST.reset=function(){\n  if(ST.keys)ST.keys.clear();\n",
        'reset keys')

    # widgets: KeyboardListener existe no catálogo e no desenho (sem mudar o visual, como o Focus)
    src = sub1(src,
        " Focus:{cat:'struct',slots:{child:'one'},",
        " KeyboardListener:{cat:'struct',slots:{child:'one'},desc:'Recebe as teclas do teclado físico em onKeyEvent, com focusNode e autofocus. Não muda o desenho.'},\n"
        " Focus:{cat:'struct',slots:{child:'one'},",
        'schema KeyboardListener')
    src = sub1(src,
        "    case 'SafeArea':case 'GestureDetector':case 'InkWell':case 'Form':case 'FittedBox':{",
        "    case 'SafeArea':case 'GestureDetector':case 'InkWell':case 'Form':case 'FittedBox':case 'Focus':case 'KeyboardListener':{",
        'render Focus')
    src = sub1(src,
        "var HANDLERS=['onPressed','onTap','onLongPress','onDoubleTap','onChanged','onSelected','onTapDown','onTapUp'];",
        "var HANDLERS=['onPressed','onTap','onLongPress','onDoubleTap','onChanged','onSelected','onTapDown','onTapUp','onPanDown','onPanStart','onPanUpdate','onPanEnd','onHorizontalDragStart','onHorizontalDragUpdate','onHorizontalDragEnd','onVerticalDragStart','onVerticalDragUpdate','onVerticalDragEnd'];",
        'HANDLERS')
    src = sub1(src,
        "  if(n.type==='Listener'||n.type==='MouseRegion'){d.classList.add('ptr');d.style.alignSelf='stretch'}\n",
        "  if(n.type==='Listener'||n.type==='MouseRegion'){d.classList.add('ptr');d.style.alignSelf='stretch'}\n"
        "  if((n.type==='Focus'||n.type==='KeyboardListener')&&M.rawProp(n,'onKeyEvent'))d.classList.add('kbd');\n"
        "  if(/^\\s*\\S/.test(M.rawProp(n,'onPanUpdate')||M.rawProp(n,'onHorizontalDragUpdate')||M.rawProp(n,'onVerticalDragUpdate')||M.rawProp(n,'onPanStart')||''))d.style.touchAction='none';\n",
        'bindRun kbd/touch')
    # o clique genérico não executa onTapDown/onTapUp nem os de arrasto (eles têm detalhes próprios)
    src = sub1(src,
        "  if(h==='onTapDown'||h==='onTapUp')return;",
        "  if(h==='onTapDown'||h==='onTapUp'||/^on(Pan|HorizontalDrag|VerticalDrag)/.test(h))return;",
        'click skip drag')
    # o antigo onTapDown no clique sai; entra o código novo de gestos e teclado
    src = sub1(src,
        "/* toque com posição: onTapDown / onTapUp recebem details.localPosition */\nscreen.addEventListener('click',function(e){",
        UI + "/* (antigo onTapDown no clique, desligado) */\nscreen.addEventListener('oficina-old-tap',function(e){",
        'old tap')
    return src
