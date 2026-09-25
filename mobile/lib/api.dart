import 'dart:async';
import 'dart:convert';
import 'dart:io';

import 'package:http/http.dart' as http;

import 'models.dart';

class ApiException implements Exception {
  final int status;
  final String message;
  ApiException(this.status, this.message);

  /// True when retrying later can help (no network, timeout, server error).
  bool get retryable => status == 0 || status >= 500 || status == 408 || status == 429;

  @override
  String toString() => message;
}

class Api {
  String baseUrl;
  String? token;
  void Function()? onUnauthorized;

  Api(this.baseUrl);

  static const _timeout = Duration(seconds: 40);

  Uri _uri(String path, [Map<String, String>? query]) =>
      Uri.parse('${baseUrl.replaceAll(RegExp(r'/+$'), '')}$path').replace(queryParameters: query);

  String photoUrl(String path) => '${baseUrl.replaceAll(RegExp(r'/+$'), '')}$path';

  Map<String, String> get _headers => {
        'Content-Type': 'application/json',
        if (token != null) 'Authorization': 'Bearer $token',
      };

  Future<dynamic> _send(Future<http.Response> Function() call) async {
    http.Response res;
    try {
      res = await call().timeout(_timeout);
    } on TimeoutException {
      throw ApiException(0, 'Server did not answer in time');
    } on SocketException {
      throw ApiException(0, 'No connection to server');
    } on http.ClientException catch (e) {
      throw ApiException(0, e.message);
    }
    if (res.statusCode == 401 && token != null) onUnauthorized?.call();
    final body = utf8.decode(res.bodyBytes);
    if (res.statusCode >= 400) {
      String msg = 'Error ${res.statusCode}';
      try {
        final d = jsonDecode(body)['detail'];
        msg = d is String ? d : jsonEncode(d);
      } catch (_) {}
      throw ApiException(res.statusCode, msg);
    }
    return body.isEmpty ? null : jsonDecode(body);
  }

  Future<dynamic> get(String path, [Map<String, String>? query]) =>
      _send(() => http.get(_uri(path, query), headers: _headers));

  Future<dynamic> post(String path, [Object? body]) =>
      _send(() => http.post(_uri(path), headers: _headers, body: jsonEncode(body ?? {})));

  // ---- auth ----
  Future<void> requestOtp(String phone) => post('/auth/otp', {'phone': phone});

  Future<(String, AppUser)> verifyOtp(String phone, String code, String? name) async {
    final j = await post('/auth/verify', {'phone': phone, 'code': code, if (name != null) 'name': name});
    return (j['access_token'] as String, AppUser.fromJson(j['user'] as Map<String, dynamic>));
  }

  // ---- reports ----
  Future<Map<String, dynamic>> createReport(Map<String, dynamic> payload) async =>
      (await post('/reports', payload)) as Map<String, dynamic>;

  Future<void> uploadPhoto(String reportId, String filePath) => _send(() async {
        final req = http.MultipartRequest('POST', _uri('/reports/$reportId/photo'));
        if (token != null) req.headers['Authorization'] = 'Bearer $token';
        req.files.add(await http.MultipartFile.fromPath('file', filePath));
        return http.Response.fromStream(await req.send());
      });

  Future<List<dynamic>> myReportsRaw() async => (await get('/me/reports')) as List<dynamic>;

  Future<List<dynamic>> queueRaw() async =>
      (await get('/reports', {'status': 'reported', 'sort': 'confidence', 'limit': '200'})) as List<dynamic>;

  Future<Report> report(String id) async => Report.fromJson((await get('/reports/$id')) as Map<String, dynamic>);

  Future<Report> verify(String id, String decision, String? note) async => Report.fromJson(
      (await post('/reports/$id/verify', {'decision': decision, 'note': note})) as Map<String, dynamic>);

  Future<void> grievance(String id, String text) => post('/reports/$id/grievance', {'text': text});
}
