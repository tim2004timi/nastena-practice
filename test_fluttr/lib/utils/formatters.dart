// Форматирование ФИО: "Иванов Иван Иванович" → "Иванов И. И."
String formatFullName(String fullName) {
  final parts = fullName.trim().split(' ');
  if (parts.isEmpty) return fullName;
  if (parts.length == 1) return fullName;

  final surname = parts[0];
  final initials = parts.skip(1).map((part) {
    if (part.isEmpty) return '';
    return '${part[0]}.';
  }).join(' ');

  return '$surname $initials';
}

