import bcrypt

# Допустимые значения для оценок студентов
ALLOWED_STUDENT_SCORES = {"5", "4", "3", "2", "н"}
STUDENT_SCORE_VALUES = {
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
    "н": 0,
}


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет соответствие пароля и хеша"""
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode("utf-8")
    if isinstance(plain_password, str):
        plain_password = plain_password.encode("utf-8")
    return bcrypt.checkpw(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Генерирует хеш пароля"""
    if isinstance(password, str):
        password = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password, salt)
    return hashed.decode("utf-8")


def student_score_to_int(score: str | None) -> int:
    """Преобразует символ оценки в числовой эквивалент."""
    if score is None:
        return 0
    cleaned_score = score.strip()
    return STUDENT_SCORE_VALUES.get(cleaned_score, 0)


def student_total_score(score_1: str | None, score_2: str | None, score_3: str | None) -> int:
    """Возвращает сумму оценок студента."""
    return (
        student_score_to_int(score_1)
        + student_score_to_int(score_2)
        + student_score_to_int(score_3)
    )


