import 'package:flutter/material.dart';
import 'package:supabase_flutter/supabase_flutter.dart';

Future<void> main() async {
  await Supabase.initialize(url: 'https://SEU-PROJETO.supabase.co', anonKey: 'SUA-CHAVE-ANON');
  runApp(const MaterialApp(debugShowCheckedModeBanner: false, home: Conta()));
}

final supabase = Supabase.instance.client;

class Conta extends StatefulWidget {
  const Conta({super.key});

  @override
  State<Conta> createState() => _ContaState();
}

class _ContaState extends State<Conta> {
  final email = TextEditingController(text: 'caramelo@escola.br');
  final senha = TextEditingController(text: 'osso1234');
  final int senhaMinima = 6;
  String aviso = '';
  int ossos = 0;
  int fase = 1;

  User? get usuario => supabase.auth.currentUser;

  Future<void> entrar(bool criar) async {
    if (senha.text.length < senhaMinima) {
      setState(() => aviso = 'A senha precisa de pelo menos $senhaMinima caracteres.');
      return;
    }
    try {
      if (criar) {
        await supabase.auth.signUp(email: email.text, password: senha.text);
      } else {
        await supabase.auth.signInWithPassword(email: email.text, password: senha.text);
      }
      await carregar();
      setState(() => aviso = criar ? 'Conta criada!' : 'Bem-vindo de volta!');
    } on AuthException catch (e) {
      setState(() => aviso = 'Não deu: ${e.message}');
    }
  }

  // o progresso de cada jogador é uma linha da tabela, marcada com o id dele
  Future<void> carregar() async {
    final linha = await supabase.from('progresso').select().eq('user_id', usuario!.id).maybeSingle();
    setState(() {
      ossos = linha == null ? 0 : linha['ossos'];
      fase = linha == null ? 1 : linha['fase'];
    });
  }

  Future<void> salvar() async {
    await supabase.from('progresso').upsert({'user_id': usuario!.id, 'ossos': ossos, 'fase': fase}, onConflict: 'user_id');
    setState(() => aviso = 'Progresso salvo na nuvem.');
  }

  Future<void> sair() async {
    await supabase.auth.signOut();
    setState(() {
      aviso = 'Você saiu.';
      ossos = 0;
      fase = 1;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(usuario == null ? 'Entrar no jogo' : 'Olá, ${usuario!.email}')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: usuario == null
            ? Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  TextField(controller: email, decoration: const InputDecoration(labelText: 'E-mail')),
                  TextField(controller: senha, obscureText: true, decoration: const InputDecoration(labelText: 'Senha')),
                  const SizedBox(height: 16),
                  FilledButton(onPressed: () => entrar(false), child: const Text('Entrar')),
                  OutlinedButton(onPressed: () => entrar(true), child: const Text('Criar conta')),
                  const SizedBox(height: 12),
                  Text(aviso),
                ],
              )
            : Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Text('Fase $fase   Ossos: $ossos', style: const TextStyle(fontSize: 24)),
                  const SizedBox(height: 12),
                  FilledButton(onPressed: () => setState(() => ossos++), child: const Text('🦴 Pegar osso')),
                  OutlinedButton(onPressed: () => setState(() => fase++), child: const Text('Passar de fase')),
                  const SizedBox(height: 12),
                  FilledButton(onPressed: salvar, child: const Text('☁ Salvar na nuvem')),
                  TextButton(onPressed: sair, child: const Text('Sair da conta')),
                  const SizedBox(height: 12),
                  Text(aviso),
                ],
              ),
      ),
    );
  }
}
