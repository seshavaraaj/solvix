import 'dart:io';

import 'package:flutter/material.dart';
import 'package:geolocator/geolocator.dart';
import 'package:image_picker/image_picker.dart';
import 'package:path/path.dart' as p;
import 'package:path_provider/path_provider.dart';
import 'package:uuid/uuid.dart';

import '../app_state.dart';
import '../models.dart';
import '../widgets/common.dart';

/// Capture a damage report. Saves to the phone first, then the sync service sends it.
class ReportFormScreen extends StatefulWidget {
  const ReportFormScreen({super.key});

  @override
  State<ReportFormScreen> createState() => _ReportFormScreenState();
}

class _ReportFormScreenState extends State<ReportFormScreen> {
  // One UUID per report, made on the phone. The server uses it to ignore duplicate sends.
  final String _id = const Uuid().v4();
  String _asset = 'house';
  String _damage = 'partially_damaged';
  double _severity = 3;
  final _desc = TextEditingController();
  final _village = TextEditingController();
  late final _taluk = TextEditingController(text: app.user?.taluk ?? '');
  late final _district = TextEditingController(text: app.user?.district ?? '');
  String? _photoPath;
  Position? _pos;
  bool _locating = false;
  String? _error;

  @override
  void initState() {
    super.initState();
    _locate();
  }

  Future<void> _locate() async {
    setState(() {
      _locating = true;
      _error = null;
    });
    try {
      if (!await Geolocator.isLocationServiceEnabled()) throw Exception(app.t('locationNeeded'));
      var perm = await Geolocator.checkPermission();
      if (perm == LocationPermission.denied) perm = await Geolocator.requestPermission();
      if (perm == LocationPermission.denied || perm == LocationPermission.deniedForever) {
        throw Exception(app.t('locationNeeded'));
      }
      final pos = await Geolocator.getCurrentPosition(
        locationSettings: const LocationSettings(accuracy: LocationAccuracy.high, timeLimit: Duration(seconds: 30)),
      );
      setState(() => _pos = pos);
    } catch (e) {
      // Fall back to the last known fix when a fresh one times out (common indoors).
      final last = await Geolocator.getLastKnownPosition();
      setState(() {
        _pos = last ?? _pos;
        if (_pos == null) _error = app.t('locationNeeded');
      });
    } finally {
      if (mounted) setState(() => _locating = false);
    }
  }

  Future<void> _takePhoto() async {
    // No maxWidth/imageQuality: resizing on the phone would strip the EXIF GPS the server checks.
    final shot = await ImagePicker().pickImage(source: ImageSource.camera);
    if (shot == null) return;
    // Copy out of the picker's cache so the file survives until sync.
    final dir = Directory(p.join((await getApplicationDocumentsDirectory()).path, 'photos'));
    await dir.create(recursive: true);
    final dest = p.join(dir.path, '$_id${p.extension(shot.path).isEmpty ? '.jpg' : p.extension(shot.path)}');
    await File(shot.path).copy(dest);
    setState(() => _photoPath = dest);
  }

  Future<void> _submit() async {
    if (_pos == null) {
      setState(() => _error = app.t('locationNeeded'));
      return;
    }
    if (_photoPath == null) {
      setState(() => _error = app.t('photoNeeded'));
      return;
    }
    String? clean(TextEditingController c) => c.text.trim().isEmpty ? null : c.text.trim();
    final payload = {
      'id': _id,
      'asset_type': _asset,
      'damage_type': _damage,
      'severity_hint': _severity.round(),
      'description': clean(_desc),
      'lat': _pos!.latitude,
      'lon': _pos!.longitude,
      'captured_at': DateTime.now().toUtc().toIso8601String(),
      'village': clean(_village),
      'taluk': clean(_taluk),
      'district': clean(_district),
    };
    await app.sync.add(_id, payload, _photoPath);
    if (!mounted) return;
    toast(context, app.t('saved'));
    Navigator.pop(context);
  }

  Widget _section(String title, Widget child) => Padding(
        padding: const EdgeInsets.only(bottom: 20),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Text(title, style: const TextStyle(fontWeight: FontWeight.w700, fontSize: 15)),
          const SizedBox(height: 8),
          child,
        ]),
      );

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    return Scaffold(
      appBar: AppBar(title: Text(app.t('reportDamage'))),
      body: SafeArea(
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            _section(
              app.t('photo'),
              Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
                if (_photoPath != null)
                  ClipRRect(
                    borderRadius: BorderRadius.circular(10),
                    child: Image.file(File(_photoPath!), height: 220, fit: BoxFit.cover),
                  ),
                const SizedBox(height: 8),
                OutlinedButton.icon(
                  onPressed: _takePhoto,
                  icon: const Icon(Icons.photo_camera),
                  label: Text(app.t(_photoPath == null ? 'takePhoto' : 'retakePhoto')),
                ),
              ]),
            ),
            _section(
              app.t('location'),
              Row(children: [
                Icon(Icons.my_location, color: _pos != null ? const Color(0xFF15803D) : scheme.onSurfaceVariant),
                const SizedBox(width: 8),
                Expanded(
                  child: Text(_locating
                      ? app.t('locating')
                      : _pos == null
                          ? app.t('locationNeeded')
                          : '${_pos!.latitude.toStringAsFixed(5)}, ${_pos!.longitude.toStringAsFixed(5)}'
                              '  (${app.t('accuracy')} ${_pos!.accuracy.round()} m)'),
                ),
                IconButton(onPressed: _locating ? null : _locate, icon: const Icon(Icons.refresh)),
              ]),
            ),
            _section(
              app.t('asset'),
              Wrap(spacing: 8, runSpacing: 8, children: [
                for (final a in assetTypes)
                  ChoiceChip(label: Text(app.t('asset.$a')), selected: _asset == a, onSelected: (_) => setState(() => _asset = a)),
              ]),
            ),
            _section(
              app.t('damage'),
              Wrap(spacing: 8, runSpacing: 8, children: [
                for (final d in damageTypes)
                  ChoiceChip(label: Text(app.t('damage.$d')), selected: _damage == d, onSelected: (_) => setState(() => _damage = d)),
              ]),
            ),
            _section(
              '${app.t('severity')}: ${_severity.round()} / 5',
              Slider(value: _severity, min: 1, max: 5, divisions: 4, onChanged: (v) => setState(() => _severity = v)),
            ),
            TextField(controller: _village, decoration: InputDecoration(labelText: app.t('village'))),
            const SizedBox(height: 12),
            Row(children: [
              Expanded(child: TextField(controller: _taluk, decoration: InputDecoration(labelText: app.t('taluk')))),
              const SizedBox(width: 12),
              Expanded(child: TextField(controller: _district, decoration: InputDecoration(labelText: app.t('district')))),
            ]),
            const SizedBox(height: 12),
            TextField(controller: _desc, maxLines: 3, decoration: InputDecoration(labelText: app.t('description'))),
            if (_error != null)
              Padding(padding: const EdgeInsets.only(top: 12), child: Text(_error!, style: TextStyle(color: scheme.error))),
            const SizedBox(height: 20),
            FilledButton.icon(
              onPressed: _submit,
              icon: const Icon(Icons.save),
              label: Text(app.t('submit')),
              style: FilledButton.styleFrom(minimumSize: const Size.fromHeight(52)),
            ),
          ],
        ),
      ),
    );
  }
}
