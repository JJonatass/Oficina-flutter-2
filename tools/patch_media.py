# Frente 3 da Oficina Flutter 2: mídia para jogos.
# - sprites próprios embutidos (assets/sprites/*.png), rootBundle + decodeImageFromList / ui.instantiateImageCodec,
#   canvas.drawImage e drawImageRect, Image.asset com os sprites
# - som: AudioPlayer + AssetSource (audioplayers) e SystemSound, com efeitos sintetizados no navegador
# - texto no Canvas: contorno, sombra, itálico, espaçamento, fonte (inclui GoogleFonts) e largura medida de verdade
import base64, json, pathlib
from patch_engine import sub1

ROOT = pathlib.Path(__file__).resolve().parent

SONS = ['pulo', 'osso', 'latido', 'batida', 'explosao', 'tiro', 'vitoria', 'derrota', 'clique', 'dano', 'poder']


def sprites_js():
    man = json.loads((ROOT / 'sprites' / 'manifest.json').read_text())
    data = {}
    for m in man:
        uri = 'data:image/png;base64,' + base64.b64encode((ROOT / 'sprites' / (m['nome'] + '.png')).read_bytes()).decode()
        data[m['caminho']] = {'w': m['largura'], 'h': m['altura'], 'q': m['quadros'], 'desc': m['desc'], 'uri': uri}
    return data


GLOBAL = r"""/* ===== Oficina 2: sprites embutidos e efeitos sonoros ===== */
window.OF_SPRITES=__SPRITES__;
window.OF_SPRITE_IMG={};
Object.keys(window.OF_SPRITES).forEach(function(k){var im=new Image();im.decoding='async';im.src=window.OF_SPRITES[k].uri;window.OF_SPRITE_IMG[k]=im});
window.OF_SONS=__SONS__;
(function(){
  var ctx=null,mudo=false;
  try{mudo=localStorage.getItem('oficina2.mudo')==='1'}catch(e){}
  function ac(){if(!ctx){var C=window.AudioContext||window.webkitAudioContext;if(!C)return null;ctx=new C()}if(ctx.state==='suspended')ctx.resume();return ctx}
  function tom(t0,tipo,f0,f1,dur,vol){var c=ctx,o=c.createOscillator(),g=c.createGain();o.type=tipo;o.frequency.setValueAtTime(f0,t0);if(f1!==f0)o.frequency.exponentialRampToValueAtTime(Math.max(20,f1),t0+dur);
    g.gain.setValueAtTime(0.0001,t0);g.gain.exponentialRampToValueAtTime(vol,t0+0.008);g.gain.exponentialRampToValueAtTime(0.0001,t0+dur);o.connect(g);g.connect(c.destination);o.start(t0);o.stop(t0+dur+0.02)}
  function ruido(t0,dur,vol,f0,f1){var c=ctx,n=Math.floor(c.sampleRate*dur),b=c.createBuffer(1,n,c.sampleRate),d=b.getChannelData(0);for(var i=0;i<n;i++)d[i]=Math.random()*2-1;
    var s=c.createBufferSource(),fl=c.createBiquadFilter(),g=c.createGain();s.buffer=b;fl.type='lowpass';fl.frequency.setValueAtTime(f0,t0);fl.frequency.exponentialRampToValueAtTime(f1,t0+dur);
    g.gain.setValueAtTime(vol,t0);g.gain.exponentialRampToValueAtTime(0.0001,t0+dur);s.connect(fl);fl.connect(g);g.connect(c.destination);s.start(t0);s.stop(t0+dur)}
  var SFX={
    pulo:function(t,v){tom(t,'square',260,720,0.16,0.18*v)},
    latido:function(t,v){[0,0.16].forEach(function(d){tom(t+d,'sawtooth',540,260,0.11,0.16*v);ruido(t+d,0.08,0.12*v,2200,600)})},
    osso:function(t,v){tom(t,'square',988,988,0.07,0.15*v);tom(t+0.07,'square',1319,1319,0.22,0.15*v)},
    moeda:function(t,v){tom(t,'square',988,988,0.07,0.15*v);tom(t+0.07,'square',1319,1319,0.22,0.15*v)},
    batida:function(t,v){ruido(t,0.12,0.5*v,1800,300);tom(t,'sine',160,60,0.12,0.4*v)},
    explosao:function(t,v){ruido(t,0.6,0.6*v,2400,120);tom(t,'sine',90,40,0.5,0.4*v)},
    tiro:function(t,v){tom(t,'square',1200,180,0.13,0.12*v)},
    vitoria:function(t,v){[523,659,784,1047].forEach(function(f,i){tom(t+i*0.09,'square',f,f,0.16+(i===3?0.2:0),0.13*v)})},
    derrota:function(t,v){tom(t,'sawtooth',420,90,0.7,0.14*v)},
    clique:function(t,v){tom(t,'square',1600,1600,0.025,0.08*v)},
    dano:function(t,v){tom(t,'square',240,70,0.22,0.16*v);ruido(t,0.08,0.25*v,1200,400)},
    poder:function(t,v){[392,523,659,784,1047,1319].forEach(function(f,i){tom(t+i*0.05,'triangle',f,f,0.09,0.2*v)})}
  };
  window.OF_SFX=function(nome,vol){if(mudo||!SFX[nome])return;var c=ac();if(!c)return;try{SFX[nome](c.currentTime+0.005,vol==null?1:Math.max(0,Math.min(1,vol)))}catch(e){}};
  window.OF_SFX_MUDO=function(m){if(m!==undefined){mudo=!!m;try{localStorage.setItem('oficina2.mudo',mudo?'1':'0')}catch(e){}if(mudo&&window.OF_MUSIC)window.OF_MUSIC.stopAll()}return mudo};
  window.OF_AC=ac;window.OF_EH_MUDO=function(){return mudo};
  /* o navegador só libera áudio depois de um gesto: o primeiro toque ou tecla destrava o contexto */
  ['pointerdown','keydown'].forEach(function(n){window.addEventListener(n,function(){if(!mudo)ac()},{capture:true})});
})();
"""

ENGINE = r"""/* ===== Oficina 2: imagens (ui.Image) e áudio ===== */
function spriteOf(path){var s=window.OF_SPRITES&&window.OF_SPRITES[String(path)];
  if(!s)throw exc('Unable to load asset: "'+path+'". O simulador tem estes sprites: '+Object.keys(window.OF_SPRITES||{}).join(', '));return s}
function mkImg(path){var s=spriteOf(path);return{nat:'Img',path:String(path),f:{width:s.w,height:s.h},src:"Image('"+path+"')"}}
function somOf(path){var p=String(path==null?'':path),m=/([\w-]+)\.(?:wav|mp3|ogg|m4a|aac)$/i.exec(p),n=m?m[1]:p;
  if(n!=='moeda'&&(window.OF_SONS||[]).indexOf(n)<0&&(window.OF_MUSICAS||[]).indexOf(n)<0)throw exc('Unable to load asset: "'+p+'". O simulador tem estes sons: '+(window.OF_SONS||[]).map(function(s){return 'sons/'+s+'.wav'}).join(', ')+' e estas músicas: '+(window.OF_MUSICAS||[]).map(function(s){return 'sons/'+s+'.mp3'}).join(', '));return n}
function isMusica(n){return (window.OF_MUSICAS||[]).indexOf(n)>=0}
function audioPlay(v,n,vol){if(v.au.h!=null&&window.OF_MUSIC){window.OF_MUSIC.stop(v.au.h);v.au.h=null}if(isMusica(n)){if(window.OF_MUSIC)v.au.h=window.OF_MUSIC.play(n,vol,!!v.au.loop);return}if(v.au.loop&&window.OF_MUSIC){v.au.h=window.OF_MUSIC.playSfxLoop(n,vol);return}sfx(n,vol)}
function assetOk(path){var p=String(path);if(window.OF_SPRITES&&window.OF_SPRITES[p])return true;try{somOf(p);return true}catch(e){return false}}
function sfx(n,v){if((window.OF_MUSICAS||[]).indexOf(n)>=0){if(window.OF_MUSIC)window.OF_MUSIC.play(n,v,false);return}if(window.OF_SFX)window.OF_SFX(n,v)}
"""

NAT = r"""  if(v.nat==='#vsync'){
    /* `this` dentro do State (por exemplo Cena(sprites!, this)): campos, getters e métodos do State */
    if(ST.fields[name])return ST.fields[name].value;
    if(ST.sgetters&&hasOwn(ST.sgetters,name)){var sgx=ST.sgetters[name],sgy=mkEnv({});if(sgx.arrow)return ev(pTern(new Ps(sgx.body)),sgy);stmt(new Ps(sgx.body),sgy,true);return sgy.ret}
    if(ST.methods[name])return runMethod(ST.methods[name],args,null);
    if(name==='mounted')return true}
  if(v.nat==='Bundle'){
    switch(name){
      case 'load':{var bp=String(args[0]);if(!assetOk(bp))spriteOf(bp);return{nat:'ByteData',path:bp,f:{},src:'ByteData'}}
      case 'loadString':throw exc('Unable to load asset: "'+args[0]+'". No simulador, rootBundle só carrega os sprites e sons prontos.')}}
  if(v.nat==='ByteData'){switch(name){case 'buffer':return v;case 'asUint8List':case 'asByteData':return{nat:'Bytes',path:v.path,f:{},src:'Uint8List'};case 'lengthInBytes':return 1024}}
  if(v.nat==='Bytes'){switch(name){case 'length':case 'lengthInBytes':return 1024;case 'buffer':return{nat:'ByteData',path:v.path,f:{},src:'ByteBuffer'}}}
  if(v.nat==='UiNS'){
    switch(name){
      case 'instantiateImageCodec':return{nat:'Codec',path:args[0]&&args[0].path,f:{},src:'Codec'};
      case 'decodeImageFromList':return mkImg(args[0]&&args[0].path);
      case 'Image':return null}}
  if(v.nat==='Codec'){switch(name){case 'getNextFrame':return{nat:'FrameInfo',path:v.path,f:{},src:'FrameInfo'};case 'frameCount':return 1;case 'repetitionCount':return 0;case 'dispose':return null}}
  if(v.nat==='FrameInfo'){switch(name){case 'image':return mkImg(v.path);case 'duration':return{raw:'Duration(milliseconds: 0)'}}}
  if(v.nat==='Img'){switch(name){case 'width':return v.f.width;case 'height':return v.f.height;case 'dispose':return null;case 'clone':return v;case 'debugDisposed':return false}}
  if(v.nat==='AssetSource'){if(name==='path')return v.path}
  if(v.nat==='Audio'){
    var an2=ARGN||[],nm2={};args.forEach(function(x,i){if(an2[i])nm2[an2[i]]=x});
    switch(name){
      case 'play':{var srcA=args[0];if(!srcA||srcA.nat!=='AssetSource')throw exc('No simulador, play() toca só AssetSource com os sons prontos (por exemplo AssetSource(\'sons/pulo.wav\')).');
        var vol=nm2.volume!==undefined?nn(nm2.volume):v.au.vol;v.au.src=srcA;audioPlay(v,somOf(srcA.path),vol);return null}
      case 'setSource':case 'setSourceAsset':{var s2=args[0];if(s2&&s2.nat==='AssetSource'){somOf(s2.path);v.au.src=s2}else if(typeof s2==='string'){somOf(s2);v.au.src={nat:'AssetSource',path:s2}}return null}
      case 'resume':if(v.au.h!=null&&window.OF_MUSIC&&window.OF_MUSIC.resume(v.au.h))return null;if(v.au.src)audioPlay(v,somOf(v.au.src.path),v.au.vol);return null;
      case 'setVolume':v.au.vol=Math.max(0,Math.min(1,nn(args[0])));if(v.au.h!=null&&window.OF_MUSIC)window.OF_MUSIC.setVolume(v.au.h,v.au.vol);return null;
      case 'setReleaseMode':v.au.loop=/loop/.test(pcol(args[0])||'');return null;
      case 'pause':if(v.au.h!=null&&window.OF_MUSIC)window.OF_MUSIC.pause(v.au.h);return null;
      case 'stop':case 'dispose':case 'release':if(v.au.h!=null&&window.OF_MUSIC){window.OF_MUSIC.stop(v.au.h);v.au.h=null}return null;
      case 'volume':return new Dbl(v.au.vol);
      case 'seek':case 'setPlaybackRate':case 'setPlayerMode':case 'setBalance':return null}}
"""

CANVAS_IMG = r"""        case 'drawImage':{var im=args[0];if(!im||im.nat!=='Img')throw exc('drawImage precisa de um ui.Image carregado');
          var iw=nn(im.f.width),ih=nn(im.f.height),fq0=args[2]&&args[2].f?pcol(args[2].f.filterQuality)||'':'';
          add({k:'img',path:im.path,s:[0,0,iw,ih],d:[nn(args[1].f.dx),nn(args[1].f.dy),iw,ih],fq:fq0},args[2]);return null}
        case 'drawImageRect':{var im2=args[0];if(!im2||im2.nat!=='Img')throw exc('drawImageRect precisa de um ui.Image carregado');
          var sr=args[1].f,dr=args[2].f,fq1=args[3]&&args[3].f?pcol(args[3].f.filterQuality)||'':'';
          add({k:'img',path:im2.path,s:[nn(sr.left),nn(sr.top),nn(sr.width),nn(sr.height)],d:[nn(dr.left),nn(dr.top),nn(dr.width),nn(dr.height)],fq:fq1},args[3]);return null}
"""

TPINFO = r"""var TPM=null;
function gfFamily(n){var G={pressStart2p:'Press Start 2P',silkscreen:'Silkscreen',vt323:'VT323',bungee:'Bungee'};return G[n]||n.replace(/([a-z])([A-Z0-9])/g,'$1 $2').replace(/^./,function(c){return c.toUpperCase()})}
function fontFam(ff){ff=String(ff||'').trim().replace(/^['"]|['"]$/g,'');if(!ff)return 'Roboto,Arial,sans-serif';
  if(/^press\s*start\s*2p$|^pressstart2p$/i.test(ff))ff='Press Start 2P';else if(/^vt\s*323$/i.test(ff))ff='VT323';
  if(/mono|courier|consolas/i.test(ff))return "'JetBrains Mono',ui-monospace,monospace";
  return "'"+ff.replace(/'/g,'')+"',Roboto,Arial,sans-serif"}
function tpInfo(tp){
  var raw=pcol(tp.f.text)||'',tm=/text:\s*('((?:[^'\\]|\\.)*)'|"((?:[^"\\]|\\.)*)")/.exec(raw);
  var txt=tm?(tm[2]!==undefined?tm[2]:tm[3]).replace(/\\n/g,'\n').replace(/\\(.)/g,'$1'):'';
  var shm=/shadows:\s*\[\s*Shadow\(([^()]*(?:\([^()]*\)[^()]*)*)\)/.exec(raw),shadow=null;
  if(shm){var sc=/color:\s*([\w.]+(?:\([^)]*\))?)/.exec(shm[1]),so=/Offset\(\s*(-?[\d.]+)\s*,\s*(-?[\d.]+)\s*\)/.exec(shm[1]),sb=/blurRadius:\s*([\d.]+)/.exec(shm[1]);
    shadow={color:sc?sc[1]:'Colors.black',dx:so?+so[1]:0,dy:so?+so[2]:0,blur:sb?+sb[1]:0}}
  var fg=/foreground:\s*Paint\(\)\.\.color = ([\s\S]*?)\.\.style = PaintingStyle\.(\w+)\.\.strokeWidth = (-?[\d.]+)/.exec(raw),stroke=null;
  var clean=raw.replace(/shadows:\s*\[[\s\S]*?\]\s*(?=[,)])/,'').replace(/foreground:\s*Paint\(\)[^,)]*(?:\([^)]*\))?[^,)]*/,'');
  var fs=/fontSize:\s*([\d.]+)/.exec(clean),cl=/color:\s*([\w.]+(?:\([^)]*\))?)/.exec(clean),fw=/fontWeight:\s*FontWeight\.(\w+)/.exec(clean);
  if(fg){if(fg[2]==='stroke')stroke={color:fg[1].trim(),w:+fg[3]||1};else cl=[0,fg[1].trim()]}
  var gf=/GoogleFonts\.(\w+)\(/.exec(raw),fm=/fontFamily:\s*(?:'([^']*)'|"([^"]*)")/.exec(raw);
  var fam=fontFam(gf?gfFamily(gf[1]):fm?(fm[1]!==undefined?fm[1]:fm[2]):'');
  var size=fs?+fs[1]:14,bold=!!(fw&&/bold|w[6-9]00/.test(fw[1])),italic=/fontStyle:\s*FontStyle\.italic/.test(raw),lsm=/letterSpacing:\s*(-?[\d.]+)/.exec(raw),ls=lsm?+lsm[1]:0;
  var font=(italic?'italic ':'')+(bold?'700 ':'400 ')+size+'px '+fam,lines=txt.split('\n'),w=0;
  try{if(!TPM)TPM=document.createElement('canvas').getContext('2d');TPM.font=font;lines.forEach(function(l){w=Math.max(w,TPM.measureText(l).width+ls*l.length)})}
  catch(e){w=lines.reduce(function(m,l){return Math.max(m,l.length)},0)*size*.55}
  return{text:txt,size:size,color:cl?cl[1]:'Colors.black',bold:bold,italic:italic,ls:ls,fam:fam,font:font,shadow:shadow,stroke:stroke,w:w,h:lines.length*size*1.2}}
"""

CANVAS_DRAW_IMG = r"""      case 'img':{var im=window.OF_SPRITE_IMG&&window.OF_SPRITE_IMG[o.path];if(!im||!im.complete||!im.naturalWidth)break;
        g.imageSmoothingEnabled=/low|medium|high/.test(o.fq||'');var am=/rgba\([^)]*,\s*([\d.]+)\)/.exec(col);if(am)g.globalAlpha=+am[1];
        g.drawImage(im,o.s[0],o.s[1],o.s[2],o.s[3],o.d[0],o.d[1],o.d[2],o.d[3]);break}
      case 'text':{var ti=o.ti;if(!ti){g.fillStyle=css(o.color);g.font=(o.bold?'700 ':'')+o.size+'px Roboto,Arial,sans-serif';g.textBaseline='top';
          String(o.text).split('\n').forEach(function(t,i){g.fillText(t,o.x,o.y+i*o.size*1.2)});break}
        g.font=ti.font;g.textBaseline='top';try{g.letterSpacing=ti.ls+'px'}catch(e){}
        if(ti.shadow){g.shadowColor=css(ti.shadow.color);g.shadowOffsetX=ti.shadow.dx*dpr;g.shadowOffsetY=ti.shadow.dy*dpr;g.shadowBlur=ti.shadow.blur*dpr}
        var tl=String(ti.text).split('\n');
        if(ti.stroke){g.strokeStyle=css(ti.stroke.color);g.lineWidth=ti.stroke.w;g.lineJoin='round';tl.forEach(function(t,i){g.strokeText(t,o.x,o.y+i*ti.size*1.2)})}
        else{g.fillStyle=css(ti.color);tl.forEach(function(t,i){g.fillText(t,o.x,o.y+i*ti.size*1.2)})}
        break}
"""


def patch(src):
    sp = json.dumps(sprites_js(), ensure_ascii=False)
    src = sub1(src, "<script>\n(function(){\n'use strict';\n/* ====== Esquema dos widgets ====== */",
               "<script>\n" + GLOBAL.replace('__SPRITES__', sp).replace('__SONS__', json.dumps(SONS)) +
               "</script>\n<script>\n(function(){\n'use strict';\n/* ====== Esquema dos widgets ====== */", 'global media')
    # fontes de jogo para Text e TextPainter (GoogleFonts.pressStart2p etc.)
    src = sub1(src, "family=Roboto:wght@400;500;700&display=swap",
               "family=Roboto:wght@400;500;700&family=Press+Start+2P&family=Silkscreen&family=VT323&family=Bungee&display=swap", 'fonts')

    src = sub1(src, "function mkDur(ms){", ENGINE + "function mkDur(ms){", 'media engine')
    # import 'dart:ui' as ui: tipos como ui.Image viram Image na análise (o interpretador não usa os tipos)
    src = sub1(src,
        "ST.extract=function(src){src=stripComments(src);",
        "ST.extract=function(src){src=stripComments(src);var ual=/import\\s+['\"]dart:ui['\"]\\s+as\\s+(\\w+)/.exec(src);ST.uiAlias=ual?ual[1]:null;if(ual)src=src.replace(new RegExp('\\\\b'+ual[1]+'\\\\.(?=[A-Z])','g'),'');",
        'ui alias')
    src = sub1(src, "  if(v.nat==='Random'){\n", NAT + "  if(v.nat==='Random'){\n", 'media natMember')
    src = sub1(src, "  throw new Error('desconhecido '+n)}",
               "  if(n==='rootBundle')return{nat:'Bundle',f:{},src:'rootBundle'};\n"
               "  if(n==='ui'||n===ST.uiAlias)return{nat:'UiNS',f:{},src:'ui'};\n"
               "  throw new Error('desconhecido '+n)}", 'lookup rootBundle')
    src = sub1(src,
        "      if(a.name==='createTicker'&&a.args.length&&a.args[0].ast!==undefined)return mkTicker(cbArg(a.args[0].ast,env));\n",
        "      if(a.name==='createTicker'&&a.args.length&&a.args[0].ast!==undefined)return mkTicker(cbArg(a.args[0].ast,env));\n"
        "      if(a.name==='decodeImageFromList'&&a.args.length&&a.args[0].ast!==undefined){var dbl=ev(a.args[0].ast,env);return mkImg(dbl&&dbl.path)}\n"
        "      if(a.name==='setState'&&a.args.length===1){var sa0=a.args[0],stx=sa0.rawText!==undefined?sa0.rawText:(sa0.ast&&sa0.ast.src)||sa0.src;\n"
        "        if(stx){var sp=new Ps(stx),se=mkEnv({});se.parent=env;if(env.self)se.self=env.self;if(sp.is('(')){var sd=0;do{if(sp.is('('))sd++;else if(sp.is(')'))sd--;sp.i++}while(sd>0&&!sp.end())}if(sp.isId('async'))sp.i++;if(sp.eat('=>'))simple(sp,se,true);else stmt(sp,se,true)}\n"
        "        else{var sfn=sa0.ast!==undefined?ev(sa0.ast,env):null;if(sfn&&sfn.lam)callLam(sfn,[])}dirty=true;return null}\n",
        'fn decodeImageFromList')
    src = sub1(src,
        "      if(a.name.indexOf('HardwareKeyboard.instance')===0){",
        "      if(a.args&&a.name==='AudioPlayer')return{nat:'Audio',f:{},au:{vol:1,src:null},src:'AudioPlayer()'};\n"
        "      if(a.args&&a.name==='AssetSource'){var asv=a.args[0]&&a.args[0].ast!==undefined?ev(a.args[0].ast,env):'';somOf(asv);return{nat:'AssetSource',path:String(asv),f:{},src:\"AssetSource('\"+asv+\"')\"}}\n"
        "      if(a.args&&a.name==='SystemSound.play'){sfx('clique',1);return null}\n"
        "      if(a.args&&/^HapticFeedback\\.\\w+$/.test(a.name))return null;\n"
        "      if(a.name.indexOf('HardwareKeyboard.instance')===0){",
        'ctor audio')
    src = sub1(src, "        case 'drawPaint':add({k:'color'},args[0]);return null;",
               CANVAS_IMG + "        case 'drawPaint':add({k:'color'},args[0]);return null;", 'canvas drawImage')
    # Paint com src que mostra a cascata (TextStyle(foreground: Paint()..style = stroke) chega inteiro ao TextPainter)
    src = sub1(src,
        "    case 'Paint':return{nat:'Paint',f:{color:{raw:'Color(0xFF000000)'},style:'PaintingStyle.fill',strokeWidth:new Dbl(0),strokeCap:'StrokeCap.butt',strokeJoin:'StrokeJoin.miter'},src:'Paint()'};",
        "    case 'Paint':{var po={nat:'Paint',f:{color:{raw:'Color(0xFF000000)'},style:'PaintingStyle.fill',strokeWidth:new Dbl(0),strokeCap:'StrokeCap.butt',strokeJoin:'StrokeJoin.miter'}};"
        "Object.defineProperty(po,'src',{enumerable:true,configurable:true,get:function(){var f=this.f;return 'Paint()..color = '+pcol(f.color)+'..style = '+pcol(f.style)+'..strokeWidth = '+nn(f.strokeWidth)},set:function(){}});return po}",
        'Paint src')
    src = sub1(src, "function tpInfo(tp){", TPINFO + "function tpInfoOld(tp){", 'tpInfo')
    src = sub1(src,
        "cs.ops.push({k:'text',x:nn(args[1].f.dx),y:nn(args[1].f.dy),text:ti.text,size:ti.size,color:ti.color,bold:ti.bold,m:cs.m.slice(),clip:cs.clip})",
        "cs.ops.push({k:'text',x:nn(args[1].f.dx),y:nn(args[1].f.dy),text:ti.text,size:ti.size,color:ti.color,bold:ti.bold,ti:ti,m:cs.m.slice(),clip:cs.clip})",
        'tp paint op')
    # desenho no canvas: imagens e texto estilizado
    src = sub1(src,
        "      case 'text':{g.fillStyle=css(o.color);g.font=(o.bold?'700 ':'')+o.size+'px Roboto,Arial,sans-serif';g.textBaseline='top';\n"
        "        String(o.text).split('\\n').forEach(function(t,i){g.fillText(t,o.x,o.y+i*o.size*1.2)});break}}",
        CANVAS_DRAW_IMG + "}", 'paintCanvas img/text')
    # SVG (reserva): imagem com recorte da folha
    src = sub1(src,
        "      case 'color':el='<rect x=\"-5000\" y=\"-5000\" width=\"10000\" height=\"10000\" fill=\"'+col+'\"'+tr+'/>';break;",
        "      case 'color':el='<rect x=\"-5000\" y=\"-5000\" width=\"10000\" height=\"10000\" fill=\"'+col+'\"'+tr+'/>';break;\n"
        "      case 'img':{var spx=window.OF_SPRITES&&window.OF_SPRITES[o.path];if(!spx)break;el='<g'+tr+'><svg x=\"'+f(o.d[0])+'\" y=\"'+f(o.d[1])+'\" width=\"'+f(o.d[2])+'\" height=\"'+f(o.d[3])+'\" viewBox=\"'+o.s.map(f).join(' ')+'\" preserveAspectRatio=\"none\"><image href=\"'+spx.uri+'\" width=\"'+spx.w+'\" height=\"'+spx.h+'\" style=\"image-rendering:pixelated\"/></svg></g>';break}",
        'paintSvg img')
    # Image.asset com os sprites prontos (filterQuality: FilterQuality.none deixa o pixel art nítido)
    src = sub1(src,
        "      if(n.type==='Image.network'||/^FadeInImage/.test(n.type)){",
        "      if(n.type==='Image.asset'){var asr='';try{asr=strVal(M.evalProp?M.evalProp(n,'src'):M.getProp(n,'src'))}catch(e){}var spa=window.OF_SPRITES&&window.OF_SPRITES[asr];\n"
        "        if(spa){d.innerHTML='';if(iw==null||!isFinite(iw))d.style.width=spa.w+'px';if(ih==null||!isFinite(ih))d.style.height=spa.h+'px';\n"
        "          var fmA={'BoxFit.cover':'cover','BoxFit.fill':'fill','BoxFit.none':'none','BoxFit.scaleDown':'scale-down'},ima=document.createElement('img');ima.src=spa.uri;ima.alt='';\n"
        "          ima.style.cssText='width:100%;height:100%;display:block;object-fit:'+(fmA[String(M.getProp(n,'fit')||'')]||'contain')+(/FilterQuality\\.none/.test(M.getProp(n,'filterQuality')||'')?';image-rendering:pixelated':'');d.appendChild(ima)}}\n"
        "      if(n.type==='Image.network'||/^FadeInImage/.test(n.type)){",
        'Image.asset sprites')
    # Text(style: GoogleFonts.pressStart2p(...)) e fontFamily das fontes de jogo
    src = sub1(src,
        "function textCss(raw){\n  raw=raw==null?raw:String(raw).trim();\n",
        "function textCss(raw){\n  raw=raw==null?raw:String(raw).trim();\n"
        "  var gfm=/^GoogleFonts\\.(\\w+)\\(([\\s\\S]*)\\)$/.exec(raw||'');if(gfm){var gin=gfm[2].trim(),gts=/^textStyle:\\s*(?:const\\s+)?TextStyle\\(([\\s\\S]*)\\)\\s*,?\\s*$/.exec(gin);"
        "var GFN={pressStart2p:'Press Start 2P',silkscreen:'Silkscreen',vt323:'VT323',bungee:'Bungee'};raw=\"TextStyle(fontFamily: '\"+(GFN[gfm[1]]||gfm[1])+\"'\"+((gts?gts[1]:gin).trim()?', '+(gts?gts[1]:gin):'')+')'}\n",
        'textCss GoogleFonts')
    src = sub1(src,
        "    css+='font-family:'+(/mono|courier|consolas/i.test(ff)?",
        "    if(/^press\\s*start\\s*2p$|^pressstart2p$/i.test(ff))ff='Press Start 2P';if(/^(Press Start 2P|Silkscreen|VT323|Bungee)$/i.test(ff)){css+=\"font-family:'\"+ff+\"',monospace;\";ff=''}\n"
        "    if(ff)css+='font-family:'+(/mono|courier|consolas/i.test(ff)?",
        'textCss game fonts')
    # quando as fontes da web chegam, a tela é redesenhada com elas
    src = sub1(src, "function animKick(){", "if(document.fonts&&document.fonts.ready)document.fonts.ready.then(function(){try{if(typeof renderCanvas==='function')renderCanvas()}catch(e){}});\nfunction animKick(){", 'fonts ready')
    # botão de som no cabeçalho
    src = sub1(src,
        '<button class="btn" id="themeBtn"',
        '<button class="btn" id="somBtn" aria-pressed="false" title="Ligar ou desligar os efeitos sonoros dos jogos">🔊 Som</button>\n  <button class="btn" id="themeBtn"',
        'som button')
    return src


SOM_BTN_JS = r"""<script>
(function(){var b=document.getElementById('somBtn');if(!b||!window.OF_SFX_MUDO)return;
  function show(){var m=window.OF_SFX_MUDO();b.textContent=m?'🔇 Som':'🔊 Som';b.setAttribute('aria-pressed',m?'true':'false')}
  b.addEventListener('click',function(){window.OF_SFX_MUDO(!window.OF_SFX_MUDO());show();if(!window.OF_SFX_MUDO())window.OF_SFX('clique')});show()})();
</script>
"""


def finish(src):
    return src + SOM_BTN_JS
