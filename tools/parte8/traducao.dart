import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(debugShowCheckedModeBanner: false, home: Menu()));

// Todos os textos do jogo ficam aqui, um mapa por idioma. Nada de texto solto pelo código.
const textos = {
  'pt': {
    'titulo': 'Caramelo e os Ossos',
    'jogar': 'Jogar',
    'ossos': '{n} ossos',
    'osso1': '1 osso',
    'ossos0': 'Nenhum osso ainda',
    'ola': 'Olá, {nome}!',
    'idioma': 'Idioma',
  },
  'en': {
    'titulo': 'Caramel and the Bones',
    'jogar': 'Play',
    'ossos': '{n} bones',
    'osso1': '1 bone',
    'ossos0': 'No bones yet',
    'ola': 'Hello, {nome}!',
    'idioma': 'Language',
  },
};

const bandeiras = {'pt': '🇧🇷 Português', 'en': '🇺🇸 English'};

class Menu extends StatefulWidget {
  const Menu({super.key});

  @override
  State<Menu> createState() => _MenuState();
}

class _MenuState extends State<Menu> {
  String idioma = 'pt';
  int ossos = 0;
  final String jogador = 'Ana';

  // busca o texto no idioma atual e troca {chaves} pelos valores
  String t(String chave, [Map<String, Object> valores = const {}]) {
    final lingua = textos[idioma] ?? textos['pt']!;
    var s = lingua[chave] ?? textos['pt']![chave] ?? chave;
    for (final k in valores.keys) {
      s = s.replaceAll('{$k}', '${valores[k]}');
    }
    return s;
  }

  // plural: cada idioma diz "0", "1" e "muitos" do seu jeito
  String contarOssos(int n) {
    if (n == 0) return t('ossos0');
    if (n == 1) return t('osso1');
    return t('ossos', {'n': n});
  }

  @override
  Widget build(BuildContext context) {
    final titulo = t('titulo');
    final jogar = t('jogar');
    return Scaffold(
      appBar: AppBar(title: Text(titulo)),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Text(t('ola', {'nome': jogador}), style: const TextStyle(fontSize: 24)),
            const SizedBox(height: 8),
            Text(contarOssos(ossos), style: const TextStyle(fontSize: 20)),
            const SizedBox(height: 16),
            FilledButton(onPressed: () => setState(() => ossos++), child: Text(jogar)),
            const SizedBox(height: 24),
            Text(t('idioma'), style: const TextStyle(fontWeight: FontWeight.bold)),
            for (final codigo in textos.keys)
              RadioListTile<String>(
                value: codigo,
                groupValue: idioma,
                title: Text(bandeiras[codigo] ?? codigo),
                onChanged: (v) => setState(() => idioma = v!),
              ),
          ],
        ),
      ),
    );
  }
}
