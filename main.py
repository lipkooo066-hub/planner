import logging
from models import Planner
from storage import load_from_csv, save_to_json, load_from_json
from ui import show_menu, display_tasks_sorted, search_task, change_task_status, display_priority_report
import os

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("planner.log", encoding='utf-8'),
        # Убираем StreamHandler, чтобы логи не засоряли консоль пользователя, пишем только в файл
    ]
)

def main():
    planner = Planner()
    state_file = "data/state.json"
    csv_file = "data/tasks.csv"

    # Создаем папку data, если её нет
    os.makedirs("data", exist_ok=True)

    # 1. Пытаемся восстановить состояние
    is_loaded = load_from_json(planner, state_file)
    
    # 2. Если сохранения нет, импортируем базовые данные из CSV
    if not is_loaded:
        if os.path.exists(csv_file):
            load_from_csv(planner, csv_file)
        else:
            print(f"Файл {csv_file} не найден. Работа с пустым списком.")

    # 3. Основной цикл программы
    while True:
        choice = show_menu()
        
        if choice == '1':
            display_tasks_sorted(planner)
        elif choice == '2':
            search_task(planner)
        elif choice == '3':
            change_task_status(planner)
        elif choice == '4':
            display_priority_report(planner)
        elif choice == '5':
            save_to_json(planner, state_file)
            print("Состояние сохранено. До свидания!")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()