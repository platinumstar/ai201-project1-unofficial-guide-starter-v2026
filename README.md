# The Unofficial Guide

name : Ronju Chowdhury
Corpus I picked : campus life

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

This project uses the campus life corpus to answer practical student questions about housing, laundry, registration, parking, and academic policies. It indexes short documents from the corpus, retrieves the most relevant chunks for a question, and rejects questions that do not match the available material. The system is designed to answer specific campus questions with evidence from the source documents rather than guessing from general knowledge.

## Chunking Strategy

**Chunk size:** 800 characters 
**Overlap:** 120 characters


I chose these settings because most campus-life documents are short and already complete on their own. The starter chunker produced 88 chunks from 88 documents, with a short average length of around 317 characters, so splitting at 800 characters did not create useful breaks. I kept the chunk size large enough to preserve whole ideas while adding a small overlap so related material stayed connected across boundaries.

## Sample Chunks
python app.py chunks
88 chunks total. Showing 5, spread across the corpus.

**Chunk 1** —  source: admin_add_drop_deadline.txt#0  - produced by: chunker.py::fallback_split
======================================================================
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.


**Chunk 2** —  source: course_biol_160.txt#0  -  produced by: chunker.py::fallback_split
======================================================================
BIOL 160 Cell Biology

I lived here my sophomore year. Format is lecture three times a week with a weekly lab. Assessment: four unit tests and a cumulative final. Not curved.

Expect 9 to 11 hours a week, the heaviest first-year course by reputation.

The one piece of advice: the unit tests come fast, roughly every three weeks; falling behind once is very hard to recover from.

**Chunk 3** — source: course_hist_118_workload.txt#0  -  produced by: chunker.py::fallback_split
======================================================================
Workload for HIST 118 Modern World History

People keep asking so: a lot of reading, about 120 pages a week, but no problem sets. That's real time, not optimistic time.

It's front-loaded — the first month is heavier than the rest, partly because you're learning the format.

**Chunk 4** — source: dining_pellew_dining_hall_followup.txt#0  -  produced by: chunker.py::fallback_split
======================================================================
Re: Pellew Dining Hall

Adding to what people have said about Pellew Dining Hall. The wait figure of 12 to 18 minutes at peak matches what I've seen. If you're trying to eat between classes, go before 11:45 and it's a different building entirely.

Also worth saying: the furthest hall from anywhere, next to the athletics centre. Nobody tells you this at orientation.

**Chunk 5** — source: housing_innisfree_hall.txt#0  -  produced by: chunker.py::fallback_split
======================================================================
Innisfree Hall — what it's actually like

Transferred in last year, so take this with a grain of salt. Built 1991, renovated 2022. Rooms are doubles arranged as pairs sharing one bathroom between two rooms.

The good: the shared-bathroom-between-two-rooms arrangement is the best compromise on campus.

The bad: no air conditioning, which matters for the first three weeks of September.

Laundry costs $1.75 wash, $1.75 dry, app-based. On noise: moderate; the building is L-shaped and the short wing is much quieter.

For each one, ask: could someone answer a question using only this,
without reading what came before or after?


## Sample Answer

**Question:**
How many washers and dryers are in Fenwick Court, and how much does laundry cost?

**Answer:**
Fenwick Court has eight washers and eight dryers, and laundry costs $1.75 per wash and $1.75 per dry.

```
[from housing_innisfree_hall.txt]
Laundry costs $1.75 wash, $1.75 dry, app-based. On noise: moderate; the building is L-shaped and the short wing is much quieter.
```

**My relevance cutoff:**
0.6

I ran all five in-scope questions and all five out-of-scope questions through retrieval and recorded the best distance for each result. The in-scope questions clustered between 0.20 and 0.37, while the out-of-scope questions were between 0.82 and 0.93. There was a clean gap between the two groups, so I placed the cutoff at 0.6. A lower cutoff would reject valid answers, and a higher cutoff would allow unrelated questions through.

| Question | In corpus? | Best distance |
|---|---|---|
| What are the quiet floors in Aldridge Hall, and how late is the library open during term? | Yes | 0.2094 |
| How many washers and dryers are in Fenwick Court, and how much does laundry cost? | Yes | 0.2001 |
| Which parking lots can students buy permits for, and is there a waitlist? | Yes | 0.3733 |
| When can students declare a major, and is there a penalty or advantage to timing? | Yes | 0.2458 |
| Is there a fee for an official transcript, and how do I get an unofficial one? | Yes | 0.2089 |
| What is the capital of Mongolia? | No | 0.8246 |
| How do I change the oil in a diesel engine? | No | 0.9340 |
| Who won the 1994 World Cup? | No | 0.8859 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.8442 |
| How do I write a for loop in Rust? | No | 0.8960 |

## How I Used AI

**1.** 
I asked AI to explain each section of the milestone as if I were a beginner, so I could understand what each requirement meant before I started writing. It gave me clear explanations and examples. I changed my approach by using those explanations as a guide.

**2.** 
I used AI mainly to help me understand the retrieval workflow and interpret the search distances. I asked for explanations of how the relevance gate works and what the threshold should represent, then I used that guidance to compare in-scope and out-of-scope results. 

**3.** 
I used AI to explain like before each section of Unit 2 and give me some ideas on narrowing down my tests to get the results. I also asked on the whether hybrid search would make difference, but I found that that it was the scorer.py being strict on mismatch on one of the expectation. So I picked a smaller prompt change instead, which resulted in correct prediction as seen in after run result.

**4.** 
For the capstone I used Claude Code to explain how to add structured logging (`obslog.py`), harden `serve.py` (input validation, rate limit, failures logged), and completed the Instrumentation and cost sections. I checked real log: I ran ten fresh questions myself, confirmed the token and latency numbers from the log lines (which caught a median latency I had stated wrongly, 693 ms instead of 682 ms), and noticed the log cannot split input from output tokens, so I report the cost as a range instead of a single figure.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

python run_eval.py --label before

What are the quiet floors in Aldridge Hall, and how late is the library open during term?
  run 1: pass  (best distance 0.209)
  run 2: pass  (best distance 0.209)
  run 3: pass  (best distance 0.209)

How many washers and dryers are in Fenwick Court, and how much does laundry cost?
  run 1: pass  (best distance 0.200)
  run 2: pass  (best distance 0.200)
  run 3: pass  (best distance 0.200)

Which parking lots can students buy permits for, and is there a waitlist?
  run 1: pass  (best distance 0.373)
  run 2: pass  (best distance 0.373)
  run 3: pass  (best distance 0.373)

When can students declare a major, and is there a penalty or advantage to timing?
  run 1: fail  (best distance 0.246)
  run 2: fail  (best distance 0.246)
  run 3: fail  (best distance 0.246)

Is there a fee for an official transcript, and how do I get an unofficial one?
  run 1: pass  (best distance 0.209)
  run 2: pass  (best distance 0.209)
  run 3: pass  (best distance 0.209)

Out-of-scope questions (the gate should refuse these):
  refused  (best distance 0.825)  What is the capital of Mongolia?
  refused  (best distance 0.934)  How do I change the oil in a diesel engine?
  refused  (best distance 0.886)  Who won the 1994 World Cup?
  refused  (best distance 0.844)  What is the recommended dosage of ibuprofen for a headache?
  refused  (best distance 0.896)  How do I write a for loop in Rust?
  -> gate refused 5 of 5

Wrote results/run_2026-09-24_2146_before.md
15 model calls this session, 9074 tokens (8370 in, 704 out)

Commit this file. It's the evidence the run actually happened.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Chunk quality — no chunk split across documents | 100% of chunks | 88/88 | 88/88 | 88/88 | MET |
| 5. Cited source is the correct source | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |


### Criterion 1 & 5 example — real output

Produced by `run_eval.py`, saved to `results/run_2026-09-24_2146_before.md`

**Question:** When can students declare a major, and is there a penalty or advantage to timing?
- Sources retrieved: admin_add_drop_deadline.txt, admin_declaring_a_major.txt, admin_grade_appeals.txt, admin_graduation_requirements.txt, admin_pass_fail_option.txt

> Students can declare a major at the end of their second semester, or later if needed.
> There is no penalty for declaring late and no advantage to declaring early, except for
> being assigned a departmental adviser (admin_declaring_a_major.txt).

This is worth including because `scorer.py` flagged this question as "fail" in the run log
above, but reading the actual output shows the fact was retrieved and correctly cited —
scorer.py's pass/fail is checking something narrower than these five criteria.

### Criterion 4 example — real output

Produced by `app.py::index` (via `chunker.py::fallback_split`), run against the `campus_life` corpus.

```
python app.py index
Corpus: campus_life
  loaded   88 documents, 27,908 characters, ~317 characters per document
  chunked  88 chunks, 317 characters on average (shortest 178, longest 549), produced by chunker.py::fallback_split
  embedding 88 chunks (first run downloads the model)...
  stored   88 chunks in 4.9s
```

88 documents in, 88 chunks out, longest chunk 549 characters — under the 800-character
chunk_size limit — so no document was split across chunks.

## Verdicts

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunk contains the answer | MET | Target was 4 of 5; all three runs came back 5/5 with no variance. Note: scorer.py flagged the major-declaring question as "fail," but manually reading the output showed the fact was present in the retrieved chunk and correctly cited — scorer.py checks something narrower than this criterion. |
| 2 | Every answer names a source | MET | Target was 5 of 5; all three runs came back 5/5, every answer cited at least one file. |
| 3 | Gate stops out-of-corpus questions | MET | Target was 4 of 5; the gate refused 5/5 out-of-scope questions, and this number doesn't vary between runs since retrieval and the cutoff comparison are deterministic. |
| 4 | Chunk quality — no chunk split across documents | MET | Target was 100% of chunks; indexing produced 88 chunks from 88 documents with a longest chunk of 549 characters, under the 800-character limit, so no document was split. |
| 5 | Cited source is the correct source | MET | Target was 4 of 5; checked each answer's cited file against where the fact actually lives in the corpus, and all 5 cited the correct source in all three runs. |

## Diagnoses

There was no MISS — all chunking and embedding stayed within range, and the
LLM found the correct answer from the corpus in every run.

Some of that is a small, clean corpus rather than proof the pipeline is
bulletproof: 88 short documents, each on a distinct topic, with little overlap
between them. A messier or larger corpus would stress retrieval and generation
harder than mine did here.

The softest spot was criterion 1. My target was "4 of 5 retrieved chunks
contain the answer," and I counted 5/5 — but scorer.py's automated check
flagged the major-declaring question as a fail, and I only kept it as MET
because I personally reread the output and judged the fact was present. That's
my own judgment breaking a tie, not a clean pass. If I tightened this criterion,
I'd change it to "5 of 5 pass scorer.py's automated check, with no manual
override allowed" — removing myself as the tiebreaker.


## The Improvement

**What I changed:**
Added one rule to `GROUNDING_INSTRUCTION` in `generate.py:282`: "State the direct
answer to the question in the first sentence, before any caveats or extra detail."

**Why I picked it:**
My Milestone 3 diagnosis found the one soft spot was generation, not retrieval —
scorer.py flagged the major-declaring answer as a fail even though the correct
chunk was retrieved and cited, so I targeted how the answer is phrased.

### Run Log — After

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Chunk quality — no chunk split across documents | 100% of chunks | 88/88 | 88/88 | 88/88 | MET |
| 5. Cited source is the correct source | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |

### Criterion 1 & 5 example — real output (after)

Produced by `run_eval.py`, saved to `results/run_2026-09-27_2244_after.md`

**Question:** When can students declare a major, and is there a penalty or advantage to timing?
- Sources retrieved: admin_add_drop_deadline.txt, admin_declaring_a_major.txt, admin_grade_appeals.txt, admin_graduation_requirements.txt, admin_pass_fail_option.txt

> Students declare a major at the end of their second semester, or later if needed,
> with no penalty for declaring late and no advantage to declaring early except for
> being assigned a departmental adviser (admin_declaring_a_major.txt).

Compare this to the before-example above: the fact is stated just as plainly, the
same source is cited, and scorer.py still flags this question as "fail" in all
three after-runs — identical to before. The prompt change didn't move this result,
which supports the diagnosis that the mismatch lives in scorer.py's matching logic,
not in how the answer is phrased.

**Did it help?**

No measurable difference. All five criteria landed on the identical numbers as
the "before" run, and scorer.py still flags the major-declaring question as a
fail in all three runs. This confirms the Milestone 3 diagnosis: the soft spot
was scorer.py's exact-match scoring logic, not how the model phrases its
answer — a prompt change can't fix a mismatch that lives in the scorer itself.


## What's Still Broken

Nothing is MISSED, but scorer.py still disagrees with my own read on criterion 1's toughest question, even after the prompt change. I'd fix this next by rewriting scorer.py's matching logic to check for the fact's presence semantically rather than exact phrase match — I stopped here because that's a change to the test itself, not the system, and Milestone 4 asked me to change one thing in the system.

## What I'd Do Differently

Criterion 1 is the one I'd write differently. My target was "4 of 5 retrieved
chunks contain the answer," but I hit 5/5 only because I personally broke a tie
that scorer.py called the other way. Next time I'd write it as "5 of 5 pass
scorer.py's automated check, with no manual override allowed" from the start,
instead of discovering after the fact that my own judgment was doing the
tiebreaking work the target was supposed to measure on its own.

## Capstone

**What This Extends**

Project 1, The Unofficial Guide: a RAG system over the campus_life corpus (88
documents). New in this unit: `serve.py` runs the existing pipeline as an HTTP
service (`POST /ask`, `GET /health`) with input validation, a per-address rate
limit, and a structured log of every request (`obslog.py` -> `logs/requests.jsonl`).
The chunker, retriever, gate and generator are unchanged.


**The Shape**

Shape A, deploy and instrument. I am adding the operational layer: a documented
run path, a structured log that records failures as well as successes, and a
measured cost per run.


**Running It**

Path B, local with logs. Start command, environment and the failure table
are in RUNNING.md under "Capstone run path". A real session's log is pasted under
Instrumentation below.

**Instrumentation**

Every request to `POST /ask` in `serve.py` writes one JSON line to `logs/requests.jsonl` through `obslog.log_event()` (`obslog.py`). Failures are logged too: a rejected input leaves a record with its status and an `error` field, so a failure never shows up only as an absence.

Fields per record:

| Field | Meaning |
|---|---|
| `ts` | Timestamp, local time, to the second |
| `status` | HTTP status returned (200, 400, 413, 429, 500, 503) |
| `latency_ms` | Time from the start of `ask()` to the response |
| `question` | What came in |
| `answer` | What went out (truncated to 2000 characters in the log) |
| `refused` | `true` if the retrieval gate refused (no model call) |
| `best_distance` | Distance of the closest retrieved chunk (gate threshold is 0.6) |
| `sources` | Every file the retriever returned |
| `cited` | Files named in the answer text, limited to `sources` |
| `tokens` | Tokens spent by this request (0 for a refusal or a cache hit) |
| `error` | Reason, on failed requests |

Entries from a real session (14 lines, copied as text from `logs/requests.jsonl`). Lines 3 and 14 are failed requests (400); line 2 is a gate refusal; line 1 is a cache hit, so `tokens` is 0.

```
{"ts": "2026-11-15T23:38:16", "status": 200, "latency_ms": 949, "question": "Which parking lots can students buy permits for, and is there a waitlist?", "answer": "Students can buy permits for the west and east lots, and there is no waitlist (admin_parking_permits.txt).", "refused": false, "best_distance": 0.3733, "sources": ["admin_parking_permits.txt", "advising_registration.txt", "dining_verrill_street_grill.txt", "money_textbooks.txt", "transit_shuttle.txt"], "cited": ["admin_parking_permits.txt"], "tokens": 0}
{"ts": "2026-11-15T23:38:16", "status": 200, "latency_ms": 48, "question": "What is the capital of Mongolia?", "answer": "I don't have enough information about that.", "refused": true, "best_distance": 0.8246, "sources": [], "cited": [], "tokens": 0}
{"ts": "2026-11-15T23:38:16", "status": 400, "latency_ms": 0, "error": "empty question"}
{"ts": "2026-11-15T23:44:59", "status": 200, "latency_ms": 1691, "question": "How many pages can I print per semester?", "answer": "You can print roughly 600 black-and-white pages per semester (admin_printing_quota.txt).", "refused": false, "best_distance": 0.3171, "sources": ["admin_graduation_requirements.txt", "admin_printing_quota.txt", "course_cs_340.txt", "course_engl_205.txt", "money_textbooks.txt"], "cited": ["admin_printing_quota.txt"], "tokens": 628}
{"ts": "2026-11-15T23:45:02", "status": 200, "latency_ms": 671, "question": "How do I connect to campus Wi-Fi?", "answer": "I do not have enough information to answer how to connect to campus Wi-Fi from the provided documents.\n\nSource: admin_wifi_and_accounts.txt", "refused": false, "best_distance": 0.5978, "sources": ["admin_add_drop_deadline.txt", "admin_wifi_and_accounts.txt", "dining_the_ridgeway_cafe.txt", "dining_verrill_street_grill.txt", "money_textbooks.txt"], "cited": ["admin_wifi_and_accounts.txt"], "tokens": 674}
{"ts": "2026-11-15T23:45:06", "status": 200, "latency_ms": 856, "question": "When does the campus shuttle run?", "answer": "The campus shuttle runs a loop every 20 minutes from 7am to 11pm on weekdays and every 40 minutes on weekends, according to `transit_shuttle.txt`.", "refused": false, "best_distance": 0.4021, "sources": ["dining_halden_hall_followup.txt", "dining_kestrel_commons_followup.txt", "dining_the_ridgeway_cafe_followup.txt", "transit_shuttle.txt", "transit_walking.txt"], "cited": ["transit_shuttle.txt"], "tokens": 719}
{"ts": "2026-11-15T23:45:10", "status": 200, "latency_ms": 755, "question": "Where can I find cheap textbooks?", "answer": "You can find textbooks without paying full price by using the library's two-hour reserve copy or by asking the campus store to price-match another listing shown on your phone. This information comes from money_textbooks.txt.", "refused": false, "best_distance": 0.2963, "sources": ["admin_library_holds.txt", "admin_printing_quota.txt", "course_math_220.txt", "money_textbooks.txt", "study_group_rooms.txt"], "cited": ["money_textbooks.txt"], "tokens": 607}
{"ts": "2026-11-15T23:45:14", "status": 200, "latency_ms": 632, "question": "What on-campus jobs are available to students?", "answer": "The documents mention library and dining jobs as available on-campus work ([money_jobs.txt]).", "refused": false, "best_distance": 0.4953, "sources": ["admin_campus_jobs_and_financial_aid.txt", "admin_wifi_and_accounts.txt", "dining_verrill_street_grill.txt", "money_jobs.txt", "money_textbooks.txt"], "cited": ["money_jobs.txt"], "tokens": 620}
{"ts": "2026-11-15T23:45:17", "status": 200, "latency_ms": 693, "question": "When does course registration open?", "answer": "Based on the provided documents, registration times are staggered by credit hours. \n\nSource: advising_registration.txt", "refused": false, "best_distance": 0.416, "sources": ["admin_add_drop_deadline.txt", "admin_study_abroad.txt", "advising_registration.txt", "dining_north_kitchen_followup.txt", "dining_verrill_street_grill_followup.txt"], "cited": ["advising_registration.txt"], "tokens": 575}
{"ts": "2026-11-15T23:45:21", "status": 200, "latency_ms": 597, "question": "What are the hours for the Verrill Street Grill?", "answer": "The hours for the Verrill Street Grill are 11:00am to 1:00am daily during term, according to dining_verrill_street_grill.txt.", "refused": false, "best_distance": 0.2779, "sources": ["dining_halden_hall.txt", "dining_kestrel_commons.txt", "dining_north_kitchen.txt", "dining_verrill_street_grill.txt", "dining_verrill_street_grill_followup.txt"], "cited": ["dining_verrill_street_grill.txt"], "tokens": 800}
{"ts": "2026-11-15T23:45:25", "status": 200, "latency_ms": 615, "question": "How many credits do I need to graduate?", "answer": "You need 120 credit hours to graduate. This information comes from admin_graduation_requirements.txt.", "refused": false, "best_distance": 0.3033, "sources": ["admin_add_drop_deadline.txt", "admin_declaring_a_major.txt", "admin_graduation_requirements.txt", "admin_pass_fail_option.txt", "course_engl_205.txt"], "cited": ["admin_graduation_requirements.txt"], "tokens": 579}
{"ts": "2026-11-15T23:45:28", "status": 200, "latency_ms": 696, "question": "Which dorm is Morrow House?", "answer": "I do not have enough information to state which dorm is Morrow House, as the documents only provide descriptions and details *about* Morrow House rather than its classification as a dorm. \n\nSources: housing_morrow_house.txt, housing_morrow_house_laundry.txt, housing_morrow_house_noise.txt", "refused": false, "best_distance": 0.3608, "sources": ["housing_aldridge_hall.txt", "housing_morrow_house.txt", "housing_morrow_house_laundry.txt", "housing_morrow_house_noise.txt", "housing_tamsin_court.txt"], "cited": ["housing_morrow_house.txt", "housing_morrow_house_laundry.txt", "housing_morrow_house_noise.txt"], "tokens": 755}
{"ts": "2026-11-15T23:45:32", "status": 200, "latency_ms": 612, "question": "What does a parking permit cost?", "answer": "I do not have enough information to answer what a parking permit costs. \n\nSource: admin_parking_permits.txt", "refused": false, "best_distance": 0.555, "sources": ["admin_parking_permits.txt", "admin_printing_quota.txt", "housing_calder_annexe.txt", "housing_fenwick_court.txt", "housing_innisfree_hall.txt"], "cited": ["admin_parking_permits.txt"], "tokens": 722}
{"ts": "2026-11-15T23:53:08", "status": 400, "latency_ms": 0, "error": "question must be a string"}
```

What the log shows: `sources` is what was retrieved, `cited` is what the answer named. For "Which parking lots..." the retriever returned five files and the answer used one. Three of the ten fresh answers (Wi-Fi, Morrow House dorm, parking cost) say "I do not have enough information" while `refused` is `false`: the gate passed them and the model declined in text, so `refused` does not capture that case.

**What It Costs**

Measured cost: **about 668 tokens per answered request** (mean of 667.9; range 575 to 800).

How I measured it: I asked ten questions that had never been asked before, so none could be served from the response cache (cached answers log 0 tokens and would understate the cost). `serve.py` records `tokens` for each request as the difference in `generate.py`'s running token total (prompt plus output) before and after the pipeline call; a lock keeps requests from overlapping so the difference is attributable to one request. I averaged the `tokens` of the ten answered lines (lines 4 to 13 above). Refusals cost 0 because Gemini is never called. Median latency for these runs was 682 ms (mean 782 ms; the 1691 ms maximum was the first request, which loads the index).

For 100 people a day: 100 requests x 668 tokens = 66,800 tokens a day, about 2.0 million tokens a month. At ten questions each it is 668,000 a day. In money, for `gemini-3.5-flash-lite` at $0.30 per million input tokens and $2.50 per million output tokens (no caching): the log's `tokens` field is prompt plus output combined, so I price it as a range. If all 668 tokens were input, a request costs about $0.0002, which is $0.02 a day and $0.60 a month for 100 requests a day. If all 668 were output (a ceiling, since these prompts are mostly retrieved context), it is about $0.0017 a request, $0.17 a day and $5.01 a month. The real figure falls between those, much nearer the low end. At ten questions each (668,000 tokens a day) the ceiling is about $1.67 a day, about $50 a month.

**Run Log and Verdicts**

Method: `python tools/measure.py` sent 30 requests per trial through `serve.py` (10 bad inputs, 10 unrelated questions, 10 answerable questions), three trials, each with an empty response cache so the model was really called again. Raw output is in `results/capstone_trial_1.json` to `_3.json`. The criteria are in `criteria.md`, committed before these runs.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Bad input gets a 4xx and a log line | 10 of 10 | 10/10 | 10/10 | 10/10 | MET |
| 2. Unrelated questions are refused | 10 of 10 | 10/10 | 10/10 | 10/10 | MET |
| 3. Every request leaves a complete log record | 30 of 30 | 30/30 | 30/30 | 30/30 | MET |
| 4. `cited` names the file that holds the answer | 9 of 10 | 10/10 | 9/10 | 9/10 | MET |
| 5. Answered request under 1,000 tokens and 2,000 ms | 9 of 10 | 5/10 | 6/10 | 6/10 | MISSED |

Real output from trial 2 (`logs/requests.jsonl`, written by `obslog.log_event()` called from `ask()` in `serve.py`). Long fields are cut and marked.

Criterion 1, a bad request (`serve.py::_reject`):
```
{"ts": "2026-11-16T22:07:51", "status": 400, "latency_ms": 0, "error": "empty question"}
```

Criterion 2, an unrelated question refused by the gate (`gate.py`, logged by `ask()`):
```
{"ts": "2026-11-16T22:07:51", "status": 200, "latency_ms": 54, "question": "What is the capital of Mongolia?", "answer": "I don't have enough information about that.", "refused": true, "best_distance": 0.8246, "sources": [], "cited": [], "tokens": 0}
```

Criterion 4, a correct citation:
```
{"ts": "2026-11-16T22:07:53", "status": 200, "latency_ms": 882, "question": "Which parking lots can students buy permits for, and is there a waitlist?", "answer": "Students can buy permits for the west and east lots, and there is no waitlist (admin_parking_permits.txt).", "refused": false, "best_distance": 0.3733, "sources": ["admin_parking_permits.txt", "advising_registration.txt", "dining_verrill_street_grill.txt", "money_textbooks.txt", "transit_shuttle.txt"], "cited": ["admin_parking_permits.txt"], "tokens": 654}
```

Criterion 5, a slow answer and the failed request (`generate.py::generate`, the retry loop):
```
{"ts": "2026-11-16T22:07:58", "status": 200, "latency_ms": 2866, "question": "What are the quiet floors in Aldridge Hall?", "answer": "The quiet floors in Aldridge Hall are floors 3 and 4 (housing_aldridge_hall.txt and housing_aldridge_hall_noise.txt).", "refused": false, "best_distance": 0.3459, "sources": ["housing_aldridge_hall.txt", "housing_aldridge_hall_noise.txt", "housing_innisfree_hall_noise.txt", "housing_old_brewhouse_noise.txt", "housing_tamsin_court_noise.txt"], "cited": ["housing_aldridge_hall.txt", "housing_aldridge_hall_noise.txt"], "tokens": 641}
{"ts": "2026-11-16T22:08:21", "status": 500, "latency_ms": 15494, "question": "What are the hours for the Verrill Street Grill?", "error": "RuntimeError: Still rate limited after 4 attempts. Wait a minute and try again - your key is fine.\nLast error: 429 RESOURCE_EXHAUSTED. [...truncated]"}
```

Diagnosis of criterion 5: this is a latency miss, not a token miss. Every answered request that returned used 561 to 800 tokens, under the 1,000 limit. The latency misses were 5, 4 and 4 requests over 2,000 ms per trial, ranging from 2.1 s to 15.5 s. The stage is the generator's rate-limit handling in `generate.py`. The mechanism: the Gemini free tier for `gemini-3.5-flash-lite` allows 15 requests per minute (the 429 message says `limit: 15`), but `config.REQUESTS_PER_MINUTE` is 30, so the local pacer lets calls through until Gemini rejects them. The retry loop then backs off 1, 2, 4 and 8 seconds, and the stderr output shows the pacer's own waits as well. Ten model calls per trial, run back to back, are enough to exceed 15 in a minute.

Criterion 4's one miss (trial 2, 9/10) is the same cause, not a citation failure: the Verrill Street Grill request exhausted its four retries and returned a 500, so it had no `cited` field at all. That is one problem (a pacer set at twice the real quota) with two symptoms: slow answers and one failed request. One caveat: my harness ran the three trials with no pause between them, so it created more load than one student would. A real user sending bursts on the free tier would still hit the same wall, but not as often.

Criteria 1, 2 and 3 were MET in all nine runs. I set 10 of 10 and 30 of 30 on purpose, since bad input and the log involve no model randomness, and they held.
