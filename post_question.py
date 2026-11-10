import json
import os
from datetime import date

bank = json.load(open("questions/bank.json"))

solved = []
if os.path.exists("progress/solved.json"):
    solved = json.load(open("progress/solved.json"))

reviews = {}
if os.path.exists("progress/reviews.json"):
    reviews = json.load(open("progress/reviews.json"))

today = date.today().isoformat()

# 1. Is a review due? Lowest question number first.
review_id = None
for key in sorted(reviews, key=int):
    due = reviews[key]["due"]
    if due is not None and due <= today:
        review_id = int(key)
        break

# 2. Pick the question: a due review, otherwise the next new one.
next_question = None
label = ""
if review_id is not None:
    for q in bank:
        if q["id"] == review_id:
            next_question = q
    label = " (review)"
else:
    for q in bank:
        if q["id"] not in solved:
            next_question = q
            break

if next_question is None:
    print("Nothing to post today!")
else:
    qid = str(next_question["id"])
    title = "Q" + qid + label + ": " + next_question["question"]
    body = "**Level " + str(next_question["level"]) + "**"
    if label:
        body = body + " · 🔁 Review: you got this one wrong before."
    body = body + "\n\n" + next_question["question"] + "\n\n"
    body = body + "Reply with just your SQL as a comment. Table: `assets`."
    open("title.txt", "w").write(title)
    open("body.txt", "w").write(body)
    print("Picked Q" + qid + label)
