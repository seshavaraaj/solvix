import 'dart:convert';

import 'package:path/path.dart' as p;
import 'package:sqflite/sqflite.dart';

import 'models.dart';

/// On-phone SQLite: the offline report queue plus a small read cache.
class LocalStore {
  late Database _db;

  Future<void> open() async {
    _db = await openDatabase(
      p.join(await getDatabasesPath(), 'meetpu.db'),
      version: 1,
      onCreate: (db, _) async {
        await db.execute('''
          CREATE TABLE pending_reports (
            id TEXT PRIMARY KEY,
            payload TEXT NOT NULL,
            photo_path TEXT,
            created INTEGER NOT NULL DEFAULT 0,
            attempts INTEGER NOT NULL DEFAULT 0,
            next_attempt_at INTEGER NOT NULL DEFAULT 0,
            last_error TEXT,
            created_at INTEGER NOT NULL
          )''');
        await db.execute('CREATE TABLE cache (key TEXT PRIMARY KEY, value TEXT NOT NULL)');
      },
    );
  }

  // ---- pending queue ----

  Future<void> enqueue(String id, Map<String, dynamic> payload, String? photoPath) => _db.insert(
        'pending_reports',
        {
          'id': id,
          'payload': jsonEncode(payload),
          'photo_path': photoPath,
          'created_at': DateTime.now().millisecondsSinceEpoch,
        },
        conflictAlgorithm: ConflictAlgorithm.ignore,
      );

  PendingReport _row(Map<String, Object?> r) => PendingReport(
        id: r['id'] as String,
        payload: jsonDecode(r['payload'] as String) as Map<String, dynamic>,
        photoPath: r['photo_path'] as String?,
        created: (r['created'] as int) == 1,
        attempts: r['attempts'] as int,
        lastError: r['last_error'] as String?,
        createdAt: DateTime.fromMillisecondsSinceEpoch(r['created_at'] as int),
      );

  Future<List<PendingReport>> pending() async =>
      (await _db.query('pending_reports', orderBy: 'created_at DESC')).map(_row).toList();

  Future<List<PendingReport>> due() async => (await _db.query(
        'pending_reports',
        where: 'next_attempt_at <= ?',
        whereArgs: [DateTime.now().millisecondsSinceEpoch],
        orderBy: 'created_at ASC',
      ))
          .map(_row)
          .toList();

  Future<void> markCreated(String id) =>
      _db.update('pending_reports', {'created': 1}, where: 'id = ?', whereArgs: [id]);

  Future<void> markFailed(String id, int attempts, String error, Duration retryIn) => _db.update(
        'pending_reports',
        {
          'attempts': attempts,
          'last_error': error,
          'next_attempt_at': DateTime.now().add(retryIn).millisecondsSinceEpoch,
        },
        where: 'id = ?',
        whereArgs: [id],
      );

  Future<void> resetBackoff() => _db.update('pending_reports', {'next_attempt_at': 0});

  Future<void> remove(String id) => _db.delete('pending_reports', where: 'id = ?', whereArgs: [id]);

  // ---- read cache ----

  Future<void> putCache(String key, Object value) => _db.insert(
        'cache',
        {'key': key, 'value': jsonEncode(value)},
        conflictAlgorithm: ConflictAlgorithm.replace,
      );

  Future<dynamic> getCache(String key) async {
    final rows = await _db.query('cache', where: 'key = ?', whereArgs: [key]);
    return rows.isEmpty ? null : jsonDecode(rows.first['value'] as String);
  }

  Future<void> clearCache() => _db.delete('cache');
}
