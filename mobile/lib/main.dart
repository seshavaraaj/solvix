import 'package:flutter/material.dart';

import 'app_state.dart';
import 'screens/citizen_home.dart';
import 'screens/login.dart';
import 'screens/staff_home.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  app = AppState();
  await app.init();
  runApp(const MeetpuApp());
}

class MeetpuApp extends StatelessWidget {
  const MeetpuApp({super.key});

  @override
  Widget build(BuildContext context) {
    return ListenableBuilder(
      listenable: app,
      builder: (context, _) {
        final user = app.user;
        return MaterialApp(
          title: 'Meetpu',
          debugShowCheckedModeBanner: false,
          theme: ThemeData(
            colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF0F5E6E)),
            // Bundled Noto Sans Tamil makes Tamil render the same on every phone.
            fontFamilyFallback: const ['NotoSansTamil'],
            inputDecorationTheme: const InputDecorationTheme(border: OutlineInputBorder()),
          ),
          home: user == null
              ? const LoginScreen()
              : user.isStaff
                  ? const StaffHome()
                  : const CitizenHome(),
        );
      },
    );
  }
}
