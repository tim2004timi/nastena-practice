import 'package:flutter/material.dart';

class AppColors {
  // Основные цвета (HSL формат)
  static Color background = _hsl(258, 0.90, 0.05); // hsl(258, 90%, 5%)
  static Color backgroundEnd = _hsl(258, 0.90, 0.03); // hsl(258, 90%, 3%)
  static Color foreground = _hsl(270, 0.10, 0.95); // hsl(270, 10%, 95%)
  static Color card = _hsl(258, 0.80, 0.08); // hsl(258, 80%, 8%)
  static Color cardEnd = _hsl(258, 0.70, 0.10); // hsl(258, 70%, 10%)
  static Color primary = _hsl(266, 0.83, 0.65); // hsl(266, 83%, 65%)
  static Color secondary = _hsl(258, 0.50, 0.15); // hsl(258, 50%, 15%)
  static Color mutedForeground = _hsl(270, 0.10, 0.60); // hsl(270, 10%, 60%)
  static Color border = _hsl(258, 0.40, 0.18); // hsl(258, 40%, 18%)
  static Color input = _hsl(258, 0.40, 0.18); // hsl(258, 40%, 18%)
  static Color ring = _hsl(266, 0.83, 0.65); // hsl(266, 83%, 65%)

  // Цвета оценок
  static Color gradeFive = _hsl(142, 0.76, 0.73); // hsl(142, 76%, 73%)
  static Color gradeFour = _hsl(142, 0.71, 0.45); // hsl(142, 71%, 45%)
  static Color gradeThree = _hsl(28, 0.80, 0.52); // hsl(28, 80%, 52%)
  static Color gradeTwo = _hsl(0, 0.84, 0.60); // hsl(0, 84%, 60%)
  static Color gradeAbsent = _hsl(25, 0.47, 0.42); // hsl(25, 47%, 42%)
  static Color gradeEmpty = _hsl(258, 0.20, 0.25); // hsl(258, 20%, 25%)

  // Дополнительные цвета
  static Color successGlow = _hsl(142, 0.71, 0.45); // hsl(142, 71%, 45%)
  static Color destructive = _hsl(0, 0.84, 0.60); // hsl(0, 84%, 60%)

  // Вспомогательная функция для HSL
  static Color _hsl(double h, double s, double l) {
    // Конвертация HSL в RGB
    final c = (1 - (2 * l - 1).abs()) * s;
    final x = c * (1 - ((h / 60) % 2 - 1).abs());
    final m = l - c / 2;

    double r, g, b;

    if (h < 60) {
      r = c;
      g = x;
      b = 0;
    } else if (h < 120) {
      r = x;
      g = c;
      b = 0;
    } else if (h < 180) {
      r = 0;
      g = c;
      b = x;
    } else if (h < 240) {
      r = 0;
      g = x;
      b = c;
    } else if (h < 300) {
      r = x;
      g = 0;
      b = c;
    } else {
      r = c;
      g = 0;
      b = x;
    }

    return Color.fromRGBO(
      ((r + m) * 255).round(),
      ((g + m) * 255).round(),
      ((b + m) * 255).round(),
      1.0,
    );
  }
}

