# Habit Tracker (CLI)

A Python tool to track daily habits and calculate consistency. 

I built this because I needed a way to track Our daily habits and studies without using complex apps that sell my data. The goal is to build the core logic here first, then add a UI and AI analysis later.

## What it does
- **Logs Habits:** Saves daily tasks with an "Effort Level" (1-10).
- **Prevents Errors:** Logic checks to stop duplicate entries for the same day.
- **Saves Data:** Uses SQLite so data persists after the script closes.
- **Analytics:** The `report` command calculates consistency percentages and average intensity.

## How to run it
1. Clone this repo.
2. Run the script:
   ```bash
   python main.py