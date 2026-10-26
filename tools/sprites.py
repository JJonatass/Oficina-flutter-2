"""Sprites próprios da Oficina Flutter 2 (pixel art original, livre para uso nas aulas).

  python3 tools/sprites.py   -> grava tools/sprites/*.png e tools/sprites/manifest.json

Cada folha é uma fila de quadros do mesmo tamanho, da esquerda para a direita.
"""
import json, math, pathlib
from PIL import Image, ImageDraw

OUT = pathlib.Path(__file__).resolve().parent / 'sprites'
OUT.mkdir(exist_ok=True)

PAL = {
    '.': None,
    'k': (34, 32, 52), 'w': (255, 255, 255), 'W': (220, 228, 240),
    's': (244, 196, 150), 'S': (214, 156, 112),           # pele
    'r': (220, 64, 52), 'R': (150, 36, 40),               # vermelho
    'b': (52, 120, 220), 'B': (30, 70, 150),              # azul
    'y': (255, 214, 64), 'Y': (220, 150, 30), 'o': (255, 246, 190),
    'g': (96, 196, 86), 'G': (46, 130, 60), 'd': (30, 86, 44),
    'n': (150, 96, 54), 'N': (98, 60, 34), 'm': (196, 140, 86),
    'p': (160, 90, 220), 'P': (100, 50, 160), 'c': (90, 220, 230),
    'e': (130, 140, 160), 'E': (80, 90, 110), 'f': (255, 150, 40),
    'O': (250, 244, 226), 'Q': (214, 200, 168),            # osso
    'C': (214, 140, 62), 'D': (160, 96, 40), 'L': (246, 206, 150), 't': (236, 104, 120),   # caramelo
}


def from_art(rows):
    h, w = len(rows), len(rows[0])
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    for y, row in enumerate(rows):
        assert len(row) == w, (row, w)
        for x, ch in enumerate(row):
            c = PAL[ch]
            if c:
                img.putpixel((x, y), c + (255,))
    return img


def sheet(frames):
    w, h = frames[0].size
    img = Image.new('RGBA', (w * len(frames), h), (0, 0, 0, 0))
    for i, f in enumerate(frames):
        img.paste(f, (i * w, 0))
    return img


# ---- herói: o vira-lata caramelo (16x16, 4 quadros de caminhada, olhando para a direita)
CORPO = [
    '................',
    '................',
    '..........DD....',
    '..D.......DCCC..',
    '..D......CCkCC..',
    '..D......CCCCLLk',
    '...D.....CCCLLL.',
    '...DC...CCCC.t..',
    '....CCCCCCCC....',
    '...CCCCCCCCCC...',
    '...CCCCCCCCCC...',
    '...CLLLLLLLLC...',
]
PATAS = [
    ['...C.C....C.C...', '...C.C....C.C...', '...D.D....D.D...', '................'],
    ['..C...C..C...C..', '..C...C..C...C..', '..D...D..D...D..', '................'],
    ['....CC.....CC...', '....CC.....CC...', '....DD.....DD...', '................'],
    ['...C..C...C..C..', '....C..C...C..C.', '....D..D...D..D.', '................'],
]
def caramelo(i):
    linhas = list(CORPO)
    if i % 2:
        linhas[3] = '.D.' + linhas[3][3:]
        linhas[4] = '.D.' + linhas[4][3:]
        linhas[5] = '..D' + linhas[5][3:]
    return from_art(linhas + PATAS[i])
heroi = sheet([caramelo(i) for i in range(4)])

# ---- osso (16x16, 6 quadros: flutua para cima e para baixo e dá uma brilhada)
OSSO = [
    '.NN..........NN.',
    'NOON........NOQN',
    'NOOONNNNNNNNOOQN',
    '.NOOOOOOOOOOOQN.',
    '.NOOOOOOOOOOQQN.',
    'NOOQNNNNNNNNOQQN',
    'NOQN........NQQN',
    '.NN..........NN.',
]
def osso(dy, brilho):
    img = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    img.paste(from_art(OSSO), (0, 4 + dy))
    if brilho:
        for x, y in brilho:
            img.putpixel((x, y + dy), PAL['y'] + (255,))
    return img
ossos = sheet([osso(0, None), osso(-1, None), osso(-1, [(4, 6), (3, 7), (5, 7), (4, 8)]), osso(0, [(4, 7)]), osso(1, None), osso(1, None)])

# ---- inimigo: gato de rua cinza, de frente (16x16, 2 quadros: olhando e piscando, com o rabo balançando)
# Cada linha tem só a metade esquerda; a direita é o espelho. O rabo entra depois, do lado direito.
GATO = [
    '........',
    '.E......',
    '.EE.....',
    '.EtE....',
    '.EttEEEE',
    '.Eeeeeee',
    '.EeEeeee',
    '.Eegkeee',
    '.Eeeeeet',
    '.Eeeeeke',
    '..EEeeee',
    '..EeeWWW',
    '.EeeeWWW',
    '.EeeeWWW',
    '.EeEeeWW',
    '.EEEEEEE',
]
def gato(piscando, rabo):
    linhas = [m + m[::-1] for m in GATO]
    if piscando:
        linhas[7] = linhas[7].replace('gk', 'EE').replace('kg', 'EE')
    linhas = [list(l) for l in linhas]
    for y, x in rabo:
        linhas[y][x] = 'E'
    return from_art([''.join(l) for l in linhas])
gato_img = sheet([gato(False, [(14, 15), (13, 15), (12, 15), (11, 14)]), gato(True, [(14, 15), (13, 15), (12, 14), (11, 14), (10, 15)])])

# ---- caixa (16x16)
caixa = from_art([
    'NNNNNNNNNNNNNNNN',
    'NmmmmmmmmmmmmmmN',
    'NmNnnnnnnnnnnNmN',
    'NmnNnnnnnnnnNnmN',
    'NmnnNnnnnnnNnnmN',
    'NmnnnNnnnnNnnnmN',
    'NmnnnnNnnNnnnnmN',
    'NmnnnnnNNnnnnnmN',
    'NmnnnnnNNnnnnnmN',
    'NmnnnnNnnNnnnnmN',
    'NmnnnNnnnnNnnnmN',
    'NmnnNnnnnnnNnnmN',
    'NmnNnnnnnnnnNnmN',
    'NmNnnnnnnnnnnNmN',
    'NmmmmmmmmmmmmmmN',
    'NNNNNNNNNNNNNNNN',
])

# ---- nave (16x16, apontando para cima, 2 quadros com fogo)
NAVE = [
    '.......ww.......',
    '......wWWw......',
    '......WccW......',
    '.....WWccWW.....',
    '.....WWWWWW.....',
    '....WWWWWWWW....',
    '...rWWWEEWWWr...',
    '..rrWWEEEEWWrr..',
    '.rrrWWWWWWWWrrr.',
    'rrrEEWWWWWWEErrr',
    'rr..EEEWWEEE..rr',
    '.....EE..EE.....',
]
nave = sheet([from_art(NAVE + f) for f in (
    ['.....yy..yy.....', '.....ff..ff.....', '......f..f......', '................'],
    ['.....yy..yy.....', '.....yy..yy.....', '.....ff..ff.....', '.....f....f.....'],
)])

# ---- tiro (8x8)
tiro = from_art([
    '...cc...', '..cwwc..', '..cwwc..', '..cwwc..', '..cwwc..', '...cc...', '...cc...', '....c...',
])

# ---- explosão (16x16, 5 quadros)
def explosao(i):
    img = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    r = [3, 5, 7, 7, 6][i]
    cores = [('w', 'y'), ('y', 'f'), ('f', 'r'), ('r', 'R'), ('E', 'e')][i]
    d.ellipse([8 - r, 8 - r, 7 + r, 7 + r], fill=PAL[cores[1]] + (255,))
    if i < 4:
        d.ellipse([8 - r // 2 - 1, 8 - r // 2 - 1, 7 + r // 2, 7 + r // 2], fill=PAL[cores[0]] + (255,))
    if i >= 2:
        for a in range(8):
            x = 8 + math.cos(a * math.pi / 4) * (r + 1)
            y = 8 + math.sin(a * math.pi / 4) * (r + 1)
            d.point([(round(x), round(y))], fill=PAL[cores[1]] + (255,))
    if i == 4:
        d.ellipse([5, 5, 10, 10], fill=(0, 0, 0, 0))
    return img
explosoes = sheet([explosao(i) for i in range(5)])

# ---- coração (16x16)
coracao = from_art([
    '................',
    '................',
    '...RRR....RRR...',
    '..RrrrR..RrrrR..',
    '.RrwwrrRRrrrrrR.',
    '.RrwrrrrrrrrrrR.',
    '.RrrrrrrrrrrrrR.',
    '.RrrrrrrrrrrrrR.',
    '..RrrrrrrrrrrR..',
    '...RrrrrrrrrR...',
    '....RrrrrrrR....',
    '.....RrrrrR.....',
    '......RrrR......',
    '.......RR.......',
    '................',
    '................',
])

# ---- maçã (16x16)
maca = from_art([
    '................',
    '.......N........',
    '.......N.GG.....',
    '......NGggG.....',
    '...RRRRNRRRR....',
    '..RrrrrRrrrrR...',
    '.RrwwrrrrrrrrR..',
    '.RrwrrrrrrrrrR..',
    '.RrrrrrrrrrrrR..',
    '.RrrrrrrrrrrrR..',
    '.RrrrrrrrrrrrR..',
    '..RrrrrrrrrrR...',
    '..RRrrrrrrrRR...',
    '...RRRRRRRRR....',
    '................',
    '................',
])

# ---- grama (bloco de chão 16x16)
grama = from_art([
    'gGgggGgggGgggGgg',
    'ggGgggggGgggggGg',
    'GgggGgggggGggggg',
    'dGddGddGdddGddGd',
    'NnnnmnnnnNnnnmnn',
    'nnNnnnnmnnnnNnnn',
    'nmnnnNnnnnmnnnnN',
    'nnnnnnnnNnnnnnnn',
    'NnnmnnnnnnnNnnmn',
    'nnnnnNnnmnnnnnnn',
    'nNnnnnnnnnNnnnnN',
    'nnnmnnNnnnnnmnnn',
    'nnnnnnnnnNnnnnnn',
    'mnnNnnnmnnnnnNnn',
    'nnnnnnnnnnnmnnnn',
    'nNnnnmnnNnnnnnnn',
])

# ---- nuvem (32x16)
nuvem = Image.new('RGBA', (32, 16), (0, 0, 0, 0))
dn = ImageDraw.Draw(nuvem)
for box in ([2, 7, 12, 15], [7, 2, 19, 14], [15, 4, 26, 15], [22, 8, 30, 15]):
    dn.ellipse(box, fill=PAL['W'] + (255,))
for box in ([3, 7, 12, 13], [8, 3, 18, 12], [16, 5, 25, 13], [23, 9, 29, 13]):
    dn.ellipse(box, fill=PAL['w'] + (255,))

# ---- camadas de fundo para parallax (128x224, em pé como a tela do celular; repetem na horizontal sem emenda)
import random
PW, PH = 128, 224
ceu = Image.new('RGBA', (PW, PH))
for y in range(PH):
    t = y / (PH - 1)
    c = tuple(int(a + (b - a) * t) for a, b in zip((78, 140, 226), (206, 234, 252)))
    for x in range(PW):
        ceu.putpixel((x, y), c + (255,))
for cx, cy, esc in ((18, 30, 1), (70, 18, 1), (104, 62, 1), (40, 92, 1)):
    n = nuvem if esc == 1 else nuvem
    ceu.alpha_composite(n, ((cx - 16) % PW, cy - 8))
    if cx - 16 + 32 > PW:
        ceu.alpha_composite(n, (cx - 16 - PW, cy - 8))


def silhueta(alturas, cor, cor2=None, borda=2):
    img = Image.new('RGBA', (PW, PH), (0, 0, 0, 0))
    for x in range(PW):
        h = int(alturas(x))
        for y in range(PH - h, PH):
            c = cor if (cor2 is None or y < PH - h + borda) else cor2
            img.putpixel((x, y), c + (255,))
    return img


montanhas = silhueta(lambda x: 92 + 34 * abs(math.sin(math.pi * x / 64)) ** 0.8 + 7 * math.sin(2 * math.pi * x / 16),
                     (122, 132, 196), (100, 108, 172))
for x in range(PW):
    topo = next(y for y in range(PH) if montanhas.getpixel((x, y))[3])
    if topo < PH - 112:
        for y in range(topo, min(PH, topo + 6 + (x % 3))):
            montanhas.putpixel((x, y), (238, 242, 252, 255))
colinas = silhueta(lambda x: 52 + 9 * math.sin(2 * math.pi * x / 128) + 4 * math.sin(2 * math.pi * x / 32), (82, 170, 96), (60, 140, 76), 3)
dc = ImageDraw.Draw(colinas)
for tx in (14, 58, 96):
    base = PH - int(52 + 9 * math.sin(2 * math.pi * tx / 128) + 4 * math.sin(2 * math.pi * tx / 32)) + 2
    dc.rectangle([tx, base - 10, tx + 2, base + 2], fill=PAL['N'] + (255,))
    dc.ellipse([tx - 7, base - 28, tx + 9, base - 7], fill=PAL['G'] + (255,))
    dc.ellipse([tx - 4, base - 26, tx + 5, base - 15], fill=PAL['g'] + (255,))

# ---- blocos para mapas do Tiled (8 colunas x 2 linhas de 16x16; o número do bloco no Tiled começa em 1)
rnd = random.Random(7)


def bloco(fundo, pontos=(), prob=0.0, transparente=False):
    b = Image.new('RGBA', (16, 16), (0, 0, 0, 0) if transparente else fundo + (255,))
    for y in range(16):
        for x in range(16):
            if pontos and rnd.random() < prob:
                b.putpixel((x, y), rnd.choice(pontos) + (255,))
    return b


def grama_topo():
    b = bloco(PAL['n'], (PAL['N'], PAL['m']), 0.12)
    for x in range(16):
        h = 4 + (1 if (x * 7) % 5 == 0 else 0)
        for y in range(h):
            b.putpixel((x, y), (PAL['g'] if y < h - 1 else PAL['G']) + (255,))
    return b


def pedra():
    b = bloco((130, 136, 150), ((112, 118, 132), (150, 156, 170)), 0.2)
    d = ImageDraw.Draw(b)
    for y in (0, 8):
        d.line([0, y, 15, y], fill=(90, 96, 110, 255))
    for x, y0 in ((5, 0), (12, 0), (2, 8), (9, 8)):
        d.line([x, y0, x, y0 + 7], fill=(90, 96, 110, 255))
    return b


def tijolo():
    b = bloco((176, 82, 56), ((160, 70, 48), (190, 96, 66)), 0.15)
    d = ImageDraw.Draw(b)
    for y in (3, 7, 11, 15):
        d.line([0, y, 15, y], fill=(226, 206, 180, 255))
    for i, y in enumerate((0, 4, 8, 12)):
        for x in ((7,) if i % 2 == 0 else (3, 11)):
            d.line([x, y, x, y + 2], fill=(226, 206, 180, 255))
    return b


def tabua():
    b = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(b)
    d.rectangle([0, 0, 15, 6], fill=PAL['m'] + (255,))
    d.line([0, 6, 15, 6], fill=PAL['N'] + (255,))
    d.line([0, 0, 15, 0], fill=(222, 170, 110, 255))
    for x in (4, 11):
        d.point((x, 3), fill=PAL['N'] + (255,))
    return b


def agua():
    b = bloco((52, 120, 220), ((70, 140, 230), (44, 104, 200)), 0.15)
    d = ImageDraw.Draw(b)
    d.line([0, 2, 3, 1, 7, 2, 11, 1, 15, 2], fill=(160, 210, 250, 255))
    return b


def piso(c1, c2):
    b = Image.new('RGBA', (16, 16), c1 + (255,))
    d = ImageDraw.Draw(b)
    d.rectangle([0, 0, 15, 15], outline=c2 + (255,))
    d.point((4, 4), fill=c2 + (255,))
    d.point((11, 10), fill=c2 + (255,))
    return b


def arbusto():
    b = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(b)
    d.ellipse([1, 6, 9, 15], fill=PAL['G'] + (255,))
    d.ellipse([6, 4, 15, 15], fill=PAL['G'] + (255,))
    d.ellipse([3, 7, 8, 12], fill=PAL['g'] + (255,))
    d.ellipse([8, 6, 13, 11], fill=PAL['g'] + (255,))
    return b


def flor():
    b = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(b)
    d.line([7, 8, 7, 15], fill=PAL['G'] + (255,))
    d.ellipse([4, 3, 10, 9], fill=PAL['p'] + (255,))
    d.point((7, 6), fill=PAL['y'] + (255,))
    return b


def placa():
    b = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(b)
    d.rectangle([7, 8, 8, 15], fill=PAL['N'] + (255,))
    d.rectangle([2, 2, 13, 9], fill=PAL['m'] + (255,), outline=PAL['N'] + (255,))
    d.line([4, 5, 11, 5], fill=PAL['N'] + (255,))
    return b


def porta():
    b = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(b)
    d.rectangle([2, 1, 13, 15], fill=PAL['N'] + (255,))
    d.rectangle([4, 3, 11, 15], fill=PAL['n'] + (255,))
    d.point((10, 9), fill=PAL['y'] + (255,))
    return b


def espinhos():
    b = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(b)
    for x0 in (0, 4, 8, 12):
        d.polygon([(x0, 15), (x0 + 2, 7), (x0 + 3, 15)], fill=PAL['e'] + (255,))
        d.line([x0 + 2, 8, x0 + 2, 14], fill=PAL['W'] + (255,))
    return b


def escada():
    b = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(b)
    d.line([3, 0, 3, 15], fill=PAL['N'] + (255,), width=2)
    d.line([12, 0, 12, 15], fill=PAL['N'] + (255,), width=2)
    for y in (2, 7, 12):
        d.line([4, y, 11, y], fill=PAL['m'] + (255,))
    return b


tiles = sheet([grama_topo(), bloco(PAL['n'], (PAL['N'], PAL['m']), 0.12), pedra(), tijolo(), tabua(), agua(),
               piso((214, 200, 168), (190, 174, 140)), piso((168, 176, 150), (146, 154, 128)),
               arbusto(), flor(), placa(), porta(), espinhos(), escada(),
               bloco((190, 230, 248), ((220, 244, 255), (160, 210, 236)), 0.15), bloco((236, 210, 140), ((220, 192, 120), (246, 226, 164)), 0.2)])


def agua_quadro(desl):
    b = bloco((52, 120, 220), ((70, 140, 230), (44, 104, 200)), 0.15)
    d = ImageDraw.Draw(b)
    pts = []
    for x in range(0, 17, 4):
        pts += [x, 2 if ((x // 4 + desl) % 2 == 0) else 1]
    d.line(pts, fill=(160, 210, 250, 255))
    d.point(((5 + desl * 5) % 16, 8), fill=(160, 210, 250, 255))
    return b


def tocha(q):
    b = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(b)
    d.rectangle([7, 8, 8, 15], fill=PAL['N'] + (255,))
    chama = [(4, 8, 11, 2), (5, 8, 10, 3), (4, 8, 11, 1)][q]
    d.ellipse([chama[0], chama[3], chama[2], chama[1] + 1], fill=PAL['f'] + (255,))
    d.ellipse([chama[0] + 2, chama[3] + 2, chama[2] - 2, chama[1]], fill=PAL['y'] + (255,))
    return b


tiles_img = Image.new('RGBA', (128, 48), (0, 0, 0, 0))
tiles_img.paste(tiles.crop((0, 0, 128, 16)), (0, 0))
tiles_img.paste(tiles.crop((128, 0, 256, 16)), (0, 16))
for i, t in enumerate([agua_quadro(1), agua_quadro(2), tocha(0), tocha(1), tocha(2)]):
    tiles_img.paste(t, (i * 16, 32))

# ---- blocos isométricos (losangos 32x16 com 8 de altura extra para o bloco)
def losango(topo, lado1, lado2, alto=True):
    b = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(b)
    y0 = 8 if alto else 16
    if alto:
        d.polygon([(0, y0 + 8), (16, y0 + 16), (16, 32), (0, 24)], fill=lado1 + (255,))
        d.polygon([(16, y0 + 16), (32, y0 + 8), (32, 24), (16, 32)], fill=lado2 + (255,))
    d.polygon([(16, y0), (32, y0 + 8), (16, y0 + 16), (0, y0 + 8)], fill=topo + (255,))
    return b


iso = Image.new('RGBA', (128, 32), (0, 0, 0, 0))
for i, t in enumerate([losango((96, 196, 86), (70, 150, 60), (50, 120, 46), False), losango((150, 96, 54), (120, 76, 42), (98, 60, 34)),
                       losango((52, 120, 220), (40, 100, 190), (30, 80, 160), False), losango((150, 156, 170), (120, 126, 140), (95, 100, 115))]):
    iso.paste(t, (i * 32, 0))


SPRITES = [
    ('heroi', heroi, 4, 'Herói: o vira-lata caramelo andando para a direita (4 quadros de 16×16)'),
    ('osso', ossos, 6, 'Osso flutuando e brilhando (6 quadros de 16×16)'),
    ('gato', gato_img, 2, 'Inimigo: gato de rua cinza, piscando e balançando o rabo (2 quadros de 16×16)'),
    ('nave', nave, 2, 'Nave apontando para cima, com fogo (2 quadros de 16×16)'),
    ('explosao', explosoes, 5, 'Explosão (5 quadros de 16×16)'),
    ('tiro', tiro, 1, 'Tiro de laser (8×8)'),
    ('caixa', caixa, 1, 'Caixa de madeira (16×16)'),
    ('coracao', coracao, 1, 'Coração para vidas (16×16)'),
    ('maca', maca, 1, 'Maçã (16×16)'),
    ('grama', grama, 1, 'Bloco de chão com grama (16×16)'),
    ('nuvem', nuvem, 1, 'Nuvem (32×16)'),
    ('ceu', ceu, 1, 'Fundo de céu para parallax (128×224)'),
    ('montanhas', montanhas, 1, 'Montanhas com fundo transparente, para parallax (128×224)'),
    ('colinas', colinas, 1, 'Colinas com árvores, fundo transparente, para parallax (128×224)'),
    ('tiles', tiles_img, 1, 'Blocos para mapas do Tiled: 8 colunas × 3 linhas de 16×16 (a última traz quadros de água e tocha)'),
    ('tiles_iso', iso, 1, 'Blocos isométricos para o Tiled: 4 de 32×32 (grama, terra, água, pedra)'),
]

manifest = []
for nome, img, quadros, desc in SPRITES:
    img.save(OUT / f'{nome}.png', optimize=True)
    manifest.append({'nome': nome, 'caminho': f'assets/sprites/{nome}.png', 'largura': img.width,
                     'altura': img.height, 'quadros': quadros, 'desc': desc})
(OUT / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=1))

# folha de conferência ampliada
prev = Image.new('RGBA', (8 + sum(i.width * 4 + 8 for _, i, _, _ in SPRITES[:6]), 2 * (16 * 4 + 8) + 8), (40, 44, 60, 255))
x, y = 8, 8
for k, (_, img, _, _) in enumerate(SPRITES):
    if k == 6:
        x, y = 8, 16 * 4 + 16
    big = img.resize((img.width * 4, img.height * 4), Image.NEAREST)
    prev.alpha_composite(big, (x, y))
    x += big.width + 8
prev.save(OUT.parent / 'sprites_preview.png')
print('\n'.join(f"{m['caminho']}  {m['largura']}x{m['altura']}  {m['quadros']} quadro(s)" for m in manifest))
