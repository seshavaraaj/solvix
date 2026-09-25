import 'dart:async';
import 'dart:io';
import 'dart:math';

import 'package:connectivity_plus/connectivity_plus.dart';
import 'package:flutter/foundation.dart';

import 'api.dart';
import 'local_store.dart';
import 'models.dart';

/// Pushes queued reports to the server. The report UUID is the server's
/// idempotency key, so sending the same report twice creates one record.
class SyncService extends ChangeNotifier {
  final Api api;
  final LocalStore store;

  SyncService(this.api, this.store);

  List<PendingReport> pending = [];
  bool running = false;
  bool online = true;
  StreamSubscription<List<ConnectivityResult>>? _sub;
  Timer? _timer;

  Future<void> start() async {
    await refresh();
    _sub = Connectivity().onConnectivityChanged.listen((results) {
      final nowOnline = results.any((r) => r != ConnectivityResult.none);
      if (nowOnline && !online) {
        // Network came back: skip the backoff wait and try at once.
        store.resetBackoff().then((_) => syncNow());
      }
      online = nowOnline;
      notifyListeners();
    });
    _timer = Timer.periodic(const Duration(seconds: 30), (_) => syncNow());
    unawaited(syncNow());
  }

  Future<void> refresh() async {
    pending = await store.pending();
    notifyListeners();
  }

  Future<void> add(String id, Map<String, dynamic> payload, String? photoPath) async {
    await store.enqueue(id, payload, photoPath);
    await refresh();
    unawaited(syncNow());
  }

  Future<void> retryAll() async {
    await store.resetBackoff();
    await syncNow();
  }

  Future<void> syncNow() async {
    if (running || api.token == null) return;
    running = true;
    notifyListeners();
    try {
      for (final item in await store.due()) {
        try {
          if (!item.created) {
            await api.createReport(item.payload);
            await store.markCreated(item.id);
          }
          if (item.photoPath != null && File(item.photoPath!).existsSync()) {
            await api.uploadPhoto(item.id, item.photoPath!);
          }
          await store.remove(item.id);
          if (item.photoPath != null) {
            // The photo now lives on the server; free space on the phone.
            try {
              File(item.photoPath!).deleteSync();
            } catch (_) {}
          }
        } on ApiException catch (e) {
          final attempts = item.attempts + 1;
          // Backoff: 15 s, 30 s, 1 min, 2 min ... capped at 10 min.
          final wait = Duration(seconds: min(600, 15 * pow(2, attempts - 1).toInt()));
          await store.markFailed(item.id, attempts, e.message, e.retryable ? wait : const Duration(hours: 1));
          if (e.status == 0) break; // offline: stop this round
        }
      }
    } finally {
      running = false;
      await refresh();
    }
  }

  @override
  void dispose() {
    _sub?.cancel();
    _timer?.cancel();
    super.dispose();
  }
}
