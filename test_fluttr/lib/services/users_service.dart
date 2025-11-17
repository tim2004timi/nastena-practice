import '../models/user.dart';
import 'api_service.dart';

class UsersService {
  final ApiService _api = ApiService();

  // GET /api/users/me
  Future<User> getCurrentUser() async {
    final response = await _api.get('/api/users/me');
    return User.fromJson(response as Map<String, dynamic>);
  }

  // PUT /api/users/me
  Future<User> updateCurrentUser({String? fio, String? login}) async {
    final body = <String, dynamic>{};
    if (fio != null) body['fio'] = fio;
    if (login != null) body['login'] = login;

    final response = await _api.put('/api/users/me', body);
    return User.fromJson(response as Map<String, dynamic>);
  }

  // GET /api/users/{user_id}
  Future<User> getUser(int userId) async {
    final response = await _api.get('/api/users/$userId');
    return User.fromJson(response as Map<String, dynamic>);
  }

  // GET /api/users
  Future<List<User>> getUsers({int skip = 0, int limit = 100}) async {
    final response = await _api.get('/api/users?skip=$skip&limit=$limit');
    final List<dynamic> usersList = response as List<dynamic>;
    return usersList
        .map((json) => User.fromJson(json as Map<String, dynamic>))
        .toList();
  }
}

