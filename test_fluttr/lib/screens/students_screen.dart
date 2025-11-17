import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:lucide_icons/lucide_icons.dart';
import '../providers/app_provider.dart';
import '../utils/colors.dart';
import '../utils/gradients.dart';
import '../utils/formatters.dart';
import '../widgets/footer_nav.dart';
import '../widgets/custom_input.dart';
import '../widgets/grade_badge.dart';
import '../widgets/grade_selector.dart';

class StudentsScreen extends StatefulWidget {
  const StudentsScreen({super.key});

  @override
  State<StudentsScreen> createState() => _StudentsScreenState();
}

class _StudentsScreenState extends State<StudentsScreen> {
  final _searchController = TextEditingController();
  String _searchQuery = '';
  String _filter = 'all'; // all, allowed, notAllowed
  int? _selectedStudentId;
  int? _selectedGradeIndex;

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  void _openGradeSelector(int studentId, int gradeIndex) {
    setState(() {
      _selectedStudentId = studentId;
      _selectedGradeIndex = gradeIndex;
    });
    showDialog(
      context: context,
      builder: (context) => GradeSelector(
        onSelect: (grade) {
          if (_selectedStudentId != null && _selectedGradeIndex != null) {
            context.read<AppProvider>().updateGrade(
                  _selectedStudentId!,
                  _selectedGradeIndex!,
                  grade,
                );
          }
        },
      ),
    ).then((_) {
      setState(() {
        _selectedStudentId = null;
        _selectedGradeIndex = null;
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return Consumer<AppProvider>(
      builder: (context, appProvider, child) {
        var students = appProvider.students;

        // Фильтрация по поиску
        if (_searchQuery.isNotEmpty) {
          students = students.where((s) {
            return s.fullName.toLowerCase().contains(_searchQuery.toLowerCase());
          }).toList();
        }

        // Фильтрация по допуску
        if (_filter == 'allowed') {
          students = students.where((s) {
            try {
              final group = appProvider.groups.firstWhere((g) => g.id == s.groupId);
              return s.isAllowed(group.controlSum);
            } catch (e) {
              return false;
            }
          }).toList();
        } else if (_filter == 'notAllowed') {
          students = students.where((s) {
            try {
              final group = appProvider.groups.firstWhere((g) => g.id == s.groupId);
              return !s.isAllowed(group.controlSum);
            } catch (e) {
              return false;
            }
          }).toList();
        }

        // Сортировка по ФИО
        students.sort((a, b) => a.fullName.compareTo(b.fullName));

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
                            // Заголовок
                            Text(
                              'Студенты',
                              style: TextStyle(
                                color: AppColors.foreground,
                                fontSize: 24,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            const SizedBox(height: 24),
                            // Поиск
                            CustomInput(
                              placeholder: 'Поиск студента...',
                              controller: _searchController,
                              prefixIcon: LucideIcons.search,
                              onChanged: (value) {
                                setState(() {
                                  _searchQuery = value;
                                });
                              },
                            ),
                            const SizedBox(height: 16),
                            // Фильтры
                            Row(
                              children: [
                                Expanded(
                                  child: GestureDetector(
                                    onTap: () => setState(() => _filter = 'all'),
                                    child: Container(
                                      height: 36,
                                      decoration: BoxDecoration(
                                        color: _filter == 'all' ? AppColors.primary : Colors.transparent,
                                        border: Border.all(
                                          color: _filter == 'all' ? AppColors.primary : AppColors.border,
                                        ),
                                        borderRadius: BorderRadius.circular(6),
                                      ),
                                      child: Center(
                                        child: Text(
                                          'Все',
                                          style: TextStyle(
                                            color: _filter == 'all' ? Colors.white : AppColors.foreground,
                                            fontSize: 14,
                                          ),
                                        ),
                                      ),
                                    ),
                                  ),
                                ),
                                const SizedBox(width: 8),
                                Expanded(
                                  child: GestureDetector(
                                    onTap: () => setState(() => _filter = 'allowed'),
                                    child: Container(
                                      height: 36,
                                      decoration: BoxDecoration(
                                        color: _filter == 'allowed' ? AppColors.primary : Colors.transparent,
                                        border: Border.all(
                                          color: _filter == 'allowed' ? AppColors.primary : AppColors.border,
                                        ),
                                        borderRadius: BorderRadius.circular(6),
                                      ),
                                      child: Center(
                                        child: Text(
                                          'Допущенные',
                                          style: TextStyle(
                                            color: _filter == 'allowed' ? Colors.white : AppColors.foreground,
                                            fontSize: 14,
                                          ),
                                        ),
                                      ),
                                    ),
                                  ),
                                ),
                                const SizedBox(width: 8),
                                Expanded(
                                  child: GestureDetector(
                                    onTap: () => setState(() => _filter = 'notAllowed'),
                                    child: Container(
                                      height: 36,
                                      decoration: BoxDecoration(
                                        color: _filter == 'notAllowed' ? AppColors.primary : Colors.transparent,
                                        border: Border.all(
                                          color: _filter == 'notAllowed' ? AppColors.primary : AppColors.border,
                                        ),
                                        borderRadius: BorderRadius.circular(6),
                                      ),
                                      child: Center(
                                        child: Text(
                                          'Недопущенные',
                                          style: TextStyle(
                                            color: _filter == 'notAllowed' ? Colors.white : AppColors.foreground,
                                            fontSize: 14,
                                          ),
                                        ),
                                      ),
                                    ),
                                  ),
                                ),
                              ],
                            ),
                            const SizedBox(height: 24),
                            // Список студентов
                            if (students.isEmpty)
                              Center(
                                child: Padding(
                                  padding: const EdgeInsets.all(48),
                                  child: Text(
                                    _searchQuery.isNotEmpty ? 'Студенты не найдены' : 'Нет студентов',
                                    style: TextStyle(
                                      color: AppColors.mutedForeground,
                                      fontSize: 16,
                                    ),
                                  ),
                                ),
                              )
                            else
                              ...students.map((student) {
                                final group = appProvider.groups.firstWhere(
                                  (g) => g.id == student.groupId,
                                  orElse: () => throw Exception('Group not found'),
                                );
                                final isAllowed = student.isAllowed(group.controlSum);
                                return Padding(
                                  padding: const EdgeInsets.only(bottom: 16),
                                  child: Container(
                                    padding: const EdgeInsets.all(16),
                                    decoration: BoxDecoration(
                                      gradient: AppGradients.cardGradient,
                                      borderRadius: BorderRadius.circular(16),
                                      border: isAllowed
                                          ? Border.all(
                                              color: AppColors.successGlow,
                                              width: 2,
                                            )
                                          : null,
                                      boxShadow: isAllowed
                                          ? [
                                              BoxShadow(
                                                color: AppColors.primary.withOpacity(0.3),
                                                blurRadius: 20,
                                                spreadRadius: 0,
                                              ),
                                            ]
                                          : null,
                                    ),
                                    child: Column(
                                      crossAxisAlignment: CrossAxisAlignment.start,
                                      children: [
                                        Text(
                                          formatFullName(student.fullName),
                                          style: TextStyle(
                                            color: AppColors.foreground,
                                            fontSize: 16,
                                            fontWeight: FontWeight.w500,
                                          ),
                                        ),
                                        const SizedBox(height: 4),
                                        Text(
                                          group.name,
                                          style: TextStyle(
                                            color: AppColors.mutedForeground,
                                            fontSize: 14,
                                          ),
                                        ),
                                        const SizedBox(height: 12),
                                        Row(
                                          children: [
                                            for (int i = 0; i < 3; i++)
                                              Padding(
                                                padding: EdgeInsets.only(right: i < 2 ? 8 : 0),
                                                child: GestureDetector(
                                                  onTap: () => _openGradeSelector(student.id, i),
                                                  child: GradeBadge(
                                                    value: student.grades[i],
                                                    onClick: () => _openGradeSelector(student.id, i),
                                                  ),
                                                ),
                                              ),
                                          ],
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
                  FooterNav(currentRoute: '/students'),
                ],
              ),
            ),
          ),
        );
      },
    );
  }
}

