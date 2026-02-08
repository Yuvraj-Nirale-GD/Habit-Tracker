import sqlite3
def get_db_connection():
    return sqlite3.connect('habits.db', check_same_thread = False)

def init_database():
    Db_habit = get_db_connection()
    cursor = Db_habit.cursor()
    # cursor.execute(' DROP TABLE Daily_Log;'
    # )
    # Db_habit.commit
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS habits(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Task TEXT UNIQUE,
                    Description TEXT,
                    Creation_Date TEXT
                )'''
                )
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS Daily_Log(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER,
                date TEXT,
                Status BOOLEAN,
                efforts INTEGER,
                FOREIGN KEY (habit_id) REFERENCES habits(id)
                )'''
                )
    Db_habit.commit()
    return Db_habit
def fetch_summary_data(cursor):
    cursor.execute('''SELECT h.Task, COUNT(l.id), AVG(l.efforts)
                      FROM habits h
                      LEFT JOIN Daily_Log l ON h.id = l.habit_id AND l.status = 1
                      GROUP BY h.id''')
    return cursor.fetchall()