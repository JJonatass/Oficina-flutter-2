# Oficina Flutter 2, frente 7e: widgets e pacotes que faltavam.
from patch_engine import sub1


def patch(src):
    # ---- Overlay e OverlayEntry
    src = sub1(src, "var FXSTART={showDatePicker:1,", "var FXSTART={Overlay:1,showDatePicker:1,", 'fxstart overlay')
    src = sub1(src, "  if(/^Navigator\\b/.test(txt)){\n    if(/\\.pop\\s*\\(/.test(txt)||/\\.maybePop\\s*\\(/.test(txt)){",
        "  if(/^Overlay\\b/.test(txt)){var om=/\\.(insert|insertAll)\\s*\\(/.exec(txt);if(!om)return false;var oa=grabArg(txt,om.index+om[0].length),ov=ev(pTern(new Ps(oa)),env);\n"
        "    (Array.isArray(ov)?ov:[ov]).forEach(function(e){if(e&&e.nat==='OvEntry'){e.on=true;ST.fx.push({k:'entry',src:e.src,id:e.id})}});return true}\n"
        "  if(/^Navigator\\b/.test(txt)){\n    if(/\\.pop\\s*\\(/.test(txt)||/\\.maybePop\\s*\\(/.test(txt)){", 'fx overlay')
    src = sub1(src, "      if(a.args&&NATCTOR[a.name])return natCtor(a.name,evalArgs(a,env));",
        "      if(a.args&&a.name==='OverlayEntry'){var oea=evalArgs(a,env),otx='OverlayEntry('+oea.map(function(x){return (x.name?x.name+': ':'')+(x.src||'')}).join(', ')+')';"
        "return{nat:'OvEntry',f:{},id:++OVID,on:false,src:bindEnv(builderBody(otx),env),src0:'OverlayEntry'}}\n"
        "      if(a.args&&NATCTOR[a.name])return natCtor(a.name,evalArgs(a,env));", 'overlayentry ctor')
    src = sub1(src, "  if(v&&v.nat==='BodyTypeNS')return name;\n",
        "  if(v&&v.nat==='BodyTypeNS')return name;\n"
        "  if(v&&v.nat==='OvEntry'){if(name==='remove'){if(v.on){v.on=false;ST.fx.push({k:'entryRem',id:v.id});dirty=true}return null}if(name==='mounted')return !!v.on;if(name==='markNeedsBuild'){dirty=true;return null}return null}\n",
        'overlayentry member')
    src = sub1(src, "function builderBody(txt){", "var OVID=0;\nfunction builderBody(txt){", 'ovid')
    src = sub1(src, "    if(f.k==='dialog'||f.k==='sheet')R.opts.over.push({k:f.k,src:f.src,sc:sc,res:res,pop:!!f.pop});",
        "    if(f.k==='dialog'||f.k==='sheet')R.opts.over.push({k:f.k,src:f.src,sc:sc,res:res,pop:!!f.pop});\n"
        "    else if(f.k==='entry'){R.opts.over.push({k:'entry',src:f.src,sc:sc,id:f.id})}\n"
        "    else if(f.k==='entryRem'){R.opts.over=R.opts.over.filter(function(o){return !(o.k==='entry'&&o.id===f.id)})}", 'applyfx overlay')
    src = sub1(src,
        "    var nd=OF.parseWidgetText(o.src);if(!nd)return;\n"
        "    if(o.k!=='snack'&&o.k!=='banner'){var sc=document.createElement('div');sc.className='ovs';screen.appendChild(sc)}\n"
        "    var w=document.createElement('div');w.className=o.k==='dialog'?'ovl dlg':",
        "    var nd=OF.parseWidgetText(o.k==='entry'?'Stack(children: ['+o.src+'])':o.src);if(!nd)return;\n"
        "    if(o.k!=='snack'&&o.k!=='banner'&&o.k!=='entry'){var sc=document.createElement('div');sc.className='ovs';screen.appendChild(sc)}\n"
        "    var w=document.createElement('div');w.className=o.k==='entry'?'ovl ent':o.k==='dialog'?'ovl dlg':",
        'render overlay entry')
    # ---- Cupertino: CupertinoTimerPicker, CupertinoListSection, CupertinoListTile e CupertinoSliverNavigationBar
    src = sub1(src, " CupertinoDatePicker:{cat:'content',slots:{},desc:",
        " CupertinoTimerPicker:{cat:'content',slots:{},desc:'Rodas de horas, minutos e segundos do iOS para escolher uma duração. mode escolhe CupertinoTimerPickerMode.hms, hm ou ms; initialTimerDuration é o valor inicial e onTimerDurationChanged recebe a Duration escolhida.'},\n"
        " CupertinoListSection:{cat:'layout',slots:{header:'one',footer:'one',children:'many'},desc:'Grupo de linhas no estilo dos Ajustes do iOS: header em cima, as linhas separadas por divisórias e footer embaixo.'},\n"
        " 'CupertinoListSection.insetGrouped':{cat:'layout',slots:{header:'one',footer:'one',children:'many'},desc:'Grupo de linhas do iOS com margem e cantos arredondados, como nos Ajustes.'},\n"
        " CupertinoListTile:{cat:'content',slots:{leading:'one',title:'one',subtitle:'one',additionalInfo:'one',trailing:'one'},desc:'Linha de lista do iOS: leading, title, subtitle, additionalInfo (texto cinza à direita) e trailing. Com onTap, mostre CupertinoListTileChevron() no trailing.'},\n"
        " CupertinoListTileChevron:{cat:'content',slots:{},desc:'A setinha › que indica que a linha abre outra tela.'},\n"
        " CupertinoSliverNavigationBar:{cat:'struct',slots:{leading:'one',middle:'one',trailing:'one',largeTitle:'one'},desc:'Barra do iOS com título grande, para usar nos slivers de um CustomScrollView. O título grande encolhe ao rolar.'},\n"
        " CupertinoDatePicker:{cat:'content',slots:{},desc:", 'cupertino schema')
    src = sub1(src, "    case 'CupertinoActionSheetAction':{", CUP_CASES + "    case 'CupertinoActionSheetAction':{", 'cupertino cases')
    src = sub1(src, "  var box=w.closest('.cdp');if(!box)return;",
        "  var box=w.closest('.cdp');if(!box)return;\n"
        "  if(box.dataset.timer){var tst={th:0,tm:0,ts:0};[].forEach.call(box.querySelectorAll('.cpkw'),function(x){tst[x.dataset.col]=wheelIdx(x)*(+x.dataset.step||1)});var tok=R.opts.dps[box.dataset.key]||{};tst.src=tok.src;R.opts.dps[box.dataset.key]=tst;\n"
        "    var traw=M.rawProp(w._pn,'onTimerDurationChanged');if(traw&&traw.trim()!=='null')afterRun(runAt(w,traw,[{raw:'Duration(hours: '+tst.th+', minutes: '+tst.tm+', seconds: '+tst.ts+')'}]));renderCanvas();return}",
        'timer settle')
    # ---- PaginatedDataTable: ordenação (sortColumnIndex, sortAscending, onSort), seleção de linhas e linhas por página
    src = sub1(src,
        "      pcols.forEach(function(c,i){var ce=child(c,'columns:'+i,'#none');ce.classList.add('pdtc');ptb.appendChild(ce)});",
        "      var psci=numVal(M.getProp(n,'sortColumnIndex')),psasc=!/false/.test(M.getProp(n,'sortAscending')||'true'),pchk=!/false/.test(M.getProp(n,'showCheckboxColumn')||'true'),psel=null;\n"
        "      try{var pprobe=OF.ST.tableRows(n,0,1);if(pprobe&&pprobe.rows[0]&&/onSelectChanged\\s*:/.test(pprobe.rows[0]))psel=true}catch(e){}\n"
        "      if(psel&&pchk){ptb.style.gridTemplateColumns='40px repeat('+Math.max(1,pcols.length)+',minmax(0,1fr))';var phc=document.createElement('div');phc.className='pdtc pdtck';"
        "var psa=M.rawProp(n,'onSelectAll');if(psa&&psa.trim()!=='null'){var pcb=document.createElement('span');pcb.className='pdtbox hh';pcb.dataset.h='pdtall';pcb._n=n;pcb.textContent='☐';phc.appendChild(pcb)}ptb.appendChild(phc)}\n"
        "      pcols.forEach(function(c,i){var ce=child(c,'columns:'+i,'#none');ce.classList.add('pdtc');var pos0=c&&M.rawProp(c,'onSort');"
        "if(pos0&&pos0.trim()!=='null'&&R_opts.run){ce.classList.add('hh');ce.dataset.h='pdtsort';ce.dataset.i=i;ce.dataset.a=(psci===i?!psasc:true)?'1':'';ce._n=c}"
        "if(psci===i){var par=document.createElement('span');par.className='pdtarr';par.textContent=psasc?' ↑':' ↓';ce.appendChild(par)}ptb.appendChild(ce)});",
        'pdt header')
    src = sub1(src,
        "      if(ptr){ptr.rows.forEach(function(tx,ri){var rn=OF.parseWidgetText(tx);if(rn){var re=build(rn,path.concat('@'+ri),'#none',null,sel);",
        "      if(ptr){ptr.rows.forEach(function(tx,ri){var rn=OF.parseWidgetText(tx);if(rn){var re=build(rn,path.concat('@'+ri),'#none',null,sel);"
        "if(psel&&pchk){var rsel=/true/.test(M.getProp(rn,'selected')||''),rck=document.createElement('div');rck.className='pdtx pdtr pdtck';var rbx=document.createElement('span');rbx.className='pdtbox'+(R_opts.run?' hh':'');rbx.dataset.h='pdtsel';rbx.dataset.v=rsel?'':'1';rbx._n=rn;rbx.textContent=rsel?'☑':'☐';rck.appendChild(rbx);ptb.appendChild(rck);if(rsel)re.dataset.sel='1'}",
        'pdt rows sel')
    src = sub1(src,
        "      if(ptr){var pen=Math.min(ptr.total,pst+prpn);pft.innerHTML='Linhas por página: '+prpn+' &nbsp; '",
        "      if(ptr){var pen=Math.min(ptr.total,pst+prpn),parp=M.rawProp(n,'onRowsPerPageChanged'),pav=String(M.getProp(n,'availableRowsPerPage')||'[10, 20, 50]').match(/\\d+/g)||['10'];"
        "pft.innerHTML='Linhas por página: '+(parp&&parp.trim()!=='null'&&R_opts.run?'<select class=pdtrpp>'+pav.map(function(x){return '<option'+(+x===prpn?' selected':'')+'>'+x+'</option>'}).join('')+'</select>':prpn)+' &nbsp; '",
        'pdt rpp')
    src = sub1(src, "  if(t.dataset.h==='pdtnav'){R.opts.pdt[t.dataset.k]=+t.dataset.v;renderCanvas();return}",
        "  if(t.dataset.h==='pdtnav'){R.opts.pdt[t.dataset.k]=+t.dataset.v;renderCanvas();return}\n"
        "  if(t.dataset.h==='pdtsort'){var sr0=t._n&&M.rawProp(t._n,'onSort');if(sr0&&sr0.trim()!=='null')afterRun(runAt(t,sr0,[+t.dataset.i,!!t.dataset.a]));return}\n"
        "  if(t.dataset.h==='pdtsel'){var sr1=t._n&&M.rawProp(t._n,'onSelectChanged'),ptab=t.closest('.pdt'),psrc=ptab&&ptab._n&&M.rawProp(ptab._n,'source');if(sr1&&sr1.trim()!=='null'){var inst=scopeOfEl(t),rr=runIn(inst,function(){return psrc?OF.ST.runSelf(psrc,sr1,[!!t.dataset.v]):OF.ST.run(sr1,[!!t.dataset.v])});rr.sc=inst;afterRun(rr)}return}\n"
        "  if(t.dataset.h==='pdtall'){var sr2=t._n&&M.rawProp(t._n,'onSelectAll');if(sr2&&sr2.trim()!=='null')afterRun(runAt(t,sr2,[true]));return}",
        'pdt fire')
    src = sub1(src, "function fire(t){", "OF.pdtRpp=function(el,v){var r=M.rawProp(el._n,'onRowsPerPageChanged');if(r&&r.trim()!=='null')afterRun(runAt(el,r,[v]))};\nfunction fire(t){", 'pdt rpp fn')
    src = sub1(src, "    var p=new Ps(raw),env=mkEnv({});", "    var p=new Ps(raw),env=mkEnv({});if(ST.__self&&ST.__self.cls){env.self=ST.__self;env.cls=ST.__self.cls}", 'run self')
    src = sub1(src, "ST.run=function(raw,args){", "ST.runSelf=function(selfExpr,raw,args){var obj=null;try{obj=ST.value(selfExpr)}catch(e){}ST.__self=obj;try{return ST.run(raw,args)}finally{ST.__self=null}};\nST.run=function(raw,args){", 'runSelf')
    # ---- Provider: Consumer3, ChangeNotifierProvider.value, Provider.value, ProxyProvider e ChangeNotifierProxyProvider
    src = sub1(src, " Consumer2:{cat:'layout',slots:{child:'one'},desc:'Do pacote provider: escuta dois objetos, <A, B>. builder recebe (context, a, b, child).'},",
        " Consumer2:{cat:'layout',slots:{child:'one'},desc:'Do pacote provider: escuta dois objetos, <A, B>. builder recebe (context, a, b, child).'},\n"
        " Consumer3:{cat:'layout',slots:{child:'one'},desc:'Do pacote provider: escuta três objetos, <A, B, C>. builder recebe (context, a, b, c, child).'},\n"
        " ProxyProvider:{cat:'struct',slots:{child:'one'},desc:'Do pacote provider: cria um objeto a partir de outro provider. update recebe (context, a, anterior).'},\n"
        " ChangeNotifierProxyProvider:{cat:'struct',slots:{child:'one'},desc:'Do pacote provider: ChangeNotifier que depende de outro provider. create cria e update recebe (context, a, anterior).'},", 'consumer3 schema')
    src = sub1(src, "Consumer:1,Consumer2:1,Selector:1,", "Consumer:1,Consumer2:1,Consumer3:1,Selector:1,", 'consumer3 builders')
    src = src.replace("case 'Consumer':case 'Consumer2':case 'Selector':", "case 'Consumer':case 'Consumer2':case 'Consumer3':case 'Selector':")
    src = sub1(src, "  if(n.type==='Consumer2'){",
        "  if(n.type==='Consumer3'){\n"
        "    var c3p=lambdaParts(raw('builder')),c3b=c3p.body,c3g=(n.generic||'').split(',').map(function(x){return x.replace(/[<>?\\s]/g,'')}),c3c=raw('child');\n"
        "    [1,2,3].forEach(function(k){if(c3p.names[k]&&c3g[k-1])c3b=bindVar(c3b,c3p.names[k],{raw:'_prov_'+c3g[k-1]})});\n"
        "    if(c3p.names[4]&&c3c)c3b=bindVar(noBang(c3b,c3p.names[4]),c3p.names[4],{raw:c3c});\n"
        "    expandText(c3b,out);return out}\n"
        "  if(n.type==='Consumer2'){", 'consumer3 expand')
    src = sub1(src, "var ALIAS={ChangeNotifierProvider:'Theme',", "var ALIAS={ProxyProvider:'Theme',ChangeNotifierProxyProvider:'Theme',ProxyProvider2:'Theme',ChangeNotifierProxyProvider2:'Theme',ChangeNotifierProvider:'Theme',", 'proxy alias')
    src = sub1(src, "      if(!info.globals.some(function(g){return g.name==='_prov_'+key}))info.globals.push({name:'_prov_'+key,type:'var',init:init})}\n  })();",
        "      if(!info.globals.some(function(g){return g.name==='_prov_'+key}))info.globals.push({name:'_prov_'+key,type:'var',init:init})}\n"
        "    var rv=/\\b(?:ChangeNotifierProvider|ListenableProvider|Provider)\\s*(?:<\\s*(\\w+)\\??\\s*>)?\\s*\\.\\s*value\\s*(?:<\\s*(\\w+)\\??\\s*>)?\\s*\\(\\s*value\\s*:\\s*/g,mv;\n"
        "    while((mv=rv.exec(src))){var ex=grabArg(src,mv.index+mv[0].length).trim(),k2=mv[1]||mv[2];if(!k2){var cm2=/^(?:const\\s+|new\\s+)?([A-Z]\\w*)\\s*\\(/.exec(ex);if(cm2)k2=cm2[1];else{var gv=info.globals.filter(function(g){return g.name===ex})[0];if(gv){var cm3=/^(?:const\\s+|new\\s+)?([A-Z]\\w*)\\s*\\(/.exec(gv.init||'');k2=cm3?cm3[1]:(gv.type&&/^[A-Z]/.test(gv.type)?gv.type:null)}}}\n"
        "      if(k2&&!info.globals.some(function(g){return g.name==='_prov_'+k2}))info.globals.push({name:'_prov_'+k2,type:'var',init:ex})}\n"
        "    var rp=/\\b(ChangeNotifierProxyProvider|ProxyProvider)\\s*<\\s*(\\w+)\\s*,\\s*(\\w+)\\??\\s*>\\s*\\(/g,mp;\n"
        "    while((mp=rp.exec(src))){var body0=src.slice(mp.index),cr=null,up=null,cmx=/\\bcreate\\s*:/.exec(body0),umx=/\\bupdate\\s*:/.exec(body0);\n"
        "      try{if(cmx)cr=lambdaParts(grabArg(body0,cmx.index+cmx[0].length)).body;if(umx)up=lambdaParts(grabArg(body0,umx.index+umx[0].length))}catch(e){}\n"
        "      var ini=cr||'null';if(up){var ub=up.body;if(up.names[1])ub=bindVar(ub,up.names[1],{raw:'_prov_'+mp[2]});if(up.names[2])ub=bindVar(noBang(ub,up.names[2]),up.names[2],{raw:'('+ini+')'});ini=ub}\n"
        "      if(!info.globals.some(function(g){return g.name==='_prov_'+mp[3]}))info.globals.push({name:'_prov_'+mp[3],type:'var',init:ini,fresh:mp[1]==='ProxyProvider'})}\n"
        "  })();", 'provider value proxy')
    src = sub1(src, "function globalVal(n){var g=ST.globals[n];if(g.fixed)return g.value;",
        "function globalVal(n){var g=ST.globals[n];if(g.fixed)return g.value;if(g.fresh&&g.init!=null){try{return coerce(g.type,ev(pTern(new Ps(g.init)),mkEnv()))}catch(e){return null}}", 'fresh global')
    src = sub1(src, "ST.globals[g.name]={name:g.name,type:g.type,init:g.init,done:false,value:null}", "ST.globals[g.name]={name:g.name,type:g.type,init:g.init,done:false,value:null,fresh:!!g.fresh}", 'fresh flag')
    # ---- laço antigo que sobrou de outro código (hot reload) e falha: sai em silêncio
    src = sub1(src, "  var keepG=(ST.anims||[]).filter(function(v){return v.nat==='Ticker'||v.nat==='Timer'||v.nat==='SensSub'});",
        "  var keepG=(ST.anims||[]).filter(function(v){return v.nat==='Ticker'||v.nat==='Timer'||v.nat==='SensSub'});keepG.forEach(function(v){v.velho=true});", 'keep old flag')
    src = sub1(src, "    catch(e){v.tk.on=false;animDrop(v);ST.tickErr={msg:e.message,exc:!!e.dartExc,src:'Ticker'}}",
        "    catch(e){v.tk.on=false;animDrop(v);if(!v.velho)ST.tickErr={msg:e.message,exc:!!e.dartExc,src:'Ticker'}}", 'old ticker')
    src = sub1(src, "  catch(e){tm.on=false;animDrop(v);ST.tickErr={msg:e.message,exc:!!e.dartExc,src:'Timer'}}",
        "  catch(e){tm.on=false;animDrop(v);if(!v.velho)ST.tickErr={msg:e.message,exc:!!e.dartExc,src:'Timer'}}", 'old timer')
    # ---- go_router: errorBuilder, canPop e refreshListenable
    src = sub1(src, "  var rr=/\\bredirect\\s*:\\s*/g,rm;out.top=null;",
        "  var rr=/\\bredirect\\s*:\\s*/g,rm;out.top=null;out.err=null;out.refresh=/\\brefreshListenable\\s*:/.test(src);\n"
        "  var reb=/\\berrorBuilder\\s*:\\s*/g,eb;while((eb=reb.exec(src))){var at0=eb.index;if(!ranges.some(function(g){return at0>g[0]&&at0<g[1]})){try{out.err=lambdaParts(grabArg(src,at0+eb[0].length).trim())}catch(e){}}}", 'errorBuilder parse')
    src = sub1(src, "  if(!hit)throw new Error('go_router: nenhuma rota combina com \"'+loc+'\"');",
        "  if(!hit&&rs.err&&rs.err.body){ST.lastHit='__erro';ST.lastShell=null;ST.lastBidx=-1;ST.lastLoc=loc;var eb2=rs.err.body.replace(/\\bstate\\s*\\.\\s*(?:matchedLocation|fullPath|location|uri\\s*\\.\\s*path|uri\\s*\\.\\s*toString\\s*\\(\\s*\\)|uri)/g,function(){return lit(loc)}).replace(/\\bstate\\s*\\.\\s*error(?:\\s*\\?\\s*\\.\\s*message|\\s*!\\s*\\.\\s*message)?/g,function(){return lit('GoException: no routes for location: '+loc)});return eb2}\n"
        "  if(!hit)throw new Error('go_router: nenhuma rota combina com \"'+loc+'\"');", 'errorBuilder use')
    src = sub1(src, "    gloc=ST.redirectFor(gloc);", "    gloc=ST.redirectFor(gloc);ST.locAtual=gloc;", 'locAtual')
    src = sub1(src, "  if(n==='ui'||n===ST.uiAlias)return{nat:'UiNS',f:{},src:'ui'};\n  throw new Error('desconhecido '+n)}",
        "  if(n==='ui'||n===ST.uiAlias)return{nat:'UiNS',f:{},src:'ui'};\n  if(n==='context')return{nat:'#ctx',f:{},src:'context'};\n  throw new Error('desconhecido '+n)}", 'context value')
    src = sub1(src, "  var want=ST.homeAbs||'/',tgt=ST.redirectFor(want);return tgt===want?null:tgt};", "  var want=ST.homeAbs||'/',tgt=ST.redirectFor(want);ST.locAtual=tgt;return tgt===want?null:tgt};", 'locAtual init')
    src = sub1(src, "      if(a.name==='notifyListeners'){dirty=true;return null}",
        "      if(a.name==='notifyListeners'){dirty=true;if(ST.routes&&ST.routes.refresh){try{var cur0=ST.locAtual||ST.homeAbs||'/',nl0=ST.redirectFor(cur0);if(nl0!==cur0){ST.locAtual=nl0;ST.fx.push(ST.goFx(nl0))}}catch(e){}}return null}", 'refresh listenable')
    src = sub1(src, "  if(v&&v.nat==='BodyTypeNS')return name;\n",
        "  if(v&&v.nat==='BodyTypeNS')return name;\n  if(name==='canPop'&&(!v||isRaw(v)||v.nat==='#ctx'||v.nat==='GoRouter'||typeof v==='string')){var nv0=window.OF&&OF.R&&OF.R.opts;return !!(nv0&&((nv0.nav&&nv0.nav.length)||(nv0.over||[]).some(function(o){return o.k==='dialog'||o.k==='sheet'})))}\n", 'canPop member')
    src = sub1(src, "      if(a.args&&NATCTOR[a.name])return natCtor(a.name,evalArgs(a,env));",
        "      if(a.args&&a.name==='Navigator.canPop'){var nv1=window.OF&&OF.R&&OF.R.opts;return !!(nv1&&nv1.nav&&nv1.nav.length)}\n"
        "      if(a.args&&NATCTOR[a.name])return natCtor(a.name,evalArgs(a,env));", 'Navigator.canPop')
    return src


CUP_CASES = r'''    case 'CupertinoTimerPicker':{
      d.className+=' cdp'+(R_opts.run?'':' cpkd');var tpk=path.join('>');d.dataset.key=tpk;d.dataset.timer='1';
      var tmode=enumName(M.getProp(n,'mode'))||'hms',tini=durMs(M.getProp(n,'initialTimerDuration')||'Duration()')/1000,tsrc=String(M.getProp(n,'initialTimerDuration')||'');
      var tmi=Math.max(1,Math.trunc(numVal(M.getProp(n,'minuteInterval'))||1)),tsi=Math.max(1,Math.trunc(numVal(M.getProp(n,'secondInterval'))||1));
      var tst=(R_opts.run&&R_opts.dps[tpk]&&R_opts.dps[tpk].src===tsrc)?R_opts.dps[tpk]:{th:Math.floor(tini/3600),tm:Math.floor(tini%3600/60),ts:Math.floor(tini%60),src:tsrc};if(R_opts.run)R_opts.dps[tpk]=tst;
      function tcol(code,max,step,val,rot){var ls=[];for(var i=0;i<max;i+=step)ls.push(i+' '+rot);var w=wheelEl(ls,32,Math.round(val/step),'cdp',tpk,R_opts.run);w.dataset.col=code;w.dataset.step=step;w._pn=n;d.appendChild(w)}
      if(tmode!=='ms')tcol('th',24,1,tst.th,'h');
      tcol('tm',60,tmi,tst.tm,'min');
      if(tmode!=='hm')tcol('ts',60,tsi,tst.ts,'s');
      d.appendChild(mkBand());R_opts.post.push(function(){wheelFix(d)});break}
    case 'CupertinoListSection':case 'CupertinoListSection.insetGrouped':{
      var ins=n.type==='CupertinoListSection.insetGrouped';d.className+=' cls'+(ins?' clsi':'');d.style.alignSelf='stretch';d.style.flex='none';
      if(n.slots.header){var clh=child(n.slots.header,'header','#none');clh.classList.add('clsh');d.appendChild(clh)}
      var clg=document.createElement('div');clg.className='clsg';(n.slots.children||[]).forEach(function(c,i){if(i){var dv=document.createElement('div');dv.className='clsd';clg.appendChild(dv)}clg.appendChild(child(c,'children:'+i,'#none'))});
      if(!(n.slots.children||[]).length)clg.appendChild(ph('children: [ ]'));d.appendChild(clg);
      if(n.slots.footer){var clf=child(n.slots.footer,'footer','#none');clf.classList.add('clsf');d.appendChild(clf)}
      break}
    case 'CupertinoListTile':{
      d.className+=' clt';d.style.alignSelf='stretch';
      if(n.slots.leading){var ctl=child(n.slots.leading,'leading','#none');ctl.classList.add('cltl');d.appendChild(ctl)}
      var ctm=document.createElement('div');ctm.className='cltm';if(n.slots.title)ctm.appendChild(child(n.slots.title,'title','#none'));else ctm.appendChild(ph('title'));
      if(n.slots.subtitle){var cts=child(n.slots.subtitle,'subtitle','#none');cts.classList.add('clts');ctm.appendChild(cts)}d.appendChild(ctm);
      if(n.slots.additionalInfo){var cta=child(n.slots.additionalInfo,'additionalInfo','#none');cta.classList.add('clta');d.appendChild(cta)}
      if(n.slots.trailing){var ctt=child(n.slots.trailing,'trailing','#none');ctt.classList.add('cltt');d.appendChild(ctt)}
      break}
    case 'CupertinoListTileChevron':{d.className+=' cltc';d.textContent='›';break}
    case 'CupertinoSliverNavigationBar':{
      d.className+=' csnb';d.style.alignSelf='stretch';var cnr=document.createElement('div');cnr.className='appbar cnb';
      if(n.slots.leading){var csl=child(n.slots.leading,'leading','#none');csl.classList.add('cnl');cnr.appendChild(csl)}
      else if(R_opts.nav.length){var csb=document.createElement('span');csb.className='bkb hh cnl';csb.dataset.h='back';csb.textContent='‹ Voltar';cnr.appendChild(csb)}
      var csm=document.createElement('div');csm.className='cnm csnm';if(n.slots.middle)csm.appendChild(child(n.slots.middle,'middle','#none'));else if(n.slots.largeTitle)csm.appendChild(child(n.slots.largeTitle,'largeTitle:m','#none'));cnr.appendChild(csm);
      if(n.slots.trailing){var cst=child(n.slots.trailing,'trailing','#none');cst.classList.add('cnt2');cnr.appendChild(cst)}
      d.appendChild(cnr);
      if(n.slots.largeTitle){var clt=child(n.slots.largeTitle,'largeTitle','#none');clt.classList.add('csnl');d.appendChild(clt)}
      R_opts.post.push(function(){var sc=d.closest('.csv');if(!sc||sc._csnb)return;sc._csnb=1;var f=function(){var big=d.querySelector('.csnl'),mid=d.querySelector('.csnm');if(!big)return;var y=sc.scrollTop,k=Math.max(0,Math.min(1,y/44));big.style.opacity=String(1-k);big.style.transform='scale('+(1-k*0.15)+')';if(mid)mid.style.opacity=n.slots.middle?'1':String(k)};sc.addEventListener('scroll',f);f()});
      break}
'''


CSS = """<script>
document.getElementById('screen').addEventListener('change',function(e){var t=e.target;if(!t.classList||!t.classList.contains('pdtrpp'))return;var p=t.closest('.pdt');if(p&&p._n&&window.OF&&OF.pdtRpp)OF.pdtRpp(p,+t.value)});
</script>
<style>
#screen .cls{display:flex;flex-direction:column;gap:6px;padding:14px 0;background:#f2f2f7}
#screen .clsi{padding:14px 16px}
#screen .clsh{font-size:13px;color:#6d6d72;text-transform:uppercase;padding:0 16px;letter-spacing:.02em}
#screen .clsf{font-size:13px;color:#6d6d72;padding:0 16px}
#screen .clsg{background:#fff;display:flex;flex-direction:column}
#screen .clsi .clsg{border-radius:10px;overflow:hidden}
#screen .clsd{height:1px;background:#c6c6c8;margin-left:16px}
#screen .clt{display:flex;align-items:center;gap:12px;min-height:44px;padding:6px 16px;background:#fff;font-size:17px;color:#000}
#screen .cltm{flex:1 1 auto;min-width:0;display:flex;flex-direction:column}
#screen .clts{font-size:13px;color:#6d6d72}
#screen .clta{color:#8a8a8e}
#screen .cltc{color:#c4c4c7;font-size:24px;line-height:1;font-weight:300}
#screen .csnb{background:#f9f9f9;position:sticky;top:0;z-index:3}
#screen .csnl{font-size:34px;font-weight:700;padding:2px 16px 8px;transform-origin:left center;color:#000}
#screen .csnm{font-weight:600}
#screen .pdtarr{font-weight:700;margin-left:2px}
#screen .pdtck{display:flex;align-items:center;justify-content:center}
#screen .pdtbox{font-size:18px;cursor:pointer;line-height:1}
#screen .pdtc.hh{cursor:pointer}
#screen .pdtrpp{font:inherit;padding:0 2px}
#screen .ovl.ent{position:absolute;left:0;right:0;bottom:0;top:24px;z-index:40;pointer-events:none;display:flex;background:none;box-shadow:none;padding:0;margin:0;max-width:none;max-height:none;transform:none;border-radius:0}
#screen .ovl.ent>.nd{flex:1 1 auto;pointer-events:none}
#screen .ovl.ent>.nd>*{pointer-events:auto}
</style>
"""
