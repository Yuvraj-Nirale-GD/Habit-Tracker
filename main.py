# """
# Project: Iron-Habit (Backend Core)
# Author: Yuvraj Nirale
# Status: Phase 1 (CLI & Logic)

# Description: 
#     The core logic engine for the Habit tracker. This script handles:
#     1. Database interactions (SQLite).
#     2. Input sanitization and validation.
#     
    
#     NOTE: This is the precursor to the planned GUI version. 
# """
from datetime import date, datetime
from DataBase import init_database, fetch_summary_data
from AIEngine import get_ai_review
import streamlit as st
import pandas as pd
import sqlite3



Db_habit = init_database()
cursor = Db_habit.cursor()

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

        habit_name = st.text_input("Create a Task: ").strip().lower()
        Description = st.text_input("Enter Description for the Habit: ")

        if st.form_submit_button("Create Task"):

        # Check if habit already exists
            if habit_name :
                cursor.execute('SELECT id FROM habits WHERE Task = ?',(habit_name,))
                if cursor.fetchone():
                    st.error("Task Already Exists!")
                else:
                    try:
                        cursor.execute('''
                                    INSERT INTO habits(Task, Description, Creation_Date)
                                    VALUES (?, ?, ?)''',(habit_name, Description, date.today().strftime("%Y-%m-%d")))

                        Db_habit.commit()
                        st.success(f"Habit '{habit_name}' created successfully!")
                        st.rurun()
                    except sqlite3.IntegrityError:
                        st.error(" Task Already Exists!")
            else:
                st.warning("Task name cannot be empty")
    st.divider()
    st.subheader("Delete Task")
    cursor.execute('SELECT id, Task FROM habits')
    all_tasks = cursor.fetchall()
    if not all_tasks:
        st.info("No Task to Delete")
    else:
        task_map = {task: t_id for t_id, task in all_tasks}
        task_to_delete = st.selectbox("Selects Task to Delete", list(task_map.keys()))
        st.warning(f"Are you sure you want to delete '{task_to_delete}'? This action cannot be undone.")
        
        if st.button(f"Delete {task_to_delete}", type = "secondary"):
            st.session_state["confirm_delete"] = True
            if st.session_state.get("confirm_delete"):
                st.error("Are you sure?")
                if st.button("Confirm",type= "primary"):


                    selected_id = task_map[task_to_delete]
                    try:
                        cursor.execute('DELETE FROM Daily_Log WHERE habit_id =?',(selected_id,))
                        cursor.execute('DELETE FROM habits WHERE id =?',(selected_id,))
                        Db_habit.commit()
                        st.success(f"{task_to_delete} deleted successfully")
                        st.rerun()


                    except Exception as e:
                        st.error(f"Failed to delete the Task: {e}")


with tab3:
    st.header("Trends")
    st.subheader("Over All Analysis")
    cursor.execute('''
                   Select date, AVG(efforts) FROM Daily_Log
                   GROUP BY date
                   ORDER BY  date ASC
                   LIMIT 30 ''')
    chart_Data = cursor.fetchall()
    if chart_Data:
        df = pd.DataFrame(chart_Data, columns= ['Date', 'Avg efforts'])
        df['Date'] = pd.to_datetime(df["Date"])
        df.set_index('Date', inplace=True)

        st.line_chart(df)
    else :
        st.info("Not enough data Present")

    st.divider()

    st.subheader("Task Analysis")
    cursor.execute("SELECT Task FROM habits")
    Tasks = [row[0] for row in cursor.fetchall()]

    if Tasks:
        selected_task = st.selectbox("Select Task :",Tasks)
   
        cursor.execute('''
                    SELECT date, efforts
                    FROM Daily_Log l
                    JOIN habits h ON l.habit_id = h.id
                    WHERE h.Task = ?
                    ''', (selected_task,))
        specific_Data = cursor.fetchall()
        if specific_Data:
            specific_df = pd.DataFrame(specific_Data, columns = ('Date', 'Efforts'))
            specific_df['Date'] = pd.to_datetime(specific_df['Date'])
            specific_df.set_index('Date',  inplace= True)

            st.scatter_chart(specific_df)
        else :
            st.info("Nothing to See here ")
    else:
        st.error("Empty table")


    st.divider()
    st.header("Performance Analysis")
    summary_results = fetch_summary_data(cursor)
    report_txt =""
    if not summary_results:
        st.info("There is nothing to see")
    else:
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