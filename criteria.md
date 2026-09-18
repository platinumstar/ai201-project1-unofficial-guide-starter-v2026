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

## 4. Something about your chunks

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
