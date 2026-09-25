import 'package:flutter/material.dart';

import '../api.dart';
import '../app_state.dart';
import '../models.dart';
import '../widgets/common.dart';
import 'report_form.dart';
import 'staff_verify.dart';

/// Staff: reports waiting for a site visit, lowest confidence first.
class StaffHome extends StatefulWidget {
  const StaffHome({super.key});

  @override
  State<StaffHome> createState() => _StaffHomeState();
}

class _StaffHomeState extends State<StaffHome> {
  List<Report> _queue = [];
  bool _fromCache = false;
  bool _loading = true;
  Object? _error;

  @override
  void initState() {
    super.initState();
    app.sync.addListener(_rebuild);
    _load();
  }

  @override
  void dispose() {
    app.sync.removeListener(_rebuild);
    super.dispose();
  }

  void _rebuild() {
    if (mounted) setState(() {});
  }

  Future<void> _load() async {
    setState(() => _loading = true);
    try {
      final raw = await app.api.queueRaw();
      await app.store.putCache('staff_queue', raw);
      _queue = raw.map((j) => Report.fromJson(j as Map<String, dynamic>)).toList();
      _fromCache = false;
      _error = null;
    } on ApiException catch (e) {
      final cached = await app.store.getCache('staff_queue');
      if (cached != null) {
        _queue = (cached as List).map((j) => Report.fromJson(j as Map<String, dynamic>)).toList();
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
    final muted = Theme.of(context).colorScheme.onSurfaceVariant;
    final pending = app.sync.pending;
    return Scaffold(
      appBar: AppBar(
        title: Text(app.t('queue')),
        actions: [
          TextButton(onPressed: app.toggleLang, child: Text(app.t('language'))),
          IconButton(onPressed: app.logout, icon: const Icon(Icons.logout), tooltip: app.t('logout')),
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () async {
          await Navigator.push(context, MaterialPageRoute(builder: (_) => const ReportFormScreen()));
          _load();
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
            if (app.user?.name != null)
              Padding(
                padding: const EdgeInsets.only(bottom: 8),
                child: Text('${app.user!.name}', style: TextStyle(color: muted)),
              ),
            if (!app.sync.online || _fromCache)
              Card(
                color: const Color(0xFFFFF3D6),
                child: Padding(
                  padding: const EdgeInsets.all(12),
                  child: Text(app.sync.online ? app.t('lastUpdated') : app.t('offline')),
                ),
              ),
            if (pending.isNotEmpty)
              Card(
                child: ListTile(
                  leading: const Icon(Icons.cloud_upload_outlined),
                  title: Text('${pending.length} × ${app.t('waitingSync')}'),
                  trailing: TextButton(
                    onPressed: app.sync.running ? null : app.sync.retryAll,
                    child: Text(app.t('syncNow')),
                  ),
                ),
              ),
            if (_loading && _queue.isEmpty)
              const Padding(padding: EdgeInsets.all(24), child: Center(child: CircularProgressIndicator())),
            if (_error != null && _queue.isEmpty) ErrorView(_error!, _load),
            if (!_loading && _error == null && _queue.isEmpty)
              Padding(
                padding: const EdgeInsets.all(32),
                child: Text(app.t('queueEmpty'), textAlign: TextAlign.center, style: TextStyle(color: muted)),
              ),
            for (final r in _queue)
              Card(
                child: InkWell(
                  borderRadius: BorderRadius.circular(12),
                  onTap: () async {
                    final changed = await Navigator.push<bool>(
                        context, MaterialPageRoute(builder: (_) => StaffVerifyScreen(report: r)));
                    if (changed == true) _load();
                  },
                  child: Padding(
                    padding: const EdgeInsets.all(12),
                    child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
                      ConfidenceBadge(r.confidence),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                          Text('${app.t('asset.${r.assetType}')} · ${app.t('damage.${r.damageType}')}',
                              style: const TextStyle(fontWeight: FontWeight.w600)),
                          if (r.place.isNotEmpty) Text(r.place, style: TextStyle(color: muted, fontSize: 13)),
                          Text(fmtDate(r.createdAt), style: TextStyle(color: muted, fontSize: 12)),
                          const SizedBox(height: 6),
                          FlagChips(r.flags),
                        ]),
                      ),
                      const Icon(Icons.chevron_right),
                    ]),
                  ),
                ),
              ),
          ],
        ),
      ),
    );
  }
}
