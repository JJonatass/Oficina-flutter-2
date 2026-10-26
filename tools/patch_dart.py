# Oficina Flutter 2, frente 7b: Dart que faltava no interpretador.
from patch_engine import sub1


def patch(src):
    # ---- campos declarados juntos: late Bola a, b; int x = 0, y = 0;
    src = sub1(src,
        "    var f=FIELD.exec(ch);\n    if(f){ci.fields.push({type:normType(f[1]),name:f[2],init:f[3]?f[3].trim():null});return}",
        "    var mf=/^(?:@\\w+\\s+)?((?:late\\s+)?(?:final\\s+|const\\s+|var\\s+)?(?:[A-Za-z_][\\w.]*(?:<[^;=]*?>)?\\??\\s+)?)([A-Za-z_]\\w*\\s*(?:=[\\s\\S]*?)?,[\\s\\S]*);$/.exec(ch);\n"
        "    if(mf){var mps=splitTopStr(mf[2],','),mok=mps.length>1&&mps.every(function(x){return /^\\s*[A-Za-z_]\\w*\\s*(?:=[\\s\\S]+)?$/.test(x)&&!/^\\s*\\w+\\s*\\(/.test(x)});\n"
        "      if(mok){var mty=mf[1].replace(/\\b(late|final|const|var)\\b/g,'').trim()||'var';mps.forEach(function(x){var mm=/^\\s*([A-Za-z_]\\w*)\\s*(?:=\\s*([\\s\\S]+))?$/.exec(x);ci.fields.push({type:mty==='var'?'var':normType(mty),name:mm[1],init:mm[2]?mm[2].trim():null})});return}}\n"
        "    var f=FIELD.exec(ch);\n    if(f){ci.fields.push({type:normType(f[1]),name:f[2],init:f[3]?f[3].trim():null});return}",
        'multi fields')
    # ---- a?.b.c: o ?. curto-circuita a cadeia inteira
    src = sub1(src, "a={t:'mem',o:a,name:name,args:args,ns:ns,targs:targs}}",
        "a={t:'mem',o:a,name:name,args:args,ns:ns||(a&&a.t==='mem'&&(a.ns||a.nsc)),nsc:ns||(a&&a.t==='mem'&&(a.ns||a.nsc)),targs:targs}}", 'null shorting')
    # ---- registros com campos nomeados: (nome: 'Ana', idade: 20), r.nome, var (:nome, :idade) = r
    src = sub1(src,
        "  if(p.is('(')){p.i++;var e=pTern(p);if(p.is(',')){var rp=[e];while(p.eat(',')){if(p.is(')'))break;rp.push(pTern(p))}p.need(')');return{t:'rec',items:rp}}p.need(')');return e}",
        "  if(p.is('(')){p.i++;"
        "if(p.pk()&&p.pk().k==='id'&&p.is(':',1)){var rnm={},rps=[];do{if(p.is(')'))break;if(p.pk()&&p.pk().k==='id'&&p.is(':',1)){var rk=p.pk().v;p.i+=2;rnm[rk]=pTern(p)}else rps.push(pTern(p))}while(p.eat(','));p.need(')');return{t:'rec',items:rps,named:rnm}}"
        "var e=pTern(p);if(p.is(',')){var rp=[e],rn=null;while(p.eat(',')){if(p.is(')'))break;if(p.pk()&&p.pk().k==='id'&&p.is(':',1)){var rk2=p.pk().v;p.i+=2;(rn||(rn={}))[rk2]=pTern(p)}else rp.push(pTern(p))}p.need(')');return{t:'rec',items:rp,named:rn}}p.need(')');return e}",
        'record parse')
    src = sub1(src, "    case 'rec':return{isRec:true,pos:a.items.map(function(x){return ev(x,env)})};",
        "    case 'rec':{var rv0={isRec:true,pos:a.items.map(function(x){return ev(x,env)})};if(a.named){rv0.nm={};Object.keys(a.named).forEach(function(k){rv0.nm[k]=ev(a.named[k],env)})}return rv0}", 'record ev')
    src = sub1(src, "  if(v&&v.isRec)return '('+v.pos.map(lit).join(', ')+')';",
        "  if(v&&v.isRec)return '('+v.pos.map(lit).concat(v.nm?Object.keys(v.nm).map(function(k){return k+': '+lit(v.nm[k])}):[]).join(', ')+(v.pos.length===1&&!v.nm?',':'')+')';", 'record lit')
    src = sub1(src, "  if(v.isRec){var rmm=/^\$(\d+)$/.exec(name);if(rmm&&v.pos[+rmm[1]-1]!==undefined)return v.pos[+rmm[1]-1]}",
        "  if(v.isRec){var rmm=/^\$(\d+)$/.exec(name);if(rmm&&v.pos[+rmm[1]-1]!==undefined)return v.pos[+rmm[1]-1];if(v.nm&&hasOwn(v.nm,name))return v.nm[name];if(name==='toString')return show(v);if(name==='hashCode')return 0}", 'record member')
    src = sub1(src,
        "    var q=i+1,names=[];while(t[q]&&!(t[q].k==='p'&&t[q].v===')')){if(t[q].k==='id')names.push(t[q].v);q++}\n"
        "    if(t[q]&&t[q+1]&&t[q+1].k==='p'&&t[q+1].v==='='&&names.length){p.i=q+2;var rv=pTern(p);p.eat(';');\n"
        "      if(run){var rec=ev(rv,env);if(!rec||!rec.isRec)throw new Error('desestruturação');names.forEach(function(n,ix){env.locals[n]=rec.pos[ix]})}return true}",
        "    var q=i+1,names=[],els=[],cur=[],dq=0;while(t[q]&&!(dq===0&&t[q].k==='p'&&t[q].v===')')){var tq=t[q];if(tq.k==='p'&&(tq.v==='('||tq.v==='<'))dq++;else if(tq.k==='p'&&(tq.v===')'||tq.v==='>'))dq--;"
        "if(dq===0&&tq.k==='p'&&tq.v===','){els.push(cur);cur=[]}else cur.push(tq);if(tq.k==='id')names.push(tq.v);q++}if(cur.length)els.push(cur);\n"
        "    var pats=els.map(function(el){var ids=el.filter(function(x){return x.k==='id'&&!MODS[x.v]}).map(function(x){return x.v}),ci=el.findIndex(function(x){return x.k==='p'&&x.v===':'});"
        "if(ci===0)return{nm:ids[ids.length-1],v:ids[ids.length-1]};if(ci>0)return{nm:el[0].v,v:ids[ids.length-1]};return{v:ids[ids.length-1]}});\n"
        "    if(t[q]&&t[q+1]&&t[q+1].k==='p'&&t[q+1].v==='='&&names.length){p.i=q+2;var rv=pTern(p);p.eat(';');\n"
        "      if(run){var rec=ev(rv,env);if(!rec||!rec.isRec)throw new Error('desestruturação');var pix=0;pats.forEach(function(pt){if(pt.nm){env.locals[pt.v]=rec.nm&&hasOwn(rec.nm,pt.nm)?rec.nm[pt.nm]:null}else env.locals[pt.v]=rec.pos[pix++]})}return true}",
        'record destructure')
    # ---- tipos de registro em declarações: ({String nome, int idade}) pessoa() vira dynamic pessoa()
    src = sub1(src, "ST.extract=function(src){src=stripComments(src);",
        "ST.extract=function(src){src=stripComments(src);src=src.replace(/(^|[;{}]|\\n)([ \\t]*(?:(?:static|final|late|const)\\s+)*)\\((\\{[^(){}]*\\}|[^(){};=]*?(?:,\\s*\\{[^(){}]*\\})?)\\)(\\??)(\\s+)([A-Za-z_]\\w*)(?=\\s*[=;(,])/g,function(m,a,b,c,d,e,f){if(/^\\s*$/.test(c))return m;return a+b+'dynamic'+e+f});", 'record types')
    src = sub1(src, "if(v&&v.isRec)return '('+v.pos.map(show).join(', ')+')';",
        "if(v&&v.isRec)return '('+v.pos.map(show).concat(v.nm?Object.keys(v.nm).map(function(k){return k+': '+show(v.nm[k])}):[]).join(', ')+')';", 'record show')
    # ---- TextInputFormatter escrito pelo aluno (classe com formatEditUpdate)
    src = sub1(src, "    else if((m=/LengthLimitingTextInputFormatter\\(\\s*(\\d+)\\s*\\)/.exec(it))){var ln=+m[1];steps.push(function(v){return v.slice(0,ln)})}});",
        "    else if((m=/LengthLimitingTextInputFormatter\\(\\s*(\\d+)\\s*\\)/.exec(it))){var ln=+m[1];steps.push(function(v){return v.slice(0,ln)})}\n"
        "    else if((m=/^\\s*(?:const\\s+)?([A-Z]\\w*)\\s*\\(/.exec(it))&&OF.ST.dataClasses&&OF.ST.dataClasses[m[1]]){var fexp=it.trim();steps.push(function(v,old){try{return OF.ST.fmtCall(fexp,old==null?'':old,v)}catch(e){return v}})}});",
        'custom formatter')
    src = sub1(src, "  return function(v){steps.forEach(function(f){v=f(v)});return v}}",
        "  return function(v,old){steps.forEach(function(f){v=f(v,old)});return v}}", 'fmt old')
    src = sub1(src, "  if(i._fmt){var nv=i._fmt(i.value);",
        "  if(i._fmt){var nv=i._fmt(i.value,i._prev);", 'fmt prev')
    src = sub1(src, "  var cnt=i.parentNode.querySelector('.cnt');if(cnt)cnt.textContent=i.value.length+'/'+(i.dataset.max||'');",
        "  i._prev=i.value;var cnt=i.parentNode.querySelector('.cnt');if(cnt)cnt.textContent=i.value.length+'/'+(i.dataset.max||'');", 'fmt store')
    src = sub1(src, "/* ===== Oficina 2: curvas, pinça, consultas de componentes ===== */", TEV + "/* ===== Oficina 2: curvas, pinça, consultas de componentes ===== */", 'tev engine')
    src = sub1(src, "  if(v&&v.nat==='BodyTypeNS')return name;\n",
        "  if(v&&v.nat==='BodyTypeNS')return name;\n  if(v&&(v.nat==='TEV'||v.nat==='TSel')){var tr=tevMember(v,name,args||[]);if(tr!==undefined)return tr}\n", 'tev member')
    src = sub1(src, "      if(a.args&&NATCTOR[a.name])return natCtor(a.name,evalArgs(a,env));",
        "      if(a.args&&(a.name==='TextEditingValue'||a.name==='TextSelection.collapsed'||a.name==='TextSelection'||a.name==='TextSelection.fromPosition')){return tevCtor(a.name,evalArgs(a,env))}\n"
        "      if(!a.args&&a.name==='TextEditingValue.empty')return mkTev('',0);\n"
        "      if(a.args&&NATCTOR[a.name])return natCtor(a.name,evalArgs(a,env));", 'tev ctor')
    # ---- Widget build(BuildContext context) => Scaffold(...);
    src = sub1(src, "    if(b>=0)for(x=b;x<t.length;x++)if(t[x].k==='id'&&t[x].v==='return'){i=x+1;break}",
        "    if(b>=0){for(x=b;x<t.length;x++){if(t[x].k==='p'&&t[x].v==='{')break;if(t[x].k==='p'&&t[x].v==='='&&t[x+1]&&t[x+1].v==='>'){i=x+2;if(t[i]&&t[i].v==='const')i++;break}}}\n"
        "    if(b>=0&&i<0)for(x=b;x<t.length;x++)if(t[x].k==='id'&&t[x].v==='return'){i=x+1;break}", 'arrow build parse')
    src = sub1(src, "    var b=BUILD.exec(ch);if(b){ci.build=buildInfo(b[1]);return}",
        "    var b=BUILD.exec(ch);if(b){ci.build=buildInfo(b[1]);return}\n"
        "    var ba=/^(?:@\\w+\\s+)?Widget\\s+build\\s*\\([^)]*\\)\\s*=>\\s*([\\s\\S]+?);$/.exec(ch);if(ba){ci.build=buildInfo('{return '+ba[1]+';}');return}", 'arrow build class')
    return src


TEV = r'''/* ===== Oficina 2: TextEditingValue e TextSelection para formatadores próprios ===== */
function mkSel(b,e){return{nat:'TSel',f:{baseOffset:b,extentOffset:e==null?b:e,start:Math.min(b,e==null?b:e),end:Math.max(b,e==null?b:e),isCollapsed:e==null||e===b},src:'TextSelection(baseOffset: '+b+', extentOffset: '+(e==null?b:e)+')'}}
function mkTev(t,c,sel){t=String(t==null?'':t);return{nat:'TEV',f:{text:t,selection:sel||mkSel(c==null?t.length:c),composing:{raw:'TextRange.empty'}},src:"TextEditingValue(text: '"+t.replace(/'/g,"\\'")+"')"}}
function tevCtor(nm,args){var o={};args.forEach(function(a){o[a.name||'_']=a.val});
  if(nm==='TextEditingValue'){var t=o.text!=null?show(o.text):'';return mkTev(t,null,o.selection&&o.selection.nat==='TSel'?o.selection:null)}
  if(nm==='TextSelection.collapsed')return mkSel(nn(o.offset));
  if(nm==='TextSelection.fromPosition')return mkSel(nn(o._&&o._.f?o._.f.offset:o._));
  return mkSel(nn(o.baseOffset),o.extentOffset!=null?nn(o.extentOffset):null)}
function tevMember(v,name,args){if(v.nat==='TEV'){if(name==='copyWith'){var o={};(ARGN||[]).forEach(function(n,i){if(n)o[n]=args[i]});
    return mkTev(o.text!=null?show(o.text):v.f.text,null,o.selection&&o.selection.nat==='TSel'?o.selection:(o.text!=null?null:v.f.selection))}
  if(name==='toString')return v.src;if(hasOwn(v.f,name))return v.f[name];return undefined}
  if(hasOwn(v.f,name))return v.f[name];if(name==='copyWith')return v;return undefined}
ST.fmtCall=function(expr,old,novo){var obj=ST.value(expr);if(!obj||!obj.cls)return novo;var r=member(obj,'formatEditUpdate',[mkTev(old),mkTev(novo)]);return r&&r.nat==='TEV'?String(r.f.text):novo};
'''
