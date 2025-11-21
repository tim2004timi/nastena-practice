"""
Модели данных приложения
"""
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum


class Grade(Enum):
    """Оценка студента"""
    FIVE = "5"
    FOUR = "4"
    THREE = "3"
    TWO = "2"
    ABSENT = "н"
    EMPTY = ""

    def __str__(self):
        return self.value if self.value else "—"

    @staticmethod
    def from_value(value):
        """Создать Grade из значения"""
        if value is None:
            return Grade.EMPTY
        value_str = str(value).strip()
        if value_str == "5":
            return Grade.FIVE
        elif value_str == "4":
            return Grade.FOUR
        elif value_str == "3":
            return Grade.THREE
        elif value_str == "2":
            return Grade.TWO
        elif value_str.lower() == "н":
            return Grade.ABSENT
        return Grade.EMPTY


@dataclass
class User:
    """Пользователь"""
    id: int
    full_name: str
    login: str

    def to_dict(self):
        return {
            "id": self.id,
            "fio": self.full_name,
            "login": self.login
        }

    @staticmethod
    def from_dict(data: dict):
        return User(
            id=data.get("id", 0),
            full_name=data.get("fio", ""),
            login=data.get("login", "")
        )


@dataclass
class Group:
    """Группа"""
    id: int
    name: str
    control_sum: int

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "control_sum": self.control_sum
        }

    @staticmethod
    def from_dict(data: dict):
        return Group(
            id=data.get("id", 0),
            name=data.get("name", ""),
            control_sum=data.get("control_sum", 0)
        )


@dataclass
class Student:
    """Студент"""
    id: int
    full_name: str
    group_id: int
    grades: List[Optional[Grade]]

    def __post_init__(self):
        if len(self.grades) < 3:
            self.grades.extend([Grade.EMPTY] * (3 - len(self.grades)))
        elif len(self.grades) > 3:
            self.grades = self.grades[:3]

    def get_sum(self) -> int:
        """Получить сумму оценок (5=5, 4=4, 3=3, 2=2, н=0, пусто=0)"""
        total = 0
        for grade in self.grades:
            if grade == Grade.FIVE:
                total += 5
            elif grade == Grade.FOUR:
                total += 4
            elif grade == Grade.THREE:
                total += 3
            elif grade == Grade.TWO:
                total += 2
        return total

    def is_allowed(self, control_sum: int) -> bool:
        """Проверить, допущен ли студент (сумма >= контрольной суммы)"""
        return self.get_sum() >= control_sum

    def format_name(self) -> str:
        """Форматировать ФИО в формат 'Фамилия И. И.'"""
        parts = self.full_name.split()
        if len(parts) >= 3:
            return f"{parts[0]} {parts[1][0]}. {parts[2][0]}."
        elif len(parts) == 2:
            return f"{parts[0]} {parts[1][0]}."
        return self.full_name

    def to_dict(self):
        return {
            "id": self.id,
            "fio": self.full_name,
            "group_id": self.group_id,
            "score_1": self.grades[0].value if self.grades[0] and self.grades[0] != Grade.EMPTY else None,
            "score_2": self.grades[1].value if len(self.grades) > 1 and self.grades[1] and self.grades[1] != Grade.EMPTY else None,
            "score_3": self.grades[2].value if len(self.grades) > 2 and self.grades[2] and self.grades[2] != Grade.EMPTY else None,
        }

    @staticmethod
    def from_dict(data: dict):
        scores = [
            data.get("score_1"),
            data.get("score_2"),
            data.get("score_3")
        ]
        grades = []
        for score in scores:
            if score is None or score == "":
                grades.append(Grade.EMPTY)
            else:
                grades.append(Grade.from_value(score))
        
        return Student(
            id=data.get("id", 0),
            full_name=data.get("fio", ""),
            group_id=data.get("group_id", 0),
            grades=grades
        )

