import sqlite3

DB_NAME = "clinic.db"

def connect_db():
    connection = sqlite3.connect(DB_NAME)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection

def create_tables():
    connection = connect_db()

    try:
        cursor = connection.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS owners (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                phone TEXT NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS doctors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                specialization TEXT NOT NULL   
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                species TEXT NOT NULL,
                age INTEGER NOT NULL,
                owner_id INTEGER,
                FOREIGN KEY(owner_id) REFERENCES owners(id) ON DELETE CASCADE
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pet_id INTEGER,
                doctor_id INTEGER,
                visit_date TEXT NOT NULL,
                diagnosis TEXT NOT NULL,
                FOREIGN KEY(pet_id) REFERENCES pets(id) ON DELETE CASCADE,
                FOREIGN KEY(doctor_id) REFERENCES doctors(id) ON DELETE CASCADE
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS  clinic_statistics AS
            SELECT
                p.name AS pet_name,
                o.full_name AS owner_name,
                d.full_name AS doctor_name,
                (SELECT COUNT(*) FROM appointments a WHERE a.pet_id = p.id) AS visit_count,
                (SELECT a.diagnosis FROM appointments a WHERE a.pet_id = p.id ORDER BY a.visit_date DESC LIMIT 1) AS last_diagnosis
            FROM pets p
            LEFT JOIN owners o ON p.owner_id = o.id
            LEFT JOIN appointments app ON p.id = app.pet_id
            LEFT JOIN doctors d ON app.doctor_id = d.id
            GROUP BY p.id
        ''')

        connection.commit()

    except sqlite3.Error as e:
        print(f"[Ошибка БД] Не удалось создать таблицы: {e}")
    finally:
        connection.close()

if __name__ == '__main__':
    create_tables()
