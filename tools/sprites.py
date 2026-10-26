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


# ---- herói (16x16, 4 quadros de caminhada, olhando para a direita)
HEAD = [
    '................',
    '.....RRRRRR.....',
    '....RrrrrrrR....',
    '...RrrrrrrrrrR..',
    '....kkssssss....',
    '....ksskskss....',
    '....ssssssss....',
    '.....ssSSss.....',
]
TORSO = [
    '....bbbbbbb.....',
    '...sbbbbbbbs....',
    '...sbBbbbBbs....',
    '....BBBBBBB.....',
]
LEGS = [
    ['....BB...BB.....', '....BB...BB.....', '...kkk...kkk....', '................'],
    ['.....BB.BB......', '.....BB.BB......', '.....kkkkk......', '................'],
    ['...BB.....BB....', '..BB.......BB...', '..kkk.......kkk.', '................'],
    ['.....BB.BB......', '.....BB.BB......', '.....kkkkk......', '................'],
]
heroi = sheet([from_art(HEAD + TORSO + l) for l in LEGS])

# ---- moeda (16x16, 6 quadros girando)
def moeda(wd):
    img = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    x0, x1 = 8 - wd / 2, 8 + wd / 2 - 1
    d.ellipse([x0, 2, x1, 13], fill=PAL['Y'] + (255,))
    if wd > 3:
        d.ellipse([x0 + 1, 3, x1 - 1, 12], fill=PAL['y'] + (255,))
        if wd > 7:
            d.line([8, 5, 8, 10], fill=PAL['Y'] + (255,))
            d.point([(x0 + 2, 5)], fill=PAL['o'] + (255,))
    return img
moedas = sheet([moeda(w) for w in (12, 10, 6, 2, 6, 10)])

# ---- slime (16x16, 2 quadros)
SLIME = [
    ['................'] * 6 + [
     '.....GGGGGG.....',
     '....GggggggG....',
     '...GgwwggwwgG...',
     '...GgwkggwkgG...',
     '..GgggggggggggG.'[:16],
     '..Ggggggggggggg.'[:16],
     '..GgggkkkkgggggG'[:16],
     '..GggggggggggggG'[:16],
     '...GGGGGGGGGGGG.'[:16],
     '................'],
    ['................'] * 8 + [
     '....GGGGGGGG....',
     '..GGggwwggwwgGG.',
     '.GgggwkggwkggggG',
     '.GgggggggggggggG',
     '.GggggkkkkgggggG',
     '..GGGGGGGGGGGGG.',
     '................',
     '................'],
]
slime = sheet([from_art([r.ljust(16, '.')[:16] for r in f]) for f in SLIME])

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

# ---- camadas de fundo para parallax (96x54, repetem na horizontal sem emenda)
PW, PH = 96, 54
ceu = Image.new('RGBA', (PW, PH))
for y in range(PH):
    t = y / (PH - 1)
    c = tuple(int(a + (b - a) * t) for a, b in zip((92, 156, 236), (196, 228, 250)))
    for x in range(PW):
        ceu.putpixel((x, y), c + (255,))
for cx, cy in ((14, 10), (52, 6), (80, 14)):
    ceu.alpha_composite(nuvem.resize((16, 8), Image.NEAREST), (cx - 8, cy - 4))


def silhueta(alturas, cor, cor2=None):
    img = Image.new('RGBA', (PW, PH), (0, 0, 0, 0))
    for x in range(PW):
        h = int(alturas(x))
        for y in range(PH - h, PH):
            c = cor if (cor2 is None or y < PH - h + 2) else cor2
            img.putpixel((x, y), c + (255,))
    return img


montanhas = silhueta(lambda x: 22 + 12 * abs(math.sin(math.pi * x / 48)) ** 0.8 + 3 * math.sin(2 * math.pi * x / 12),
                     (120, 132, 190), (98, 108, 168))
for x in range(PW):  # neve nos picos
    for y in range(PH):
        if montanhas.getpixel((x, y))[3] and y < 20:
            montanhas.putpixel((x, y), (236, 240, 250, 255))
colinas = silhueta(lambda x: 12 + 4 * math.sin(2 * math.pi * x / 96) + 2 * math.sin(2 * math.pi * x / 32), (70, 160, 90), (52, 128, 70))
dc = ImageDraw.Draw(colinas)
for tx in (10, 40, 70):  # árvores
    base = PH - int(12 + 4 * math.sin(2 * math.pi * tx / 96) + 2 * math.sin(2 * math.pi * tx / 32))
    dc.rectangle([tx, base - 6, tx + 1, base + 1], fill=PAL['N'] + (255,))
    dc.ellipse([tx - 4, base - 15, tx + 5, base - 4], fill=PAL['G'] + (255,))
    dc.ellipse([tx - 2, base - 14, tx + 3, base - 8], fill=PAL['g'] + (255,))

SPRITES = [
    ('heroi', heroi, 4, 'Herói andando para a direita (4 quadros de 16×16)'),
    ('moeda', moedas, 6, 'Moeda girando (6 quadros de 16×16)'),
    ('slime', slime, 2, 'Inimigo slime pulsando (2 quadros de 16×16)'),
    ('nave', nave, 2, 'Nave apontando para cima, com fogo (2 quadros de 16×16)'),
    ('explosao', explosoes, 5, 'Explosão (5 quadros de 16×16)'),
    ('tiro', tiro, 1, 'Tiro de laser (8×8)'),
    ('caixa', caixa, 1, 'Caixa de madeira (16×16)'),
    ('coracao', coracao, 1, 'Coração para vidas (16×16)'),
    ('maca', maca, 1, 'Maçã (16×16)'),
    ('grama', grama, 1, 'Bloco de chão com grama (16×16)'),
    ('nuvem', nuvem, 1, 'Nuvem (32×16)'),
    ('ceu', ceu, 1, 'Fundo de céu para parallax (96×54)'),
    ('montanhas', montanhas, 1, 'Montanhas com fundo transparente, para parallax (96×54)'),
    ('colinas', colinas, 1, 'Colinas com árvores, fundo transparente, para parallax (96×54)'),
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
