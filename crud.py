import sqlite3
from database import connect_db
from models import Doctor

def create_doctor(full_name: str, specialization: str):
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO doctor (full_name, specialization) VALUES (?, ?)",
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


def create_appointments(pet_id: int, doctor_id: int, visit_date: str,  diagnosis: str):
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO appointments (pet_id, doctor_id, visit_date, diagnosis) VALUES (?, ?, ?, ?",
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
            SELECT a.id, a.visit_date, d.full_name, d.diagnosis
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
