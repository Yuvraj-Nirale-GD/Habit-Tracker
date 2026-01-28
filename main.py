# """
# Project: Iron-Habit (Backend Core)
# Author: Yuvraj Nirale
# Status: Phase 1 (CLI & Logic)

# Description: 
#     The core logic engine for the Habit tracker. This script handles:
#     1. Database interactions (SQLite).
#     2. Input sanitization and validation.
#     3. Mathematical calculation of consistency scores.
    
#     NOTE: This is the precursor to the planned GUI version. 
# """

from datetime import date, datetime
import sqlite3

Db_habit = sqlite3.connect('habits.db')
cursor = Db_habit.cursor()
# cursor.execute(' DROP TABLE Daily_Log;'
# )
# Db_habit.commit
cursor.execute('''
               CREATE TABLE IF NOT EXISTS habits(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Task TEXT,
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

def  Create_Habit():
    start_date = date.today().strftime("%Y-%m-%d") # strftime to format date in YYYY-MM-DD
    
    while True:
        habit_name = input("Create a Task: ").strip().lower()

        if habit_name == '':
            print("Task cannot be empty")
            continue
        else:
            break
    Description = input("Enter Description for the Habit: ").strip()
    # Check if habit already exists
    cursor.execute('SELECT ID FROM habits WHERE task = ?',(habit_name,))

    existing_entry = cursor.fetchone() #if fetchone returns None, means no existing entry

    if existing_entry:
        print(f"You have already logged the habit '{habit_name}' ")
    else:
        cursor.execute('''
                       INSERT INTO habits(Task, Description, Creation_Date)
                       VALUES (?, ?, ?)''',(habit_name, Description, start_date))

        Db_habit.commit()
        print(f"Habit '{habit_name}' created successfully!")
    
     
def Daily_Log_Insert():
    today_date= date.today().strftime("%Y-%m-%d")

    cursor.execute('SELECT id, Task, Description FROM habits')
    habits = cursor.fetchall() # habit is tuple

    if not habits:
        print(f"There is no Task logged")
        return
        
    for habit in habits:
        habit_id, habit_name, dec = habit

        print(f"Task : {habit_name.upper()}\n Description = ({dec})")
        status = input(f"Did you complete '{habit_name}' today? (y/n): ").strip().lower()
        
        is_done = 1 if status == 'y' else 0
        effort = 0

        if is_done:
            while True:
                try:
                    effort = int(input("enter Eforts you've Put(0-10) :"))
                    if 0 <= effort <= 10:
                        break
                except ValueError : pass
        
        cursor.execute('''
                INSERT INTO Daily_Log(habit_id, date, status, efforts)
                VALUES (?,?,?,?)''', (habit_id, today_date, is_done, effort))
        Db_habit.commit()
        print(f"Task Logged Successfully")

def Analysis():
    cursor.execute('SELECT id, Task, Creation_Date FROM habits')
    habit = cursor.fetchall()

    for hbt in habit:
        h_id = hbt[0]
        name=hbt[1]
        crt_dt = hbt[2]

        start_date = datetime.strptime(crt_dt, "%Y-%m-%d").date() #coverting string from database back to date 
        days_passed = (date.today() - start_date).days + 1 # adding one for today

        cursor.execute('SELECT COUNT(*), AVG(efforts) FROM Daily_Log WHERE habit_id =? AND status =1', (h_id,))
        row = cursor.fetchone()
        totalCount= row[0]
        Average_effort = row[1] if row[1] else 0

    

        Consistancy = (totalCount/days_passed)*100

        print(f"Task: {name.upper()}")
        print(f"   Since: {start_date} ({days_passed} days ago)")
        print(f"   Done: {totalCount} times")
        print(f"   Consistency: {Consistancy:.1f}%")
        print(f"   Average Effort: {Average_effort:.1f}/10")

        if Consistancy < 50:
            print("you are not putting your all efforts")
        elif 50< Consistancy <70:
            print(" you can do more, why are you not pushing your limits")
        else:
            print(" congrats! You are above your other competitors")


while True:
    print("\n1: Create Task | 2: Daily Check | 3: Analysis | 4: Exit")
    try:
        choice = int(input("Choose Operation: "))
        if choice == 1: Create_Habit()
        elif choice == 2: Daily_Log_Insert()
        elif choice == 3: Analysis()
        elif choice == 4: break
        else: print("Invalid Input")
    except ValueError:
        print("Please enter a number.")