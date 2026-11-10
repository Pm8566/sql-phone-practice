# SQL practice from my phone

A small automation I built to practise SQL every day from my phone, using GitHub Issues as the interface and GitHub Actions to mark my answers.

I'm learning SQL from the basics, so this repo is an honest log of that, mistakes included. Every attempt (right or wrong) is recorded in [`progress/log.md`](progress/log.md).

## How it works

1. **A question arrives.** Every day at 1pm (UK time in winter), a scheduled GitHub Action picks the next question and opens it as a GitHub Issue. The GitHub mobile app notifies me.
2. **I reply with SQL**, as a comment on the Issue.
3. **It's marked automatically.** A second Action runs my SQL against a small made-up ITAD (IT asset disposition) database in SQLite and compares the result with the expected one.
4. **It replies ✅ or ❌.** A wrong answer gets a hint (never the answer). A right answer closes the Issue.
5. **Every attempt is committed** to `progress/`, with the time it took me.

### Review queue (spaced repetition)
Any question I get wrong comes back as a review 1 day, then 3 days, then 7 days after I get it right. Once I've passed all three reviews it counts as learned. Reviews always come before new questions.

## Design choices

- **Answers can't be peeked at.** The repo is public, so the expected results are stored only as SHA-256 hashes (`questions/bank.json`). The checker hashes my result and compares the two.
- **Bad SQL can't break anything.** Each check builds a fresh in-memory database from `schema.sql`.
- **Safe against script injection.** My comment is passed to Python through an environment variable, never pasted straight into a shell command.
- **One question at a time.** If a question is still open, no new one is posted.

## Files

| File | What it does |
|---|---|
| `schema.sql` | Builds the made-up ITAD `assets` table |
| `questions/bank.json` | Questions, hints and hashed expected results |
| `check.py` | Runs a query and compares its hashed result |
| `post_question.py` | Picks today's question (a due review first, otherwise the next new one) |
| `mark.py` | Marks a reply, updates progress and the review queue, logs time taken |
| `.github/workflows/daily-question.yml` | Posts the daily question |
| `.github/workflows/mark-answer.yml` | Marks replies, commits the attempt, closes the Issue if correct |
| `progress/` | My solved questions, review queue and full attempt log |

## Try the checker locally

```
python3 check.py 1 "SELECT * FROM assets"
```

## What's next
More levels as I progress: aggregates and `GROUP BY`, then JOINs across new tables, subqueries/CTEs and window functions.
