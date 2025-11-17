import '../models/group.dart';
import 'api_service.dart';

class GroupsService {
  final ApiService _api = ApiService();

  // GET /api/groups
  Future<List<Group>> getGroups() async {
    final response = await _api.get('/api/groups');
    final List<dynamic> groupsList = response as List<dynamic>;
    return groupsList
        .map((json) => Group.fromJson(json as Map<String, dynamic>))
        .toList();
  }

  // GET /api/groups/{group_id}
  Future<Group> getGroup(int groupId) async {
    final response = await _api.get('/api/groups/$groupId');
    return Group.fromJson(response as Map<String, dynamic>);
  }

  // POST /api/groups
  Future<Group> createGroup(String name, int controlSum) async {
    final response = await _api.post(
      '/api/groups',
      {
        'name': name,
        'control_sum': controlSum,
      },
    );
    return Group.fromJson(response as Map<String, dynamic>);
  }

  // PUT /api/groups/{group_id}
  Future<Group> updateGroup(int groupId, String name, int controlSum) async {
    final response = await _api.put(
      '/api/groups/$groupId',
      {
        'name': name,
        'control_sum': controlSum,
      },
    );
    return Group.fromJson(response as Map<String, dynamic>);
  }

  // DELETE /api/groups/{group_id}
  Future<void> deleteGroup(int groupId) async {
    await _api.delete('/api/groups/$groupId');
  }
}

