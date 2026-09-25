import 'dart:convert';

import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'api.dart';
import 'i18n.dart';
import 'local_store.dart';
import 'models.dart';
import 'sync.dart';

/// Server used when none is saved. Override at build time:
/// flutter build apk --dart-define=API_URL=https://meetpu-api.onrender.com
const defaultApiUrl = String.fromEnvironment('API_URL', defaultValue: 'http://10.0.2.2:8000');

/// Everything the screens share: session, language, API client, offline queue.
class AppState extends ChangeNotifier {
  late final SharedPreferences _prefs;
  late final Api api;
  final LocalStore store = LocalStore();
  late final SyncService sync;

  AppUser? user;
  String lang = 'en';

  String t(String key) => translate(lang, key);

  Future<void> init() async {
    _prefs = await SharedPreferences.getInstance();
    await store.open();
    lang = _prefs.getString('lang') ?? 'en';
    api = Api(_prefs.getString('api_url') ?? defaultApiUrl);
    api.token = _prefs.getString('token');
    api.onUnauthorized = logout;
    final u = _prefs.getString('user');
    if (api.token != null && u != null) user = AppUser.fromJson(jsonDecode(u) as Map<String, dynamic>);
    sync = SyncService(api, store);
    await sync.start();
  }

  void toggleLang() {
    lang = lang == 'en' ? 'ta' : 'en';
    _prefs.setString('lang', lang);
    notifyListeners();
  }

  Future<void> setApiUrl(String url) async {
    api.baseUrl = url.trim();
    await _prefs.setString('api_url', api.baseUrl);
    notifyListeners();
  }

  Future<void> login(String token, AppUser u) async {
    api.token = token;
    user = u;
    await _prefs.setString('token', token);
    await _prefs.setString('user', jsonEncode(u.toJson()));
    notifyListeners();
    await sync.syncNow();
  }

  Future<void> logout() async {
    api.token = null;
    user = null;
    await _prefs.remove('token');
    await _prefs.remove('user');
    await store.clearCache();
    notifyListeners();
  }
}

late final AppState app;
