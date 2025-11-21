import requests
from typing import List, Optional
from models import User, Group, Student, Grade


class ApiService:
    """Сервис для работы с API"""
    
    def __init__(self, base_url: str = "http://37.9.13.207:8000/api"):
        self.base_url = base_url
        self.token: Optional[str] = None
    
    def set_token(self, token: str):
        """Установить токен авторизации"""
        self.token = token
    
    def _get_headers(self) -> dict:
        """Получить заголовки для запросов"""
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers
    
    def login(self, login: str, password: str) -> Optional[dict]:
        """Вход в систему"""
        try:
            response = requests.post(
                f"{self.base_url}/auth/token",
                data={
                    "grant_type": "password",
                    "username": login,
                    "password": password,
                    "scope": "",
                    "client_id": "string",
                    "client_secret": ""
                },
                headers={
                    "accept": "application/json",
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                timeout=None
            )
            if response.status_code == 200:
                data = response.json()
                token = data.get("access_token")
                if token:
                    self.set_token(token)
                return {
                    "access_token": token,
                    "user": data.get("user", {})
                }
            else:
                print(f"Ошибка входа: статус {response.status_code}")
                try:
                    error_detail = response.json()
                    print(f"Детали ошибки: {error_detail}")
                except:
                    print(f"Текст ответа: {response.text}")
            return None
        except Exception as e:
            print(f"Ошибка при входе: {e}")
            return None
    
    def register(self, full_name: str, login: str, password: str) -> Optional[dict]:
        """Регистрация нового пользователя"""
        try:
            response = requests.post(
                f"{self.base_url}/auth/register",
                json={
                    "login": login,
                    "fio": full_name,
                    "password": password
                },
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 200:
                data = response.json()
                token = data.get("access_token")
                if token:
                    self.set_token(token)
                return {
                    "access_token": token,
                    "user": data.get("user", {})
                }
            return None
        except Exception as e:
            print(f"Ошибка при регистрации: {e}")
            return None
    
    def get_current_user(self) -> Optional[User]:
        """Получить текущего пользователя"""
        try:
            response = requests.get(f"{self.base_url}/users/me", headers=self._get_headers())
            if response.status_code == 200:
                return User.from_dict(response.json())
            return None
        except Exception as e:
            print(f"Ошибка при получении пользователя: {e}")
            return None
    
    def update_user(self, full_name: str, login: str) -> Optional[User]:
        """Обновить данные пользователя"""
        try:
            response = requests.put(
                f"{self.base_url}/users/me",
                json={"fio": full_name, "login": login},
                headers=self._get_headers()
            )
            if response.status_code == 200:
                return User.from_dict(response.json())
            return None
        except Exception as e:
            print(f"Ошибка при обновлении пользователя: {e}")
            return None
    
    def get_groups(self) -> List[Group]:
        """Получить список всех групп"""
        try:
            response = requests.get(f"{self.base_url}/groups", headers=self._get_headers())
            if response.status_code == 200:
                return [Group.from_dict(g) for g in response.json()]
            return []
        except Exception as e:
            print(f"Ошибка при получении групп: {e}")
            return []
    
    def get_group(self, group_id: int) -> Optional[Group]:
        """Получить группу по ID"""
        try:
            response = requests.get(f"{self.base_url}/groups/{group_id}", headers=self._get_headers())
            if response.status_code == 200:
                data = response.json()
                group_data = {k: v for k, v in data.items() if k != "students"}
                return Group.from_dict(group_data)
            return None
        except Exception as e:
            print(f"Ошибка при получении группы: {e}")
            return None
    
    def get_group_with_students(self, group_id: int) -> tuple[Optional[Group], List[Student]]:
        """Получить группу со студентами"""
        try:
            response = requests.get(f"{self.base_url}/groups/{group_id}", headers=self._get_headers())
            if response.status_code == 200:
                data = response.json()
                students_data = data.get("students", [])
                students = [Student.from_dict(s) for s in students_data]
                group_data = {k: v for k, v in data.items() if k != "students"}
                group = Group.from_dict(group_data)
                return group, students
            return None, []
        except Exception as e:
            print(f"Ошибка при получении группы со студентами: {e}")
            return None, []
    
    def create_group(self, name: str, control_sum: int) -> Optional[Group]:
        """Создать новую группу"""
        try:
            response = requests.post(
                f"{self.base_url}/groups",
                json={"name": name, "control_sum": control_sum},
                headers=self._get_headers()
            )
            if response.status_code in [200, 201]:
                return Group.from_dict(response.json())
            return None
        except Exception as e:
            print(f"Ошибка при создании группы: {e}")
            return None
    
    def update_group(self, group_id: int, name: str, control_sum: int) -> Optional[Group]:
        """Обновить группу"""
        try:
            response = requests.put(
                f"{self.base_url}/groups/{group_id}",
                json={"name": name, "control_sum": control_sum},
                headers=self._get_headers()
            )
            if response.status_code == 200:
                return Group.from_dict(response.json())
            return None
        except Exception as e:
            print(f"Ошибка при обновлении группы: {e}")
            return None
    
    def delete_group(self, group_id: int) -> bool:
        """Удалить группу"""
        try:
            response = requests.delete(f"{self.base_url}/groups/{group_id}", headers=self._get_headers())
            return response.status_code == 204
        except Exception as e:
            print(f"Ошибка при удалении группы: {e}")
            return False
    
    def get_students(self, group_id: Optional[int] = None) -> List[Student]:
        """Получить список студентов (опционально по группе)"""
        try:
            url = f"{self.base_url}/students"
            response = requests.get(url, headers=self._get_headers())
            if response.status_code == 200:
                students = [Student.from_dict(s) for s in response.json()]
                if group_id is not None:
                    students = [s for s in students if s.group_id == group_id]
                return students
            return []
        except Exception as e:
            print(f"Ошибка при получении студентов: {e}")
            return []
    
    def get_student(self, student_id: int) -> Optional[Student]:
        """Получить студента по ID"""
        try:
            students = self.get_students()
            for student in students:
                if student.id == student_id:
                    return student
            return None
        except Exception as e:
            print(f"Ошибка при получении студента: {e}")
            return None
    
    def create_student(self, full_name: str, group_id: int) -> Optional[Student]:
        """Создать нового студента"""
        try:
            response = requests.post(
                f"{self.base_url}/students",
                json={
                    "fio": full_name,
                    "group_id": group_id,
                    "score_1": None,
                    "score_2": None,
                    "score_3": None
                },
                headers=self._get_headers()
            )
            if response.status_code in [200, 201]:
                return Student.from_dict(response.json())
            return None
        except Exception as e:
            print(f"Ошибка при создании студента: {e}")
            return None
    
    def update_student_grade(self, student_id: int, grade_index: int, grade: Optional[Grade]) -> Optional[Student]:
        """Обновить оценку студента"""
        try:
            student = self.get_student(student_id)
            if not student:
                return None
            
            student.grades[grade_index] = grade if grade is not None else Grade.EMPTY
            
            response = requests.put(
                f"{self.base_url}/students/{student_id}",
                json=student.to_dict(),
                headers=self._get_headers()
            )
            if response.status_code == 200:
                return Student.from_dict(response.json())
            return None
        except Exception as e:
            print(f"Ошибка при обновлении оценки: {e}")
            return None
    
    def delete_student(self, student_id: int) -> bool:
        """Удалить студента"""
        try:
            response = requests.delete(f"{self.base_url}/students/{student_id}", headers=self._get_headers())
            return response.status_code == 204
        except Exception as e:
            print(f"Ошибка при удалении студента: {e}")
            return False
