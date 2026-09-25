import 'package:flutter/material.dart';

import '../api.dart';
import '../app_state.dart';
import '../models.dart';
import '../widgets/common.dart';
import 'report_detail.dart';
import 'report_form.dart';

/// Citizen: own reports (server copy plus items still on the phone) and the report button.
class CitizenHome extends StatefulWidget {
  const CitizenHome({super.key});

  @override
  State<CitizenHome> createState() => _CitizenHomeState();
}

class _CitizenHomeState extends State<CitizenHome> {
  List<Report> _reports = [];
  bool _fromCache = false;
  bool _loading = true;
  Object? _error;

  @override
  void initState() {
    super.initState();
    app.sync.addListener(_onSync);
    _load();
  }

  @override
  void dispose() {
    app.sync.removeListener(_onSync);
    super.dispose();
  }

  int _lastPending = -1;
  void _onSync() {
    // Reload server list when an item leaves the queue.
    if (app.sync.pending.length < _lastPending) _load();
    _lastPending = app.sync.pending.length;
    if (mounted) setState(() {});
  }

  Future<void> _load() async {
    setState(() => _loading = true);
    try {
      final raw = await app.api.myReportsRaw();
      await app.store.putCache('my_reports', raw);
      _reports = raw.map((j) => Report.fromJson(j as Map<String, dynamic>)).toList();
      _fromCache = false;
      _error = null;
    } on ApiException catch (e) {
      final cached = await app.store.getCache('my_reports');
      if (cached != null) {
        _reports = (cached as List).map((j) => Report.fromJson(j as Map<String, dynamic>)).toList();
        _fromCache = true;
      } else {
        _error = e;
      }
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final pending = app.sync.pending;
    final serverIds = _reports.map((r) => r.id).toSet();
    final localOnly = pending.where((p) => !serverIds.contains(p.id)).toList();
    final muted = Theme.of(context).colorScheme.onSurfaceVariant;

    return Scaffold(
      appBar: AppBar(
        title: Text(app.t('myReports')),
        actions: [
          TextButton(onPressed: app.toggleLang, child: Text(app.t('language'))),
          IconButton(onPressed: app.logout, icon: const Icon(Icons.logout), tooltip: app.t('logout')),
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () async {
          await Navigator.push(context, MaterialPageRoute(builder: (_) => const ReportFormScreen()));
          if (mounted) setState(() {});
        },
        icon: const Icon(Icons.add_a_photo),
        label: Text(app.t('reportDamage')),
      ),
      body: RefreshIndicator(
        onRefresh: () async {
          await app.sync.retryAll();
          await _load();
        },
        child: ListView(
          padding: const EdgeInsets.fromLTRB(16, 8, 16, 96),
          children: [
            if (!app.sync.online || _fromCache)
              Card(
                color: const Color(0xFFFFF3D6),
                child: Padding(
                  padding: const EdgeInsets.all(12),
                  child: Text(app.sync.online ? app.t('lastUpdated') : app.t('offline')),
                ),
              ),
            if (_loading && _reports.isEmpty) const Padding(padding: EdgeInsets.all(24), child: Center(child: CircularProgressIndicator())),
            if (_error != null && _reports.isEmpty && localOnly.isEmpty) ErrorView(_error!, _load),
            for (final p in localOnly)
              Card(
                child: ListTile(
                  leading: const Icon(Icons.phone_android),
                  title: Text(
                      '${app.t('asset.${p.payload['asset_type']}')} · ${app.t('damage.${p.payload['damage_type']}')}'),
                  subtitle: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                    Text(fmtDate(p.createdAt), style: TextStyle(color: muted, fontSize: 12)),
                    const SizedBox(height: 6),
                    PendingChip(p),
                    if (p.lastError != null)
                      Text(p.lastError!, style: TextStyle(color: muted, fontSize: 11)),
                  ]),
                  trailing: IconButton(
                    icon: const Icon(Icons.sync),
                    tooltip: app.t('syncNow'),
                    onPressed: app.sync.running ? null : app.sync.retryAll,
                  ),
                ),
              ),
            for (final r in _reports)
              Card(
                child: ListTile(
                  title: Text('${app.t('asset.${r.assetType}')} · ${app.t('damage.${r.damageType}')}'),
                  subtitle: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                    if (r.place.isNotEmpty) Text(r.place),
                    Text(fmtDate(r.createdAt), style: TextStyle(color: muted, fontSize: 12)),
                    const SizedBox(height: 6),
                    StatusChip(r.status),
                  ]),
                  trailing: const Icon(Icons.chevron_right),
                  onTap: () async {
                    await Navigator.push(
                        context, MaterialPageRoute(builder: (_) => ReportDetailScreen(reportId: r.id, initial: r)));
                    _load();
                  },
                ),
              ),
            if (!_loading && _error == null && _reports.isEmpty && localOnly.isEmpty)
              Padding(
                padding: const EdgeInsets.all(32),
                child: Text(app.t('noReports'), textAlign: TextAlign.center, style: TextStyle(color: muted)),
              ),
          ],
        ),
      ),
    );
  }
}
