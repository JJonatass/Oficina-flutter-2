# Oficina Flutter 2 · Jogos

Simulador de Flutter no navegador com a trilha de jogos 2D, em 94 aulas, 7 projetos e 5 desafios: laço do jogo, Ticker e
delta time, CustomPainter, toque, arrasto, teclado, sprites, som, efeitos visuais, Flame (componentes, efeitos,
partículas, paralaxe, overlays), joystick, Forge2D (corpos, impulsos, contatos, juntas e raycast), sensores de
movimento, mapas do Tiled, inimigos com máquina de estados, recorde com Hive e ranking com Supabase. A Parte 7
fecha com o jogo completo: telas e pausa com o Navigator, plataforma com colisão no mapa, fases com estrelas,
geração procedural, busca de caminho (BFS e A*), desempenho e multijogador em tempo real, e o Projeto 6.
A Parte 8 traz mais sistemas: diálogos e escolhas, inventário salvo em JSON, conquistas, bando (comportamento de
grupo), conta do jogador com Supabase Auth e tradução. A Parte 9 traz mais gêneros e técnicas: IA de turnos com
minimax e poda alfa-beta, combinar 3 com cascatas, quebra-cabeça de caixas com desfazer, câmera (suave, olhar à frente,
zona morta, limites e tremor), salvar o jogo inteiro em espaços, replay e fantasma com passo fixo, jogo de ritmo,
campo de visão com névoa de guerra e o Projeto 7 (defesa de torres com mapa de fluxo e reserva de tiros). A Parte 10
tem cinco desafios (reação, cobrinha, caramelo voador, quebra-blocos, memória), que começam com um esqueleto
jogável e partes marcadas com FAÇA, e o projeto final guiado (documento do jogo, etapas e ficha de avaliação).
O herói é um vira-lata caramelo.

Vinte e três aulas são de leitura (📖), com texto, figuras animadas, um teste rápido e um código para experimentar:
matemática de jogos (vetores, ângulos, interpolação, física e passo de tempo, colisão, probabilidade), game design
(ciclo principal, dificuldade, game feel, design de fases, economia, testes com jogadores, narrativa, análise com MDA, ética e bem-estar do jogador), arte e som (pixel art,
animação, interface e acessibilidade, efeitos e música), arquitetura, publicação e carreira (game jams e portfólio).

Na página:
- **⬇ Projeto** baixa a aula aberta como projeto Flutter (.zip com pubspec.yaml, lib/main.dart, sprites, sons e mapas).
- **Professor** mostra o progresso da turma, baixa a planilha da turma (.csv) e, ligando a opção, a resposta de cada etapa.
- **🎨 Desenhar**: editor de pixel art com quadros de animação; o sprite fica salvo e pode ser usado no código.
- **🗺 Mapa**: editor de fases em blocos que gera o .tmx (camadas, sólidos, perigos, ossos, início e fim).
- **🔗 Compartilhar** gera um link com o código, os sprites e os mapas; **🕹 Galeria** guarda os jogos recebidos,
  com estrelas. Não há servidor: cada jogo fica salvo só no navegador de quem abriu o link.
- **📘 Aula** (botão fixo no canto da tela): abre a aula atual numa janela, com Anterior/Próxima e a lista de todas as aulas por parte, com busca.
- **🧠 Revisão**: seis perguntas por parte, com as opções embaralhadas e o melhor resultado guardado no navegador.
- **📚 Glossário**: termos de jogos com busca e um botão que abre a aula onde cada um aparece.
- No celular, dá para instalar como app (PWA) e abrir sem internet.

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
- `tools/patch_plat.py`: respostas do modo professor, ⬇ Projeto (.zip) e PWA (manifest, sw.js e ícones gerados na raiz)
- `tools/patch_leitura.py`: janela de leitura das aulas 📖, teste rápido e figuras animadas
- `tools/teoria.py`, `tools/teoria/*.dart`: conteúdo e códigos das aulas de leitura
- `tools/parte7.py`, `tools/parte7/*.dart`: Parte 7 (jogo completo) e Projeto 6
- `tools/patch_jogo.py`: um jogo por tela do Navigator, tear-off de métodos, Supabase entre abas, Color.fromRGBO
- `tools/patch_ferramentas.py`: 🎨 Desenhar, 🗺 Mapa, 🔗 Compartilhar, 🕹 Galeria e planilha da turma
- `tools/parte8.py`, `tools/parte8/*.dart`: Partes 8 e 10 (sistemas de jogo, desafios) e Sala de jogos
- `tools/parte9.py`, `tools/parte9/*.dart`: Parte 9 (mais gêneros e técnicas) e Projeto 7
- `tools/revisao.py`, `tools/patch_revisao.py`: perguntas de revisão de cada parte e glossário
- `tools/patch_aula.py`: janela da aula (botão 📘 Aula)
- `tools/solucoes.py`: gabarito das etapas dos exercícios (conferido no build)
- `tools/sprites.py`, `tools/maps.py`: sprites e mapas prontos
- `tools/lessons.py`: aulas, exercícios e partes
