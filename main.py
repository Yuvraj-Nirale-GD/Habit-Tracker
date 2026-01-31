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
import streamlit as st
from datetime import date, datetime
import sqlite3
import google.generativeai as gemini
try:
    api_key = st.secrets["AI_API_KEY"]
    gemini.configure(api_key = api_key)
    model = gemini.GenerativeModel('gemini-2.5-flash')
except KeyError:
    st.error("API key not found, Add it to your Secrets.")


def get_ai_review(data_summary):
    prompt = f"""
    You are an Teacher and mentor, and coach.
    You are brutally honest, no-sugarcoated analyst.
    Analyze the following habit tracking data for the user.
    If the Consistency is low, call out his laziness.
    if the efforts are low even when Done is checked, call it out.
    provide actionable, hard-hitting feedback.
    
    Data : {data_summary}
    """
    response = model.generate_content(prompt)
    return response.text

def get_db_connection():
    return sqlite3.connect('habits.db', check_same_thread = False)

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

st.set_page_config(page_title= "Iron-Habit", layout= "wide")
st.title("Iron Habit Tracker")

tab1, tab2 , tab3 = st.tabs(["Daily Log", "Manage Task", "Analysis"])

with tab1:
    st.header("Daily Log")
    cursor.execute('SELECT id, Task, Description FROM habits')
    habits = cursor.fetchall() # store all the data fetched in habits as a tuple

    if not habits:
        st.info(f"There is no Task logged")
    else :
        with st.form("Daily_Checklist_form"):
            for h_id, h_name, h_desc in habits:
                col1, col2, col3 = st.columns([2, 1, 2])
                with col1:
                    st.subheader(f"Task : {h_name.upper()}")
                    st.caption(h_desc)
                with col2:
                    st.checkbox(f"Done :", key = f"status_{h_id}")
                with col3:
                    st.slider("Select your Efforts :",0 , 10 , 2, key = f"effort_{h_id}")
                st.divider() 
            
            if st.form_submit_button("Submit Logs"):
                today_date = date.today().strftime("%Y-%m-%d")
            
                for h_id, h_name, _ in habits:
                    
                    is_done_val = st.session_state[f"status_{h_id}"] # Geting all values directly from session_state
                    effort_val = st.session_state[f"effort_{h_id}"]
                    
                    # Check if this specific habit was already logged today
                    cursor.execute('''
                                   INSERT OR REPLACE INTO Daily_Log (habit_id, date, status, efforts) 
                                   VALUES (?, ?, ?, ?)''',(h_id, today_date, is_done_val, effort_val))
                                   
                Db_habit.commit()
                
                st.success(f"Successfully updated")


with tab2:
    st.header("Add new Task")    
    with st.form("Create_New_Task"):

        habit_name = st.text_input(("Create a Task: ").strip().lower())
        Description = st.text_input("Enter Description for the Habit: ")

        if st.form_submit_button("Create Task"):

        # Check if habit already exists
            if habit_name :
                try:
                    cursor.execute('''
                                INSERT INTO habits(Task, Description, Creation_Date)
                                VALUES (?, ?, ?)''',(habit_name, Description, date.today().strftime("%Y-%m-%d")))

                    Db_habit.commit()
                    st.success(f"Habit '{habit_name}' created successfully!")
                except sqlite3.IntegrityError:
                    st.error(" Task Already Exists!")
            else:
                st.warning("Task name cannot be empty")

with tab3:
    st.header("Performance Analysis")
    cursor.execute('''
                   SELECT h.Task, COUNT(l.id),AVG(l.efforts)
                   FROM habits h
                   LEFT JOIN Daily_Log l ON h.id = l.habit_id AND l.status = 1
                   GROUP BY h.id
                   ''')
    summary_results = cursor.fetchall()

    report_txt =""
    for task, count, avg_efforts in summary_results:
        Avg_efforts_str = f"{avg_efforts:.1f}" if avg_efforts else "0.0"
        st.metric(label=task.upper(), value = f"{count} days", delta = f"Average Efforts : {Avg_efforts_str}")
        report_txt += f"Task : {task}, Completed: {count} times, Average Efforts : {Avg_efforts_str}\n"

    st.divider()
    if st.button("Get Your Analyzed Report"):
        with st.spinner(" Getting Your Feedback From AI"):
            try:
                feedback = get_ai_review(report_txt)
                st.markdown(f"### FeedBack\n{feedback}")
            except Exception as e :
                st.error(f"AI faild to Respond. error in Code:{e}")