# Oficina Flutter 2, frente 7a: desenho completo no Canvas.
# Gradientes (Paint.shader com LinearGradient/RadialGradient/SweepGradient.createShader e ui.Gradient.linear/radial/sweep),
# MaskFilter.blur, BlendMode, canvas.drawShadow e ParagraphBuilder + canvas.drawParagraph.
from patch_engine import sub1

ENGINE = r"""/* ===== Oficina 2: gradientes, desfoque, modos de mistura e parágrafos no Canvas ===== */
var GR_AL={topLeft:[-1,-1],topCenter:[0,-1],topRight:[1,-1],centerLeft:[-1,0],center:[0,0],centerRight:[1,0],bottomLeft:[-1,1],bottomCenter:[0,1],bottomRight:[1,1]};
function grAlinha(v,def){var s=String(pcol(v)||'').trim().replace(/^const\s+/,''),m;if(!s)return def;
  if((m=/Alignment(?:Directional)?\.(\w+)/.exec(s))){var k=m[1].replace(/Start/,'Left').replace(/End/,'Right').replace(/^start/,'centerLeft').replace(/^end/,'centerRight');if(GR_AL[k])return GR_AL[k]}
  if((m=/Alignment\(\s*(-?[\d.]+)\s*,\s*(-?[\d.]+)\s*\)/.exec(s)))return[+m[1],+m[2]];return def}
function grCores(v){return toIter(v).map(function(c){return pcol(c)})}
function grStops(v,n){var s=v==null?null:toIter(v).map(function(x){return nn(x)});if(!s||s.length!==n){s=[];for(var i=0;i<n;i++)s.push(n===1?0:i/(n-1))}return s}
function grArgs(args){var pos=[],nm={};args.forEach(function(a){if(a.name)nm[a.name]=a.val;else pos.push(a.val)});return{pos:pos,nm:nm}}
function grSrc(nome,args){return nome+'('+args.map(function(a){return (a.name?a.name+': ':'')+(a.src||'')}).join(', ')+')'}
function grShader(gd,rc){var nm=gd.nm,L=nn(rc.f.left),T=nn(rc.f.top),W=nn(rc.f.width),H=nn(rc.f.height);function pt(a){return[L+(a[0]+1)/2*W,T+(a[1]+1)/2*H]}
  var cols=grCores(nm.colors),st=grStops(nm.stops,cols.length);
  if(gd.t==='LinearGradient'){var a=pt(grAlinha(nm.begin,[-1,0])),b=pt(grAlinha(nm.end,[1,0]));return{t:'linear',x0:a[0],y0:a[1],x1:b[0],y1:b[1],c:cols,s:st}}
  if(gd.t==='RadialGradient'){var c=pt(grAlinha(nm.center,[0,0])),r=(nm.radius!=null?nn(nm.radius):0.5)*Math.min(W,H);return{t:'radial',x0:c[0],y0:c[1],r:r,c:cols,s:st}}
  var c2=pt(grAlinha(nm.center,[0,0]));return{t:'sweep',x0:c2[0],y0:c2[1],a0:nm.startAngle!=null?nn(nm.startAngle):0,a1:nm.endAngle!=null?nn(nm.endAngle):Math.PI*2,c:cols,s:st}}
function grUi(nome,args){var g=grArgs(args),p=g.pos;
  if(nome==='Gradient.linear')return{t:'linear',x0:nn(p[0].f.dx),y0:nn(p[0].f.dy),x1:nn(p[1].f.dx),y1:nn(p[1].f.dy),c:grCores(p[2]),s:grStops(p[3],toIter(p[2]).length)};
  if(nome==='Gradient.radial')return{t:'radial',x0:nn(p[0].f.dx),y0:nn(p[0].f.dy),r:nn(p[1]),c:grCores(p[2]),s:grStops(p[3],toIter(p[2]).length)};
  return{t:'sweep',x0:nn(p[0].f.dx),y0:nn(p[0].f.dy),a0:p[5]!=null?nn(p[5]):0,a1:p[6]!=null?nn(p[6]):Math.PI*2,c:grCores(p[1]),s:grStops(p[2],toIter(p[1]).length)}}
function mfSigma(v){var s=String(pcol(v)||''),m=/MaskFilter\.blur\(\s*[\w.]+\s*,\s*([\d.]+)/.exec(s);return m?+m[1]:0}
var BLENDS={srcOver:'source-over',srcIn:'source-in',srcOut:'source-out',srcATop:'source-atop',dstOver:'destination-over',dstIn:'destination-in',dstOut:'destination-out',dstATop:'destination-atop',
  plus:'lighter',xor:'xor',multiply:'multiply',screen:'screen',overlay:'overlay',darken:'darken',lighten:'lighten',colorDodge:'color-dodge',colorBurn:'color-burn',hardLight:'hard-light',
  softLight:'soft-light',difference:'difference',exclusion:'exclusion',hue:'hue',saturation:'saturation',color:'color',luminosity:'luminosity',clear:'destination-out',src:'copy',dst:'destination-over'};
function blendOf(v){var m=/BlendMode\.(\w+)/.exec(String(pcol(v)||''));return m&&BLENDS[m[1]]&&m[1]!=='srcOver'?BLENDS[m[1]]:null}
function paraTp(pa,largura){var base=String(pa.base||'').replace(/^\s*(?:const\s+)?(?:ParagraphStyle|TextStyle)\(/,'').replace(/\)\s*$/,''),est='';
  for(var i=pa.sp.length-1;i>=0;i--)if(pa.sp[i][1]){est=String(pa.sp[i][1]).replace(/^\s*(?:const\s+)?TextStyle\(/,'').replace(/\)\s*$/,'');break}
  var estilo='TextStyle('+[base,est].filter(function(x){return x.trim()}).join(', ')+')',txt=pa.sp.map(function(s){return s[0]}).join('');
  function tpDe(t){return{nat:'TextPainter',f:{text:{raw:"TextSpan(text: '"+t.replace(/\\/g,'\\\\').replace(/'/g,"\\'").replace(/\n/g,'\\n')+"', style: "+estilo+")"}},st:{},src:'TextPainter()'}}
  var ti=tpInfo(tpDe('M'));if(largura&&isFinite(largura)){if(!TPM)TPM=document.createElement('canvas').getContext('2d');TPM.font=ti.font;
    var linhas=[];txt.split('\n').forEach(function(par){var lin='';par.split(/(\s+)/).forEach(function(w){var t=lin+w;if(lin&&TPM.measureText(t.replace(/\s+$/,'')).width>largura){linhas.push(lin.replace(/\s+$/,''));lin=w.replace(/^\s+/,'')}else lin=t});linhas.push(lin)});txt=linhas.join('\n')}
  return tpDe(txt)}
"""

MEMBER = (
    "  if(v&&v.nat==='Grad'&&name==='createShader'){return{nat:'Shader',f:{},sh:grShader(v,args[0]),src:'Shader'}}\n"
    "  if(v&&v.nat==='ParaB'){switch(name){case 'pushStyle':v.st.push(pcol(args[0]));return null;case 'pop':if(v.st.length>1)v.st.pop();return null;"
    "case 'addText':v.sp.push([String(args[0]),v.st[v.st.length-1]]);return null;case 'addPlaceholder':return null;"
    "case 'build':return{nat:'Para',f:{},sp:v.sp.slice(),base:v.base,w:Infinity,src:'Paragraph'}}}\n"
    "  if(v&&v.nat==='Para'){if(name==='layout'){var lc=String(pcol(args[0])||''),lm=/width:\\s*([\\d.]+)/.exec(lc);v.w=lm?+lm[1]:Infinity;if(!lm&&args[0]&&args[0].f&&args[0].f.width!=null)v.w=nn(args[0].f.width);v.tp=paraTp(v,v.w);return null}"
    "if(!v.tp)v.tp=paraTp(v,v.w);var pti=tpInfo(v.tp);switch(name){case 'height':return new Dbl(pti.h);case 'width':return new Dbl(isFinite(v.w)?v.w:pti.w);case 'longestLine':case 'maxIntrinsicWidth':case 'minIntrinsicWidth':return new Dbl(pti.w);"
    "case 'didExceedMaxLines':return false;case 'alphabeticBaseline':case 'ideographicBaseline':return new Dbl(pti.size*0.8);case 'computeLineMetrics':return []}}\n"
)

CTOR = (
    "      if(a.args&&/^(?:Linear|Radial|Sweep)Gradient$/.test(a.name)){var gra=evalArgs(a,env),gg=grArgs(gra);return{nat:'Grad',t:a.name,nm:gg.nm,f:{},src:grSrc(a.name,gra)}}\n"
    "      if(a.args&&/^(?:ui\\.)?Gradient\\.(?:linear|radial|sweep)$/.test(a.name)){var gua=evalArgs(a,env);return{nat:'Shader',f:{},sh:grUi(a.name.replace(/^ui\\./,''),gua),src:'Shader'}}\n"
    "      if(a.args&&/^(?:ui\\.)?ParagraphBuilder$/.test(a.name)){var pba=evalArgs(a,env);return{nat:'ParaB',f:{},sp:[],st:[null],base:pba[0]?pcol(pba[0].val):'',src:'ParagraphBuilder()'}}\n"
)

CANVAS_FN = r"""function grFill(g,sh){try{var gr;
  if(sh.t==='linear')gr=g.createLinearGradient(sh.x0,sh.y0,sh.x1,sh.y1);else if(sh.t==='radial')gr=g.createRadialGradient(sh.x0,sh.y0,0,sh.x0,sh.y0,Math.max(0.001,sh.r));
  else{if(!g.createConicGradient)return null;gr=g.createConicGradient(sh.a0,sh.x0,sh.y0)}
  var span=sh.t==='sweep'?Math.max(0,Math.min(1,(sh.a1-sh.a0)/(Math.PI*2))):1;
  sh.c.forEach(function(c,i){gr.addColorStop(Math.max(0,Math.min(1,sh.s[i]*span)),pcssColor(c))});return gr}catch(e){return null}}
"""


def patch(src):
    src = sub1(src, "/* ===== Oficina 2: curvas, pinça, consultas de componentes ===== */",
               ENGINE + "/* ===== Oficina 2: curvas, pinça, consultas de componentes ===== */", 'draw engine')
    src = sub1(src, "  if(v&&v.nat==='BodyTypeNS')return name;\n", "  if(v&&v.nat==='BodyTypeNS')return name;\n" + MEMBER, 'draw member')
    src = sub1(src, "      if(a.args&&NATCTOR[a.name])return natCtor(a.name,evalArgs(a,env));",
               CTOR + "      if(a.args&&NATCTOR[a.name])return natCtor(a.name,evalArgs(a,env));", 'draw ctor')
    # o Paint passa a levar shader, desfoque e modo de mistura
    src = sub1(src,
        "      function pn(p){return{color:pcol(p.f.color),",
        "      function pn(p){return{sh:p.f.shader&&p.f.shader.sh||null,blur:p.f.maskFilter!=null?mfSigma(p.f.maskFilter):0,blend:p.f.blendMode!=null?blendOf(p.f.blendMode):null,color:pcol(p.f.color),",
        'pn extra')
    src = sub1(src,
        "        case 'drawPath':add({k:'path',d:args[0].st.d},args[1]);return null;",
        "        case 'drawPath':add({k:'path',d:args[0].st.d},args[1]);return null;\n"
        "        case 'drawShadow':add({k:'shadow',d:args[0].st.d,e:nn(args[2])},{f:{color:args[1]}});return null;\n"
        "        case 'drawParagraph':{var pp0=args[0];if(!pp0||pp0.nat!=='Para')throw exc('drawParagraph precisa de um Paragraph (ParagraphBuilder(...).build())');if(!pp0.tp)pp0.tp=paraTp(pp0,pp0.w);return member(pp0.tp,'paint',[v,args[1]])}",
        'canvas shadow paragraph')
    # no navegador: gradiente, filtro de desfoque e globalCompositeOperation
    src = sub1(src, "function tintMix(col,t){", CANVAS_FN + "function tintMix(col,t){", 'grFill')
    src = sub1(src,
        "    g.fillStyle=col;g.strokeStyle=col;g.lineWidth=p.sw||1;g.lineCap=p.cap||'butt';g.lineJoin=p.join||'miter';",
        "    g.fillStyle=col;g.strokeStyle=col;g.lineWidth=p.sw||1;g.lineCap=p.cap||'butt';g.lineJoin=p.join||'miter';\n"
        "    if(p.sh){var grd=grFill(g,p.sh);if(grd){g.fillStyle=grd;g.strokeStyle=grd}}\n"
        "    if(p.blur&&('filter' in g))g.filter='blur('+(p.blur*dpr*Math.sqrt(Math.abs(m[0]*m[3]-m[1]*m[2])))+'px)';\n"
        "    if(p.blend)g.globalCompositeOperation=p.blend;",
        'canvas paint extra')
    src = sub1(src,
        "      case 'color':g.fillRect(-5000,-5000,10000,10000);break;",
        "      case 'color':g.fillRect(-5000,-5000,10000,10000);break;\n"
        "      case 'shadow':if(o.d){var esc=Math.sqrt(Math.abs(m[0]*m[3]-m[1]*m[2]));g.globalAlpha*=0.45;if('filter' in g)g.filter='blur('+Math.max(1,o.e*0.8*dpr*esc)+'px)';g.translate(0,o.e*0.5);g.fill(p2d(o.d))}break;",
        'canvas shadow')
    return src
