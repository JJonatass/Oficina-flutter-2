# Oficina Flutter 2, frente 7f: Hive e Supabase simulados, Google Fonts de verdade e NestedScrollView com rolagem em duas etapas.
from patch_engine import sub1

GLOBAL = r"""/* ===== Oficina 2: Google Fonts carregadas sob demanda ===== */
(function(){var pedidas={},ESP={pressStart2p:'Press Start 2P',vt323:'VT323',ptSans:'PT Sans',ptSerif:'PT Serif',ptMono:'PT Mono',ibmPlexSans:'IBM Plex Sans',ibmPlexMono:'IBM Plex Mono',ibmPlexSerif:'IBM Plex Serif',
  dmSans:'DM Sans',dmSerifDisplay:'DM Serif Display',dmMono:'DM Mono',notoSansJp:'Noto Sans JP',mPlusRounded1c:'M PLUS Rounded 1c',pixelifySans:'Pixelify Sans',jetBrainsMono:'JetBrains Mono'};
  var BASE={'Press Start 2P':1,Silkscreen:1,VT323:1,Bungee:1,Roboto:1,'JetBrains Mono':1,'IBM Plex Sans':1,'Bricolage Grotesque':1};
  window.OF_GF_NOME=function(id){id=String(id||'');if(ESP[id])return ESP[id];
    return id.replace(/([a-z])([A-Z])/g,'$1 $2').replace(/([a-zA-Z])(\d)/g,'$1 $2').replace(/(\d)([a-z])/g,function(m,a,b){return a+b.toUpperCase()}).replace(/(^| )([a-z])/g,function(m,a,b){return a+b.toUpperCase()})};
  window.OF_GF_CARREGA=function(fam){if(!fam||BASE[fam]||pedidas[fam])return;pedidas[fam]=1;
    try{var l=document.createElement('link');l.rel='stylesheet';l.href='https://fonts.googleapis.com/css2?family='+encodeURIComponent(fam).replace(/%20/g,'+')+':ital,wght@0,400;0,700;1,400&display=swap';
      l.onload=function(){if(document.fonts&&document.fonts.load){Promise.all([document.fonts.load('400 16px "'+fam+'"'),document.fonts.load('700 16px "'+fam+'"')]).then(function(){if(window.OF&&OF.rerender)OF.rerender()},function(){})}};
      document.head.appendChild(l)}catch(e){}};
  window.OF_GF=function(id){var f=window.OF_GF_NOME(id);window.OF_GF_CARREGA(f);return f};
})();
"""

ENGINE = r"""/* ===== Oficina 2: Hive e Supabase simulados ===== */
if(!DBP.hive)DBP.hive={};if(!DBP.sb)DBP.sb={t:{},seq:{},users:{},cur:null};
var _dbClear1=ST.dbClear;ST.dbClear=function(){_dbClear1();DBP.hive={};DBP.sb={t:{},seq:{},users:{},cur:null};dbSave()};
var SBNAT={HiveBox:1,SbInst:1,SbClient:1,SbQ:1,SbAuth:1,SbUser:1,SbSession:1,SbAuthResp:1,SbAuthState:1,AuthException:1,PostgrestException:1,HiveError:1};
NATCLS.Hive=1;NATCTOR.UserAttributes=1;NATCLS.Supabase=1;NATCLS.AuthChangeEvent=1;
function hvKey(k){return k instanceof Dbl?k.v:k}
function hvBox(name){var b=DBP.hive[name];if(!b)b=DBP.hive[name]={e:[],ai:0};return b}
function hvIdx(b,k){k=hvKey(k);for(var i=0;i<b.e.length;i++)if(b.e[i][0]===k)return i;return -1}
function hvPut(b,k,v){k=hvKey(k);if(typeof k!=='number'&&typeof k!=='string')throw hvErr('Keys must be integers or strings');if(typeof k==='number'&&k>=b.ai)b.ai=k+1;var i=hvIdx(b,k),pv=fsPlain(v);if(i>=0)b.e[i][1]=pv;else b.e.push([k,pv])}
function hvErr(m){var e=exc('HiveError: '+m);e.val={nat:'HiveError',f:{message:m},src:'HiveError: '+m};return e}
function hvOpen(name){name=String(name).toLowerCase();hvBox(name);return{nat:'HiveBox',f:{name:name},name:name,src:"Instance of 'Box<dynamic>'"}}
function hvMember(v,name,a){
  a=a||[];var an=ARGN||[];ARGN=null;var pos=[],nm={};a.forEach(function(x,i){if(an[i])nm[an[i]]=x;else pos.push(x)});
  var b=hvBox(v.name),ch=function(r){dirty=true;dbSave();return r};
  switch(name){
    case 'name':return v.name;case 'isOpen':return true;case 'path':return '/simulador/'+v.name+'.hive';case 'lazy':return false;
    case 'put':hvPut(b,pos[0],pos[1]);return ch(null);
    case 'putAll':if(pos[0]&&pos[0].isMap)pos[0].m.forEach(function(x,k){hvPut(b,k,x)});return ch(null);
    case 'add':{var k=b.ai;hvPut(b,k,pos[0]);return ch(k)}
    case 'addAll':return ch((pos[0]||[]).map(function(x){var k=b.ai;hvPut(b,k,x);return k}));
    case 'get':{var i=hvIdx(b,pos[0]);if(i<0)return nm.defaultValue!==undefined?nm.defaultValue:null;return fsBack(b.e[i][1])}
    case 'getAt':{var gi=nn(pos[0]);if(gi<0||gi>=b.e.length)throw exc('RangeError (index): Index out of range: index should be less than '+b.e.length+': '+gi);return fsBack(b.e[gi][1])}
    case 'keyAt':{var ki=nn(pos[0]);if(ki<0||ki>=b.e.length)throw exc('RangeError (index): Index out of range: '+ki);return b.e[ki][0]}
    case 'putAt':{var pi=nn(pos[0]);if(pi<0||pi>=b.e.length)throw exc('RangeError (index): Index out of range: '+pi);b.e[pi][1]=fsPlain(pos[1]);return ch(null)}
    case 'delete':{var di=hvIdx(b,pos[0]);if(di>=0)b.e.splice(di,1);return ch(null)}
    case 'deleteAt':{var dd=nn(pos[0]);if(dd>=0&&dd<b.e.length)b.e.splice(dd,1);return ch(null)}
    case 'deleteAll':(pos[0]||[]).forEach(function(k){var j=hvIdx(b,k);if(j>=0)b.e.splice(j,1)});return ch(null);
    case 'clear':{var n0=b.e.length;b.e=[];return ch(n0)}
    case 'containsKey':return hvIdx(b,pos[0])>=0;
    case 'keys':return b.e.map(function(x){return x[0]});
    case 'values':return b.e.map(function(x){return fsBack(x[1])});
    case 'valuesBetween':return b.e.map(function(x){return fsBack(x[1])});
    case 'length':return b.e.length;case 'isEmpty':return !b.e.length;case 'isNotEmpty':return !!b.e.length;
    case 'toMap':{var mp={isMap:true,m:new Map()};b.e.forEach(function(x){mp.m.set(x[0],fsBack(x[1]))});return mp}
    case 'listenable':return{nat:'ValueNotifier',f:{value:v},src:'ValueListenable<Box>'};
    case 'watch':return{nat:'Stream',kind:'live',ms:0,get:function(){return v},src:'Stream<BoxEvent>'};
    case 'close':case 'compact':case 'flush':return null;
    case 'deleteFromDisk':delete DBP.hive[v.name];return ch(null);
    case 'toString':return v.src}
  throw new Error('membro Box.'+name)}
function hvStatic(name,args){var pos=args||[];
  switch(name){
    case 'initFlutter':case 'init':case 'registerAdapter':case 'close':return null;
    case 'openBox':case 'openLazyBox':return hvOpen(show(pos[0]));
    case 'box':case 'lazyBox':return hvOpen(show(pos[0]));
    case 'isBoxOpen':return !!DBP.hive[String(show(pos[0])).toLowerCase()];
    case 'boxExists':return !!DBP.hive[String(show(pos[0])).toLowerCase()];
    case 'deleteBoxFromDisk':delete DBP.hive[String(show(pos[0])).toLowerCase()];dirty=true;dbSave();return null;
    case 'deleteFromDisk':DBP.hive={};dirty=true;dbSave();return null}
  throw new Error('membro estático Hive.'+name)}
/* --- Supabase: banco Postgres de mentira (PostgREST) e auth --- */
var SB_PEND=[];
function sbErr(msg,code){var e=exc('PostgrestException(message: '+msg+', code: '+code+', details: null, hint: null)');e.val={nat:'PostgrestException',f:{message:msg,code:code,details:null,hint:null},src:'PostgrestException(message: '+msg+', code: '+code+')'};return e}
function sbAuthErr(msg,status,code){var e=exc('AuthException(message: '+msg+', statusCode: '+status+', code: '+code+')');e.val={nat:'AuthException',f:{message:msg,statusCode:String(status),code:code},src:'AuthException(message: '+msg+', statusCode: '+status+', code: '+code+')'};return e}
function sbTab(t){return DBP.sb.t[t]=DBP.sb.t[t]||[]}
function sbQ(t){return{nat:'SbQ',f:{},t:t,op:null,cols:'*',fl:[],ord:[],lim:null,off:0,one:0,ret:false,data:null,done:false,res:undefined,src:"Instance of 'PostgrestFilterBuilder'"}}
function sbMatch(r,f){var a=fsU(r[f.c]),b=f.v;
  switch(f.op){
    case 'eq':return JSON.stringify(a)===JSON.stringify(b);case 'neq':return JSON.stringify(a)!==JSON.stringify(b);
    case 'gt':return a!=null&&a>b;case 'gte':return a!=null&&a>=b;case 'lt':return a!=null&&a<b;case 'lte':return a!=null&&a<=b;
    case 'in':return (b||[]).some(function(x){return JSON.stringify(x)===JSON.stringify(a)});
    case 'is':return b===null?a==null:a===b;
    case 'like':case 'ilike':{if(typeof a!=='string')return false;var re=new RegExp('^'+String(b).replace(/[.*+?^${}()|[\]\\]/g,'\\$&').replace(/%/g,'.*').replace(/_/g,'.')+'$',f.op==='ilike'?'i':'');return re.test(a)}
    case 'contains':return Array.isArray(a)&&(b||[]).every(function(x){return a.some(function(y){return JSON.stringify(y)===JSON.stringify(x)})})}
  return true}
function sbRows(q){var rows=sbTab(q.t).filter(function(r){return q.fl.every(function(f){return sbMatch(r,f)})});return rows}
function sbOut(r,cols){var o={};if(!cols||cols.trim()==='*'||!cols.trim())o=JSON.parse(JSON.stringify(r));else cols.split(',').forEach(function(c){c=c.trim();var al=/^(\w+)\s*:\s*(\w+)$/.exec(c);if(al){o[al[1]]=r[al[2]]}else if(/^\w+$/.test(c))o[c]=r[c]});return fsBack(o)}
function sbFinish(q,rows){
  if(q.ord.length)rows=rows.slice().sort(function(x,y){for(var i=0;i<q.ord.length;i++){var o=q.ord[i],a=fsU(x[o.c]),b=fsU(y[o.c]);if(a==null&&b!=null)return o.asc?1:-1;if(b==null&&a!=null)return o.asc?-1:1;if(a<b)return o.asc?-1:1;if(a>b)return o.asc?1:-1}return 0});
  if(q.off)rows=rows.slice(q.off);if(q.lim!=null)rows=rows.slice(0,q.lim);
  var out=rows.map(function(r){return sbOut(r,q.cols)});
  if(q.one===1){if(out.length!==1)throw sbErr('JSON object requested, multiple (or no) rows returned','PGRST116');return out[0]}
  if(q.one===2){if(out.length>1)throw sbErr('JSON object requested, multiple (or no) rows returned','PGRST116');return out.length?out[0]:null}
  return out}
function sbNovo(t,m){var o=fsToPlainMap(m);if(o.id===undefined){var s=DBP.sb.seq[t]=(DBP.sb.seq[t]||0)+1;sbTab(t).forEach(function(r){if(typeof r.id==='number'&&r.id>=s)s=DBP.sb.seq[t]=r.id+1});o.id=s}
  if(o.created_at===undefined)o.created_at=new Date().toISOString();return o}
function sbExec(q){
  if(q.done)return q.res;q.done=true;var i=SB_PEND.indexOf(q);if(i>=0)SB_PEND.splice(i,1);var T=sbTab(q.t),res=null;
  if(q.op==='select'||q.op===null)res=sbFinish(q,sbRows(q));
  else if(q.op==='insert'||q.op==='upsert'){var lst=Array.isArray(q.data)?q.data:[q.data],ins=[],key=q.conf||'id';
    lst.forEach(function(m){var o=sbNovo(q.t,m);
      if(q.op==='upsert'){var j=T.findIndex(function(r){return JSON.stringify(r[key])===JSON.stringify(o[key])});if(j>=0){o=Object.assign({},T[j],fsToPlainMap(m));T[j]=o;ins.push(o);return}}
      else if(T.some(function(r){return JSON.stringify(r.id)===JSON.stringify(o.id)}))throw sbErr('duplicate key value violates unique constraint "'+q.t+'_pkey"','23505');
      T.push(o);ins.push(o)});
    res=q.ret?sbFinish(q,ins):null;dirty=true;dbSave()}
  else if(q.op==='update'){if(!q.fl.length)throw sbErr('UPDATE requires a WHERE clause','21000');var up=fsToPlainMap(q.data),hit=sbRows(q);hit.forEach(function(r){Object.assign(r,up)});res=q.ret?sbFinish(q,hit):null;dirty=true;dbSave()}
  else if(q.op==='delete'){if(!q.fl.length)throw sbErr('DELETE requires a WHERE clause','21000');var del=sbRows(q);DBP.sb.t[q.t]=T.filter(function(r){return del.indexOf(r)<0});res=q.ret?sbFinish(q,del):null;dirty=true;dbSave()}
  else if(q.op==='stream')res=sbFinish(q,sbRows(q));
  q.res=res;return res}
function sbVal(v){if(v&&v.nat==='SbQ'&&v.op!=='stream')return sbExec(v);return v}
function sbFlush(){var l=SB_PEND.splice(0);l.forEach(function(q){if(!q.done)sbExec(q)})}
function sbStream(q){return{nat:'Stream',kind:'live',ms:0,get:function(){var c=Object.assign({},q,{done:false,op:'stream'});return sbFinish(c,sbRows(c))},src:'Stream<List<Map<String, dynamic>>>'}}
function sbUser(email){var u=DBP.sb.users[email];if(!u)return null;var md={isMap:true,m:new Map()};Object.keys(u.meta||{}).forEach(function(k){md.m.set(k,fsBack(u.meta[k]))});
  return{nat:'SbUser',f:{id:u.id,email:email,userMetadata:md,createdAt:u.at,emailConfirmedAt:u.at,role:'authenticated'},src:"Instance of 'User'"}}
function sbSession(){var e=DBP.sb.cur;if(!e)return null;return{nat:'SbSession',f:{user:sbUser(e),accessToken:'token-simulado',tokenType:'bearer',expiresIn:3600},src:"Instance of 'Session'"}}
function sbResp(e){return{nat:'SbAuthResp',f:{user:sbUser(e),session:sbSession()},src:"Instance of 'AuthResponse'"}}
var SB_EVT={ev:'initialSession'};
function sbMember(v,name,a){
  if(v.nat==='HiveBox')return hvMember(v,name,a);
  a=a||[];var an=ARGN||[];ARGN=null;var pos=[],nm={};a.forEach(function(x,i){if(an[i])nm[an[i]]=x;else pos.push(x)});
  if(v.nat==='SbInst'){if(name==='client')return{nat:'SbClient',f:{},src:"Instance of 'SupabaseClient'"}}
  if(v.nat==='SbClient'){
    if(name==='from')return sbQ(show(pos[0]));
    if(name==='auth')return{nat:'SbAuth',f:{},src:"Instance of 'GoTrueClient'"};
    if(name==='rpc')throw sbErr('Funções RPC não são simuladas na Oficina','PGRST202');
    if(name==='removeAllChannels'||name==='dispose')return null}
  if(v.nat==='SbQ'){var q=v,pd=function(op,d){q.op=op;q.data=d;if(SB_PEND.indexOf(q)<0)SB_PEND.push(q);return q},fil=function(op,c,val){q.fl.push({op:op,c:String(show(c)),v:fsU(fsPlain(val))});return q};
    switch(name){
      case 'select':if(q.op===null||q.op==='select'){q.op='select';q.cols=pos.length?show(pos[0]):'*'}else{q.ret=true;q.cols=pos.length?show(pos[0]):'*'}return q;
      case 'insert':return pd('insert',pos[0]);
      case 'upsert':q.conf=nm.onConflict!=null?show(nm.onConflict):null;return pd('upsert',pos[0]);
      case 'update':return pd('update',pos[0]);
      case 'delete':return pd('delete',null);
      case 'eq':case 'neq':case 'gt':case 'gte':case 'lt':case 'lte':case 'like':case 'ilike':return fil(name,pos[0],pos[1]);
      case 'inFilter':case 'in_':return fil('in',pos[0],pos[1]);
      case 'isFilter':case 'is_':return fil('is',pos[0],pos[1]);
      case 'contains':return fil('contains',pos[0],pos[1]);
      case 'match':if(pos[0]&&pos[0].isMap)pos[0].m.forEach(function(x,k){fil('eq',k,x)});return q;
      case 'order':q.ord.push({c:show(pos[0]),asc:nm.ascending===true});return q;
      case 'limit':q.lim=nn(pos[0]);return q;
      case 'range':q.off=nn(pos[0]);q.lim=nn(pos[1])-nn(pos[0])+1;return q;
      case 'single':q.one=1;return q;
      case 'maybeSingle':q.one=2;return q;
      case 'stream':q.op='stream';return q;
      case 'count':return sbRows(q).length;
      case 'then':{var r0=sbExec(q);return pos[0]?callLam(pos[0],[r0]):r0}
      case 'listen':return member(sbStream(q),'listen',a);
      case 'asStream':return sbStream(q)}
    if(q.op==='stream')return member(sbStream(q),name,a);
    return member(sbExec(q),name,a)}
  if(v.nat==='SbAuth'){var U=DBP.sb.users,em=function(){return String(show(nm.email!==undefined?nm.email:pos[0])).trim()},pw=function(){return String(show(nm.password!==undefined?nm.password:pos[1]))};
    switch(name){
      case 'currentUser':return DBP.sb.cur?sbUser(DBP.sb.cur):null;
      case 'currentSession':return sbSession();
      case 'onAuthStateChange':return{nat:'Stream',kind:'live',ms:0,get:function(){return{nat:'SbAuthState',f:{event:'AuthChangeEvent.'+SB_EVT.ev,session:sbSession()},src:"Instance of 'AuthState'"}},src:'Stream<AuthState>'};
      case 'signUp':{var e1=em(),p1=pw();if(!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(e1))throw sbAuthErr('Unable to validate email address: invalid format',400,'email_address_invalid');
        if(p1.length<6)throw sbAuthErr('Password should be at least 6 characters.',422,'weak_password');if(U[e1])throw sbAuthErr('User already registered',422,'user_already_exists');
        var meta={};if(nm.data&&nm.data.isMap)meta=fsToPlainMap(nm.data);
        U[e1]={id:'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g,function(c){var r=Math.random()*16|0;return (c==='x'?r:(r&3|8)).toString(16)}),pass:p1,meta:meta,at:new Date().toISOString()};
        DBP.sb.cur=e1;SB_EVT.ev='signedIn';dirty=true;dbSave();return sbResp(e1)}
      case 'signInWithPassword':{var e2=em(),p2=pw();if(!U[e2]||U[e2].pass!==p2)throw sbAuthErr('Invalid login credentials',400,'invalid_credentials');DBP.sb.cur=e2;SB_EVT.ev='signedIn';dirty=true;dbSave();return sbResp(e2)}
      case 'signOut':DBP.sb.cur=null;SB_EVT.ev='signedOut';dirty=true;dbSave();return null;
      case 'updateUser':{var cu=DBP.sb.cur&&U[DBP.sb.cur];if(!cu)throw sbAuthErr('Auth session missing!',400,'session_not_found');var at=pos[0];if(at&&at.nat==='UserAttributes'){if(at.f.data&&at.f.data.isMap)Object.assign(cu.meta,fsToPlainMap(at.f.data));if(at.f.password)cu.pass=show(at.f.password)}dirty=true;dbSave();return{nat:'SbAuthResp',f:{user:sbUser(DBP.sb.cur)},src:"Instance of 'UserResponse'"}}
      case 'resetPasswordForEmail':return null}}
  if(SBNAT[v.nat]&&v.f&&v.f[name]!==undefined)return v.f[name];
  if(name==='toString')return v.src;
  throw new Error('membro '+(v.src||v.nat)+'.'+name)}
function sbStatic(name,args){if(name==='initialize'){SB_EVT.ev='initialSession';return{nat:'SbInst',f:{},src:"Instance of 'Supabase'"}}if(name==='instance')return{nat:'SbInst',f:{},src:"Instance of 'Supabase'"};throw new Error('membro estático Supabase.'+name)}
"""


def patch(src):
    # Google Fonts: qualquer família, carregada do Google Fonts na hora
    src = sub1(src, "/* ===== Oficina 2: sensores de movimento", GLOBAL + "/* ===== Oficina 2: sensores de movimento", 'gf global')
    src = sub1(src, "function gfFamily(n){var G={pressStart2p:'Press Start 2P',silkscreen:'Silkscreen',vt323:'VT323',bungee:'Bungee'};return G[n]||n.replace(/([a-z])([A-Z0-9])/g,'$1 $2').replace(/^./,function(c){return c.toUpperCase()})}",
        "function gfFamily(n){return window.OF_GF?window.OF_GF(n):n}", 'gfFamily')
    src = sub1(src, "raw=\"TextStyle(fontFamily: '\"+(GFN[gfm[1]]||gfm[1])+\"'\"",
        "raw=\"TextStyle(fontFamily: '\"+(gfm[1]==='getFont'?(function(){var gq=/^\\s*['\"]([^'\"]+)['\"]\\s*,?\\s*/.exec(gin);if(gq){gin=gin.slice(gq[0].length);gts=/^textStyle:\\s*(?:const\\s+)?TextStyle\\(([\\s\\S]*)\\)\\s*,?\\s*$/.exec(gin.trim());window.OF_GF_CARREGA&&OF_GF_CARREGA(gq[1]);return gq[1]}return 'Roboto'})():(window.OF_GF?OF_GF(gfm[1]):(GFN[gfm[1]]||gfm[1])))+\"'\"", 'gf textstyle')
    # fontFamily: 'Lobster' explícito também tenta carregar
    # Hive e Supabase
    src = sub1(src, "function natCtor(name,args){\n", ENGINE + "function natCtor(name,args){\n  if(name==='UserAttributes'){var ua={};args.forEach(function(x){if(x.name)ua[x.name]=x.val});return{nat:'UserAttributes',f:ua,src:'UserAttributes()'}}\n", 'sb engine')
    src = sub1(src, "  if(v.nat==='Prefs')return prefsMember(v,name,args);\n",
        "  if(v.nat==='Prefs')return prefsMember(v,name,args);\n  if(SBNAT[v.nat])return sbMember(v,name,args);\n", 'sb member')
    src = sub1(src, "    if(c==='SharedPreferences'){if(name==='getInstance')",
        "    if(c==='Hive')return hvStatic(name,args);\n    if(c==='Supabase')return sbStatic(name,args);\n    if(c==='AuthChangeEvent')return 'AuthChangeEvent.'+name;\n"
        "    if(c==='SharedPreferences'){if(name==='getInstance')", 'sb static')
    src = sub1(src, "(val.nat&&(FBNAT[val.nat]||val.nat==='SqlDb'||val.nat==='Prefs'))", "(val.nat&&(FBNAT[val.nat]||SBNAT[val.nat]||val.nat==='SqlDb'||val.nat==='Prefs'))", 'sb capture')
    # await: espera de verdade o construtor de consultas do Supabase
    src = sub1(src, "  if(p.isId('await')&&p.pk(1)&&!(p.pk(1).k==='p'&&/^[=;,)]$/.test(p.pk(1).v))){p.i++;return pUn(p)}",
        "  if(p.isId('await')&&p.pk(1)&&!(p.pk(1).k==='p'&&/^[=;,)]$/.test(p.pk(1).v))){p.i++;return{t:'aw',a:pUn(p)}}", 'await node')
    src = sub1(src, "    case 'is':{var iv2=ev(a.a,env),r2=isType(iv2,a.ty);return a.neg?!r2:r2}",
        "    case 'is':{var iv2=ev(a.a,env),r2=isType(iv2,a.ty);return a.neg?!r2:r2}\n    case 'aw':return sbVal(ev(a.a,env));", 'await ev')
    src = sub1(src, "    if(k.v==='await'){p.i++;simple(p,env,run);return}", "    if(k.v==='await'){p.i++;simple(p,env,run);if(run)sbFlush();return}", 'await stmt flush')
    src = sub1(src, "    else err='handler';\n  }catch(e){err=e.message;isExc=!!e.dartExc}", "    else err='handler';\n    sbFlush();\n  }catch(e){SB_PEND.length=0;err=e.message;isExc=!!e.dartExc}", 'run flush')
    # FutureBuilder e StreamBuilder com Supabase e Hive
    src = sub1(src, "        if(ex2&&/Firebase|\\.collection\\(|\\.doc\\(/.test(ex2)){ms=600;data=ev(pTern(new Ps(ex2.trim())),env);if(data===undefined)data=null}",
        "        if(ex2&&/Firebase|\\.collection\\(|\\.doc\\(|\\.from\\(|Supabase|Hive|\\.box\\(/.test(ex2)){ms=600;data=sbVal(ev(pTern(new Ps(ex2.trim())),env));if(data===undefined)data=null}", 'fut sb')
    src = sub1(src, "        data=ev(pTern(new Ps(rc.call)),env);if(data===undefined)data=null}",
        "        data=sbVal(ev(pTern(new Ps(rc.call)),env));if(data===undefined)data=null;if(!ms&&/supabase|Supabase|\\.from\\(/.test(body))ms=600}", 'fut sb call')
    src = sub1(src, "  if(!sv||sv.nat!=='Stream'&&sv.nat!=='StreamController')throw new Error('este tipo de Stream",
        "  if(sv&&sv.nat==='SbQ')sv=sbStream(sv);\n  if(!sv||sv.nat!=='Stream'&&sv.nat!=='StreamController')throw new Error('este tipo de Stream", 'stream sb')
    # NestedScrollView: o cabeçalho recolhe primeiro e só depois a lista de dentro rola
    src = sub1(src, "single('body','#single','body: adicione um widget');var nbd=d.lastChild;if(nbd&&nbd.classList)nbd.classList.add('nsb');",
        "single('body','#single','body: adicione um widget');var nbd=d.lastChild;if(nbd&&nbd.classList)nbd.classList.add('nsb');R_opts.post.push(function(){if(window.OF_NSV)OF_NSV(d)});", 'nsv post')
    src = sub1(src, "    if(vlp.names[1])vbody=bindVar(vbody,vlp.names[1],vlv);",
        "    if(vlv&&typeof vlv==='object'&&!isD(vlv)&&!isRaw(vlv)){var vcv=ST.capVals=ST.capVals||{},vid=null;Object.keys(vcv).forEach(function(q){if(vcv[q]===vlv)vid=q});if(!vid){vid='__cv'+(++CAPN);vcv[vid]=vlv}vlv={raw:vid}}\n"
        "    if(vlp.names[1])vbody=bindVar(vbody,vlp.names[1],vlv);", 'vlb objeto')
    src = sub1(src, '    if(ff)css+=\'font-family:\'+(/mono|courier|consolas/i.test(ff)?"\'JetBrains Mono\',ui-monospace,monospace":/serif/i.test(ff)&&!/sans/i.test(ff)||/georgia|times/i.test(ff)?\'Georgia,serif\':/cursive|pacifico|lobster|dancing/i.test(ff)?"\'Brush Script MT\',cursive":"\'"+ff.replace(/\'/g,\'\')+"\',Roboto,system-ui,sans-serif")+\';\'}', '    if(ff){var ffq="\'"+ff.replace(/\'/g,\'\')+"\',";if(window.OF_GF_CARREGA&&!/^(monospace|serif|sans-serif|cursive|courier|consolas|georgia|times|arial|helvetica|system-ui|roboto)/i.test(ff))OF_GF_CARREGA(ff.replace(/\'/g,\'\'));css+=\'font-family:\'+(/mono|courier|consolas/i.test(ff)?ffq+"\'JetBrains Mono\',ui-monospace,monospace":/serif/i.test(ff)&&!/sans/i.test(ff)||/georgia|times/i.test(ff)?ffq+\'Georgia,serif\':/cursive|pacifico|lobster|dancing|caveat|script/i.test(ff)?ffq+"\'Brush Script MT\',cursive":ffq+"Roboto,system-ui,sans-serif")+\';\'}}', 'fontfamily css')
    # cascata com caminho: def..target.setFrom(p) e obj..a.b = 1
    src = sub1(src, "p.i++;var cargs=null,cset=null;if(p.is('(')){p.i++;cargs=pArgs(p)}else if(p.is('=')){",
        "p.i++;var cargs=null,cset=null,segs=[];while(true){if(p.is('.')&&p.pk(1)&&p.pk(1).k==='id'){segs.push({name:cn,args:null});cn=p.pk(1).v;p.i+=2;continue}if(p.is('(')){p.i++;var aa0=pArgs(p);if(p.is('.')&&p.pk(1)&&p.pk(1).k==='id'){segs.push({name:cn,args:aa0});cn=p.pk(1).v;p.i+=2;continue}cargs=aa0}break}if(cargs){}else if(p.is('=')){", 'casc path parse')
    src = sub1(src, "cops.push({name:cn,args:cargs,set:cset})", "cops.push({name:cn,args:cargs,set:cset,segs:segs.length?segs:null})", 'casc path push')
    src = sub1(src, "case 'casc':{var co=ev(a.o,env);a.ops.forEach(function(op){",
        "case 'casc':{var co=ev(a.o,env);a.ops.forEach(function(op){var co0=co;try{if(op.segs)op.segs.forEach(function(s){co=member(co,s.name,s.args?s.args.map(function(x){return ev(x.ast,env)}):null)});", 'casc path ev')
    src = sub1(src, "member(co,op.name,cargs)}});return co}", "member(co,op.name,cargs)}}finally{co=co0}});return co}", 'casc path end')
    # tickers mantidos no hot reload deixam de ser "velhos" (os erros deles voltam a aparecer)
    src = sub1(src, "  if(!fresh)keepG.forEach(function(v){if(ST.anims.indexOf(v)<0)ST.anims.push(v)});", "  if(!fresh)keepG.forEach(function(v){v.velho=false;if(ST.anims.indexOf(v)<0)ST.anims.push(v)});", 'keep not old')
    # várias variáveis locais numa declaração: final dx = 1, dy = 2;  int a, b;
    src = sub1(src, "  if(t[i]&&t[i].k==='id'&&t[i+1]&&t[i+1].k==='p'&&(t[i+1].v==='='||t[i+1].v===';')){\n    if(!had)return false;j=i}",
        "  if(t[i]&&t[i].k==='id'&&t[i+1]&&t[i+1].k==='p'&&(t[i+1].v==='='||t[i+1].v===';'||(had&&t[i+1].v===','))){\n    if(!had)return false;j=i}", 'multi local had')
    src = sub1(src, "    if(!(t[j]&&t[j].k==='id'&&t[j+1]&&t[j+1].k==='p'&&(t[j+1].v==='='||t[j+1].v===';')))return false}",
        "    if(!(t[j]&&t[j].k==='id'&&t[j+1]&&t[j+1].k==='p'&&(t[j+1].v==='='||t[j+1].v===';'||t[j+1].v===',')))return false}", 'multi local typed')
    src = sub1(src, "env.locals[name]=tn?coerce(tn,iv):iv}}else if(run)env.locals[name]=null;\n  return true}",
        "env.locals[name]=tn?coerce(tn,iv):iv}}else if(run)env.locals[name]=null;\n"
        "  while(p.is(',')&&p.pk(1)&&p.pk(1).k==='id'&&p.pk(2)&&p.pk(2).k==='p'&&/^[=,;]$/.test(p.pk(2).v)){p.i++;var n2=p.pk().v;p.i++;if(p.eat('=')){var ie2=pTern(p);if(run){var iv2=ev(ie2,env);env.locals[n2]=tn?coerce(tn,iv2):iv2}}else if(run)env.locals[n2]=null}\n"
        "  return true}", 'multi local more')
    # static const dentro do State (ou do widget) usado sem o nome da classe
    src = sub1(src, "  ST.exts=info.exts||[];ST.routes=info.routes||[];",
        "  ST.stStatics={};(info.states||[]).forEach(function(sx){var ss=sx.ci&&sx.ci.statics||{};Object.keys(ss).forEach(function(k){ss[k].done=false;ST.stStatics[k]=ss[k]})});Object.keys(info.classes||{}).forEach(function(cn){var c=info.classes[cn];if(c.kind!=='data'&&c.ci&&c.ci.statics)Object.keys(c.ci.statics).forEach(function(k){if(!ST.stStatics[k]){c.ci.statics[k].done=false;ST.stStatics[k]=c.ci.statics[k]}})});\n"
        "  ST.exts=info.exts||[];ST.routes=info.routes||[];", 'state statics load')
    src = sub1(src, "  if(n==='context')return{nat:'#ctx',f:{},src:'context'};", "  if(ST.stStatics&&hasOwn(ST.stStatics,n))return staticGet(ST.stStatics[n]);\n  if(n==='context')return{nat:'#ctx',f:{},src:'context'};", 'state statics lookup')
    assert src.count("(FirebaseAuth|FirebaseFirestore)")==3
    src = src.replace("(FirebaseAuth|FirebaseFirestore)", "(FirebaseAuth|FirebaseFirestore|Supabase)")
    return src


CSS = r"""<style>
.screen .nd.nsv.nsr>.nsb{overflow:hidden;display:flex;flex-direction:column;min-height:0}
.screen .nd.nsv.nsr>.nsb.list,.screen .nd.nsv.nsr>.nsb.csv{overflow-y:auto;flex:none;max-height:none}
.screen .nd.nsv.nsr>.nsb .nd.list,.screen .nd.nsv.nsr>.nsb .nd.csv{overflow-y:auto;flex:1 1 0;min-height:0;height:auto;max-height:none}
</style>
<script>
/* ===== Oficina 2: NestedScrollView em duas etapas ===== */
window.OF_NSV=function(d){if(!d.isConnected)return;d.classList.add('nsr');var b=d.querySelector(':scope>.nsb');if(!b)return;
  var fix=0;Array.prototype.forEach.call(d.children,function(c){if(c===b)return;var cs=getComputedStyle(c);if(cs.position==='sticky'){var t=parseFloat(cs.top)||0;fix=Math.max(fix,t+c.offsetHeight)}});
  b.style.flex='none';b.style.minHeight='0';b.style.height=Math.max(80,d.clientHeight-fix)+'px';
  if(d._nsv)return;d._nsv=1;
  function inner(t){var e=t;while(e&&e!==d){if(e!==b&&e.scrollHeight>e.clientHeight+1){var oy=getComputedStyle(e).overflowY;if(oy==='auto'||oy==='scroll')return e}if(e===b){if(b.scrollHeight>b.clientHeight+1&&/auto|scroll/.test(getComputedStyle(b).overflowY))return b;break}e=e.parentElement}
    var l=b.querySelector('.nd.list,.nd.csv');return l&&l.scrollHeight>l.clientHeight+1?l:null}
  function mover(dy,t){var i=inner(t),mx=d.scrollHeight-d.clientHeight;
    if(dy>0){var tome=Math.min(dy,Math.max(0,mx-d.scrollTop));d.scrollTop+=tome;if(i&&dy-tome>0)i.scrollTop+=dy-tome;return true}
    if(i&&i.scrollTop>0){var r=Math.min(-dy,i.scrollTop);i.scrollTop-=r;if(-dy-r>0)d.scrollTop+=dy+r;return true}
    d.scrollTop+=dy;return true}
  d.addEventListener('wheel',function(e){if(!b.contains(e.target)&&!d.contains(e.target))return;var k=e.deltaMode===1?16:e.deltaMode===2?d.clientHeight:1;if(mover(e.deltaY*k,e.target))e.preventDefault()},{passive:false});
  var ty=null;d.addEventListener('touchstart',function(e){ty=e.touches[0].clientY},{passive:true});
  d.addEventListener('touchmove',function(e){if(ty==null)return;var y=e.touches[0].clientY,dy=ty-y;ty=y;if(mover(dy,e.target))e.preventDefault()},{passive:false});
  d.addEventListener('touchend',function(){ty=null},{passive:true})};
</script>
"""


LIM = [
 ("e fonte, incluindo GoogleFonts.pressStart2p, silkscreen, vt323 e bungee. tp.width",
  "e fonte: GoogleFonts.pressStart2p, silkscreen, vt323 e bungee já vêm prontas, e qualquer outra GoogleFonts.xxx (ou GoogleFonts.getFont) é baixada do Google Fonts na hora, se houver internet. tp.width"),
 ("e ContactCallbacks (beginContact e endContact). Não tem juntas (joints) nem raycast.'",
  "e ContactCallbacks (beginContact e endContact). Juntas: RevoluteJoint (com motor e limites), WeldJoint, DistanceJoint, RopeJoint, PrismaticJoint e MouseJoint (arrastar um corpo com o dedo), criadas com world.createJoint. world.raycast com RayCastCallback devolve o ponto, a normal e a fração.',\n"
  " 'Sensores: sensors_plus com accelerometerEventStream, userAccelerometerEventStream, gyroscopeEventStream e magnetometerEventStream (listen ou StreamBuilder). No celular os valores vêm do aparelho; no computador, o painel de inclinação que aparece no canto faz o papel do celular.',\n"
  " 'Desenho avançado: gradientes no Paint (ui.Gradient.linear, radial e sweep, ou LinearGradient, RadialGradient e SweepGradient com createShader), MaskFilter.blur, BlendMode, canvas.drawShadow e ParagraphBuilder com drawParagraph.'"),
 ("Mapas isométricos, camadas de imagem e blocos animados não são desenhados.'",
  "Também desenha mapas isométricos (iso.tmx), camadas de imagem e blocos animados (a água e as tochas de arena.tmx).'"),
 (" 'Registros com campos nomeados, como (a: 1, b: 2) e r.a. Registros posicionais, como (1, \"a\"), funcionam.',\n", ""),
 ("'Pacotes: só os simulados no botão 📡 Sensores (GPS, bateria, rede, câmera, http). Sensores em tempo real, som, microfone, biometria, lanterna e QR só funcionam no celular.'",
  "'Pacotes: além dos simulados no botão 📡 Sensores (GPS, bateria, rede, câmera, http), funcionam sensors_plus, audioplayers, hive, supabase_flutter e google_fonts. Microfone, biometria, lanterna e QR só funcionam no celular.'"),
 ("switch como expressão, records,", "switch como expressão, records (posicionais e com campos nomeados, como (a: 1, b: 2), r.a e var (:a, :b) = r), build com =>,"),
 (" MediaQuery.of(context).size devolve 360 x 640. Arrasto (onPanUpdate) ainda não existe.'", " MediaQuery.of(context).size devolve 360 x 640.'"),
 ("Não existem: shaders, gradientes no Paint, MaskFilter (desfoque), drawImage, drawParagraph, drawShadow e BlendMode. Cada desenho",
  "Também funcionam drawImage, drawImageRect, gradientes no shader, MaskFilter.blur, BlendMode, drawShadow e drawParagraph; não existem drawVertices, drawAtlas e FragmentShader. Cada desenho"),
 ("'NestedScrollView: o cabeçalho e o corpo rolam juntos; não há a regra de que a rolagem interna só começa depois do cabeçalho recolher. SliverAppBar encolhe por recorte (não refaz o layout) e floating e snap não têm efeito.'",
  "'NestedScrollView: como no Flutter, o cabeçalho recolhe primeiro e só depois a lista de dentro rola (com a roda do mouse ou o dedo); ao voltar, a lista sobe até o topo antes de o cabeçalho reabrir. SliverAppBar encolhe por recorte (não refaz o layout), floating e snap não têm efeito e innerBoxIsScrolled é sempre false.'"),
 ("'PaginatedDataTable: lê rowCount e getRow do seu DataTableSource e pagina com as setas. Não há ordenação (sortColumnIndex), seleção de linhas nem escolha de availableRowsPerPage.'",
  "'PaginatedDataTable: lê rowCount e getRow do seu DataTableSource, pagina com as setas, ordena pelo cabeçalho (sortColumnIndex, sortAscending e onSort da DataColumn), mostra as caixas de seleção (DataRow.selected e onSelectChanged, e onSelectAll) e deixa escolher entre availableRowsPerPage (onRowsPerPageChanged).'"),
 ("'Draggable, LongPressDraggable e DragTarget funcionam com o mouse ou o dedo, mas a cópia que acompanha o ponteiro é um clone do widget, o offset em DragTargetDetails é Offset(0, 0) e onMove não é chamado.'",
  "'Draggable, LongPressDraggable e DragTarget funcionam com o mouse ou o dedo, com onDragUpdate, onMove e o offset certo em DragTargetDetails e DraggableDetails. A cópia que acompanha o ponteiro é um clone do widget.'"),
 ("e Firebase (cloud_firestore e firebase_auth) são simulados no navegador.", "Hive, Supabase e Firebase (cloud_firestore e firebase_auth) são simulados no navegador."),
 ("↺ Reiniciar apaga o banco, os documentos e as contas.'",
  "↺ Reiniciar apaga o banco, os documentos, as caixas do Hive e as contas.',\n"
  " 'Hive simulado: Hive.initFlutter, openBox e box, put, get (com defaultValue), add, addAll, putAll, delete, deleteAt, getAt, putAt, clear, keys, values, length, containsKey, toMap e listenable (com ValueListenableBuilder). Não há adapters (TypeAdapter) nem caixas criptografadas: objetos de classes suas são guardados como Map.',\n"
  " 'Supabase simulado: Supabase.initialize, Supabase.instance.client e a tabela com from(...).select, insert, update, upsert e delete, filtros eq, neq, gt, gte, lt, lte, like, ilike, inFilter e match, order (ascending é false por padrão, como no pacote), limit, range, single e maybeSingle; cada linha nova ganha id e created_at. stream(primaryKey: ...) funciona no StreamBuilder. Auth: signUp, signInWithPassword, signOut, currentUser, currentSession e onAuthStateChange, com AuthException e PostgrestException. Não há rpc, storage, tabelas ligadas no select nem regras RLS.'"),
 ("Hive, Isar e Supabase não existem.'", "Isar não existe.'"),
 ("Widgets que não existem no simulador: Overlay e OverlayEntry (use showDialog ou SnackBar), PositionedTransition,", "Overlay.of(context).insert com OverlayEntry funciona (entry.remove() tira da tela). Widgets que não existem no simulador: PositionedTransition,"),
 ("'Listener e MouseRegion: os eventos chegam sem o objeto do evento (posição, botão), então não dá para ler e.position.",
  "'Listener e MouseRegion: os eventos trazem localPosition, position, delta e buttons (onPointerDown, onPointerMove, onPointerUp, onPointerHover, onPointerSignal, onEnter, onExit e onHover), e MouseRegion aceita cursor."),
 ("Não existem CupertinoTimerPicker, CupertinoListSection e CupertinoSliverNavigationBar.'", "Também existem CupertinoTimerPicker, CupertinoListSection e CupertinoSliverNavigationBar (o título grande encolhe ao rolar).'"),
 ("Consumer3, ProxyProvider, ChangeNotifierProvider.value e providers criados dentro de uma função não existem.'",
  "Consumer3, ProxyProvider, ChangeNotifierProxyProvider, Provider.value e ChangeNotifierProvider.value também funcionam; providers criados dentro de uma função não existem.'"),
 ("Não existem refreshListenable, errorBuilder, context.canPop, navigatorContainerBuilder e StatefulShellRoute sem indexedStack.'",
  "refreshListenable (o redirect roda de novo a cada notifyListeners), errorBuilder e context.canPop também funcionam; navigatorContainerBuilder e StatefulShellRoute sem indexedStack não existem.'"),
 ("fontFamily usa só uma fonte parecida (monoespaçada, com serifa ou padrão), sem baixar a fonte.'",
  "fontFamily e GoogleFonts baixam a fonte do Google Fonts quando há internet; sem rede, aparece uma fonte parecida.'"),
 ("um TextInputFormatter escrito por você (classe própria) não roda, e autofillHints e maxLengthEnforcement não valem.'",
  "um TextInputFormatter escrito por você (classe com formatEditUpdate) também roda; autofillHints e maxLengthEnforcement não valem.'"),
 ("'As curvas (Curves.*) das animações implícitas são aproximadas por CSS;", "'As curvas (Curves.*) das animações implícitas seguem a fórmula do Flutter (amostrada em CSS linear());"),
 ("'AnimatedList e Hero: não mostram a animação de entrada, saída ou voo.'",
  "'AnimatedList anima a entrada e a saída (insertItem e removeItem) e Hero voa entre as telas, interpolando posição e tamanho; flightShuttleBuilder e placeholderBuilder não valem.'"),
]


def patch_limits(src):
    for a, b in LIM:
        src = sub1(src, a, b, 'lim ' + a[:30])
    return src
