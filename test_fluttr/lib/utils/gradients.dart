import 'package:flutter/material.dart';
import 'colors.dart';

class AppGradients {
  // Градиент фона приложения (вертикальный сверху вниз)
  static LinearGradient backgroundGradient = LinearGradient(
    begin: Alignment.topCenter,
    end: Alignment.bottomCenter,
    colors: [
      AppColors.background,
      AppColors.backgroundEnd,
    ],
  );

  // Градиент карточек (диагональный 135°)
  static LinearGradient cardGradient = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [
      AppColors.card,
      AppColors.cardEnd,
    ],
  );
}

