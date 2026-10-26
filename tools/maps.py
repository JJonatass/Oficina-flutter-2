"""Mapas prontos do Tiled para a Oficina Flutter 2 (gera tools/maps/*.tmx).

  python3 tools/maps.py

Os mapas usam o tileset tiles.png (8 colunas x 2 linhas de 16x16), incorporado no próprio .tmx, com as camadas em CSV.
Blocos: 1 grama, 2 terra, 3 pedra, 4 tijolo, 5 tábua, 6 água, 7 piso claro, 8 piso escuro,
        9 arbusto, 10 flor, 11 placa, 12 porta, 13 espinhos, 14 escada, 15 gelo, 16 areia.
"""
import pathlib

OUT = pathlib.Path(__file__).resolve().parent / 'maps'
OUT.mkdir(exist_ok=True)
T = 16
TILESET = ('<tileset firstgid="1" name="tiles" tilewidth="16" tileheight="16" tilecount="16" columns="8">\n'
           '  <image source="tiles.png" width="128" height="32"/>\n </tileset>')


def csv(grid):
    return ',\n'.join(','.join(str(v) for v in row) for row in grid)


def layer(i, nome, grid):
    h, w = len(grid), len(grid[0])
    return f' <layer id="{i}" name="{nome}" width="{w}" height="{h}">\n  <data encoding="csv">\n{csv(grid)}\n</data>\n </layer>'


def objgroup(i, nome, objs):
    linhas = []
    for o in objs:
        attrs = f'id="{o["id"]}"' + (f' name="{o["name"]}"' if o.get('name') else '') + (f' type="{o["type"]}"' if o.get('type') else '')
        attrs += f' x="{o["x"]}" y="{o["y"]}"'
        if o.get('w'):
            attrs += f' width="{o["w"]}" height="{o["h"]}"'
        props = o.get('props')
        if props:
            ps = ''.join(f'<property name="{k}" type="{"int" if isinstance(v, int) else "string"}" value="{v}"/>' for k, v in props.items())
            linhas.append(f'  <object {attrs}>\n   <properties>{ps}</properties>\n  </object>')
        elif o.get('w'):
            linhas.append(f'  <object {attrs}/>')
        else:
            linhas.append(f'  <object {attrs}>\n   <point/>\n  </object>')
    return f' <objectgroup id="{i}" name="{nome}">\n' + '\n'.join(linhas) + '\n </objectgroup>'


def rects(grid, solidos):
    """Junta blocos sólidos vizinhos da mesma linha num retângulo e une linhas iguais logo abaixo."""
    h, w = len(grid), len(grid[0])
    runs = []
    for y in range(h):
        x = 0
        while x < w:
            if grid[y][x] in solidos:
                x0 = x
                while x < w and grid[y][x] in solidos:
                    x += 1
                runs.append([x0, y, x - x0, 1])
            else:
                x += 1
    juntos = []
    for r in runs:
        for j in juntos:
            if j[0] == r[0] and j[2] == r[2] and j[1] + j[3] == r[1]:
                j[3] += 1
                break
        else:
            juntos.append(r)
    return juntos


def tmx(w, h, camadas, nid):
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<map version="1.10" tiledversion="1.10.2" orientation="orthogonal" renderorder="right-down" width="{w}" height="{h}" '
            f'tilewidth="16" tileheight="16" infinite="0" nextlayerid="{len(camadas) + 1}" nextobjectid="{nid}">\n '
            + TILESET + '\n' + '\n'.join(camadas) + '\n</map>\n')


# ---------------------------------------------------------------- arena (vista de cima)
ARENA = [
    'PPPPPPPPPPPPPPPPPPPP',
    'P..f......$.....f..P',
    'P.$....A.......$...P',
    'P....PPPP...PPPP...P',
    'P....P.........P.$.P',
    'P.$..P..$...$..P...P',
    'P....P....S....P...P',
    'P..................P',
    'P.f.....$...$.....fP',
    'PPPP...PPPPPPPP..PPP',
    'P..................P',
    'P.$..S.........$...P',
    'P.......A..........P',
    'P...PPP.....PPP..$.P',
    'P...P$.......$P....P',
    'P...P....I....P....P',
    'P...PPPP...PPPP....P',
    'P.$..........$...f.P',
    'P........S.........P',
    'P.f..$.........$...P',
    'PPPPPPPPPPPPPPPPPPPP',
]
AW, AH = len(ARENA[0]), len(ARENA)
chao = [[7 if (x + y) % 2 == 0 else 8 for x in range(AW)] for y in range(AH)]
paredes = [[3 if ARENA[y][x] == 'P' else 0 for x in range(AW)] for y in range(AH)]
deco = [[10 if ARENA[y][x] == 'f' else (9 if ARENA[y][x] == 'A' else 0) for x in range(AW)] for y in range(AH)]
nid = 1
sol = []
for r in rects(paredes, {3}):
    sol.append({'id': nid, 'type': 'parede', 'x': r[0] * T, 'y': r[1] * T, 'w': r[2] * T, 'h': r[3] * T})
    nid += 1
for y in range(AH):
    for x in range(AW):
        if ARENA[y][x] == 'A':
            sol.append({'id': nid, 'type': 'parede', 'x': x * T + 2, 'y': y * T + 4, 'w': 12, 'h': 12})
            nid += 1
objs = []
for y in range(AH):
    for x in range(AW):
        c = ARENA[y][x]
        cx, cy = x * T + T // 2, y * T + T // 2
        if c == '$':
            objs.append({'id': nid, 'name': 'moeda', 'type': 'moeda', 'x': cx, 'y': cy, 'props': {'valor': 1}})
        elif c == 'S':
            objs.append({'id': nid, 'name': 'slime', 'type': 'inimigo', 'x': cx, 'y': cy})
        elif c == 'I':
            objs.append({'id': nid, 'name': 'inicio', 'type': 'inicio', 'x': cx, 'y': cy})
        else:
            continue
        nid += 1
(OUT / 'arena.tmx').write_text(tmx(AW, AH, [layer(1, 'chao', chao), layer(2, 'paredes', paredes), layer(3, 'decoracao', deco),
                                              objgroup(4, 'solidos', sol), objgroup(5, 'objetos', objs)], nid))

# ---------------------------------------------------------------- fase de plataforma (vista de lado)
FASE = [
    '................................................',
    '................................................',
    '................................................',
    '..........$$.............$$$....................',
    '.........====...........======..............F...',
    '...$.....................................$$$#...',
    '..===.........$$...........................#....',
    '.............====.....$......p.........====#....',
    '......f.............=====..GGGG.....f......#....',
    '.I...GGGG.....a.............DDDD...GGGGG...#....',
    'GGGGGDDDD..GGGGGG....GGGG...DDDD^^^DDDDDGGGGGGGG',
    'DDDDDDDDDwwDDDDDDwwwwDDDDwwwDDDDDDDDDDDDDDDDDDDD',
    'DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD',
]
FW, FH = len(FASE[0]), len(FASE)
TIL = {'G': 1, 'D': 2, '=': 5, 'w': 6, '^': 13, '#': 14}
blocos = [[TIL.get(FASE[y][x], 0) for x in range(FW)] for y in range(FH)]
fundo = [[{'f': 10, 'a': 9, 'p': 11}.get(FASE[y][x], 0) for x in range(FW)] for y in range(FH)]
nid = 1
sol = []
for r in rects(blocos, {1, 2}):
    sol.append({'id': nid, 'type': 'chao', 'x': r[0] * T, 'y': r[1] * T, 'w': r[2] * T, 'h': r[3] * T})
    nid += 1
for r in rects(blocos, {5}):
    sol.append({'id': nid, 'type': 'plataforma', 'x': r[0] * T, 'y': r[1] * T, 'w': r[2] * T, 'h': 7})
    nid += 1
objs = []
for r in rects(blocos, {13}):
    objs.append({'id': nid, 'name': 'espinhos', 'type': 'perigo', 'x': r[0] * T, 'y': r[1] * T + 8, 'w': r[2] * T, 'h': 8})
    nid += 1
for r in rects(blocos, {6}):
    objs.append({'id': nid, 'name': 'agua', 'type': 'perigo', 'x': r[0] * T, 'y': r[1] * T + 3, 'w': r[2] * T, 'h': 13})
    nid += 1
for y in range(FH):
    for x in range(FW):
        c = FASE[y][x]
        cx, cy = x * T + T // 2, y * T + T // 2
        if c == '$':
            objs.append({'id': nid, 'name': 'moeda', 'type': 'moeda', 'x': cx, 'y': cy, 'props': {'valor': 1}})
        elif c == 'I':
            objs.append({'id': nid, 'name': 'inicio', 'type': 'inicio', 'x': cx, 'y': (y + 1) * T})
        elif c == 'F':
            objs.append({'id': nid, 'name': 'fim', 'type': 'fim', 'x': x * T, 'y': y * T, 'w': T, 'h': T * 2})
        else:
            continue
        nid += 1
(OUT / 'fase1.tmx').write_text(tmx(FW, FH, [layer(1, 'fundo', fundo), layer(2, 'blocos', blocos),
                                              objgroup(3, 'solidos', sol), objgroup(4, 'objetos', objs)], nid))
print('\n'.join(str(p) for p in sorted(OUT.glob('*.tmx'))))
