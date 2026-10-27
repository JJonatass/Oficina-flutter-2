import 'package:flutter/material.dart';
import 'package:hive_flutter/hive_flutter.dart';

Future<void> main() async {
  await Hive.initFlutter();
  await Hive.openBox('publicar');
  runApp(const MaterialApp(debugShowCheckedModeBanner: false, home: Lista()));
}

class Etapa {
  final String grupo;
  final String titulo;
  final String comoFazer;
  const Etapa(this.grupo, this.titulo, this.comoFazer);
}

const String versao = '1.0.0+1';
const grupos = ['Identidade', 'Versão', 'Qualidade', 'Loja'];

const etapas = [
  Etapa('Identidade', 'Nome do jogo', 'android:label no AndroidManifest.xml e CFBundleDisplayName no Info.plist.'),
  Etapa('Identidade', 'Ícone', 'flutter pub add dev:flutter_launcher_icons e rode dart run flutter_launcher_icons.'),
  Etapa('Identidade', 'Tela de abertura', 'flutter pub add dev:flutter_native_splash e rode dart run flutter_native_splash:create.'),
  Etapa('Identidade', 'Id do pacote', 'applicationId em android/app/build.gradle (ex.: br.edu.escola.caramelo). Não muda depois de publicar.'),
  Etapa('Versão', 'Versão $versao', 'version: no pubspec.yaml. O número depois do + precisa crescer a cada envio para a loja.'),
  Etapa('Qualidade', 'Testar num celular de verdade', 'flutter run --release num aparelho simples, não só no emulador.'),
  Etapa('Qualidade', 'Sem prints e testes de mentira', 'Tire os print(), as chaves de teste e os atalhos de trapaça.'),
  Etapa('Loja', 'Chave de assinatura', 'keytool -genkey ... e configure o key.properties. Guarde a chave: sem ela não há atualização.'),
  Etapa('Loja', 'Gerar o pacote', 'flutter build appbundle (Android) ou flutter build ipa (iOS) ou flutter build web.'),
  Etapa('Loja', 'Página da loja', 'Descrição curta, capturas de tela, classificação indicativa e política de privacidade.'),
];

class Lista extends StatefulWidget {
  const Lista({super.key});

  @override
  State<Lista> createState() => _ListaState();
}

class _ListaState extends State<Lista> {
  final caixa = Hive.box('publicar');

  bool feito(Etapa e) => caixa.get(e.titulo, defaultValue: false);

  @override
  Widget build(BuildContext context) {
    final prontas = etapas.where((e) => feito(e)).length;
    return Scaffold(
      appBar: AppBar(title: Text('Publicar: $prontas de ${etapas.length}')),
      body: ListView(
        children: [
          LinearProgressIndicator(value: prontas / etapas.length, minHeight: 8),
          for (final g in grupos)
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Padding(
                  padding: const EdgeInsets.fromLTRB(16, 16, 16, 4),
                  child: Text(g, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                ),
                for (final e in etapas.where((x) => x.grupo == g))
                  CheckboxListTile(
                    value: feito(e),
                    title: Text(e.titulo),
                    subtitle: Text(e.comoFazer),
                    onChanged: (v) => setState(() {
                      caixa.put(e.titulo, v);
                    }),
                  ),
              ],
            ),
          if (prontas == etapas.length)
            const Padding(
              padding: EdgeInsets.all(16),
              child: Text('Tudo pronto: pode enviar para a loja! 🎉', style: TextStyle(fontSize: 18)),
            ),
        ],
      ),
    );
  }
}
