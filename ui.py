from models import Planner, TaskNotFoundError, ReportRow
import logging

def show_menu():
    print("\n--- Планировщик сессии ---")
    print("1. Показать все задачи (отсортированные по дедлайну)")
    print("2. Найти задачу по названию")
    print("3. Изменить статус задачи")
    print("4. Отчет по приоритетам")
    print("5. Выход и сохранение")
    return input("Выберите действие: ")

def display_tasks_sorted(planner: Planner):
    print("\n--- Задачи (Сортировка вставками по дате) ---")
    tasks = planner.get_all_tasks_sorted_by_deadline()
    if not tasks:
        print("Задач нет.")
        return
    for task in tasks:
        # Здесь проявляется полиморфизм: priority() вызывается у абстрактного Task
        print(f"[{task.deadline}] {task.title} (Статус: {task.status}, Приоритет: {task.priority()})")

def search_task(planner: Planner):
    title = input("Введите название задачи: ")
    try:
        task = planner.find_task_by_title(title)
        print(f"\nЗадача найдена: {task.title}")
        print(f"Дедлайн: {task.deadline}, Статус: {task.status}")
    except TaskNotFoundError as e:
        print(f"\nОшибка: {e}")
        logging.warning(f"Поиск несуществующей задачи: {title}")

def change_task_status(planner: Planner):
    title = input("Введите название задачи для изменения: ")
    try:
        task = planner.find_task_by_title(title)
        print("Доступные статусы: new, in_progress, done")
        new_status = input("Введите новый статус: ")
        task.status = new_status # Тут отработает валидация property
        print("Статус успешно изменен!")
        logging.info(f"Изменен статус задачи '{title}' на '{new_status}'")
    except TaskNotFoundError:
        print("Задача не найдена.")
    except Exception as e:
        print(f"Ошибка: {e}")

def display_priority_report(planner: Planner):
    print("\n--- Отчет: Самые приоритетные задачи (Экзамены) ---")
    reports = []
    for course_name, course in planner.courses.items():
        for task in course.tasks:
            if task.priority() == 1: # 1 - Наивысший приоритет (Экзамены)
                # Используем dataclass для создания строки отчета
                row = ReportRow(course_name, task.title, task.deadline, task.priority())
                reports.append(row)
    
    if not reports:
        print("Приоритетных задач (экзаменов) нет.")
    else:
        for r in reports:
            print(f"Курс: {r.course_name} | Экзамен: {r.task_title} | Дедлайн: {r.deadline}")