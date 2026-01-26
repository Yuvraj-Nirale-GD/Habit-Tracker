"""
Project: Iron-Habit (Backend Core)
Author: Yuvraj Nirale
Status: Phase 1 (CLI & Logic)

Description: 
    The core logic engine for the Habit tracker. This script handles:
    1. Database interactions (SQLite).
    2. Input sanitization and validation.
    3. Mathematical calculation of consistency scores.
    
    NOTE: This is the precursor to the planned GUI version. 
"""

from datetime import date
import sqlite3

Db_habit = sqlite3.connect('habits.db')
cursor = Db_habit.cursor()
cursor.execute('''
               CREATE TABLE IF NOT EXISTS habits(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               date TEXT,
               task TEXT,
               status BOOL,
               efforts INTEGER)'''
            )
Db_habit.commit()
today_date = date.today().strftime("%Y-%m-%d") # strftime to format date in YYYY-MM-DD

while True:
    habit_name = input("Enter your Daily Habit (type 'exit' to stop): ").strip().lower()
    
    if habit_name == '':
        print("Task cannot be empty")
        continue

    if habit_name == 'exit':
        break

    elif habit_name == 'report':
        cursor.execute('''
                       SELECT task,
                       COUNT(*) AS total,
                       SUM(status) AS completed,
                       AVG(efforts) AS avg_effort
                       FROM habits
                       GROUP BY task
                       ''')
        
        report = cursor.fetchall()

        if not report:
            print('No habits logged yet.')
            continue
        else:
            print("\n--- Habit Report ---")
            for row in report:
                task_name = row[0]
                total = row[1]
                completed = row[2]  
                ave_effort = row[3]

                consistancy = (completed/total)*100 

                print(f"Habit: {task_name},\nConsistency: {consistancy:.1f}%,\nAverage Effort: {ave_effort:.1f}")
        
        if input("do you want to continue? (type yes to continue)").strip().lower() == 'yes':
            continue
        else:
            break
        
    cursor.execute('''
                   SELECT * FROM habits WHERE date = ? AND task = ?''',
                   (today_date, habit_name)
                   )
    existing_entry = cursor.fetchone() #if fetchone returns None, means no existing entry
    if existing_entry:
        print(f"You have already logged the habit '{habit_name}' for today.")
        continue            

    status = input(f"Did you complete '{habit_name}' today? (yes/no): ").strip().lower()
    efforts = 0
    if status == "yes": 
        while True:
            try:
                efforts = int(input(f"How much Effort did you put into completing '{habit_name}'? (1-10): "))
                if (1 <= efforts <= 10):
                    break
                else:
                    print("bruhh, Effort must be between 1 and 10.")
                    continue
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 10 for Effort.")

    cursor.execute('''
                   INSERT INTO habits (date, task, status, efforts)
                   VALUES (?, ?, ?, ?)''',
                   (today_date, habit_name, status == 'yes', efforts)# status == 'yes' converts to boolean, if it is no then False
                    )
    Db_habit.commit()
    print(f"Habit {habit_name} logged successfully!")