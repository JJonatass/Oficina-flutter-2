# Oficina Flutter 2 · Jogos

Simulador de Flutter no navegador com a trilha de jogos 2D, em 38 aulas e 5 projetos: laço do jogo, Ticker e
delta time, CustomPainter, toque, arrasto, teclado, sprites, som, Flame (componentes, efeitos, partículas,
paralaxe, overlays), joystick, Forge2D (corpos, impulsos, contatos, juntas e raycast), sensores de movimento e
mapas do Tiled.

Publicado em https://oficina-flutter-2.vercel.app (cada push no `main` gera um deploy novo).

O `index.html` é gerado; para mudar aulas ou o motor, edite `tools/` e rode:

    python3 tools/build.py

- `tools/upstream.html`: simulador da Oficina Flutter (base)
- `tools/patch_engine.py`: recursos de jogo (Ticker, Timer.periodic, Rect.overlaps, getters do State, hot reload do laço) e a lista de limites
- `tools/patch_input.py`, `patch_media.py`: gestos, teclado, imagens e som
- `tools/patch_flame.py`, `flame_prelude*.dart`: Flame simplificado
- `tools/patch_limits.py`, `patch_extra.py`: música, sprites, overlays, Forge2D e Tiled
- `tools/patch_draw.py`: gradientes, desfoque, BlendMode, drawShadow e drawParagraph
- `tools/patch_dart.py`: registros nomeados, `?.` em cadeia, TextInputFormatter próprio, build com `=>`
- `tools/patch_sens.py`: sensors_plus (DeviceMotionEvent no celular, painel de inclinação no computador)
- `tools/patch_ui.py`: Listener, MouseRegion, Draggable, curvas exatas, AnimatedList e Hero
- `tools/patch_widgets.py`: Overlay, Cupertino, PaginatedDataTable, Provider e go_router
- `tools/patch_data.py`: Hive, Supabase, Google Fonts e NestedScrollView
- `tools/sprites.py`, `tools/maps.py`: sprites e mapas prontos
- `tools/lessons.py`: aulas, exercícios e partes
