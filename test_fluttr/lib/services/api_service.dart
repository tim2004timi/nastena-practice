import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  static const String baseUrl = 'http://37.9.13.207:8000';
  static final ApiService _instance = ApiService._internal();
  String? _token;

  factory ApiService() {
    return _instance;
  }

  ApiService._internal();

  // Установить токен
  void setToken(String? token) {
    _token = token;
  }

  // Получить токен
  String? getToken() => _token;

  // Удалить токен
  void clearToken() {
    _token = null;
  }

  // Получить заголовки с авторизацией
  Map<String, String> _getHeaders({bool includeAuth = true}) {
    final headers = <String, String>{
      'Content-Type': 'application/json',
    };
    if (includeAuth && _token != null) {
      headers['Authorization'] = 'Bearer $_token';
    }
    return headers;
  }

  // Обработка ответа
  dynamic _handleResponse(http.Response response) {
    if (response.statusCode >= 200 && response.statusCode < 300) {
      if (response.body.isEmpty) {
        return null;
      }
      return json.decode(response.body);
    } else {
      final errorBody = response.body.isNotEmpty
          ? json.decode(response.body)
          : <String, dynamic>{};
      final errorMessage = errorBody['detail'] ?? 
          errorBody['message'] ?? 
          'Ошибка: ${response.statusCode}';
      throw Exception(errorMessage);
    }
  }

  // GET запрос
  Future<dynamic> get(String endpoint, {bool includeAuth = true}) async {
    final url = Uri.parse('$baseUrl$endpoint');
    final response = await http.get(
      url,
      headers: _getHeaders(includeAuth: includeAuth),
    );
    return _handleResponse(response);
  }

  // POST запрос
  Future<dynamic> post(
    String endpoint,
    Map<String, dynamic>? body, {
    bool includeAuth = true,
    bool isFormData = false,
  }) async {
    final url = Uri.parse('$baseUrl$endpoint');
    http.Response response;
    
    if (isFormData) {
      // Для form data (используется в /api/auth/token)
      // application/x-www-form-urlencoded
      final headers = <String, String>{
        'Content-Type': 'application/x-www-form-urlencoded',
      };
      if (includeAuth && _token != null) {
        headers['Authorization'] = 'Bearer $_token';
      }
      // Для form data отправляем как Map<String, String>
      // Пакет http автоматически закодирует это в application/x-www-form-urlencoded
      final formBody = body?.map((key, value) => MapEntry(key, value.toString()));
      response = await http.post(
        url,
        headers: headers,
        body: formBody,
      );
    } else {
      response = await http.post(
        url,
        headers: _getHeaders(includeAuth: includeAuth),
        body: body != null ? json.encode(body) : null,
      );
    }
    
    return _handleResponse(response);
  }

  // PUT запрос
  Future<dynamic> put(
    String endpoint,
    Map<String, dynamic>? body, {
    bool includeAuth = true,
  }) async {
    final url = Uri.parse('$baseUrl$endpoint');
    final response = await http.put(
      url,
      headers: _getHeaders(includeAuth: includeAuth),
      body: body != null ? json.encode(body) : null,
    );
    return _handleResponse(response);
  }

  // DELETE запрос
  Future<void> delete(String endpoint, {bool includeAuth = true}) async {
    final url = Uri.parse('$baseUrl$endpoint');
    final response = await http.delete(
      url,
      headers: _getHeaders(includeAuth: includeAuth),
    );
    _handleResponse(response);
  }
}

