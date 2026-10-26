# Oficina Flutter 2, frente 6: joystick e botões na tela, ColorEffect e MoveAlongPathEffect, Forge2D simplificado,
# mapas do Tiled, overlays vivos com ValueNotifier, transparência e tinta no canvas, arrasto estável.
import json, pathlib
from patch_engine import sub1

ROOT = pathlib.Path(__file__).resolve().parent


def maps_js():
    out = {}
    for p in sorted((ROOT / 'maps').glob('*.tmx')):
        out['assets/tiles/' + p.name] = p.read_text()
    return out


ENGINE = r"""/* ===== Oficina 2: EdgeInsets lido pelo Flame (margin do joystick e dos botões) ===== */
function edgeOf(v){var r=String(pcol(v)||'').trim().replace(/^const\s+/,''),o={l:0,t:0,r:0,b:0},m;
  function num(s){s=String(s).trim();if(/^-?[\d.]+$/.test(s))return +s;try{return nn(ST.value(s))}catch(e){return 0}}
  if((m=/^EdgeInsets\.all\(([^)]*)\)/.exec(r))){var a=num(m[1]);o={l:a,t:a,r:a,b:a}}
  else if((m=/^EdgeInsets\.fromLTRB\(([^)]*)\)/.exec(r))){var q=m[1].split(',').map(num);o={l:q[0]||0,t:q[1]||0,r:q[2]||0,b:q[3]||0}}
  else if((m=/^EdgeInsets\.(?:only|symmetric)\(([^)]*)\)/.exec(r))){m[1].split(',').forEach(function(pt){var k=/^\s*(\w+)\s*:\s*([\s\S]+)$/.exec(pt);if(!k)return;var x=num(k[2]);
    if(k[1]==='left')o.l=x;else if(k[1]==='top')o.t=x;else if(k[1]==='right')o.r=x;else if(k[1]==='bottom')o.b=x;else if(k[1]==='horizontal'){o.l=o.r=x}else if(k[1]==='vertical'){o.t=o.b=x}})}
  else if(r==='EdgeInsets.zero'){}
  return o}
/* ===== Oficina 2: Forge2D simplificado (corpos rígidos com círculos, polígonos e arestas) ===== */
var B2={ids:0};
function b2tipo(b){var t=String(pcol(b.f.bodyType)||'static');return /dynamic/.test(t)?'d':/kinematic/.test(t)?'k':'s'}
function b2rot(a,x,y){var c=Math.cos(a),s=Math.sin(a);return[c*x-s*y,s*x+c*y]}
function b2polyMass(v,d){var n=v.length;if(n<3)return{m:0,c:[0,0],I:0};var A=0,cx=0,cy=0,I=0;
  for(var i=0;i<n;i++){var e1=v[i],e2=v[(i+1)%n],cr=e1[0]*e2[1]-e1[1]*e2[0],a=cr/2;A+=a;cx+=a*(e1[0]+e2[0])/3;cy+=a*(e1[1]+e2[1])/3;
    I+=(0.25/3*cr)*((e1[0]*e1[0]+e2[0]*e1[0]+e2[0]*e2[0])+(e1[1]*e1[1]+e2[1]*e1[1]+e2[1]*e2[1]))}
  if(A<0){A=-A;cx=-cx;cy=-cy;I=-I}if(A<1e-12)return{m:0,c:[0,0],I:0};return{m:d*A,c:[cx/A,cy/A],I:d*I}}
function b2forma(fx){var sh=fx.f.shape;if(!sh||!sh.cls)throw exc('FixtureDef precisa de um shape (CircleShape, PolygonShape, EdgeShape ou ChainShape)');
  var c=sh.cls,f=fx.f.filter&&fx.f.filter.f||{};
  var s={id:fx.__bid||(fx.__bid=++B2.ids),fx:fx,sensor:fx.f.isSensor===true,fr:nn(fx.f.friction),re:nn(fx.f.restitution),de:nn(fx.f.density),
    cat:f.categoryBits!=null?nn(f.categoryBits):1,mask:f.maskBits!=null?nn(f.maskBits):65535,grp:f.groupIndex!=null?nn(f.groupIndex):0};
  if(isSub(c,'CircleShape')){s.k='c';s.c=[vx(sh.f.position),vy(sh.f.position)];s.r=nn(sh.f.radius)}
  else if(isSub(c,'PolygonShape')){s.k='p';s.v=toIter(sh.f.vertices).map(function(p){return[vx(p),vy(p)]});if(s.v.length<2)throw exc('PolygonShape sem vértices: use setAsBoxXY, setAsBox ou set')}
  else if(isSub(c,'EdgeShape')){s.k='p';s.v=[[vx(sh.f.vertex1),vy(sh.f.vertex1)],[vx(sh.f.vertex2),vy(sh.f.vertex2)]]}
  else if(isSub(c,'ChainShape')){s.k='chain';var pts=toIter(sh.f.pontos).map(function(p){return[vx(p),vy(p)]});s.segs=[];for(var i=0;i+1<pts.length;i++)s.segs.push([pts[i],pts[i+1]]);if(sh.f.fechada===true&&pts.length>2)s.segs.push([pts[pts.length-1],pts[0]])}
  else throw exc('Forma não suportada no Forge2D do simulador: '+c);
  return s}
function b2massa(b){var t=b2tipo(b),M=0,cx=0,cy=0,I=0;
  var fs=toIter(b.f.fixtures);fs.forEach(function(fx){var s=fx.__s=b2forma(fx);if(s.de<=0||s.k==='chain')return;var r;
    if(s.k==='c'){var m=s.de*Math.PI*s.r*s.r;r={m:m,c:s.c,I:m*(0.5*s.r*s.r+s.c[0]*s.c[0]+s.c[1]*s.c[1])}}else r=b2polyMass(s.v,s.de);
    M+=r.m;cx+=r.m*r.c[0];cy+=r.m*r.c[1];I+=r.I});
  var lc=[0,0];if(M>0){lc=[cx/M,cy/M];I-=M*(lc[0]*lc[0]+lc[1]*lc[1])}
  var p={t:t,lc:lc,invM:0,invI:0};
  if(t==='d'){if(M<=0){M=1;I=0}p.invM=1/M;p.invI=(I>0&&b.f.fixedRotation!==true)?1/I:0}
  b.__p=p;b.f.mass=new Dbl(t==='d'?M:0);b.f.inertia=new Dbl(t==='d'?I:0);b.f.localCenter=mkVec(lc[0],lc[1]);return p}
function b2p(b){return b.__p||b2massa(b)}
function b2centro(b){var p=b2p(b),r=b2rot(nn(b.f.angle),p.lc[0],p.lc[1]);return[vx(b.f.position)+r[0],vy(b.f.position)+r[1]]}
function b2cr(a,b){return a[0]*b[1]-a[1]*b[0]}
function b2prep(v){var n=v.length,ns=[];
  if(n===2){var ex=v[1][0]-v[0][0],ey=v[1][1]-v[0][1],l=Math.hypot(ex,ey)||1;ns=[[ey/l,-ex/l],[-ey/l,ex/l]]}
  else{var gx=0,gy=0;v.forEach(function(p){gx+=p[0];gy+=p[1]});gx/=n;gy/=n;
    for(var i=0;i<n;i++){var a=v[i],b=v[(i+1)%n],x=b[0]-a[0],y=b[1]-a[1],L=Math.hypot(x,y)||1,nx=y/L,ny=-x/L;if(nx*((a[0]+b[0])/2-gx)+ny*((a[1]+b[1])/2-gy)<0){nx=-nx;ny=-ny}ns.push([nx,ny])}}
  return{v:v,n:ns}}
function b2maxSep(A,B){var best=-Infinity,bi=0;for(var i=0;i<A.n.length;i++){var n=A.n[i],vi=A.v[i],s=Infinity;for(var j=0;j<B.v.length;j++){var d=(B.v[j][0]-vi[0])*n[0]+(B.v[j][1]-vi[1])*n[1];if(d<s)s=d}if(s>best){best=s;bi=i}}return{s:best,i:bi}}
function b2clip(pts,n,off){var out=[],d0=pts[0][0]*n[0]+pts[0][1]*n[1]-off,d1=pts[1][0]*n[0]+pts[1][1]*n[1]-off;
  if(d0<=0)out.push(pts[0]);if(d1<=0)out.push(pts[1]);
  if(d0*d1<0){var t=d0/(d0-d1);out.push([pts[0][0]+t*(pts[1][0]-pts[0][0]),pts[0][1]+t*(pts[1][1]-pts[0][1])])}return out}
function b2PP(A,B){var sa=b2maxSep(A,B);if(sa.s>0)return null;var sb=b2maxSep(B,A);if(sb.s>0)return null;
  var ref=A,inc=B,ri=sa.i,flip=false;if(sb.s>sa.s+1e-4){ref=B;inc=A;ri=sb.i;flip=true}
  var n=ref.n[ri],v1=ref.v[ri],v2=ref.v[(ri+1)%ref.v.length],ii=0,mn=Infinity;
  for(var j=0;j<inc.n.length;j++){var d=n[0]*inc.n[j][0]+n[1]*inc.n[j][1];if(d<mn){mn=d;ii=j}}
  var pts=[inc.v[ii],inc.v[(ii+1)%inc.v.length]],tx=v2[0]-v1[0],ty=v2[1]-v1[1],tl=Math.hypot(tx,ty)||1;tx/=tl;ty/=tl;
  pts=b2clip(pts,[-tx,-ty],-(tx*v1[0]+ty*v1[1]));if(pts.length<2)return null;pts=b2clip(pts,[tx,ty],tx*v2[0]+ty*v2[1]);if(pts.length<1)return null;
  var cs=[];pts.forEach(function(p){var sep=(p[0]-v1[0])*n[0]+(p[1]-v1[1])*n[1];if(sep<=0)cs.push({p:[p[0]-n[0]*sep/2,p[1]-n[1]*sep/2],depth:-sep})});
  if(!cs.length)return null;return{n:flip?[-n[0],-n[1]]:n,pts:cs}}
function b2PC(P,c,r){var sep=-Infinity,ni=0;for(var i=0;i<P.n.length;i++){var s=P.n[i][0]*(c[0]-P.v[i][0])+P.n[i][1]*(c[1]-P.v[i][1]);if(s>r)return null;if(s>sep){sep=s;ni=i}}
  if(sep<1e-9){var n=P.n[ni],dp=r-sep;return{n:n,pts:[{p:[c[0]-n[0]*(r-dp/2),c[1]-n[1]*(r-dp/2)],depth:dp}]}}
  var v1=P.v[ni],v2=P.v[(ni+1)%P.v.length],ex=v2[0]-v1[0],ey=v2[1]-v1[1],L2=ex*ex+ey*ey,u=L2?((c[0]-v1[0])*ex+(c[1]-v1[1])*ey)/L2:0;u=Math.max(0,Math.min(1,u));
  var q=[v1[0]+u*ex,v1[1]+u*ey],dx=c[0]-q[0],dy=c[1]-q[1],dist=Math.hypot(dx,dy);if(dist>r||dist<1e-12)return null;
  var nn2=[dx/dist,dy/dist],dep=r-dist;return{n:nn2,pts:[{p:[(q[0]+c[0]-nn2[0]*r)/2,(q[1]+c[1]-nn2[1]*r)/2],depth:dep}]}}
function b2CC(a,ra,b,rb){var dx=b[0]-a[0],dy=b[1]-a[1],d=Math.hypot(dx,dy);if(d>ra+rb)return null;var n=d>1e-9?[dx/d,dy/d]:[0,1],dep=ra+rb-d;
  return{n:n,pts:[{p:[a[0]+n[0]*(ra-dep/2),a[1]+n[1]*(ra-dep/2)],depth:dep}]}}
function b2mundo(S,s){var a=S.a,px=S.p[0],py=S.p[1];function tr(q){var r=b2rot(a,q[0],q[1]);return[r[0]+px,r[1]+py]}
  if(s.k==='c'){var c=tr(s.c);return[{k:'c',c:c,r:s.r,bb:[c[0]-s.r,c[1]-s.r,c[0]+s.r,c[1]+s.r]}]}
  function poly(v){var w=v.map(tr),xs=w.map(function(q){return q[0]}),ys=w.map(function(q){return q[1]}),P=b2prep(w);P.k='p';P.bb=[Math.min.apply(null,xs),Math.min.apply(null,ys),Math.max.apply(null,xs),Math.max.apply(null,ys)];return P}
  if(s.k==='p')return[poly(s.v)];return s.segs.map(poly)}
function b2colide(x,y){if(x.k==='c'&&y.k==='c')return b2CC(x.c,x.r,y.c,y.r);
  if(x.k==='p'&&y.k==='c')return b2PC(x,y.c,y.r);
  if(x.k==='c'&&y.k==='p'){var m=b2PC(y,x.c,x.r);if(m)m.n=[-m.n[0],-m.n[1]];return m}
  return b2PP(x,y)}
function b2filtro(a,b){if(a.grp===b.grp&&a.grp!==0)return a.grp>0;return (a.cat&b.mask)!==0&&(b.cat&a.mask)!==0}
function b2passo(w,dt){
  var corpos=toIter(w.f.bodies).filter(function(b){return b&&b.f.destruido!==true});
  var g=w.f.gravity?[vx(w.f.gravity),vy(w.f.gravity)]:[0,10];
  var S=corpos.map(function(b){var p=b2p(b),a=nn(b.f.angle),pos=[vx(b.f.position),vy(b.f.position)],r=b2rot(a,p.lc[0],p.lc[1]);
    return{b:b,t:p.t,lc:p.lc,invM:p.invM,invI:p.invI,a:a,p:pos,c:[pos[0]+r[0],pos[1]+r[1]],v:[vx(b.f.linearVelocity),vy(b.f.linearVelocity)],w:nn(b.f.angularVelocity),
      gs:b.f.gravityScale==null?1:nn(b.f.gravityScale),ld:nn(b.f.linearDamping),ad:nn(b.f.angularDamping),F:b.__F||[0,0,0],tq:nn(b.f.torque)||0,
      fx:toIter(b.f.fixtures).map(function(fx){return fx.__s||(fx.__s=b2forma(fx))})}});
  var ws=w.__ws||(w.__ws={}),novo={},toques={};
  var nSub=2,h=Math.min(dt,0.05)/nSub;
  for(var sub=0;sub<nSub;sub++){
    S.forEach(function(s){if(s.t!=='d')return;s.v[0]+=h*(g[0]*s.gs+s.F[0]*s.invM);s.v[1]+=h*(g[1]*s.gs+s.F[1]*s.invM);s.w+=h*(s.F[2]+s.tq)*s.invI;
      s.v[0]/=1+h*s.ld;s.v[1]/=1+h*s.ld;s.w/=1+h*s.ad});
    S.forEach(function(s){var r=b2rot(s.a,s.lc[0],s.lc[1]);s.p=[s.c[0]-r[0],s.c[1]-r[1]];s.W=[];s.fx.forEach(function(sh){b2mundo(s,sh).forEach(function(m){m.s=sh;s.W.push(m)})})});
    var cs=[];
    for(var i=0;i<S.length;i++)for(var j=i+1;j<S.length;j++){var A=S[i],B=S[j];if(A.t!=='d'&&B.t!=='d')continue;
      for(var a=0;a<A.W.length;a++)for(var bI=0;bI<B.W.length;bI++){var x=A.W[a],y=B.W[bI];
        if(x.bb[0]>y.bb[2]||y.bb[0]>x.bb[2]||x.bb[1]>y.bb[3]||y.bb[1]>x.bb[3])continue;
        if(!b2filtro(x.s,y.s))continue;var m=b2colide(x,y);if(!m)continue;
        var key=x.s.id<y.s.id?x.s.id+'_'+y.s.id:y.s.id+'_'+x.s.id;toques[key]={fa:x.s.fx,fb:y.s.fx};
        if(x.s.sensor||y.s.sensor)continue;
        cs.push({A:A,B:B,n:m.n,pts:m.pts,mu:Math.sqrt(Math.max(0,x.s.fr*y.s.fr)),e:Math.max(x.s.re,y.s.re),key:x.s.id+'_'+y.s.id})}}
    cs.forEach(function(c){var A=c.A,B=c.B,n=c.n,t=[n[1],-n[0]];
      c.pts.forEach(function(pt,k){pt.rA=[pt.p[0]-A.c[0],pt.p[1]-A.c[1]];pt.rB=[pt.p[0]-B.c[0],pt.p[1]-B.c[1]];
        var rnA=b2cr(pt.rA,n),rnB=b2cr(pt.rB,n),kn=A.invM+B.invM+A.invI*rnA*rnA+B.invI*rnB*rnB;pt.mn=kn>0?1/kn:0;
        var rtA=b2cr(pt.rA,t),rtB=b2cr(pt.rB,t),kt=A.invM+B.invM+A.invI*rtA*rtA+B.invI*rtB*rtB;pt.mt=kt>0?1/kt:0;
        var dv=[B.v[0]-B.w*pt.rB[1]-A.v[0]+A.w*pt.rA[1],B.v[1]+B.w*pt.rB[0]-A.v[1]-A.w*pt.rA[0]],vn=dv[0]*n[0]+dv[1]*n[1];
        pt.bias=0.2/h*Math.max(0,pt.depth-0.005);pt.bounce=vn<-1?-c.e*vn:0;
        var old=ws[c.key+'_'+k];pt.jn=old?old[0]:0;pt.jt=old?old[1]:0;
        var P=[n[0]*pt.jn+t[0]*pt.jt,n[1]*pt.jn+t[1]*pt.jt];b2aplica(A,B,pt,P)});c.t=t});
    for(var it=0;it<8;it++)cs.forEach(function(c){var A=c.A,B=c.B,n=c.n,t=c.t;
      c.pts.forEach(function(pt){
        var dv=[B.v[0]-B.w*pt.rB[1]-A.v[0]+A.w*pt.rA[1],B.v[1]+B.w*pt.rB[0]-A.v[1]-A.w*pt.rA[0]],vn=dv[0]*n[0]+dv[1]*n[1];
        var dj=pt.mn*(-vn+Math.max(pt.bias,pt.bounce)),j0=pt.jn;pt.jn=Math.max(j0+dj,0);dj=pt.jn-j0;b2aplica(A,B,pt,[n[0]*dj,n[1]*dj]);
        dv=[B.v[0]-B.w*pt.rB[1]-A.v[0]+A.w*pt.rA[1],B.v[1]+B.w*pt.rB[0]-A.v[1]-A.w*pt.rA[0]];var vt=dv[0]*t[0]+dv[1]*t[1],mx=c.mu*pt.jn,t0=pt.jt;
        pt.jt=Math.max(-mx,Math.min(mx,t0-pt.mt*vt));var djt=pt.jt-t0;b2aplica(A,B,pt,[t[0]*djt,t[1]*djt])})});
    cs.forEach(function(c){c.pts.forEach(function(pt,k){novo[c.key+'_'+k]=[pt.jn,pt.jt]})});
    S.forEach(function(s){if(s.t==='s')return;s.c[0]+=h*s.v[0];s.c[1]+=h*s.v[1];s.a+=h*s.w});
  }
  w.__ws=novo;
  S.forEach(function(s){var b=s.b;b.__F=null;if(s.t!=='s'){var r=b2rot(s.a,s.lc[0],s.lc[1]);var pos=b.f.position;pos.f.x=new Dbl(s.c[0]-r[0]);pos.f.y=new Dbl(s.c[1]-r[1]);b.f.angle=new Dbl(s.a);
      b.f.linearVelocity.f.x=new Dbl(s.v[0]);b.f.linearVelocity.f.y=new Dbl(s.v[1]);b.f.angularVelocity=new Dbl(s.w)}
    b.f.torque=new Dbl(0);var cp=b.f.componente;if(cp&&cp.f){cp.f.position=b.f.position;cp.f.angle=b.f.angle}});
  var antes=w.__toques||{};w.__toques=toques;
  Object.keys(toques).forEach(function(k){if(!antes[k])b2evento('beginContact',toques[k])});
  Object.keys(antes).forEach(function(k){if(!toques[k])b2evento('endContact',antes[k])});
  return null}
function b2aplica(A,B,pt,P){A.v[0]-=P[0]*A.invM;A.v[1]-=P[1]*A.invM;A.w-=A.invI*b2cr(pt.rA,P);B.v[0]+=P[0]*B.invM;B.v[1]+=P[1]*B.invM;B.w+=B.invI*b2cr(pt.rB,P)}
function b2evento(nome,par){var fa=par.fa,fb=par.fb,A=fa.f.body,B=fb.f.body;if(!A||!B)return;if(A.f.destruido===true||B.f.destruido===true)return;
  var uA=fa.f.userData!=null?fa.f.userData:A.f.userData,uB=fb.f.userData!=null?fb.f.userData:B.f.userData;
  var ct={nat:'FlEvent',f:{fixtureA:fa,fixtureB:fb,bodyA:A,bodyB:B,isTouching:true,isEnabled:true},src:'Contact'};
  if(uA&&uA.cls&&flHas(uA,nome))flCall(uA,nome,[uB,ct]);
  if(uB&&uB.cls&&flHas(uB,nome))flCall(uB,nome,[uA,ct])}
function b2testa(fx,pt){var b=fx.f.body,s=fx.__s||(fx.__s=b2forma(fx)),a=nn(b.f.angle),l=b2rot(-a,vx(pt)-vx(b.f.position),vy(pt)-vy(b.f.position));
  if(s.k==='c')return Math.hypot(l[0]-s.c[0],l[1]-s.c[1])<=s.r;
  if(s.k==='p'&&s.v.length>2){var P=b2prep(s.v);for(var i=0;i<P.n.length;i++)if(P.n[i][0]*(l[0]-P.v[i][0])+P.n[i][1]*(l[1]-P.v[i][1])>0)return false;return true}
  return false}
function b2desenha(comp,cv){var b=comp.f.body;if(!b||!b.f)return null;var paint=comp.f.paint;
  toIter(b.f.fixtures).forEach(function(fx){var s=fx.__s||(fx.__s=b2forma(fx));
    if(s.k==='c'){cvCall(cv,'drawCircle',[mkOffset(s.c[0],s.c[1]),new Dbl(s.r),paint]);return}
    var lp={nat:'Paint',f:{color:paint&&paint.f&&paint.f.color||{raw:'Color(0xFFFFFFFF)'},style:'PaintingStyle.stroke',strokeWidth:new Dbl(0.15),strokeCap:'StrokeCap.round',strokeJoin:'StrokeJoin.round'},src:'Paint()'};
    if(s.k==='p'&&s.v.length===2){cvCall(cv,'drawLine',[mkOffset(s.v[0][0],s.v[0][1]),mkOffset(s.v[1][0],s.v[1][1]),lp]);return}
    if(s.k==='chain'){s.segs.forEach(function(sg){cvCall(cv,'drawLine',[mkOffset(sg[0][0],sg[0][1]),mkOffset(sg[1][0],sg[1][1]),lp])});return}
    var d='M'+s.v.map(function(q){return q[0]+' '+q[1]}).join(' L')+' Z';cvCall(cv,'drawPath',[{nat:'Path',f:{},st:{d:d,cx:0,cy:0,sx:0,sy:0,has:true},src:'Path()'},paint])});
  return null}
/* ===== Oficina 2: mapas do Tiled (.tmx com camadas de blocos e de objetos) ===== */
var TL={cache:{},img:{}};
function tlTexto(nome){var s=String(nome),M=window.OF_MAPS||{};if(M[s])return{k:s,t:M[s]};var base=s.split('/').pop();
  var ks=Object.keys(M);for(var i=0;i<ks.length;i++)if(ks[i].split('/').pop()===base)return{k:ks[i],t:M[ks[i]]};
  throw exc('Unable to load asset: "'+s+'". O simulador tem estes mapas: '+ks.map(function(x){return x.split('/').pop()}).join(', ')+'. Mapas seus entram pelo botão 🖼 Sprites.')}
function tlNum(x,d){var v=parseFloat(x);return isFinite(v)?v:(d||0)}
function tlDados(el,w,h){var dt=el.querySelector('data');if(!dt)return[];var enc=dt.getAttribute('encoding'),cmp=dt.getAttribute('compression'),out=[];
  if(cmp)throw exc('Mapa com camada comprimida ('+cmp+'): no Tiled, em Mapa > Propriedades do mapa, troque o formato da camada para CSV.');
  if(enc==='csv')out=dt.textContent.trim().split(/\s*,\s*/).map(function(x){return Number(x)>>>0});
  else if(enc==='base64'){var bin=atob(dt.textContent.trim());for(var i=0;i+3<bin.length;i+=4)out.push((bin.charCodeAt(i)|(bin.charCodeAt(i+1)<<8)|(bin.charCodeAt(i+2)<<16)|(bin.charCodeAt(i+3)<<24))>>>0)}
  else dt.querySelectorAll('tile').forEach(function(t){out.push(Number(t.getAttribute('gid')||0)>>>0)});
  while(out.length<w*h)out.push(0);return out}
function tlProps(el){var o={};if(!el)return o;var ps=el.querySelector(':scope > properties');if(!ps)return o;
  ps.querySelectorAll(':scope > property').forEach(function(p){var t=p.getAttribute('type')||'string',v=p.getAttribute('value');if(v==null)v=p.textContent;
    o[p.getAttribute('name')]=t==='int'?parseInt(v,10):t==='float'?parseFloat(v):t==='bool'?v==='true':v});return o}
function tlParse(nome){var tx=tlTexto(nome);if(TL.cache[tx.k]&&TL.cache[tx.k].src===tx.t)return TL.cache[tx.k];
  var doc=new DOMParser().parseFromString(tx.t,'application/xml'),mp=doc.querySelector('map');if(!mp||doc.querySelector('parsererror'))throw exc('O arquivo '+tx.k.split('/').pop()+' não é um mapa .tmx válido.');
  if((mp.getAttribute('orientation')||'orthogonal')!=='orthogonal')throw exc('O simulador só lê mapas ortogonais (quadrados) do Tiled.');
  var W=tlNum(mp.getAttribute('width')),H=tlNum(mp.getAttribute('height')),tw=tlNum(mp.getAttribute('tilewidth')),th=tlNum(mp.getAttribute('tileheight'));
  var sets=[];mp.querySelectorAll(':scope > tileset').forEach(function(ts){if(ts.getAttribute('source'))throw exc('O tileset '+ts.getAttribute('source')+' está num arquivo separado (.tsx). No Tiled, use "Embed tileset" (incorporar) antes de exportar.');
    var im=ts.querySelector('image');if(!im)return;sets.push({first:tlNum(ts.getAttribute('firstgid'),1),tw:tlNum(ts.getAttribute('tilewidth'),tw),th:tlNum(ts.getAttribute('tileheight'),th),
      cols:tlNum(ts.getAttribute('columns'),1)||1,sp:tlNum(ts.getAttribute('spacing')),mg:tlNum(ts.getAttribute('margin')),img:im.getAttribute('source')})});
  sets.sort(function(a,b){return a.first-b.first});
  var camadas=[];
  (function andar(pai){Array.prototype.forEach.call(pai.children,function(el){var nm=el.getAttribute('name')||'',vis=el.getAttribute('visible')!=='0';
    if(el.tagName==='layer')camadas.push({k:'tiles',nome:nm,vis:vis,op:tlNum(el.getAttribute('opacity'),1),d:tlDados(el,W,H)});
    else if(el.tagName==='objectgroup'){var obs=[];el.querySelectorAll(':scope > object').forEach(function(o){
      obs.push({id:tlNum(o.getAttribute('id')),name:o.getAttribute('name')||'',type:o.getAttribute('type')||o.getAttribute('class')||'',x:tlNum(o.getAttribute('x')),y:tlNum(o.getAttribute('y')),
        w:tlNum(o.getAttribute('width')),h:tlNum(o.getAttribute('height')),rot:tlNum(o.getAttribute('rotation')),gid:tlNum(o.getAttribute('gid')),props:tlProps(o)})});camadas.push({k:'objetos',nome:nm,vis:vis,obs:obs})}
    else if(el.tagName==='group')andar(el)})})(mp);
  var r={src:tx.t,k:tx.k,W:W,H:H,tw:tw,th:th,sets:sets,camadas:camadas};TL.cache[tx.k]=r;return r}
function tlImg(src){var base=String(src).split('/').pop(),I=window.OF_SPRITE_IMG||{};if(I['assets/sprites/'+base])return I['assets/sprites/'+base];
  var ks=Object.keys(I);for(var i=0;i<ks.length;i++)if(ks[i].split('/').pop()===base)return I[ks[i]];return null}
function tlCompor(m){if(m.chave&&window.OF_SPRITE_IMG[m.chave])return m.chave;
  for(var i=0;i<m.sets.length;i++){var im=tlImg(m.sets[i].img);if(!im)throw exc('O mapa usa a imagem '+m.sets[i].img+', que não está nos sprites. Acrescente o tileset pelo botão 🖼 Sprites.');if(!im.complete||!im.naturalWidth)return null}
  var c=document.createElement('canvas');c.width=Math.max(1,m.W*m.tw);c.height=Math.max(1,m.H*m.th);var g=c.getContext('2d');g.imageSmoothingEnabled=false;
  m.camadas.forEach(function(L){if(L.k!=='tiles'||!L.vis)return;g.globalAlpha=L.op;
    for(var y=0;y<m.H;y++)for(var x=0;x<m.W;x++){var raw=L.d[y*m.W+x]>>>0,gid=raw&0x1FFFFFFF;if(!gid)continue;var ts=null;
      for(var s=m.sets.length-1;s>=0;s--)if(gid>=m.sets[s].first){ts=m.sets[s];break}if(!ts)continue;var ix=gid-ts.first,cx=ix%ts.cols,cy=Math.floor(ix/ts.cols),
      sx=ts.mg+cx*(ts.tw+ts.sp),sy=ts.mg+cy*(ts.th+ts.sp),fh=(raw&0x80000000)!==0,fv=(raw&0x40000000)!==0,dx=x*m.tw,dy=(y+1)*m.th-ts.th;
      g.save();g.translate(dx+(fh?ts.tw:0),dy+(fv?ts.th:0));g.scale(fh?-1:1,fv?-1:1);g.drawImage(tlImg(ts.img),sx,sy,ts.tw,ts.th,0,0,ts.tw,ts.th);g.restore()}});
  var chave='__tl:'+m.k+':'+(++TL.n||(TL.n=1)),uri=c.toDataURL(),img=new Image();img.src=uri;
  window.OF_SPRITES[chave]={w:c.width,h:c.height,q:1,desc:'mapa',uri:uri,interno:true};window.OF_SPRITE_IMG[chave]=img;m.chave=chave;return chave}
var FLN_EXTRA={
  __flVisible:function(cam){var g=flRootOf(cam);if(!g){Object.keys(FL.byKey).forEach(function(k){var e=FL.byKey[k];if(e&&e.game&&e.game.f.camera===cam)g=e.game})}
    var t=g?FL.camT(g):{ax:0,ay:0,z:1,px:0,py:0},w=g?vx(g.f.size):360,h=g?vy(g.f.size):640;return mkRect(t.px-t.ax/t.z,t.py-t.ay/t.z,w/t.z,h/t.z)},
  __flMargem:function(mg,tam,c){var e=edgeOf(mg),W=vx(tam),H=vy(tam),w=vx(c.f.size),h=vy(c.f.size),ax=nn(c.f.anchor.f.x),ay=nn(c.f.anchor.f.y);
    var x=(e.l!==0||e.r===0)?e.l+w*ax:W-e.r-w*(1-ax),y=(e.t!==0||e.b===0)?e.t+h*ay:H-e.b-h*(1-ay);return mkVec(x,y)},
  __flDirecao:function(d){var x=vx(d),y=vy(d);if(!x&&!y)return 8;var a=Math.atan2(y,x)*180/Math.PI;
    if(a>-22.5&&a<=22.5)return 3;if(a>22.5&&a<=67.5)return 5;if(a>67.5&&a<=112.5)return 4;if(a>112.5&&a<=157.5)return 6;if(a>157.5||a<=-157.5)return 7;if(a>-157.5&&a<=-112.5)return 1;if(a>-112.5&&a<=-67.5)return 0;return 2},
  __flPathAt:function(p,t){var el=flPathEl(p),L=el.getTotalLength(),q=el.getPointAtLength(Math.max(0,Math.min(1,nn(t)))*L);return mkVec(q.x,q.y)},
  __flPathAngle:function(p,t){var el=flPathEl(p),L=el.getTotalLength(),s=Math.max(0,Math.min(1,nn(t)))*L,a=el.getPointAtLength(Math.max(0,s-0.5)),b=el.getPointAtLength(Math.min(L,s+0.5));return new Dbl(Math.atan2(b.y-a.y,b.x-a.x))},
  __flTelaParaMundo:function(g,p){var t=FL.camT(g);return mkVec((vx(p)-t.ax)/t.z+t.px,(vy(p)-t.ay)/t.z+t.py)},
  __flMundoParaTela:function(g,p){var t=FL.camT(g);return mkVec((vx(p)-t.px)*t.z+t.ax,(vy(p)-t.py)*t.z+t.ay)},
  __b2Caixa:function(hx,hy,c,a){var A=nn(a),cx=vx(c),cy=vy(c);return[[-1,-1],[1,-1],[1,1],[-1,1]].map(function(k){var r=b2rot(A,k[0]*nn(hx),k[1]*nn(hy));return mkVec(r[0]+cx,r[1]+cy)})},
  __b2Escala:function(g){return new Dbl(isVec(g)?vy(g):nn(g))},
  __b2Massa:function(b){b2massa(b);return null},
  __b2Impulso:function(b,im,pt){var p=b2p(b);if(p.t!=='d')return null;var ix=vx(im),iy=vy(im),lv=b.f.linearVelocity;lv.f.x=new Dbl(vx(lv)+ix*p.invM);lv.f.y=new Dbl(vy(lv)+iy*p.invM);
    if(pt!=null){var c=b2centro(b),r=[vx(pt)-c[0],vy(pt)-c[1]];b.f.angularVelocity=new Dbl(nn(b.f.angularVelocity)+p.invI*(r[0]*iy-r[1]*ix))}return null},
  __b2Forca:function(b,f,pt){var F=b.__F||(b.__F=[0,0,0]),fx=vx(f),fy=vy(f);F[0]+=fx;F[1]+=fy;if(pt!=null){var c=b2centro(b);F[2]+=(vx(pt)-c[0])*fy-(vy(pt)-c[1])*fx}return null},
  __b2ImpulsoAngular:function(b,i){var p=b2p(b);if(p.t==='d')b.f.angularVelocity=new Dbl(nn(b.f.angularVelocity)+p.invI*nn(i));return null},
  __b2Centro:function(b){var c=b2centro(b);return mkVec(c[0],c[1])},
  __b2PontoMundo:function(b,l){var r=b2rot(nn(b.f.angle),vx(l),vy(l));return mkVec(r[0]+vx(b.f.position),r[1]+vy(b.f.position))},
  __b2PontoLocal:function(b,p){var r=b2rot(-nn(b.f.angle),vx(p)-vx(b.f.position),vy(p)-vy(b.f.position));return mkVec(r[0],r[1])},
  __b2VetorMundo:function(b,l){var r=b2rot(nn(b.f.angle),vx(l),vy(l));return mkVec(r[0],r[1])},
  __b2TestPoint:function(fx,p){return b2testa(fx,p)},
  __b2Passo:function(w,dt){return b2passo(w,nn(dt))},
  __b2Desenhar:function(c,cv){return b2desenha(c,cv)},
  __b2Mundo:function(c){var o=c.f.parent,s=0;while(o&&s++<200){if(flIs(o,'Forge2DWorld'))return o;o=o.f&&o.f.parent}var g=flRootOf(c);
    if(g&&g.f.world&&flIs(g.f.world,'Forge2DWorld'))return g.f.world;throw exc('BodyComponent precisa estar num Forge2DGame: use world.add(...) dentro do onLoad.')},
  __tlCarregar:function(nome){var m=tlParse(nome);
    var camadas=m.camadas.map(function(L){if(L.k==='tiles')return['tiles',L.nome,L.d.map(function(x){return x&0x1FFFFFFF})];
      return['objetos',L.nome,L.obs.map(function(o){return[o.id,o.name,o.type,new Dbl(o.x),new Dbl(o.y),new Dbl(o.w),new Dbl(o.h),new Dbl(o.rot),o.gid,o.props]})]});
    return[m.W,m.H,m.tw,m.th,camadas,{nat:'TlData',f:{},tl:m,src:'TiledMap'}]},
  __tlProps:function(o){return jsonConv(o||{})},
  __tlDesenhar:function(c,cv){var d=c.f.tileMap.f.dados,m=d&&d.tl;if(!m)return null;var k=tlCompor(m);if(!k)return null;var im=window.OF_SPRITE_IMG[k];if(!im||!im.complete||!im.naturalWidth)return null;
    var ds=c.f.tileMap.f.destTileSize;cvCall(cv,'drawImageRect',[mkImg(k),mkRect(0,0,m.W*m.tw,m.H*m.th),mkRect(0,0,m.W*vx(ds),m.H*vy(ds)),null]);return null}
};
function flPathEl(p){if(!p||p.nat!=='Path')throw exc('MoveAlongPathEffect precisa de um Path');var d=p.st&&p.st.d||'';if(!d)throw exc('O Path está vazio: use moveTo, lineTo, quadraticBezierTo ou addOval');
  FL.paths=FL.paths||{};var el=FL.paths[d];if(!el){el=document.createElementNS('http://www.w3.org/2000/svg','path');el.setAttribute('d',d);FL.paths[d]=el}return el}
Object.keys(FLN_EXTRA).forEach(function(k){FLN[k]=FLN_EXTRA[k]});
ST.b2dbg={p:b2p,mundo:b2mundo,colide:b2colide};
"""


def patch(src):
    # ---- prelúdio: forge2d e tiled também ligam o Flame
    src = sub1(src, "ST.extract=function(src){src=stripComments(src);if(/package:flame\\//.test(src))",
               "ST.extract=function(src){src=stripComments(src);if(/package:flame(?:_forge2d|_tiled)?\\//.test(src))", 'extract forge2d')
    # ---- natives e motor de física: depois do FLN
    src = sub1(src, "/* ===== Oficina 2: curvas, pinça, consultas de componentes ===== */",
               ENGINE + "/* ===== Oficina 2: curvas, pinça, consultas de componentes ===== */", 'extra engine')
    # ---- BodyType.dynamic e EdgeInsets.left
    src = sub1(src,
        "  if(n==='rootBundle')return{nat:'Bundle',f:{},src:'rootBundle'};\n",
        "  if(n==='BodyType')return{nat:'BodyTypeNS',f:{},src:'BodyType'};\n"
        "  if(n==='rootBundle')return{nat:'Bundle',f:{},src:'rootBundle'};\n", 'lookup BodyType')
    src = sub1(src,
        "function member(v,name,args){\n  var targs=TARGS;TARGS=null;\n",
        "function member(v,name,args){\n  var targs=TARGS;TARGS=null;\n"
        "  if(v&&v.nat==='BodyTypeNS')return name;\n"
        "  if(v&&isRaw(v)&&/^\\s*(?:const\\s+)?EdgeInsets\\./.test(v.raw)&&/^(left|top|right|bottom|horizontal|vertical)$/.test(name)){var eo=edgeOf(v);return new Dbl(name==='left'?eo.l:name==='top'?eo.t:name==='right'?eo.r:name==='bottom'?eo.b:name==='horizontal'?eo.l+eo.r:eo.t+eo.b)}\n",
        'member BodyType/EdgeInsets')
    # ---- tinta (ColorEffect) carimbada nos comandos de desenho, como a opacidade
    src = sub1(src,
        "  var gaOld=cv.st.ga,opc=isP?nn(c.f.opacity):1;if(opc!=null&&opc<1)cv.st.ga=(gaOld==null?1:gaOld)*Math.max(0,opc);",
        "  var gaOld=cv.st.ga,opc=isP?nn(c.f.opacity):1;if(opc!=null&&opc<1)cv.st.ga=(gaOld==null?1:gaOld)*Math.max(0,opc);\n"
        "  var tiOld=cv.st.tint;if(isP&&c.f.tintColor!=null&&nn(c.f.tintAmount)>0)cv.st.tint={c:pcol(c.f.tintColor),a:Math.min(1,nn(c.f.tintAmount))};",
        'tint start')
    src = sub1(src, "  cv.st.ga=gaOld;cvCall(cv,'restore',[])};", "  cv.st.ga=gaOld;cv.st.tint=tiOld;cvCall(cv,'restore',[])};", 'tint end')
    src = sub1(src,
        "cv.st.ops.push=function(o){if(cv.st.ga!=null&&cv.st.ga<1&&o.ga==null)o.ga=cv.st.ga;",
        "cv.st.ops.push=function(o){if(cv.st.ga!=null&&cv.st.ga<1&&o.ga==null)o.ga=cv.st.ga;if(cv.st.tint&&o.tint==null)o.tint=cv.st.tint;",
        'tint stamp')
    # ---- paintCanvas: transparência (OpacityEffect, botões) e tinta
    src = sub1(src,
        "    g.save();\n    if(o.clip>=0&&res.clips[o.clip]){",
        "    g.save();if(o.ga!=null)g.globalAlpha=Math.max(0,Math.min(1,o.ga));\n"
        "    if(o.tint&&o.k!=='img'){col=tintMix(col,o.tint)}\n"
        "    if(o.clip>=0&&res.clips[o.clip]){", 'canvas alpha')
    src = sub1(src,
        "g.imageSmoothingEnabled=/low|medium|high/.test(o.fq||'');var am=/rgba\\([^)]*,\\s*([\\d.]+)\\)/.exec(col);if(am)g.globalAlpha=+am[1];\n"
        "        g.drawImage(im,o.s[0],o.s[1],o.s[2],o.s[3],o.d[0],o.d[1],o.d[2],o.d[3]);break}",
        "g.imageSmoothingEnabled=/low|medium|high/.test(o.fq||'');var am=/rgba\\([^)]*,\\s*([\\d.]+)\\)/.exec(col);if(am)g.globalAlpha=(o.ga==null?1:o.ga)*(+am[1]);\n"
        "        if(o.tint){var tc=tintCanvas(im,o.s,o.tint);g.drawImage(tc,0,0,tc.width,tc.height,o.d[0],o.d[1],o.d[2],o.d[3])}else g.drawImage(im,o.s[0],o.s[1],o.s[2],o.s[3],o.d[0],o.d[1],o.d[2],o.d[3]);break}",
        'canvas img tint')
    src = sub1(src, "function paintCanvas(res,w,h){",
        "function tintMix(col,t){var a=tintRGB(col),b=tintRGB(pcssColor(t.c));if(!a||!b)return col;var k=t.a;"
        "return 'rgba('+Math.round(a[0]+(b[0]-a[0])*k)+','+Math.round(a[1]+(b[1]-a[1])*k)+','+Math.round(a[2]+(b[2]-a[2])*k)+','+a[3]+')'}\n"
        "var TINTC=document.createElement('canvas'),TINTK={};function tintRGB(c){if(TINTK[c])return TINTK[c];TINTC.width=TINTC.height=1;var g=TINTC.getContext('2d');g.clearRect(0,0,1,1);g.fillStyle='#000';g.fillStyle=c;g.fillRect(0,0,1,1);"
        "var d=g.getImageData(0,0,1,1).data,m=/rgba\\([^)]*,\\s*([\\d.]+)\\)/.exec(c);return TINTK[c]=[d[0],d[1],d[2],m?+m[1]:1]}\n"
        "function tintCanvas(im,s,t){var c=document.createElement('canvas');c.width=Math.max(1,Math.round(s[2]));c.height=Math.max(1,Math.round(s[3]));var g=c.getContext('2d');"
        "g.drawImage(im,s[0],s[1],s[2],s[3],0,0,c.width,c.height);g.globalCompositeOperation='source-atop';g.globalAlpha=t.a;g.fillStyle=pcssColor(t.c);g.fillRect(0,0,c.width,c.height);return c}\n"
        "function paintCanvas(res,w,h){", 'tint helpers')
    # ---- toque em BodyComponent: o ponto cai dentro de alguma fixture
    src = sub1(src,
        "if(flIs(c,mixin)&&flIs(c,'PositionComponent')){var iv=FL.inv(FL.mat(c));if(iv){var lp=FL.apply(iv,px,py);if(lp[0]>=0&&lp[1]>=0&&lp[0]<vx(c.f.size)&&lp[1]<vy(c.f.size))found={c:c,lx:lp[0],ly:lp[1]}}}}",
        "if(flIs(c,mixin)&&flIs(c,'PositionComponent')){var iv=FL.inv(FL.mat(c));if(iv){var lp=FL.apply(iv,px,py);"
        "if(flIs(c,'BodyComponent')){var bb=c.f.body;if(bb&&bb.f&&toIter(bb.f.fixtures).some(function(fx){return b2testa(fx,mkVec(px,py))}))found={c:c,lx:lp[0],ly:lp[1]}}"
        "else if(lp[0]>=0&&lp[1]>=0&&lp[0]<vx(c.f.size)&&lp[1]<vy(c.f.size))found={c:c,lx:lp[0],ly:lp[1]}}}}",
        'pick body')
    # ---- overlays vivos: ValueNotifier mudou durante o jogo -> redesenha os overlays
    src = sub1(src,
        "    if(o&&o.nat==='ValueNotifier'&&ast.name==='value'){if(o.f.value!==val){o.f.value=val;dirty=true}return}",
        "    if(o&&o.nat==='ValueNotifier'&&ast.name==='value'){if(o.f.value!==val){o.f.value=val;dirty=true;window.OF_VN_SUJO=true}return}",
        'vn dirty')
    src = sub1(src,
        "FL.live.slice().forEach(function(g){var ov=g.f.overlays",
        "if(window.OF_VN_SUJO&&!FL.vnT){window.OF_VN_SUJO=false;FL.vnT=setTimeout(function(){FL.vnT=0;if(window.OF.rerender)OF.rerender()},80)}\n  FL.live.slice().forEach(function(g){var ov=g.f.overlays",
        'vn rerender')
    # ---- arrasto: deslocamento pelas coordenadas da janela (o celular pode mudar de lugar na página quando o painel Estado cresce)
    src = sub1(src,
        "function gwPos(el,e){var sr=screen.getBoundingClientRect(),k=sr.width/360||1,rc=el.getBoundingClientRect();return[(e.clientX-rc.left)/k,(e.clientY-rc.top)/k]}",
        "function gwPos(el,e){var sr=screen.getBoundingClientRect(),k=sr.width/360||1;if(!el.isConnected){var nv=screen.querySelector('.gw[data-gwk=\"'+el.dataset.gwk+'\"]');if(nv)el=nv}var rc=el.getBoundingClientRect();var r=[(e.clientX-rc.left)/k,(e.clientY-rc.top)/k];r.c=[e.clientX/k,e.clientY/k];return r}",
        'gwPos')
    src = sub1(src,
        "var d=gwPtr[e.pointerId];if(!d)return;var p=gwPos(d.el,e),dx=p[0]-d.last[0],dy=p[1]-d.last[1];if(!dx&&!dy)return;",
        "var d=gwPtr[e.pointerId];if(!d)return;var p=gwPos(d.el,e),dx=p.c[0]-d.last.c[0],dy=p.c[1]-d.last.c[1];if(!dx&&!dy)return;",
        'gw delta')
    src = sub1(src,
        "  var p=gPos(d.el,e),dx=p.g[0]-d.last.g[0],dy=p.g[1]-d.last.g[1];",
        "  var p=gPos(d.el,e);p.c=[e.clientX/p.k,e.clientY/p.k];var dx=p.c[0]-d.last.c[0],dy=p.c[1]-d.last.c[1];",
        'pan delta')
    src = sub1(src,
        "    dx=p.g[0]-d.start.g[0];dy=p.g[1]-d.start.g[1]}",
        "    dx=p.c[0]-d.start.c[0];dy=p.c[1]-d.start.c[1]}", 'pan delta start')
    src = sub1(src,
        "  if(de){var p1=gPos(de,e);gDrag=",
        "  if(de){var p1=gPos(de,e);p1.c=[e.clientX/p1.k,e.clientY/p1.k];gDrag=", 'pan start c')
    src = sub1(src,
        "    if(dcm.getters[name])return evalGetter(v,dcm.getters[name]);\n    if(dcm.methods[name])return runMethod(dcm.methods[name],args,v);\n    throw new Error('membro '+v.cls+'.'+name)}",
        "    if(hasOwn(dcm.getters,name))return evalGetter(v,dcm.getters[name]);\n    if(hasOwn(dcm.methods,name))return runMethod(dcm.methods[name],args,v);\n"
        "    if(name==='toString')return v.enumv?v.cls+'.'+v.f.name:\"Instance of '\"+v.cls+\"'\";if(name==='hashCode')return flId(v);if(name==='runtimeType')return v.cls;\n"
        "    throw new Error('membro '+v.cls+'.'+name)}", 'member hasOwn')
    src = sub1(src, "if(FLN[a.name]&&a.name.indexOf('__fl')===0){", "if(FLN[a.name]&&/^__(?:fl|b2|tl)/.test(a.name)){", 'FLN prefixes')
    # ---- construtores: super(...) também roda o corpo do construtor da classe mãe, e sem super(...) explícito chama o padrão
    src = sub1(src,
        "      if(sm){var pc=dc.ext&&ST.dataClasses[dc.ext];if(pc){var pa=evalArgs(pPrim(new Ps('X('+sm[1]+')')),envI);initFrom(pc,pc.params,pc.cinit,pa,o)}}",
        "      if(sm){supOk=true;var pc=dc.ext&&ST.dataClasses[dc.ext];if(pc){var pa=evalArgs(pPrim(new Ps('X('+sm[1]+')')),envI);var pv=initFrom(pc,pc.params,pc.cinit,pa,o);superBody(pc,pv,o)}}",
        'super body')
    src = sub1(src,
        "function initFrom(dc,params,init,args,o){\n  var vals=bindArgs(params,args);",
        "function superBody(pc,pv,o){if(pc.cbody&&pc.cbody.length>2&&!pc.fromHack){try{runCtorBody({name:'<ctor>',params:'',body:pc.cbody,arrow:false,owner:pc.name},pv,o)}catch(e){if(e.dartExc)throw e}}}\n"
        "function initFrom(dc,params,init,args,o){\n  var vals=bindArgs(params,args),supOk=false;",
        'initFrom flag')
    src = sub1(src,
        "      else if(am&&!/^assert/.test(it)){try{o.f[am[1]]=coerce(fieldType(dc,am[1]),ev(pTern(new Ps(am[2])),envI))}catch(e){if(e.dartExc)throw e}}})}\n  return vals}",
        "      else if(am&&!/^assert/.test(it)){try{o.f[am[1]]=coerce(fieldType(dc,am[1]),ev(pTern(new Ps(am[2])),envI))}catch(e){if(e.dartExc)throw e}}})}\n"
        "  if(!supOk&&!dc.fromHack&&dc.ext&&ST.dataClasses[dc.ext]&&ST.dataClasses.Component&&isSub(dc.name,'Component')){var ipc=ST.dataClasses[dc.ext];var ipv=initFrom(ipc,ipc.params,ipc.cinit,[],o);superBody(ipc,ipv,o)}\n"
        "  return vals}",
        'implicit super')
    src = sub1(src,
        "    if(!ci.params.length&&!ci.cinit&&ci.ext){var pc=info.classes[ci.ext].ci;ci.params=pc.params;ci.cinit=pc.cinit}}",
        "    if(!ci.params.length&&!ci.cinit&&ci.ext){var pc=info.classes[ci.ext].ci;ci.params=pc.params;ci.cinit=pc.cinit;ci.fromHack=true}}",
        'fromHack')
    src = sub1(src, "  if(!((ST.re&&ST.re.test(raw))||/\\$|\\?|[*\\/%]|\\d\\s*[+-]\\s*\\d|\\[|\\bwidget\\b/.test(raw)))return raw;",
        "  if(!((ST.re&&ST.re.test(raw))||/\\$|\\?|[*\\/%]|\\d\\s*[+-]\\s*\\d|\\[|\\bwidget\\b|__flg\\d/.test(raw)))return raw;", 'subst flg')
    src = sub1(src, ".nd.gw{display:block}", ".nd.gw{display:block;touch-action:none;user-select:none;-webkit-user-select:none;-webkit-touch-callout:none}", 'gw touch')
    # ---- janela separada (⤢ Janela) com jogos: quadros do canvas, arrasto, teclado e laço que não para
    src = sub1(src,
        "  if(ch)try{patchRender()}catch(e2){}\n  animKick()}",
        "  if(ch)try{patchRender()}catch(e2){}\n  window.__ofPasso=performance.now();if(typeof popFrame==='function')popFrame();\n  animKick()}",
        'anim pop frame')
    src = sub1(src,
        "function popSched(){if(!popRaf)popRaf=requestAnimationFrame(popSync)}",
        "function popSched(){if(!popRaf)popRaf=requestAnimationFrame(popSync)}\n"
        "function popFrame(){if(!popW||popRaf)return;if(!popAlive()){popStop();return}var m=popW.document.getElementById('pmirror');"
        "var ca=screen.querySelectorAll('canvas'),cb=m.querySelectorAll('canvas');if(ca.length!==cb.length){popSched();return}"
        "for(var k=0;k<ca.length;k++){try{if(cb[k].width!==ca[k].width||cb[k].height!==ca[k].height){cb[k].width=ca[k].width;cb[k].height=ca[k].height}var g=cb[k].getContext('2d');g.clearRect(0,0,cb[k].width,cb[k].height);g.drawImage(ca[k],0,0)}catch(e){}}}\n"
        "function popLaco(){if(!popAlive())return;var agora=performance.now();"
        "if(ST.anims&&ST.anims.length&&agora-(window.__ofPasso||0)>45){if(animRaf){cancelAnimationFrame(animRaf);animRaf=0}animStep()}"
        "if(window.OF_MUSIC&&OF_MUSIC.tickAll)OF_MUSIC.tickAll();popW.requestAnimationFrame(popLaco)}\n"
        "OF.popKey=function(tipo,e){var n=kName(e);if(tipo==='keydown'){if(!(S.run&&ST.active))return false;ST.keys.add(n);var u=kDispatch(e.repeat?'KeyRepeatEvent':'KeyDownEvent',e);return !!(u||gLoop()||(ST.flameLive&&ST.flameLive()))}"
        "ST.keys.delete(n);if(!(S.run&&ST.active))return false;kDispatch('KeyUpEvent',e);return true};",
        'pop frame fn')
    src = sub1(src,
        "  if(t==='pointermove'){document.dispatchEvent(new PointerEvent(t,init));return}\n"
        "  if(t==='pointerup'||t==='pointercancel'){popDown=false;(mp.el||document).dispatchEvent(new PointerEvent(t,init));return}",
        "  if(t==='pointermove'){(screen.contains(mp.el)?mp.el:screen).dispatchEvent(new PointerEvent(t,init));return}\n"
        "  if(t==='pointerup'||t==='pointercancel'){popDown=false;(screen.contains(mp.el)?mp.el:screen).dispatchEvent(new PointerEvent(t,init));return}",
        'pop pointer fwd')
    src = sub1(src,
        "  if(t==='pointerdown'){if(!mp.el)return;popDown=true;mp.el.dispatchEvent(new PointerEvent(t,init));return}",
        "  if(t==='pointerdown'){if(!mp.el)return;popDown=true;if(e.target&&e.target.closest&&e.target.closest('.gw'))e.preventDefault();mp.el.dispatchEvent(new PointerEvent(t,init));return}",
        'pop pointerdown')
    src = sub1(src,
        "  ['input','change','keydown'].forEach(function(n){d.addEventListener(n,popField,true)});",
        "  ['input','change','keydown'].forEach(function(n){d.addEventListener(n,popField,true)});\n"
        "  ['keydown','keyup'].forEach(function(n){d.addEventListener(n,function(e){var a=d.activeElement;if(a&&/^(INPUT|TEXTAREA|SELECT)$/.test(a.tagName))return;"
        "if(OF.popKey(n,e)&&/^(arrow\\w+|space)$/.test(kName(e)))e.preventDefault()})});\n"
        "  w.addEventListener('blur',function(){ST.keys.clear()});\n"
        "  try{if(window.OF_AC){var acx=OF_AC();if(acx&&acx.resume)acx.resume()}}catch(e){}\n"
        "  w.requestAnimationFrame(popLaco);",
        'pop keys')
    src = sub1(src,
        "  if(t==='wheel'){if(mp.el&&mp.el.closest('.ivw[data-iv]')){e.preventDefault();mp.el.dispatchEvent(new WheelEvent('wheel',init))}}}",
        "  if(t==='wheel'){init.ctrlKey=e.ctrlKey;init.deltaX=e.deltaX||0;if(mp.el&&(mp.el.closest('.ivw[data-iv]')||(e.ctrlKey&&screen.contains(mp.el)))){e.preventDefault();mp.el.dispatchEvent(new WheelEvent('wheel',init))}}}",
        'pop wheel')
    src = sub1(src, "window.OF_MUSICAS=", global_js() + "window.OF_MUSICAS=", 'global maps')
    return src


SPRITES_UI_EXTRA = r"""<script>
(function(){
  /* mapas do Tiled: os prontos e os do aluno */
  try{var mm=JSON.parse(localStorage.getItem('oficina2.mapas')||'{}');Object.keys(mm).forEach(function(k){window.OF_MAPS[k]=mm[k]})}catch(e){}
})();
</script>
"""


def global_js():
    return 'window.OF_MAPS=' + json.dumps(maps_js(), ensure_ascii=False) + ';\n'
