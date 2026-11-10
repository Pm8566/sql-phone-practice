import json
import os

bank = json.load(open("questions/bank.json"))

solved = []
if os.path.exists("progress/solved.json"):
    solved = json.load(open("progress/solved.json"))

next_question = None
for q in bank:
    if q["id"] not in solved:
        next_question = q
        break

if next_question is None:
    print("All questions solved!")
else:
    qid = str(next_question["id"])
    title = "Q" + qid + ": " + next_question["question"]
    body = "**Level " + str(next_question["level"]) + "**\n\n"
    body = body + next_question["question"] + "\n\n"
    body = body + "Reply with just your SQL as a comment. Table: `assets`."
    open("title.txt", "w").write(title)
    open("body.txt", "w").write(body)
    print("Picked Q" + qid)
