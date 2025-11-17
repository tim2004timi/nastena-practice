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
import '../widgets/custom_button.dart';
import '../widgets/confirm_dialog.dart';

class GroupDetailScreen extends StatefulWidget {
  final int groupId;

  const GroupDetailScreen({super.key, required this.groupId});

  @override
  State<GroupDetailScreen> createState() => _GroupDetailScreenState();
}

class _GroupDetailScreenState extends State<GroupDetailScreen> {
  final _searchController = TextEditingController();
  final _nameController = TextEditingController();
  final _controlSumController = TextEditingController();
  final _studentNameController = TextEditingController();
  String _searchQuery = '';
  String _filter = 'all'; // all, allowed, notAllowed
  bool _isEditing = false;
  bool _showAddStudentForm = false;
  int? _selectedGradeIndex;
  int? _selectedStudentId;

  @override
  void dispose() {
    _searchController.dispose();
    _nameController.dispose();
    _controlSumController.dispose();
    _studentNameController.dispose();
    super.dispose();
  }

  void _toggleEdit() {
    setState(() {
      _isEditing = !_isEditing;
      if (_isEditing) {
        final group = context.read<AppProvider>().groups.firstWhere(
              (g) => g.id == widget.groupId,
            );
        _nameController.text = group.name;
        _controlSumController.text = group.controlSum.toString();
      }
    });
  }

  Future<void> _saveChanges() async {
    final controlSum = int.tryParse(_controlSumController.text);
    if (controlSum == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: const Text('Введите корректную контрольную сумму'),
          backgroundColor: AppColors.destructive,
        ),
      );
      return;
    }

    final appProvider = context.read<AppProvider>();
    await appProvider.updateGroup(widget.groupId, _nameController.text, controlSum);
    setState(() {
      _isEditing = false;
    });
  }

  void _toggleAddStudentForm() {
    setState(() {
      _showAddStudentForm = !_showAddStudentForm;
      if (!_showAddStudentForm) {
        _studentNameController.clear();
      }
    });
  }

  Future<void> _addStudent() async {
    final name = _studentNameController.text.trim();
    if (name.isEmpty) return;

    final appProvider = context.read<AppProvider>();
    await appProvider.addStudent(name, widget.groupId);
    setState(() {
      _studentNameController.clear();
      _showAddStudentForm = false;
    });
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
        final group = appProvider.groups.firstWhere(
          (g) => g.id == widget.groupId,
          orElse: () => throw Exception('Group not found'),
        );

        var students = appProvider.getStudentsByGroup(widget.groupId);

        // Фильтрация по поиску
        if (_searchQuery.isNotEmpty) {
          students = students.where((s) {
            return s.fullName.toLowerCase().contains(_searchQuery.toLowerCase());
          }).toList();
        }

        // Фильтрация по допуску
        if (_filter == 'allowed') {
          students = students.where((s) => s.isAllowed(group.controlSum)).toList();
        } else if (_filter == 'notAllowed') {
          students = students.where((s) => !s.isAllowed(group.controlSum)).toList();
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
                            // Информация о группе
                            Container(
                              padding: const EdgeInsets.all(20),
                              decoration: BoxDecoration(
                                gradient: AppGradients.cardGradient,
                                borderRadius: BorderRadius.circular(16),
                              ),
                              child: Row(
                                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                children: [
                                  Expanded(
                                    child: _isEditing
                                        ? Column(
                                            crossAxisAlignment: CrossAxisAlignment.start,
                                            children: [
                                              CustomInput(
                                                label: 'Название',
                                                controller: _nameController,
                                              ),
                                              const SizedBox(height: 16),
                                              CustomInput(
                                                label: 'Контрольная сумма',
                                                controller: _controlSumController,
                                                keyboardType: TextInputType.number,
                                              ),
                                            ],
                                          )
                                        : Column(
                                            crossAxisAlignment: CrossAxisAlignment.start,
                                            children: [
                                              Text(
                                                group.name,
                                                style: TextStyle(
                                                  color: AppColors.foreground,
                                                  fontSize: 24,
                                                  fontWeight: FontWeight.bold,
                                                ),
                                              ),
                                              const SizedBox(height: 8),
                                              Text(
                                                'Контрольная сумма: ${group.controlSum}',
                                                style: TextStyle(
                                                  color: AppColors.mutedForeground,
                                                  fontSize: 14,
                                                ),
                                              ),
                                            ],
                                          ),
                                  ),
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
                            // Добавление студента (только в режиме редактирования)
                            if (_isEditing) ...[
                              Row(
                                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                children: [
                                  Text(
                                    'Добавить студента',
                                    style: TextStyle(
                                      color: AppColors.mutedForeground,
                                      fontSize: 14,
                                      fontWeight: FontWeight.w600,
                                    ),
                                  ),
                                  GestureDetector(
                                    onTap: _toggleAddStudentForm,
                                    child: Container(
                                      width: 32,
                                      height: 32,
                                      decoration: BoxDecoration(
                                        border: Border.all(color: AppColors.border),
                                        borderRadius: BorderRadius.circular(8),
                                      ),
                                      child: const Icon(
                                        LucideIcons.plus,
                                        size: 16,
                                        color: Colors.white,
                                      ),
                                    ),
                                  ),
                                ],
                              ),
                              const SizedBox(height: 12),
                              if (_showAddStudentForm)
                                Container(
                                  padding: const EdgeInsets.all(16),
                                  decoration: BoxDecoration(
                                    gradient: AppGradients.cardGradient,
                                    borderRadius: BorderRadius.circular(16),
                                  ),
                                  child: Column(
                                    children: [
                                      CustomInput(
                                        placeholder: 'Иванов И. И.',
                                        controller: _studentNameController,
                                      ),
                                      const SizedBox(height: 12),
                                      Row(
                                        children: [
                                          Expanded(
                                            child: CustomButton(
                                              label: 'Добавить',
                                              icon: LucideIcons.check,
                                              onPressed: _addStudent,
                                              variant: ButtonVariant.default_,
                                            ),
                                          ),
                                          const SizedBox(width: 12),
                                          Expanded(
                                            child: CustomButton(
                                              label: 'Отмена',
                                              onPressed: _toggleAddStudentForm,
                                              variant: ButtonVariant.outline,
                                            ),
                                          ),
                                        ],
                                      ),
                                    ],
                                  ),
                                ),
                              const SizedBox(height: 16),
                            ],
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
                                        Row(
                                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                          children: [
                                            Expanded(
                                              child: Text(
                                                formatFullName(student.fullName),
                                                style: TextStyle(
                                                  color: AppColors.foreground,
                                                  fontSize: 16,
                                                  fontWeight: FontWeight.w500,
                                                ),
                                              ),
                                            ),
                                            if (_isEditing)
                                              GestureDetector(
                                                onTap: () async {
                                                  final confirmed = await ConfirmDialog.show(
                                                    context,
                                                    title: 'Удаление студента',
                                                    message: 'Вы точно хотите удалить студента ${formatFullName(student.fullName)}?',
                                                  );
                                                  if (confirmed == true && mounted) {
                                                    appProvider.deleteStudent(student.id);
                                                  }
                                                },
                                                child: Container(
                                                  width: 24,
                                                  height: 24,
                                                  child: const Icon(
                                                    LucideIcons.x,
                                                    size: 16,
                                                    color: Colors.red,
                                                  ),
                                                ),
                                              ),
                                          ],
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

