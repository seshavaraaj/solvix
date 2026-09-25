import 'package:flutter/material.dart';

import '../app_state.dart';
import '../models.dart';

const statusColors = {
  'reported': Color(0xFFB87A04),
  'verified': Color(0xFF2563EB),
  'rejected': Color(0xFFC0392B),
  'approved': Color(0xFF15803D),
  'paid': Color(0xFF7C3AED),
};

String fmtDate(DateTime d) {
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  final h = d.hour.toString().padLeft(2, '0');
  final m = d.minute.toString().padLeft(2, '0');
  return '${d.day} ${months[d.month - 1]}, $h:$m';
}

class StatusChip extends StatelessWidget {
  final String status;
  const StatusChip(this.status, {super.key});

  @override
  Widget build(BuildContext context) {
    final c = statusColors[status] ?? Colors.grey;
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 3),
      decoration: BoxDecoration(color: c.withValues(alpha: 0.12), borderRadius: BorderRadius.circular(99)),
      child: Row(mainAxisSize: MainAxisSize.min, children: [
        Container(width: 8, height: 8, decoration: BoxDecoration(color: c, shape: BoxShape.circle)),
        const SizedBox(width: 6),
        Flexible(
          child: Text(app.t('status.$status'),
              style: TextStyle(color: c, fontWeight: FontWeight.w600, fontSize: 12), overflow: TextOverflow.ellipsis),
        ),
      ]),
    );
  }
}

class PendingChip extends StatelessWidget {
  final PendingReport item;
  const PendingChip(this.item, {super.key});

  @override
  Widget build(BuildContext context) {
    final failed = item.lastError != null;
    final c = failed ? const Color(0xFFB45309) : const Color(0xFF5F6D73);
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 3),
      decoration: BoxDecoration(color: c.withValues(alpha: 0.12), borderRadius: BorderRadius.circular(99)),
      child: Row(mainAxisSize: MainAxisSize.min, children: [
        Icon(failed ? Icons.sync_problem : Icons.cloud_upload_outlined, size: 14, color: c),
        const SizedBox(width: 6),
        Text(app.t(failed ? 'syncFailed' : 'waitingSync'),
            style: TextStyle(color: c, fontWeight: FontWeight.w600, fontSize: 12)),
      ]),
    );
  }
}

class FlagChips extends StatelessWidget {
  final List<Flag> flags;
  const FlagChips(this.flags, {super.key});

  @override
  Widget build(BuildContext context) {
    if (flags.isEmpty) {
      return Row(children: [
        const Icon(Icons.check_circle, size: 16, color: Color(0xFF15803D)),
        const SizedBox(width: 6),
        Text(app.t('noFlags'), style: const TextStyle(color: Color(0xFF15803D))),
      ]);
    }
    return Wrap(
      spacing: 6,
      runSpacing: 6,
      children: [
        for (final f in flags)
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
            decoration: BoxDecoration(color: const Color(0xFFFDECEA), borderRadius: BorderRadius.circular(6)),
            child: Text(
              app.t('flag.${f.code}') + (f.distanceM != null ? ' · ${f.distanceM} m' : ''),
              style: const TextStyle(color: Color(0xFF8E2A1F), fontSize: 12),
            ),
          ),
      ],
    );
  }
}

class ConfidenceBadge extends StatelessWidget {
  final int value;
  const ConfidenceBadge(this.value, {super.key});

  @override
  Widget build(BuildContext context) {
    final (bg, fg) = value >= 80
        ? (const Color(0xFFE5F4EA), const Color(0xFF15803D))
        : value >= 50
            ? (const Color(0xFFFDF1E0), const Color(0xFFB45309))
            : (const Color(0xFFFDECEA), const Color(0xFFC0392B));
    return Container(
      width: 44,
      padding: const EdgeInsets.symmetric(vertical: 4),
      decoration: BoxDecoration(color: bg, borderRadius: BorderRadius.circular(8)),
      child: Text('$value', textAlign: TextAlign.center, style: TextStyle(color: fg, fontWeight: FontWeight.w700)),
    );
  }
}

class Timeline extends StatelessWidget {
  final List<HistoryItem> history;
  const Timeline(this.history, {super.key});

  @override
  Widget build(BuildContext context) {
    final muted = Theme.of(context).colorScheme.onSurfaceVariant;
    return Column(children: [
      for (var i = 0; i < history.length; i++)
        IntrinsicHeight(
          child: Row(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
            SizedBox(
              width: 24,
              child: Column(children: [
                Container(
                  margin: const EdgeInsets.only(top: 4),
                  width: 12,
                  height: 12,
                  decoration: BoxDecoration(
                      color: statusColors[history[i].toStatus] ?? Colors.grey, shape: BoxShape.circle),
                ),
                if (i < history.length - 1) Expanded(child: Container(width: 2, color: Colors.black12)),
              ]),
            ),
            Expanded(
              child: Padding(
                padding: const EdgeInsets.only(bottom: 16, left: 6),
                child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Text(app.t('status.${history[i].toStatus}'), style: const TextStyle(fontWeight: FontWeight.w700)),
                  Text(
                    '${fmtDate(history[i].createdAt)}'
                    '${history[i].actorName != null ? ' · ${app.t('by')} ${history[i].actorName}' : ''}',
                    style: TextStyle(color: muted, fontSize: 12),
                  ),
                  if (history[i].note != null && history[i].note!.isNotEmpty)
                    Padding(
                      padding: const EdgeInsets.only(top: 4),
                      child: Text(history[i].note!),
                    ),
                ]),
              ),
            ),
          ]),
        ),
    ]);
  }
}

class ErrorView extends StatelessWidget {
  final Object error;
  final VoidCallback onRetry;
  const ErrorView(this.error, this.onRetry, {super.key});

  @override
  Widget build(BuildContext context) => Center(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(mainAxisSize: MainAxisSize.min, children: [
            const Icon(Icons.cloud_off, size: 40),
            const SizedBox(height: 8),
            Text('$error', textAlign: TextAlign.center),
            const SizedBox(height: 12),
            OutlinedButton(onPressed: onRetry, child: Text(app.t('retry'))),
          ]),
        ),
      );
}

void toast(BuildContext context, String msg) =>
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(msg)));
