import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/user.dart';
import '../models/group.dart';
import '../models/student.dart';

class StorageService {
  static const String _usersKey = 'users';
  static const String _currentUserKey = 'current_user';
  static const String _groupsKey = 'groups';
  static const String _studentsKey = 'students';

  Future<List<User>> getUsers() async {
    final prefs = await SharedPreferences.getInstance();
    final usersJson = prefs.getString(_usersKey);
    if (usersJson == null) return [];
    final List<dynamic> usersList = json.decode(usersJson);
    return usersList.map((json) => User.fromJson(json)).toList();
  }

  Future<void> saveUsers(List<User> users) async {
    final prefs = await SharedPreferences.getInstance();
    final usersJson = json.encode(users.map((u) => u.toJson()).toList());
    await prefs.setString(_usersKey, usersJson);
  }

  Future<User?> getCurrentUser() async {
    final prefs = await SharedPreferences.getInstance();
    final userJson = prefs.getString(_currentUserKey);
    if (userJson == null) return null;
    return User.fromJson(json.decode(userJson));
  }

  Future<void> setCurrentUser(User? user) async {
    final prefs = await SharedPreferences.getInstance();
    if (user == null) {
      await prefs.remove(_currentUserKey);
    } else {
      await prefs.setString(_currentUserKey, json.encode(user.toJson()));
    }
  }

  Future<List<Group>> getGroups() async {
    final prefs = await SharedPreferences.getInstance();
    final groupsJson = prefs.getString(_groupsKey);
    if (groupsJson == null) return [];
    final List<dynamic> groupsList = json.decode(groupsJson);
    return groupsList.map((json) => Group.fromJson(json)).toList();
  }

  Future<void> saveGroups(List<Group> groups) async {
    final prefs = await SharedPreferences.getInstance();
    final groupsJson = json.encode(groups.map((g) => g.toJson()).toList());
    await prefs.setString(_groupsKey, groupsJson);
  }

  Future<List<Student>> getStudents() async {
    final prefs = await SharedPreferences.getInstance();
    final studentsJson = prefs.getString(_studentsKey);
    if (studentsJson == null) return [];
    final List<dynamic> studentsList = json.decode(studentsJson);
    return studentsList.map((json) => Student.fromJson(json)).toList();
  }

  Future<void> saveStudents(List<Student> students) async {
    final prefs = await SharedPreferences.getInstance();
    final studentsJson = json.encode(students.map((s) => s.toJson()).toList());
    await prefs.setString(_studentsKey, studentsJson);
  }
}

