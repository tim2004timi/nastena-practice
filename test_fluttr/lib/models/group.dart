import 'student.dart';

class Group {
  final int id;
  final String name;
  final int controlSum;
  final int? studentsQuantity;
  final int? excludedStudentsQuantity;
  final List<Student>? students;

  Group({
    required this.id,
    required this.name,
    required this.controlSum,
    this.studentsQuantity,
    this.excludedStudentsQuantity,
    this.students,
  });

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'control_sum': controlSum,
      if (studentsQuantity != null) 'students_quantity': studentsQuantity,
      if (excludedStudentsQuantity != null) 'excluded_students_quantity': excludedStudentsQuantity,
      if (students != null) 'students': students!.map((s) => s.toJson()).toList(),
    };
  }

  factory Group.fromJson(Map<String, dynamic> json) {
    return Group(
      id: json['id'] as int,
      name: json['name'] as String,
      controlSum: json['control_sum'] as int,
      studentsQuantity: json['students_quantity'] as int?,
      excludedStudentsQuantity: json['excluded_students_quantity'] as int?,
      students: json['students'] != null
          ? (json['students'] as List<dynamic>)
              .map((s) => Student.fromJson(s as Map<String, dynamic>))
              .toList()
          : null,
    );
  }

  Group copyWith({
    int? id,
    String? name,
    int? controlSum,
    int? studentsQuantity,
    int? excludedStudentsQuantity,
    List<Student>? students,
  }) {
    return Group(
      id: id ?? this.id,
      name: name ?? this.name,
      controlSum: controlSum ?? this.controlSum,
      studentsQuantity: studentsQuantity ?? this.studentsQuantity,
      excludedStudentsQuantity: excludedStudentsQuantity ?? this.excludedStudentsQuantity,
      students: students ?? this.students,
    );
  }
}

