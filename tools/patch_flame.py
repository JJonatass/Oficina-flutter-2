# Frente 4 da Oficina Flutter 2: Flame simplificado.
# - interpretador: setters (set x(v)), Vector2 nativo, tear-off de método de objeto, Set de teclas
# - prelúdio Dart (tools/flame_prelude.dart) acrescentado quando o código importa package:flame
# - motor do Flame em JS (FL): ciclo de vida, update, render com câmera, colisões, toque, arrasto, teclado
# - GameWidget como raiz (runApp(GameWidget(game: ...))) ou dentro da árvore de widgets
import json, pathlib
from patch_engine import sub1

ROOT = pathlib.Path(__file__).resolve().parent

VEC = r"""/* ===== Oficina 2: Vector2 (pacote vector_math, usado pelo Flame) ===== */
function mkVec(x,y){var v={nat:'Vec2',f:{x:new Dbl(+x||0),y:new Dbl(+y||0)}};
  Object.defineProperty(v,'src',{enumerable:true,configurable:true,get:function(){return 'Vector2('+dstr(nn(this.f.x))+', '+dstr(nn(this.f.y))+')'},set:function(){}});return v}
function isVec(v){return !!v&&v.nat==='Vec2'}
function vx(v){return nn(v.f.x)}function vy(v){return nn(v.f.y)}
function vecMember(v,name,args){
  var a0=args&&args[0],a1=args&&args[1];
  switch(name){
    case 'x':case 'y':return v.f[name];
    case 'length':return new Dbl(Math.hypot(vx(v),vy(v)));
    case 'length2':return new Dbl(vx(v)*vx(v)+vy(v)*vy(v));
    case 'normalized':{var l=Math.hypot(vx(v),vy(v))||1;return mkVec(vx(v)/l,vy(v)/l)}
    case 'normalize':{var l2=Math.hypot(vx(v),vy(v));if(l2){v.f.x=new Dbl(vx(v)/l2);v.f.y=new Dbl(vy(v)/l2)}return new Dbl(l2)}
    case 'clone':return mkVec(vx(v),vy(v));
    case 'setValues':v.f.x=new Dbl(nn(a0));v.f.y=new Dbl(nn(a1));return null;
    case 'setFrom':v.f.x=new Dbl(vx(a0));v.f.y=new Dbl(vy(a0));return null;
    case 'setZero':v.f.x=new Dbl(0);v.f.y=new Dbl(0);return null;
    case 'setAll':v.f.x=new Dbl(nn(a0));v.f.y=new Dbl(nn(a0));return null;
    case 'add':v.f.x=new Dbl(vx(v)+vx(a0));v.f.y=new Dbl(vy(v)+vy(a0));return null;
    case 'sub':v.f.x=new Dbl(vx(v)-vx(a0));v.f.y=new Dbl(vy(v)-vy(a0));return null;
    case 'addScaled':v.f.x=new Dbl(vx(v)+vx(a0)*nn(a1));v.f.y=new Dbl(vy(v)+vy(a0)*nn(a1));return null;
    case 'scale':v.f.x=new Dbl(vx(v)*nn(a0));v.f.y=new Dbl(vy(v)*nn(a0));return null;
    case 'scaled':return mkVec(vx(v)*nn(a0),vy(v)*nn(a0));
    case 'multiply':v.f.x=new Dbl(vx(v)*vx(a0));v.f.y=new Dbl(vy(v)*vy(a0));return null;
    case 'divide':v.f.x=new Dbl(vx(v)/vx(a0));v.f.y=new Dbl(vy(v)/vy(a0));return null;
    case 'negate':v.f.x=new Dbl(-vx(v));v.f.y=new Dbl(-vy(v));return null;
    case 'absolute':v.f.x=new Dbl(Math.abs(vx(v)));v.f.y=new Dbl(Math.abs(vy(v)));return null;
    case 'translate':v.f.x=new Dbl(vx(v)+nn(a0));v.f.y=new Dbl(vy(v)+nn(a1));return null;
    case 'clampScalar':v.f.x=new Dbl(Math.max(nn(a0),Math.min(nn(a1),vx(v))));v.f.y=new Dbl(Math.max(nn(a0),Math.min(nn(a1),vy(v))));return null;
    case 'clamp':v.f.x=new Dbl(Math.max(vx(a0),Math.min(vx(a1),vx(v))));v.f.y=new Dbl(Math.max(vy(a0),Math.min(vy(a1),vy(v))));return null;
    case 'clampLength':{var lc=Math.hypot(vx(v),vy(v)),mn=nn(a0),mx=nn(a1);if(lc>0&&(lc<mn||lc>mx)){var k=Math.max(mn,Math.min(mx,lc))/lc;v.f.x=new Dbl(vx(v)*k);v.f.y=new Dbl(vy(v)*k)}return null}
    case 'distanceTo':return new Dbl(Math.hypot(vx(v)-vx(a0),vy(v)-vy(a0)));
    case 'distanceToSquared':{var dx=vx(v)-vx(a0),dy=vy(v)-vy(a0);return new Dbl(dx*dx+dy*dy)}
    case 'dot':return new Dbl(vx(v)*vx(a0)+vy(v)*vy(a0));
    case 'cross':return new Dbl(vx(v)*vy(a0)-vy(v)*vx(a0));
    case 'angleTo':return new Dbl(Math.atan2(vy(a0),vx(a0))-Math.atan2(vy(v),vx(v)));
    case 'angleToSigned':return new Dbl(Math.atan2(vx(v)*vy(a0)-vy(v)*vx(a0),vx(v)*vx(a0)+vy(v)*vy(a0)));
    case 'screenAngle':return new Dbl(Math.atan2(vx(v),-vy(v)));
    case 'isZero':return vx(v)===0&&vy(v)===0;
    case 'isNaN':return isNaN(vx(v))||isNaN(vy(v));
    case 'toOffset':return mkOffset(vx(v),vy(v));
    case 'toSize':return mkSize(vx(v),vy(v));
    case 'toRect':return mkRect(0,0,vx(v),vy(v));
    case 'rotate':{var c=Math.cos(nn(a0)),s=Math.sin(nn(a0)),x=vx(v),y=vy(v);v.f.x=new Dbl(x*c-y*s);v.f.y=new Dbl(x*s+y*c);return null}
    case 'floor':v.f.x=new Dbl(Math.floor(vx(v)));v.f.y=new Dbl(Math.floor(vy(v)));return null;
    case 'round':v.f.x=new Dbl(Math.round(vx(v)));v.f.y=new Dbl(Math.round(vy(v)));return null;
    case 'toString':return '['+dstr(vx(v))+','+dstr(vy(v))+']';
    case 'storage':return [v.f.x,v.f.y]}
  throw new Error('Vector2.'+name)}
function vecCtor(name,vals){
  switch(name){
    case 'Vector2':return mkVec(nn(vals[0]),nn(vals[1]));
    case 'Vector2.zero':return mkVec(0,0);
    case 'Vector2.all':return mkVec(nn(vals[0]),nn(vals[0]));
    case 'Vector2.copy':return mkVec(vx(vals[0]),vy(vals[0]));
    case 'Vector2.array':{var ar=toIter(vals[0]);return mkVec(nn(ar[0]),nn(ar[1]))}
    case 'Vector2.random':return mkVec(Math.random(),Math.random())}
  return null}
"""

SETTERS = r"""function setterOf(cn,nm){var seen=0;while(cn&&seen++<20){var dc=ST.dataClasses[cn];if(!dc)return null;if(dc.setters&&dc.setters[nm])return dc.setters[nm];
  var w=(dc.withs||[]).slice().reverse();for(var i=0;i<w.length;i++){var wc=ST.dataClasses[w[i]];if(wc&&wc.setters&&wc.setters[nm])return wc.setters[nm]}cn=dc.ext}return null}
function callSetter(o,sx,val){var e=mkEnv({});e.self=o;e.cls=o.cls;e.params[sx.param]=val;if(sx.arrow)ev(pTern(new Ps(sx.body)),e);else stmt(new Ps(sx.body),e,true);mutated=true}
function setMemberX(o,name,val){
  if(!o)return false;
  if(o.cls){if(!hasOwn(o.f,name)){var sx=setterOf(o.cls,name);if(sx){callSetter(o,sx,val);return true}}o.f[name]=coerce(fieldType(ST.dataClasses[o.cls],name),val);mutated=true;return true}
  if(o.nat==='Vec2'&&(name==='x'||name==='y')){o.f[name]=new Dbl(nn(val));mutated=true;return true}
  if(o.nat==='FlEvent'&&hasOwn(o.f,name)){o.f[name]=val;return true}
  if(o.nat==='#vsync'&&ST.fields[name]){ST.fields[name].value=coerce(ST.fields[name].type,val);mutated=true;return true}
  return false}
"""

FL = r"""/* ===== Oficina 2: motor do Flame simplificado ===== */
var FL={byKey:{},live:[],ids:0,loop:null};
function flIs(o,t){return !!o&&!!o.cls&&isSub(o.cls,t)}
function flHas(o,m){return !!o&&!!o.cls&&!!methodOf(o.cls,m)}
function flCall(o,m,args){if(!flHas(o,m))return undefined;steps=0;return member(o,m,args||[])}
function flKids(o){var k=o&&o.f&&o.f.children;return Array.isArray(k)?k:[]}
function flId(o){return o.__fid||(o.__fid=++FL.ids)}
function flRootOf(o){var s=0;while(o&&s++<200){if(flIs(o,'FlameGame'))return o;if(o.__owner)return o.__owner;o=o.f&&o.f.parent}return null}
FL.reset=function(){FL.byKey={};FL.live=[];if(FL.loop){var ix=ST.anims.indexOf(FL.loop);if(ix>=0)ST.anims.splice(ix,1)}FL.loop=null};
FL.add=function(p,c){if(!p||!c||!c.cls)throw exc('add() precisa de um componente');c.f.parent=p;c.__rm=false;(p.__pend||(p.__pend=[])).push(c);return null};
FL.remove=function(c){if(c){c.__rm=true}return null};
FL.sortKids=function(o){var k=flKids(o);if(k.length>1){var ok=true;for(var i=1;i<k.length;i++)if(nn(k[i-1].f.priority)>nn(k[i].f.priority)){ok=false;break}if(!ok){k.forEach(function(c,i){c.__ord=i});k.sort(function(a,b){return (nn(a.f.priority)-nn(b.f.priority))||(a.__ord-b.__ord)})}}};
FL.life=function(o,g,depth){
  if(!o||(depth||0)>40)return;
  var k=flKids(o);
  for(var i=k.length-1;i>=0;i--){var c=k[i];if(c.__rm){k.splice(i,1);c.__mounted=false;flCall(c,'onRemove');c.f.parent=null}}
  var guard=0;
  while(o.__pend&&o.__pend.length&&guard++<50){
    var pend=o.__pend.splice(0);
    pend.forEach(function(c){if(c.__rm){c.__rm=false;return}
      if(!c.__loaded){c.__loaded=true;if(g&&g.f.size)flCall(c,'onGameResize',[g.f.size]);flCall(c,'onLoad')}
      if(k.indexOf(c)<0)k.push(c);c.__mounted=true;flCall(c,'onMount')})}
  FL.sortKids(o);
  flKids(o).slice().forEach(function(c){FL.life(c,g,(depth||0)+1)})};
FL.lifeAll=function(g){FL.life(g,g);var w=g.f.world,cam=g.f.camera;if(w){w.__owner=g;FL.life(w,g)}if(cam){cam.__owner=g;FL.life(cam,g);if(cam.f.viewport){cam.f.viewport.__owner=g;FL.life(cam.f.viewport,g)}if(cam.f.viewfinder)cam.f.viewfinder.__owner=g}};
FL.ensure=function(g,w,h){
  if(!g.__fl){g.__fl={pairs:{}};g.f.size=mkVec(w,h);
    if(FL.live.indexOf(g)<0)FL.live.push(g);
    flCall(g,'onGameResize',[g.f.size]);
    try{flCall(g,'onLoad')}catch(e){g.__flErr=e.message;throw e}
    g.__loaded=true;g.__mounted=true;FL.lifeAll(g);flCall(g,'onMount');
    if(!FL.loop){FL.loop={nat:'FlLoop',f:{},last:ST.now()};ST.anims.push(FL.loop)}}
  else if(Math.abs(vx(g.f.size)-w)>0.5||Math.abs(vy(g.f.size)-h)>0.5){g.f.size=mkVec(w,h);flCall(g,'onGameResize',[g.f.size])}
  return g};
FL.upd=function(c,dt){if(!c||c.__rm)return;flCall(c,'update',[dt]);flKids(c).slice().forEach(function(k){FL.upd(k,dt)})};
FL.tick=function(g,dt){
  if(g.__flErr)return;
  FL.lifeAll(g);
  if(g.f.paused===true)return;
  var d=new Dbl(dt);
  FL.upd(g,d);if(g.f.world)FL.upd(g.f.world,d);var cam=g.f.camera;if(cam&&cam.f.viewport)FL.upd(cam.f.viewport,d);
  if(cam&&cam.f.seguindo&&cam.f.seguindo.f){var t=cam.f.seguindo,ctr=FL.absCenter(t);cam.f.viewfinder.f.position=mkVec(ctr[0],ctr[1])}
  if(flIs(g,'HasCollisionDetection'))FL.collide(g);
  FL.lifeAll(g)};
FL.step=function(now){var lp=FL.loop;if(!lp)return false;var dt=Math.min(0.1,Math.max(0,(now-lp.last)/1000));lp.last=now;
  var any=false;FL.live.slice().forEach(function(g){any=true;try{FL.tick(g,dt)}catch(e){g.__flErr=e.message;ST.tickErr={msg:e.message,exc:!!e.dartExc,src:'jogo Flame'}}});return any};
/* posições absolutas (sem rotação), no espaço do pai de mais alto nível (mundo ou tela) */
FL.topLeft=function(c){var x=0,y=0,o=c,s=0;while(o&&s++<100){if(flIs(o,'PositionComponent')){var sx=o.f.scale?vx(o.f.scale):1,sy=o.f.scale?vy(o.f.scale):1;
    x+=vx(o.f.position)-nn(o.f.anchor.f.x)*vx(o.f.size)*Math.abs(sx);y+=vy(o.f.position)-nn(o.f.anchor.f.y)*vy(o.f.size)*Math.abs(sy)}o=o.f.parent}return[x,y]};
FL.rect=function(c){var tl=FL.topLeft(c),sx=c.f.scale?Math.abs(vx(c.f.scale)):1,sy=c.f.scale?Math.abs(vy(c.f.scale)):1;return[tl[0],tl[1],vx(c.f.size)*sx,vy(c.f.size)*sy]};
FL.absCenter=function(c){var r=FL.rect(c);return[r[0]+r[2]/2,r[1]+r[3]/2]};
FL.inWorld=function(c){var o=c,s=0;while(o&&s++<100){if(flIs(o,'World'))return true;o=o.f.parent}return false};
FL.camT=function(g){var cam=g.f.camera,vf=cam&&cam.f.viewfinder,w=vx(g.f.size),h=vy(g.f.size);if(!vf)return{ax:0,ay:0,z:1,px:0,py:0};
  return{ax:nn(vf.f.anchor.f.x)*w,ay:nn(vf.f.anchor.f.y)*h,z:nn(vf.f.zoom)||1,px:vx(vf.f.position),py:vy(vf.f.position)}};
/* colisões entre hitboxes (retângulo e círculo) */
FL.hitboxes=function(o,out){flKids(o).forEach(function(c){if(c.__rm||!c.__mounted)return;if(flIs(c,'ShapeHitbox'))out.push(c);else FL.hitboxes(c,out)});return out};
FL.hbShape=function(h){var owner=h.f.parent,r;if(h.f.tamanhoDoDono===true){r=FL.rect(owner)}else{r=FL.rect(h)}
  return{x:r[0],y:r[1],w:r[2],h:r[3],c:h.f.circulo===true,owner:owner,type:pcol(h.f.collisionType)||''}};
FL.overlap=function(a,b){
  if(a.c&&b.c){var ra=Math.min(a.w,a.h)/2,rb=Math.min(b.w,b.h)/2,dx=(a.x+a.w/2)-(b.x+b.w/2),dy=(a.y+a.h/2)-(b.y+b.h/2);return dx*dx+dy*dy<(ra+rb)*(ra+rb)}
  if(a.c||b.c){var ci=a.c?a:b,rc=a.c?b:a,r=Math.min(ci.w,ci.h)/2,cx=ci.x+ci.w/2,cy=ci.y+ci.h/2,nx=Math.max(rc.x,Math.min(cx,rc.x+rc.w)),ny=Math.max(rc.y,Math.min(cy,rc.y+rc.h));return (cx-nx)*(cx-nx)+(cy-ny)*(cy-ny)<r*r}
  return a.x<b.x+b.w&&b.x<a.x+a.w&&a.y<b.y+b.h&&b.y<a.y+a.h};
FL.collide=function(g){
  var hs=[];FL.hitboxes(g,hs);if(g.f.world)FL.hitboxes(g.f.world,hs);
  var sh=hs.map(FL.hbShape).filter(function(s){return !/inactive/.test(s.type)&&s.owner&&!s.owner.__rm}),now={},prev=g.__fl.pairs;
  for(var i=0;i<sh.length;i++)for(var j=i+1;j<sh.length;j++){var a=sh[i],b=sh[j];
    if(a.owner===b.owner)continue;if(/passive/.test(a.type)&&/passive/.test(b.type))continue;if(!FL.overlap(a,b))continue;
    var ia=flId(a.owner),ib=flId(b.owner),key=ia<ib?ia+'|'+ib:ib+'|'+ia;if(now[key])continue;now[key]=[a.owner,b.owner];
    var px=(Math.max(a.x,b.x)+Math.min(a.x+a.w,b.x+b.w))/2,py=(Math.max(a.y,b.y)+Math.min(a.y+a.h,b.y+b.h))/2,pts={isSet:true,s:new Set([mkVec(px,py)])};
    [[a.owner,b.owner],[b.owner,a.owner]].forEach(function(pr){if(!flIs(pr[0],'CollisionCallbacks')||pr[0].__rm)return;
      if(!prev[key])flCall(pr[0],'onCollisionStart',[pts,pr[1]]);if(!pr[0].__rm)flCall(pr[0],'onCollision',[pts,pr[1]])})}
  Object.keys(prev).forEach(function(k){if(!now[k]){var p=prev[k];[[p[0],p[1]],[p[1],p[0]]].forEach(function(pr){if(flIs(pr[0],'CollisionCallbacks'))flCall(pr[0],'onCollisionEnd',[pr[1]])})}});
  g.__fl.pairs=now};
/* desenho: transformações de cada PositionComponent, câmera para o mundo, depuração */
function cvCall(cv,m,args){return member(cv,m,args)}
FL.renderTree=function(c,cv,g){
  if(!c||c.__rm||!c.__mounted&&c!==g)return;
  var isP=flIs(c,'PositionComponent');
  cvCall(cv,'save',[]);
  if(isP){cvCall(cv,'translate',[new Dbl(vx(c.f.position)),new Dbl(vy(c.f.position))]);
    var an=nn(c.f.angle);if(an)cvCall(cv,'rotate',[new Dbl(an)]);
    var sx=vx(c.f.scale),sy=vy(c.f.scale);if(sx!==1||sy!==1)cvCall(cv,'scale',[new Dbl(sx),new Dbl(sy)]);
    cvCall(cv,'translate',[new Dbl(-nn(c.f.anchor.f.x)*vx(c.f.size)),new Dbl(-nn(c.f.anchor.f.y)*vy(c.f.size))])}
  if(c!==g)flCall(c,'render',[cv]);
  if(isP&&(c.f.debugMode===true||g.f.debugMode===true)){
    var dp={nat:'Paint',f:{color:{raw:flIs(c,'ShapeHitbox')?'Color(0xFFFFEB3B)':'Color(0xFFFF00FF)'},style:'PaintingStyle.stroke',strokeWidth:new Dbl(1),strokeCap:'StrokeCap.butt',strokeJoin:'StrokeJoin.miter'},src:'Paint()'};
    if(flIs(c,'ShapeHitbox')&&c.f.circulo===true){var hr=Math.min(vx(c.f.size),vy(c.f.size))/2,own=c.f.tamanhoDoDono===true?c.f.parent:c,orr=Math.min(vx(own.f.size),vy(own.f.size))/2;
      cvCall(cv,'drawCircle',[mkOffset(c.f.tamanhoDoDono===true?vx(own.f.size)/2:hr,c.f.tamanhoDoDono===true?vy(own.f.size)/2:hr),new Dbl(c.f.tamanhoDoDono===true?orr:hr),dp])}
    else{var bw=vx(c.f.size),bh=vy(c.f.size);if(flIs(c,'ShapeHitbox')&&c.f.tamanhoDoDono===true){bw=vx(c.f.parent.f.size);bh=vy(c.f.parent.f.size)}cvCall(cv,'drawRect',[mkRect(0,0,bw,bh),dp])}
    if(!flIs(c,'ShapeHitbox')){var tp={nat:'TextPainter',f:{text:{raw:"TextSpan(text: '"+Math.round(vx(c.f.position))+', '+Math.round(vy(c.f.position))+"', style: TextStyle(fontSize: 9, color: Color(0xFFFF00FF)))"}},st:{},src:'TextPainter()'};
      member(tp,'paint',[cv,mkOffset(0,-11)])}}
  FL.sortKids(c);
  flKids(c).forEach(function(k){FL.renderTree(k,cv,g)});
  cvCall(cv,'restore',[])};
FL.render=function(g,cv){
  var bg=null;try{bg=flCall(g,'backgroundColor')}catch(e){}
  if(bg!=null)cvCall(cv,'drawColor',[bg]);
  if(g.f.world){var t=FL.camT(g);cvCall(cv,'save',[]);cvCall(cv,'translate',[new Dbl(t.ax),new Dbl(t.ay)]);if(t.z!==1)cvCall(cv,'scale',[new Dbl(t.z),new Dbl(t.z)]);cvCall(cv,'translate',[new Dbl(-t.px),new Dbl(-t.py)]);
    g.f.world.__mounted=true;FL.renderTree(g.f.world,cv,g);cvCall(cv,'restore',[])}
  flCall(g,'render',[cv]);
  FL.sortKids(g);flKids(g).forEach(function(k){FL.renderTree(k,cv,g)});
  var vp=g.f.camera&&g.f.camera.f.viewport;if(vp){vp.__mounted=true;FL.renderTree(vp,cv,g)}};
/* entrada: toque, arrasto e teclado */
FL.pick=function(g,x,y,mixin){
  var found=null;
  function walk(c,px,py){if(found||!c||c.__rm||!c.__mounted)return;var k=flKids(c);for(var i=k.length-1;i>=0&&!found;i--)walk(k[i],px,py);
    if(found)return;if(flIs(c,mixin)&&flIs(c,'PositionComponent')){var r=FL.rect(c);if(px>=r[0]&&py>=r[1]&&px<r[0]+r[2]&&py<r[1]+r[3])found={c:c,lx:px-r[0],ly:py-r[1]}}}
  var vp=g.f.camera&&g.f.camera.f.viewport;if(vp)walk(vp,x,y);
  var gk=flKids(g);for(var i=gk.length-1;i>=0&&!found;i--)walk(gk[i],x,y);
  if(!found&&g.f.world){var t=FL.camT(g),wx=(x-t.ax)/t.z+t.px,wy=(y-t.ay)/t.z+t.py;walk(g.f.world,wx,wy)}
  if(!found&&flIs(g,mixin))found={c:g,lx:x,ly:y};
  return found};
FL.ev=function(o){var f={};Object.keys(o).forEach(function(k){var v=o[k];f[k]=Array.isArray(v)?mkVec(v[0],v[1]):v});f.handled=false;f.continuePropagation=false;return{nat:'FlEvent',f:f,src:'Event'}};
FL.drag=null;
FL.pointer=function(kind,key,x,y,dx,dy,vxv,vyv){
  var ent=FL.byKey[key];if(!ent||!ent.game||!ent.game.__loaded)return false;var g=ent.game,used=false;
  try{
    if(kind==='down'){var h=FL.pick(g,x,y,'TapCallbacks');if(h){used=true;flCall(h.c,'onTapDown',[FL.ev({localPosition:[h.lx,h.ly],canvasPosition:[x,y],devicePosition:[x,y]})]);FL.tapC=h}
      var d=FL.pick(g,x,y,'DragCallbacks');FL.drag=d?{c:d.c,sx:x,sy:y,lx:d.lx,ly:d.ly,started:false,g:g}:null;if(d)used=true}
    else if(kind==='move'&&FL.drag&&FL.drag.g===g){var dr=FL.drag;used=true;
      if(!dr.started){dr.started=true;flCall(dr.c,'onDragStart',[FL.ev({localPosition:[dr.lx,dr.ly],canvasPosition:[dr.sx,dr.sy],devicePosition:[dr.sx,dr.sy]})])}
      var z=FL.inWorld(dr.c)?FL.camT(g).z:1;
      flCall(dr.c,'onDragUpdate',[FL.ev({localDelta:[dx/z,dy/z],canvasDelta:[dx,dy],deviceDelta:[dx,dy],localStartPosition:[dr.lx,dr.ly],canvasStartPosition:[dr.sx,dr.sy],canvasEndPosition:[x,y],localEndPosition:[dr.lx+(x-dr.sx)/z,dr.ly+(y-dr.sy)/z]})])}
    else if(kind==='up'){var t=FL.tapC;FL.tapC=null;var dr2=FL.drag;FL.drag=null;
      if(dr2&&dr2.started&&dr2.g===g){used=true;flCall(dr2.c,'onDragEnd',[FL.ev({velocity:[vxv,vyv]})])}
      else if(t){used=true;flCall(t.c,'onTapUp',[FL.ev({localPosition:[t.lx,t.ly],canvasPosition:[x,y],devicePosition:[x,y]})])}}
  }catch(e){g.__flErr=e.message;ST.tickErr={msg:e.message,exc:!!e.dartExc,src:'jogo Flame'}}
  return used};
FL.key=function(kind,code,ch){
  if(!FL.live.length)return false;var used=false;
  var ev=ST.mkKey(kind,code,ch),keys={isSet:true,s:new Set(Array.from(ST.keys).map(function(k){return 'LogicalKeyboardKey.'+k}))};
  FL.live.forEach(function(g){if(!g.__loaded||g.__flErr)return;
    try{if(flIs(g,'KeyboardEvents')){used=true;flCall(g,'onKeyEvent',[ev,keys])}
      var walk=function(c){if(!c||c.__rm)return;if(c!==g&&flIs(c,'KeyboardHandler')){used=true;flCall(c,'onKeyEvent',[ev,keys])}flKids(c).slice().forEach(walk)};
      walk(g);if(g.f.world)walk(g.f.world)}
    catch(e){g.__flErr=e.message;ST.tickErr={msg:e.message,exc:!!e.dartExc,src:'jogo Flame'}}});
  return used};
FL.paint=function(raw,key,w,h){
  raw=String(raw||'').trim();
  var ent=FL.byKey[key];
  if(!ent||ent.raw!==raw){var gv;var isNew=/^(?:const\s+)?[A-Z]\w*\s*\(/.test(raw);gv=ST.value(raw);if(!gv||!flIs(gv,'FlameGame'))throw new Error('game precisa ser um FlameGame (por exemplo, game: MeuJogo())');
    ent=FL.byKey[key]={raw:raw,game:gv,isNew:isNew}}
  else if(!ent.isNew){var gv2=ST.value(raw);if(gv2!==ent.game&&gv2&&flIs(gv2,'FlameGame'))ent.game=gv2}
  var g=ent.game;
  if(g.__flErr)throw new Error(g.__flErr);
  var old=ST.sync;ST.sync=true;
  var cv={nat:'Canvas',f:{},st:{ops:[],clips:[],m:[1,0,0,1,0,0],clip:-1,stack:[]},src:'Canvas()'};
  try{FL.ensure(g,w,h);FL.render(g,cv)}catch(e){g.__flErr=e.message;throw e}finally{ST.sync=old}
  return{ops:cv.st.ops,clips:cv.st.clips}};
ST.FL=FL;FL.callM=flCall;FL.member=member;ST.flamePaint=FL.paint;ST.flamePointer=FL.pointer;ST.flameKey=FL.key;ST.flameLive=function(){return FL.live.length>0};
/* funções nativas que o prelúdio chama */
var FLN={
  __flAdd:function(p,c){return FL.add(p,c)},
  __flRemove:function(c){return FL.remove(c)},
  __flMounted:function(c){return !!(c&&c.__mounted&&!c.__rm)},
  __flRemoved:function(c){return !!(c&&c.__rm)},
  __flRoot:function(c){var g=flRootOf(c);if(!g)throw exc('Este componente ainda não está no jogo: use game só depois do onLoad.');return g},
  __flCenter:function(c){var a=FL.absCenter(c);return mkVec(a[0],a[1])},
  __flAbsPos:function(c){var tl=FL.topLeft(c);return mkVec(tl[0]+nn(c.f.anchor.f.x)*vx(c.f.size),tl[1]+nn(c.f.anchor.f.y)*vy(c.f.size))},
  __flTopLeft:function(c){var tl=FL.topLeft(c);return mkVec(tl[0],tl[1])},
  __flRect:function(c){var r=FL.rect(c);return mkRect(r[0],r[1],r[2],r[3])},
  __flAngleTo:function(c,t){var a=FL.absCenter(c);return new Dbl(Math.atan2(vy(t)-a[1],vx(t)-a[0])+Math.PI/2)},
  __flVisible:function(cam){var g=flRootOf(cam),t=g?FL.camT(g):{ax:0,ay:0,z:1,px:0,py:0},w=g?vx(g.f.size):360,h=g?vy(g.f.size):640;return mkRect(t.px-t.ax/t.z,t.py-t.ay/t.z,w/t.z,h/t.z)},
  __flImage:function(p){var s=String(p),S=window.OF_SPRITES||{};if(S[s])return mkImg(s);var b=s.split('/').pop(),k='assets/sprites/'+b;if(S[k])return mkImg(k);
    throw exc('Unable to load asset: "'+s+'". O simulador tem estes sprites: '+Object.keys(S).map(function(x){return x.split('/').pop()}).join(', '))},
  __flImgSize:function(im){if(!im||im.nat!=='Img')throw exc('Sprite precisa de uma imagem carregada');return mkVec(nn(im.f.width),nn(im.f.height))}
};
"""

UI_EVENTS = r"""/* ===== Oficina 2: toque, arrasto e teclado no GameWidget (Flame) ===== */
var gwDrag=null;
function gwPos(el,e){var sr=screen.getBoundingClientRect(),k=sr.width/360||1,rc=el.getBoundingClientRect();return[(e.clientX-rc.left)/k,(e.clientY-rc.top)/k]}
screen.addEventListener('pointerdown',function(e){
  if(!(S.run&&ST.active)||!ST.flamePointer)return;var el=e.target.closest&&e.target.closest('.gw');if(!el)return;
  var p=gwPos(el,e);gwDrag={el:el,key:el.dataset.gwk,id:e.pointerId,last:p,hist:[[performance.now(),p]]};
  try{screen.setPointerCapture(e.pointerId)}catch(x){}
  if(ST.flamePointer('down',el.dataset.gwk,p[0],p[1],0,0,0,0))e.preventDefault()});
screen.addEventListener('pointermove',function(e){
  var d=gwDrag;if(!d||e.pointerId!==d.id)return;var p=gwPos(d.el,e),dx=p[0]-d.last[0],dy=p[1]-d.last[1];if(!dx&&!dy)return;
  d.last=p;d.hist.push([performance.now(),p]);if(d.hist.length>8)d.hist.shift();ST.flamePointer('move',d.key,p[0],p[1],dx,dy,0,0)});
function gwEnd(e){var d=gwDrag;if(!d||e.pointerId!==d.id)return;gwDrag=null;var p=gwPos(d.el,e),h=d.hist,now=performance.now(),a=h[0];
  for(var i=0;i<h.length;i++)if(now-h[i][0]<=100){a=h[i];break}var b=h[h.length-1],dt=Math.max(1,b[0]-a[0])/1000;
  ST.flamePointer('up',d.key,p[0],p[1],0,0,(b[1][0]-a[1][0])/dt,(b[1][1]-a[1][1])/dt)}
screen.addEventListener('pointerup',gwEnd);screen.addEventListener('pointercancel',gwEnd);
"""


def prelude_js():
    return json.dumps((ROOT / 'flame_prelude.dart').read_text())


def patch(src):
    # ---- setters em classes
    src = sub1(src,
        "  var ci={name:name,fields:[],params:[],methods:{},getters:{},",
        "  var ci={name:name,fields:[],params:[],methods:{},getters:{},setters:{},",
        'ci setters')
    src = sub1(src,
        "    var g=GETA.exec(ch);",
        "    var sset=/^(?:@\\w+\\s+)?set\\s+(\\w+)\\s*\\(\\s*(?:[\\w<>?,]+\\s+)?(\\w+)\\s*\\)\\s*(?:=>\\s*([\\s\\S]+?);|(\\{[\\s\\S]*\\}))$/.exec(ch);"
        "if(sset){ci.setters[sset[1]]={param:sset[2],body:sset[3]!==undefined?sset[3]:sset[4],arrow:sset[3]!==undefined};return}\n"
        "    var g=GETA.exec(ch);",
        'parse setter')
    src = sub1(src, "function mkDur(ms){", VEC + SETTERS + FL + "function mkDur(ms){", 'flame helpers')
    src = sub1(src,
        "    if(o&&o.cls){o.f[ast.name]=coerce(fieldType(ST.dataClasses[o.cls],ast.name),val);mutated=true;return}\n",
        "    if(setMemberX(o,ast.name,val))return;\n",
        'assignTo setter')
    src = sub1(src,
        "  if(env.self&&hasOwn(env.self.f,n)){env.self.f[n]=coerce(fieldType(ST.dataClasses[env.self.cls],n),v);mutated=true;return}\n",
        "  if(env.self&&hasOwn(env.self.f,n)){env.self.f[n]=coerce(fieldType(ST.dataClasses[env.self.cls],n),v);mutated=true;return}\n"
        "  if(env.self&&env.self.cls){var stx=setterOf(env.self.cls,n);if(stx){callSetter(env.self,stx,v);return}}\n",
        'setVar setter')
    src = sub1(src,
        "if(op.set){var sv2=ev(op.set,env);if(co&&(co.cls||co.nat==='Paint')){co.f[op.name]=sv2;mutated=true}",
        "if(op.set){var sv2=ev(op.set,env);if(co&&co.nat==='Paint'){co.f[op.name]=sv2;mutated=true}else if(setMemberX(co,op.name,sv2)){}",
        'casc setter')
    # ---- parâmetro nomeado opcional não passado vale null (radius == null ? ... funciona)
    src = sub1(src,
        "    if(found)vals[pr.name]=val});\n  return vals}",
        "    if(found)vals[pr.name]=val;else if(pr.plain)vals[pr.name]=null});\n  return vals}",
        'bindArgs null')
    # ---- this.campo é o campo do objeto, mesmo quando um parâmetro tem o mesmo nome (this.amount = amount)
    src = sub1(src,
        "p.i+=3;var thn=p.t[p.i-1].v;if(p.is('(')){p.i++;return{t:'fn',name:thn,args:pArgs(p)}}return{t:'id',name:thn}}",
        "p.i+=3;var thn=p.t[p.i-1].v;if(p.is('(')){p.i++;return{t:'fn',name:thn,args:pArgs(p)}}return{t:'mem',o:{t:'id',name:'this'},name:thn,args:null}}",
        'this.field')
    src = sub1(src,
        "      out.push({name:tm?tm[1]:mm[1],named:sg[1]===1,def:def})})});\n  return out}",
        "      out.push({name:tm?tm[1]:mm[1],named:sg[1]===1,def:def,plain:!tm})})});\n  return out}",
        'declParams plain')
    # ---- campo = await algo(); dentro de um objeto (antes criava uma variável local)
    src = sub1(src,
        "  if(!hasOwn(env.locals,name)&&ST.fields[name]){ST.fields[name].value=coerce(ST.fields[name].type,val);mutated=true}\n  else env.locals[name]=val}",
        "  if(!hasOwn(env.locals,name)&&ST.fields[name]){ST.fields[name].value=coerce(ST.fields[name].type,val);mutated=true}\n"
        "  else if(!hasOwn(env.locals,name)&&(function(){var e=env;while(e){if(e.self&&e.self.cls&&(hasOwn(e.self.f,name)||setterOf(e.self.cls,name)))return true;e=e.parent}return false})()){setVar(env,name,val)}\n"
        "  else env.locals[name]=val}",
        'bindDecl self field')
    # Timer do Flame (Timer(1.5, repeat: true, onTick: ...)) vira FlTimer; Timer(Duration, ...) continua sendo o do dart:async
    src = sub1(src,
        "      if(a.args&&(a.name==='Timer.periodic'||a.name==='Timer')){",
        "      if(a.args&&a.name==='Timer'&&ST.dataClasses.FlTimer){var ft0=a.args.filter(function(x){return !x.name})[0];if(ft0&&ft0.ast!==undefined&&typeof nn(ev(ft0.ast,env))==='number')return construct('FlTimer',evalArgs(a,env))}\n"
        "      if(a.args&&(a.name==='Timer.periodic'||a.name==='Timer')){",
        'Flame Timer')
    # ---- objetos com ciclos (componente <-> pai) não estouram a pilha ao virar texto
    src = sub1(src,
        "  if(v&&v.cls)return v.cls+'('+Object.keys(v.f).map(function(k){return k+': '+lit(v.f[k])}).join(', ')+')';",
        "  if(v&&v.cls){var fkc=null;Object.keys(ST.fields||{}).forEach(function(k){if(ST.fields[k].value===v)fkc=k});if(fkc)return fkc;\n"
        "    if(isSub(v.cls,'Component')||lit.d>6)return v.cls+'()';lit.d=(lit.d||0)+1;try{return v.cls+'('+Object.keys(v.f).map(function(k){return k+': '+lit(v.f[k])}).join(', ')+')'}finally{lit.d--}}",
        'lit cycles')
    # ---- () => contador++ e (v) => x = v: corpo de seta que é uma atribuição vira um bloco
    src = sub1(src,
        "  if(p.eat('=>')){lam.body=pTern(p);lam.src=p.src.slice(startTok.s,p.t[p.i-1].e)}",
        "  if(p.eat('=>')){var k0=p.i,dd2=0,asg=false,kk=k0;\n"
        "    for(;kk<t.length;kk++){var tk2=t[kk];if(tk2.k!=='p')continue;if('([{'.indexOf(tk2.v)>=0&&tk2.v.length===1)dd2++;else if(')]}'.indexOf(tk2.v)>=0&&tk2.v.length===1){if(dd2===0)break;dd2--}else if(dd2===0&&(tk2.v===','||tk2.v===';'))break;else if(dd2===0&&/^(=|\\+=|-=|\\*=|\\/=|\\?\\?=|\\+\\+|--|~\\/=|%=)$/.test(tk2.v))asg=true}\n"
        "    if(asg&&kk>k0){lam.block='{'+p.src.slice(t[k0].s,t[kk-1].e)+';}';p.i=kk;lam.src=p.src.slice(startTok.s,t[kk-1].e);return lam}\n"
        "    lam.body=pTern(p);lam.src=p.src.slice(startTok.s,p.t[p.i-1].e)}",
        'arrow assignment')
    # ---- Vector2
    src = sub1(src, "  if(v.nat==='Random'){\n",
               "  if(v.nat==='Vec2')return vecMember(v,name,args);\n"
               "  if(v.nat==='FlEvent'){if(hasOwn(v.f,name))return v.f[name];if(name==='stopPropagation'){v.f.continuePropagation=false;return null}return null}\n"
               "  if(v.nat==='Random'){\n", 'natMember Vec2')
    src = sub1(src,
        "      if(a.args&&NATCTOR[a.name])return natCtor(a.name,evalArgs(a,env));",
        "      if(a.args&&/^Vector2(?:\\.(?:zero|all|copy|array|random))?$/.test(a.name)){var vca=evalArgs(a,env).filter(function(x){return !x.name}).map(function(x){return x.val});return vecCtor(a.name,vca)}\n"
        "      if(a.args&&a.name==='FlameAudio.play'){var fap=evalArgs(a,env),fav=fap.filter(function(x){return x.name==='volume'})[0];sfx(somOf(fap[0].val),fav?nn(fav.val):1);return null}\n"
        "      if(a.args&&/^FlameAudio\\.\\w+$/.test(a.name))return null;\n"
        "      if(a.args&&NATCTOR[a.name])return natCtor(a.name,evalArgs(a,env));",
        'ctor Vector2')
    src = sub1(src,
        "  if(l&&l.nat==='Offset'&&r&&r.nat==='Offset'&&(op==='+'||op==='-')){",
        "  if(isVec(l)&&isVec(r)){switch(op){case '+':return mkVec(vx(l)+vx(r),vy(l)+vy(r));case '-':return mkVec(vx(l)-vx(r),vy(l)-vy(r));case '==':return vx(l)===vx(r)&&vy(l)===vy(r);case '!=':return !(vx(l)===vx(r)&&vy(l)===vy(r))}}\n"
        "  if(isVec(l)&&r!=null&&typeof nn(r)==='number'){switch(op){case '*':return mkVec(vx(l)*nn(r),vy(l)*nn(r));case '/':return mkVec(vx(l)/nn(r),vy(l)/nn(r))}}\n"
        "  if(isVec(r)&&l!=null&&typeof nn(l)==='number'&&op==='*')return mkVec(vx(r)*nn(l),vy(r)*nn(l));\n"
        "  if(l&&l.nat==='Offset'&&r&&r.nat==='Offset'&&(op==='+'||op==='-')){",
        'binary Vec2')
    src = sub1(src,
        "    case 'un':{var v=ev(a.a,env);if(a.op==='!')return !v;return isD(v)?new Dbl(-v.v):-v}",
        "    case 'un':{var v=ev(a.a,env);if(a.op==='!')return !v;if(isVec(v))return mkVec(-vx(v),-vy(v));if(v&&v.nat==='Offset')return mkOffset(-nn(v.f.dx),-nn(v.f.dy));return isD(v)?new Dbl(-v.v):-v}",
        'unary Vec2')
    # ---- Set<LogicalKeyboardKey>.contains(LogicalKeyboardKey.x)
    src = sub1(src,
        "      case 'contains':return sset.has(nn(args[0]));",
        "      case 'contains':return sset.has(nn(args[0]))||(isRaw(args[0])&&sset.has(args[0].raw));",
        'set contains raw')
    # ---- tear-off de método de objeto (onTick: criarInimigo dentro de um componente)
    src = sub1(src,
        "  if(n==='rootBundle')return{nat:'Bundle',f:{},src:'rootBundle'};\n",
        "  if(n==='rootBundle')return{nat:'Bundle',f:{},src:'rootBundle'};\n"
        "  var tvs=env.self||curThis(env);if(tvs&&tvs.cls){var mtf=methodOf(tvs.cls,n);if(mtf)return{lam:true,src:n,pn:[],call:function(args){return runMethod(mtf,args,tvs)}}}\n",
        'lookup method tear-off')
    # ---- funções nativas do prelúdio
    src = sub1(src,
        "      if(a.name==='createTicker'&&a.args.length&&a.args[0].ast!==undefined)return mkTicker(cbArg(a.args[0].ast,env));\n",
        "      if(a.name==='createTicker'&&a.args.length&&a.args[0].ast!==undefined)return mkTicker(cbArg(a.args[0].ast,env));\n"
        "      if(FLN[a.name]&&a.name.indexOf('__fl')===0){var fla=a.args.map(function(x){if(x.ast===undefined)throw new Error('arg');return ev(x.ast,env)});return FLN[a.name].apply(null,fla)}\n",
        'fn FLN')
    # ---- laço do Flame no mesmo relógio do Ticker
    src = sub1(src,
        "    if(v.nat==='Ticker'||v.nat==='Timer'){if(gameStep(v,now))changed=true;return}\n",
        "    if(v.nat==='FlLoop'){if(FL.step(now))changed=true;return}\n"
        "    if(v.nat==='Ticker'||v.nat==='Timer'){if(gameStep(v,now))changed=true;return}\n",
        'tick FlLoop')
    src = sub1(src, "ST.reset=function(){\n", "ST.reset=function(){\n  FL.reset();\n", 'reset FL')
    src = sub1(src, "ST.load=function(info){\n  var keepG=", "ST.load=function(info){\n  FL.reset();\n  var keepG=", 'load FL')
    # ---- prelúdio acrescentado ao código que importa o Flame
    src = sub1(src,
        "ST.extract=function(src){src=stripComments(src);",
        "var FLAME_PRELUDE=" + prelude_js() + ";\n"
        "ST.extract=function(src){src=stripComments(src);if(/package:flame\\//.test(src))src=src+'\\n'+stripComments(FLAME_PRELUDE);",
        'prelude')
    src = sub1(src,
        "ST.fxOn=/\\b(GoRouter|Navigator|",
        "ST.fxOn=/\\b(GameWidget|GoRouter|Navigator|",
        'fxOn GameWidget')

    # ---- widget GameWidget
    src = sub1(src,
        " KeyboardListener:{cat:'struct',slots:{child:'one'},",
        " GameWidget:{cat:'struct',slots:{},desc:'Mostra um jogo do Flame (game: MeuJogo()). Ocupa todo o espaço que recebe.'},\n"
        " KeyboardListener:{cat:'struct',slots:{child:'one'},",
        'schema GameWidget')
    src = sub1(src,
        "    case 'SafeArea':case 'GestureDetector':case 'InkWell':case 'Form':case 'FittedBox':case 'Focus':case 'KeyboardListener':{",
        "    case 'GameWidget':{d.className+=' gw';d.dataset.gwk=path.join('>');d.style.flex='1 1 auto';d.style.alignSelf='stretch';d.style.width='100%';d.style.height='100%';d.style.minHeight='0';d.style.position='relative';d.style.overflow='hidden';d.style.touchAction='none';\n"
        "      var gwr=M.rawProp(n,'game'),gwk=path.join('>'),gwl=document.createElement('div');gwl.className='gwc';d.appendChild(gwl);\n"
        "      if(!gwr||!gwr.trim()){gwl.className+=' cper';gwl.textContent='GameWidget precisa de game: MeuJogo()';break}\n"
        "      R_opts.post.push(function(){var w=d.clientWidth||360,h=d.clientHeight||600,res=null;try{res=OF.ST.flamePaint(gwr,gwk,w,h)}catch(e){gwl.className='gwc cper';gwl.textContent='Flame: '+e.message;return}if(res){gwl.innerHTML='';gwl.appendChild(paintCanvas(res,w,h))}});\n"
        "      break}\n"
        "    case 'SafeArea':case 'GestureDetector':case 'InkWell':case 'Form':case 'FittedBox':case 'Focus':case 'KeyboardListener':{",
        'render GameWidget')
    src = sub1(src, ".nd.cpt>.cpl{", ".nd.gw{display:block}.nd.gw>.gwc{position:absolute;inset:0}.nd.gw>.gwc.cper{color:#B3261E;font-size:12px;padding:6px;background:rgba(255,255,255,.9);inset:0 0 auto 0}\n.nd.cpt>.cpl{", 'css gw')
    # runApp(GameWidget(game: ...)) sem build(): a raiz é o argumento do runApp
    src = sub1(src,
        "    if(i<0&&t[0]&&t[0].k==='id'&&/^[A-Z]/.test(t[0].v))i=0;\n",
        "    if(i<0){for(x=0;x<t.length-2;x++)if(t[x].k==='id'&&t[x].v==='runApp'&&t[x+1].v==='('&&t[x+2].k==='id'&&/^(?:GameWidget|const)$/.test(t[x+2].v)){i=x+2;if(t[i].v==='const')i++;break}}\n"
        "    if(i<0&&t[0]&&t[0].k==='id'&&/^[A-Z]/.test(t[0].v))i=0;\n",
        'parse runApp root')
    # eventos do navegador para o Flame (o código do arrasto de widgets ignora o GameWidget)
    src = sub1(src, "/* ===== Oficina 2: toque instantâneo, arrastar e teclado ===== */",
               UI_EVENTS + "/* ===== Oficina 2: toque instantâneo, arrastar e teclado ===== */", 'ui flame events')
    src = sub1(src,
        "function kDispatch(kind,e){\n  if(!(S.run&&ST.active))return false;\n",
        "function kDispatch(kind,e){\n  if(!(S.run&&ST.active))return false;\n"
        "  var flUsed=ST.flameKey?ST.flameKey(kind,kName(e),e.key&&e.key.length===1?e.key:null):false;\n",
        'kDispatch flame')
    src = sub1(src,
        "  var els=[].slice.call(screen.querySelectorAll('.kbd')).reverse(),done=false,code=kName(e);",
        "  var els=[].slice.call(screen.querySelectorAll('.kbd')).reverse(),done=!!flUsed,code=kName(e);",
        'kDispatch done')
    src = sub1(src,
        "  if((used||gLoop())&&/^(arrow\\w+|space)$/.test(n))e.preventDefault()});",
        "  if((used||gLoop()||(ST.flameLive&&ST.flameLive()))&&/^(arrow\\w+|space)$/.test(n))e.preventDefault()});",
        'keydown prevent flame')
    return src
