# Oficina Flutter 2, frente 7c: sensors_plus (acelerômetro, giroscópio, magnetômetro) e Stream.listen.
# No celular (aberto pela Vercel ou GitHub Pages) os valores vêm do DeviceMotionEvent; no computador, do painel de inclinação.
from patch_engine import sub1

GLOBAL = r"""/* ===== Oficina 2: sensores de movimento (DeviceMotionEvent no celular, painel de inclinação no computador) ===== */
window.OF_SENS={acc:[0,0,9.81],user:[0,0,0],gyro:[0,0,0],mag:[22,5,-40],real:false,tx:0,ty:0,usado:false};
(function(){var ios=/iPhone|iPad|iPod/.test(navigator.userAgent)||(navigator.platform==='MacIntel'&&navigator.maxTouchPoints>1),liga=false;
  function onMotion(e){var g=e.accelerationIncludingGravity,a=e.acceleration,r=e.rotationRate,S=window.OF_SENS,k=ios?-1:1;
    if(g&&g.x!=null){S.real=true;S.acc=[k*g.x,k*g.y,k*g.z]}if(a&&a.x!=null)S.user=[k*a.x,k*a.y,k*a.z];
    if(r&&r.alpha!=null){var d=Math.PI/180;S.gyro=[r.beta*d,r.gamma*d,r.alpha*d]}}
  window.OF_SENS_LIGAR=function(){if(liga)return;if(typeof DeviceMotionEvent==='undefined')return;
    if(typeof DeviceMotionEvent.requestPermission==='function'){DeviceMotionEvent.requestPermission().then(function(r){if(r==='granted'){liga=true;window.addEventListener('devicemotion',onMotion)}}).catch(function(){})}
    else{liga=true;window.addEventListener('devicemotion',onMotion)}};
  if(typeof DeviceMotionEvent!=='undefined'&&typeof DeviceMotionEvent.requestPermission!=='function')window.OF_SENS_LIGAR();
  window.OF_SENS_INCLINA=function(tx,ty){var S=window.OF_SENS;S.tx=Math.max(-1,Math.min(1,tx));S.ty=Math.max(-1,Math.min(1,ty));if(S.real)return;
    var G=9.81,ax=-G*Math.sin(S.tx*Math.PI/2),ay=G*Math.sin(S.ty*Math.PI/2);S.acc=[ax,ay,Math.sqrt(Math.max(0,G*G-ax*ax-ay*ay))]};
})();
"""

ENGINE = r"""/* ===== Oficina 2: sensors_plus e Stream.listen ===== */
var SENSF={accelerometerEventStream:'acc',userAccelerometerEventStream:'user',gyroscopeEventStream:'gyro',magnetometerEventStream:'mag',
  accelerometerEvents:'acc',userAccelerometerEvents:'user',gyroscopeEvents:'gyro',magnetometerEvents:'mag'};
var SENSN={acc:'AccelerometerEvent',user:'UserAccelerometerEvent',gyro:'GyroscopeEvent',mag:'MagnetometerEvent'};
function sensMs(v){var s=String(pcol(v)||''),m;if(!s)return 20;if(/gameInterval/.test(s))return 20;if(/uiInterval/.test(s))return 66;if(/normalInterval/.test(s))return 200;if(/fastestInterval/.test(s))return 16;
  if((m=/milliseconds:\s*(\d+)/.exec(s)))return Math.max(16,+m[1]);if((m=/microseconds:\s*(\d+)/.exec(s)))return Math.max(16,+m[1]/1000);return 20}
function sensStream(k,ms){window.OF_SENS.usado=true;if(window.OF_SENS_PAD)OF_SENS_PAD();
  return{nat:'Stream',kind:'live',sensor:k,ms:ms||20,get:function(){var v=window.OF_SENS[k];return{nat:'FlEvent',f:{x:new Dbl(v[0]),y:new Dbl(v[1]),z:new Dbl(v[2]),timestamp:{raw:'DateTime.now()'}},src:SENSN[k]+'(x: '+v[0].toFixed(2)+', y: '+v[1].toFixed(2)+', z: '+v[2].toFixed(2)+')'}},src:'Stream<'+SENSN[k]+'>'}}
function streamListen(sv,args){var cb=null,ond=null;args.forEach(function(a){if(a&&a.lam&&!cb)cb=a});
  var sub={nat:'SensSub',f:{},tm:{on:true,paused:false,next:0,ms:sv.ms||20,cb:cb,sv:sv,n:0},src:'StreamSubscription'};
  if(sv.kind==='ctl'){var c=sv.ctl.st;(c.subs||(c.subs=[])).push(sub);return sub}
  if(sv.kind==='iter'&&!sv.ms){toIter(sv.items).forEach(function(x){if(cb)callLam(cb,[x])});return sub}
  sub.tm.next=0;ST.anims.push(sub);if(typeof animKickHook==='function')animKickHook();return sub}
function sensStep(v,now){var tm=v.tm;if(!tm.on){animDrop(v);return false}if(window.OF_SENS_PAD&&!v.velho)OF_SENS_PAD();if(!tm.cb)return now>=tm.next?(tm.next=now+tm.ms,true):false;if(tm.paused||now<tm.next)return false;
  tm.next=now+tm.ms;var sv=tm.sv,ev2;
  if(sv.sensor)ev2=sv.get();
  else if(sv.kind==='periodic'){ev2=sv.lam?callLam(sv.lam,[tm.n]):tm.n;tm.n++}
  else if(sv.kind==='iter'){var it=toIter(sv.items);if(tm.n>=it.length&&!sv.inf){tm.on=false;animDrop(v);return false}ev2=it[tm.n%Math.max(1,it.length)];tm.n++}
  else if(sv.kind==='live'){ev2=sv.get()}
  steps=0;try{callLam(tm.cb,[ev2])}catch(e){tm.on=false;animDrop(v);ST.tickErr={msg:e.message,exc:!!e.dartExc,src:'listen'}}return true}
function subMember(v,name){var tm=v.tm;switch(name){case 'cancel':tm.on=false;animDrop(v);if(tm.sv&&tm.sv.kind==='ctl'){var ss=tm.sv.ctl.st.subs||[],ix=ss.indexOf(v);if(ix>=0)ss.splice(ix,1)}return null;
  case 'pause':tm.paused=true;return null;case 'resume':tm.paused=false;return null;case 'isPaused':return !!tm.paused;case 'onData':if(arguments[2]&&arguments[2][0])tm.cb=arguments[2][0];return null}return null}
"""


def patch(src):
    src = sub1(src, "window.OF_MUSICAS=", GLOBAL + "window.OF_MUSICAS=", 'sens global')
    src = sub1(src, "/* ===== Oficina 2: curvas, pinça, consultas de componentes ===== */",
               ENGINE + "/* ===== Oficina 2: curvas, pinça, consultas de componentes ===== */", 'sens engine')
    # funções e getters do sensors_plus
    src = sub1(src, "      if(a.args&&NATCTOR[a.name])return natCtor(a.name,evalArgs(a,env));",
        "      if(a.args&&SENSF[a.name]){var sva=evalArgs(a,env),spd=sva.filter(function(x){return x.name==='samplingPeriod'})[0];return sensStream(SENSF[a.name],sensMs(spd&&spd.val))}\n"
        "      if(a.args&&NATCTOR[a.name])return natCtor(a.name,evalArgs(a,env));", 'sens call')
    src = sub1(src, "      if(a.name==='decodeImageFromList'&&a.args.length&&a.args[0].ast!==undefined){",
        "      if(SENSF[a.name]&&/Stream$/.test(a.name)){var sfa=a.args.filter(function(x){return x.name==='samplingPeriod'})[0];return sensStream(SENSF[a.name],sensMs(sfa&&sfa.ast!==undefined?ev(sfa.ast,env):null))}\n"
        "      if(a.name==='decodeImageFromList'&&a.args.length&&a.args[0].ast!==undefined){", 'sens fn')
    src = sub1(src, "  if(n==='BodyType')return{nat:'BodyTypeNS',f:{},src:'BodyType'};\n",
        "  if(n==='BodyType')return{nat:'BodyTypeNS',f:{},src:'BodyType'};\n"
        "  if(SENSF[n]&&/Events$/.test(n))return sensStream(SENSF[n],20);\n", 'sens lookup')
    # Stream.listen e StreamSubscription
    src = sub1(src, "  if(v&&v.nat==='BodyTypeNS')return name;\n",
        "  if(v&&v.nat==='BodyTypeNS')return name;\n"
        "  if(v&&v.nat==='Stream'&&name==='listen')return streamListen(v,args||[]);\n"
        "  if(v&&v.nat==='SensSub')return subMember(v,name,args||[]);\n", 'listen member')
    src = sub1(src, "    if(v.nat==='Ticker'||v.nat==='Timer'){if(gameStep(v,now))changed=true;return}",
        "    if(v.nat==='Ticker'||v.nat==='Timer'){if(gameStep(v,now))changed=true;return}\n"
        "    if(v.nat==='SensSub'){if(sensStep(v,now))changed=true;return}", 'tick sens')
    src = sub1(src, "      case 'add':sc0.has=true;sc0.last=args[0];sc0.err=null;dirty=true;return null;",
        "      case 'add':sc0.has=true;sc0.last=args[0];sc0.err=null;dirty=true;(sc0.subs||[]).slice().forEach(function(sb){if(sb.tm.on&&!sb.tm.paused&&sb.tm.cb)callLam(sb.tm.cb,[args[0]])});return null;",
        'ctl add listeners')
    src = sub1(src, "  var keepG=(ST.anims||[]).filter(function(v){return v.nat==='Ticker'||v.nat==='Timer'});",
        "  var keepG=(ST.anims||[]).filter(function(v){return v.nat==='Ticker'||v.nat==='Timer'||v.nat==='SensSub'});", 'keep sens')
    src = sub1(src, "!(ST.anims||[]).some(function(v){return v.nat==='Ticker'||v.nat==='Timer'}))toast(",
        "!(ST.anims||[]).some(function(v){return v.nat==='Ticker'||v.nat==='Timer'||v.nat==='SensSub'}))toast(", 'toast sens')
    # StreamBuilder com sensor: redesenha no ritmo do sensor
    src = sub1(src, "  if(sv.nat==='StreamController')sv={nat:'Stream',kind:'ctl',ctl:sv};",
        "  if(sv.nat==='StreamController')sv={nat:'Stream',kind:'ctl',ctl:sv};\n"
        "  if(sv.sensor&&!(ST.anims||[]).some(function(a){return a.nat==='SensSub'&&!a.tm.cb})){ST.anims.push({nat:'SensSub',f:{},tm:{on:true,next:0,ms:Math.max(33,sv.ms),cb:null},src:'StreamSubscription'})}",
        'streambuilder sens')
    # toque na tela do celular pede permissão dos sensores (iPhone)
    src = sub1(src, "screen.addEventListener('pointerdown',function(e){\n  if(!(S.run&&ST.active)||!ST.flamePointer)return;",
        "screen.addEventListener('pointerdown',function(){if(window.OF_SENS&&OF_SENS.usado&&window.OF_SENS_LIGAR)OF_SENS_LIGAR()},true);\n"
        "screen.addEventListener('pointerdown',function(e){\n  if(!(S.run&&ST.active)||!ST.flamePointer)return;", 'sens permission')
    src = sub1(src, "function animKick(){", "function animKickHook(){try{animKick()}catch(e){}}\nfunction animKick(){", 'kick hook')
    src = sub1(src, "ST.load=function(info){\n  FL.reset();", "ST.load=function(info){\n  FL.reset();if(window.OF_SENS_ESCONDE)OF_SENS_ESCONDE();", 'sens hide')
    return src


PAD = r"""<style>
#tiltPad{position:fixed;left:16px;bottom:16px;z-index:60;background:var(--panel,#fff);border:1px solid var(--line,#ccd);border-radius:12px;padding:10px;box-shadow:0 6px 24px rgba(0,0,0,.18);font:12px/1.3 system-ui,sans-serif;color:var(--ink,#123);width:150px}
#tiltPad b{display:block;margin-bottom:6px;font-size:12.5px}
#tiltPad .tz{position:relative;width:130px;height:130px;border-radius:50%;background:repeating-radial-gradient(circle,transparent 0 20px,rgba(128,128,160,.15) 20px 21px),var(--panel2,#eef);border:1px solid var(--line,#ccd);touch-action:none;cursor:grab}
#tiltPad .tz i{position:absolute;width:26px;height:26px;margin:-13px 0 0 -13px;border-radius:50%;background:#2a6df4;left:50%;top:50%;box-shadow:0 2px 6px rgba(0,0,0,.3)}
#tiltPad .tr{display:flex;gap:6px;margin-top:8px;flex-wrap:wrap}#tiltPad button{font:600 11.5px system-ui,sans-serif;padding:4px 8px;border-radius:999px;border:1px solid var(--line,#ccd);background:var(--panel2,#eef);color:inherit;cursor:pointer}
#tiltPad .tv{margin-top:6px;font-family:ui-monospace,monospace;font-size:11px;opacity:.8}
</style>
<div id="tiltPad" hidden role="group" aria-label="Inclinação do celular simulado">
 <b>📐 Inclinar o celular</b>
 <div class="tz" title="Arraste a bolinha para inclinar o celular simulado (acelerômetro)"><i></i></div>
 <div class="tr"><button type="button" data-t="0">Nivelar</button><button type="button" data-t="x">Fechar</button></div>
 <div class="tv" aria-live="off"></div>
</div>
<script>
(function(){
  var P=document.getElementById('tiltPad'),Z=P.querySelector('.tz'),D=Z.querySelector('i'),V=P.querySelector('.tv'),fechado=false,arr=false;
  function mostrar(){var S=window.OF_SENS;V.textContent=S.real?'Usando os sensores do celular':'x '+S.acc[0].toFixed(1)+'  y '+S.acc[1].toFixed(1)+'  z '+S.acc[2].toFixed(1)}
  function por(tx,ty){OF_SENS_INCLINA(tx,ty);D.style.left=(50+tx*42)+'%';D.style.top=(50+ty*42)+'%';mostrar()}
  function pos(e){var r=Z.getBoundingClientRect(),x=(e.clientX-r.left)/r.width*2-1,y=(e.clientY-r.top)/r.height*2-1,l=Math.hypot(x,y);if(l>1){x/=l;y/=l}por(x,y)}
  Z.addEventListener('pointerdown',function(e){arr=true;try{Z.setPointerCapture(e.pointerId)}catch(x){}pos(e)});
  Z.addEventListener('pointermove',function(e){if(arr)pos(e)});
  Z.addEventListener('pointerup',function(){arr=false});Z.addEventListener('pointercancel',function(){arr=false});
  P.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;if(b.dataset.t==='0')por(0,0);else{fechado=true;P.hidden=true}});
  window.OF_SENS_ESCONDE=function(){P.hidden=true};
  window.OF_SENS_PAD=function(){if(fechado||window.OF_SENS.real||!P.hidden)return;P.hidden=false;mostrar()};
  setInterval(function(){if(!P.hidden){if(window.OF_SENS.real)P.hidden=true;else mostrar()}},500);
})();
</script>
"""
