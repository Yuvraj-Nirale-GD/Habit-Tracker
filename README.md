# 🛡️ Iron-Habit: AI-Powered Habit Tracking Tool

## Overview

This web-based application, built with **Streamlit** and integrated with **Google Gemini AI**, quantifies your discipline and provides brutally honest feedback on your performance.

This project was created to understand file handling, database integration, AI integration & optimization, and basic application flow in Python.


## What it does

- **Logs Habits:** Saves daily tasks with an "Effort Level" (1-10).
- **Prevents Errors:** Logic checks to stop duplicate entries for the same day.
- **Saves Data:** Uses SQLite so data persists after the script closes.
- **Analytics:** The `report` command calculates consistency percentages and average intensity.


## Features

- **Daily Log:** Effort-based tracking (0-10 scale) to measure intensity, not just completion.
- **Smart "Upsert" Logic:** Log your habits at different times of the day; the engine updates existing entries or creates new ones automatically.
- **AI Performance Audit:** A "Brutally Honest Coach" persona (powered by Gemini 1.5 Flash) that analyzes your data and calls out slacking.
- **Persistence:** Relational SQLite storage ensuring your data stays local and secure.


## Tech Stack

- **Frontend:** Streamlit
- **Backend:** Python 3.x
- **Database:** SQLite3
- **Intelligence:** Google Gemini AI (Generative AI SDK)


## Project Structure

```text
.
├── main.py              # Main Application logic
├── .streamlit/
│   └── secrets.toml     # API Keys (Excluded from GitHub)
├── habits.db            # SQLite Database (Local only)
├── .gitignore           # Safety filter for sensitive files
└── README.md            # Documentation
```


### Daily Log Entry
-- ![Iron-Habit Interface](assets/HabitTracker-Daily_Log.jpg)

-- ![Iron-Habit Task Manager](assets/HabitTracker-TaskManager.png)

### AI in Action
![AI Analysis Demo](assets/HabitTracker-Analysis.gif)


## How to Run
1. Clone the repository
   ```bash
   git clone https://github.com/Yuvraj-Nirale-GD/Habit-Tracker.git
   ```
2. install Dependecies:
   ```
   pip install streamlit 
   pip install google-generativeai

   ```
3. Setup Secrets: Create .streamlit/secrets.toml
   ```secrets.toml

   AI_API_KEY = "your_gemini_api_key_here"
   ```
4. Run the Engine:
   ```
   streamlit run main.py
   ```
--Note: Database is created automatically on first run.



