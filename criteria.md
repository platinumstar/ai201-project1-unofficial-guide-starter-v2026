# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
When I ran my questions with ask  all my results 5 out of 5 came within the threshold of 0.6 cutoff as they were between 0.209 and 0.400.  
I kept the target at 4 of 5  because in campus life there are similar mentions of duplicates of the laundry in different documents. 
Specifically laundry documents for different dorms. I noticed when I did not mentioned the building clearly I got the answer : I do not have enough information to answer your question because you did not specify which building's laundry facilities you are asking about.

> **Revised in unit 2:** 
> For at least 4 of 5 questions, `scorer.py`'s automated
> check passes with no manual override — not just "I judged the fact was
> present when I read the output."
>
> **Why revised:** 
> In my before and after runs, `scorer.py` flagged the
> major-declaring question as a fail in all three runs each time, but I still
> counted it as passing because I personally reread the retrieved chunk and
> the generated answer and judged the fact was there and correctly cited. That
> means the criterion, as originally written, couldn't be measured the same
> way twice — the automated check and my own read disagreed, and I broke the
> tie myself rather than the target holding on its own. The revised version
> removes me as the tiebreaker so the criterion is checkable without my
> judgment filling the gap.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
The grounding instruction is in generate.py (GROUNDING_INSTRUCTION, generate.py:276). Grounding specifies the to return : "name the file you used.". Since it is designed and hardcoded in this way on the prompt; I expected all 5 to give the source, and not 4 out of 5

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

**Why this target:**

"I haven't run Milestone 4 yet, so I'm setting this target before I've seen the actual distance gap between in-scope and out-of-scope questions. I'll revisit it once I have real numbers."
<!-- What did your distances look like when you set the cutoff in Milestone 4?
     Was there a clean gap, or did the two groups overlap? -->

---

## 4. The chunk quality — none split 

100% of the 88 chunks are complete documents — none are split, since every document is under the 800-character chunk_size (average 317, longest 549).

**Why this target:**
When running index I noticed loaded 88 documents stored 88 chunks, so all the documents included are within chunk size as given below:
>python app.py index
Corpus: campus_life
  loaded   88 documents, 27,908 characters, ~317 characters per document
  chunked  88 chunks, 317 characters on average (shortest 178, longest 549), produced by chunker.py::fallback_split
  embedding 88 chunks (first run downloads the model)...
  stored   88 chunks in 4.9s


---

## 5. Cited source is the correct source

In at least 4 of my 5 test questions, the document named in the answer is one that actually contains the fact used to answer.

**Why this target:**
I set 4 of 5, not 5 of 5, because several of my questions are two-part, and if a fact is split across two similar documents (like the multiple add/drop and pass-fail policy docs), the model could plausibly cite the wrong one of several close matches. When I looked up "When can you declare a major and is there any penalty or advantage for when you declare it?", it pulled back from multiple sources (5 chunks) —
 admin_add_drop_deadline.txt, admin_declaring_a_major.txt, admin_graduation_requirements.txt, admin_meal_plan_changes.txt, admin_pass_fail_option.txt 
 — but still cited the correct one, admin_declaring_a_major.txt, which I verified.

## 6. Bad input is rejected with a client error and is logged

Out of 10 deliberately bad requests to `POST /ask` (empty question, non-string
question, a 10,000-character question, a missing field, and a malformed JSON
body), all 10 return a 4xx status (never a 500), and all 10 leave a record in
`logs/requests.jsonl` with `status` and `error` filled in.

**Why this target:**
10 of 10, not 9. A bad request is fully under my control, so there is no
randomness from the model to excuse a miss, and a single 500 would mean
`serve.py` crashed on input a user can send by accident. A failure that
doesn't appear in the log is one I'd never find later, so the log check is
part of the same target.

---

# Capstone criteria

Written before any capstone results. These test the operational layer added in
`serve.py` and `obslog.py` (Shape A, deploy and instrument).

## 1. Bad input is rejected with a client error and logged

Out of 10 deliberately bad requests to `POST /ask` (2 empty questions, 2
non-string questions, 2 questions over 1,000 characters, 2 bodies that are not
a JSON object, 2 missing `question` fields), all 10 return a 4xx status and
none returns a 500. All 10 leave a line in `logs/requests.jsonl` with `status`
and `error` filled in.

**Why this target:**
10 of 10. A bad request is fully under my control and involves no model
randomness, so one 500 would mean `serve.py` crashed on input a user can send
by accident. A failure that is not logged is one I could never find later, so
the log check is part of the same target.

## 2. Clearly unrelated questions are refused, never answered

Out of 10 questions with nothing to do with campus life (for example "What is
the capital of Mongolia?", "Who won the 1994 World Cup?"), all 10 return
`refused: true` with status 200, `tokens` of 0, and no invented answer.

**Why this target:**
10 of 10, not 9. These questions sit far from every chunk in the corpus: in my
earlier runs Mongolia scored a distance of 0.82 and my unit 1 off-topic
questions scored 0.84 to 0.90, all well above the 0.6 gate threshold. Nothing
about them is borderline, so one that gets through means the gate is broken,
and a made-up answer to a student is worse than a refusal. Refusals also cost
0 tokens because the model is never called, so this checks the cost saving too.
I am deliberately not testing campus-sounding questions the corpus lacks
(tuition, gym hours); those are a harder case I have not measured.

## 3. Every request leaves a complete log record

Across a session of 30 requests (10 answered, 10 refused, 10 failed), there
are exactly 30 new lines in `logs/requests.jsonl`. Each has `ts`,
`status` and `latency_ms`. Every 200 line also has `question`, `answer` and
`tokens`.

**Why this target:**
30 of 30 and no missing fields. The log is how I find out what happened after
the fact, and a missing line shows up only as an absence. The cost figure and
the latency numbers in the README are computed from these fields.

## 4. `cited` names the file that holds the answer

For at least 9 of 10 answered questions with known source files, `cited` is
non-empty and includes the file that actually contains the answer.

**Why this target:**
9 of 10. The retriever returns five files per question and most are noise
(for parking, only one of five was used), so `cited` is how a reader finds the
right document. In my log the model sometimes cites a file while saying it
cannot answer (Wi-Fi, parking cost), so I need some tolerance for that.

## 5. An answered request stays cheap and fast

Across 10 fresh questions (not cached), at least 9 of 10 answered requests use
under 1,000 tokens and return in under 2,000 ms.

**Why this target:**
My earlier measurement averaged 668 tokens and a 682 ms median, with a 1,691 ms
maximum on the first request, which loads the index. 1,000 tokens and 2,000 ms
leave headroom for longer answers but would catch a prompt that grew too large.
This counts answered requests only: refusals cost 0 tokens and cache hits are
instant, so including them would hide the real cost.
