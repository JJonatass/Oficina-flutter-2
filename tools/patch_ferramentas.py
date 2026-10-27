# Oficina Flutter 2 · ferramentas de criação: editor de pixel art, editor de mapas do Tiled,
# compartilhar jogo por link, galeria da turma e planilha da turma no painel do professor.
from patch_engine import sub1

CSS = r"""<style>
.fx-grid{display:grid;grid-template-columns:minmax(0,1fr) 220px;gap:14px}
@media (max-width:760px){.fx-grid{grid-template-columns:minmax(0,1fr)}}
.fx-tools{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0}
.fx-tools .btn{font-size:13px;padding:4px 9px}
.fx-tools .btn.on{outline:2px solid var(--acc,#2f6fed);outline-offset:1px}
.fx-pal{display:grid;grid-template-columns:repeat(8,1fr);gap:4px;margin:6px 0}
.fx-pal button{aspect-ratio:1;border:1px solid var(--line);border-radius:5px;cursor:pointer;padding:0;min-width:0;background-clip:padding-box}
.fx-pal button.on{outline:3px solid var(--ink);outline-offset:1px}
.fx-pal button.vazio{background:repeating-conic-gradient(#ccc 0 25%,#fff 0 50%) 0 0/8px 8px}
.fx-wrap{overflow:auto;max-width:100%;border:1px solid var(--line);border-radius:8px;background:repeating-conic-gradient(var(--panel) 0 25%,var(--panel2) 0 50%) 0 0/16px 16px}
.fx-wrap canvas{display:block;touch-action:none;image-rendering:pixelated;cursor:crosshair}
.fx-frames{display:flex;gap:6px;flex-wrap:wrap;margin:6px 0}
.fx-frames canvas{width:48px;height:48px;image-rendering:pixelated;border:2px solid var(--line);border-radius:6px;cursor:pointer;background:repeating-conic-gradient(#ddd 0 25%,#fff 0 50%) 0 0/8px 8px}
.fx-frames canvas.on{border-color:var(--ink)}
.fx-prev{width:128px;height:128px;image-rendering:pixelated;border:1px solid var(--line);border-radius:8px;background:repeating-conic-gradient(#ddd 0 25%,#fff 0 50%) 0 0/16px 16px}
.fx-code{font:12px/1.4 var(--f-mono);white-space:pre-wrap;word-break:break-all;background:var(--panel2);border:1px solid var(--line);border-radius:8px;padding:8px;margin:6px 0}
.fx-tiles{display:grid;grid-template-columns:repeat(6,1fr);gap:4px}
.fx-tiles button{aspect-ratio:1;padding:0;border:1px solid var(--line);border-radius:5px;cursor:pointer;background:var(--panel2);min-width:0}
.fx-tiles button.on{outline:3px solid var(--ink);outline-offset:1px}
.fx-tiles canvas{width:100%;height:100%;image-rendering:pixelated;display:block}
.fx-lbl{font-size:12px;color:var(--ink2);margin-top:8px}
.fx-row{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin:6px 0}
.fx-row input[type=number]{width:64px}
.fx-row input[type=text],.fx-row input:not([type]){min-width:0;flex:1}
.gal-list{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:10px;margin-top:10px}
.gal-c{border:1px solid var(--line);border-radius:10px;padding:10px;background:var(--panel2);display:flex;flex-direction:column;gap:6px;min-width:0}
.gal-c.novo{outline:2px solid var(--acc,#2f6fed)}
.gal-c b{font-size:15px}.gal-c small{color:var(--ink2)}
.gal-st{display:flex;gap:2px}.gal-st button{border:0;background:none;font-size:22px;cursor:pointer;padding:0 2px;color:#E0A100;line-height:1}
.gal-c .fx-tools .btn{font-size:12px}
.fx-link{width:100%;font:12px var(--f-mono);min-height:70px}
</style>
"""

HTML = r"""
<div class="modal" id="pxModal" hidden role="dialog" aria-modal="true" aria-label="Editor de pixel art"><div class="mbox">
  <div class="mh"><b>🎨 Editor de pixel art</b><button class="btn" id="pxClose" aria-label="Fechar">✕</button></div>
  <div class="mb">
   <div class="fx-row">
    <label>Tamanho <select id="pxTam"><option>8</option><option selected>16</option><option>24</option><option>32</option></select></label>
    <label>Abrir <select id="pxAbrir"><option value="">um sprite pronto ou seu…</option></select></label>
    <button class="btn" id="pxNovo">Novo</button>
   </div>
   <div class="fx-grid">
    <div style="min-width:0">
     <div class="fx-tools" id="pxTools">
      <button class="btn on" data-t="lapis">✏️ Lápis</button><button class="btn" data-t="borracha">🧽 Borracha</button><button class="btn" data-t="balde">🪣 Balde</button><button class="btn" data-t="gotas">💧 Pegar cor</button>
      <button class="btn" id="pxEsp">↔ Espelhar</button><button class="btn" id="pxLimpa">🗑 Limpar quadro</button><button class="btn" id="pxDesf">↶ Desfazer</button>
      <label class="fx-row" style="margin:0"><input type="checkbox" id="pxCasca" checked> ver quadro anterior</label>
     </div>
     <div class="fx-wrap" style="display:flex;justify-content:center"><canvas id="pxCv" width="384" height="384" aria-label="Área de desenho"></canvas></div>
     <div class="fx-lbl">Quadros da animação (clique para editar)</div>
     <div class="fx-frames" id="pxFrames"></div>
     <div class="fx-tools"><button class="btn" id="pxAdd">＋ Quadro vazio</button><button class="btn" id="pxDup">⧉ Duplicar</button><button class="btn" id="pxDel">✕ Apagar quadro</button></div>
    </div>
    <div>
     <div class="fx-lbl">Paleta (clique duas vezes para trocar a cor)</div>
     <div class="fx-pal" id="pxPal"></div>
     <input type="color" id="pxCor" hidden>
     <div class="fx-lbl">Prévia</div>
     <canvas class="fx-prev" id="pxPrev" width="32" height="32"></canvas>
     <label class="fx-row">Velocidade <input type="range" id="pxFps" min="2" max="16" value="8"> <span id="pxFpsT">8</span> quadros/s</label>
     <div class="fx-lbl">Salvar nos seus sprites</div>
     <div class="fx-row"><input id="pxNome" placeholder="meu_heroi.png" maxlength="40" aria-label="Nome do arquivo"></div>
     <button class="btn pri" id="pxSalvar">Salvar sprite</button>
     <div class="sprerr" id="pxErr" role="status"></div>
    </div>
   </div>
   <div id="pxUso"></div>
  </div></div></div>

<div class="modal" id="mpModal" hidden role="dialog" aria-modal="true" aria-label="Editor de mapas"><div class="mbox">
  <div class="mh"><b>🗺 Editor de mapas</b><button class="btn" id="mpClose" aria-label="Fechar">✕</button></div>
  <div class="mb">
   <div class="fx-row">
    <label>Largura <input type="number" id="mpW" min="10" max="120" value="40"></label>
    <label>Altura <input type="number" id="mpH" min="8" max="40" value="13"></label>
    <button class="btn" id="mpNovo">Novo mapa</button>
    <label>Abrir <select id="mpAbrir"><option value="">um mapa pronto ou seu…</option></select></label>
   </div>
   <div class="fx-grid">
    <div style="min-width:0">
     <div class="fx-tools" id="mpCamadas"><button class="btn on" data-c="blocos">Camada blocos</button><button class="btn" data-c="fundo">Camada fundo (não bate)</button><button class="btn" data-c="obj">Objetos</button><button class="btn" id="mpBorr">🧽 Borracha</button><button class="btn" id="mpDesf">↶ Desfazer</button></div>
     <div class="fx-wrap" style="max-height:60vh"><canvas id="mpCv" width="800" height="260" aria-label="Mapa"></canvas></div>
     <p class="mt">Arraste para pintar. Na camada blocos, grama, terra, pedra, tijolo, gelo e areia são chão sólido; a tábua só segura por cima; água e espinhos são perigo.</p>
    </div>
    <div>
     <div class="fx-lbl">Blocos (tiles.png)</div>
     <div class="fx-tiles" id="mpTiles"></div>
     <div class="fx-lbl">Objetos</div>
     <div class="fx-tools" id="mpObjs"></div>
     <div class="fx-lbl">Salvar nos seus mapas</div>
     <div class="fx-row"><input id="mpNome" placeholder="minha_fase.tmx" maxlength="40" aria-label="Nome do mapa"></div>
     <button class="btn pri" id="mpSalvar">Salvar mapa</button>
     <div class="sprerr" id="mpErr" role="status"></div>
    </div>
   </div>
   <div id="mpUso"></div>
  </div></div></div>

<div class="modal" id="shModal" hidden role="dialog" aria-modal="true" aria-label="Compartilhar jogo"><div class="mbox">
  <div class="mh"><b>🔗 Compartilhar o seu jogo</b><button class="btn" id="shClose" aria-label="Fechar">✕</button></div>
  <div class="mb">
   <p class="mt">O link leva o código desta aula (e os seus sprites e mapas que ele usa). Quem abrir o link joga na Galeria e pode dar estrelas.</p>
   <div class="fx-row"><label style="flex:1">Nome do jogo <input id="shTit" maxlength="50"></label></div>
   <div class="fx-row"><label style="flex:1">Autor <input id="shAut" maxlength="40"></label></div>
   <button class="btn pri" id="shGerar">Gerar link</button>
   <div class="sprerr" id="shErr" role="status"></div>
   <textarea class="fx-link" id="shLink" readonly hidden aria-label="Link do jogo"></textarea>
   <div class="fx-tools"><button class="btn" id="shCopiar" hidden>Copiar link</button></div>
  </div></div></div>

<div class="modal" id="galModal" hidden role="dialog" aria-modal="true" aria-label="Galeria"><div class="mbox">
  <div class="mh"><b>🕹 Galeria da turma</b><button class="btn" id="galClose" aria-label="Fechar">✕</button></div>
  <div class="mb">
   <p class="mt">Jogos que chegaram por link ficam guardados aqui, neste navegador. Cole um link para acrescentar, jogue e dê de 1 a 5 estrelas.</p>
   <div class="fx-row"><input id="galIn" placeholder="Cole aqui o link de um jogo" aria-label="Link de um jogo"><button class="btn pri" id="galAdd">Acrescentar</button></div>
   <div class="sprerr" id="galErr" role="status"></div>
   <div class="gal-list" id="galList"></div>
  </div></div></div>
"""

JS = r"""<script>
/* ===== Oficina 2: ferramentas de criação ===== */
(function(){
  function $(i){return document.getElementById(i)}
  function aviso(m,ms){var t=$('toast');if(!t)return;t.textContent=m;t.classList.add('on');clearTimeout(t._t);t._t=setTimeout(function(){t.classList.remove('on')},ms||4200)}
  function abrir(id){$(id).hidden=false}
  function fechavel(id,btn){$(btn).addEventListener('click',function(){$(id).hidden=true});$(id).addEventListener('click',function(e){if(e.target===$(id))$(id).hidden=true});
    document.addEventListener('keydown',function(e){if(e.key==='Escape'&&!$(id).hidden)$(id).hidden=true})}
  function ls(k,d){try{var v=localStorage.getItem(k);return v?JSON.parse(v):d}catch(e){return d}}
  function lsSet(k,v){try{localStorage.setItem(k,JSON.stringify(v));return true}catch(e){return false}}
  function slug(s,ext){s=String(s||'').trim().toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'').replace(/[^a-z0-9_.-]+/g,'_').replace(/^_+|_+$/g,'');s=s.replace(new RegExp('\\.'+ext+'$'),'');return (s||'meu')+'.'+ext}
  function copiar(t,btn){var ok=function(){if(btn){var o=btn.textContent;btn.textContent='Copiado';setTimeout(function(){btn.textContent=o},1300)}};try{navigator.clipboard.writeText(t).then(ok,function(){})}catch(e){}}

  /* ---------------------------------------------------------------- editor de pixel art */
  var PAL=['', '#000000','#1D2B53','#7E2553','#008751','#AB5236','#5F574F','#C2C3C7','#FFF1E8','#FF004D','#FFA300','#FFEC27','#00E436','#29ADFF','#83769C','#FF77A8',
           '#D68C3E','#9C5A22','#F2D3A0','#222034','#EC6878','#6B6F78','#B8BCC4','#3D4A5C'];
  var px={n:16,frames:[],q:0,cor:16,ferr:'lapis',pal:PAL.slice(),hist:[],fps:8,t0:0};
  function vazio(){return new Array(px.n*px.n).fill(0)}
  function novoPx(n){px.n=n;px.frames=[vazio()];px.q=0;px.hist=[];desenhaTudo()}
  function cel(){var c=$('pxCv');return c.width/px.n}
  function desenha(){var c=$('pxCv'),g=c.getContext('2d'),s=cel(),f=px.frames[px.q];g.clearRect(0,0,c.width,c.height);
    if($('pxCasca').checked&&px.q>0){g.globalAlpha=0.25;var a=px.frames[px.q-1];for(var i=0;i<a.length;i++)if(a[i]){g.fillStyle=px.pal[a[i]];g.fillRect((i%px.n)*s,Math.floor(i/px.n)*s,s,s)}g.globalAlpha=1}
    for(var j=0;j<f.length;j++)if(f[j]){g.fillStyle=px.pal[f[j]];g.fillRect((j%px.n)*s,Math.floor(j/px.n)*s,s,s)}
    g.strokeStyle='rgba(0,0,0,0.12)';g.lineWidth=1;for(var k=0;k<=px.n;k++){g.beginPath();g.moveTo(k*s+0.5,0);g.lineTo(k*s+0.5,c.height);g.moveTo(0,k*s+0.5);g.lineTo(c.width,k*s+0.5);g.stroke()}}
  function quadroCanvas(f,cv){cv.width=px.n;cv.height=px.n;var g=cv.getContext('2d');g.clearRect(0,0,px.n,px.n);for(var i=0;i<f.length;i++)if(f[i]){g.fillStyle=px.pal[f[i]];g.fillRect(i%px.n,Math.floor(i/px.n),1,1)}return cv}
  function desenhaQuadros(){var F=$('pxFrames');F.innerHTML='';px.frames.forEach(function(f,i){var cv=quadroCanvas(f,document.createElement('canvas'));if(i===px.q)cv.className='on';cv.title='Quadro '+(i+1);cv.addEventListener('click',function(){px.q=i;desenhaTudo()});F.appendChild(cv)})}
  function desenhaPal(){var P=$('pxPal');P.innerHTML='';px.pal.forEach(function(c,i){var b=document.createElement('button');b.type='button';if(!i){b.className='vazio';b.title='Transparente'}else{b.style.background=c;b.title=c}if(i===px.cor)b.classList.add('on');
      b.addEventListener('click',function(){px.cor=i;desenhaPal()});
      b.addEventListener('dblclick',function(){if(!i)return;var inp=$('pxCor');inp.value=px.pal[i];inp.onchange=function(){px.pal[i]=inp.value;desenhaTudo()};inp.click()});P.appendChild(b)})}
  function desenhaTudo(){desenha();desenhaQuadros();desenhaPal()}
  function guarda(){px.hist.push(JSON.stringify({f:px.frames,q:px.q}));if(px.hist.length>60)px.hist.shift()}
  function pinta(i,v){var f=px.frames[px.q];if(f[i]===v)return;f[i]=v}
  function balde(i,v){var f=px.frames[px.q],alvo=f[i];if(alvo===v)return;var pilha=[i];while(pilha.length){var k=pilha.pop();if(f[k]!==alvo)continue;f[k]=v;var x=k%px.n,y=Math.floor(k/px.n);if(x>0)pilha.push(k-1);if(x<px.n-1)pilha.push(k+1);if(y>0)pilha.push(k-px.n);if(y<px.n-1)pilha.push(k+px.n)}}
  function idxDe(e){var c=$('pxCv'),r=c.getBoundingClientRect(),x=Math.floor((e.clientX-r.left)/r.width*px.n),y=Math.floor((e.clientY-r.top)/r.height*px.n);if(x<0||y<0||x>=px.n||y>=px.n)return -1;return y*px.n+x}
  var desenhando=false;
  function acao(e,primeiro){var i=idxDe(e);if(i<0)return;
    if(px.ferr==='gotas'){var v=px.frames[px.q][i];if(v){px.cor=v;desenhaPal()}return}
    if(primeiro)guarda();
    if(px.ferr==='balde'){if(primeiro)balde(i,px.cor)}else pinta(i,px.ferr==='borracha'?0:px.cor);
    desenha();desenhaQuadros()}
  function preview(t){var m=$('pxModal');if(m.hidden){px.anim=0;return}var cv=$('pxPrev'),k=Math.floor(t/1000*px.fps)%px.frames.length;quadroCanvas(px.frames[k],cv);px.anim=requestAnimationFrame(preview)}
  function listaSprites(){var s=$('pxAbrir');s.innerHTML='<option value="">um sprite pronto ou seu…</option>';Object.keys(window.OF_SPRITES||{}).forEach(function(k){var o=window.OF_SPRITES[k];if(k.indexOf('__')===0||!o||!o.uri)return;var fw=o.w/(o.q||1);if(fw>32||o.h>32)return;var op=document.createElement('option');op.value=k;op.textContent=k.split('/').pop()+(o.own?' (seu)':'')+' · '+(o.q||1)+' quadro(s)';s.appendChild(op)})}
  function abrirSprite(k){var o=window.OF_SPRITES[k];if(!o)return;var im=new Image();im.onload=function(){var q=o.q||1,fw=Math.round(o.w/q),n=Math.max(fw,o.h);var nn=[8,16,24,32].filter(function(x){return x>=n})[0]||32;
      var cv=document.createElement('canvas');cv.width=o.w;cv.height=o.h;var g=cv.getContext('2d');g.drawImage(im,0,0);var d=g.getImageData(0,0,o.w,o.h).data;
      var cores={},lista=[''];function idx(r,gg,b,a){if(a<128)return 0;var h='#'+[r,gg,b].map(function(v){return ('0'+v.toString(16)).slice(-2)}).join('').toUpperCase();if(cores[h]==null){if(lista.length>=32)return 1;cores[h]=lista.length;lista.push(h)}return cores[h]}
      var fr=[];for(var f=0;f<q;f++){var a=new Array(nn*nn).fill(0);for(var y=0;y<o.h;y++)for(var x=0;x<fw;x++){var p=(y*o.w+f*fw+x)*4;a[y*nn+x]=idx(d[p],d[p+1],d[p+2],d[p+3])}fr.push(a)}
      while(lista.length<PAL.length)lista.push(PAL[lista.length]);px.pal=lista;px.n=nn;$('pxTam').value=String(nn);px.frames=fr;px.q=0;px.hist=[];px.cor=1;$('pxNome').value=o.own?k.split('/').pop():slug(k.split('/').pop().replace('.png','')+'_meu','png');desenhaTudo()};im.src=o.uri}
  function salvarPx(){var nome=slug($('pxNome').value||'meu_sprite','png'),k='assets/sprites/'+nome,base=window.OF_SPRITES[k];
    if(base&&!base.own){$('pxErr').textContent='Já existe um sprite pronto chamado '+nome+'. Escolha outro nome.';return}
    var q=px.frames.length,cv=document.createElement('canvas');cv.width=px.n*q;cv.height=px.n;var g=cv.getContext('2d');
    px.frames.forEach(function(f,i){for(var j=0;j<f.length;j++)if(f[j]){g.fillStyle=px.pal[f[j]];g.fillRect(i*px.n+j%px.n,Math.floor(j/px.n),1,1)}});
    var uri=cv.toDataURL('image/png'),own=ls('oficina2.sprites',{});own[k]={w:cv.width,h:cv.height,q:q,desc:'Desenhado no editor',uri:uri};
    if(!lsSet('oficina2.sprites',own)){$('pxErr').textContent='O navegador não tem mais espaço. Apague alguma imagem sua no 🖼 Sprites.';return}
    var im=new Image();im.src=uri;own[k].own=true;window.OF_SPRITES[k]=own[k];window.OF_SPRITE_IMG[k]=im;$('pxErr').textContent='';$('pxNome').value=nome;listaSprites();
    var flame=q>1?"animation = await game.loadSpriteAnimation(\n  '"+nome+"',\n  SpriteAnimationData.sequenced(amount: "+q+", stepTime: "+(1/px.fps).toFixed(2)+", textureSize: Vector2.all("+px.n+")),\n);":"sprite = await game.loadSprite('"+nome+"');";
    $('pxUso').innerHTML='<h3>Pronto: '+nome+' ('+q+' quadro'+(q>1?'s':'')+' de '+px.n+'×'+px.n+')</h3><p class="mt">No Flame, dentro do onLoad de um '+(q>1?'SpriteAnimationComponent':'SpriteComponent')+':</p><div class="fx-code" id="pxSnip"></div><button class="btn" id="pxCopSnip">Copiar</button><p class="mt">No Flutter sem Flame, o caminho é assets/sprites/'+nome+'.</p>';
    $('pxSnip').textContent=flame;$('pxCopSnip').addEventListener('click',function(){copiar(flame,this)});
    if(window.OF&&OF.rerender)OF.rerender();aviso('Sprite '+nome+' salvo nos seus sprites.')}
  function ligaPx(){
    var cv=$('pxCv');
    cv.addEventListener('pointerdown',function(e){desenhando=true;try{cv.setPointerCapture(e.pointerId)}catch(x){}acao(e,true);e.preventDefault()});
    cv.addEventListener('pointermove',function(e){if(desenhando&&px.ferr!=='balde'&&px.ferr!=='gotas')acao(e,false)});
    cv.addEventListener('pointerup',function(){desenhando=false});cv.addEventListener('pointercancel',function(){desenhando=false});
    [].forEach.call($('pxTools').querySelectorAll('[data-t]'),function(b){b.addEventListener('click',function(){px.ferr=b.dataset.t;[].forEach.call($('pxTools').querySelectorAll('[data-t]'),function(x){x.classList.toggle('on',x===b)})})});
    $('pxEsp').addEventListener('click',function(){guarda();var f=px.frames[px.q],n=px.n,g=f.slice();for(var y=0;y<n;y++)for(var x=0;x<n;x++)f[y*n+x]=g[y*n+n-1-x];desenhaTudo()});
    $('pxLimpa').addEventListener('click',function(){guarda();px.frames[px.q]=vazio();desenhaTudo()});
    $('pxDesf').addEventListener('click',function(){var h=px.hist.pop();if(!h)return;var o=JSON.parse(h);px.frames=o.f;px.q=Math.min(o.q,px.frames.length-1);desenhaTudo()});
    $('pxCasca').addEventListener('change',desenha);
    $('pxAdd').addEventListener('click',function(){guarda();px.frames.splice(px.q+1,0,vazio());px.q++;desenhaTudo()});
    $('pxDup').addEventListener('click',function(){guarda();px.frames.splice(px.q+1,0,px.frames[px.q].slice());px.q++;desenhaTudo()});
    $('pxDel').addEventListener('click',function(){if(px.frames.length<2)return;guarda();px.frames.splice(px.q,1);px.q=Math.max(0,px.q-1);desenhaTudo()});
    $('pxFps').addEventListener('input',function(){px.fps=+this.value;$('pxFpsT').textContent=this.value});
    $('pxTam').addEventListener('change',function(){novoPx(+this.value)});
    $('pxNovo').addEventListener('click',function(){px.pal=PAL.slice();novoPx(+$('pxTam').value);$('pxNome').value=''});
    $('pxAbrir').addEventListener('change',function(){if(this.value)abrirSprite(this.value)});
    $('pxSalvar').addEventListener('click',salvarPx);
    fechavel('pxModal','pxClose');
    $('pxBtn').addEventListener('click',function(){listaSprites();if(!px.frames.length)novoPx(16);else desenhaTudo();abrir('pxModal');if(!px.anim)px.anim=requestAnimationFrame(preview)})}

  /* ---------------------------------------------------------------- editor de mapas */
  var T=16,SOLIDO=[1,2,3,4,15,16],TABUA=5,PERIGO=[6,13],TILES=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,19];
  var NOMES={1:'grama',2:'terra',3:'pedra',4:'tijolo',5:'tábua',6:'água',7:'piso claro',8:'piso escuro',9:'arbusto',10:'flor',11:'placa',12:'porta',13:'espinhos',14:'escada',15:'gelo',16:'areia',19:'tocha'};
  var OBJS=[['osso','🦴 Osso'],['dourado','⭐ Osso dourado'],['inimigo','🐱 Gato'],['inicio','🐶 Início'],['fim','🚪 Chegada']];
  var mp={w:40,h:13,blocos:[],fundo:[],objs:[],cam:'blocos',tile:1,obj:'osso',borr:false,hist:[],s:20};
  function tileset(){var I=window.OF_SPRITE_IMG||{};return I['assets/sprites/tiles.png']}
  function novoMapa(w,h,chao){mp.w=w;mp.h=h;mp.blocos=new Array(w*h).fill(0);mp.fundo=new Array(w*h).fill(0);mp.objs=[];mp.hist=[];
    if(chao){for(var x=0;x<w;x++){mp.blocos[(h-3)*w+x]=1;mp.blocos[(h-2)*w+x]=2;mp.blocos[(h-1)*w+x]=2}mp.objs.push({t:'inicio',x:1,y:h-4});mp.objs.push({t:'fim',x:w-3,y:h-5})}desenhaMapa()}
  function tileEm(g,id,dx,dy,s){var im=tileset();if(!im||!id)return;var k=id-1;g.drawImage(im,(k%8)*16,Math.floor(k/8)*16,16,16,dx,dy,s,s)}
  function iconeObj(g,t,dx,dy,s){var I=window.OF_SPRITE_IMG||{},nome={osso:'osso',dourado:'osso_dourado',inimigo:'gato',inicio:'heroi'}[t];
    if(t==='fim'){tileEm(g,12,dx,dy,s);tileEm(g,12,dx,dy+s,s);return}var im=I['assets/sprites/'+nome+'.png'];if(im)g.drawImage(im,0,0,16,16,dx,dy,s,s)}
  function desenhaMapa(){var c=$('mpCv'),s=mp.s;c.width=mp.w*s;c.height=mp.h*s;var g=c.getContext('2d');g.imageSmoothingEnabled=false;g.fillStyle='#8FD3F4';g.fillRect(0,0,c.width,c.height);
    for(var i=0;i<mp.w*mp.h;i++){var x=(i%mp.w)*s,y=Math.floor(i/mp.w)*s;tileEm(g,mp.fundo[i],x,y,s);tileEm(g,mp.blocos[i],x,y,s)}
    if(mp.cam==='fundo'){g.fillStyle='rgba(255,255,255,0.25)';for(var j=0;j<mp.w*mp.h;j++)if(mp.blocos[j])g.fillRect((j%mp.w)*s,Math.floor(j/mp.w)*s,s,s)}
    mp.objs.forEach(function(o){iconeObj(g,o.t,o.x*s,o.y*s,s)});
    g.strokeStyle='rgba(0,0,0,0.08)';for(var k=0;k<=mp.w;k++){g.beginPath();g.moveTo(k*s+0.5,0);g.lineTo(k*s+0.5,c.height);g.stroke()}for(k=0;k<=mp.h;k++){g.beginPath();g.moveTo(0,k*s+0.5);g.lineTo(c.width,k*s+0.5);g.stroke()}}
  function guardaMp(){mp.hist.push(JSON.stringify({b:mp.blocos,f:mp.fundo,o:mp.objs}));if(mp.hist.length>60)mp.hist.shift()}
  function celMp(e){var c=$('mpCv'),r=c.getBoundingClientRect(),x=Math.floor((e.clientX-r.left)/r.width*mp.w),y=Math.floor((e.clientY-r.top)/r.height*mp.h);if(x<0||y<0||x>=mp.w||y>=mp.h)return null;return{x:x,y:y}}
  function pintaMp(p,primeiro){if(!p)return;var i=p.y*mp.w+p.x;
    if(mp.cam==='obj'){if(!primeiro)return;guardaMp();var ja=mp.objs.findIndex(function(o){return o.x===p.x&&(o.y===p.y||(o.t==='fim'&&o.y+1===p.y))});
      if(ja>=0){mp.objs.splice(ja,1)}else if(!mp.borr){if(mp.obj==='inicio'||mp.obj==='fim')mp.objs=mp.objs.filter(function(o){return o.t!==mp.obj});mp.objs.push({t:mp.obj,x:p.x,y:mp.obj==='fim'?Math.max(0,p.y-1):p.y})}desenhaMapa();return}
    if(primeiro)guardaMp();var arr=mp.cam==='fundo'?mp.fundo:mp.blocos;arr[i]=mp.borr?0:mp.tile;desenhaMapa()}
  function retangulos(ids){var runs=[];for(var y=0;y<mp.h;y++){var x=0;while(x<mp.w){if(ids.indexOf(mp.blocos[y*mp.w+x])>=0){var x0=x;while(x<mp.w&&ids.indexOf(mp.blocos[y*mp.w+x])>=0)x++;runs.push([x0,y,x-x0,1])}else x++}}
    var j=[];runs.forEach(function(r){var u=j.filter(function(q){return q[0]===r[0]&&q[2]===r[2]&&q[1]+q[3]===r[1]})[0];if(u)u[3]++;else j.push(r)});return j}
  function csv(a){var l=[];for(var y=0;y<mp.h;y++)l.push(a.slice(y*mp.w,y*mp.w+mp.w).join(','));return l.join(',\n')}
  function gerarTmx(){var id=1,sol=[],obj=[];
    retangulos(SOLIDO).forEach(function(r){sol.push('  <object id="'+(id++)+'" type="chao" x="'+r[0]*T+'" y="'+r[1]*T+'" width="'+r[2]*T+'" height="'+r[3]*T+'"/>')});
    retangulos([TABUA]).forEach(function(r){sol.push('  <object id="'+(id++)+'" type="plataforma" x="'+r[0]*T+'" y="'+r[1]*T+'" width="'+r[2]*T+'" height="7"/>')});
    retangulos([13]).forEach(function(r){obj.push('  <object id="'+(id++)+'" name="espinhos" type="perigo" x="'+r[0]*T+'" y="'+(r[1]*T+8)+'" width="'+r[2]*T+'" height="8"/>')});
    retangulos([6]).forEach(function(r){obj.push('  <object id="'+(id++)+'" name="agua" type="perigo" x="'+r[0]*T+'" y="'+(r[1]*T+3)+'" width="'+r[2]*T+'" height="13"/>')});
    mp.objs.forEach(function(o){var cx=o.x*T+T/2,cy=o.y*T+T/2;
      if(o.t==='osso'||o.t==='dourado')obj.push('  <object id="'+(id++)+'" name="'+o.t+'" type="'+o.t+'" x="'+cx+'" y="'+cy+'">\n   <properties><property name="valor" type="int" value="'+(o.t==='dourado'?5:1)+'"/></properties>\n  </object>');
      else if(o.t==='inimigo'||o.t==='inicio')obj.push('  <object id="'+(id++)+'" name="'+(o.t==='inimigo'?'gato':'inicio')+'" type="'+o.t+'" x="'+cx+'" y="'+(o.y+1)*T+'">\n   <point/>\n  </object>');
      else if(o.t==='fim')obj.push('  <object id="'+(id++)+'" name="fim" type="fim" x="'+o.x*T+'" y="'+o.y*T+'" width="'+T+'" height="'+2*T+'"/>')});
    var fundo=mp.fundo.slice();mp.objs.forEach(function(o){if(o.t==='fim'){fundo[o.y*mp.w+o.x]=12;if(o.y+1<mp.h)fundo[(o.y+1)*mp.w+o.x]=12}});
    return '<?xml version="1.0" encoding="UTF-8"?>\n<map version="1.10" tiledversion="1.10.2" orientation="orthogonal" renderorder="right-down" width="'+mp.w+'" height="'+mp.h+'" tilewidth="16" tileheight="16" infinite="0" nextlayerid="5" nextobjectid="'+id+'">\n'+
      ' <tileset firstgid="1" name="tiles" tilewidth="16" tileheight="16" tilecount="24" columns="8">\n  <image source="tiles.png" width="128" height="48"/>\n  <tile id="5"><animation><frame tileid="5" duration="300"/><frame tileid="16" duration="300"/><frame tileid="17" duration="300"/></animation></tile>\n  <tile id="18"><animation><frame tileid="18" duration="120"/><frame tileid="19" duration="120"/><frame tileid="20" duration="120"/></animation></tile>\n </tileset>\n'+
      ' <layer id="1" name="fundo" width="'+mp.w+'" height="'+mp.h+'">\n  <data encoding="csv">\n'+csv(fundo)+'\n</data>\n </layer>\n'+
      ' <layer id="2" name="blocos" width="'+mp.w+'" height="'+mp.h+'">\n  <data encoding="csv">\n'+csv(mp.blocos)+'\n</data>\n </layer>\n'+
      ' <objectgroup id="3" name="solidos">\n'+sol.join('\n')+'\n </objectgroup>\n <objectgroup id="4" name="objetos">\n'+obj.join('\n')+'\n </objectgroup>\n</map>\n'}
  function abrirMapa(k){var t=(window.OF_MAPS||{})[k];if(!t)return;var d=new DOMParser().parseFromString(t,'application/xml'),m=d.querySelector('map');if(!m)return;
    if(m.getAttribute('orientation')!=='orthogonal'){$('mpErr').textContent='Este editor abre só mapas ortogonais (vista de lado ou de cima).';return}
    var w=+m.getAttribute('width'),h=+m.getAttribute('height');function camada(n){var l=[].filter.call(d.querySelectorAll('layer'),function(x){return x.getAttribute('name')===n})[0];if(!l)return null;
      var dt=l.querySelector('data');if(!dt||dt.getAttribute('encoding')!=='csv')return null;return dt.textContent.trim().split(/[\s,]+/).map(function(v){return (+v)&0x1fffffff})}
    var b=camada('blocos')||camada('paredes'),f=camada('fundo'),ch=camada('chao'),dc=camada('decoracao');
    if(!b){$('mpErr').textContent='Não achei a camada de blocos neste mapa.';return}
    if(!f){f=new Array(w*h).fill(0);if(ch)ch.forEach(function(v,i){f[i]=v});if(dc)dc.forEach(function(v,i){if(v)f[i]=v})}
    mp.w=w;mp.h=h;mp.blocos=b;mp.fundo=f.map(function(v){return v===12?0:v});mp.objs=[];mp.hist=[];$('mpW').value=w;$('mpH').value=h;
    [].forEach.call(d.querySelectorAll('objectgroup[name="objetos"] object'),function(o){var ty=o.getAttribute('type')||o.getAttribute('class'),x=+o.getAttribute('x'),y=+o.getAttribute('y');
      if(ty==='osso'||ty==='dourado')mp.objs.push({t:ty,x:Math.floor(x/T),y:Math.floor(y/T)});
      else if(ty==='inimigo'||ty==='inicio')mp.objs.push({t:ty,x:Math.floor(x/T),y:Math.max(0,Math.round(y/T)-1)});
      else if(ty==='fim')mp.objs.push({t:'fim',x:Math.floor(x/T),y:Math.floor(y/T)})});
    $('mpNome').value=/^assets\/tiles\//.test(k)&&ls('oficina2.mapas',{})[k]?k.split('/').pop():slug(k.split('/').pop().replace('.tmx','')+'_meu','tmx');$('mpErr').textContent='';desenhaMapa()}
  function listaMapas(){var s=$('mpAbrir');s.innerHTML='<option value="">um mapa pronto ou seu…</option>';Object.keys(window.OF_MAPS||{}).forEach(function(k){var t=window.OF_MAPS[k];if(/orientation="isometric"/.test(t))return;var op=document.createElement('option');op.value=k;op.textContent=k.split('/').pop()+(ls('oficina2.mapas',{})[k]?' (seu)':'');s.appendChild(op)})}
  function salvarMp(){var nome=slug($('mpNome').value||'minha_fase','tmx'),k='assets/tiles/'+nome,om=ls('oficina2.mapas',{});
    if(window.OF_MAPS[k]&&!om[k]){$('mpErr').textContent='Já existe um mapa pronto chamado '+nome+'. Escolha outro nome.';return}
    if(!mp.objs.some(function(o){return o.t==='inicio'})){$('mpErr').textContent='Ponha o objeto 🐶 Início em algum lugar do mapa.';return}
    var t=gerarTmx();om[k]=t;if(!lsSet('oficina2.mapas',om)){$('mpErr').textContent='O navegador não tem mais espaço. Apague algum mapa seu no 🖼 Sprites.';return}
    window.OF_MAPS[k]=t;$('mpErr').textContent='';$('mpNome').value=nome;listaMapas();
    var snip="final mapa = await TiledComponent.load('"+nome+"', Vector2.all(48));";
    $('mpUso').innerHTML='<h3>Pronto: '+nome+' ('+mp.w+'×'+mp.h+' blocos)</h3><p class="mt">Use no lugar do mapa do Projeto 6 ou da aula de plataforma (camadas solidos e objetos como as delas):</p><div class="fx-code" id="mpSnip"></div><button class="btn" id="mpCop">Copiar</button>';
    $('mpSnip').textContent=snip;$('mpCop').addEventListener('click',function(){copiar(snip,this)});if(window.OF&&OF.rerender)OF.rerender();aviso('Mapa '+nome+' salvo nos seus mapas.')}
  function ligaMp(){
    var T2=$('mpTiles');TILES.forEach(function(id){var b=document.createElement('button');b.type='button';b.title=NOMES[id];var cv=document.createElement('canvas');cv.width=16;cv.height=16;b.appendChild(cv);b.dataset.id=id;
      b.addEventListener('click',function(){mp.tile=id;mp.borr=false;if(mp.cam==='obj')mudaCam('blocos');marca()});T2.appendChild(b)});
    var O=$('mpObjs');OBJS.forEach(function(o){var b=document.createElement('button');b.className='btn';b.type='button';b.textContent=o[1];b.dataset.o=o[0];b.addEventListener('click',function(){mp.obj=o[0];mp.borr=false;mudaCam('obj');marca()});O.appendChild(b)});
    function marca(){[].forEach.call(T2.children,function(b){b.classList.toggle('on',+b.dataset.id===mp.tile&&mp.cam!=='obj'&&!mp.borr)});[].forEach.call(O.children,function(b){b.classList.toggle('on',b.dataset.o===mp.obj&&mp.cam==='obj'&&!mp.borr)});$('mpBorr').classList.toggle('on',mp.borr)}
    function mudaCam(c){mp.cam=c;[].forEach.call($('mpCamadas').querySelectorAll('[data-c]'),function(b){b.classList.toggle('on',b.dataset.c===c)});desenhaMapa();marca()}
    [].forEach.call($('mpCamadas').querySelectorAll('[data-c]'),function(b){b.addEventListener('click',function(){mudaCam(b.dataset.c)})});
    $('mpBorr').addEventListener('click',function(){mp.borr=!mp.borr;marca()});
    $('mpDesf').addEventListener('click',function(){var h=mp.hist.pop();if(!h)return;var o=JSON.parse(h);mp.blocos=o.b;mp.fundo=o.f;mp.objs=o.o;desenhaMapa()});
    var cv=$('mpCv'),pint=false;cv.addEventListener('pointerdown',function(e){pint=true;try{cv.setPointerCapture(e.pointerId)}catch(x){}pintaMp(celMp(e),true);e.preventDefault()});
    cv.addEventListener('pointermove',function(e){if(pint)pintaMp(celMp(e),false)});cv.addEventListener('pointerup',function(){pint=false});cv.addEventListener('pointercancel',function(){pint=false});
    $('mpNovo').addEventListener('click',function(){var w=Math.max(10,Math.min(120,+$('mpW').value||40)),h=Math.max(8,Math.min(40,+$('mpH').value||13));novoMapa(w,h,true);$('mpNome').value=''});
    $('mpAbrir').addEventListener('change',function(){if(this.value)abrirMapa(this.value)});
    $('mpSalvar').addEventListener('click',salvarMp);fechavel('mpModal','mpClose');
    $('mpBtn').addEventListener('click',function(){listaMapas();if(!mp.blocos.length)novoMapa(40,13,true);[].forEach.call(T2.children,function(b){var g=b.firstChild.getContext('2d');g.clearRect(0,0,16,16);tileEm(g,+b.dataset.id,0,0,16)});marca();desenhaMapa();abrir('mpModal')})}

  /* ---------------------------------------------------------------- compartilhar e galeria */
  var SITE='https://oficina-flutter-2.vercel.app/';
  function b64u(bytes){var s='';for(var i=0;i<bytes.length;i++)s+=String.fromCharCode(bytes[i]);return btoa(s).replace(/\+/g,'-').replace(/\//g,'_').replace(/=+$/,'')}
  function deB64u(t){t=t.replace(/-/g,'+').replace(/_/g,'/');while(t.length%4)t+='=';var s=atob(t),u=new Uint8Array(s.length);for(var i=0;i<s.length;i++)u[i]=s.charCodeAt(i);return u}
  function comprime(txt){var dados=new TextEncoder().encode(txt);if(typeof CompressionStream==='undefined')return Promise.resolve('0'+b64u(dados));
    return new Response(new Blob([dados]).stream().pipeThrough(new CompressionStream('deflate-raw'))).arrayBuffer().then(function(ab){return '1'+b64u(new Uint8Array(ab))})}
  function descomprime(t){var tipo=t[0],u=deB64u(t.slice(1));if(tipo==='0')return Promise.resolve(new TextDecoder().decode(u));
    return new Response(new Blob([u]).stream().pipeThrough(new DecompressionStream('deflate-raw'))).text()}
  function anexos(code){var a={s:{},m:{}},own=ls('oficina2.sprites',{}),om=ls('oficina2.mapas',{}),rr=/['"]([\w\/.-]+\.(png|jpg|jpeg|gif|webp|tmx))['"]/g,m;
    while((m=rr.exec(code))){var base=m[1].split('/').pop();if(m[2]==='tmx'){var km='assets/tiles/'+base;if(om[km])a.m[km]=om[km]}else{var ks='assets/sprites/'+base;if(own[ks])a.s[ks]=own[ks]}}
    Object.keys(a.m).forEach(function(k){var im=/<image[^>]*source="([^"]+)"/.exec(a.m[k]);if(im){var ks='assets/sprites/'+im[1].split('/').pop();if(own[ks])a.s[ks]=own[ks]}});return a}
  function gal(){return ls('oficina2.galeria',[])}
  function galSalva(l){return lsSet('oficina2.galeria',l)}
  function idDe(j){var h=0,s=j.t+'|'+j.a+'|'+j.c;for(var i=0;i<s.length;i++)h=(h*31+s.charCodeAt(i))|0;return 'g'+(h>>>0).toString(36)}
  function recebe(j,link){var l=gal(),id=idDe(j),ja=l.filter(function(x){return x.id===id})[0];if(!ja){ja={id:id,t:j.t,a:j.a,c:j.c,x:j.x||{},d:new Date().toISOString().slice(0,10),nota:0,link:link};l.unshift(ja);if(!galSalva(l))aviso('O navegador não tem espaço para guardar mais jogos na galeria.')}return id}
  function lerLink(link){var m=/[#&]jogo=([A-Za-z0-9_-]+)/.exec(link||'');if(!m)return Promise.reject(new Error('Esse texto não tem um jogo da Oficina.'));
    return descomprime(m[1]).then(function(t){var j=JSON.parse(t);if(!j||typeof j.c!=='string')throw new Error('Link incompleto.');return j})}
  var destaque=null;
  function desenhaGal(){var L=$('galList');L.innerHTML='';var l=gal();
    if(!l.length){L.innerHTML='<p class="mt">Nenhum jogo ainda. Peça para os colegas usarem o botão 🔗 Compartilhar e mandarem o link.</p>';return}
    l.forEach(function(j){var c=document.createElement('div');c.className='gal-c'+(j.id===destaque?' novo':'');
      c.innerHTML='<b></b><small></small><div class="gal-st"></div><div class="fx-tools"><button class="btn pri" data-a="jogar">▶ Jogar</button><button class="btn" data-a="link">Copiar link</button><button class="btn" data-a="apagar">Apagar</button></div>';
      c.querySelector('b').textContent=j.t;c.querySelector('small').textContent='por '+(j.a||'alguém')+' · '+j.d;
      var st=c.querySelector('.gal-st');for(var k=1;k<=5;k++)(function(k){var b=document.createElement('button');b.type='button';b.textContent=k<=j.nota?'★':'☆';b.title=k+' estrela'+(k>1?'s':'');b.setAttribute('aria-label',b.title);
        b.addEventListener('click',function(){var l2=gal();l2.forEach(function(x){if(x.id===j.id)x.nota=k});galSalva(l2);desenhaGal()});st.appendChild(b)})(k);
      c.querySelector('[data-a=jogar]').addEventListener('click',function(){jogar(j)});
      c.querySelector('[data-a=link]').addEventListener('click',function(){copiar(j.link||'',this)});
      c.querySelector('[data-a=apagar]').addEventListener('click',function(){var b=this;if(b.dataset.sure!=='1'){b.dataset.sure='1';b.textContent='Apagar mesmo?';return}galSalva(gal().filter(function(x){return x.id!==j.id}));desenhaGal()});
      L.appendChild(c)})}
  function jogar(j){
    Object.keys((j.x&&j.x.s)||{}).forEach(function(k){var s=j.x.s[k];if(!s||!s.uri)return;var o=Object.assign({},s,{own:true});window.OF_SPRITES[k]=o;var im=new Image();im.src=s.uri;window.OF_SPRITE_IMG[k]=im});
    Object.keys((j.x&&j.x.m)||{}).forEach(function(k){window.OF_MAPS[k]=j.x.m[k]});
    var sel=$('lessonSel'),i=(window.OF.LESSONS||[]).findIndex(function(L){return /^Sala de jogos/.test(String(L.t).replace(/^\d+\.\s*/,''))});if(i<0){aviso('Não achei a Sala de jogos.');return}
    sel.selectedIndex=i;sel.dispatchEvent(new Event('change',{bubbles:true}));
    setTimeout(function(){var c=$('code');c.value=j.c;c.dispatchEvent(new Event('input',{bubbles:true}));$('galModal').hidden=true;
      setTimeout(function(){var vs=$('vS');if(vs)vs.click();var t=document.querySelector('[data-a=test]');if(t&&t.getAttribute('aria-pressed')!=='true')t.click();aviso('Jogando: '+j.t+' (de '+(j.a||'alguém')+')')},150)},150)}
  function ligaGal(){
    fechavel('shModal','shClose');fechavel('galModal','galClose');
    $('shBtn').addEventListener('click',function(){var L=(window.OF.LESSONS||[])[(OF.A&&OF.A.S||{}).lesson]||{};$('shTit').value=$('shTit').value||String(L.t||'Meu jogo').replace(/^\d+\.\s*/,'').replace(/^Projeto · /,'');
      $('shAut').value=$('shAut').value||(function(){try{var v=localStorage.getItem('oficina2.name')||'';try{var p=JSON.parse(v);if(typeof p==='string')v=p}catch(x){}return v}catch(e){return ''}})();$('shLink').hidden=true;$('shCopiar').hidden=true;$('shErr').textContent='';abrir('shModal')});
    $('shGerar').addEventListener('click',function(){var code=(OF.A&&OF.A.S&&OF.A.S.src)||$('code').value||'';if(!code.trim()){$('shErr').textContent='Não há código nesta aula.';return}
      var j={t:$('shTit').value.trim()||'Meu jogo',a:$('shAut').value.trim(),c:code,x:anexos(code)};
      comprime(JSON.stringify(j)).then(function(z){var base=/^https?:/.test(location.protocol)&&window.top===window.self?location.origin+location.pathname:SITE,link=base+'#jogo='+z;
        $('shLink').value=link;$('shLink').hidden=false;$('shCopiar').hidden=false;$('shErr').textContent=link.length>8000?'O link ficou longo ('+Math.round(link.length/1000)+' mil caracteres): alguns aplicativos de mensagem cortam. Prefira mandar por e-mail ou num documento.':'';
        recebe(j,link);copiar(link,null);aviso('Link gerado e copiado. Ele também ficou na sua 🕹 Galeria.')}).catch(function(e){$('shErr').textContent='Não consegui gerar o link: '+e.message})});
    $('shCopiar').addEventListener('click',function(){copiar($('shLink').value,this)});
    $('galBtn').addEventListener('click',function(){destaque=null;$('galErr').textContent='';desenhaGal();abrir('galModal')});
    $('galAdd').addEventListener('click',function(){var t=$('galIn').value.trim();lerLink(t).then(function(j){destaque=recebe(j,t.slice(t.indexOf('http')>=0?t.indexOf('http'):0));$('galIn').value='';$('galErr').textContent='';desenhaGal()}).catch(function(e){$('galErr').textContent=e.message})});
    if(/[#&]jogo=/.test(location.hash)){lerLink(location.hash).then(function(j){destaque=recebe(j,location.href);try{history.replaceState(null,'',location.pathname+location.search)}catch(e){}desenhaGal();abrir('galModal')}).catch(function(e){aviso('Não consegui abrir o jogo do link: '+e.message,6000)})}}

  /* ---------------------------------------------------------------- planilha da turma */
  function salvarArquivo(nome,blob){var dentro=window.self!==window.top;
    var cap=null;try{if(window.claude&&typeof window.claude.use==='function')return window.claude.use('downloads').then(function(d){if(!d)throw new Error('sem permissão');return d.save({filename:nome,data:blob})}).then(function(){aviso('Salvo: '+nome)},function(e){aviso(dentro?'Aqui dentro o navegador não deixa baixar. Abra oficina-flutter-2.vercel.app e baixe lá.':'Não consegui salvar ('+(e&&e.code||e.message)+').',5000)})}catch(e){}
    if(dentro){aviso('Aqui dentro o navegador não deixa baixar. Abra oficina-flutter-2.vercel.app e baixe lá.',5000);return}
    var a=document.createElement('a'),u=URL.createObjectURL(blob);a.href=u;a.download=nome;document.body.appendChild(a);a.click();setTimeout(function(){URL.revokeObjectURL(u);a.remove()},4000);aviso('Baixando '+nome)}
  window.OF_SALVAR=salvarArquivo;
  function ligaCsv(){var out=$('profOut');if(!out)return;var b=document.createElement('button');b.className='btn';b.id='profCsv';b.textContent='⬇ Baixar planilha (.csv)';b.hidden=true;out.parentNode.insertBefore(b,out.nextSibling);
    new MutationObserver(function(){b.hidden=!out.querySelector('table')}).observe(out,{childList:true,subtree:true});
    b.addEventListener('click',function(){var tb=out.querySelector('table');if(!tb)return;var T=(window.OF.LESSONS||[]).map(function(L){return String(L.t).replace(/^\d+\.\s*/,'')}),lin=[];
      [].forEach.call(tb.querySelectorAll('tr'),function(tr,ri){var cel=[].map.call(tr.children,function(td,ci){var v=td.textContent.trim();if(ri===0&&ci>=2)v=T[ci-2]||v;if(ri>0&&ci>=2)v=v?'sim':'';return '"'+v.replace(/"/g,'""')+'"'});lin.push(cel.join(';'))});
      salvarArquivo('turma_oficina_flutter_2.csv',new Blob(['﻿'+lin.join('\r\n')],{type:'text/csv'}))})}

  function inicia(){try{ligaPx()}catch(e){console.error(e)}try{ligaMp()}catch(e){console.error(e)}try{ligaGal()}catch(e){console.error(e)}try{ligaCsv()}catch(e){console.error(e)}}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',inicia);else inicia();
})();
</script>
"""


def patch(src):
    src = sub1(src,
        '<button class="btn" id="sprBtn" title="Sprites prontos e suas próprias imagens">🖼 Sprites</button>',
        '<button class="btn" id="sprBtn" title="Sprites prontos e suas próprias imagens">🖼 Sprites</button>'
        '<button class="btn" id="pxBtn" title="Desenhar um sprite em pixel art">🎨 Desenhar</button>'
        '<button class="btn" id="mpBtn" title="Montar um mapa do Tiled">🗺 Mapa</button>'
        '<button class="btn" id="shBtn" title="Gerar um link do seu jogo">🔗 Compartilhar</button>'
        '<button class="btn" id="galBtn" title="Jogos da turma">🕹 Galeria</button>',
        'botoes ferramentas')
    return src


def finish(src):
    return src + CSS + HTML + JS
