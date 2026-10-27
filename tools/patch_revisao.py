# Oficina Flutter 2 · 🧠 Revisão (perguntas de cada parte, com o melhor resultado guardado no navegador)
# e 📚 Glossário (termos com busca e link para a aula onde aparecem).
import json
from patch_engine import sub1
import revisao


def validar(lessons):
    titulos = {L['t'] for L in lessons.LESSONS}
    partes = {p[1] for p in lessons.PARTS}
    for t, d, aula in revisao.GLOSSARIO:
        assert aula in titulos, f'glossário: a aula "{aula}" ({t}) não existe'
    for parte, qs in revisao.REVISAO.items():
        assert parte in partes, f'revisão: a parte "{parte}" não existe'
        for q in qs:
            assert len(q) == 4 and 0 <= q[2] < len(q[1]), f'revisão: pergunta mal formada em {parte}: {q[0]}'


CSS = r"""<style>
.rv-q{border:1px solid var(--line);border-radius:10px;padding:10px 12px;margin:10px 0;background:var(--panel2)}
.rv-q p{margin:0 0 6px;font-weight:600}
.rv-q label{display:flex;gap:8px;align-items:flex-start;padding:4px 2px;cursor:pointer}
.rv-q.ok{border-color:#2BA36B}.rv-q.err{border-color:#E5484D}
.rv-exp{font-size:13px;color:var(--ink2);margin-top:4px}
.rv-res{font-weight:700;margin:8px 0}
.gl-it{border-bottom:1px solid var(--line);padding:8px 2px;display:flex;gap:10px;align-items:flex-start;justify-content:space-between}
.gl-it div{min-width:0}.gl-it b{display:block}.gl-it small{color:var(--ink2)}
.gl-it .btn{flex-shrink:0;font-size:12px}
</style>
"""

HTML = r"""
<div class="modal" id="rvModal" hidden role="dialog" aria-modal="true" aria-label="Revisão"><div class="mbox">
  <div class="mh"><b>🧠 Revisão da parte</b><button class="btn" id="rvClose" aria-label="Fechar">✕</button></div>
  <div class="mb">
    <div class="fx-row"><label>Parte <select id="rvParte"></select></label></div>
    <div id="rvLista"></div>
    <div class="fx-row"><button class="btn pri" id="rvConf">Conferir respostas</button><button class="btn" id="rvLimpa">Tentar de novo</button></div>
    <div class="rv-res" id="rvRes" role="status"></div>
  </div></div></div>
<div class="modal" id="glModal" hidden role="dialog" aria-modal="true" aria-label="Glossário"><div class="mbox">
  <div class="mh"><b>📚 Glossário</b><button class="btn" id="glClose" aria-label="Fechar">✕</button></div>
  <div class="mb">
    <div class="fx-row"><input id="glBusca" placeholder="Buscar termo ou palavra…" aria-label="Buscar no glossário"></div>
    <div id="glLista"></div>
  </div></div></div>
"""

JS = r"""<script>
/* ===== Oficina 2: revisão das partes e glossário ===== */
(function(){
  var REV=__REV__,GLO=__GLO__;
  function $(i){return document.getElementById(i)}
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
  function ls(k,d){try{var v=localStorage.getItem(k);return v?JSON.parse(v):d}catch(e){return d}}
  function lsSet(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}}
  function fechavel(id,btn){$(btn).addEventListener('click',function(){$(id).hidden=true});$(id).addEventListener('click',function(e){if(e.target===$(id))$(id).hidden=true});
    document.addEventListener('keydown',function(e){if(e.key==='Escape'&&!$(id).hidden)$(id).hidden=true})}
  function tit(L){return String(L.t).replace(/^\d+\.\s*/,'')}
  function parteAtual(){var Ls=window.OF.LESSONS||[],P=window.OF.PARTS||[],i=$('lessonSel')?$('lessonSel').selectedIndex:0,nome=null;
    P.forEach(function(p){var k=Ls.findIndex(function(L){return tit(L)===p[0]});if(k>=0&&k<=i&&/^Parte /.test(p[1]))nome=p[1]});return nome}
  function irPara(titulo){var Ls=window.OF.LESSONS||[],k=Ls.findIndex(function(L){return tit(L)===titulo});if(k<0)return;var s=$('lessonSel');s.selectedIndex=k;s.dispatchEvent(new Event('change',{bubbles:true}))}
  // as opções aparecem embaralhadas a cada tentativa (o valor guarda a posição original)
  function ordem(n){var o=[];for(var i=0;i<n;i++)o.push(i);for(var k=n-1;k>0;k--){var r=Math.floor(Math.random()*(k+1)),t=o[k];o[k]=o[r];o[r]=t}return o}
  function opcoes(){var best=ls('oficina2.revisao',{}),sel=$('rvParte'),v=sel.value;sel.innerHTML=Object.keys(REV).map(function(p){var b=best[p];return '<option value="'+esc(p)+'">'+esc(p)+(b!=null?' · melhor '+b+'/'+REV[p].length:'')+'</option>'}).join('');if(v)sel.value=v}
  function mostra(){var p=$('rvParte').value,qs=REV[p]||[];$('rvRes').textContent='';
    $('rvLista').innerHTML=qs.map(function(q,i){return '<div class="rv-q" data-i="'+i+'"><p>'+(i+1)+'. '+esc(q[0])+'</p>'+ordem(q[1].length).map(function(j){return '<label><input type="radio" name="rv'+i+'" value="'+j+'"> <span>'+esc(q[1][j])+'</span></label>'}).join('')+'<div class="rv-exp" hidden></div></div>'}).join('')}
  function confere(){var p=$('rvParte').value,qs=REV[p]||[],ok=0,falta=0;
    qs.forEach(function(q,i){var box=document.querySelector('.rv-q[data-i="'+i+'"]'),m=box.querySelector('input:checked'),ex=box.querySelector('.rv-exp');box.classList.remove('ok','err');
      if(!m){falta++;ex.hidden=true;return}var certo=+m.value===q[2];if(certo)ok++;box.classList.add(certo?'ok':'err');ex.hidden=false;ex.textContent=(certo?'✓ ':'✗ Resposta: '+q[1][q[2]]+'. ')+q[3]});
    if(falta){$('rvRes').textContent='Faltam '+falta+' pergunta(s).';return}
    var best=ls('oficina2.revisao',{});if(best[p]==null||ok>best[p]){best[p]=ok;lsSet('oficina2.revisao',best)}
    $('rvRes').textContent='Você acertou '+ok+' de '+qs.length+(ok===qs.length?'. Parte revisada! 🎉':'. Releia as aulas das erradas e tente de novo.');opcoes()}
  function glossario(){var b=($('glBusca').value||'').trim().toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,''),n=function(s){return String(s).toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'')};
    var it=GLO.filter(function(g){return !b||n(g[0]+' '+g[1]).indexOf(b)>=0}).sort(function(a,c){return a[0].localeCompare(c[0],'pt')});
    $('glLista').innerHTML=it.length?it.map(function(g){return '<div class="gl-it"><div><b>'+esc(g[0])+'</b><span>'+esc(g[1])+'</span><br><small>Aula: '+esc(g[2])+'</small></div><button class="btn" data-aula="'+esc(g[2])+'">Ver aula</button></div>'}).join(''):'<p>Nenhum termo encontrado.</p>'}
  function inicia(){if(!$('rvBtn'))return;
    fechavel('rvModal','rvClose');fechavel('glModal','glClose');
    $('rvBtn').addEventListener('click',function(){opcoes();var pa=parteAtual();if(pa&&REV[pa])$('rvParte').value=pa;mostra();$('rvModal').hidden=false});
    $('rvParte').addEventListener('change',mostra);$('rvConf').addEventListener('click',confere);$('rvLimpa').addEventListener('click',mostra);
    $('glBtn').addEventListener('click',function(){glossario();$('glModal').hidden=false;setTimeout(function(){$('glBusca').focus()},50)});
    $('glBusca').addEventListener('input',glossario);
    $('glLista').addEventListener('click',function(e){var a=e.target.closest('[data-aula]');if(!a)return;$('glModal').hidden=true;irPara(a.getAttribute('data-aula'))})}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',inicia);else inicia();
})();
</script>
"""


def patch(src):
    src = sub1(src,
        '<button class="btn" id="galBtn" title="Jogos da turma">🕹 Galeria</button>',
        '<button class="btn" id="galBtn" title="Jogos da turma">🕹 Galeria</button>'
        '<button class="btn" id="rvBtn" title="Perguntas de revisão da parte">🧠 Revisão</button>'
        '<button class="btn" id="glBtn" title="Termos de jogos com link para a aula">📚 Glossário</button>',
        'botoes revisao')
    return src


def finish(src):
    js = JS.replace('__REV__', json.dumps(revisao.REVISAO, ensure_ascii=False)).replace('__GLO__', json.dumps(revisao.GLOSSARIO, ensure_ascii=False))
    return src + CSS + HTML + js
