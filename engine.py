import json

def calculate_contribution(commits, pull_requests, tasks_completed):
    commit_score = commits * 2
    pr_score = pull_requests * 10
    task_score = tasks_completed * 5
    return commit_score + pr_score + task_score

# Load team stats from our mock database file
with open("data.json", "r") as f:
    team_members = json.load(f)

# Calculate individual scores
scores = {}
for name, stats in team_members.items():
    scores[name] = calculate_contribution(
        stats["commits"], 
        stats["pull_requests"], 
        stats["tasks_completed"]
    )

# Calculate total team effort
total_points = sum(scores.values())

# Output live equity breakdown
print("--- Live Project Equity Breakdown (from JSON) ---")
for name, score in scores.items():
    equity = (score / total_points) * 100
    print(f"{name}: {equity:.1f}% equity ({score} points)")