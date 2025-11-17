import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:go_router/go_router.dart';
import 'package:lucide_icons/lucide_icons.dart';
import '../providers/app_provider.dart';
import '../utils/colors.dart';
import '../utils/gradients.dart';
import '../widgets/custom_input.dart';
import '../widgets/custom_button.dart';

class AddGroupScreen extends StatefulWidget {
  const AddGroupScreen({super.key});

  @override
  State<AddGroupScreen> createState() => _AddGroupScreenState();
}

class _AddGroupScreenState extends State<AddGroupScreen> {
  final _nameController = TextEditingController();
  final _controlSumController = TextEditingController();
  final _studentNameController = TextEditingController();
  final List<String> _students = [];
  bool _showAddStudentForm = false;

  @override
  void dispose() {
    _nameController.dispose();
    _controlSumController.dispose();
    _studentNameController.dispose();
    super.dispose();
  }

  void _toggleAddStudentForm() {
    setState(() {
      _showAddStudentForm = !_showAddStudentForm;
      if (!_showAddStudentForm) {
        _studentNameController.clear();
      }
    });
  }

  void _addStudent() {
    final name = _studentNameController.text.trim();
    if (name.isNotEmpty) {
      setState(() {
        _students.add(name);
        _studentNameController.clear();
        _showAddStudentForm = false;
      });
    }
  }

  void _removeStudent(int index) {
    setState(() {
      _students.removeAt(index);
    });
  }

  Future<void> _createGroup() async {
    if (_nameController.text.isEmpty || _controlSumController.text.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: const Text('Заполните все поля'),
          backgroundColor: AppColors.destructive,
        ),
      );
      return;
    }

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
    await appProvider.addGroup(_nameController.text, controlSum, _students);

    if (mounted) {
      context.go('/groups');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: BoxDecoration(gradient: AppGradients.backgroundGradient),
        child: SafeArea(
          child: Column(
            children: [
              // Заголовок
              Padding(
                padding: const EdgeInsets.all(24),
                child: Row(
                  children: [
                    GestureDetector(
                      onTap: () => context.go('/groups'),
                      child: Container(
                        width: 40,
                        height: 40,
                        decoration: BoxDecoration(
                          color: Colors.transparent,
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: const Icon(
                          LucideIcons.arrowLeft,
                          size: 24,
                          color: Colors.white,
                        ),
                      ),
                    ),
                    const SizedBox(width: 16),
                    Text(
                      'Новая группа',
                      style: TextStyle(
                        color: AppColors.foreground,
                        fontSize: 24,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ],
                ),
              ),
              Expanded(
                child: SingleChildScrollView(
                  padding: const EdgeInsets.symmetric(horizontal: 24),
                  child: ConstrainedBox(
                    constraints: const BoxConstraints(maxWidth: 448),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        // Форма группы
                        CustomInput(
                          label: 'Название группы',
                          placeholder: 'А12',
                          controller: _nameController,
                        ),
                        const SizedBox(height: 16),
                        CustomInput(
                          label: 'Контрольная сумма',
                          placeholder: '12',
                          controller: _controlSumController,
                          keyboardType: TextInputType.number,
                        ),
                        const SizedBox(height: 24),
                        SizedBox(
                          width: double.infinity,
                          height: 48,
                          child: CustomButton(
                            label: 'Добавить группу',
                            onPressed: _createGroup,
                            variant: ButtonVariant.default_,
                            isFullWidth: true,
                          ),
                        ),
                        const SizedBox(height: 32),
                        // Секция студентов
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Text(
                              'Студенты',
                              style: TextStyle(
                                color: AppColors.foreground,
                                fontSize: 18,
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
                                  size: 20,
                                  color: Colors.white,
                                ),
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 16),
                        // Форма добавления студента
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
                        // Список студентов
                        if (_students.isEmpty)
                          Center(
                            child: Padding(
                              padding: const EdgeInsets.all(32),
                              child: Text(
                                'Нажмите +, чтобы добавить студентов',
                                style: TextStyle(
                                  color: AppColors.mutedForeground,
                                  fontSize: 14,
                                ),
                              ),
                            ),
                          )
                        else
                          ..._students.asMap().entries.map((entry) {
                            final index = entry.key;
                            final name = entry.value;
                            return Padding(
                              padding: const EdgeInsets.only(bottom: 12),
                              child: Container(
                                padding: const EdgeInsets.all(16),
                                decoration: BoxDecoration(
                                  gradient: AppGradients.cardGradient,
                                  borderRadius: BorderRadius.circular(12),
                                ),
                                child: Row(
                                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                  children: [
                                    Expanded(
                                      child: Text(
                                        name,
                                        style: TextStyle(
                                          color: AppColors.foreground,
                                          fontSize: 16,
                                        ),
                                      ),
                                    ),
                                    GestureDetector(
                                      onTap: () => _removeStudent(index),
                                      child: const Icon(
                                        LucideIcons.x,
                                        size: 16,
                                        color: Colors.red,
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                            );
                          }),
                        const SizedBox(height: 24),
                      ],
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

