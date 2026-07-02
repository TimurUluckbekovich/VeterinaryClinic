import sqlite3
from database import connect_db
from models import Doctor, Pet

def create_doctor(full_name: str, specialization: str):
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO doctors (full_name, specialization) VALUES (?, ?)",
            (full_name, specialization),
        )
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"[Ошибка CRUD] Не удалось добавить врача: {e}")
        return None
    finally:
        conn.close()

def get_doctor_by_id(doctor_id: int):
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, full_name, specialization FROM doctors WHERE id = ?", (doctor_id,))
        row = cursor.fetchone()
        return Doctor.from_db(row) if row else None
    except sqlite3.Error as e:
        print(f"[Ошибка CRUD] Не удалось получить данные врача: {e}")
        return None
    finally:
        conn.close()

def get_all_doctors():
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, full_name, specialization FROM doctors")
        rows = cursor.fetchall()
        return [Doctor.from_db(row) for row in rows]
    except sqlite3.Error as e:
        print(f"[Ошибка CRUD] Не удалось получить список врачей: {e}")
        return []
    finally:
        conn.close()

def update_doctor(doctor_id: int, full_name: str, specialization: str):
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE doctors SET full_name = ?, specialization = ? WHERE id = ?",
            (full_name, specialization, doctor_id)
        )
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"[Ошибка CRUD] Не удалось обновить данные врача: {e}")
        return False
    finally:
        conn.close()


def delete_doctor(doctor_id: int):
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM doctors WHERE id = ?", (doctor_id,))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"[Ошибка CRUD] Не удалось удалить врача: {e}")
        return False
    finally:
        conn.close()


def create_appointment(pet_id: int, doctor_id: int, visit_date: str,  diagnosis: str):
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO appointments (pet_id, doctor_id, visit_date, diagnosis) VALUES (?, ?, ?, ?)",
            (pet_id, doctor_id, visit_date, diagnosis)
        )
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"[Ошибка CRUD] Не удалось записать питомца на приём: {e}")
        return None
    finally:
        conn.close()

def get_pet_medical_history(pet_id: int):
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT a.id, a.visit_date, d.full_name, a.diagnosis
            FROM appointments a
            JOIN doctors d ON a.doctor_id = d.id
            WHERE a.pet_id = ?
            ORDER BY a.visit_date DESC
        ''', (pet_id,))
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"[Ошибка CRUD] Не удалось загрузить историю приёмов: {e}")
        return []
    finally:
        conn.close()


def create_pet(name: str, species: str, age: int, owner_id: int = None):
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO pets (name, species, age, owner_id) VALUES (?, ?, ?, ?)",
            (name, species, age, owner_id)
        )
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"[Ошибка CRUD] Не удалось добавить питомца: {e}")
        return None
    finally:
        conn.close()


def get_pet_by_id(pet_id: int):
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, species, age, owner_id FROM pets WHERE id = ?", (pet_id,))
        row = cursor.fetchone()
        return Pet.from_db(row) if row else None
    except sqlite3.Error as e:
        print(f"[Ошибка CRUD] Не удалось получить данные питомца: {e}")
        return None
    finally:
        conn.close()

def get_all_pets():
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, species, age, owner_id FROM pets")
        rows = cursor.fetchall()
        return [Pet.from_db(row) for row in rows]
    except sqlite3.Error as e:
        print(f"[Ошибка CRUD] Не удалось получить список питомцев: {e}")
        return []
    finally:
        conn.close()


def update_pet(pet_id: int, name: str, species: str, age: int, owner_id: int = None):
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE pets SET name = ?, species = ?, age = ?, owner_id = ? WHERE id = ?",
            (name, species, age, owner_id, pet_id)
        )
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"[Ошибка CRUD] Не удалось обновить данные питомца: {e}")
        return False
    finally:
        conn.close()


def delete_pet(pet_id: int):
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM pets WHERE id = ?", (pet_id,))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"[Ошибка CRUD] Не удалось удалить питомца: {e}")
        return False
    finally:
        conn.close()

def get_clinic_aggregates():
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(id), AVG(age), MIN(age), MAX(age) FROM pets")
        row = cursor.fetchone()
        if row and row[0] > 0:
            return {
                "total_pets": row[0],
                "avg_age": round(row[1], 1),
                "min_age": row[2],
                "max_age": row[3]
            }
        return {"total_pets": 0, "avg_age": 0, "min_age": 0, "max_age": 0}
    except sqlite3.Error as e:
        print(f"[Ошибка статистики] Не удалось посчитать агрегаты: {e}")
        return None
    finally:
        conn.close()


def get_species_stats():
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT species, COUNT(id) FROM pets GROUP BY species")
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"[Ошибка статистики] Не удалось сгруппировать по видам: {e}")
        return []
    finally:
        conn.close()


def get_top_doctors():
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT d.full_name, COUNT(a.id) AS app_count
            FROM doctors d
            LEFT JOIN appointments a ON d.id = a.doctor_id
            GROUP BY d.id
            HAVING app_count > (
                SELECT AVG(cnt)
                FROM (SELECT COUNT(*) AS cnt FROM appointments GROUP BY doctor_id)
            )
        ''')
    except sqlite3.Error as e:
        print(f"[Ошибка статистики] Не удалось выполнить сложный запрос по врачам: {e}")
        return []
    finally:
        conn.close()

def get_clinic_statistics_view():
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT pet_name, owner_name, doctor_name, visit_count, last_diagnosis FROM clinic_statistics")
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"[Ошибка статистики] Не удалось прочитать VIEW: {e}")
        return []
    finally:
        conn.close()