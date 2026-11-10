import json
import os
from datetime import datetime, timezone

from check import check

title = os.environ["ISSUE_TITLE"]
comment = os.environ["COMMENT_BODY"]

question_id = int(title.split(":")[0].replace("Q", ""))

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

now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
result = "CORRECT" if ok else "WRONG"
with open("progress/log.md", "a") as log:
    log.write("- " + now + " | Q" + str(question_id) + " | " + result + " | `" + sql.replace("\n", " ") + "`\n")

reply = ("✅ " if ok else "❌ ") + message
open("reply.txt", "w").write(reply)
open("result.txt", "w").write(result)
