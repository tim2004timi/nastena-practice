enum Grade {
  five,    // 5
  four,    // 4
  three,   // 3
  two,     // 2
  absent,  // "н" (неявка)
  empty    // null (пусто)
}

extension GradeExtension on Grade {
  String get displayValue {
    switch (this) {
      case Grade.five:
        return '5';
      case Grade.four:
        return '4';
      case Grade.three:
        return '3';
      case Grade.two:
        return '2';
      case Grade.absent:
        return 'н';
      case Grade.empty:
        return '—';
    }
  }

  int? get numericValue {
    switch (this) {
      case Grade.five:
        return 5;
      case Grade.four:
        return 4;
      case Grade.three:
        return 3;
      case Grade.two:
        return 2;
      case Grade.absent:
      case Grade.empty:
        return null;
    }
  }

  static Grade? fromString(String? value) {
    if (value == null) return Grade.empty;
    switch (value) {
      case '5':
        return Grade.five;
      case '4':
        return Grade.four;
      case '3':
        return Grade.three;
      case '2':
        return Grade.two;
      case 'н':
        return Grade.absent;
      default:
        return Grade.empty;
    }
  }
}

