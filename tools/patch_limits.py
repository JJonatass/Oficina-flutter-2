# Limites trabalhados (Oficina Flutter 2):
# - curvas dos efeitos, opacidade no canvas, children.query/whereType/firstChild/componentsAtPoint
# - overlays do GameWidget (overlayBuilderMap, initialActiveOverlays, game.overlays)
# - música sintetizada em loop (FlameAudio.bgm, AudioPlayer com ReleaseMode.loop)
# - imagens próprias do aluno (painel 🖼 Sprites, guardadas no navegador)
# - gesto de pinça (onScaleStart/Update/End) com dois dedos ou Ctrl + roda do mouse
# - vários return no build: if (cond) return A; ... return B;
from patch_engine import sub1

GLOBAL = r"""/* ===== Oficina 2: imagens do aluno e músicas sintetizadas ===== */
(function(){try{var own=JSON.parse(localStorage.getItem('oficina2.sprites')||'{}');Object.keys(own).forEach(function(k){var s=own[k];if(!s||!s.uri)return;s.own=true;window.OF_SPRITES[k]=s;var im=new Image();im.src=s.uri;window.OF_SPRITE_IMG[k]=im})}catch(e){}})();
window.OF_MUSICAS=['musica_aventura','musica_espaco','musica_menu'];
window.OF_MUSIC=(function(){
  var TR={
    musica_aventura:{bpm:132,wave:'square',lead:'C5 . E5 . G5 . E5 . D5 . F5 . A5 . F5 . C5 . E5 . G5 . C6 . B5 . G5 . D5 . . . E5 . G5 . C6 . G5 . F5 . A5 . C6 . A5 . G5 . E5 . D5 . B4 . C5 . . . . . . .',
      bass:'C3 . . . C3 . . . F2 . . . F2 . . . C3 . . . C3 . . . G2 . . . G2 . . .',drum:'k . h . s . h . k . h . s . h h'},
    musica_espaco:{bpm:100,wave:'triangle',lead:'A4 C5 E5 C5 A4 C5 E5 C5 F4 A4 C5 A4 F4 A4 C5 A4 G4 B4 D5 B4 G4 B4 D5 B4 E4 G#4 B4 G#4 E4 G#4 B4 E5',
      bass:'A2 . . . . . . . F2 . . . . . . . G2 . . . . . . . E2 . . . . . . .',drum:'k . . . h . . . s . . . h . . .'},
    musica_menu:{bpm:84,wave:'sine',lead:'E5 . . G5 . . A5 . G5 . E5 . D5 . . . C5 . . E5 . . G5 . E5 . D5 . C5 . . .',
      bass:'C3 . . . . . . . A2 . . . . . . . F2 . . . . . . . G2 . . . . . . .',drum:'k . . . h . . . k . . . h . . .'}
  };
  function midi(n){var m=/^([A-G])(#|b)?(\d)$/.exec(n);if(!m)return null;var b={C:0,D:2,E:4,F:5,G:7,A:9,B:11}[m[1]]+(m[2]==='#'?1:m[2]==='b'?-1:0);return 440*Math.pow(2,(b+12*(+m[3]+1)-69)/12)}
  Object.keys(TR).forEach(function(k){var t=TR[k];['lead','bass','drum'].forEach(function(f){t[f]=t[f].split(/\s+/)});t.len=Math.max(t.lead.length,t.bass.length,t.drum.length)});
  var ids=0,live={},noiseBuf=null,bgmId=null;
  function noise(c){if(!noiseBuf){var n=c.sampleRate*0.5;noiseBuf=c.createBuffer(1,n,c.sampleRate);var d=noiseBuf.getChannelData(0);for(var i=0;i<n;i++)d[i]=Math.random()*2-1}return noiseBuf}
  function tone(c,out,tp,f,t0,dur,v){var o=c.createOscillator(),g=c.createGain();o.type=tp;o.frequency.setValueAtTime(f,t0);g.gain.setValueAtTime(0.0001,t0);g.gain.exponentialRampToValueAtTime(v,t0+0.01);g.gain.exponentialRampToValueAtTime(0.0001,t0+dur);o.connect(g);g.connect(out);o.start(t0);o.stop(t0+dur+0.02)}
  function drum(c,out,k,t0,v){if(k==='k'){var o=c.createOscillator(),g=c.createGain();o.frequency.setValueAtTime(150,t0);o.frequency.exponentialRampToValueAtTime(45,t0+0.12);g.gain.setValueAtTime(0.5*v,t0);g.gain.exponentialRampToValueAtTime(0.0001,t0+0.14);o.connect(g);g.connect(out);o.start(t0);o.stop(t0+0.16);return}
    var s=c.createBufferSource(),f=c.createBiquadFilter(),g2=c.createGain(),d=k==='s'?0.09:0.03;s.buffer=noise(c);f.type=k==='s'?'bandpass':'highpass';f.frequency.value=k==='s'?1800:6000;g2.gain.setValueAtTime((k==='s'?0.25:0.12)*v,t0);g2.gain.exponentialRampToValueAtTime(0.0001,t0+d);s.connect(f);f.connect(g2);g2.connect(out);s.start(t0);s.stop(t0+d+0.01)}
  function tick(it){var c=it.c;if(!c||it.paused)return;var t=TR[it.name],st=60/t.bpm/4;
    while(it.next<c.currentTime+0.15){var i=it.step;
      if(i>=t.len){if(!it.loop){stop(it.id);return}it.step=i=0}
      var l=t.lead[i%t.lead.length],b=t.bass[i%t.bass.length],d=t.drum[i%t.drum.length];
      if(l&&l!=='.'){var fl=midi(l);if(fl)tone(c,it.out,t.wave,fl,it.next,st*1.8,0.07)}
      if(b&&b!=='.'){var fb=midi(b);if(fb)tone(c,it.out,'triangle',fb,it.next,st*3.5,0.13)}
      if(d&&d!=='.')drum(c,it.out,d,it.next,1);
      it.step++;it.next+=st}}
  function play(name,vol,loop){if(window.OF_EH_MUDO&&window.OF_EH_MUDO())return null;var c=window.OF_AC&&window.OF_AC();if(!c||!TR[name])return null;
    var id=++ids,out=c.createGain();out.gain.value=Math.max(0,Math.min(1,vol==null?1:vol))*0.6;out.connect(c.destination);
    var it={id:id,name:name,loop:!!loop,c:c,out:out,step:0,next:c.currentTime+0.05,paused:false};it.timer=setInterval(function(){tick(it)},30);live[id]=it;tick(it);return id}
  function stop(id){var it=live[id];if(!it)return;clearInterval(it.timer);try{it.out.gain.setTargetAtTime(0,it.c.currentTime,0.02);setTimeout(function(){try{it.out.disconnect()}catch(e){}},200)}catch(e){}delete live[id];if(bgmId===id)bgmId=null}
  function playSfxLoop(name,vol){if(!window.OF_SFX)return null;var id=++ids;var it={id:id,timer:setInterval(function(){window.OF_SFX(name,vol)},700),out:{gain:{setTargetAtTime:function(){}},disconnect:function(){}},c:{currentTime:0}};window.OF_SFX(name,vol);live[id]=it;return id}
  return{play:play,stop:stop,playSfxLoop:playSfxLoop,
    stopAll:function(){Object.keys(live).forEach(function(k){stop(+k)})},
    pause:function(id){if(live[id])live[id].paused=true},
    resume:function(id){var it=live[id];if(!it)return false;if(it.paused){it.paused=false;if(it.c&&it.c.currentTime!=null)it.next=it.c.currentTime+0.05}return true},
    setVolume:function(id,v){var it=live[id];if(it&&it.out&&it.out.gain&&it.c&&it.c.destination)it.out.gain.value=Math.max(0,Math.min(1,v))*0.6},
    bgm:function(name,vol){if(bgmId!=null)stop(bgmId);bgmId=play(name,vol,true);return bgmId},
    bgmStop:function(){if(bgmId!=null)stop(bgmId)},
    bgmPause:function(){if(bgmId!=null&&live[bgmId])live[bgmId].paused=true},
    bgmResume:function(){if(bgmId!=null&&live[bgmId]){live[bgmId].paused=false;live[bgmId].next=live[bgmId].c.currentTime+0.05}}};
})();
"""

ENGINE = r"""/* ===== Oficina 2: curvas, pinça, consultas de componentes ===== */
var TARGS=null;
ST.mkScale=function(o){var f={focalPoint:mkOffset(o.f[0],o.f[1]),localFocalPoint:mkOffset(o.l[0],o.l[1]),pointerCount:o.n||0};
  if(o.kind==='update'){f.scale=new Dbl(o.s);f.horizontalScale=new Dbl(o.s);f.verticalScale=new Dbl(o.s);f.rotation=new Dbl(o.r||0);f.focalPointDelta=mkOffset(o.d[0],o.d[1])}
  if(o.kind==='end'){f.velocity={nat:'GDetails',f:{pixelsPerSecond:mkOffset(0,0)},src:'Velocity'};f.scaleVelocity=new Dbl(0)}
  return{nat:'GDetails',f:f,src:o.kind==='start'?'ScaleStartDetails':o.kind==='end'?'ScaleEndDetails':'ScaleUpdateDetails'}};
function compMember(v,name,args,targs){
  function ok(x){return !targs||isType(x,String(targs[0]).replace(/\?$/,''))}
  var k=Array.isArray(v.f.children)?v.f.children:[];
  switch(name){
    case 'firstChild':{for(var i=0;i<k.length;i++)if(ok(k[i]))return k[i];return null}
    case 'lastChild':{for(var j=k.length-1;j>=0;j--)if(ok(k[j]))return k[j];return null}
    case 'descendants':{var out=[];(function w(c){(c.f.children||[]).forEach(function(x){if(ok(x))out.push(x);w(x)})})(v);return out}
    case 'componentsAtPoint':{var pt=args[0],px=vx(pt),py=vy(pt),res=[];
      (function w(c){(c.f.children||[]).forEach(function(x){w(x);if(flIs(x,'PositionComponent')&&ok(x)){var iv=FL.inv(FL.mat(x));if(iv){var lp=FL.apply(iv,px,py);if(lp[0]>=0&&lp[1]>=0&&lp[0]<vx(x.f.size)&&lp[1]<vy(x.f.size))res.push(x)}}})})(v);
      if(flIs(v,'FlameGame')&&v.f.world)(function w(c){(c.f.children||[]).forEach(function(x){w(x)})})(v.f.world);
      return res}}
  return undefined}
"""

FLN_CURVE = r"""  __flCurve:function(c,p){var t=Math.max(0,Math.min(1,nn(p)));if(c==null)return new Dbl(t);var nm=null;if(c&&c.nat==='Curve')nm=c.f.name;else{var m=/Curves\.(\w+)/.exec(pcol(c)||'');nm=m&&m[1]}var f=CURVES[nm]||CURVES.linear;return new Dbl(f(t))},
"""

UI_SCALE = r"""/* ===== Oficina 2: pinça (onScaleStart/Update/End): dois dedos, ou Ctrl + roda do mouse ===== */
var scG=null,scWheel=null;
function scFind(t){return gFind(t,['onScaleStart','onScaleUpdate','onScaleEnd'])}
function scInfo(){var ids=Object.keys(scG.ptrs),n=ids.length,fx=0,fy=0,lx=0,ly=0,qx=0,qy=0;ids.forEach(function(i){fx+=scG.ptrs[i].g[0];fy+=scG.ptrs[i].g[1];lx+=scG.ptrs[i].l[0];ly+=scG.ptrs[i].l[1];qx+=scG.ptrs[i].c[0];qy+=scG.ptrs[i].c[1]});
  fx/=n;fy/=n;lx/=n;ly/=n;qx/=n;qy/=n;var span=0,ang=0;if(n>=2){var a=scG.ptrs[ids[0]].g,b=scG.ptrs[ids[1]].g;span=Math.hypot(b[0]-a[0],b[1]-a[1]);ang=Math.atan2(b[1]-a[1],b[0]-a[0])}return{n:n,f:[fx,fy],l:[lx,ly],c:[qx,qy],span:span,ang:ang}}
function scFire(kind,o){var r=gRaw(scG.el,kind==='start'?'onScaleStart':kind==='end'?'onScaleEnd':'onScaleUpdate');if(r){o.kind=kind;window.__ofQuietMut=true;try{gRun(scG.el,r,[ST.mkScale(o)])}finally{window.__ofQuietMut=false}}}
function scRestart(){var inf=scInfo();if(scG.started)scFire('end',{f:inf.f,l:inf.l,n:inf.n});scG.started=true;scG.base={span:inf.span,ang:inf.ang};scG.lastF=inf.f;scG.lastC=inf.c;scFire('start',{f:inf.f,l:inf.l,n:inf.n})}
screen.addEventListener('pointerdown',function(e){
  if(!(S.run&&ST.active))return;var el=scFind(e.target);if(!el)return;
  if(!scG||scG.el!==el)scG={el:el,ptrs:{},started:false};var p=gPos(el,e);scG.ptrs[e.pointerId]={g:p.g,l:p.l,c:[e.clientX/p.k,e.clientY/p.k]};
  try{screen.setPointerCapture(e.pointerId)}catch(x){}scRestart()});
screen.addEventListener('pointermove',function(e){
  if(!scG||!scG.ptrs[e.pointerId])return;var p=gPos(scG.el,e);scG.ptrs[e.pointerId]={g:p.g,l:p.l,c:[e.clientX/p.k,e.clientY/p.k]};var inf=scInfo();
  var s=inf.n>=2&&scG.base.span>0?inf.span/scG.base.span:1,r=inf.n>=2?inf.ang-scG.base.ang:0,d=[inf.c[0]-scG.lastC[0],inf.c[1]-scG.lastC[1]];scG.lastF=inf.f;scG.lastC=inf.c;
  scFire('update',{f:inf.f,l:inf.l,n:inf.n,s:s,r:r,d:d})});
function scUp(e){if(!scG||!scG.ptrs[e.pointerId])return;delete scG.ptrs[e.pointerId];
  if(!Object.keys(scG.ptrs).length){scFire('end',{f:scG.lastF,l:scG.lastF,n:0});scG=null}else scRestart()}
screen.addEventListener('pointerup',scUp);screen.addEventListener('pointercancel',scUp);
screen.addEventListener('wheel',function(e){
  if(!(S.run&&ST.active))return;var el=scFind(e.target);if(!el||!gRaw(el,'onScaleUpdate'))return;e.preventDefault();
  var p=gPos(el,e);
  if(!scWheel||scWheel.el!==el){scWheel={el:el,s:1};scG={el:el,ptrs:{},started:true,base:{span:1,ang:0},lastF:p.g};scFire('start',{f:p.g,l:p.l,n:2})}
  scWheel.s*=Math.exp(-e.deltaY/400);scG={el:el,ptrs:{},started:true,base:{span:1,ang:0},lastF:p.g};scFire('update',{f:p.g,l:p.l,n:2,s:scWheel.s,r:0,d:[0,0]});
  clearTimeout(scWheel.t);scWheel.t=setTimeout(function(){if(scWheel&&scWheel.el===el){scG={el:el,ptrs:{},started:true,lastF:p.g};scFire('end',{f:p.g,l:p.l,n:0});scWheel=null;scG=null}},260)},{passive:false});
"""

OVERLAY_FNS = r"""/* ===== Oficina 2: overlays do GameWidget ===== */
function ovSplit(s){var out=[],d=0,q=null,st=0;for(var i=0;i<s.length;i++){var c=s[i];if(q){if(c==='\\'){i++;continue}if(c===q)q=null;continue}if(c==="'"||c==='"'){q=c;continue}
  if('([{'.indexOf(c)>=0)d++;else if(')]}'.indexOf(c)>=0)d--;else if(c===','&&d===0){out.push(s.slice(st,i));st=i+1}}out.push(s.slice(st));return out.filter(function(x){return x.trim()})}
function ovParse(raw){var out={};if(!raw)return out;var s=String(raw).trim().replace(/^const\s+/,'').replace(/^<[^>]*>\s*/,'');if(s[0]!=='{')return out;s=s.slice(1,s.lastIndexOf('}'));
  ovSplit(s).forEach(function(pt){var m=/^\s*(['"])(.*?)\1\s*:\s*([\s\S]*)$/.exec(pt);if(!m)return;var fn=m[3].trim(),pm=/^\(([^)]*)\)\s*(?:=>\s*([\s\S]*)|\{([\s\S]*)\})\s*$/.exec(fn);if(!pm)return;
    var ps=pm[1].split(',').map(function(x){return x.trim().split(/\s+/).pop()}).filter(Boolean),body=pm[2]!==undefined?pm[2].trim():null;
    if(body===null){var rb=pm[3],ri=rb.lastIndexOf('return');if(ri<0)return;body=rb.slice(ri+6).trim()}
    out[m[2]]={ctx:ps[0],game:ps[1],body:body.replace(/;\s*$/,'').trim()}});
  return out}
"""


def patch(src):
    # ---- música e imagens do aluno (script global)
    src = sub1(src, "window.OF_SONS=", GLOBAL + "window.OF_SONS=", 'global music')
    # ---- interpretador
    src = sub1(src, "function mkDur(ms){", ENGINE + "function mkDur(ms){", 'limits engine')
    src = sub1(src, "  __flAdd:function(p,c){return FL.add(p,c)},\n", FLN_CURVE + "  __flAdd:function(p,c){return FL.add(p,c)},\n", 'FLN curve')
    src = sub1(src, "FL.reset=function(){FL.byKey={};FL.live=[];", "FL.reset=function(){if(window.OF_MUSIC)window.OF_MUSIC.stopAll();FL.byKey={};FL.live=[];", 'reset music')
    # chamada genérica: lista.whereType<T>(), children.query<T>(), firstChild<T>()
    src = sub1(src,
        "      var ns=p.is('?.'),name=p.pk(1).v;p.i+=2;var args=null;\n      if(p.is('(')){p.i++;args=pArgs(p)}\n      a={t:'mem',o:a,name:name,args:args,ns:ns}}",
        "      var ns=p.is('?.'),name=p.pk(1).v;p.i+=2;var args=null,targs=null;\n"
        "      if(p.is('<')){var gi0=p.i,gd0=0;for(var gj=p.i;gj<p.t.length;gj++){var tg=p.t[gj];if(tg.k!=='p')continue;if(tg.v==='<')gd0++;else if(tg.v==='>'){gd0--;if(gd0===0){if(p.t[gj+1]&&p.t[gj+1].k==='p'&&p.t[gj+1].v==='('){targs=[p.src.slice(p.t[gi0+1].s,tg.s).trim()];p.i=gj+1}break}}else if(/^[;{})\\]=]$/.test(tg.v)||tg.v==='>>'||tg.v==='&&'||tg.v==='||')break}}\n"
        "      if(p.is('(')){p.i++;args=pArgs(p)}\n      a={t:'mem',o:a,name:name,args:args,ns:ns,targs:targs}}",
        'pPost generics')
    src = sub1(src,
        "      if(a.args)ARGN=a.args.map(function(x){return x.name});\n      try{return member(mo,a.name,margs)}finally{ARGN=null}}",
        "      if(a.args)ARGN=a.args.map(function(x){return x.name});\n      try{TARGS=a.targs||null;return member(mo,a.name,margs)}finally{ARGN=null;TARGS=null}}",
        'ev mem targs')
    src = sub1(src,
        "function member(v,name,args){\n",
        "function member(v,name,args){\n  var targs=TARGS;TARGS=null;\n"
        "  if(v&&v.cls&&ST.dataClasses.Component&&/^(firstChild|lastChild|descendants|componentsAtPoint)$/.test(name)&&isSub(v.cls,'Component')){var cmr=compMember(v,name,args||[],targs);if(cmr!==undefined)return cmr}\n"
        "  if(Array.isArray(v)&&(name==='whereType'||name==='query'))return v.filter(function(x){return !targs||isType(x,String(targs[0]).replace(/\\?$/,''))});\n",
        'member generics')
    # ---- FlameAudio.bgm, FlameAudio.loop
    src = sub1(src,
        "      if(a.args&&/^FlameAudio\\.\\w+$/.test(a.name))return null;\n",
        "      if(a.args&&/^FlameAudio\\.bgm\\.\\w+$/.test(a.name)){var bgm=a.name.split('.')[2],bga=evalArgs(a,env),bgv=bga.filter(function(x){return x.name==='volume'})[0],bgp=bga.filter(function(x){return !x.name})[0];\n"
        "        if(window.OF_MUSIC){if(bgm==='play'&&bgp){var bn=somOf(bgp.val);if(isMusica(bn))window.OF_MUSIC.bgm(bn,bgv?nn(bgv.val):1);else window.OF_MUSIC.playSfxLoop(bn,bgv?nn(bgv.val):1)}else if(bgm==='stop')window.OF_MUSIC.bgmStop();else if(bgm==='pause')window.OF_MUSIC.bgmPause();else if(bgm==='resume')window.OF_MUSIC.bgmResume()}return null}\n"
        "      if(a.args&&(a.name==='FlameAudio.loop'||a.name==='FlameAudio.playLongAudio'||a.name==='FlameAudio.loopLongAudio')){var lpa=evalArgs(a,env),lpv=lpa.filter(function(x){return x.name==='volume'})[0],ln=somOf(lpa.filter(function(x){return !x.name})[0].val),lvol=lpv?nn(lpv.val):1;\n"
        "        if(window.OF_MUSIC){var lloop=a.name!=='FlameAudio.playLongAudio';if(isMusica(ln))window.OF_MUSIC.play(ln,lvol,lloop);else if(lloop)window.OF_MUSIC.playSfxLoop(ln,lvol);else sfx(ln,lvol)}return null}\n"
        "      if(a.args&&/^FlameAudio\\.\\w+$/.test(a.name))return null;\n",
        'FlameAudio bgm')
    # ---- overlays: o jogo vira um identificador que o código do overlay consegue usar
    src = sub1(src,
        "    if(isSub(v.cls,'Component')||lit.d>6)return v.cls+'()';",
        "    if(ST.dataClasses.FlameGame&&isSub(v.cls,'FlameGame'))return '__flg'+flId(v);\n    if(isSub(v.cls,'Component')||lit.d>6)return v.cls+'()';",
        'lit FlameGame')
    src = sub1(src,
        "  if(n==='rootBundle')return{nat:'Bundle',f:{},src:'rootBundle'};\n",
        "  if(n.indexOf('__flg')===0&&typeof FL!=='undefined'){var gid=+n.slice(5);for(var gi=0;gi<FL.live.length;gi++)if(FL.live[gi].__fid===gid)return FL.live[gi]}\n"
        "  if(n==='rootBundle')return{nat:'Bundle',f:{},src:'rootBundle'};\n",
        'lookup __flg')
    src = sub1(src,
        "ST.FL=FL;",
        "ST.bindVar=bindVar;ST.flameGameOf=function(key){var e=FL.byKey[key],g=e&&e.game;if(!g||!g.f.overlays||!g.f.overlays.f)return null;var nms=(g.f.overlays.f.ativos||[]).slice();g.__ovSig=nms.join('|');return{names:nms,ref:'__flg'+flId(g)}};\nST.FL=FL;",
        'expose overlays')
    src = sub1(src,
        "FL.live.slice().forEach(function(g){any=true;try{FL.tick(g,dt)}",
        "FL.live.slice().forEach(function(g){var ov=g.f.overlays&&g.f.overlays.f&&g.f.overlays.f.ativos;if(ov){var sg=ov.join('|');if(sg!==(g.__ovSig||'')&&!FL.ovT){g.__ovSig=sg;FL.ovT=setTimeout(function(){FL.ovT=0;if(window.OF&&OF.rerender)OF.rerender()},0)}}});\n  FL.live.slice().forEach(function(g){any=true;try{FL.tick(g,dt)}",
        'overlay change')
    src = sub1(src,
        "  else if(r.mutated&&!(ST.anims||[]).some(function(v){return v.nat==='Ticker'||v.nat==='Timer'}))toast(",
        "  else if(r.mutated&&!window.__ofQuietMut&&!(ST.flameLive&&ST.flameLive())&&!(ST.anims||[]).some(function(v){return v.nat==='Ticker'||v.nat==='Timer'}))toast(",
        'no toast flame')
    # ---- renderer: GameWidget com overlays e initialActiveOverlays
    src = sub1(src, "function paintSvg(res,w,h){", OVERLAY_FNS + "function paintSvg(res,w,h){", 'overlay fns')
    src = sub1(src,
        "      R_opts.post.push(function(){var w=d.clientWidth||360,h=d.clientHeight||600,res=null;try{res=OF.ST.flamePaint(gwr,gwk,w,h)}",
        "      var gwo=OF.ST.flameGameOf?OF.ST.flameGameOf(gwk):null;\n"
        "      if(gwo&&gwo.names.length){var ovm=ovParse(M.rawProp(n,'overlayBuilderMap'));gwo.names.forEach(function(nm){var en=ovm[nm];if(!en)return;var body=en.body;try{if(en.game)body=OF.ST.bindVar(body,en.game,{raw:gwo.ref})}catch(e){}\n"
        "        var ovn=OF.parseWidgetText(body);if(!ovn)return;var host=document.createElement('div');host.className='gwov';host.dataset.ov=nm;host.appendChild(child(ovn,'ov:'+nm,'#single'));d.appendChild(host)})}\n"
        "      var gwi=M.rawProp(n,'initialActiveOverlays');\n"
        "      R_opts.post.push(function(){var w=d.clientWidth||360,h=d.clientHeight||600,res=null;try{res=OF.ST.flamePaint(gwr,gwk,w,h,gwi)}",
        'render overlays')
    src = sub1(src, ".nd.gw{display:block}",
               ".nd.gw{display:block}.nd.gw>.gwov{position:absolute;inset:0;display:flex;flex-direction:column;pointer-events:none;z-index:2}.nd.gw>.gwov>*{flex:1 1 auto;min-height:0}.nd.gw>.gwov .hh,.nd.gw>.gwov button,.nd.gw>.gwov input,.nd.gw>.gwov .btn,.nd.gw>.gwov .card,.nd.gw>.gwov .fab{pointer-events:auto}",
               'css overlays')
    # ---- CustomPaint(size: Size.infinite): ocupa todo o espaço do pai
    src = sub1(src,
        "      if(csz){cw=+csz[1];chh=+(csz[2]||csz[1])}\n      else if(/Size\\b/.test(szr)){",
        "      if(csz){cw=+csz[1];chh=+(csz[2]||csz[1])}\n"
        "      else if(/^\\s*(?:const\\s+)?Size\\.infinite\\s*$/.test(szr)&&M.rawProp(n,'painter')){d.style.alignSelf='stretch';d.style.flex='1 1 auto';d.style.width='100%';d.style.height='100%';d.style.minHeight='0';d.classList.add('cpd');var lyI=document.createElement('div');lyI.className='cpsv';d.appendChild(lyI);\n"
        "        var scpI=OF.ST.cur;R_opts.post.push(function(){var pe=d.parentElement,ps=pe,pn=0;while(ps&&pn++<4&&ps.classList&&ps.classList.contains('hh')){ps.style.flex='1 1 auto';ps.style.alignSelf='stretch';ps.style.minHeight='0';ps.style.minWidth='0';ps=ps.parentElement}var w=d.clientWidth||(pe&&pe.clientWidth)||300,h=d.clientHeight||(pe&&pe.clientHeight)||400,res=null;OF.ST.enter(scpI);try{res=OF.ST.paintOps(n,'painter',w,h)}catch(e){lyI.className+=' cper';lyI.textContent='painter: '+e.message;return}finally{OF.ST.leave()}if(res){if(OF.useSvg)lyI.innerHTML=paintSvg(res,w,h);else{lyI.innerHTML='';lyI.appendChild(paintCanvas(res,w,h))}}});\n"
        "        cw=-1}\n      else if(/Size\\b/.test(szr)){",
        'Size.infinite')
    # ---- pinça no GestureDetector
    src = sub1(src, "/* teclado: Focus(onKeyEvent) e KeyboardListener(onKeyEvent) recebem as teclas quando o foco não está no editor */",
               UI_SCALE + "/* teclado: Focus(onKeyEvent) e KeyboardListener(onKeyEvent) recebem as teclas quando o foco não está no editor */", 'ui scale')
    # ---- vários return no build: a tela principal é o último return; os anteriores dependem da condição
    src = sub1(src,
        "    if(b>=0)for(x=b;x<t.length;x++)if(t[x].k==='id'&&t[x].v==='return'){i=x+1;break}\n",
        "    if(b>=0)for(x=b;x<t.length;x++)if(t[x].k==='id'&&t[x].v==='return'){i=x+1;break}\n"
        "    var mret=b>=0?buildReturns(src,t,b):null;if(mret&&mret.alts.length)i=mret.main;\n",
        'parse multi return')
    src = sub1(src,
        "    var root=toNode(e,src);\n",
        "    var root=toNode(e,src);\n"
        "    if(mret&&mret.alts.length){root.__alts=[];mret.alts.forEach(function(al){try{var pa=new Parser(src,t,al.at),ea=pa.expr();if(ea.kind==='call')root.__alts.push({cond:al.cond,node:toNode(ea,src)})}catch(er){}})}\n",
        'root alts')
    src = sub1(src,
        "function parseSource(src){",
        r"""function buildReturns(src,t,b){
  var x=b;while(x<t.length&&!(t[x].k==='p'&&(t[x].v==='{'||t[x].v==='=>')))x++;
  if(x>=t.length||t[x].v!=='{')return null;
  var d=0,alts=[],main=-1,i=x+1;
  function skipParen(j){var dd=0;for(;j<t.length;j++){if(t[j].v==='(')dd++;else if(t[j].v===')'){dd--;if(dd===0)return j}}return -1}
  function skipStmt(j){var dd=0;for(;j<t.length;j++){var v=t[j].v;if(t[j].k==='p'){if('([{'.indexOf(v)>=0&&v.length===1)dd++;else if(')]}'.indexOf(v)>=0&&v.length===1)dd--;else if(v===';'&&dd===0)return j}}return -1}
  while(i<t.length){var k=t[i];
    if(k.k==='p'&&k.v==='}')break;
    if(k.k==='id'&&k.v==='if'&&t[i+1]&&t[i+1].v==='('){var ce=skipParen(i+1);if(ce<0)return null;var cond=src.slice(t[i+2].s,t[ce-1].e),j=ce+1,braced=false;
      if(t[j]&&t[j].v==='{'){braced=true;j++}
      if(!(t[j]&&t[j].k==='id'&&t[j].v==='return'))return null;
      var se=skipStmt(j+1);if(se<0)return null;alts.push({cond:cond,at:j+1});j=se+1;
      if(braced){if(!(t[j]&&t[j].v==='}'))return null;j++}
      if(t[j]&&t[j].k==='id'&&t[j].v==='else')return null;
      i=j;continue}
    if(k.k==='id'&&k.v==='return'){main=i+1;break}
    var se2=skipStmt(i);if(se2<0)return null;i=se2+1}
  if(main<0)return null;return{main:main,alts:alts}}
function parseSource(src){""",
        'buildReturns fn')
    src = sub1(src,
        "  try{renderInner(root,selKey,screen)}finally{M.ev=false}",
        "  try{var rr=root;if(root&&root.__alts&&R_opts.run){for(var ai=0;ai<root.__alts.length;ai++){var al=root.__alts[ai],cv0=false;try{cv0=OF.ST.value(al.cond)===true}catch(x){}if(cv0){rr=al.node;break}}}renderInner(rr,selKey,screen)}finally{M.ev=false}",
        'render alts')
    # ---- botão de sprites e rerender
    src = sub1(src, "R.opts.rerender=function(){renderCanvas()};", "R.opts.rerender=function(){renderCanvas()};OF.rerender=R.opts.rerender;", 'OF.rerender')
    src = sub1(src,
        '<button class="btn" id="somBtn"',
        '<button class="btn" id="sprBtn" title="Sprites prontos e suas próprias imagens">🖼 Sprites</button>\n  <button class="btn" id="somBtn"',
        'spr button')
    return src


SPRITES_UI = r"""<style>
.sprlist{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px;margin-top:10px}
.sprc{border:1px solid var(--line);border-radius:10px;padding:8px;display:flex;flex-direction:column;gap:6px;background:var(--panel2);min-width:0}
.sprc .sprv{height:72px;display:flex;align-items:center;justify-content:center;background:repeating-conic-gradient(var(--panel) 0 25%,var(--panel2) 0 50%) 0 0/16px 16px;border-radius:6px}
.sprc .sprv img{height:56px;width:100%;image-rendering:pixelated;object-fit:contain}
.sprc code{font:11.5px/1.3 var(--f-mono);word-break:break-all;color:var(--ink)}
.sprc .sprm{font-size:11.5px;color:var(--ink2)}
.sprc .sprb{display:flex;gap:6px;flex-wrap:wrap}.sprc .sprb .btn{font-size:12px;padding:3px 8px}
.sprerr{color:var(--err);font-size:13px;min-height:1em}
</style>
<div class="modal" id="sprModal" hidden role="dialog" aria-modal="true" aria-label="Sprites"><div class="mbox">
  <div class="mh"><b>Sprites</b><button class="btn" id="sprClose" aria-label="Fechar">✕</button></div>
  <div class="mb">
   <p class="mt">Use o caminho no código: rootBundle.load('assets/sprites/heroi.png'), Image.asset(...) ou, no Flame, só o nome do arquivo (loadSprite('heroi.png')).</p>
   <h3>Suas imagens</h3>
   <p class="mt">PNG, JPG, GIF ou WebP de até 400 KB. Elas ficam guardadas só neste navegador.</p>
   <div class="mrow"><input type="file" id="sprFile" accept="image/png,image/jpeg,image/gif,image/webp" aria-label="Arquivo de imagem"><input id="sprName" placeholder="nome.png" maxlength="40" aria-label="Nome do sprite"><button class="btn pri" id="sprAdd">Adicionar</button></div>
   <div class="sprerr" id="sprErr" role="status"></div>
   <div class="sprlist" id="sprOwn"></div>
   <h3>Prontos do simulador</h3>
   <div class="sprlist" id="sprList"></div>
  </div></div></div>
<script>
(function(){
  var M=document.getElementById('sprModal'),B=document.getElementById('sprBtn');if(!M||!B)return;
  function own(){try{return JSON.parse(localStorage.getItem('oficina2.sprites')||'{}')}catch(e){return{}}}
  function save(o){localStorage.setItem('oficina2.sprites',JSON.stringify(o))}
  function card(k,s,isOwn){var c=document.createElement('div');c.className='sprc';
    var v=document.createElement('div');v.className='sprv';var im=document.createElement('img');im.src=s.uri;im.alt='';v.appendChild(im);c.appendChild(v);
    var cd=document.createElement('code');cd.textContent=k;c.appendChild(cd);
    var m=document.createElement('div');m.className='sprm';m.textContent=s.w+'×'+s.h+(s.q>1?' · '+s.q+' quadros de '+(s.w/s.q)+'×'+s.h:'')+(s.desc&&!isOwn?' · '+s.desc:'');c.appendChild(m);
    var bt=document.createElement('div');bt.className='sprb';
    var cp=document.createElement('button');cp.className='btn';cp.textContent='Copiar caminho';cp.addEventListener('click',function(){var done=function(){cp.textContent='Copiado';setTimeout(function(){cp.textContent='Copiar caminho'},1200)};try{navigator.clipboard.writeText(k).then(done,function(){})}catch(e){}});bt.appendChild(cp);
    if(isOwn){var del=document.createElement('button');del.className='btn';del.textContent='Apagar';del.addEventListener('click',function(){
      if(del.dataset.sure!=='1'){del.dataset.sure='1';del.textContent='Apagar mesmo?';return}
      var o=own();delete o[k];try{save(o)}catch(e){}delete window.OF_SPRITES[k];delete window.OF_SPRITE_IMG[k];draw();if(window.OF&&OF.rerender)OF.rerender()});bt.appendChild(del)}
    c.appendChild(bt);return c}
  function draw(){var L=document.getElementById('sprList'),O=document.getElementById('sprOwn');L.innerHTML='';O.innerHTML='';var o=own(),n=0;
    Object.keys(window.OF_SPRITES||{}).forEach(function(k){var s=window.OF_SPRITES[k];if(o[k]){O.appendChild(card(k,s,true));n++}else L.appendChild(card(k,s,false))});
    if(!n){var p=document.createElement('p');p.className='mt';p.textContent='Nenhuma imagem sua ainda. Escolha um arquivo acima.';O.appendChild(p)}}
  function err(t){document.getElementById('sprErr').textContent=t||''}
  B.addEventListener('click',function(){err('');draw();M.hidden=false});
  document.getElementById('sprClose').addEventListener('click',function(){M.hidden=true});
  M.addEventListener('click',function(e){if(e.target===M)M.hidden=true});
  document.getElementById('sprFile').addEventListener('change',function(){var f=this.files&&this.files[0];if(!f)return;var nm=document.getElementById('sprName');
    if(!nm.value)nm.value=f.name.toLowerCase().replace(/\.[a-z0-9]+$/,'').replace(/[^a-z0-9_-]+/g,'_').replace(/^_+|_+$/g,'')+'.'+((/\.(png|jpe?g|gif|webp)$/i.exec(f.name)||[0,'png'])[1].toLowerCase())});
  document.getElementById('sprAdd').addEventListener('click',function(){
    var f=document.getElementById('sprFile').files[0];if(!f){err('Escolha um arquivo de imagem primeiro.');return}
    if(f.size>400*1024){err('Essa imagem tem '+Math.round(f.size/1024)+' KB. O limite é 400 KB: diminua a imagem ou salve como PNG menor.');return}
    var nome=(document.getElementById('sprName').value||'').trim().toLowerCase().replace(/[^a-z0-9_.-]+/g,'_');
    if(!/\.(png|jpe?g|gif|webp)$/.test(nome))nome=(nome||'imagem').replace(/\.+$/,'')+'.png';
    var k='assets/sprites/'+nome,base=window.OF_SPRITES[k];if(base&&!base.own){err('Já existe um sprite pronto com o nome '+nome+'. Escolha outro nome.');return}
    var rd=new FileReader();rd.onload=function(){var uri=rd.result,im=new Image();im.onload=function(){
      var o=own();o[k]={w:im.naturalWidth,h:im.naturalHeight,q:1,desc:'Sua imagem',uri:uri};
      try{save(o)}catch(e){err('O navegador não tem mais espaço para imagens. Apague alguma das suas antes.');return}
      o[k].own=true;window.OF_SPRITES[k]=o[k];window.OF_SPRITE_IMG[k]=im;err('');document.getElementById('sprFile').value='';document.getElementById('sprName').value='';draw();if(window.OF&&OF.rerender)OF.rerender()};
      im.onerror=function(){err('Não consegui abrir essa imagem. Tente outro arquivo.')};im.src=uri};rd.readAsDataURL(f)});
})();
</script>
"""


def finish(src):
    return src + SPRITES_UI
