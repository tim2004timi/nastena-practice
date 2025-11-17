import 'package:flutter/foundation.dart';
import '../models/user.dart';
import '../models/group.dart';
import '../models/student.dart';
import '../models/grade.dart';
import '../services/auth_service.dart';
import '../services/groups_service.dart';
import '../services/students_service.dart';
import '../services/users_service.dart';

class AppProvider with ChangeNotifier {
  final AuthService _auth = AuthService();
  final GroupsService _groupsService = GroupsService();
  final StudentsService _studentsService = StudentsService();
  final UsersService _usersService = UsersService();

  User? _currentUser;
  List<Group> _groups = [];
  List<Student> _students = [];
  bool _isLoading = false;

  User? get currentUser => _currentUser;
  List<Group> get groups => _groups;
  List<Student> get students => _students;
  bool get isLoading => _isLoading;

  AppProvider() {
    _init();
  }

  Future<void> _init() async {
    _isLoading = true;
    notifyListeners();

    try {
      _currentUser = await _auth.getCurrentUser();
      if (_currentUser != null) {
        await _loadData();
      }
    } catch (e) {
      // Игнорируем ошибки при инициализации
      _currentUser = null;
    }

    _isLoading = false;
    notifyListeners();
  }

  Future<void> login(String login, String password) async {
    try {
      _currentUser = await _auth.login(login, password);
      await _loadData();
      notifyListeners();
    } catch (e) {
      rethrow;
    }
  }

  Future<void> register(String fullName, String login, String password) async {
    try {
      _currentUser = await _auth.register(fullName, login, password);
      await _loadData();
      notifyListeners();
    } catch (e) {
      rethrow;
    }
  }

  Future<void> logout() async {
    await _auth.logout();
    _currentUser = null;
    _groups = [];
    _students = [];
    notifyListeners();
  }

  Future<void> updateUser(String fullName, String login) async {
    if (_currentUser == null) return;

    try {
      _currentUser = await _usersService.updateCurrentUser(
        fio: fullName,
        login: login,
      );
      notifyListeners();
    } catch (e) {
      rethrow;
    }
  }

  Future<void> addGroup(String name, int controlSum, List<String> studentNames) async {
    try {
      // Создаем группу через API
      final newGroup = await _groupsService.createGroup(name, controlSum);

      // Добавляем студентов через API
      for (final studentName in studentNames) {
        await _studentsService.createStudent(
          fio: studentName,
          groupId: newGroup.id,
        );
      }

      // Перезагружаем данные
      await _loadData();
      notifyListeners();
    } catch (e) {
      rethrow;
    }
  }

  Future<void> updateGroup(int id, String name, int controlSum) async {
    try {
      await _groupsService.updateGroup(id, name, controlSum);
      await _loadData();
      notifyListeners();
    } catch (e) {
      rethrow;
    }
  }

  Future<void> deleteGroup(int id) async {
    try {
      // Получаем студентов группы перед удалением
      final groupStudents = _students.where((s) => s.groupId == id).toList();
      
      // Удаляем всех студентов группы
      for (final student in groupStudents) {
        await _studentsService.deleteStudent(student.id);
      }

      // Удаляем группу
      await _groupsService.deleteGroup(id);

      // Перезагружаем данные
      await _loadData();
      notifyListeners();
    } catch (e) {
      rethrow;
    }
  }

  Future<void> addStudent(String fullName, int groupId) async {
    try {
      await _studentsService.createStudent(
        fio: fullName,
        groupId: groupId,
      );
      await _loadData();
      notifyListeners();
    } catch (e) {
      rethrow;
    }
  }

  Future<void> deleteStudent(int studentId) async {
    try {
      await _studentsService.deleteStudent(studentId);
      await _loadData();
      notifyListeners();
    } catch (e) {
      rethrow;
    }
  }

  Future<void> updateGrade(int studentId, int gradeIndex, Grade? grade) async {
    try {
      final student = _students.firstWhere((s) => s.id == studentId);
      
      // Конвертируем Grade в строку для API
      // Если grade == null или Grade.empty, то gradeString = null (очистка оценки)
      String? gradeString;
      if (grade != null && grade != Grade.empty) {
        gradeString = grade.displayValue;
      } else {
        gradeString = null;
      }

      // Обновляем соответствующую оценку
      String? score1 = student.score1;
      String? score2 = student.score2;
      String? score3 = student.score3;

      switch (gradeIndex) {
        case 0:
          score1 = gradeString;
          break;
        case 1:
          score2 = gradeString;
          break;
        case 2:
          score3 = gradeString;
          break;
      }

      await _studentsService.updateStudent(
        studentId: studentId,
        score1: score1,
        score2: score2,
        score3: score3,
      );

      await _loadData();
      notifyListeners();
    } catch (e) {
      rethrow;
    }
  }

  Future<void> _loadData() async {
    try {
      _groups = await _groupsService.getGroups();
      _students = await _studentsService.getStudents();
    } catch (e) {
      // Игнорируем ошибки загрузки данных
    }
  }

  List<Student> getStudentsByGroup(int groupId) {
    return _students.where((s) => s.groupId == groupId).toList();
  }

  int getGroupStudentCount(int groupId) {
    return _students.where((s) => s.groupId == groupId).length;
  }

  int getGroupNotAllowedCount(int groupId) {
    try {
      final group = _groups.firstWhere((g) => g.id == groupId);
      return _students.where((s) => s.groupId == groupId && !s.isAllowed(group.controlSum)).length;
    } catch (e) {
      return 0;
    }
  }
}

