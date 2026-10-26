#!/usr/bin/env python3
"""Monta o index.html da Oficina Flutter 2 a partir do simulador original.

  python3 tools/build.py

1. tools/upstream.html  -> simulador da Oficina Flutter (motor, renderizador, editor)
2. tools/patch_engine.py -> recursos de jogo no interpretador (Ticker, Timer, colisão)
3. tools/lessons.py      -> aulas, exercícios, limites e partes da trilha de jogos
"""
import json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
import patch_engine, patch_input, patch_media, patch_flame, patch_limits, patch_extra, lessons  # noqa: E402


def sub1(src, old, new, label):
    n = src.count(old)
    if n != 1:
        raise SystemExit(f'[build] âncora "{label}" encontrada {n} vezes')
    return src.replace(old, new, 1)


def cut(src, start, end, new, label):
    """Troca tudo entre start (incluso) e end (incluso) por new."""
    i = src.find(start)
    j = src.find(end, i)
    if i < 0 or j < 0 or src.count(start) != 1:
        raise SystemExit(f'[build] bloco "{label}" não encontrado')
    return src[:i] + new + src[j + len(end):]


def js(v):
    return json.dumps(v, ensure_ascii=False)


def lessons_js():
    out = []
    for L in lessons.LESSONS:
        o = {'t': 'x. ' + L['t'], 'text': L['text'], 'tryit': L['tryit'], 'code': L['code'].lstrip('\n')}
        if L.get('lim'):
            o['lim'] = L['lim']
        if L.get('setup'):
            o['setup'] = L['setup']
        out.append(js(o))
    return 'var LESSONS=[\n' + ',\n'.join(out) + '\n];\n'


def build():
    src = (ROOT / 'tools' / 'upstream.html').read_text(encoding='utf-8')
    src = patch_engine.patch(src)
    src = patch_input.patch(src)
    src = patch_media.patch(src)
    src = patch_flame.patch(src)
    src = patch_limits.patch(src)
    src = patch_extra.patch(src)

    # marca e textos do cabeçalho
    src = sub1(src, '<title>Oficina Flutter</title>', '<title>Oficina Flutter 2</title>', 'title')
    src = sub1(src, '<b>Oficina Flutter</b><span>monte telas arrastando widgets ou escrevendo Dart</span>',
               '<b>Oficina Flutter 2</b><span>jogos 2D com Flutter: laço, desenho, toque e colisão</span>', 'brand')
    # progresso e banco separados da Oficina 1 (mesmo navegador, chaves diferentes)
    for old, new in [("'oficina.", "'oficina2."), ("'oficina_db'", "'oficina2_db'"), ("'oficinaTela'", "'oficina2Tela'")]:
        if old not in src:
            raise SystemExit(f'[build] chave {old} não encontrada')
        src = src.replace(old, new)

    # aulas
    src = cut(src, 'var LESSONS=[\n', '/*NL-END*/\n];\n', lessons_js(), 'LESSONS')
    src = cut(src, '/*ORDER-BEGIN*/', '/*ORDER-END*/', '/*ORDER-BEGIN*//*ORDER-END*/', 'ORDER')
    src = cut(src, 'var GOALS=[\n', '\n];\nLESSONS.forEach(function(L){GOALS', 'var GOALS=[\n];\nLESSONS.forEach(function(L){GOALS', 'GOALS')
    src = cut(src, 'var LIMS=[\n', '\n];\nLESSONS.forEach(function(L){LIMS', 'var LIMS=[\n];\nLESSONS.forEach(function(L){LIMS', 'LIMS')
    src = re.sub(r"var NOSTATE=\[[^\]]*\];", 'var NOSTATE=[];', src, count=1)
    src = cut(src, '/*PARTS-BEGIN*/', '/*PARTS-END*/',
              '/*PARTS-BEGIN*/\nwindow.OF.PARTS=' + js(lessons.PARTS) + ';\n/*PARTS-END*/', 'PARTS')
    ex = ''.join('add(' + js(k) + ',' + js(v) + ');\n' for k, v in lessons.EXERCISES.items())
    src = cut(src, 'function add(sub,steps){EX[sub]=steps}\n', 'OF.EX=EX;',
              'function add(sub,steps){EX[sub]=steps}\n' + ex + 'OF.EX=EX;', 'EX')
    for k, v in lessons.EXERCISES.items():
        if not any(k in L['t'] for L in lessons.LESSONS):
            raise SystemExit(f'[build] exercícios "{k}" não batem com nenhuma aula')
        code = next(L['code'] for L in lessons.LESSONS if k in L['t']).lstrip('\n')
        for step in v:
            if re.search(step[2], code):
                raise SystemExit(f'[build] a etapa "{step[0]}" ({k}) já vem cumprida no código inicial')

    src = patch_media.finish(src)
    src = patch_limits.finish(src)
    src = src + patch_extra.SPRITES_UI_EXTRA
    (ROOT / 'index.html').write_text(src, encoding='utf-8')
    print(f'index.html: {len(src):,} bytes, {len(lessons.LESSONS)} aulas')


if __name__ == '__main__':
    build()
