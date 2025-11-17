import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:go_router/go_router.dart';
import 'package:lucide_icons/lucide_icons.dart';
import '../providers/app_provider.dart';
import '../utils/colors.dart';
import '../utils/gradients.dart';
import '../widgets/footer_nav.dart';
import '../widgets/custom_input.dart';
import '../widgets/confirm_dialog.dart';

class GroupsScreen extends StatefulWidget {
  const GroupsScreen({super.key});

  @override
  State<GroupsScreen> createState() => _GroupsScreenState();
}

class _GroupsScreenState extends State<GroupsScreen> {
  final _searchController = TextEditingController();
  String _searchQuery = '';

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Consumer<AppProvider>(
      builder: (context, appProvider, child) {
        final groups = appProvider.groups.where((group) {
          if (_searchQuery.isEmpty) return true;
          return group.name.toLowerCase().contains(_searchQuery.toLowerCase());
        }).toList();

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
                            // Поиск и добавление
                            Row(
                              children: [
                                Expanded(
                                  child: CustomInput(
                                    placeholder: 'Поиск группы...',
                                    controller: _searchController,
                                    prefixIcon: LucideIcons.search,
                                    onChanged: (value) {
                                      setState(() {
                                        _searchQuery = value;
                                      });
                                    },
                                  ),
                                ),
                                const SizedBox(width: 12),
                                GestureDetector(
                                  onTap: () => context.go('/groups/add'),
                                  child: Container(
                                    width: 48,
                                    height: 48,
                                    decoration: BoxDecoration(
                                      gradient: AppGradients.cardGradient,
                                      borderRadius: BorderRadius.circular(8),
                                      border: Border.all(color: AppColors.border),
                                    ),
                                    child: const Icon(
                                      LucideIcons.plus,
                                      size: 24,
                                      color: Colors.white,
                                    ),
                                  ),
                                ),
                              ],
                            ),
                            const SizedBox(height: 24),
                            // Список групп
                            if (groups.isEmpty)
                              Center(
                                child: Padding(
                                  padding: const EdgeInsets.all(48),
                                  child: Text(
                                    _searchQuery.isEmpty ? 'Нет групп' : 'Группы не найдены',
                                    style: TextStyle(
                                      color: AppColors.mutedForeground,
                                      fontSize: 16,
                                    ),
                                  ),
                                ),
                              )
                            else
                              ...groups.map((group) {
                                final studentCount = appProvider.getGroupStudentCount(group.id);
                                final notAllowedCount = appProvider.getGroupNotAllowedCount(group.id);

                                return Padding(
                                  padding: const EdgeInsets.only(bottom: 16),
                                  child: Container(
                                    padding: const EdgeInsets.all(20),
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
                                              child: GestureDetector(
                                                onTap: () => context.go('/groups/${group.id}'),
                                                child: Text(
                                                  group.name,
                                                  style: TextStyle(
                                                    color: AppColors.foreground,
                                                    fontSize: 20,
                                                    fontWeight: FontWeight.bold,
                                                  ),
                                                ),
                                              ),
                                            ),
                                            GestureDetector(
                                              onTap: () async {
                                                final confirmed = await ConfirmDialog.show(
                                                  context,
                                                  title: 'Удаление группы',
                                                  message: 'Вы точно хотите удалить группу ${group.name} и всех студентов в ней?',
                                                );
                                                if (confirmed == true && mounted) {
                                                  appProvider.deleteGroup(group.id);
                                                }
                                              },
                                              child: Container(
                                                width: 32,
                                                height: 32,
                                                decoration: BoxDecoration(
                                                  color: Colors.transparent,
                                                  borderRadius: BorderRadius.circular(8),
                                                ),
                                                child: const Icon(
                                                  LucideIcons.x,
                                                  size: 20,
                                                  color: Colors.red,
                                                ),
                                              ),
                                            ),
                                          ],
                                        ),
                                        const SizedBox(height: 12),
                                        GestureDetector(
                                          onTap: () => context.go('/groups/${group.id}'),
                                          child: Row(
                                            children: [
                                              Text(
                                                'Студентов: ',
                                                style: TextStyle(
                                                  color: AppColors.mutedForeground,
                                                  fontSize: 14,
                                                ),
                                              ),
                                              Text(
                                                '$studentCount',
                                                style: TextStyle(
                                                  color: AppColors.foreground,
                                                  fontSize: 18,
                                                  fontWeight: FontWeight.w600,
                                                ),
                                              ),
                                              const SizedBox(width: 24),
                                              Text(
                                                'Недопущены: ',
                                                style: TextStyle(
                                                  color: AppColors.mutedForeground,
                                                  fontSize: 14,
                                                ),
                                              ),
                                              Text(
                                                '$notAllowedCount',
                                                style: TextStyle(
                                                  color: AppColors.destructive,
                                                  fontSize: 18,
                                                  fontWeight: FontWeight.w600,
                                                ),
                                              ),
                                            ],
                                          ),
                                        ),
                                      ],
                                    ),
                                  ),
                                );
                              }),
                            const SizedBox(height: 80), // Отступ для футера
                          ],
                        ),
                      ),
                    ),
                  ),
                  FooterNav(currentRoute: '/groups'),
                ],
              ),
            ),
          ),
        );
      },
    );
  }
}

