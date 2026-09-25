import 'package:flutter/material.dart';

import '../api.dart';
import '../app_state.dart';
import '../models.dart';
import '../widgets/common.dart';

/// Citizen view of one report: photo, status timeline, grievance.
class ReportDetailScreen extends StatefulWidget {
  final String reportId;
  final Report? initial;
  const ReportDetailScreen({super.key, required this.reportId, this.initial});

  @override
  State<ReportDetailScreen> createState() => _ReportDetailScreenState();
}

class _ReportDetailScreenState extends State<ReportDetailScreen> {
  late Report? _r = widget.initial;
  Object? _error;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    try {
      final r = await app.api.report(widget.reportId);
      setState(() {
        _r = r;
        _error = null;
      });
    } on ApiException catch (e) {
      setState(() => _error = e);
    }
  }

  Future<void> _grievance() async {
    final ctl = TextEditingController();
    final text = await showDialog<String>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: Text(app.t('grievance')),
        content: TextField(
          controller: ctl,
          maxLines: 4,
          autofocus: true,
          decoration: InputDecoration(hintText: app.t('grievanceHint')),
        ),
        actions: [
          TextButton(onPressed: () => Navigator.pop(ctx), child: Text(app.t('cancel'))),
          FilledButton(onPressed: () => Navigator.pop(ctx, ctl.text.trim()), child: Text(app.t('send'))),
        ],
      ),
    );
    if (text == null || text.length < 3) return;
    try {
      await app.api.grievance(widget.reportId, text);
      if (!mounted) return;
      toast(context, app.t('grievanceSent'));
      _load();
    } on ApiException catch (e) {
      if (mounted) toast(context, e.status == 0 ? app.t('needOnline') : e.message);
    }
  }

  @override
  Widget build(BuildContext context) {
    final r = _r;
    final muted = Theme.of(context).colorScheme.onSurfaceVariant;
    return Scaffold(
      appBar: AppBar(title: Text(r == null ? '' : app.t('asset.${r.assetType}'))),
      body: r == null
          ? (_error != null ? ErrorView(_error!, _load) : const Center(child: CircularProgressIndicator()))
          : RefreshIndicator(
              onRefresh: _load,
              child: ListView(
                padding: const EdgeInsets.all(16),
                children: [
                  if (r.photoUrl != null)
                    ClipRRect(
                      borderRadius: BorderRadius.circular(10),
                      child: Image.network(app.api.photoUrl(r.photoUrl!),
                          height: 220,
                          fit: BoxFit.cover,
                          errorBuilder: (_, __, ___) => const SizedBox(height: 60, child: Icon(Icons.image_not_supported))),
                    ),
                  const SizedBox(height: 12),
                  Text('${app.t('asset.${r.assetType}')} · ${app.t('damage.${r.damageType}')}',
                      style: Theme.of(context).textTheme.titleLarge),
                  if (r.place.isNotEmpty) Text(r.place, style: TextStyle(color: muted)),
                  const SizedBox(height: 8),
                  Align(alignment: Alignment.centerLeft, child: StatusChip(r.status)),
                  if (r.paymentRef != null)
                    Padding(
                      padding: const EdgeInsets.only(top: 8),
                      child: Text('${app.t('paymentRef')}: ${r.paymentRef}'),
                    ),
                  const SizedBox(height: 24),
                  Text(app.t('timeline'), style: const TextStyle(fontWeight: FontWeight.w700, fontSize: 16)),
                  const SizedBox(height: 12),
                  Timeline(r.history),
                  if (r.grievanceCount > 0)
                    Text('${r.grievanceCount} ${app.t('grievances')}', style: TextStyle(color: muted)),
                  const SizedBox(height: 16),
                  OutlinedButton.icon(
                    onPressed: _grievance,
                    icon: const Icon(Icons.report_outlined),
                    label: Text(app.t('grievance')),
                  ),
                ],
              ),
            ),
    );
  }
}
