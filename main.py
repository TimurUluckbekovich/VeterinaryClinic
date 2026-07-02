import database
import crud
from models import Dog, Cat, Pet


def admin_menu():
    while True:
        print("\n--- РЕЖИМ АДМИНИСТРАТОРА ---")
        print("1. Добавить нового питомца")
        print("2. Редактировать данные питомца")
        print("3. Удалить питомца")
        print("4. Добавить нового врача")
        print("5. Просмотреть сводную статистику клиники")
        print("6. Вернуться в главное меню")

        choice = input("Выберите действие: ")

        if choice == "1":
            name = input("Имя питомца: ")
            species = input("Вид животного (например, Собака/Кот): ")
            age = int(input("Возраст питомца: "))
            owner_id = input("ID владельца (нажмите Enter, если нет): ")
            owner_id = int(owner_id) if owner_id else None

            crud.create_pet(name, species, age, owner_id)
            print(" Питомец успешно зарегистрирован!")

        elif choice == "2":
            pet_id = int(input("Введите ID питомца для редактирования: "))
            name = input("Новое имя: ")
            species = input("Новый вид: ")
            age = int(input("Новый возраст: "))
            owner_id = input("Новый ID владельца (нажмите Enter для пропуска): ")
            owner_id = int(owner_id) if owner_id else None

            crud.update_pet(pet_id, name, species, age, owner_id)
            print(" Данные питомца успешно обновлены!")

        elif choice == "3":
            pet_id = int(input("Введите ID питомца для удаления: "))
            crud.delete_pet(pet_id)
            print(" Питомец удален из системы.")

        elif choice == "4":
            full_name = input("ФИО врача: ")
            specialization = input("Специализация: ")
            crud.create_doctor(full_name, specialization)
            print(" Вруч успешно добавлен в штат!")

        elif choice == "5":
            print("\n=== АНАЛИТИКА КЛИНИКИ ===")
            agg = crud.get_clinic_aggregates()
            print(f"Общее количество пациентов: {agg['total_pets']}")
            print(f"Средний возраст: {agg['avg_age']} лет")
            print(f"Возрастной диапазон: от {agg['min_age']} до {agg['max_age']} лет")

            print("\n[GROUP BY] Популяция по видам:")
            for species, count in crud.get_species_stats():
                print(f" - {species}: {count}")

            print("\n[Вложенный запрос] Востребованные врачи (приёмов выше среднего):")
            for doc_name, count in crud.get_top_doctors():
                print(f" * {doc_name} (Всего визитов: {count})")

            print("\n[VIEW] Последние записи из clinic_statistics:")
            for row in crud.get_clinic_statistics_view():
                print(
                    f" Пациент: {row[0]} | Владелец: {row[1]} | Доктор: {row[2]} | Визитов: {row[3]} | Диагноз: {row[4]}")

        elif choice == "6":
            break


def owner_menu():
    while True:
        print("\n--- РЕЖИМ ВЛАДЕЛЬЦА ---")
        print("1. Посмотреть список всех питомцев клиники")
        print("2. Записать питомца на приём к врачу")
        print("3. Просмотреть медицинскую историю питомца")
        print("4. Вернуться в главное меню")

        choice = input("Выберите действие: ")

        if choice == "1":
            print("\nПациенты нашей клиники:")
            pets = crud.get_all_pets()
            for p in pets:
                print(f"ID: {p.get_id()} | {p.show_info()} | Статус: {p.get_vaccination_status()}")
                if p.species.lower() == "собака":
                    print(f"   Голос: {Dog.make_sound(p)}")
                elif p.species.lower() == "кот":
                    print(f"   Голос: {Cat.make_sound(p)}")

        elif choice == "2":
            pet_id = int(input("Введите ID вашего питомца: "))
            doc_id = int(input("Введите ID врача: "))
            visit_date = input("Введите дату (ГГГГ-ММ-ДД): ")
            diagnosis = input("Укажите причину обращения / диагноз: ")

            crud.create_appointment(pet_id, doc_id, visit_date, diagnosis)
            print(" Запись на приём успешно зафиксирована!")

        elif choice == "3":
            pet_id = int(input("Введите ID питомца для выгрузки карты: "))
            print(f"\n=== КАРТА ПАЦИЕНТА ID {pet_id} ===")
            history = crud.get_pet_medical_history(pet_id)
            if not history:
                print("История посещений чиста.")
            for row in history:
                print(f"Дата: {row[1]} | Доктор: {row[2]} | Диагноз: {row[3]}")

        elif choice == "4":
            break


def main():
    database.create_tables()
    while True:
        print("\n=====================================")
        print(" СИСТЕМА ВЕТЕРИНАРНОЙ КЛИНИКИ ")
        print("=====================================")
        print("1. Войти как Администратор")
        print("2. Войти как Владелец")
        print("3. Выйти из приложения")

        role = input("Выберите роль для авторизации: ")

        if role == "1":
            admin_menu()
        elif role == "2":
            owner_menu()
        elif role == "3":
            print("Работа завершена. До встречи!")
            break


if __name__ == "__main__":
    main()