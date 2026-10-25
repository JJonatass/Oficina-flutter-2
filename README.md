# Oficina Flutter 2 · Jogos

Simulador de Flutter no navegador com a trilha de jogos 2D: laço do jogo, Ticker e delta time,
CustomPainter, toque, gravidade, listas de objetos, colisão AABB, estados e o projeto Pula-Caixa.

O `index.html` é gerado; para mudar aulas ou o motor, edite `tools/` e rode:

    python3 tools/build.py

- `tools/upstream.html`: simulador da Oficina Flutter (base)
- `tools/patch_engine.py`: recursos de jogo (Ticker, Timer.periodic, Rect.overlaps, getters do State, hot reload do laço)
- `tools/lessons.py`: aulas, exercícios e partes
