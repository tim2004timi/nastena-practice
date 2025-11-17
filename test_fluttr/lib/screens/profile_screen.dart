import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:go_router/go_router.dart';
import 'package:lucide_icons/lucide_icons.dart';
import '../providers/app_provider.dart';
import '../utils/colors.dart';
import '../utils/gradients.dart';
import '../widgets/footer_nav.dart';
import '../widgets/custom_input.dart';

class ProfileScreen extends StatefulWidget {
  const ProfileScreen({super.key});

  @override
  State<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends State<ProfileScreen> {
  bool _isEditing = false;
  final _fullNameController = TextEditingController();
  final _loginController = TextEditingController();

  @override
  void dispose() {
    _fullNameController.dispose();
    _loginController.dispose();
    super.dispose();
  }

  void _toggleEdit() {
    setState(() {
      _isEditing = !_isEditing;
      if (_isEditing) {
        final user = context.read<AppProvider>().currentUser;
        if (user != null) {
          _fullNameController.text = user.fullName;
          _loginController.text = user.login;
        }
      }
    });
  }

  Future<void> _saveChanges() async {
    final appProvider = context.read<AppProvider>();
    await appProvider.updateUser(_fullNameController.text, _loginController.text);
    setState(() {
      _isEditing = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Consumer<AppProvider>(
      builder: (context, appProvider, child) {
        final user = appProvider.currentUser;
        if (user == null) {
          return const Scaffold(body: Center(child: CircularProgressIndicator()));
        }

        final groupsCount = appProvider.groups.length;
        final studentsCount = appProvider.students.length;

        return Scaffold(
          body: Container(
            decoration: BoxDecoration(gradient: AppGradients.backgroundGradient),
            child: SafeArea(
              child: Column(
                children: [
                  Expanded(
                    child: SingleChildScrollView(
                      padding: const EdgeInsets.all(24),
                      child: ConstrainedBox(
                        constraints: const BoxConstraints(maxWidth: 448),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            // Профиль пользователя
                            Container(
                              padding: const EdgeInsets.all(24),
                              decoration: BoxDecoration(
                                gradient: AppGradients.cardGradient,
                                borderRadius: BorderRadius.circular(16),
                              ),
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Row(
                                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                    children: [
                                      Expanded(
                                        child: _isEditing
                                            ? Column(
                                                crossAxisAlignment: CrossAxisAlignment.start,
                                                children: [
                                                  CustomInput(
                                                    label: 'ФИО',
                                                    controller: _fullNameController,
                                                  ),
                                                  const SizedBox(height: 16),
                                                  CustomInput(
                                                    label: 'Логин',
                                                    controller: _loginController,
                                                  ),
                                                ],
                                              )
                                            : Column(
                                                crossAxisAlignment: CrossAxisAlignment.start,
                                                children: [
                                                  Text(
                                                    user.fullName,
                                                    style: TextStyle(
                                                      color: AppColors.foreground,
                                                      fontSize: 24,
                                                      fontWeight: FontWeight.bold,
                                                    ),
                                                  ),
                                                  const SizedBox(height: 8),
                                                  Text(
                                                    '@${user.login}',
                                                    style: TextStyle(
                                                      color: AppColors.mutedForeground,
                                                      fontSize: 16,
                                                    ),
                                                  ),
                                                ],
                                              ),
                                      ),
                                      Row(
                                        children: [
                                          if (!_isEditing)
                                            GestureDetector(
                                              onTap: () async {
                                                await appProvider.logout();
                                                if (mounted) {
                                                  context.go('/login');
                                                }
                                              },
                                              child: Container(
                                                width: 40,
                                                height: 40,
                                                decoration: BoxDecoration(
                                                  color: Colors.transparent,
                                                  borderRadius: BorderRadius.circular(8),
                                                ),
                                                child: const Icon(
                                                  LucideIcons.logOut,
                                                  color: Colors.red,
                                                  size: 24,
                                                ),
                                              ),
                                            ),
                                          if (!_isEditing) const SizedBox(width: 8),
                                          GestureDetector(
                                            onTap: _isEditing ? _saveChanges : _toggleEdit,
                                            child: Container(
                                              width: 40,
                                              height: 40,
                                              decoration: BoxDecoration(
                                                color: Colors.transparent,
                                                borderRadius: BorderRadius.circular(8),
                                              ),
                                              child: Icon(
                                                _isEditing ? LucideIcons.check : LucideIcons.settings,
                                                color: AppColors.foreground,
                                                size: 24,
                                              ),
                                            ),
                                          ),
                                        ],
                                      ),
                                    ],
                                  ),
                                ],
                              ),
                            ),
                            const SizedBox(height: 24),
                            // Статистика
                            Row(
                              children: [
                                Expanded(
                                  child: Container(
                                    padding: const EdgeInsets.all(20),
                                    decoration: BoxDecoration(
                                      gradient: AppGradients.cardGradient,
                                      borderRadius: BorderRadius.circular(16),
                                    ),
                                    child: Column(
                                      crossAxisAlignment: CrossAxisAlignment.start,
                                      children: [
                                        Container(
                                          width: 40,
                                          height: 40,
                                          decoration: BoxDecoration(
                                            color: AppColors.primary.withOpacity(0.2),
                                            shape: BoxShape.circle,
                                          ),
                                          child: const Icon(
                                            LucideIcons.folderOpen,
                                            size: 20,
                                            color: Colors.white,
                                          ),
                                        ),
                                        const SizedBox(height: 12),
                                        Text(
                                          '$groupsCount',
                                          style: TextStyle(
                                            color: AppColors.foreground,
                                            fontSize: 30,
                                            fontWeight: FontWeight.bold,
                                          ),
                                        ),
                                        const SizedBox(height: 4),
                                        Text(
                                          'Групп',
                                          style: TextStyle(
                                            color: AppColors.mutedForeground,
                                            fontSize: 14,
                                          ),
                                        ),
                                      ],
                                    ),
                                  ),
                                ),
                                const SizedBox(width: 16),
                                Expanded(
                                  child: Container(
                                    padding: const EdgeInsets.all(20),
                                    decoration: BoxDecoration(
                                      gradient: AppGradients.cardGradient,
                                      borderRadius: BorderRadius.circular(16),
                                    ),
                                    child: Column(
                                      crossAxisAlignment: CrossAxisAlignment.start,
                                      children: [
                                        Container(
                                          width: 40,
                                          height: 40,
                                          decoration: BoxDecoration(
                                            color: AppColors.primary.withOpacity(0.2),
                                            shape: BoxShape.circle,
                                          ),
                                          child: const Icon(
                                            LucideIcons.users,
                                            size: 20,
                                            color: Colors.white,
                                          ),
                                        ),
                                        const SizedBox(height: 12),
                                        Text(
                                          '$studentsCount',
                                          style: TextStyle(
                                            color: AppColors.foreground,
                                            fontSize: 30,
                                            fontWeight: FontWeight.bold,
                                          ),
                                        ),
                                        const SizedBox(height: 4),
                                        Text(
                                          'Студентов',
                                          style: TextStyle(
                                            color: AppColors.mutedForeground,
                                            fontSize: 14,
                                          ),
                                        ),
                                      ],
                                    ),
                                  ),
                                ),
                              ],
                            ),
                            const SizedBox(height: 80), // Отступ для футера
                          ],
                        ),
                      ),
                    ),
                  ),
                  FooterNav(currentRoute: '/'),
                ],
              ),
            ),
          ),
        );
      },
    );
  }
}

