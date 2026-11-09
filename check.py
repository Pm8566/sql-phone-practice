import sys
import json
import sqlite3
import hashlib

def fingerprint(rows, ordered):
	lines = []
	for row in rows:
		clean_row = []
		for value in row:
			if isinstance(value, float) and value.is_integer():
				value = int(value)
			clean_row.append(value)
		lines.append(json.dumps(clean_row))
	if not ordered:
		lines.sort()
	text = "\n".join(lines)
	return hashlib.sha256(text.encode()).hexdigest()

def check(question_id, sql):
	bank = json.load(open("questions/bank.json"))
	question = None
	for q in bank:
		if q["id"] == question_id:
			question = q
	con = sqlite3.connect(":memory:")
	con.executescript(open("schema.sql").read())
	try:
		rows = con.execute(sql).fetchall()
	except sqlite3.Error as e:
		return False, "Your SQL didn't run: " + str(e)
	if fingerprint(rows, question["ordered"]) == question["fingerprint"]:
		return True, "Correct!"
	return False, "Not quite. Hint: " + question["hint"]

if __name__ == "__main__":
	question_id = int(sys.argv[1])
	sql = sys.argv[2]
	ok, message = check(question_id, sql)
	print("CORRECT" if ok else "WRONG", "-", message)
