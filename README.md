# Dynamic Equity Engine ⚖️

A lightweight, transparent web application built with **Python**, **Flask**, and **Git** to calculate, track, and visualize team equity dynamically based on actual contribution metrics.

## 🚀 Features
* **Automated Git Sync:** Instantly parses local Git history (`git shortlog`) to pull accurate commit counts.
* **Weighted Scoring Algorithm:** Computes total contribution points using configurable metrics:
  * Commits: `2 points`
  * Pull Requests: `10 points`
  * Tasks Completed: `5 points`
* **Live Visual Progress Bars:** Renders real-time equity percentage shares dynamically.
* **Full Administrative Control:** Add, update, or remove team members seamlessly with instant deletion controls.
* **JSON Persistence:** Lightweight decoupled local data storage (`data.json`).

## 🛠️ Tech Stack
* **Backend:** Python, Flask
* **Frontend:** HTML5, CSS3, Jinja2 Templates
* **Version Control:** Git

## ⚙️ Quick Start (Local Setup)

1. Clone or open the repository locally:
   ```bash
   cd dynamic-equity-engine
2. python3 -m venv venv
source venv/bin/activate
3. pip install -r requirements.txt
python3 app.py
4. Open your browser and navigate to: http://127.0.0.1:5000