class User {
  final int id;
  final String fio;
  final String login;
  final bool? isActive;
  final String? createdAt;
  final String? updatedAt;
  final int? studentsQuantity;
  final int? groupsQuantity;

  User({
    required this.id,
    required this.fio,
    required this.login,
    this.isActive,
    this.createdAt,
    this.updatedAt,
    this.studentsQuantity,
    this.groupsQuantity,
  });

  // Геттер для обратной совместимости
  String get fullName => fio;

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'fio': fio,
      'login': login,
      if (isActive != null) 'is_active': isActive,
      if (createdAt != null) 'created_at': createdAt,
      if (updatedAt != null) 'updated_at': updatedAt,
      if (studentsQuantity != null) 'students_quantity': studentsQuantity,
      if (groupsQuantity != null) 'groups_quantity': groupsQuantity,
    };
  }

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: (json['id'] ?? 0) as int, // Если id отсутствует (в auth/token), используем 0
      fio: json['fio'] as String,
      login: json['login'] as String,
      isActive: json['is_active'] as bool?,
      createdAt: json['created_at'] as String?,
      updatedAt: json['updated_at'] as String?,
      studentsQuantity: json['students_quantity'] as int?,
      groupsQuantity: json['groups_quantity'] as int?,
    );
  }

  User copyWith({
    int? id,
    String? fio,
    String? login,
    bool? isActive,
    String? createdAt,
    String? updatedAt,
    int? studentsQuantity,
    int? groupsQuantity,
  }) {
    return User(
      id: id ?? this.id,
      fio: fio ?? this.fio,
      login: login ?? this.login,
      isActive: isActive ?? this.isActive,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
      studentsQuantity: studentsQuantity ?? this.studentsQuantity,
      groupsQuantity: groupsQuantity ?? this.groupsQuantity,
    );
  }
}

