import 'package:flutter/material.dart';

import '../api.dart';
import '../app_state.dart';
import '../models.dart';
import '../widgets/common.dart';

/// Staff: check one report on site, then confirm or reject it.
class StaffVerifyScreen extends StatefulWidget {
  final Report report;
  const StaffVerifyScreen({super.key, required this.report});

  @override
  State<StaffVerifyScreen> createState() => _StaffVerifyScreenState();
}

class _StaffVerifyScreenState extends State<StaffVerifyScreen> {
  final _note = TextEditingController();
  bool _busy = false;
  String? _error;

  Future<void> _decide(String decision) async {
    if (decision == 'rejected' && _note.text.trim().isEmpty) {
      setState(() => _error = app.t('noteRequired'));
      return;
    }
    setState(() {
      _busy = true;
      _error = null;
    });
    try {
      await app.api.verify(widget.report.id, decision, _note.text.trim().isEmpty ? null : _note.text.trim());
      if (!mounted) return;
      toast(context, app.t('decisionSaved'));
      Navigator.pop(context, true);
    } on ApiException catch (e) {
      setState(() => _error = e.status == 0 ? app.t('needOnline') : e.message);
    } finally {
      if (mounted) setState(() => _busy = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final r = widget.report;
    final scheme = Theme.of(context).colorScheme;
    final muted = scheme.onSurfaceVariant;
    final flood = r.inFloodExtent == null
        ? app.t('noFloodLayer')
        : r.inFloodExtent!
            ? app.t('inFlood')
            : app.t('outFlood');

    return Scaffold(
      appBar: AppBar(title: Text('${app.t('asset.${r.assetType}')} · ${app.t('damage.${r.damageType}')}')),
      body: SafeArea(
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            if (r.photoUrl != null)
              ClipRRect(
                borderRadius: BorderRadius.circular(10),
                child: Image.network(app.api.photoUrl(r.photoUrl!),
                    height: 240,
                    fit: BoxFit.cover,
                    errorBuilder: (_, __, ___) => const SizedBox(height: 60, child: Icon(Icons.image_not_supported))),
              ),
            const SizedBox(height: 12),
            if (r.place.isNotEmpty) Text(r.place, style: Theme.of(context).textTheme.titleMedium),
            Text('${app.t('reporter')}: ${r.reporterName ?? '—'} · ${fmtDate(r.createdAt)}',
                style: TextStyle(color: muted)),
            if (r.description != null) Padding(padding: const EdgeInsets.only(top: 8), child: Text(r.description!)),
            const SizedBox(height: 16),
            Row(children: [
              ConfidenceBadge(r.confidence),
              const SizedBox(width: 8),
              Text(app.t('confidence'), style: TextStyle(color: muted)),
            ]),
            const SizedBox(height: 10),
            Text(app.t('flags'), style: const TextStyle(fontWeight: FontWeight.w700)),
            const SizedBox(height: 6),
            FlagChips(r.flags),
            const SizedBox(height: 12),
            Row(children: [
              Icon(Icons.water, size: 18, color: r.inFloodExtent == true ? const Color(0xFF1D6FB8) : muted),
              const SizedBox(width: 6),
              Text(flood),
            ]),
            const SizedBox(height: 6),
            Text('${app.t('reportedLoc')}: ${r.lat.toStringAsFixed(5)}, ${r.lon.toStringAsFixed(5)}',
                style: TextStyle(color: muted, fontSize: 13)),
            const SizedBox(height: 20),
            TextField(controller: _note, maxLines: 3, decoration: InputDecoration(labelText: app.t('note'))),
            if (_error != null)
              Padding(padding: const EdgeInsets.only(top: 8), child: Text(_error!, style: TextStyle(color: scheme.error))),
            const SizedBox(height: 16),
            Row(children: [
              Expanded(
                child: OutlinedButton(
                  onPressed: _busy ? null : () => _decide('rejected'),
                  style: OutlinedButton.styleFrom(
                    foregroundColor: scheme.error,
                    minimumSize: const Size.fromHeight(50),
                  ),
                  child: Text(app.t('rejectReport')),
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: FilledButton(
                  onPressed: _busy ? null : () => _decide('verified'),
                  style: FilledButton.styleFrom(minimumSize: const Size.fromHeight(50)),
                  child: Text(app.t('confirmDamage')),
                ),
              ),
            ]),
          ],
        ),
      ),
    );
  }
}
