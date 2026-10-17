import unittest
from models import Planner, Homework, InvalidTaskError, TaskNotFoundError

class TestModels(unittest.TestCase):
    
    def setUp(self):
        """Подготовка данных перед каждым тестом."""
        self.planner = Planner()
        self.task1 = Homework("Тест 1", "2026-10-20")
        self.task2 = Homework("Тест 2", "2026-11-01")
        self.planner.add_task_to_course("Course A", self.task1)
        self.planner.add_task_to_course("Course B", self.task2)

    def test_search_existing_task(self):
        """Тесткейс №1: Поиск существующей задачи"""
        found = self.planner.find_task_by_title("Тест 1")
        self.assertEqual(found.title, "Тест 1")

    def test_search_nonexistent_task(self):
        """Тесткейс №2: Поиск несуществующей"""
        with self.assertRaises(TaskNotFoundError):
            self.planner.find_task_by_title("Ничего")

    def test_invalid_date(self):
        """Тесткейс №5: Неверная дата"""
        with self.assertRaises(InvalidTaskError):
            Homework("Плохая дата", "32.13.2026")

    def test_insertion_sort(self):
        """Тесткейс №7: Сортировка"""
        # task2 позже task1. Добавим task3, которая раньше всех.
        task3 = Homework("Тест 3", "2026-09-15")
        self.planner.add_task_to_course("Course A", task3)
        
        sorted_tasks = self.planner.get_all_tasks_sorted_by_deadline()
        # Ожидаемый порядок: Тест 3 (09-15), Тест 1 (10-20), Тест 2 (11-01)
        self.assertEqual(sorted_tasks[0].title, "Тест 3")
        self.assertEqual(sorted_tasks[1].title, "Тест 1")
        self.assertEqual(sorted_tasks[2].title, "Тест 2")

if __name__ == '__main__':
    unittest.main()