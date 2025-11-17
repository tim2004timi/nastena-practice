import 'package:flutter/material.dart';
import '../models/grade.dart';
import '../utils/colors.dart';
import '../utils/gradients.dart';
import 'grade_badge.dart';

class GradeSelector extends StatelessWidget {
  final Function(Grade?) onSelect;

  const GradeSelector({
    super.key,
    required this.onSelect,
  });

  @override
  Widget build(BuildContext context) {
    return Dialog(
      backgroundColor: Colors.transparent,
      child: Container(
        constraints: const BoxConstraints(maxWidth: 280),
        padding: const EdgeInsets.all(20),
        decoration: BoxDecoration(
          gradient: AppGradients.cardGradient,
          borderRadius: BorderRadius.circular(16),
        ),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Выберите оценку',
              style: TextStyle(
                color: AppColors.foreground,
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 16),
            GridView.count(
              shrinkWrap: true,
              crossAxisCount: 3,
              crossAxisSpacing: 12,
              mainAxisSpacing: 12,
              childAspectRatio: 1,
              children: [
                _buildGradeButton(context, Grade.five),
                _buildGradeButton(context, Grade.four),
                _buildGradeButton(context, Grade.three),
                _buildGradeButton(context, Grade.two),
                _buildGradeButton(context, Grade.absent),
                _buildClearButton(context),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildGradeButton(BuildContext context, Grade grade) {
    return GestureDetector(
      onTap: () {
        onSelect(grade);
        Navigator.of(context).pop();
      },
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 150),
        child: GradeBadge(value: grade),
      ),
    );
  }

  Widget _buildClearButton(BuildContext context) {
    return GestureDetector(
      onTap: () {
        onSelect(null);
        Navigator.of(context).pop();
      },
      child: Container(
        height: 56,
        decoration: BoxDecoration(
          color: AppColors.gradeEmpty,
          borderRadius: BorderRadius.circular(8),
        ),
        child: Center(
          child: Text(
            'Очистить',
            style: TextStyle(
              color: Colors.white,
              fontSize: 14,
              fontWeight: FontWeight.w600,
            ),
          ),
        ),
      ),
    );
  }
}

