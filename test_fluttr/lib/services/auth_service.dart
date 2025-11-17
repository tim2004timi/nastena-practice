import '../models/user.dart';
import 'api_service.dart';

class AuthService {
  final ApiService _api = ApiService();

  Future<User> login(String username, String password) async {
    try {
      // POST /api/auth/token с form data
      final response = await _api.post(
        '/api/auth/token',
        {
          'username': username,
          'password': password,
        },
        includeAuth: false,
        isFormData: true,
      );

      final accessToken = response['access_token'] as String;
      
      // Сохраняем токен в памяти
      _api.setToken(accessToken);
      
      // Получаем полную информацию о пользователе через /api/auth/me
      // чтобы получить id и другие поля
      final userResponse = await _api.get('/api/auth/me');
      return User.fromJson(userResponse as Map<String, dynamic>);
    } catch (e) {
      // Пробрасываем оригинальную ошибку для отладки
      // В продакшене можно заменить на общее сообщение
      final errorMessage = e.toString().replaceAll('Exception: ', '');
      throw Exception(errorMessage.isNotEmpty ? errorMessage : 'Неверный логин или пароль');
    }
  }

  Future<User> register(String fio, String login, String password) async {
    try {
      final response = await _api.post(
        '/api/auth/register',
        {
          'login': login,
          'fio': fio,
          'password': password,
        },
        includeAuth: false,
      );

      final accessToken = response['access_token'] as String;
      
      // Сохраняем токен в памяти
      _api.setToken(accessToken);
      
      // Получаем полную информацию о пользователе через /api/auth/me
      // чтобы получить id и другие поля
      final userResponse = await _api.get('/api/auth/me');
      return User.fromJson(userResponse as Map<String, dynamic>);
    } catch (e) {
      final errorMessage = e.toString().replaceAll('Exception: ', '');
      throw Exception(errorMessage);
    }
  }

  Future<void> logout() async {
    // Удаляем токен из памяти
    _api.clearToken();
  }

  Future<User?> getCurrentUser() async {
    try {
      // GET /api/auth/me
      final response = await _api.get('/api/auth/me');
      return User.fromJson(response as Map<String, dynamic>);
    } catch (e) {
      // Если токен недействителен или отсутствует, возвращаем null
      return null;
    }
  }

  // Проверка наличия токена
  bool get isAuthenticated => _api.getToken() != null;
}

