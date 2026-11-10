import json
import os
from datetime import datetime, timezone, date, timedelta

from check import check

INTERVALS = [1, 3, 7]  # NEW: days until each review

title = os.environ["ISSUE_TITLE"]
comment = os.environ["COMMENT_BODY"]

# NEW: "Q1 (review): ..." -> "Q1" -> 1
question_id = int(title.split(":")[0].split()[0].replace("Q", ""))

lines = []
for line in comment.splitlines():
    if not line.strip().startswith("```"):
        lines.append(line)
sql = "\n".join(lines).strip()

ok, message = check(question_id, sql)

os.makedirs("progress", exist_ok=True)

solved = []
if os.path.exists("progress/solved.json"):
    solved = json.load(open("progress/solved.json"))
if ok and question_id not in solved:
    solved.append(question_id)
with open("progress/solved.json", "w") as f:
    json.dump(solved, f)

# NEW: review queue
reviews = {}
if os.path.exists("progress/reviews.json"):
    reviews = json.load(open("progress/reviews.json"))

key = str(question_id)
if not ok:
    reviews[key] = {"step": 0, "due": None}
elif key in reviews:
    step = reviews[key]["step"]
    if step < len(INTERVALS):
        due = date.today() + timedelta(days=INTERVALS[step])
        reviews[key] = {"step": step + 1, "due": due.isoformat()}
    else:
        del reviews[key]

with open("progress/reviews.json", "w") as f:
    json.dump(reviews, f, indent=2)

# NEW: minutes from question posted to this answer
minutes = "?"
if os.environ.get("ISSUE_CREATED") and os.environ.get("COMMENT_CREATED"):
    posted = datetime.fromisoformat(os.environ["ISSUE_CREATED"].replace("Z", "+00:00"))
    answered = datetime.fromisoformat(os.environ["COMMENT_CREATED"].replace("Z", "+00:00"))
    minutes = str(round((answered - posted).total_seconds() / 60))

now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
result = "CORRECT" if ok else "WRONG"
with open("progress/log.md", "a") as log:
    log.write("- " + now + " | Q" + str(question_id) + " | " + result + " | " + minutes + " min | `" + sql.replace("\n", " ") + "`\n")

reply = ("✅ " if ok else "❌ ") + message
open("reply.txt", "w").write(reply)
open("result.txt", "w").write(result)
