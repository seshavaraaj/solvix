import 'package:flutter_test/flutter_test.dart';
import 'package:meetpu/i18n.dart';
import 'package:meetpu/models.dart';

void main() {
  test('translate falls back to English, then to the key', () {
    expect(translate('ta', 'asset.house'), 'வீடு');
    expect(translate('en', 'asset.house'), 'House');
    expect(translate('ta', 'no.such.key'), 'no.such.key');
  });

  test('every status, asset and damage type has both languages', () {
    for (final k in [
      ...statuses.map((s) => 'status.$s'),
      ...assetTypes.map((a) => 'asset.$a'),
      ...damageTypes.map((d) => 'damage.$d'),
    ]) {
      expect(translate('en', k), isNot(k), reason: k);
      expect(translate('ta', k), isNot(translate('en', k)), reason: k);
    }
  });

  test('Report.fromJson reads the API shape', () {
    final r = Report.fromJson({
      'id': 'abc',
      'asset_type': 'hut',
      'damage_type': 'washed_away',
      'severity_hint': 4,
      'lat': 12.97,
      'lon': 80.21,
      'village': 'Velachery',
      'district': 'Chennai',
      'confidence': 60,
      'flags': [
        {'code': 'gps_mismatch', 'message': 'x', 'distance_m': 1200}
      ],
      'status': 'verified',
      'status_changed_at': '2026-09-25T10:00:00Z',
      'created_at': '2026-09-24T10:00:00Z',
      'history': [
        {'to_status': 'reported', 'actor_name': 'A', 'created_at': '2026-09-24T10:00:00Z'},
        {'to_status': 'verified', 'actor_name': 'VAO', 'note': 'ok', 'created_at': '2026-09-25T10:00:00Z'},
      ],
      'grievances': [],
    });
    expect(r.flags.single.distanceM, 1200);
    expect(r.history.map((h) => h.toStatus), ['reported', 'verified']);
    expect(r.place, 'Velachery, Chennai');
  });
}
