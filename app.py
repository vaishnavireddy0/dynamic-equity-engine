import json
import subprocess
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def calculate_contribution(commits, pull_requests, tasks_completed):
    return (commits * 2) + (pull_requests * 10) + (tasks_completed * 5)

def get_git_commits():
    """Automatically counts commits from the local Git repository"""
    try:
        result = subprocess.run(
            ["git", "shortlog", "-sn", "HEAD"], 
            capture_output=True, text=True, check=True
        )
        git_data = {}
        for line in result.stdout.strip().split("\n"):
            if line:
                parts = line.strip().split("\t")
                if len(parts) == 2:
                    count, name = int(parts[0]), parts[1]
                    git_data[name] = count
        return git_data
    except Exception:
        return {}

@app.route("/", methods=["GET", "POST"])
def dashboard():
    if request.method == "POST":
        action = request.form.get("action")
        
        with open("data.json", "r") as f:
            team_members = json.load(f)

        if action == "sync_git":
            git_commits = get_git_commits()
            for name, commits in git_commits.items():
                if name in team_members:
                    team_members[name]["commits"] = commits
                else:
                    team_members[name] = {"commits": commits, "pull_requests": 0, "tasks_completed": 0}

        elif action == "manual_add":
            name = request.form.get("name")
            commits = int(request.form.get("commits", 0))
            pull_requests = int(request.form.get("pull_requests", 0))
            tasks_completed = int(request.form.get("tasks_completed", 0))

            if name:
                team_members[name] = {
                    "commits": commits,
                    "pull_requests": pull_requests,
                    "tasks_completed": tasks_completed
                }

        elif action == "delete":
            name_to_delete = request.form.get("name")
            if name_to_delete in team_members:
                del team_members[name_to_delete]

        with open("data.json", "w") as f:
            json.dump(team_members, f, indent=4)

        return redirect(url_for("dashboard"))

    with open("data.json", "r") as f:
        team_members = json.load(f)

    scores = {}
    for name, stats in team_members.items():
        scores[name] = calculate_contribution(
            stats["commits"], stats["pull_requests"], stats["tasks_completed"]
        )

    total_points = sum(scores.values())
    
    breakdown = []
    for name, score in scores.items():
        equity = (score / total_points) * 100 if total_points > 0 else 0
        breakdown.append({"name": name, "score": score, "equity": round(equity, 1)})

    breakdown = sorted(breakdown, key=lambda x: x["equity"], reverse=True)

    return render_template("index.html", breakdown=breakdown)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)