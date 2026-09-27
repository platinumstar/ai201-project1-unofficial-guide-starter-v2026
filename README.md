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


**1.** I asked AI to explain each section of the milestone as if I were a beginner, so I could understand what each requirement meant before I started writing. It gave me clear explanations and examples. I changed my approach by using those explanations as a guide.

**2.** I used AI mainly to help me understand the retrieval workflow and interpret the search distances. I asked for explanations of how the relevance gate works and what the threshold should represent, then I used that guidance to compare in-scope and out-of-scope results. 

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

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

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

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
