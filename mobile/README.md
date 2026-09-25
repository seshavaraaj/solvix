# Meetpu mobile app (Flutter, Android)

One app with two roles, chosen by the phone number used to log in:

- **Citizen**: report damage with photo and GPS, see the status timeline, raise a grievance.
- **Staff (VAO)**: verification queue sorted by lowest confidence, see flags and photo, confirm or reject with a site note.

Both roles can report damage offline. Reports are saved in SQLite on the phone and sent when the network returns. Each report carries a UUID made on the phone, so a retry never creates a second record on the server.

## Run

Needs the Flutter SDK, a JDK (17 or newer) and the Android SDK.

```bash
cd mobile
flutter pub get
flutter run                                   # emulator or USB phone
flutter build apk --debug                     # build/app/outputs/flutter-apk/app-debug.apk
flutter build apk --release --dart-define=API_URL=https://meetpu-api.onrender.com
```

The server address defaults to `http://10.0.2.2:8000`, which reaches the API on your computer from the Android emulator. On a real phone, tap the server icon on the login screen and enter the Render URL, or build with `--dart-define=API_URL=...`.

## Demo logins

| Role | Phone | OTP |
|---|---|---|
| Citizen | 9000000000, or any new number | 123456 |
| Staff | 9800000001 (Chennai) or 9800000002 (Chengalpattu) | 123456 |

## Notes

- Photos are taken with the system camera and sent without resizing on the phone, so the server can read the EXIF GPS and time.
- Location comes from the phone's GPS. If a fresh fix times out, the last known position is used.
- Staff decisions need a network connection. Report capture does not.
- Tamil strings in `lib/i18n.dart` are a first draft. Have a native speaker review them.
- Bundled font: Noto Sans Tamil (SIL Open Font License, `assets/fonts/OFL.txt`).
