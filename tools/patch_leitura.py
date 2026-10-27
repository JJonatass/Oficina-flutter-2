# Oficina Flutter 2, frente 9: aulas de leitura (conteúdo teórico).
# Cada aula de leitura tem blocos (título, parágrafo, figura animada, dica) e um quiz no fim.
# A leitura abre num painel por cima da Oficina; o código de demonstração continua no editor.
from patch_engine import sub1

HTML = r"""<div class="modal" id="leModal" hidden role="dialog" aria-modal="true" aria-labelledby="leTit"><div class="mbox lebox">
  <div class="mh"><b id="leTit">Leitura</b><span class="sp"></span><span id="leProg" class="leprog"></span><button class="btn" id="leClose" aria-label="Fechar a leitura">✕</button></div>
  <div class="mb le" id="leBody"></div>
  <div class="lefoot"><span class="mt">O código desta aula está no editor: feche a leitura e experimente em ▶ Testar.</span><button class="btn pri" id="leOk">Ir para o código</button></div>
</div></div>
<style>
.lebox{width:min(820px,100%)}
.le{font-size:15px;line-height:1.6}
.le h2{font-family:'Bricolage Grotesque',system-ui,sans-serif;font-size:20px;margin:22px 0 6px;text-wrap:balance}
.le h2:first-child{margin-top:12px}
.le p{margin:0 0 10px;max-width:68ch}
.le code{font:13px 'JetBrains Mono',ui-monospace,monospace;background:var(--panel2);border:1px solid var(--line);border-radius:5px;padding:0 4px}
.le figure{margin:12px 0 16px;display:flex;flex-direction:column;gap:6px}
.le figure canvas{width:100%;height:auto;max-width:640px;border-radius:10px;background:var(--panel2);border:1px solid var(--line)}
.le figcaption{font-size:13px;color:var(--ink2);max-width:64ch}
.le .dica{border-left:4px solid var(--accent);background:var(--accent-soft);border-radius:0 8px 8px 0;padding:8px 12px;margin:10px 0 14px;max-width:68ch}
.le .dica b:first-child{display:block;font-size:12px;text-transform:uppercase;letter-spacing:.05em;margin-bottom:2px}
.le .quiz{margin-top:24px;border-top:1px solid var(--line);padding-top:8px}
.le .qq{margin:14px 0}
.le .qq>p{font-weight:600;margin-bottom:6px}
.le .qo{display:flex;flex-direction:column;gap:6px}
.le .qo button{font:inherit;font-size:14px;text-align:left;padding:8px 12px;border:1px solid var(--line);border-radius:8px;background:var(--panel);color:var(--ink);cursor:pointer}
.le .qo button:hover{border-color:var(--accent)}
.le .qo button.certa{border-color:var(--ok);background:rgba(10,132,103,.10)}
.le .qo button.errada{border-color:var(--err);background:rgba(196,43,59,.08)}
.le .qe{font-size:13.5px;color:var(--ink2);margin:6px 0 0;max-width:68ch}
.le .qres{font-weight:600;margin-top:10px}
.lefoot{display:flex;gap:12px;align-items:center;justify-content:space-between;flex-wrap:wrap;padding:10px 16px;border-top:1px solid var(--line)}
.leprog{font-size:12.5px;color:var(--ink2);margin-right:8px}
.lesson .lebtn{margin:4px 0 8px;align-self:start;justify-self:start;width:auto;height:auto}
</style>
"""

ENGINE = r"""
/* ===== Oficina 2: aulas de leitura ===== */
function leKey(L){return L.t.replace(/^\d+\.\s*/,'')}
function leMd(s){return esc(s).replace(/\*\*([^*]+)\*\*/g,'<b>$1</b>').replace(/`([^`]+)`/g,'<code>$1</code>').replace(/_([^_]+)_/g,'<i>$1</i>')}
function leQuiz(){try{var q=JSON.parse(localStorage.getItem('oficina2.quiz')||'{}');return q&&typeof q==='object'?q:{}}catch(e){return {}}}
function leLidos(){try{return JSON.parse(localStorage.getItem('oficina2.lidos')||'[]')}catch(e){return []}}
var leFigs=[],leAtual=null;
function leParar(){leFigs.forEach(function(f){f.vivo=false});leFigs=[]}
function leRender(L){
  var k=leKey(L),qz=leQuiz()[k]||{},h='';
  L.leitura.forEach(function(b){
    if(b.h)h+='<h2>'+leMd(b.h)+'</h2>';
    else if(b.p)h+='<p>'+leMd(b.p)+'</p>';
    else if(b.dica)h+='<div class="dica"><b>'+esc(b.titulo||'Dica')+'</b>'+leMd(b.dica)+'</div>';
    else if(b.fig)h+='<figure><canvas data-fig="'+esc(b.fig)+'" width="640" height="'+(b.alt||260)+'" role="img" aria-label="'+esc(b.legenda||'')+'"></canvas>'+(b.legenda?'<figcaption>'+leMd(b.legenda)+'</figcaption>':'')+'</figure>'});
  if(L.quiz&&L.quiz.length){
    h+='<div class="quiz"><h2>Teste rápido</h2>';
    L.quiz.forEach(function(q,i){var esc0=qz[i];
      h+='<div class="qq" data-q="'+i+'"><p>'+(i+1)+'. '+leMd(q.q)+'</p><div class="qo">'+q.ops.map(function(o,j){
        var cls=esc0==null?'':(j===q.ok?'certa':(j===esc0?'errada':''));
        return '<button type="button" data-o="'+j+'" class="'+cls+'"'+(esc0!=null?' aria-pressed="'+(j===esc0)+'"':'')+'>'+leMd(o)+'</button>'}).join('')+'</div>'+
        (esc0!=null?'<p class="qe">'+(esc0===q.ok?'✓ Isso. ':'✗ Não é essa. ')+leMd(q.exp)+'</p>':'')+'</div>'});
    var resp=Object.keys(qz).length,ac=L.quiz.filter(function(q,i){return qz[i]===q.ok}).length;
    h+='<p class="qres">'+(resp?'Acertos: '+ac+' de '+L.quiz.length+(ac===L.quiz.length?' 🏆':''):'Escolha uma resposta em cada pergunta.')+'</p></div>'}
  $('leBody').innerHTML=h;
  var ac2=L.quiz?L.quiz.filter(function(q,i){return qz[i]===q.ok}).length:0;
  $('leProg').textContent=L.quiz?('Teste: '+ac2+'/'+L.quiz.length):'';
  leParar();
  [].forEach.call($('leBody').querySelectorAll('canvas[data-fig]'),function(c){var fn=window.OF_FIGS&&OF_FIGS[c.dataset.fig];if(fn){var st={vivo:true};leFigs.push(st);fn(c,st)}})}
function leAbrir(L){if(!L||!L.leitura)return;leAtual=L;$('leTit').textContent='📖 '+L.t.replace(/^\d+\.\s*/,'');leRender(L);$('leModal').hidden=false;$('leBody').scrollTop=0;
  var ls=leLidos(),k=leKey(L);if(ls.indexOf(k)<0){ls.push(k);try{localStorage.setItem('oficina2.lidos',JSON.stringify(ls))}catch(e){}}
  setTimeout(function(){$('leClose').focus()},30)}
function leFechar(){$('leModal').hidden=true;leParar()}
function leAuto(L){if(leLidos().indexOf(leKey(L))<0)setTimeout(function(){leAbrir(L)},60)}
document.addEventListener('click',function(e){
  var t=e.target;if(!t||!t.closest)return;
  if(t.closest('#leBtn')){leAbrir(OF.LESSONS[S.lesson]);return}
  if(t.closest('#leClose')||t.closest('#leOk')){leFechar();return}
  if(t.id==='leModal'){leFechar();return}
  var b=t.closest('#leBody .qo button');if(b&&leAtual){var qi=+b.closest('.qq').dataset.q,oi=+b.dataset.o,k=leKey(leAtual),all=leQuiz();all[k]=all[k]||{};all[k][qi]=oi;
    try{localStorage.setItem('oficina2.quiz',JSON.stringify(all))}catch(e2){}
    var y=$('leBody').scrollTop;leRender(leAtual);$('leBody').scrollTop=y;
    var ok=leAtual.quiz.every(function(q,i){return all[k][i]===q.ok});if(ok){toast('Teste completo! 🏆');if(!leAtual.steps)markDone(leAtual)}}});
document.addEventListener('keydown',function(e){if(e.key==='Escape'&&$('leModal')&&!$('leModal').hidden)leFechar()});
"""

FIGS = r"""<script>
/* ===== Oficina 2: figuras animadas das aulas de leitura ===== */
(function(){
  function cor(n,pad){try{var v=getComputedStyle(document.documentElement).getPropertyValue(n).trim();return v||pad}catch(e){return pad}}
  function laco(c,st,desenha){var g=c.getContext('2d'),t0=performance.now();
    function f(agora){if(!st.vivo||!c.isConnected)return;var t=(agora-t0)/1000;g.setTransform(1,0,0,1,0,0);g.clearRect(0,0,c.width,c.height);desenha(g,t,c.width,c.height);requestAnimationFrame(f)}
    requestAnimationFrame(f)}
  function seta(g,x0,y0,x1,y1,cr,w){var dx=x1-x0,dy=y1-y0,l=Math.hypot(dx,dy);if(l<1)return;var ux=dx/l,uy=dy/l;g.strokeStyle=cr;g.lineWidth=w||3;g.lineCap='round';g.beginPath();g.moveTo(x0,y0);g.lineTo(x1,y1);g.moveTo(x1,y1);g.lineTo(x1-ux*12-uy*6,y1-uy*12+ux*6);g.moveTo(x1,y1);g.lineTo(x1-ux*12+uy*6,y1-uy*12-ux*6);g.stroke()}
  function txt(g,s,x,y,cr,tam,al){g.fillStyle=cr;g.font=(tam||14)+'px "IBM Plex Sans",system-ui,sans-serif';g.textAlign=al||'left';g.fillText(s,x,y)}
  var VERM='#E5484D',VERDE='#2BA36B',OURO='#E0A100',CAR='#D68C3E';
  window.OF_FIGS={
    vetor:function(c,st){laco(c,st,function(g,t,W,H){var ink=cor('--ink','#0F1B2D'),lin=cor('--line','#D6DDE7');
      g.strokeStyle=lin;g.lineWidth=1;for(var x=20;x<W;x+=40){g.beginPath();g.moveTo(x,0);g.lineTo(x,H);g.stroke()}for(var y=20;y<H;y+=40){g.beginPath();g.moveTo(0,y);g.lineTo(W,y);g.stroke()}
      var ox=140,oy=H-50,px=ox+200+130*Math.cos(t*0.7),py=oy-120+70*Math.sin(t*1.1),dx=px-ox,dy=py-oy,l=Math.hypot(dx,dy);
      g.strokeStyle=VERM;g.lineWidth=3;g.beginPath();g.moveTo(ox,oy);g.lineTo(px,oy);g.stroke();g.strokeStyle=VERDE;g.beginPath();g.moveTo(px,oy);g.lineTo(px,py);g.stroke();
      seta(g,ox,oy,px,py,ink,3);seta(g,ox,oy,ox+dx/l*60,oy+dy/l*60,OURO,5);
      g.fillStyle=CAR;g.beginPath();g.arc(ox,oy,12,0,7);g.fill();g.fillStyle=ink;g.beginPath();g.arc(px,py,6,0,7);g.fill();
      txt(g,'dx = '+Math.round(dx),(ox+px)/2,oy+22,VERM,15,'center');txt(g,'dy = '+Math.round(dy),px+10,(oy+py)/2,VERDE,15);
      txt(g,'|d| = '+Math.round(l),20,26,ink,15);txt(g,'unitário: ('+(dx/l).toFixed(2)+', '+(dy/l).toFixed(2)+')',20,48,OURO,15)})},
    circulo:function(c,st){laco(c,st,function(g,t,W,H){var ink=cor('--ink','#0F1B2D'),lin=cor('--line','#D6DDE7'),cx=170,cy=H/2,r=95,a=(t*0.8)%(2*Math.PI),px=cx+r*Math.cos(a),py=cy+r*Math.sin(a);
      g.strokeStyle=lin;g.lineWidth=2;g.beginPath();g.arc(cx,cy,r,0,7);g.stroke();g.beginPath();g.moveTo(cx-r-20,cy);g.lineTo(cx+r+20,cy);g.moveTo(cx,cy-r-20);g.lineTo(cx,cy+r+20);g.stroke();
      g.strokeStyle=OURO;g.lineWidth=3;g.beginPath();g.arc(cx,cy,26,0,a,false);g.stroke();
      g.strokeStyle=VERM;g.lineWidth=4;g.beginPath();g.moveTo(cx,cy);g.lineTo(px,cy);g.stroke();g.strokeStyle=VERDE;g.beginPath();g.moveTo(px,cy);g.lineTo(px,py);g.stroke();
      seta(g,cx,cy,px,py,ink,2);g.fillStyle=CAR;g.beginPath();g.arc(px,py,8,0,7);g.fill();
      var gr=a*180/Math.PI;txt(g,'ângulo: '+Math.round(gr)+'°',330,60,OURO,16);
      txt(g,'cos = '+Math.cos(a).toFixed(2)+'  (x)',330,95,VERM,16);txt(g,'sin = '+Math.sin(a).toFixed(2)+'  (y)',330,125,VERDE,16);
      txt(g,'x = cx + cos(a) · raio',330,170,ink,15);txt(g,'y = cy + sin(a) · raio',330,195,ink,15)})},
    curvas:function(c,st){var fs=[function(t){return t},function(t){return t*t},function(t){return 1-(1-t)*(1-t)},function(t){return t*t*(3-2*t)}],nomes=['linear','acelera','freia','suave'],cs=['#7A8AA0',VERM,VERDE,OURO];
      laco(c,st,function(g,t,W,H){var ink=cor('--ink','#0F1B2D'),lin=cor('--line','#D6DDE7'),u=(t%2.4)/2,tt=Math.min(1,u);
        for(var i=0;i<4;i++){var y=40+i*55;g.strokeStyle=lin;g.lineWidth=3;g.beginPath();g.moveTo(30,y);g.lineTo(330,y);g.stroke();g.fillStyle=cs[i];g.beginPath();g.arc(30+300*fs[i](tt),y,11,0,7);g.fill();txt(g,nomes[i],30,y+26,cs[i],13)}
        var gx=390,gy=30,gw=220,gh=200;g.strokeStyle=lin;g.lineWidth=1;g.strokeRect(gx,gy,gw,gh);
        for(var k=0;k<4;k++){g.strokeStyle=cs[k];g.lineWidth=2.5;g.beginPath();for(var s=0;s<=40;s++){var x=s/40,X=gx+gw*x,Y=gy+gh-gh*fs[k](x);if(s)g.lineTo(X,Y);else g.moveTo(X,Y)}g.stroke()}
        g.strokeStyle=ink;g.lineWidth=1;g.beginPath();g.moveTo(gx+gw*tt,gy);g.lineTo(gx+gw*tt,gy+gh);g.stroke();txt(g,'t = '+tt.toFixed(2),gx,gy+gh+20,ink,13);txt(g,'tempo →',gx+gw,gy+gh+20,ink,12,'right')})},
    seguidor:function(c,st){var p={x:100,y:130},q={x:100,y:130};laco(c,st,function(g,t,W,H){var ink=cor('--ink','#0F1B2D'),lin=cor('--line','#D6DDE7');
      var alvo={x:W/2+220*Math.cos(t*0.9),y:H/2+80*Math.sin(t*1.7)};var dt=1/60;
      var f1=1-Math.pow(0.02,dt),f2=1-Math.pow(0.3,dt);p.x+=(alvo.x-p.x)*f1;p.y+=(alvo.y-p.y)*f1;q.x+=(alvo.x-q.x)*f2;q.y+=(alvo.y-q.y)*f2;
      g.fillStyle=lin;g.beginPath();g.arc(alvo.x,alvo.y,7,0,7);g.fill();
      g.fillStyle=CAR;g.beginPath();g.arc(p.x,p.y,13,0,7);g.fill();g.fillStyle='#7A8AA0';g.beginPath();g.arc(q.x,q.y,13,0,7);g.fill();
      txt(g,'alvo',alvo.x+10,alvo.y-8,ink,12);txt(g,'laranja: lerp com 0.02 (rápido)   cinza: 0.3 (preguiçoso)',16,H-14,ink,13)})},
    ciclo:function(c,st){laco(c,st,function(g,t,W,H){var ink=cor('--ink','#0F1B2D'),pn=cor('--panel','#fff'),lin=cor('--line','#D6DDE7');
      var cx=W/2,cy=H/2+6,R=92,nos=[['Objetivo','pegar o osso',-Math.PI/2,CAR],['Desafio','antes de sumir',Math.PI/6,VERM],['Recompensa','pontos e combo',5*Math.PI/6,VERDE]];
      g.strokeStyle=lin;g.lineWidth=3;g.beginPath();g.arc(cx,cy,R,0,7);g.stroke();
      var a=t*1.3-Math.PI/2;g.fillStyle=OURO;g.beginPath();g.arc(cx+R*Math.cos(a),cy+R*Math.sin(a),8,0,7);g.fill();
      nos.forEach(function(n){var x=cx+R*Math.cos(n[2]),y=cy+R*Math.sin(n[2]);g.fillStyle=pn;g.strokeStyle=n[3];g.lineWidth=3;g.beginPath();g.roundRect?g.roundRect(x-70,y-24,140,48,12):g.rect(x-70,y-24,140,48);g.fill();g.stroke();
        txt(g,n[0],x,y-3,n[3],16,'center');txt(g,n[1],x,y+16,ink,12,'center')})})},
    fluxo:function(c,st){laco(c,st,function(g,t,W,H){var ink=cor('--ink','#0F1B2D'),lin=cor('--line','#D6DDE7'),x0=60,y0=H-40,w=W-100,h=H-70;
      g.fillStyle='rgba(43,163,107,.16)';g.beginPath();g.moveTo(x0,y0-20);g.lineTo(x0+w,y0-h);g.lineTo(x0+w,y0-h+70);g.lineTo(x0+70,y0);g.lineTo(x0,y0);g.closePath();g.fill();
      g.strokeStyle=ink;g.lineWidth=1.5;g.beginPath();g.moveTo(x0,y0-h);g.lineTo(x0,y0);g.lineTo(x0+w,y0);g.stroke();
      txt(g,'habilidade do jogador →',x0+w,y0+24,ink,13,'right');g.save();g.translate(x0-24,y0-h/2);g.rotate(-Math.PI/2);txt(g,'desafio →',0,0,ink,13,'center');g.restore();
      txt(g,'ansiedade',x0+40,y0-h+30,VERM,14);txt(g,'tédio',x0+w-60,y0-30,'#7A8AA0',14);txt(g,'fluxo',x0+w*0.55,y0-h*0.5+8,VERDE,15);
      var u=(t%8)/8;g.strokeStyle=OURO;g.lineWidth=2;g.beginPath();for(var s=0;s<=60;s++){var v=s/60,X=x0+20+v*(w-40),Y=y0-30-v*(h-60)+16*Math.sin(v*18);if(s)g.lineTo(X,Y);else g.moveTo(X,Y)}g.stroke();
      var X1=x0+20+u*(w-40),Y1=y0-30-u*(h-60)+16*Math.sin(u*18);g.fillStyle=CAR;g.beginPath();g.arc(X1,Y1,8,0,7);g.fill()})},
    suco:function(c,st){var ev=[];laco(c,st,function(g,t,W,H){var ink=cor('--ink','#0F1B2D'),fase=t%1.6,bate=fase<0.02;
      [[W*0.27,false],[W*0.73,true]].forEach(function(s){var x=s[0],j=s[1],e=Math.max(0,1-fase*3),sh=j?e*8*Math.sin(t*90):0,sq=j?e:0;
        g.save();g.translate(sh,0);g.fillStyle=cor('--line','#D6DDE7');g.fillRect(x-120,H-50,240,6);
        var w=70*(1+0.35*sq),h=70*(1-0.3*sq);g.fillStyle=j?'rgb('+Math.round(214+41*e*0.8)+','+Math.round(140+115*e*0.8)+','+Math.round(62+193*e*0.8)+')':CAR;g.fillRect(x-w/2,H-50-h,w,h);
        if(j)for(var k=0;k<10;k++){var a=k/10*Math.PI*2,d=fase*160;if(fase<0.5){g.fillStyle=OURO;g.beginPath();g.arc(x+Math.cos(a)*d,H-85+Math.sin(a)*d*0.7+fase*fase*300,3.5*(1-fase*2),0,7);g.fill()}}
        g.restore();txt(g,j?'com suco':'sem suco',x,30,ink,15,'center')})})},
    pixel:function(c,st){var A=['................','................','..........DD....','..D.......DCCC..','..D......CCkCC..','..D......CCCCLLk','...D.....CCCLLL.','...DC...CCCC.t..','....CCCCCCCC....','...CCCCCCCCCC...','...CCCCCCCCCC...','...CLLLLLLLLC...','...C.C....C.C...','...C.C....C.C...','...D.D....D.D...','................'],
      P=[{C:'#D68C3E',D:'#A0602A',L:'#F6CE96',k:'#222034',t:'#EC6878'},{C:'#2B2B33',D:'#15151A',L:'#D9D4C7',k:'#FFFFFF',t:'#EC6878'},{C:'#F2EEE6',D:'#6B4A2E',L:'#C9A27A',k:'#222034',t:'#EC6878'}];
      laco(c,st,function(g,t,W,H){var pal=P[Math.floor(t/2.5)%3],z=Math.min(13,1+Math.floor((t%2.5)*12)),lin=cor('--line','#D6DDE7'),ink=cor('--ink','#0F1B2D'),ox=40,oy=20;
        for(var y=0;y<16;y++)for(var x=0;x<16;x++){var ch=A[y][x];if(pal[ch]){g.fillStyle=pal[ch];g.fillRect(ox+x*z,oy+y*z,z,z)}if(z>6){g.strokeStyle=lin;g.lineWidth=.5;g.strokeRect(ox+x*z,oy+y*z,z,z)}}
        g.imageSmoothingEnabled=false;for(var y2=0;y2<16;y2++)for(var x2=0;x2<16;x2++){var c2=A[y2][x2];if(pal[c2]){g.fillStyle=pal[c2];g.fillRect(320+x2*2,40+y2*2,2,2)}}
        txt(g,'tamanho real (16 × 16)',320,90,ink,13);txt(g,'ampliado '+z+'×',320,120,ink,13);
        var cs=Object.keys(pal);cs.forEach(function(k,i){g.fillStyle=pal[k];g.fillRect(320+i*34,150,28,28);g.strokeStyle=lin;g.strokeRect(320+i*34,150,28,28)});txt(g,'paleta: 5 cores',320,200,ink,13)})},
    squash:function(c,st){laco(c,st,function(g,t,W,H){var ink=cor('--ink','#0F1B2D'),lin=cor('--line','#D6DDE7'),u=(t%1.2)/1.2,alt=4*u*(1-u),chao=Math.max(0,1-Math.min(u,1-u)/0.08),rap=Math.abs(1-2*u);
      g.fillStyle=lin;g.fillRect(0,H-30,W,4);
      [[W*0.3,0],[W*0.7,0.7]].forEach(function(s){var ex=s[1],est=1+ex*0.35*rap*(1-chao),esm=1-ex*0.45*chao,sw=1/(est*esm),sh=est*esm,r=26,w=r*2*sw,h=r*2*sh;
        g.fillStyle=ex?CAR:'#7A8AA0';g.beginPath();g.ellipse(s[0],H-30-h/2-alt*150,w/2,h/2,0,0,7);g.fill();txt(g,ex?'esmaga e estica':'bola rígida',s[0],H-8,ink,14,'center')})})},
    adsr:function(c,st){laco(c,st,function(g,t,W,H){var ink=cor('--ink','#0F1B2D'),lin=cor('--line','#D6DDE7'),A=0.08,D=0.25,S=0.55,Sd=0.6,R=0.5,T=A+D+Sd+R,x0=40,y0=H-40,w=W-80,h=H-80;
      function X(s){return x0+w*s/T}function Y(v){return y0-h*v}
      g.strokeStyle=lin;g.lineWidth=1;g.beginPath();g.moveTo(x0,Y(1));g.lineTo(x0,y0);g.lineTo(x0+w,y0);g.stroke();
      g.strokeStyle=OURO;g.lineWidth=3;g.beginPath();g.moveTo(X(0),Y(0));g.lineTo(X(A),Y(1));g.lineTo(X(A+D),Y(S));g.lineTo(X(A+D+Sd),Y(S));g.lineTo(X(T),Y(0));g.stroke();
      [['ataque',A/2],['decaimento',A+D/2],['sustentação',A+D+Sd/2],['soltura',A+D+Sd+R/2]].forEach(function(l){txt(g,l[0],X(l[1]),y0+20,ink,12,'center')});
      var p=(t%(T+0.6));if(p<=T){var v=p<A?p/A:p<A+D?1-(1-S)*(p-A)/D:p<A+D+Sd?S:S*(1-(p-A-D-Sd)/R);g.strokeStyle=ink;g.beginPath();g.moveTo(X(p),Y(0));g.lineTo(X(p),Y(1));g.stroke();
        g.fillStyle=CAR;g.fillRect(W-30,Y(v),14,y0-Y(v));txt(g,'volume',W-23,Y(1)-8,ink,11,'center')}})},
    passo:function(c,st){laco(c,st,function(g,t,W,H){var ink=cor('--ink','#0F1B2D'),lin=cor('--line','#D6DDE7'),wx=W*0.55,u=(t%2.4)/2.4;
      g.fillStyle=ink;g.fillRect(wx,30,8,H-70);txt(g,'parede fina',wx+4,22,ink,12,'center');
      [[40,'60 quadros por segundo: muitos passos curtos',1/60,VERDE],[H/2+20,'8 quadros por segundo: poucos passos longos',1/8,VERM]].forEach(function(l){var y=l[0],dt=l[2],v=900,x0=30,bateu=false,pts=[];
        for(var s=0;s<=u*1.2+1e-9;s+=dt){var x=x0+v*s;if(!bateu&&x>=wx&&x<=wx+8){bateu=true}if(bateu&&dt<0.05){x=Math.min(x,wx-2)}pts.push(x)}
        pts.forEach(function(x,i){g.fillStyle=l[3];g.globalAlpha=0.35+0.65*(i+1)/pts.length;g.beginPath();g.arc(Math.min(x,W-10),y+40,7,0,7);g.fill()});g.globalAlpha=1;
        txt(g,l[1],30,y+20,ink,13)})})},
    colisao:function(c,st){laco(c,st,function(g,t,W,H){var ink=cor('--ink','#0F1B2D'),lin=cor('--line','#D6DDE7');
      var ax=110+60*Math.cos(t*0.9),ay=H/2,bx=200,by=H/2,r=45,hit=Math.hypot(ax-bx,ay-by)<2*r;
      g.fillStyle=hit?VERM:'#7A8AA0';g.globalAlpha=0.7;g.beginPath();g.arc(bx,by,r,0,7);g.fill();g.fillStyle=CAR;g.beginPath();g.arc(ax,ay,r,0,7);g.fill();g.globalAlpha=1;
      g.strokeStyle=ink;g.lineWidth=2;g.beginPath();g.moveTo(ax,ay);g.lineTo(bx,by);g.stroke();
      txt(g,'distância '+Math.round(Math.hypot(ax-bx,ay-by))+(hit?' < ':' ≥ ')+'soma dos raios '+2*r,155,H-24,hit?VERM:ink,13,'center');
      var rx=430+70*Math.cos(t*0.8),ry=H/2-40,rw=90,rh=70,sx=470,sy=H/2-20,sw=110,sh=80,h2=rx<sx+sw&&rx+rw>sx&&ry<sy+sh&&ry+rh>sy;
      g.globalAlpha=0.7;g.fillStyle=h2?VERM:'#7A8AA0';g.fillRect(sx,sy,sw,sh);g.fillStyle=CAR;g.fillRect(rx,ry,rw,rh);g.globalAlpha=1;
      txt(g,h2?'as faixas em x E em y se cruzam':'separados em x ou em y',500,H-24,h2?VERM:ink,13,'center')})},
    sorteio:function(c,st){var itens=[['Osso',60,'#E9D8A6'],['Bola',25,'#64B5F6'],['Coleira',12,'#BA68C8'],['Dourado',3,'#FFC107']];
      laco(c,st,function(g,t,W,H){var ink=cor('--ink','#0F1B2D'),x0=40,w=W-80,y=70,h=46,acc=0;
        itens.forEach(function(it){var ww=w*it[1]/100;g.fillStyle=it[2];g.fillRect(x0+acc,y,ww,h);txt(g,it[0]+' '+it[1],x0+acc+ww/2,y+h+20+(it[1]<10?18:0),ink,12,'center');acc+=ww});
        var n=(Math.floor(t*1.3)*37+11)%100,px=x0+w*(n+0.5)/100,fase=(t*1.3)%1;
        seta(g,px,y-40,px,y-4,ink,3);txt(g,'sorteou '+n,px,y-46,ink,13,'center');
        var ac=0,sai='';itens.forEach(function(it){if(!sai&&n<ac+it[1])sai=it[0];ac+=it[1]});
        txt(g,'0 a 99 caiu na faixa: '+sai,W/2,H-30,ink,16,'center')})},
    ritmo:function(c,st){var tr=[0.2,0.45,0.8,0.1,0.25,0.5,0.85,0.9,0.15,1];
      laco(c,st,function(g,t,W,H){var ink=cor('--ink','#0F1B2D'),lin=cor('--line','#D6DDE7'),x0=30,w=(W-60)/tr.length,base=H-40,alt=H-80,k=(t*1.2)%tr.length;
        tr.forEach(function(v,i){g.fillStyle=v>=0.8?'#FF8A65':(v<=0.2?'#B0BEC5':'#81C784');g.fillRect(x0+i*w+3,base-v*alt,w-6,v*alt)});
        g.strokeStyle=ink;g.lineWidth=2;g.beginPath();tr.forEach(function(v,i){var x=x0+i*w+w/2,y=base-v*alt;if(i)g.lineTo(x,y);else g.moveTo(x,y)});g.stroke();
        var i=Math.floor(k),f=k-i,v=tr[i]+(tr[Math.min(i+1,tr.length-1)]-tr[i])*f;g.fillStyle=CAR;g.beginPath();g.arc(x0+(i+f)*w+w/2,base-v*alt,8,0,7);g.fill();
        txt(g,'tensão',x0,22,ink,13);txt(g,'tempo de jogo →',W-30,H-12,ink,12,'right')})},
    hud:function(c,st){laco(c,st,function(g,t,W,H){var ink=cor('--ink','#0F1B2D'),px=W/2-150,py=20,pw=300,ph=H-40;
      g.fillStyle='#8FD3F4';g.fillRect(px,py,pw,ph);g.strokeStyle=ink;g.lineWidth=2;g.strokeRect(px,py,pw,ph);
      var a=0.25+0.15*Math.sin(t*2);g.fillStyle='rgba(43,163,107,'+a+')';g.beginPath();g.arc(px+30,py+ph,110,-Math.PI/2,0);g.lineTo(px+30,py+ph);g.fill();g.beginPath();g.arc(px+pw-30,py+ph,110,Math.PI,Math.PI*1.5);g.lineTo(px+pw-30,py+ph);g.fill();
      txt(g,'polegar',px+40,py+ph-118,ink,12);txt(g,'polegar',px+pw-40,py+ph-118,ink,12,'right');
      g.fillStyle='rgba(229,72,77,0.18)';g.fillRect(px,py,pw,44);txt(g,'♥♥♡  Ossos: 12   (informação no alto)',px+10,py+28,ink,13);
      [[px+40,py+ph-40],[px+100,py+ph-40],[px+pw-50,py+ph-50]].forEach(function(b){g.fillStyle='rgba(0,0,0,0.35)';g.beginPath();g.arc(b[0],b[1],24,0,7);g.fill()});
      txt(g,'botões ao',W-12,H/2-8,ink,13,'right');txt(g,'alcance',W-12,H/2+10,ink,13,'right');txt(g,'≥ 48 de',12,H/2-8,ink,13);txt(g,'toque',12,H/2+10,ink,13)})},
    economia:function(c,st){laco(c,st,function(g,t,W,H){var ink=cor('--ink','#0F1B2D'),lin=cor('--line','#D6DDE7'),x0=50,y0=H-40,w=W-90,h=H-70,n=15,k=(t*3)%n;
      g.strokeStyle=lin;g.lineWidth=1;g.beginPath();g.moveTo(x0,y0-h);g.lineTo(x0,y0);g.lineTo(x0+w,y0);g.stroke();
      function X(i){return x0+w*i/(n-1)}var mx=10*Math.pow(1.5,n-1);function Y(v){return y0-h*v/mx}
      g.strokeStyle=VERM;g.lineWidth=3;g.beginPath();for(var i=0;i<n;i++){var v=10*Math.pow(1.5,i);if(i)g.lineTo(X(i),Y(v));else g.moveTo(X(i),Y(v))}g.stroke();
      g.strokeStyle=VERDE;g.beginPath();for(i=0;i<n;i++){var v2=(5+3*i)*60;if(i)g.lineTo(X(i),Y(v2));else g.moveTo(X(i),Y(v2))}g.stroke();
      var ii=Math.floor(k);g.fillStyle=ink;g.beginPath();g.arc(X(ii),Y(10*Math.pow(1.5,ii)),5,0,7);g.fill();
      txt(g,'custo do nível (cresce ×1,5)',x0+10,30,VERM,13);txt(g,'ganho em 1 hora (cresce +3/min)',x0+10,50,VERDE,13);txt(g,'nível →',W-20,H-14,ink,12,'right')})},
    camadas:function(c,st){laco(c,st,function(g,t,W,H){var ink=cor('--ink','#0F1B2D'),lin=cor('--line','#D6DDE7'),bx=[[40,'Modelo','dados e regras',CAR],[W-240,'Visual','widgets e componentes','#64B5F6']];
      bx.forEach(function(b){g.fillStyle=b[3];g.globalAlpha=0.25;g.fillRect(b[0],60,200,H-120);g.globalAlpha=1;g.strokeStyle=b[3];g.lineWidth=2;g.strokeRect(b[0],60,200,H-120);txt(g,b[1],b[0]+100,95,ink,18,'center');txt(g,b[2],b[0]+100,118,ink,12,'center')});
      var u=(t*0.6)%2,ida=u<1,f=ida?u:u-1,y=ida?H/2-10:H/2+40,x=ida?(W-240)-(W-240-240)*f:240+(W-240-240)*f;
      seta(g,W-240,H/2-10,240,H/2-10,ink,2);txt(g,'comando: pegarOsso()',W/2,H/2-20,ink,13,'center');
      seta(g,240,H/2+40,W-240,H/2+40,ink,2);txt(g,'aviso: notifyListeners()',W/2,H/2+30,ink,13,'center');
      g.fillStyle=ida?VERM:VERDE;g.beginPath();g.arc(x,y,7,0,7);g.fill()})},
    calor:function(c,st){var G=[];var s=7;function r(){s=(s*9301+49297)%233280;return s/233280}for(var y=0;y<9;y++){G.push([]);for(var x=0;x<20;x++)G[y].push(Math.max(0,1-Math.hypot(x-13,y-4)/6)+(y===4?0.4:0)+r()*0.15)}
      laco(c,st,function(g,t,W,H){var ink=cor('--ink','#0F1B2D'),s2=24,ox=(W-20*s2)/2,oy=12,a=0.5+0.5*Math.sin(t*1.5);
        for(var y=0;y<9;y++)for(var x=0;x<20;x++){var v=Math.min(1,G[y][x]);g.fillStyle='rgba(229,72,77,'+(v*(0.4+0.6*a)).toFixed(3)+')';g.fillRect(ox+x*s2,oy+y*s2,s2-2,s2-2)}
        g.strokeStyle=ink;g.lineWidth=2;g.strokeRect(ox+10*s2,oy+1*s2,6*s2,7*s2);txt(g,'aqui morre muita gente: o trecho está difícil demais?',W/2,H-14,ink,13,'center')})},
    loja:function(c,st){var et=['código','teste no celular','ícone e versão','build assinado','loja'];
      laco(c,st,function(g,t,W,H){var ink=cor('--ink','#0F1B2D'),n=et.length,w=(W-40)/n,k=(t*0.7)%(n+1);
        et.forEach(function(e,i){var x=20+i*w,on=i<k;g.fillStyle=on?VERDE:'#B0BEC5';g.globalAlpha=on?0.9:0.5;g.fillRect(x+6,H/2-30,w-24,60);g.globalAlpha=1;txt(g,e,x+w/2-9,H/2+5,on?'#fff':ink,12,'center');if(i<n-1)seta(g,x+w-16,H/2,x+w+4,H/2,ink,2)});
        txt(g,'cada passo só começa quando o anterior está pronto',W/2,H-24,ink,13,'center')})},
    narrativa:function(c,st){var N=[['Muro',0,0.5],['Gentil',1,0.28],['Bravo',1,0.72],['Segredo',2,0.2],['Sozinho',2,0.45],['Desculpa',2,0.7],['Fuga',2,0.92],['Amigos',3,0.2]],E=[[0,1],[0,2],[1,3],[1,4],[2,5],[2,6],[5,3],[3,7]];
      laco(c,st,function(g,t,W,H){var ink=cor('--ink','#0F1B2D');function P(i){return[60+N[i][1]*(W-120)/3,20+N[i][2]*(H-40)]}
        var cam=[[0,1,3,7],[0,2,5,3,7],[0,1,4],[0,2,6]][Math.floor(t/2.5)%4],k=Math.min(cam.length-1,Math.floor((t%2.5)/2.5*cam.length*1.3));
        E.forEach(function(e){var a=P(e[0]),b=P(e[1]),on=false;for(var i=0;i<k;i++)if(cam[i]===e[0]&&cam[i+1]===e[1])on=true;g.strokeStyle=on?OURO:'rgba(120,130,150,0.6)';g.lineWidth=on?4:2;g.beginPath();g.moveTo(a[0],a[1]);g.lineTo(b[0],b[1]);g.stroke()});
        N.forEach(function(n,i){var p=P(i),fim=[4,6,7].indexOf(i)>=0,on=cam.slice(0,k+1).indexOf(i)>=0;g.fillStyle=on?OURO:(fim?'#FF8A65':'#81C784');g.fillRect(p[0]-42,p[1]-14,84,28);txt(g,n[0],p[0],p[1]+5,'#0F1B2D',13,'center')})})},
    mda:function(c,st){var B=[['Mecânicas','regras e código'],['Dinâmicas','o que acontece ao jogar'],['Estéticas','o que o jogador sente']];
      laco(c,st,function(g,t,W,H){var ink=cor('--ink','#0F1B2D'),bw=(W-80)/3,y=H/2-36;
        B.forEach(function(b,i){var x=20+i*(bw+20);g.fillStyle=['#81C784','#FFD54F','#FF8A65'][i];g.fillRect(x,y,bw,72);txt(g,b[0],x+bw/2,y+30,'#0F1B2D',17,'center');txt(g,b[1],x+bw/2,y+54,'#0F1B2D',12,'center')});
        var k=(t*0.45)%2,ida=k<1,f=ida?k:k-1,x0=ida?20+bw/2:W-20-bw/2,x1=ida?W-20-bw/2:20+bw/2,xp=x0+(x1-x0)*f,yy=ida?y-22:y+96;
        seta(g,20+bw/2,y-22,W-20-bw/2,y-22,ida?CAR:'rgba(120,130,150,0.5)',3);seta(g,W-20-bw/2,y+96,20+bw/2,y+96,ida?'rgba(120,130,150,0.5)':CAR,3);
        txt(g,'quem faz o jogo começa pelas regras',W/2,y-32,ink,12,'center');txt(g,'quem joga começa pelo que sente',W/2,y+116,ink,12,'center');
        g.fillStyle=ink;g.beginPath();g.arc(xp,yy,7,0,7);g.fill()})},
    bau:function(c,st){laco(c,st,function(g,t,W,H){var ink=cor('--ink','#0F1B2D'),lin=cor('--line','#D6DDE7'),x0=50,y0=H-30,w=W-70,h=H-60,N=60,p=0.05;
        g.strokeStyle=lin;g.lineWidth=1;[0.5,0.9].forEach(function(q){var yq=y0-q*h;g.beginPath();g.moveTo(x0,yq);g.lineTo(x0+w,yq);g.stroke();txt(g,Math.round(q*100)+'%',x0-8,yq+4,ink,11,'right')});
        g.strokeStyle=ink;g.beginPath();g.moveTo(x0,y0-h);g.lineTo(x0,y0);g.lineTo(x0+w,y0);g.stroke();txt(g,'baús abertos',x0+w,y0+20,ink,11,'right');
        g.strokeStyle=CAR;g.lineWidth=3;g.beginPath();for(var n=0;n<=N;n++){var yy=y0-(1-Math.pow(1-p,n))*h,xx=x0+n/N*w;if(n===0)g.moveTo(xx,yy);else g.lineTo(xx,yy)}g.stroke();
        var m=Math.floor((t*8)%(N+1)),pr=1-Math.pow(1-p,m),xm=x0+m/N*w,ym=y0-pr*h;g.fillStyle=OURO;g.beginPath();g.arc(xm,ym,7,0,7);g.fill();
        txt(g,m+' baús: '+Math.round(pr*100)+'% de chance de já ter a coleira (5% cada)',x0+10,y0-h+4,ink,13,'left')})},
    jam:function(c,st){var F=[['Ideia',2],['Protótipo',10],['Conteúdo',16],['Polimento',12],['Entrega',4],['Dormir!',4]];
      laco(c,st,function(g,t,W,H){var ink=cor('--ink','#0F1B2D'),x0=20,w=W-40,tot=48,hora=(t*4)%(tot+6),x=x0;
        F.forEach(function(f,i){var fw=f[1]/tot*w;g.fillStyle=['#90CAF9','#81C784','#FFD54F','#FF8A65','#BA68C8','#B0BEC5'][i];g.globalAlpha=hora>=(x-x0)/w*tot?0.95:0.35;g.fillRect(x,H/2-26,fw-3,52);g.globalAlpha=1;
          g.save();g.translate(x+fw/2,H/2+44);txt(g,f[0],0,0,ink,12,'center');g.restore();x+=fw});
        for(var hh=0;hh<=48;hh+=12)txt(g,hh+'h',x0+hh/tot*w,H/2-36,ink,11,'center');
        var xc=x0+Math.min(tot,hora)/tot*w;g.strokeStyle=VERM;g.lineWidth=2;g.beginPath();g.moveTo(xc,H/2-30);g.lineTo(xc,H/2+30);g.stroke()})},
    motor:function(c,st){laco(c,st,function(g,t,W,H){var ink=cor('--ink','#0F1B2D'),w=(W-60)/2,x1=20,x2=40+w,y=36,h=H-70,k=(t*1.2)%3;
        [[x1,'Flutter puro','#90CAF9',['toque / Timer','setState','build','widgets na tela']],[x2,'Flame','#FFCC80',['laço do jogo (sempre)','update(dt)','render(canvas)','componentes']]].forEach(function(col,ci){
          g.fillStyle=col[2];g.globalAlpha=0.35;g.fillRect(col[0],y-8,w,h);g.globalAlpha=1;txt(g,col[1],col[0]+w/2,y+12,ink,16,'center');
          col[3].forEach(function(e,i){var yy=y+40+i*((h-60)/4),on=ci===1?Math.floor((t*3)%4)===i:(k<1.6&&Math.floor(k/0.4)===i);g.fillStyle=on?CAR:'rgba(255,255,255,0.85)';g.fillRect(col[0]+14,yy,w-28,26);txt(g,e,col[0]+w/2,yy+18,on?'#fff':'#0F1B2D',13,'center');
            if(i<3)txt(g,'▼',col[0]+w/2,yy+26+((h-60)/4-26)/2+5,ink,11,'center')})});
        txt(g,'redesenha só quando algo muda',x1+w/2,H-14,ink,12,'center');txt(g,'redesenha todo quadro, ~60 vezes por segundo',x2+w/2,H-14,ink,12,'center')})},
    pilha:function(c,st){var seq=[3,2,1,0,1,2,3];laco(c,st,function(g,t,W,H){var ink=cor('--ink','#0F1B2D'),k=Math.floor(t*0.9)%(seq.length+1),n=k<seq.length?seq[k]:0,topo=3-n,volta=k>3;
        txt(g,'contar(3): cada chamada espera a de cima terminar',W/2,22,ink,14,'center');
        for(var i=0;i<=topo&&k<seq.length;i++){var y=H-30-i*42;g.fillStyle=i===topo?(volta?VERDE:CAR):'#B0BEC5';g.fillRect(W/2-120,y-30,240,36);
          txt(g,'contar('+(3-i)+')'+(i===topo?(volta||3-i===0?'  → devolve':'  → chama contar('+(2-i)+')'):'  esperando…'),W/2,y-7,'#0F1B2D',14,'center')}
        if(k>=seq.length)txt(g,'pilha vazia: resultado pronto',W/2,H/2,VERDE,16,'center');
        txt(g,'caso base: contar(0) não chama ninguém',W/2,H-6,ink,12,'center')})},
    projeto:function(c,st){var et=['Documento','Protótipo','Uma fase','Arte e som','Teste','Entrega'];
      laco(c,st,function(g,t,W,H){var ink=cor('--ink','#0F1B2D'),lin=cor('--line','#D6DDE7'),x0=110,w=(W-130)/6,sem=(t*0.8)%7;
        for(var s=0;s<6;s++){txt(g,'sem '+(s+1),x0+s*w+w/2,18,ink,11,'center');g.strokeStyle=lin;g.beginPath();g.moveTo(x0+s*w,24);g.lineTo(x0+s*w,H-10);g.stroke()}
        et.forEach(function(e,i){var y=34+i*((H-44)/6),h=(H-44)/6-8,feito=sem>i+1;txt(g,e,x0-8,y+h/2+5,ink,13,'right');g.fillStyle=feito?VERDE:(sem>i?OURO:'#B0BEC5');g.globalAlpha=feito||sem>i?0.9:0.45;g.fillRect(x0+i*w+3,y,w-6,h);g.globalAlpha=1;if(feito)txt(g,'✓',x0+i*w+w/2,y+h/2+5,'#fff',14,'center')});
        g.strokeStyle=VERM;g.lineWidth=2;var xs=x0+Math.min(6,sem)*w;g.beginPath();g.moveTo(xs,24);g.lineTo(xs,H-10);g.stroke()})}
  };
})();
</script>
"""


def patch(src):
    src = sub1(src, "var goalsDone=false,hintOpen=null;", ENGINE + "var goalsDone=false,hintOpen=null;", 'leitura engine')
    src = sub1(src,
        "+(L.lim?'<p class=\"lim\"><b>Limites do simulador:</b> '+esc(L.lim)+'</p>':'')+'<div id=\"goalBox\" class=\"goals\"></div>';",
        "+(L.lim?'<p class=\"lim\"><b>Limites do simulador:</b> '+esc(L.lim)+'</p>':'')+(L.leitura?'<button class=\"btn pri lebtn\" id=\"leBtn\">📖 Ler a aula ('+L.leitura.filter(function(b){return b.p}).length+' parágrafos, '+(L.quiz?L.quiz.length:0)+' perguntas)</button>':'')+'<div id=\"goalBox\" class=\"goals\"></div>';if(L.leitura)leAuto(L);",
        'leitura botao')
    src = sub1(src, "(L.proj?'🛠 ':'')", "(L.leitura?'📖 ':'')+(L.proj?'🛠 ':'')", 'leitura menu')
    return src


def finish(src):
    return src + HTML + FIGS
