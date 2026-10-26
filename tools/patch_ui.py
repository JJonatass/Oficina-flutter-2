# Oficina Flutter 2, frente 7d: Listener e MouseRegion com o evento, Draggable completo, curvas exatas,
# animação de entrada e saída no AnimatedList e voo do Hero entre telas.
from patch_engine import sub1

ENGINE = r"""/* ===== Oficina 2: eventos de ponteiro com posição ===== */
ST.mkPtr=function(o){var f={localPosition:mkOffset(o.l[0],o.l[1]),position:mkOffset(o.g[0],o.g[1]),delta:mkOffset(o.d?o.d[0]:0,o.d?o.d[1]:0),
  buttons:o.b||0,kind:{raw:'PointerDeviceKind.'+(o.k||'mouse')},pointer:o.p||1,down:!!o.b,timeStamp:mkDur(o.t||0)};
  return{nat:'GDetails',f:f,src:o.src||'PointerEvent'}};
ST.CURVES=CURVES;
"""

UI = r"""/* ===== Oficina 2: Listener e MouseRegion recebem o evento (posição, delta, botões) ===== */
function ptrEv(el,e,src,last){var p=gPos(el,e),d=last?[(e.clientX-last[0])/p.k,(e.clientY-last[1])/p.k]:[0,0];
  return ST.mkPtr({l:p.l,g:p.g,d:d,b:e.buttons||0,k:e.pointerType==='touch'?'touch':e.pointerType==='pen'?'stylus':'mouse',p:e.pointerId||1,t:e.timeStamp,src:src})}
var ptrUlt=null;
function ptrFireE(start,name,e,src){
  if(!(S.run&&ST.active))return;
  for(var el=start&&start.closest('.ptr');el;el=el.parentElement&&el.parentElement.closest('.ptr')){
    var raw=el._n&&M.rawProp(el._n,name);if(raw&&raw.trim()!=='null'){afterRun(runAt(el,raw,[ptrEv(el,e,src,ptrUlt)]));return}}}
"""

CURVE = r"""function curveCss(raw){var c=/Curves\.(\w+)/.exec(raw||'');c=c?c[1]:'linear';var f=OF.ST.CURVES&&OF.ST.CURVES[c];
  if(f&&CURVE_LIN){var pts=[];for(var i=0;i<=40;i++){var t=i/40;pts.push(+f(t).toFixed(4)+' '+(t*100).toFixed(1)+'%')}return 'linear('+pts.join(', ')+')'}
  return curveCssOld(raw)}
var CURVE_LIN=(function(){try{return window.CSS&&CSS.supports&&CSS.supports('transition-timing-function','linear(0, 0.5 50%, 1)')}catch(e){return false}})();
function curveCssOld(raw){"""

AL_HERO = r"""/* ===== Oficina 2: AnimatedList (entrada e saída) e Hero (voo entre telas) ===== */
var alPend=[];
window.OF_AL=function(tipo,key,idx,ms){try{var nm=null,F=OF.ST.fields||{};Object.keys(F).forEach(function(k){if(F[k].value===key)nm=k});
  var lst=(nm&&screen.querySelector('.list[data-al="'+nm+'"]'))||screen.querySelector('.list[data-al]');var dur=ms||300;
  if(tipo==='rem'&&lst&&lst.children[idx]){var old=lst.children[idx],r=old.getBoundingClientRect();alPend.push({t:'rem',nm:nm,idx:idx,dur:dur,g:old.cloneNode(true),h:r.height})}
  else if(tipo==='ins')alPend.push({t:'ins',nm:nm,idx:idx,dur:dur})}catch(e){}};
function alApply(){if(!alPend.length)return;var P=alPend;alPend=[];
  P.forEach(function(a){var lst=(a.nm&&screen.querySelector('.list[data-al="'+a.nm+'"]'))||screen.querySelector('.list[data-al]');if(!lst||!lst.animate)return;
    if(a.t==='ins'){var c=lst.children[a.idx];if(!c)return;var h=c.getBoundingClientRect().height||48;c.style.overflow='hidden';
      c.animate([{opacity:0,maxHeight:'0px',transform:'translateX(-24px)'},{opacity:1,maxHeight:h+'px',transform:'none'}],{duration:a.dur,easing:'ease-out'}).onfinish=function(){c.style.overflow=''}}
    else{var g=a.g;g.style.pointerEvents='none';g.style.overflow='hidden';var ref=lst.children[a.idx]||null;lst.insertBefore(g,ref);
      var an=g.animate([{opacity:1,maxHeight:a.h+'px'},{opacity:0,maxHeight:'0px'}],{duration:a.dur,easing:'ease-in'});an.onfinish=function(){g.remove()}}})}
function heroMapa(){var m={};screen.querySelectorAll('*').forEach(function(el){if(el._n&&el._n.type==='Hero'){var t=M.rawProp(el._n,'tag');if(t!=null&&!m[t])m[t]={el:el,r:el.getBoundingClientRect()}}});return m}
function rotaSig(){var o=R.opts;return (o.nav?o.nav.length:0)+'|'+(o.nav&&o.nav.length?String(o.nav[o.nav.length-1]).slice(0,200):'')+'|'+(o.rootSrc||'')+'|'+(ST.shellLoc||'')+'|'+(ST.curLoc||'')}
function heroVoo(antes,sig0){try{if(!S.run||rotaSig()===sig0)return;var depois=heroMapa();
  Object.keys(depois).forEach(function(t){var a=antes[t],b=depois[t];if(!a||!b||!b.el.animate)return;var r0=a.r,r1=b.r;if(!r1.width||!r1.height)return;
    var dx=r0.left-r1.left,dy=r0.top-r1.top,sx=r0.width/r1.width,sy=r0.height/r1.height;
    b.el.style.transformOrigin='0 0';b.el.style.position=b.el.style.position||'relative';b.el.style.zIndex='50';
    b.el.animate([{transform:'translate('+dx+'px,'+dy+'px) scale('+sx+','+sy+')'},{transform:'none'}],{duration:300,easing:'cubic-bezier(.4,0,.2,1)'}).onfinish=function(){b.el.style.zIndex=''}})}catch(e){}}
"""


def patch(src):
    src = sub1(src, "/* ===== Oficina 2: curvas, pinça, consultas de componentes ===== */",
               ENGINE + "/* ===== Oficina 2: curvas, pinça, consultas de componentes ===== */", 'ui engine')
    src = sub1(src, "ST.mkDetails=function(v){return{nat:'DragDetails',f:{data:v},src:'DragTargetDetails()'}};",
        "ST.mkDetails=function(v,o){return{nat:'DragDetails',f:{data:v,offset:o?mkOffset(o[0],o[1]):mkOffset(0,0)},src:'DragTargetDetails()'}};", 'mkDetails')
    # DragDetails.offset
    src = sub1(src, "    switch(name){case 'data':return v.f.data;case 'offset':return mkOffset(0,0)}}",
               "    switch(name){case 'data':return v.f.data;case 'offset':return v.f.offset||mkOffset(0,0)}}", 'dragdetails offset')
    # Listener / MouseRegion
    src = sub1(src, "/* Listener e MouseRegion: eventos de ponteiro e de mouse */", UI + "/* Listener e MouseRegion: eventos de ponteiro e de mouse */", 'ui listener fns')
    src = sub1(src,
        "screen.addEventListener('pointerdown',function(e){ptrFire(e.target,'onPointerDown')});\n"
        "screen.addEventListener('pointerup',function(e){ptrFire(e.target,'onPointerUp')});\n"
        "var ptrMv=0;\n"
        "screen.addEventListener('pointermove',function(e){if(e.buttons&&Date.now()-ptrMv>120){ptrMv=Date.now();ptrFire(e.target,'onPointerMove')}});",
        "screen.addEventListener('pointerdown',function(e){ptrUlt=[e.clientX,e.clientY];ptrFireE(e.target,'onPointerDown',e,'PointerDownEvent')});\n"
        "screen.addEventListener('pointerup',function(e){ptrFireE(e.target,'onPointerUp',e,'PointerUpEvent');ptrUlt=null});\n"
        "screen.addEventListener('pointercancel',function(e){ptrFireE(e.target,'onPointerCancel',e,'PointerCancelEvent');ptrUlt=null});\n"
        "var ptrMv=0;\n"
        "screen.addEventListener('pointermove',function(e){if(Date.now()-ptrMv<16)return;ptrMv=Date.now();if(e.buttons)ptrFireE(e.target,'onPointerMove',e,'PointerMoveEvent');else ptrFireE(e.target,'onPointerHover',e,'PointerHoverEvent');"
        "if(!e.buttons){var hv=mrWalk(e.target,'onHover');if(hv)afterRun(runAt(hv,M.rawProp(hv._n,'onHover'),[ptrEv(hv,e,'PointerHoverEvent',ptrUlt)]))}ptrUlt=[e.clientX,e.clientY]});\n"
        "screen.addEventListener('wheel',function(e){if(!(S.run&&ST.active))return;for(var el=e.target.closest&&e.target.closest('.ptr');el;el=el.parentElement&&el.parentElement.closest('.ptr')){var raw=el._n&&M.rawProp(el._n,'onPointerSignal');if(raw&&raw.trim()!=='null'){var pe=ptrEv(el,e,'PointerScrollEvent');pe.f.scrollDelta=mkOffset(e.deltaX,e.deltaY);afterRun(runAt(el,raw,[pe]));return}}});",
        'listener events')
    src = sub1(src,
        "  var h=mrWalk(e.target,'onHover');if(h&&!(h===mrCur))afterRun(runAt(h,M.rawProp(h._n,'onHover'),[]));\n",
        "", 'mouseover hover dup')
    src = sub1(src,
        "  if(mrCur){var ex=M.rawProp(mrCur._n,'onExit');if(ex&&ex.trim()!=='null')afterRun(runAt(mrLive(),ex,[]))}\n"
        "  mrCur=t;if(t)afterRun(runAt(t,M.rawProp(t._n,'onEnter'),[]))});",
        "  if(mrCur){var ex=M.rawProp(mrCur._n,'onExit');if(ex&&ex.trim()!=='null'){var ml=mrLive();afterRun(runAt(ml,ex,[ptrEv(ml,e,'PointerExitEvent')]))}}\n"
        "  mrCur=t;if(t){var en=M.rawProp(t._n,'onEnter');if(en&&en.trim()!=='null')afterRun(runAt(t,en,[ptrEv(t,e,'PointerEnterEvent')]))}});",
        'mouseregion events')
    src = sub1(src,
        "  if(n.type==='Listener'||n.type==='MouseRegion'){d.classList.add('ptr');d.style.alignSelf='stretch'}",
        "  if(n.type==='Listener'||n.type==='MouseRegion'){d.classList.add('ptr');d.style.alignSelf='stretch';"
        "if(n.type==='MouseRegion'){var mcr=String(M.rawProp(n,'cursor')||''),mcm=/SystemMouseCursors\\.(\\w+)/.exec(mcr);if(mcm){var CUR={click:'pointer',basic:'default',text:'text',grab:'grab',grabbing:'grabbing',move:'move',forbidden:'not-allowed',wait:'wait',precise:'crosshair',help:'help',none:'none',zoomIn:'zoom-in',zoomOut:'zoom-out',resizeLeftRight:'ew-resize',resizeUpDown:'ns-resize'};d.style.cursor=CUR[mcm[1]]||'default'}}}",
        'mouseregion cursor')
    # Draggable: deslocamento, onMove e onDragUpdate
    src = sub1(src,
        "  if(dgs){dgs.fl.style.left=(e.clientX-dgs.ox)+'px';dgs.fl.style.top=(e.clientY-dgs.oy)+'px';dgHover(e.clientX,e.clientY)}});",
        "  if(dgs){dgs.fl.style.left=(e.clientX-dgs.ox)+'px';dgs.fl.style.top=(e.clientY-dgs.oy)+'px';dgHover(e.clientX,e.clientY);dgMove(e)}});\n"
        "function dgOff(e){var sr=screen.getBoundingClientRect(),k=sr.width/360||1;return[(e.clientX-dgs.ox-sr.left)/k,(e.clientY-dgs.oy-sr.top)/k]}\n"
        "var dgMv=0,dgLast=null;function dgMove(e){if(!dgs)return;var now=Date.now();if(now-dgMv<30)return;dgMv=now;var off=dgOff(e);dgs.off=off;dgs.lastE=[e.clientX,e.clientY,now];\n"
        "  var sEl=screen.querySelector('[data-dg=\"'+dgs.key+'\"]'),sn=sEl&&sEl._n||dgs.n,up=dgRaw(sn,'onDragUpdate');\n"
        "  if(up){var sr=screen.getBoundingClientRect(),k=sr.width/360||1,dd=dgLast?[(e.clientX-dgLast[0])/k,(e.clientY-dgLast[1])/k]:[0,0];afterRun(runAt(sEl||screen,up,[ST.mkGest({gp:[(e.clientX-sr.left)/k,(e.clientY-sr.top)/k],lp:[dgs.ox/k,dgs.oy/k],d:dd,src:'DragUpdateDetails'})]))}\n"
        "  dgLast=[e.clientX,e.clientY];\n"
        "  if(dgs.hov){var tEl=screen.querySelector('[data-dt=\"'+dgs.hov+'\"]'),mv=tEl&&tEl._n&&dgRaw(tEl._n,'onMove');if(mv)afterRun(runAt(tEl,mv,[ST.mkDetails(dgs.data,off)]))}}",
        'drag move')
    src = sub1(src,
        "    if(ad){afterRun(runAt(tEl,ad,[ST.mkDetails(g.data)]));took=true}",
        "    if(ad){afterRun(runAt(tEl,ad,[ST.mkDetails(g.data,g.off)]));took=true}", 'accept offset')
    src = sub1(src,
        "  if(cb)afterRun(runAt(sEl||screen,cb,took?[]:[null,null]));\n"
        "  if(eb)afterRun(runAt(sEl||screen,eb,[ST.mkDetails(null)]));",
        "  var gOffv=g.off?mkOffsetUI(g.off):null;dgLast=null;\n"
        "  if(cb)afterRun(runAt(sEl||screen,cb,took?[]:[ST.mkGest({src:'Velocity'}),gOffv]));\n"
        "  if(eb){var ed=ST.mkDetails(null,g.off);ed.f.wasAccepted=took;ed.f.velocity={nat:'GDetails',f:{pixelsPerSecond:mkOffsetUI([0,0])},src:'Velocity'};ed.src='DraggableDetails';afterRun(runAt(sEl||screen,eb,[ed]))}",
        'drag end offset')
    src = sub1(src, "function dgEnd(cancel){", "function mkOffsetUI(p){return ST.mkDetails(null,p).f.offset}\nfunction dgEnd(cancel){", 'mkOffsetUI')
    src = sub1(src, "  var g=dgs;dgs=null;g.fl.remove();", "  var g=dgs;dgs=null;g.fl.remove();", 'noop')
    # curvas exatas nas animações implícitas
    src = sub1(src, "function curveCss(raw){", CURVE, 'curve css')
    # AnimatedList e Hero
    src = sub1(src,
        "    case 'ListView.builder':case 'ListView.separated':case 'AnimatedList':{d.className+=' list';",
        "    case 'ListView.builder':case 'ListView.separated':case 'AnimatedList':{d.className+=' list';if(n.type==='AnimatedList'){d.dataset.al=String(M.rawProp(n,'key')||'').trim()||'_'}",
        'al marker')
    src = sub1(src, "function renderCanvas(){\n  R.renderScreen(S.root,S.sel,S.xray,screen);",
        AL_HERO + "var heroUlt=null;\nfunction renderCanvas(){\n  R.renderScreen(S.root,S.sel,S.xray,screen);\n  alApply();if(S.run&&heroUlt)heroVoo(heroUlt.m,heroUlt.s);heroUlt=S.run?{m:heroMapa(),s:rotaSig()}:null;",
        'render hooks')
    src = sub1(src,
        "    if(name==='insertItem'||name==='insertAllItems'){v.st.delta+=name==='insertItem'?1:Math.max(0,nn(args[1])||0);dirty=true;return null}\n"
        "    if(name==='removeItem'||name==='removeAllItems'){v.st.delta-=1;dirty=true;return null}}",
        "    if(name==='insertItem'||name==='insertAllItems'){v.st.delta+=name==='insertItem'?1:Math.max(0,nn(args[1])||0);dirty=true;if(window.OF_AL)OF_AL('ins',v,nn(args[0]),alDur(ARGN,args));return null}\n"
        "    if(name==='removeItem'||name==='removeAllItems'){v.st.delta-=1;dirty=true;if(window.OF_AL)OF_AL('rem',v,nn(args[0]),alDur(ARGN,args));return null}}",
        'al hooks')
    src = sub1(src, "function mkDur(ms){", "function alDur(an,args){var r=300;(an||[]).forEach(function(n,i){if(n==='duration'&&args[i]){var m=/(\\d+)/.exec(show(args[i]));var s=String(pcol(args[i])||show(args[i]));var mm=/milliseconds:\\s*(\\d+)/.exec(s),se=/seconds:\\s*([\\d.]+)/.exec(s);r=mm?+mm[1]:se?+se[1]*1000:r}});return r}\nfunction mkDur(ms){", 'alDur')
    return src
