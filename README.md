# Habit Tracker (CLI)

## Overview
Habit Tracker is a simple application built using Python and SQLite that helps users track daily habits and maintain consistency over time.

This project was created to understand file handling, database integration, and basic application flow in Python.

I built this because I needed a way to track Our daily habits and studies without using complex apps that sell my data. The goal is to build the core logic here first, then add a UI and AI analysis later.

## What it does
- **Logs Habits:** Saves daily tasks with an "Effort Level" (1-10).
- **Prevents Errors:** Logic checks to stop duplicate entries for the same day.
- **Saves Data:** Uses SQLite so data persists after the script closes.
- **Analytics:** The `report` command calculates consistency percentages and average intensity.

## Features
- Add new habits
- Mark habits as completed
- Store habit data persistently using SQLite
- View habit completion history

## Tech Stack
- Python
- SQLite
- Command Line Interface (CLI)

## Project Structure
- `main.py` – Application entry point
- `database.py` – Handles SQLite database operations
- `habits.db` – Local database file

## How to Run
1. Clone the repository
   ```bash
   git clone https://github.com/Yuvraj-Nirale-GD/Habit-Tracker.git
   ```
2. Nevigate to the project Directory
   ```cd Habit-Tracker
   ```
3. Run the Appication
   ```python main.py
   ```

