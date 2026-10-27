# Oficina Flutter 2 · Parte 7 (jogo completo): ajustes do motor.
# - cada rota do Navigator tem o seu jogo: push/pushReplacement criam um jogo novo e o jogo da rota de baixo
#   fica parado (como o TickerMode do Flutter) até a rota de cima sair.
from patch_engine import sub1


def patch(src):
    # chave do GameWidget inclui a rota em que ele está
    tag = ("((OF.ST.navTag=function(){var o=R_opts,s=null;"
           "if(o.nav&&o.nav.length)s=(o.navRes||[])[o.nav.length-1];else if(o.rootSrc)s=o.rootSc;"
           "if(!s)return 'r0|';if(!s.__rid)s.__rid=(OF.ST.ridN=(OF.ST.ridN||0)+1);return 'r'+s.__rid+'|'}))()")
    src = sub1(src, "d.dataset.gwk=path.join('>')", "d.dataset.gwk=" + tag + "+path.join('>')", 'gw key 1')
    src = sub1(src, "gwk=path.join('>'),gwl", "gwk=OF.ST.navTag()+path.join('>'),gwl", 'gw key 2')
    # o jogo lembra a rota; só o da rota de cima anda e ouve o teclado
    # jogos de rotas que já saíram da pilha deixam de existir (param de andar e de tocar)
    src = sub1(src, "    ent=FL.byKey[key]={raw:raw,game:gv,isNew:isNew}}",
               "    ent=FL.byKey[key]={raw:raw,game:gv,isNew:isNew};"
               "var vivas=['r0'],ro=OF.R&&OF.R.opts;if(ro){(ro.navRes||[]).forEach(function(r){if(r&&r.__rid)vivas.push('r'+r.__rid)});if(ro.rootSc&&ro.rootSc.__rid)vivas.push('r'+ro.rootSc.__rid)}"
               "Object.keys(FL.byKey).forEach(function(k2){var t2=k2.split('|')[0];if(k2.indexOf('|')>0&&vivas.indexOf(t2)<0){var gm=FL.byKey[k2].game;var ix=FL.live.indexOf(gm);if(ix>=0)FL.live.splice(ix,1);delete FL.byKey[k2];try{if(gm&&gm.__loaded)flCall(gm,'onRemove')}catch(x){}}})}",
               'poda de jogos mortos')
    src = sub1(src, "  var g=ent.game;\n  if(g.__flErr)throw new Error(g.__flErr);",
               "  var g=ent.game;g.__tag=key.split('|')[0];\n  if(g.__flErr)throw new Error(g.__flErr);", 'gw tag')
    src = sub1(src, "  FL.live.slice().forEach(function(g){any=true;try{FL.tick(g,dt)}",
               "  var tagAgora=ST.navTag?ST.navTag().split('|')[0]:null;"
               "FL.live.slice().forEach(function(g){any=true;if(tagAgora&&g.__tag&&g.__tag!==tagAgora)return;try{FL.tick(g,dt)}",
               'tick só na rota de cima')
    src = sub1(src, "FL.live.forEach(function(g){if(!g.__loaded||g.__flErr)return;",
               "var tagK=ST.navTag?ST.navTag().split('|')[0]:null;"
               "FL.live.forEach(function(g){if(!g.__loaded||g.__flErr)return;if(tagK&&g.__tag&&g.__tag!==tagK)return;",
               'teclado só na rota de cima')
    # obj.metodo sem parênteses vira função (tear-off), não chamada: onPressed: jogo.continuar
    src = sub1(src, "    case 'mem':{var mo=ev(a.o,env);if(a.ns&&mo==null)return null;\n",
               "    case 'mem':{var mo=ev(a.o,env);if(a.ns&&mo==null)return null;\n"
               "      if(!a.args&&mo&&mo.cls&&ST.dataClasses[mo.cls]&&!hasOwn(mo.f,a.name)&&!ST.dataClasses[mo.cls].getters[a.name]&&ST.dataClasses[mo.cls].methods[a.name]){var tom=ST.dataClasses[mo.cls].methods[a.name],tob=mo;return{lam:true,src:(mo.__fid?'__flg'+mo.__fid+'.':'')+a.name,pn:[],call:function(args){return runMethod(tom,args||[],tob)}}}\n",
               'tearoff de metodo')
    # ... e o handler "jogo.continuar" de um overlay (jogo vira __flgN) também roda
    src = sub1(src, "if(p.is('.',1)&&p.pk(2)&&p.pk(2).k==='id'&&!p.is('(',3)&&(ST.fields[nm]||(ST.globals&&ST.globals[nm]))){",
               "if(p.is('.',1)&&p.pk(2)&&p.pk(2).k==='id'&&!p.is('(',3)&&(ST.fields[nm]||(ST.globals&&ST.globals[nm])||/^__flg\\d+$/.test(nm))){",
               'handler tearoff overlay')
    # splitTopStr: a seta => não fecha um <...> (dois lambdas na lista de inicialização quebravam o super(...))
    src = sub1(src, "    if('([{<'.indexOf(c)>=0)d++;else if(')]}>'.indexOf(c)>=0)d--;\n    if(c===sep&&d===0){out.push(cur);cur=''}else cur+=c;",
               "    if((c==='>'&&(str[i-1]==='='||str[i+1]==='='))||(c==='<'&&str[i+1]==='=')){}else if('([{<'.indexOf(c)>=0)d++;else if(')]}>'.indexOf(c)>=0)d--;\n    if(c===sep&&d===0){out.push(cur);cur=''}else cur+=c;",
               'splitTopStr seta')
    # Supabase simulado em tempo real entre abas: outra aba gravou no banco -> esta aba relê e redesenha
    src = sub1(src, "function dbSave(){try{localStorage.setItem('oficina_db',",
               "window.addEventListener('storage',function(e){if(e.key!=='oficina_db'||!e.newValue)return;try{"
               "var o=JSON.parse(e.newValue,function(k,v){return v&&typeof v==='object'&&v.$d!==undefined?new Dbl(v.$d):v});"
               "if(o&&o.sb){DBP.sb=o.sb;if(window.OF&&OF.rerender)OF.rerender()}}catch(x){}});\n"
               "function dbSave(){try{localStorage.setItem('oficina_db',", 'supabase entre abas')
    # geração procedural e busca de caminho fazem dezenas de milhares de voltas: limite maior antes de acusar loop infinito
    src = sub1(src, "function tick(){if(++steps>20000)throw", "function tick(){if(++steps>400000)throw", 'limite de voltas')
    # max e min do dart:math como valor: lista.reduce(max)
    src = sub1(src, "  if(n==='context')return{nat:'#ctx',f:{},src:'context'};",
               "  if((n==='max'||n==='min')&&!(ST.funcs&&hasOwn(ST.funcs,n))){var mfn=n;return{lam:true,src:n,pn:[],call:function(args){var x=args[0],y=args[1];var r=mfn==='max'?(nn(x)>=nn(y)?x:y):(nn(x)<=nn(y)?x:y);return r}}}\n"
               "  if(n==='context')return{nat:'#ctx',f:{},src:'context'};", 'max min tearoff')
    # Color.fromRGBO e Color.fromARGB calculados (o pintor já entende o texto)
    src = sub1(src, "    if(c==='Color'&&name==='lerp'){",
               "    if(c==='Color'&&name==='fromRGBO'){var cr=Math.round(nn(args[0])),cg=Math.round(nn(args[1])),cb=Math.round(nn(args[2])),co=Math.max(0,Math.min(1,nn(args[3])));return{raw:'Color.fromRGBO('+cr+', '+cg+', '+cb+', '+(+co.toFixed(3))+')'}}\n"
               "    if(c==='Color'&&name==='fromARGB'){var fa=Math.round(nn(args[0])),fr=Math.round(nn(args[1])),fg=Math.round(nn(args[2])),fb=Math.round(nn(args[3]));return{raw:'Color.fromRGBO('+fr+', '+fg+', '+fb+', '+(+(fa/255).toFixed(3))+')'}}\n"
               "    if(c==='Color'&&name==='lerp'){", 'color fromRGBO')
    # limites do simulador: o que a Parte 7 acrescentou
    src = sub1(src, "Não há rpc, storage, tabelas ligadas no select nem regras RLS.',",
               "Não há rpc, storage, tabelas ligadas no select nem regras RLS. Duas abas abertas na mesma aula compartilham o banco e se atualizam na hora, como dois aparelhos.',\n"
               " 'Navigator e jogos: cada tela aberta com push ou pushReplacement tem o seu jogo do Flame. O jogo da tela de baixo fica parado enquanto outra está por cima, e o de uma tela que saiu é descartado (com onRemove).',\n"
               " 'dart:math: Random (com ou sem semente; a sequência não é a mesma do Dart), min e max (também como valor, em reduce(max)), sqrt, pow, sin, cos, atan2 e pi. A classe Point não existe: use uma classe sua com x e y.',",
               'limites parte 7')
    # obj.campo(args) quando o campo guarda uma função: chama a função (antes devolvia a própria função)
    src = sub1(src, "      try{TARGS=a.targs||null;return member(mo,a.name,margs)}finally{ARGN=null;TARGS=null}}",
               "      if(a.args&&mo&&mo.cls&&hasOwn(mo.f,a.name)&&mo.f[a.name]&&mo.f[a.name].lam){ARGN=null;return callLam(mo.f[a.name],margs)}\n"
               "      try{TARGS=a.targs||null;return member(mo,a.name,margs)}finally{ARGN=null;TARGS=null}}", 'campo funcao chamada')
    # parâmetros [opcionais] com valor padrão que tem chaves, como [Map m = const {}]
    src = sub1(src, "  var inner=txt.trim(),bi=inner.indexOf('{'),out=[];",
               "  var inner=txt.trim(),bi=-1,out=[];for(var ii=0,dd=0;ii<inner.length;ii++){var ch=inner[ii];if(ch==='['||ch==='(')dd++;else if(ch===']'||ch===')')dd--;else if(ch==='{'&&dd===0){bi=ii;break}}",
               'parseParams chaves')
    src = sub1(src, "    if(!found&&pr.def!=null){try{val=ev(pTern(new Ps(pr.def)),mkEnv())}",
               "    if(!found&&pr.def!=null){try{val=ev(pTern(new Ps(String(pr.def).replace(/^const\\s+/,''))),mkEnv())}", 'padrao const')
    src = sub1(src, "  var bi=inner.indexOf('{'),si=inner.indexOf('[');",
               "  var si=inner.indexOf('['),bi=-1;for(var ii=0,dd=0;ii<inner.length;ii++){var ch=inner[ii];if(ch==='['||ch==='(')dd++;else if(ch===']'||ch===')')dd--;else if(ch==='{'&&dd===0){bi=ii;break}}",
               'declParams chaves')
    # DateTime.now() com milissegundos (o relógio de reação e o multijogador precisam)
    src = sub1(src, "    if(c==='DateTime'&&name==='now'){var n=new Date();return mkDate(n.getFullYear(),n.getMonth()+1,n.getDate(),n.getHours(),n.getMinutes(),n.getSeconds())}",
               "    if(c==='DateTime'&&name==='now'){var n=new Date();var dn=mkDate(n.getFullYear(),n.getMonth()+1,n.getDate(),n.getHours(),n.getMinutes(),n.getSeconds());dn.j=new Date(n.getTime());return dn}",
               'now com ms')
    # Offset == Offset compara dx e dy (contains, indexOf e == em listas de posições)
    src = sub1(src, "function eq(a,b){\n  if(isRaw(a)&&isRaw(b))return a.raw===b.raw;",
               "function eq(a,b){\n  if(isRaw(a)&&isRaw(b))return a.raw===b.raw;\n"
               "  if(a&&b&&a.nat&&b.nat&&a.nat===b.nat&&(a.nat==='Offset'||a.nat==='Size'||a.nat==='Vec2')){var ka=a.nat==='Offset'?['dx','dy']:(a.nat==='Size'?['width','height']:['x','y']);return nn(a.f[ka[0]])===nn(b.f[ka[0]])&&nn(a.f[ka[1]])===nn(b.f[ka[1]])}",
               'eq offset')
    # contains, indexOf e remove de listas comparam com == do Dart (Offset, números, classes com operator ==)
    src = sub1(src, "      case 'remove':{var ix=v.indexOf(args[0]);if(ix>=0)v.splice(ix,1);mutated=true;return ix>=0}\n      case 'contains':return v.indexOf(args[0])>=0;\n      case 'indexOf':return v.indexOf(args[0]);",
               "      case 'remove':{var ix=lstIdx(v,args[0]);if(ix>=0)v.splice(ix,1);mutated=true;return ix>=0}\n      case 'contains':return lstIdx(v,args[0])>=0;\n      case 'indexOf':return lstIdx(v,args[0]);",
               'lista eq')
    src = sub1(src, "function eq(a,b){", "function lstIdx(v,x){var i=v.indexOf(x);if(i>=0||x==null||typeof x!=='object')return i;if(!(x instanceof Dbl||x.nat==='Offset'||x.nat==='Size'||x.nat==='Vec2'||(x.cls&&ST.dataClasses[x.cls]&&ST.dataClasses[x.cls].methods['operator=='])))return -1;for(var k=0;k<v.length;k++){try{if(v[k]&&typeof v[k]==='object'&&eq(v[k],x))return k}catch(e){}}return -1}\nfunction eq(a,b){", 'lstIdx')
    return src
