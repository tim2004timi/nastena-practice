import 'package:flutter/material.dart';
import '../models/grade.dart';
import '../utils/colors.dart';

class GradeBadge extends StatelessWidget {
  final Grade? value;
  final VoidCallback? onClick;

  const GradeBadge({
    super.key,
    required this.value,
    this.onClick,
  });

  @override
  Widget build(BuildContext context) {
    final displayValue = value?.displayValue ?? '—';
    final color = _getColor(value);

    final badge = Container(
      width: 40,
      height: 40,
      constraints: const BoxConstraints(minWidth: 48, minHeight: 48), // touch-target
      decoration: BoxDecoration(
        color: color,
        borderRadius: BorderRadius.circular(8),
      ),
      child: Center(
        child: Text(
          displayValue,
          style: const TextStyle(
            color: Colors.white,
            fontSize: 14,
            fontWeight: FontWeight.w600,
          ),
        ),
      ),
    );

    if (onClick != null) {
      return GestureDetector(
        onTap: onClick,
        child: AnimatedContainer(
          duration: const Duration(milliseconds: 150),
          child: badge,
        ),
      );
    }

    return badge;
  }

  Color _getColor(Grade? grade) {
    if (grade == null) return AppColors.gradeEmpty;

    switch (grade) {
      case Grade.five:
        return AppColors.gradeFive;
      case Grade.four:
        return AppColors.gradeFour;
      case Grade.three:
        return AppColors.gradeThree;
      case Grade.two:
        return AppColors.gradeTwo;
      case Grade.absent:
        return AppColors.gradeAbsent;
      case Grade.empty:
        return AppColors.gradeEmpty;
    }
  }
}

