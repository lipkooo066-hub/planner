from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict, Optional

# --- Кастомные исключения ---
class InvalidTaskError(Exception):
    """Выбрасывается, если данные задачи некорректны."""
    pass

class TaskNotFoundError(Exception):
    """Выбрасывается, если задача не найдена."""
    pass

# --- Dataclass для отчетов ---
@dataclass
class ReportRow:
    """Используем dataclass для удобного хранения строк отчета."""
    course_name: str
    task_title: str
    deadline: str
    priority: int

# --- Иерархия задач (Полиморфизм и Наследование) ---
class Task:
    """Базовый класс для всех задач. Не инстанцируется напрямую."""
    def __init__(self, title: str, deadline: str, status: str = "new"):
        self.title = title
        self.deadline = deadline
        self.status = status

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        if not value or not value.strip():
            raise InvalidTaskError("Название задачи не может быть пустым.")
        self._title = value.strip()

    @property
    def deadline(self) -> str:
        return self._deadline

    @deadline.setter
    def deadline(self, value: str):
        # Проверяем формат даты
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise InvalidTaskError(f"Неверный формат даты: {value}. Ожидается YYYY-MM-DD.")
        self._deadline = value

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str):
        allowed_statuses = {"new", "in_progress", "done"}
        if value not in allowed_statuses:
            raise InvalidTaskError(f"Недопустимый статус: {value}. Разрешены: {allowed_statuses}")
        self._status = value

    def priority(self) -> int:
        """Метод для демонстрации полиморфизма. Переопределяется в наследниках."""
        raise NotImplementedError("Метод должен быть реализован в подклассах")

# Наследование: "Домашнее задание ЯВЛЯЕТСЯ Задачей"
class Homework(Task):
    def priority(self) -> int:
        return 2  # Обычный приоритет

# Наследование: "Экзамен ЯВЛЯЕТСЯ Задачей"
class Exam(Task):
    def priority(self) -> int:
        return 1  # Наивысший приоритет, экзамены важнее

# --- Композиция: Предмет содержит Задачи ---
class Course:
    def __init__(self, name: str):
        if not name.strip():
            raise ValueError("Имя курса не может быть пустым")
        self.name = name
        self.tasks: List[Task] = [] # list для хранения порядка задач

    def add_task(self, task: Task):
        self.tasks.append(task)

# --- Композиция: Планировщик содержит Предметы ---
class Planner:
    def __init__(self):
        # dict для быстрого поиска курса по названию (Сложность O(1))
        self.courses: Dict[str, Course] = {}
        # set для уникальных названий курсов (если потребуется вывести список)
        self.course_names = set()

    def add_course(self, name: str) -> Course:
        if name not in self.courses:
            self.courses[name] = Course(name)
            self.course_names.add(name)
        return self.courses[name]

    def add_task_to_course(self, course_name: str, task: Task):
        course = self.add_course(course_name)
        course.add_task(task)

    # --- Свой алгоритм поиска (Линейный поиск - O(n)) ---
    def find_task_by_title(self, title: str) -> Task:
        """
        Линейный поиск задачи по всем курсам.
        Сложность O(n), так как мы проверяем каждый элемент по очереди.
        Предусловие: список не обязан быть отсортирован.
        """
        for course in self.courses.values():
            for task in course.tasks:
                if task.title == title:
                    return task
        raise TaskNotFoundError(f"Задача '{title}' не найдена.")

    # --- Свой алгоритм сортировки (Сортировка вставками - O(n^2)) ---
    def get_all_tasks_sorted_by_deadline(self) -> List[Task]:
        """
        Собирает все задачи и сортирует их по дедлайну алгоритмом вставок.
        Встроенные sorted() или .sort() здесь не используются по условию.
        Сложность O(n^2).
        """
        # Собираем все задачи в один список
        all_tasks = []
        for course in self.courses.values():
            all_tasks.extend(course.tasks)
            
        # Сортировка вставками
        for i in range(1, len(all_tasks)):
            key_task = all_tasks[i]
            j = i - 1
            # Сравниваем строковые представления дат (формат YYYY-MM-DD позволяет это делать)
            while j >= 0 and all_tasks[j].deadline > key_task.deadline:
                all_tasks[j + 1] = all_tasks[j]
                j -= 1
            all_tasks[j + 1] = key_task
            
        return all_tasks