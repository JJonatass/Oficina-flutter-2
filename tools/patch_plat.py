# Oficina Flutter 2, frente 8: plataforma.
# - modo professor: resposta de cada etapa dos exercícios (antes → depois), com botão para aplicar no código
# - baixar o projeto Flutter: .zip com pubspec.yaml, lib/main.dart, sprites, sons (gravados em WAV) e mapas
# - instalar como app (PWA): manifest, service worker e ícones, para abrir sem internet
import json, pathlib
from patch_engine import sub1

ROOT = pathlib.Path(__file__).resolve().parent

CSS = r"""<style>
.stg .sb{font:inherit;font-size:12px;font-weight:500;padding:2px 8px;border:1px solid var(--accent);border-radius:999px;background:var(--accent-soft);color:var(--ink);cursor:pointer}
.stg .sol{flex-basis:100%;margin:2px 0 4px 28px;font-weight:400;font-size:12.5px;background:var(--panel2);border:1px solid var(--line);border-radius:8px;padding:8px 10px;color:var(--ink);display:flex;flex-direction:column;gap:6px;min-width:0}
.stg .sol pre{margin:0;padding:6px 8px;border-radius:6px;font:12px/1.45 'JetBrains Mono',ui-monospace,monospace;white-space:pre-wrap;word-break:break-word;max-height:180px;overflow:auto}
.stg .sol pre.an{background:rgba(196,43,59,.08);border-left:3px solid var(--err)}
.stg .sol pre.de{background:rgba(10,132,103,.08);border-left:3px solid var(--ok)}
.stg .sol .sr{display:flex;gap:6px;align-items:center;flex-wrap:wrap}
.stg .sol b{font-size:11.5px;text-transform:uppercase;letter-spacing:.04em;color:var(--ink2)}
.profsw{display:flex;gap:8px;align-items:center;margin:4px 0 10px}
#dlBtn[disabled]{opacity:.6}
</style>
"""

ENGINE_UI = r"""
/* ===== Oficina 2: modo professor (respostas) ===== */
function profOn(){try{return localStorage.getItem('oficina2.prof')==='1'}catch(e){return false}}
var solOpen=null;
function solHtml(L,i){var g=L.steps[i];if(!g||!g.sol)return '';
  return '<div class="sol">'+g.sol.map(function(p,k){return (g.sol.length>1?'<b>Troca '+(k+1)+' de '+g.sol.length+'</b>':'')+'<b>Antes</b><pre class="an">'+esc(p[0])+'</pre><b>Depois</b><pre class="de">'+esc(p[1])+'</pre>'}).join('')+
    '<div class="sr"><button class="btn pri" data-apl="'+i+'">Aplicar no código</button><span class="mt">Aplica as trocas no código que está no editor.</span></div></div>'}
function solAplicar(i){var L=OF.LESSONS[S.lesson],g=L&&L.steps&&L.steps[i];if(!g||!g.sol)return;var src=S.src,falta=0;
  g.sol.forEach(function(p){if(src.indexOf(p[0])>=0)src=src.replace(p[0],p[1]);else falta++});
  if(falta===g.sol.length){toast('O trecho do "antes" não está mais no código. Faça a troca à mão ou recomece a aula.');return}
  A.setCode(src);A.analyze();S.sel=null;renderAll(false);
  toast(falta?'Apliquei parte das trocas; '+falta+' trecho(s) já tinham mudado.':'Resposta aplicada no código.')}
"""

DL_JS = r"""<script>
/* ===== Oficina 2: baixar o projeto Flutter (.zip) ===== */
window.OF_WAV=function(d,sr){var n=d.length,out=new DataView(new ArrayBuffer(44+n*2));
  function str(o,s){for(var i=0;i<s.length;i++)out.setUint8(o+i,s.charCodeAt(i))}
  str(0,'RIFF');out.setUint32(4,36+n*2,true);str(8,'WAVE');str(12,'fmt ');out.setUint32(16,16,true);out.setUint16(20,1,true);out.setUint16(22,1,true);
  out.setUint32(24,sr,true);out.setUint32(28,sr*2,true);out.setUint16(32,2,true);out.setUint16(34,16,true);str(36,'data');out.setUint32(40,n*2,true);
  for(var i=0;i<n;i++){var v=Math.max(-1,Math.min(1,d[i]));out.setInt16(44+i*2,v<0?v*0x8000:v*0x7FFF,true)}
  return new Uint8Array(out.buffer)};
(function(){
  var crcT=null;
  function crc32(b){if(!crcT){crcT=new Uint32Array(256);for(var n=0;n<256;n++){var c=n;for(var k=0;k<8;k++)c=c&1?0xEDB88320^(c>>>1):c>>>1;crcT[n]=c>>>0}}var c=0xFFFFFFFF;for(var i=0;i<b.length;i++)c=crcT[(c^b[i])&255]^(c>>>8);return (c^0xFFFFFFFF)>>>0}
  function zipar(arqs){var enc=new TextEncoder(),partes=[],central=[],off=0;
    arqs.forEach(function(a){var nm=enc.encode(a.nome),d=a.dados,crc=crc32(d);
      var h=new DataView(new ArrayBuffer(30));h.setUint32(0,0x04034b50,true);h.setUint16(4,20,true);h.setUint16(6,0x0800,true);h.setUint16(12,0x21,true);h.setUint32(14,crc,true);h.setUint32(18,d.length,true);h.setUint32(22,d.length,true);h.setUint16(26,nm.length,true);
      partes.push(new Uint8Array(h.buffer),nm,d);
      var c=new DataView(new ArrayBuffer(46));c.setUint32(0,0x02014b50,true);c.setUint16(4,20,true);c.setUint16(6,20,true);c.setUint16(8,0x0800,true);c.setUint16(14,0x21,true);c.setUint32(16,crc,true);c.setUint32(20,d.length,true);c.setUint32(24,d.length,true);c.setUint16(28,nm.length,true);c.setUint32(42,off,true);
      central.push(new Uint8Array(c.buffer),nm);off+=30+nm.length+d.length});
    var tam=0;central.forEach(function(x){tam+=x.length});
    var e=new DataView(new ArrayBuffer(22));e.setUint32(0,0x06054b50,true);e.setUint16(8,arqs.length,true);e.setUint16(10,arqs.length,true);e.setUint32(12,tam,true);e.setUint32(16,off,true);
    return new Blob(partes.concat(central,[new Uint8Array(e.buffer)]),{type:'application/zip'})}
  function bytesDe(uri){var b64=String(uri).split(',')[1]||'',bin=atob(b64),u=new Uint8Array(bin.length);for(var i=0;i<bin.length;i++)u[i]=bin.charCodeAt(i);return u}
  function texto(s){return new TextEncoder().encode(s)}
  function slug(t){return String(t||'jogo').normalize('NFD').replace(/[̀-ͯ]/g,'').toLowerCase().replace(/[^a-z0-9]+/g,'_').replace(/^_+|_+$/g,'').replace(/^(\d)/,'jogo_$1').slice(0,40)||'jogo'}
  window.OF_PROJETO=function(code,titulo){
    var flame=/package:flame\//.test(code),arqs=[],pastas={},faltam=[],sons=[],musicas=[],pkgs={};
    var re=/import\s+'package:([a-z0-9_]+)\//g,m;while((m=re.exec(code)))if(m[1]!=='flutter')pkgs[m[1]]=1;
    function poe(caminho,dados){if(arqs.some(function(a){return a.nome===caminho}))return;arqs.push({nome:caminho,dados:dados});pastas[caminho.replace(/[^/]+$/,'')]=1}
    function sprite(base,destino){var k='assets/sprites/'+base,s=(window.OF_SPRITES||{})[k];if(s&&s.uri){poe(destino,bytesDe(s.uri));return true}return false}
    var refs={},rr=/['"]([\w\/.-]+\.(png|wav|mp3|tmx))['"]/g;while((m=rr.exec(code)))refs[m[1]]=m[2];
    Object.keys(refs).forEach(function(r){var ext=refs[r],base=r.split('/').pop();
      if(ext==='png'){var dest=/^assets\//.test(r)?r:(flame?'assets/images/'+base:'assets/sprites/'+base);if(!sprite(base,dest))faltam.push(r)}
      else if(ext==='tmx'){var M=window.OF_MAPS||{},t=M['assets/tiles/'+base]||M[r];if(t){poe('assets/tiles/'+base,texto(t));var ims=/<image[^>]*source="([^"]+)"/g,im;while((im=ims.exec(t))){var b=im[1].split('/').pop();sprite(b,'assets/images/'+b)||faltam.push(b)}}else faltam.push(r)}
      else{var nome=base.replace(/\.(wav|mp3)$/,''),dest2=/^assets\//.test(r)?r:(flame?'assets/audio/'+base:'assets/'+r.replace(/^\/+/,''));
        if(ext==='wav'&&(window.OF_SONS||[]).indexOf(nome)>=0)sons.push({nome:nome,dest:dest2});
        else if(ext==='mp3'&&(window.OF_MUSICAS||[]).indexOf(nome)>=0){var novo=r.replace(/\.mp3$/,'.wav');code=code.split("'"+r+"'").join("'"+novo+"'").split('"'+r+'"').join('"'+novo+'"');musicas.push({nome:nome,dest:dest2.replace(/\.mp3$/,'.wav')})}
        else faltam.push(r)}});
    var nomeApp=slug(titulo);
    var deps=Object.keys(pkgs).sort().map(function(p){return '  '+p+': any'}).join('\n');
    var ps=Object.keys(pastas).sort();
    var pub='name: '+nomeApp+'\ndescription: Jogo feito na Oficina Flutter 2.\npublish_to: none\nversion: 1.0.0+1\n\nenvironment:\n  sdk: ">=3.4.0 <4.0.0"\n\ndependencies:\n  flutter:\n    sdk: flutter\n'+(deps?deps+'\n':'')+
      '\nflutter:\n  uses-material-design: true\n'+(ps.length?'  assets:\n'+ps.map(function(p){return '    - '+p}).join('\n')+'\n':'');
    var leia='Projeto gerado pela Oficina Flutter 2 ('+titulo+').\n\nComo rodar no seu computador ou celular:\n  1. Descompacte esta pasta.\n  2. No terminal, dentro dela: flutter create .\n     (cria as pastas android, ios, web etc. sem apagar o lib/main.dart nem o pubspec.yaml)\n  3. flutter pub get\n  4. flutter run\n\n'+
      (Object.keys(pkgs).length?'Os pacotes ('+Object.keys(pkgs).join(', ')+') estão no pubspec.yaml com a versão "any": o flutter pub get escolhe a mais nova que funciona junto. O pub get grava as versões escolhidas no pubspec.lock: guarde esse arquivo junto com o projeto para todo mundo usar as mesmas. Se quiser travar no pubspec.yaml, troque "any" por ^ e o número que está no pubspec.lock (por exemplo flame: ^1.37.0).\n\n':'')+
      (sons.length?'Os efeitos sonoros foram gravados em WAV a partir do som sintetizado no navegador.\n':'')+
      (musicas.length?'As músicas foram gravadas em WAV (uma volta do tema, que emenda sem corte quando toca em loop), e no main.dart os nomes .mp3 viraram .wav. Para usar uma música sua, troque o arquivo mantendo o nome.\n':'')+
      (pkgs.sensors_plus?'\nsensors_plus no iPhone: acrescente NSMotionUsageDescription ao ios/Runner/Info.plist.\n':'')+
      (pkgs.supabase_flutter?'\nSupabase: troque url e anonKey no main.dart pelos do seu projeto (Project Settings > API) e crie as tabelas usadas no código.\n':'')+
      (pkgs.firebase_core||pkgs.cloud_firestore||pkgs.firebase_auth?'\nFirebase: rode flutterfire configure para gerar o firebase_options.dart do seu projeto.\n':'')+
      (faltam.length?'\nArquivos citados no código que não estão no simulador (acrescente à mão): '+faltam.join(', ')+'\n':'');
    var renders=sons.map(function(s){return (window.OF_SFX_WAV?window.OF_SFX_WAV(s.nome):Promise.resolve(null)).then(function(w){if(w)poe(s.dest,w);else faltam.push(s.dest)})})
      .concat(musicas.map(function(s){return (window.OF_MUSIC&&OF_MUSIC.render?OF_MUSIC.render(s.nome):Promise.resolve(null)).then(function(w){if(w)poe(s.dest,w);else faltam.push(s.dest)})}));
    return Promise.all(renders).then(function(){
      ps=Object.keys(pastas).sort();
      pub=pub.replace(/\nflutter:[\s\S]*$/,'\nflutter:\n  uses-material-design: true\n'+(ps.length?'  assets:\n'+ps.map(function(p){return '    - '+p}).join('\n')+'\n':''));
      var base=nomeApp+'/';
      var todos=[{nome:base+'pubspec.yaml',dados:texto(pub)},{nome:base+'lib/main.dart',dados:texto(code)},{nome:base+'LEIA-ME.txt',dados:texto(leia)}]
        .concat(arqs.map(function(a){return{nome:base+a.nome,dados:a.dados}}));
      return{nome:nomeApp+'.zip',blob:zipar(todos),arquivos:todos.map(function(a){return a.nome})}})};
  var b=document.getElementById('dlBtn');
  function aviso(m,ms){var t=document.getElementById('toast');if(!t)return;t.textContent=m;t.classList.add('on');clearTimeout(t._t);t._t=setTimeout(function(){t.classList.remove('on')},ms||4200)}
  /* dentro do Claude, o download passa pela permissão downloads do artefato */
  var dlCap=null;try{if(window.claude&&typeof window.claude.use==='function')window.claude.use('downloads').then(function(d){dlCap=d}).catch(function(){})}catch(e){}
  if(b)b.addEventListener('click',function(){
    var dentro=window.self!==window.top;
    if(dentro&&!dlCap){aviso('Aqui dentro o navegador não deixa baixar arquivos. Abra oficina-flutter-2.vercel.app e use ⬇ Projeto lá.',5000);return}
    var L=(window.OF.LESSONS||[])[(window.OF.A&&OF.A.S||{}).lesson]||{},src=(OF.A&&OF.A.S&&OF.A.S.src)||'';
    b.disabled=true;
    window.OF_PROJETO(src,String(L.t||'jogo').replace(/^\d+\.\s*/,'')).then(function(r){
      var info=r.nome+' ('+r.arquivos.length+' arquivos). Veja o LEIA-ME.txt dentro do .zip.';
      if(dlCap)return dlCap.save({filename:r.nome,data:r.blob}).then(function(){aviso('Salvo: '+info)},function(e){
        var c=e&&e.code;if(c==='declined')aviso('Download cancelado.');else if(c==='rate_limited')aviso('Já há um pedido de download aberto. Tente de novo em instantes.');
        else aviso('Não deu para salvar aqui ('+(c||'erro')+'). Abra oficina-flutter-2.vercel.app e use ⬇ Projeto lá.',5000)});
      var a=document.createElement('a'),u=URL.createObjectURL(r.blob);a.href=u;a.download=r.nome;document.body.appendChild(a);a.click();setTimeout(function(){URL.revokeObjectURL(u);a.remove()},4000);
      aviso('Baixando '+info);
    }).catch(function(e){aviso('Não consegui montar o .zip: '+e.message,6000)}).then(function(){b.disabled=false})});
})();
/* ===== Oficina 2: instalar como app (PWA) ===== */
(function(){try{if('serviceWorker' in navigator&&location.protocol==='https:'&&window.top===window.self&&/vercel\.app$|github\.io$|localhost$/.test(location.hostname))navigator.serviceWorker.register('sw.js')}catch(e){}})();
</script>
"""

SFX_WAV = r"""
  window.OF_SFX_WAV=function(nome){
    if(!SFX[nome]||typeof OfflineAudioContext==='undefined')return Promise.resolve(null);
    var sr=22050,off=new OfflineAudioContext(1,Math.ceil(sr*1.4),sr),old=ctx;ctx=off;
    try{SFX[nome](0.01,1)}finally{ctx=old}
    return off.startRendering().then(function(buf){
      var d=buf.getChannelData(0),fim=d.length;while(fim>1&&Math.abs(d[fim-1])<0.0005)fim--;fim=Math.min(d.length,fim+Math.round(sr*0.03));
      var n=fim,out=new DataView(new ArrayBuffer(44+n*2));
      function str(o,s){for(var i=0;i<s.length;i++)out.setUint8(o+i,s.charCodeAt(i))}
      str(0,'RIFF');out.setUint32(4,36+n*2,true);str(8,'WAVE');str(12,'fmt ');out.setUint32(16,16,true);out.setUint16(20,1,true);out.setUint16(22,1,true);
      out.setUint32(24,sr,true);out.setUint32(28,sr*2,true);out.setUint16(32,2,true);out.setUint16(34,16,true);str(36,'data');out.setUint32(40,n*2,true);
      for(var i=0;i<n;i++){var v=Math.max(-1,Math.min(1,d[i]));out.setInt16(44+i*2,v<0?v*0x8000:v*0x7FFF,true)}
      return new Uint8Array(out.buffer)})};
"""


def patch(src):
    # respostas no quadro de etapas da aula
    src = sub1(src, "var goalsDone=false,hintOpen=null;", ENGINE_UI + "var goalsDone=false,hintOpen=null;", 'prof ui fn')
    src = sub1(src,
        "+(i===cur&&g.h&&op?'<div class=\"ht\">'+esc(g.h)+'</div>':'')+'</li>'}).join('')+'</ol>';",
        "+(i===cur&&g.h&&op?'<div class=\"ht\">'+esc(g.h)+'</div>':'')+(profOn()&&g.sol?'<button class=\"sb\" data-s=\"'+i+'\" aria-expanded=\"'+(solOpen===S.lesson+':'+i)+'\">📝 Resposta</button>'+(solOpen===S.lesson+':'+i?solHtml(L,i):''):'')+'</li>'}).join('')+'</ol>';",
        'prof goal html')
    src = sub1(src,
        "$('lessonBox').addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('#goalBox .hb');",
        "$('lessonBox').addEventListener('click',function(e){var sb=e.target.closest&&e.target.closest('#goalBox .sb');if(sb){var sk=S.lesson+':'+sb.dataset.s;solOpen=solOpen===sk?null:sk;updateGoals();return}"
        "var ap=e.target.closest&&e.target.closest('#goalBox [data-apl]');if(ap){solAplicar(+ap.dataset.apl);return}"
        "var b=e.target.closest&&e.target.closest('#goalBox .hb');", 'prof goal click')
    # passos com a resposta (4º elemento)
    src = sub1(src, "L.steps=st.map(function(s){return {t:s[0],h:s[1],re:s[2]}})", "L.steps=st.map(function(s){return {t:s[0],h:s[1],re:s[2],sol:s[3]||null}})", 'steps sol')
    # respostas no painel de exercícios (modo professor)
    src = sub1(src, "+(g.h&&!s[j]?'<div class=\"ht\">💡 '+esc(g.h)+'</div>':'')+'</li>'}).join('')",
        "+(g.h&&!s[j]?'<div class=\"ht\">💡 '+esc(g.h)+'</div>':'')+(profOn()&&g.sol?'<div class=\"ht\">📝 '+g.sol.map(function(p){return '<code>'+esc(p[0].length>80?p[0].slice(0,80)+'…':p[0])+'</code> → <code>'+esc(p[1].length>120?p[1].slice(0,120)+'…':p[1])+'</code>'}).join('<br>')+'</div>':'')+'</li>'}).join('')",
        'prof ex modal')
    # chave no painel do professor
    src = sub1(src, "   <h3>Turma</h3>",
        "   <h3>Respostas</h3>\n   <label class=\"profsw\"><input type=\"checkbox\" id=\"profSol\"> Mostrar a resposta de cada etapa dos exercícios (botão 📝 Resposta)</label>\n   <h3>Turma</h3>", 'prof sol switch')
    src = sub1(src, "$('profBtn').addEventListener('click',function(){$('profModal').hidden=false;",
        "$('profSol').addEventListener('change',function(){try{localStorage.setItem('oficina2.prof',this.checked?'1':'0')}catch(e){}solOpen=null;updateGoals();toast(this.checked?'Respostas visíveis nos exercícios.':'Respostas escondidas.')});\n"
        "$('profBtn').addEventListener('click',function(){$('profSol').checked=profOn();$('profModal').hidden=false;", 'prof sol load')
    # botão de baixar o projeto
    src = sub1(src, '  <button class="btn" id="sprBtn"',
        '  <button class="btn" id="dlBtn" title="Baixar o projeto Flutter desta aula (.zip com pubspec.yaml, lib/main.dart e os arquivos usados)">⬇ Projeto</button>\n  <button class="btn" id="sprBtn"', 'dl btn')
    # sons gravados em WAV para o .zip
    src = sub1(src, "  window.OF_SFX=function(nome,vol){", SFX_WAV + "  window.OF_SFX=function(nome,vol){", 'sfx wav')
    # PWA
    src = sub1(src, '<link rel="preconnect" href="https://fonts.googleapis.com">\n',
        '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="manifest" href="manifest.webmanifest">\n<meta name="theme-color" content="#0B64D8">\n'
        '<link rel="icon" type="image/png" sizes="192x192" href="icone-192.png">\n<link rel="apple-touch-icon" href="icone-180.png">\n'
        '<meta name="apple-mobile-web-app-capable" content="yes">\n<meta name="mobile-web-app-capable" content="yes">\n', 'pwa head')
    return src


def finish(src):
    return src + CSS + DL_JS


SW = r"""/* Oficina Flutter 2: service worker. Guarda a página e as fontes para abrir sem internet. */
const VERSAO = '__VERSAO__';
const CACHE = 'oficina2-' + VERSAO;
const BASE = ['./', 'index.html', 'manifest.webmanifest', 'icone-192.png', 'icone-512.png', 'icone-180.png'];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(BASE)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', (e) => {
  e.waitUntil(caches.keys().then((ks) => Promise.all(ks.filter((k) => k.startsWith('oficina2-') && k !== CACHE).map((k) => caches.delete(k)))).then(() => self.clients.claim()));
});

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (req.mode === 'navigate' || (url.origin === location.origin && BASE.some((b) => url.pathname.endsWith(b.replace('./', '/'))))) {
    // página: rede primeiro (para pegar a versão nova); sem rede, a cópia guardada
    e.respondWith(fetch(req).then((r) => { const cp = r.clone(); caches.open(CACHE).then((c) => c.put(req, cp)); return r; })
      .catch(() => caches.match(req).then((r) => r || caches.match('index.html'))));
    return;
  }
  if (/fonts\.(googleapis|gstatic)\.com$/.test(url.hostname)) {
    // fontes: cópia guardada primeiro
    e.respondWith(caches.match(req).then((r) => r || fetch(req).then((resp) => { const cp = resp.clone(); caches.open(CACHE).then((c) => c.put(req, cp)); return resp; })));
  }
});
"""


def write_pwa(out_dir, versao):
    from PIL import Image
    out_dir = pathlib.Path(out_dir)
    man = {
        'name': 'Oficina Flutter 2 · Jogos',
        'short_name': 'Oficina 2',
        'description': 'Simulador de Flutter no navegador com a trilha de jogos 2D.',
        'start_url': './',
        'scope': './',
        'display': 'standalone',
        'background_color': '#EEF1F5',
        'theme_color': '#0B64D8',
        'lang': 'pt-BR',
        'icons': [
            {'src': 'icone-192.png', 'sizes': '192x192', 'type': 'image/png', 'purpose': 'any'},
            {'src': 'icone-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'any maskable'},
        ],
    }
    (out_dir / 'manifest.webmanifest').write_text(json.dumps(man, ensure_ascii=False, indent=1), encoding='utf-8')
    (out_dir / 'sw.js').write_text(SW.replace('__VERSAO__', versao), encoding='utf-8')
    heroi = Image.open(ROOT / 'sprites' / 'heroi.png').crop((0, 0, 16, 16))
    for tam in (180, 192, 512):
        img = Image.new('RGBA', (tam, tam), (11, 100, 216, 255))
        lado = int(tam * 0.62) // 16 * 16
        cao = heroi.resize((lado, lado), Image.NEAREST)
        img.alpha_composite(cao, ((tam - lado) // 2, (tam - lado) // 2 + tam // 24))
        img.save(out_dir / f'icone-{tam}.png', optimize=True)
