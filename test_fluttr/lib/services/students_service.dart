import '../models/student.dart';
import 'api_service.dart';

class StudentsService {
  final ApiService _api = ApiService();

  // GET /api/students
  Future<List<Student>> getStudents() async {
    final response = await _api.get('/api/students');
    final List<dynamic> studentsList = response as List<dynamic>;
    return studentsList
        .map((json) => Student.fromJson(json as Map<String, dynamic>))
        .toList();
  }

  // POST /api/students
  Future<Student> createStudent({
    required String fio,
    required int groupId,
    String? score1,
    String? score2,
    String? score3,
  }) async {
    final body = <String, dynamic>{
      'fio': fio,
      'group_id': groupId,
    };
    if (score1 != null) body['score_1'] = score1;
    if (score2 != null) body['score_2'] = score2;
    if (score3 != null) body['score_3'] = score3;

    final response = await _api.post('/api/students', body);
    return Student.fromJson(response as Map<String, dynamic>);
  }

  // PUT /api/students/{student_id}
  Future<Student> updateStudent({
    required int studentId,
    String? fio,
    int? groupId,
    String? score1,
    String? score2,
    String? score3,
  }) async {
    final body = <String, dynamic>{};
    if (fio != null) body['fio'] = fio;
    if (groupId != null) body['group_id'] = groupId;
    // Отправляем все оценки, даже если они null (для очистки)
    body['score_1'] = score1;
    body['score_2'] = score2;
    body['score_3'] = score3;

    final response = await _api.put('/api/students/$studentId', body);
    return Student.fromJson(response as Map<String, dynamic>);
  }

  // DELETE /api/students/{student_id}
  Future<void> deleteStudent(int studentId) async {
    await _api.delete('/api/students/$studentId');
  }
}

