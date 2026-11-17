#!/usr/bin/env python3
"""Run the capstone trials against serve.py and score all five criteria.

    python tools/measure.py            # 3 trials (what the run log needs)
    python tools/measure.py --trials 1

Each trial sends 30 requests through Flask's test client (no server needed):
  10 bad requests, 10 clearly unrelated questions, 10 answerable questions.
Every trial uses its own empty response cache, so trial 2 and 3 really call
the model again instead of replaying trial 1. The answerable group calls the
model (about 10 requests, roughly 700 tokens each).

Scoring reads logs/requests.jsonl, the same file a reader would check.
Raw per-trial output goes to results/capstone_trial_<n>.json.
"""

import argparse
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import config  # noqa: E402
import obslog  # noqa: E402

BAD = [  # (label, kwargs for client.post)
    ("empty question 1", {"json": {"question": ""}}),
    ("empty question 2", {"json": {"question": "   "}}),
    ("non-string 1", {"json": {"question": 42}}),
    ("non-string 2", {"json": {"question": ["a", "b"]}}),
    ("too long 1", {"json": {"question": "a" * 1001}}),
    ("too long 2", {"json": {"question": "why " * 400}}),
    ("not an object 1", {"json": ["question"]}),
    ("not an object 2", {"data": "just text", "content_type": "text/plain"}),
    ("missing field 1", {"json": {}}),
    ("missing field 2", {"json": {"q": "wrong key"}}),
]

UNRELATED = [
    "What is the capital of Mongolia?",
    "Who won the 1994 World Cup?",
    "What is the recommended dosage of ibuprofen for a headache?",
    "How do I write a for loop in Rust?",
    "How tall is Mount Everest?",
    "What is the boiling point of mercury?",
    "Who painted the Mona Lisa?",
    "How do I bake sourdough bread?",
    "What is the current price of Bitcoin?",
    "Who is the prime minister of Canada?",
]

# (question, file that holds the answer)
ANSWERABLE = [
    ("Which parking lots can students buy permits for, and is there a waitlist?", "admin_parking_permits.txt"),
    ("When can students declare a major, and is there a penalty or advantage to timing?", "admin_declaring_a_major.txt"),
    ("What are the quiet floors in Aldridge Hall?", "housing_aldridge_hall.txt"),
    ("How many washers and dryers are in Fenwick Court?", "housing_fenwick_court.txt"),
    ("How many pages can I print per semester?", "admin_printing_quota.txt"),
    ("When does the campus shuttle run?", "transit_shuttle.txt"),
    ("Where can I find cheap textbooks?", "money_textbooks.txt"),
    ("What are the hours for the Verrill Street Grill?", "dining_verrill_street_grill.txt"),
    ("How many credits do I need to graduate?", "admin_graduation_requirements.txt"),
    ("What on-campus jobs are available to students?", "money_jobs.txt"),
]


def read_log() -> list[dict]:
    if not obslog.LOG_PATH.exists():
        return []
    return [json.loads(line) for line in obslog.LOG_PATH.read_text().splitlines() if line.strip()]


def run_trial(n: int) -> dict:
    # A fresh cache per trial, so the model is genuinely called again.
    config.CACHE_DIR = Path(tempfile.mkdtemp(prefix=f"capstone_cache_{n}_"))
    import serve  # imported late so the cache dir above is in place

    serve._hits.clear()
    before = len(read_log())
    client = serve.app.test_client()
    sent = []  # (group, label, http status, response json)

    def post(group, label, ip, **kw):
        r = client.post("/ask", environ_base={"REMOTE_ADDR": ip}, **kw)
        sent.append((group, label, r.status_code, r.get_json(silent=True)))

    for label, kw in BAD:
        post("bad", label, "10.0.0.1", **kw)
    for q in UNRELATED:
        post("unrelated", q, "10.0.0.2", json={"question": q})
    for q, _ in ANSWERABLE:
        post("answerable", q, "10.0.0.3", json={"question": q})

    new = read_log()[before:]

    # Lines line up with requests one-to-one, in order, if criterion 3 holds.
    c3_lines = len(new) == len(sent)
    needed_all = ("ts", "status", "latency_ms")
    needed_200 = ("question", "answer", "tokens")
    c3_fields = all(all(k in rec for k in needed_all) for rec in new) and all(
        all(k in rec for k in needed_200) for rec in new if rec.get("status") == 200
    )
    c3_ok = sum(
        1
        for rec in new
        if all(k in rec for k in needed_all)
        and (rec.get("status") != 200 or all(k in rec for k in needed_200))
    )

    bad_log = new[0:10] if c3_lines else []
    unrel_log = new[10:20] if c3_lines else []
    ans_log = new[20:30] if c3_lines else []

    c1 = sum(
        1
        for (g, _, status, _), rec in zip(sent[0:10], bad_log)
        if 400 <= status < 500 and rec.get("status") == status and rec.get("error")
    )
    c2 = sum(
        1
        for (g, _, status, body), rec in zip(sent[10:20], unrel_log)
        if status == 200 and body and body.get("refused") is True and rec.get("tokens") == 0
    )
    c4 = sum(
        1
        for (_, expected), rec in zip(ANSWERABLE, ans_log)
        if rec.get("cited") and expected in rec["cited"]
    )
    c5 = sum(
        1
        for rec in ans_log
        if rec.get("status") == 200 and rec.get("tokens", 10**9) < 1000 and rec.get("latency_ms", 10**9) < 2000
    )

    return {
        "trial": n,
        "c1": c1,
        "c2": c2,
        "c3": c3_ok if c3_lines else 0,
        "c3_total": len(sent),
        "c3_lines_match": c3_lines,
        "c4": c4,
        "c5": c5,
        "answered_tokens": [r.get("tokens") for r in ans_log],
        "answered_latency_ms": [r.get("latency_ms") for r in ans_log],
        "new_log_lines": new,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--trials", type=int, default=3)
    args = ap.parse_args()

    out_dir = ROOT / "results"
    out_dir.mkdir(exist_ok=True)
    results = []
    for n in range(1, args.trials + 1):
        res = run_trial(n)
        results.append(res)
        (out_dir / f"capstone_trial_{n}.json").write_text(json.dumps(res, indent=2))
        print(f"trial {n}: c1={res['c1']}/10 c2={res['c2']}/10 "
              f"c3={res['c3']}/{res['c3_total']} c4={res['c4']}/10 c5={res['c5']}/10")

    targets = [("1 bad input rejected + logged", "c1", 10, 10),
               ("2 unrelated refused", "c2", 10, 10),
               ("3 complete log record", "c3", 30, 30),
               ("4 cited names the file", "c4", 10, 9),
               ("5 cheap and fast", "c5", 10, 9)]
    print("\n| Criterion | Target | " + " | ".join(f"Run {r['trial']}" for r in results) + " | Verdict |")
    print("|---|---|" + "---|" * len(results) + "---|")
    for name, key, total, target in targets:
        vals = [r[key] for r in results]
        verdict = "MET" if all(v >= target for v in vals) else "MISSED"
        cells = " | ".join(f"{v}/{total}" for v in vals)
        print(f"| {name} | {target} of {total} | {cells} | {verdict} |")


if __name__ == "__main__":
    main()
