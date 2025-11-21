# Отчет по эндпоинтам API

## Auth

### POST /api/auth/token application/x-www-form-urlencoded
**Входные данные:**
- `username`: str (form data)
- `password`: str (form data)

**Выходные данные:**
```json
{
  "access_token": "string",
  "token_type": "bearer",
  "user": {
    "login": "string",
    "fio": "string",
    "is_active": true,
    "created_at": "datetime",
    "updated_at": "datetime"
  }
}
```

### POST /api/auth/register
**Входные данные:**
```json
{
  "login": "string",
  "fio": "string",
  "password": "string"
}
```

**Выходные данные:**
```json
{
  "access_token": "string",
  "token_type": "bearer",
  "user": {
    "login": "string",
    "fio": "string",
    "is_active": true,
    "created_at": "datetime",
    "updated_at": "datetime"
  }
}
```

### GET /api/auth/me
**Входные данные:** нет

**Выходные данные:**
```json
{
  "id": 0,
  "login": "string",
  "fio": "string",
  "is_active": true,
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

## Users

### GET /api/users/me
**Входные данные:** нет

**Выходные данные:**
```json
{
  "id": 0,
  "login": "string",
  "fio": "string",
  "is_active": true,
  "created_at": "datetime",
  "updated_at": "datetime",
  "students_quantity": 0,
  "groups_quantity": 0
}
```

### PUT /api/users/me
**Входные данные:**
```json
{
  "fio": "string",
  "login": "string"
}
```

**Выходные данные:**
```json
{
  "id": 0,
  "login": "string",
  "fio": "string",
  "is_active": true,
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### GET /api/users/{user_id}
**Входные данные:**
- `user_id`: int (path parameter)

**Выходные данные:**
```json
{
  "id": 0,
  "login": "string",
  "fio": "string",
  "is_active": true,
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### GET /api/users
**Входные данные:**
- `skip`: int (query parameter, default: 0)
- `limit`: int (query parameter, default: 100)

**Выходные данные:**
```json
[
  {
    "id": 0,
    "login": "string",
    "fio": "string",
    "is_active": true,
    "created_at": "datetime",
    "updated_at": "datetime"
  }
]
```

## Groups

### POST /api/groups
**Входные данные:**
```json
{
  "name": "string",
  "control_sum": 0
}
```

**Выходные данные:**
```json
{
  "id": 0,
  "name": "string",
  "control_sum": 0,
  "students_quantity": 0,
  "excluded_students_quantity": 0
}
```

### PUT /api/groups/{group_id}
**Входные данные:**
- `group_id`: int (path parameter)
```json
{
  "name": "string",
  "control_sum": 0
}
```

**Выходные данные:**
```json
{
  "id": 0,
  "name": "string",
  "control_sum": 0,
  "students_quantity": 0,
  "excluded_students_quantity": 0
}
```

### DELETE /api/groups/{group_id}
**Входные данные:**
- `group_id`: int (path parameter)

**Выходные данные:** нет (204 No Content)

### GET /api/groups
**Входные данные:** нет

**Выходные данные:**
```json
[
  {
    "id": 0,
    "name": "string",
    "control_sum": 0,
    "students_quantity": 0,
    "excluded_students_quantity": 0
  }
]
```

### GET /api/groups/{group_id}
**Входные данные:**
- `group_id`: int (path parameter)

**Выходные данные:**
```json
{
  "id": 0,
  "name": "string",
  "control_sum": 0,
  "students_quantity": 0,
  "excluded_students_quantity": 0,
  "students": [
    {
      "id": 0,
      "fio": "string",
      "score_1": "string",
      "score_2": "string",
      "score_3": "string",
      "group_id": 0
    }
  ]
}
```

## Students

### POST /api/students
**Входные данные:**
```json
{
  "fio": "string",
  "group_id": 0,
  "score_1": "string",
  "score_2": "string",
  "score_3": "string"
}
```

**Выходные данные:**
```json
{
  "id": 0,
  "fio": "string",
  "score_1": "string",
  "score_2": "string",
  "score_3": "string",
  "group_id": 0
}
```

### GET /api/students
**Входные данные:** нет

**Выходные данные:**
```json
[
  {
    "id": 0,
    "fio": "string",
    "score_1": "string",
    "score_2": "string",
    "score_3": "string",
    "group_id": 0,
    "group_name": "string"
  }
]
```

### PUT /api/students/{student_id}
**Входные данные:**
- `student_id`: int (path parameter)
```json
{
  "fio": "string",
  "score_1": "string",
  "score_2": "string",
  "score_3": "string",
  "group_id": 0
}
```

**Выходные данные:**
```json
{
  "id": 0,
  "fio": "string",
  "score_1": "string",
  "score_2": "string",
  "score_3": "string",
  "group_id": 0
}
```

### DELETE /api/students/{student_id}
**Входные данные:**
- `student_id`: int (path parameter)

**Выходные данные:** нет (204 No Content)

