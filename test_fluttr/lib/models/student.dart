import 'grade.dart';

class Student {
  final int id;
  final String fio;
  final int groupId;
  final String? score1;
  final String? score2;
  final String? score3;
  final String? groupName;

  Student({
    required this.id,
    required this.fio,
    required this.groupId,
    this.score1,
    this.score2,
    this.score3,
    this.groupName,
  });

  // Геттер для обратной совместимости
  String get fullName => fio;

  // Геттер для получения оценок как List<Grade?>
  List<Grade?> get grades {
    return [
      GradeExtension.fromString(score1),
      GradeExtension.fromString(score2),
      GradeExtension.fromString(score3),
    ];
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'fio': fio,
      'group_id': groupId,
      if (score1 != null) 'score_1': score1,
      if (score2 != null) 'score_2': score2,
      if (score3 != null) 'score_3': score3,
      if (groupName != null) 'group_name': groupName,
    };
  }

  factory Student.fromJson(Map<String, dynamic> json) {
    return Student(
      id: json['id'] as int,
      fio: json['fio'] as String,
      groupId: json['group_id'] as int,
      score1: json['score_1'] as String?,
      score2: json['score_2'] as String?,
      score3: json['score_3'] as String?,
      groupName: json['group_name'] as String?,
    );
  }

  Student copyWith({
    int? id,
    String? fio,
    int? groupId,
    String? score1,
    String? score2,
    String? score3,
    String? groupName,
  }) {
    return Student(
      id: id ?? this.id,
      fio: fio ?? this.fio,
      groupId: groupId ?? this.groupId,
      score1: score1 ?? this.score1,
      score2: score2 ?? this.score2,
      score3: score3 ?? this.score3,
      groupName: groupName ?? this.groupName,
    );
  }

  int getGradeSum() {
    return grades.fold<int>(
      0,
      (sum, grade) => sum + (grade?.numericValue ?? 0),
    );
  }

  bool isAllowed(int controlSum) {
    return getGradeSum() >= controlSum;
  }
}

