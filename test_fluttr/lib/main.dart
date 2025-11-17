import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:go_router/go_router.dart';
import 'providers/app_provider.dart';
import 'screens/login_screen.dart';
import 'screens/register_screen.dart';
import 'screens/profile_screen.dart';
import 'screens/groups_screen.dart';
import 'screens/add_group_screen.dart';
import 'screens/group_detail_screen.dart';
import 'screens/students_screen.dart';
import 'screens/not_found_screen.dart';
import 'utils/colors.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatefulWidget {
  const MyApp({super.key});

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  late final AppProvider _appProvider;
  late final GoRouter _router;

  @override
  void initState() {
    super.initState();
    _appProvider = AppProvider();
    _router = GoRouter(
      initialLocation: '/login',
      refreshListenable: _appProvider,
      redirect: (context, state) {
        final isLoggedIn = _appProvider.currentUser != null;
        final isLoginRoute = state.matchedLocation == '/login' || state.matchedLocation == '/register';

        // Редирект только при изменении статуса авторизации, не при каждом обновлении данных
        if (!isLoggedIn && !isLoginRoute) {
          return '/login';
        }

        if (isLoggedIn && isLoginRoute) {
          return '/';
        }

        return null;
      },
      routes: [
        GoRoute(
          path: '/login',
          builder: (context, state) => const LoginScreen(),
        ),
        GoRoute(
          path: '/register',
          builder: (context, state) => const RegisterScreen(),
        ),
        GoRoute(
          path: '/',
          builder: (context, state) => const ProfileScreen(),
        ),
        GoRoute(
          path: '/groups',
          builder: (context, state) => const GroupsScreen(),
        ),
        GoRoute(
          path: '/groups/add',
          builder: (context, state) => const AddGroupScreen(),
        ),
        GoRoute(
          path: '/groups/:id',
          builder: (context, state) {
            final id = int.parse(state.pathParameters['id']!);
            return GroupDetailScreen(groupId: id);
          },
        ),
        GoRoute(
          path: '/students',
          builder: (context, state) => const StudentsScreen(),
        ),
      ],
      errorBuilder: (context, state) => const NotFoundScreen(),
    );
  }

  @override
  void dispose() {
    _appProvider.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider.value(
      value: _appProvider,
      child: MaterialApp.router(
        title: 'Успеваемость студентов',
        debugShowCheckedModeBanner: false,
        theme: ThemeData(
          useMaterial3: true,
          colorScheme: ColorScheme.dark(
            primary: AppColors.primary,
            background: AppColors.background,
            surface: AppColors.card,
            onPrimary: Colors.white,
            onBackground: AppColors.foreground,
            onSurface: AppColors.foreground,
          ),
          scaffoldBackgroundColor: AppColors.background,
        ),
        routerConfig: _router,
      ),
    );
  }
}
