# Oficina Flutter 2 · janela da aula: um botão fixo (📘 Aula) abre, de qualquer lugar, a aula aberta
# (texto, Experimente, leitura, etapas) e a lista de todas as aulas por parte, com busca.
# Também põe em cada aula a linha "Você vai usar" (pré-requisitos, do trilha.py) e o aviso das partes eletivas.
import json
import trilha

CSS = r"""<style>
#aulaFab{position:fixed;z-index:90;left:max(14px,env(safe-area-inset-left,0px));bottom:calc(14px + env(safe-area-inset-bottom,0px));
  border:0;border-radius:999px;padding:11px 16px;font:600 15px var(--f-ui,system-ui,sans-serif);cursor:pointer;
  background:var(--accent,#2f6fed);color:var(--accent-ink,#fff);box-shadow:0 4px 14px rgba(0,0,0,.28)}
#aulaFab:focus-visible{outline:3px solid var(--ink);outline-offset:2px}
#auModal{z-index:95}
#auModal .mbox{width:min(900px,100%);height:min(90vh,900px)}
#auModal .mb{overflow:auto;flex:1;min-height:0}
.au-nav{display:flex;gap:6px;flex-wrap:wrap;align-items:center;padding:8px 14px;border-bottom:1px solid var(--line)}
.au-nav .sp{flex:1}
.au-tab[aria-pressed="true"]{background:var(--accent);color:var(--accent-ink);border-color:var(--accent)}
#auModal .lesson{display:grid!important;max-height:none!important;overflow:visible;border:0;padding:4px 2px;grid-template-columns:minmax(0,1fr)}
#auModal .lesson h1{cursor:default;font-size:19px}
#auModal .lesson h1::after{content:''}
#auModal .lesson>*{display:revert}
#auModal .lesson p{max-width:none}
.au-busca{width:100%;margin:4px 0 8px}
.au-parte{font-weight:700;margin:14px 0 4px;color:var(--ink)}
.au-item{display:flex;gap:8px;align-items:center;width:100%;text-align:left;border:1px solid transparent;background:none;color:var(--ink);
  padding:7px 8px;border-radius:8px;cursor:pointer;font:inherit}
.au-item:hover{background:var(--panel2)}
.au-item.on{border-color:var(--accent);background:var(--panel2)}
.au-item .n{color:var(--ink2);min-width:2.2em;text-align:right;font-variant-numeric:tabular-nums}
.au-item .ok{margin-left:auto;color:#2BA36B}
.lesson p.usa{grid-column:1/-1;font-size:13px;color:var(--ink2)}
.lesson p.usa a{color:var(--accent);cursor:pointer;text-decoration:underline;text-underline-offset:2px}
.lesson p.eletiva{grid-column:1/-1;font-size:13px;background:rgba(43,163,107,.12);border:1px solid rgba(43,163,107,.45);border-radius:8px;padding:5px 10px}
.au-item .el{font-size:11px;color:#2BA36B;border:1px solid currentColor;border-radius:999px;padding:0 6px}
</style>
"""

HTML = r"""
<button id="aulaFab" type="button" title="Abrir a aula e a lista de aulas" aria-haspopup="dialog">📘 Aula</button>
<div class="modal" id="auModal" hidden role="dialog" aria-modal="true" aria-label="Aula"><div class="mbox">
  <div class="mh"><b id="auTit">📘 Aula</b><button class="btn" id="auClose" aria-label="Fechar">✕</button></div>
  <div class="au-nav">
    <button class="btn au-tab" id="auTabAula" aria-pressed="true">Esta aula</button>
    <button class="btn au-tab" id="auTabLista" aria-pressed="false">Todas as aulas</button>
    <span class="sp"></span>
    <button class="btn" id="auAnt" aria-label="Aula anterior">◀ Anterior</button>
    <button class="btn" id="auProx" aria-label="Próxima aula">Próxima ▶</button>
  </div>
  <div class="mb">
    <div id="auAula"></div>
    <div id="auLista" hidden>
      <input class="au-busca" id="auBusca" placeholder="Buscar aula…" aria-label="Buscar aula">
      <div id="auItens"></div>
    </div>
  </div></div></div>
"""

JS = r"""<script>
/* ===== Oficina 2: janela da aula (botão 📘 Aula) ===== */
(function(){
  function $(i){return document.getElementById(i)}
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
  function tit(L){return String(L.t).replace(/^\d+\.\s*/,'')}
  function feitas(){try{return JSON.parse(localStorage.getItem('oficina2.done')||'[]')}catch(e){return[]}}
  var casa=null,proximo=null,classes='';
  function sel(){return $('lessonSel')}
  function atual(){return sel()?sel().selectedIndex:0}
  // a caixa da aula vai para dentro da janela (os botões dela continuam funcionando) e volta ao fechar
  function traz(){var b=$('lessonBox');if(!b||b.parentNode===$('auAula'))return;casa=b.parentNode;proximo=b.nextSibling;classes=b.className;b.classList.remove('fold');b.classList.add('open');$('auAula').appendChild(b)}
  function devolve(){var b=$('lessonBox');if(!b||!casa||b.parentNode!==$('auAula'))return;casa.insertBefore(b,proximo);b.className=classes;try{window.dispatchEvent(new Event('resize'))}catch(e){}}
  function titulo(){var Ls=window.OF.LESSONS||[],L=Ls[atual()];$('auTit').textContent='📘 '+(L?(atual()+1)+'. '+tit(L):'Aula');$('auAnt').disabled=atual()<=0;$('auProx').disabled=atual()>=Ls.length-1}
  function aba(lista){$('auTabAula').setAttribute('aria-pressed',String(!lista));$('auTabLista').setAttribute('aria-pressed',String(lista));$('auAula').hidden=lista;$('auLista').hidden=!lista;if(lista){lista_();setTimeout(function(){var on=$('auItens').querySelector('.on');if(on)on.scrollIntoView({block:'center'})},30)}}
  function lista_(){var Ls=window.OF.LESSONS||[],P=window.OF.PARTS||[],f=feitas(),b=($('auBusca').value||'').trim().toLowerCase(),inicio={},h='';
    P.forEach(function(p){var k=Ls.findIndex(function(L){return tit(L)===p[0]});if(k>=0)inicio[k]=p[1]});
    Ls.forEach(function(L,i){var t=tit(L);if(inicio[i]&&!b)h+='<div class="au-parte">'+esc(inicio[i])+'</div>';
      if(b&&t.toLowerCase().indexOf(b)<0)return;
      h+='<button class="au-item'+(i===atual()?' on':'')+'" data-i="'+i+'"><span class="n">'+(i+1)+'</span><span>'+(L.leitura?'📖 ':'')+esc(t)+'</span>'+(f.indexOf(t)>=0?'<span class="ok">✓</span>':'')+'</button>'});
    $('auItens').innerHTML=h||'<p>Nenhuma aula encontrada.</p>'}
  function ir(i){var s=sel();if(!s||i<0||i>=s.options.length)return;s.selectedIndex=i;s.dispatchEvent(new Event('change',{bubbles:true}));setTimeout(titulo,50)}
  function abre(){traz();titulo();aba(false);$('auModal').hidden=false;$('auClose').focus()}
  function fecha(){$('auModal').hidden=true;devolve();$('aulaFab').focus()}
  var USA=__USA__;
  function parteDe(i){var Ls=window.OF.LESSONS||[],P=window.OF.PARTS||[],nome='';P.forEach(function(p){var k=Ls.findIndex(function(L){return tit(L)===p[0]});if(k>=0&&k<=i&&/^Parte /.test(p[1]))nome=p[1]});return nome}
  // a linha "Você vai usar" e o aviso de eletiva entram logo depois do título da aula
  function enfeita(){var b=$('lessonBox');if(!b||b.querySelector('.usa,.eletiva'))return;var h=b.querySelector('h1');if(!h)return;var Ls=window.OF.LESSONS||[],i=atual(),L=Ls[i];if(!L)return;
    var html='',us=USA[tit(L)]||[];
    if(us.length)html+='<p class="usa">🔗 Você vai usar: '+us.map(function(u){var k=Ls.findIndex(function(x){return tit(x)===u});return '<a data-ir="'+k+'">'+(k+1)+'. '+esc(u)+'</a>'}).join(' · ')+'</p>';
    if(/Eletiva/.test(parteDe(i)))html+='<p class="eletiva">🌿 Aula eletiva: as Partes 8 e 9 são um cardápio. Escolha as aulas que servem ao seu jogo, na ordem que quiser.</p>';
    if(html)h.insertAdjacentHTML('afterend',html)}
  function inicia(){if(!$('aulaFab'))return;
    var lb=$('lessonBox');if(lb){new MutationObserver(enfeita).observe(lb,{childList:true});enfeita();
      lb.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('[data-ir]');if(!a)return;e.preventDefault();e.stopPropagation();ir(+a.getAttribute('data-ir'))},true)}
    $('aulaFab').addEventListener('click',abre);$('auClose').addEventListener('click',fecha);
    $('auModal').addEventListener('click',function(e){if(e.target===$('auModal'))fecha()});
    document.addEventListener('keydown',function(e){if(e.key==='Escape'&&!$('auModal').hidden&&!document.querySelector('.modal:not(#auModal):not([hidden]),.le-modal:not([hidden])'))fecha()},true);
    $('auTabAula').addEventListener('click',function(){aba(false)});$('auTabLista').addEventListener('click',function(){aba(true)});
    $('auAnt').addEventListener('click',function(){ir(atual()-1);aba(false)});$('auProx').addEventListener('click',function(){ir(atual()+1);aba(false)});
    $('auBusca').addEventListener('input',lista_);
    $('auItens').addEventListener('click',function(e){var it=e.target.closest('[data-i]');if(!it)return;ir(+it.getAttribute('data-i'));aba(false)});
    if(sel())sel().addEventListener('change',function(){if(!$('auModal').hidden)setTimeout(titulo,50)})}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',inicia);else inicia();
})();
</script>
"""


def finish(src):
    return src + CSS + HTML + JS.replace('__USA__', json.dumps(trilha.USA, ensure_ascii=False))
