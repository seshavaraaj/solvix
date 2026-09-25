const statuses = ['reported', 'verified', 'rejected', 'approved', 'paid'];
const assetTypes = ['house', 'hut', 'cattle', 'crop', 'boat', 'shop', 'other'];
const damageTypes = ['fully_damaged', 'partially_damaged', 'washed_away', 'submerged', 'dead', 'other'];

DateTime? _date(dynamic v) => v == null ? null : DateTime.parse(v as String).toLocal();

class AppUser {
  final int id;
  final String role;
  final String? name;
  final String? phone;
  final String? district;
  final String? taluk;

  AppUser({required this.id, required this.role, this.name, this.phone, this.district, this.taluk});

  factory AppUser.fromJson(Map<String, dynamic> j) => AppUser(
        id: j['id'] as int,
        role: j['role'] as String,
        name: j['name'] as String?,
        phone: j['phone'] as String?,
        district: j['district'] as String?,
        taluk: j['taluk'] as String?,
      );

  Map<String, dynamic> toJson() =>
      {'id': id, 'role': role, 'name': name, 'phone': phone, 'district': district, 'taluk': taluk};

  bool get isStaff => role == 'staff' || role == 'admin';
}

class Flag {
  final String code;
  final String message;
  final int? distanceM;

  Flag(this.code, this.message, this.distanceM);

  factory Flag.fromJson(Map<String, dynamic> j) =>
      Flag(j['code'] as String, j['message'] as String? ?? '', (j['distance_m'] as num?)?.toInt());
}

class HistoryItem {
  final String toStatus;
  final String? actorName;
  final String? actorRole;
  final String? note;
  final DateTime createdAt;

  HistoryItem(this.toStatus, this.actorName, this.actorRole, this.note, this.createdAt);

  factory HistoryItem.fromJson(Map<String, dynamic> j) => HistoryItem(
        j['to_status'] as String,
        j['actor_name'] as String?,
        j['actor_role'] as String?,
        j['note'] as String?,
        _date(j['created_at'])!,
      );
}

class Report {
  final String id;
  final String assetType;
  final String damageType;
  final int? severity;
  final String? description;
  final double lat;
  final double lon;
  final String? district;
  final String? taluk;
  final String? village;
  final String? reporterName;
  final String? photoUrl;
  final bool? inFloodExtent;
  final int confidence;
  final List<Flag> flags;
  final String status;
  final DateTime statusChangedAt;
  final DateTime createdAt;
  final String? paymentRef;
  final List<HistoryItem> history;
  final int grievanceCount;

  Report({
    required this.id,
    required this.assetType,
    required this.damageType,
    this.severity,
    this.description,
    required this.lat,
    required this.lon,
    this.district,
    this.taluk,
    this.village,
    this.reporterName,
    this.photoUrl,
    this.inFloodExtent,
    required this.confidence,
    required this.flags,
    required this.status,
    required this.statusChangedAt,
    required this.createdAt,
    this.paymentRef,
    this.history = const [],
    this.grievanceCount = 0,
  });

  factory Report.fromJson(Map<String, dynamic> j) => Report(
        id: j['id'] as String,
        assetType: j['asset_type'] as String,
        damageType: j['damage_type'] as String,
        severity: (j['severity_hint'] as num?)?.toInt(),
        description: j['description'] as String?,
        lat: (j['lat'] as num).toDouble(),
        lon: (j['lon'] as num).toDouble(),
        district: j['district'] as String?,
        taluk: j['taluk'] as String?,
        village: j['village'] as String?,
        reporterName: j['reporter_name'] as String?,
        photoUrl: j['photo_url'] as String?,
        inFloodExtent: j['in_flood_extent'] as bool?,
        confidence: (j['confidence'] as num).toInt(),
        flags: ((j['flags'] as List?) ?? []).map((f) => Flag.fromJson(f as Map<String, dynamic>)).toList(),
        status: j['status'] as String,
        statusChangedAt: _date(j['status_changed_at'])!,
        createdAt: _date(j['created_at'])!,
        paymentRef: j['payment_ref'] as String?,
        history: ((j['history'] as List?) ?? [])
            .map((h) => HistoryItem.fromJson(h as Map<String, dynamic>))
            .toList(),
        grievanceCount: ((j['grievances'] as List?) ?? []).length,
      );

  String get place => [village, taluk, district].whereType<String>().where((s) => s.isNotEmpty).join(', ');
}

/// A report saved on the phone that has not fully reached the server yet.
class PendingReport {
  final String id;
  final Map<String, dynamic> payload;
  final String? photoPath;
  final bool created;
  final int attempts;
  final String? lastError;
  final DateTime createdAt;

  PendingReport({
    required this.id,
    required this.payload,
    this.photoPath,
    this.created = false,
    this.attempts = 0,
    this.lastError,
    required this.createdAt,
  });
}
