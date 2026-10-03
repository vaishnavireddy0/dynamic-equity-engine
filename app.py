import json
import subprocess
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

def calculate_contribution(commits, pull_requests, tasks_completed):
    return (commits * 2) + (pull_requests * 10) + (tasks_completed * 5)

def get_git_commits():
    """Automatically counts commits from the local Git repository"""
    try:
        # Runs 'git shortlog -sn' to get author names and commit counts
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
        
        if action == "sync_git":
            git_commits = get_git_commits()
            with open("data.json", "r") as f:
                team_members = json.load(f)
            
            # Update commit counts for anyone matching git authors
            for name, commits in git_commits.items():
                if name in team_members:
                    team_members[name]["commits"] = commits
                else:
                    # Add new git author automatically
                    team_members[name] = {"commits": commits, "pull_requests": 0, "tasks_completed": 0}

            with open("data.json", "w") as f:
                json.dump(team_members, f, indent=4)

        elif action == "manual_add":
            name = request.form.get("name")
            commits = int(request.form.get("commits", 0))
            pull_requests = int(request.form.get("pull_requests", 0))
            tasks_completed = int(request.form.get("tasks_completed", 0))

            if name:
                with open("data.json", "r") as f:
                    team_members = json.load(f)
                
                team_members[name] = {
                    "commits": commits,
                    "pull_requests": pull_requests,
                    "tasks_completed": tasks_completed
                }

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

    # Sort breakdown by highest equity first
    breakdown = sorted(breakdown, key=lambda x: x["equity"], reverse=True)

    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dynamic Equity Engine</title>
        <style>
            body { font-family: -apple-system, sans-serif; background: #0f172a; color: #f8fafc; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
            .card { background: #1e293b; padding: 30px; border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); width: 450px; }
            h2 { margin-top: 0; color: #38bdf8; text-align: center; }
            .member { margin: 15px 0; padding: 12px; background: #334155; border-radius: 8px; }
            .info { display: flex; justify-content: space-between; margin-bottom: 6px; font-weight: 500; }
            .progress-bar-bg { background: #1e293b; border-radius: 6px; height: 10px; width: 100%; overflow: hidden; }
            .progress-bar-fill { background: #38bdf8; height: 100%; border-radius: 6px; transition: width 0.4s ease; }
            .sync-btn { background: #10b981; color: white; margin-bottom: 20px; }
            .sync-btn:hover { background: #059669; }
            form { border-top: 1px solid #475569; padding-top: 15px; margin-top: 15px; }
            input, button { width: 100%; padding: 10px; margin: 6px 0; border-radius: 6px; border: 1px solid #475569; background: #0f172a; color: white; box-sizing: border-box; }
            button { background: #38bdf8; color: #0f172a; font-weight: bold; cursor: pointer; border: none; }
            button:hover { background: #0ea5e9; }
        </style>
    </head>
    <body>
        <div class="card">
            <h2>Dynamic Equity Dashboard</h2>
            
            <form method="POST">
                <input type="hidden" name="action" value="sync_git">
                <button type="submit" class="sync-btn">Sync Real Git Commits</button>
            </form>

            {% for item in breakdown %}
            <div class="member">
                <div class="info">
                    <span>{{ item.name }}</span>
                    <span>{{ item.equity }}% <small>({{ item.score }} pts)</small></span>
                </div>
                <div class="progress-bar-bg">
                    <div class="progress-bar-fill" style="width: {{ item.equity }}%;"></div>
                </div>
            </div>
            {% endfor %}

            <form method="POST">
                <input type="hidden" name="action" value="manual_add">
                <h3>Add / Update Teammate</h3>
                <input type="text" name="name" placeholder="Name" required>
                <input type="number" name="commits" placeholder="Commits count" required>
                <input type="number" name="pull_requests" placeholder="Pull Requests count" required>
                <input type="number" name="tasks_completed" placeholder="Tasks completed" required>
                <button type="submit">Update Contribution</button>
            </form>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_template, breakdown=breakdown)

if __name__ == "__main__":
    app.run(debug=True, port=5000)