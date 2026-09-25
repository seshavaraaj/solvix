import 'package:flutter/material.dart';

import '../api.dart';
import '../app_state.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _phone = TextEditingController();
  final _name = TextEditingController();
  final _otp = TextEditingController();
  bool _otpSent = false;
  bool _busy = false;
  String? _error;

  Future<void> _run(Future<void> Function() fn) async {
    setState(() {
      _busy = true;
      _error = null;
    });
    try {
      await fn();
    } on ApiException catch (e) {
      setState(() => _error = e.message);
    } finally {
      if (mounted) setState(() => _busy = false);
    }
  }

  void _sendOtp() => _run(() async {
        if (_phone.text.replaceAll(RegExp(r'\D'), '').length < 10) {
          throw ApiException(422, app.t('phone'));
        }
        await app.api.requestOtp(_phone.text);
        setState(() => _otpSent = true);
      });

  void _verify() => _run(() async {
        final (token, user) = await app.api.verifyOtp(
            _phone.text, _otp.text.trim(), _name.text.trim().isEmpty ? null : _name.text.trim());
        await app.login(token, user);
      });

  Future<void> _editServer() async {
    final ctl = TextEditingController(text: app.api.baseUrl);
    final url = await showDialog<String>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: Text(app.t('server')),
        content: TextField(controller: ctl, keyboardType: TextInputType.url, autofocus: true),
        actions: [
          TextButton(onPressed: () => Navigator.pop(ctx), child: Text(app.t('cancel'))),
          FilledButton(onPressed: () => Navigator.pop(ctx, ctl.text), child: Text(app.t('save'))),
        ],
      ),
    );
    if (url != null && url.trim().isNotEmpty) await app.setApiUrl(url);
    setState(() {});
  }

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    return Scaffold(
      appBar: AppBar(
        actions: [
          TextButton(onPressed: app.toggleLang, child: Text(app.t('language'))),
          IconButton(onPressed: _editServer, icon: const Icon(Icons.dns_outlined), tooltip: app.t('server')),
        ],
      ),
      body: SafeArea(
        child: ListView(
          padding: const EdgeInsets.all(24),
          children: [
            Icon(Icons.water_drop, size: 48, color: scheme.primary),
            const SizedBox(height: 12),
            Text(app.t('appName'),
                style: Theme.of(context).textTheme.headlineMedium?.copyWith(fontWeight: FontWeight.w800)),
            const SizedBox(height: 4),
            Text(app.t('tagline'), style: TextStyle(color: scheme.onSurfaceVariant)),
            const SizedBox(height: 28),
            TextField(
              controller: _phone,
              enabled: !_otpSent,
              keyboardType: TextInputType.phone,
              decoration: InputDecoration(labelText: app.t('phone'), prefixText: '+91 '),
            ),
            if (!_otpSent) ...[
              const SizedBox(height: 12),
              TextField(controller: _name, decoration: InputDecoration(labelText: app.t('name'))),
              const SizedBox(height: 16),
              FilledButton(onPressed: _busy ? null : _sendOtp, child: Text(app.t('sendOtp'))),
            ] else ...[
              const SizedBox(height: 12),
              TextField(
                controller: _otp,
                keyboardType: TextInputType.number,
                autofocus: true,
                decoration: InputDecoration(labelText: app.t('otp'), helperText: app.t('otpHint')),
              ),
              const SizedBox(height: 16),
              FilledButton(onPressed: _busy ? null : _verify, child: Text(app.t('verify'))),
              TextButton(
                onPressed: _busy ? null : () => setState(() => _otpSent = false),
                child: Text(app.t('changeNumber')),
              ),
            ],
            if (_busy) const Padding(padding: EdgeInsets.only(top: 16), child: LinearProgressIndicator()),
            if (_error != null)
              Padding(
                padding: const EdgeInsets.only(top: 12),
                child: Text(_error!, style: TextStyle(color: scheme.error)),
              ),
            const SizedBox(height: 32),
            Text(app.t('demoNotice'), style: TextStyle(color: scheme.onSurfaceVariant, fontSize: 12)),
            Text('${app.t('server')}: ${app.api.baseUrl}',
                style: TextStyle(color: scheme.onSurfaceVariant, fontSize: 12)),
          ],
        ),
      ),
    );
  }
}
