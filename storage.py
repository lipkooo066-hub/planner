import csv
import json
import logging
from typing import Generator
from models import Planner, Homework, Exam, InvalidTaskError

# Настройка логирования
logger = logging.getLogger(__name__)

def read_csv_generator(filepath: str) -> Generator[dict, None, None]:
    """
    Генератор для построчного чтения CSV.
    Преимущество: не загружает весь файл в память, читает по одной строке.
    """
    try:
        with open(filepath, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                yield row
    except FileNotFoundError:
        logger.error(f"Файл {filepath} не найден.")
        raise
    except Exception as e:
        logger.error(f"Ошибка при чтении CSV: {e}")
        raise

def load_from_csv(planner: Planner, filepath: str):
    """Читает данные из CSV через генератор и заполняет планировщик."""
    logger.info(f"Начало загрузки данных из {filepath}")
    loaded_count = 0
    for row in read_csv_generator(filepath):
        try:
            course_name = row.get('course', 'Unknown')
            title = row['title']
            task_type = row['type']
            deadline = row['deadline']
            status = row.get('status', 'new')

            if task_type == 'homework':
                task = Homework(title, deadline, status)
            elif task_type == 'exam':
                task = Exam(title, deadline, status)
            else:
                logger.warning(f"Неизвестный тип задачи: {task_type}. Пропуск строки.")
                continue

            planner.add_task_to_course(course_name, task)
            loaded_count += 1
            logger.debug(f"Задача '{title}' успешно загружена.")
        except InvalidTaskError as e:
            # Ловим наши кастомные исключения валидации
            logger.error(f"Ошибка валидации задачи '{row.get('title', 'Unknown')}': {e}")
        except KeyError as e:
            logger.error(f"В CSV отсутствует обязательная колонка: {e}")
            
    logger.info(f"Загрузка завершена. Успешно загружено задач: {loaded_count}")

def save_to_json(planner: Planner, filepath: str):
    """Сохраняет текущее состояние планировщика в JSON."""
    data = {"courses": []}
    for course in planner.courses.values():
        course_data = {"name": course.name, "tasks": []}
        for task in course.tasks:
            task_type = "homework" if isinstance(task, Homework) else "exam"
            course_data["tasks"].append({
                "title": task.title,
                "type": task_type,
                "deadline": task.deadline,
                "status": task.status
            })
        data["courses"].append(course_data)

    try:
        with open(filepath, mode='w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        logger.info(f"Состояние успешно сохранено в {filepath}")
    except Exception as e:
        logger.error(f"Ошибка при сохранении JSON: {e}")

def load_from_json(planner: Planner, filepath: str) -> bool:
    """Загружает состояние из JSON (если файл существует)."""
    try:
        with open(filepath, mode='r', encoding='utf-8') as file:
            data = json.load(file)
            for course_data in data.get("courses", []):
                course_name = course_data["name"]
                for task_data in course_data.get("tasks", []):
                    task_type = task_data["type"]
                    if task_type == "homework":
                        task = Homework(task_data["title"], task_data["deadline"], task_data["status"])
                    else:
                        task = Exam(task_data["title"], task_data["deadline"], task_data["status"])
                    planner.add_task_to_course(course_name, task)
        logger.info(f"Состояние восстановлено из {filepath}")
        return True
    except FileNotFoundError:
        logger.info(f"Файл сохранения {filepath} не найден. Начинаем с чистого листа.")
        return False
    except Exception as e:
        logger.error(f"Ошибка при загрузке состояния из JSON: {e}")
        return False