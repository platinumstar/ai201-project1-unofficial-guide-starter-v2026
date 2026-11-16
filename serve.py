#!/usr/bin/env python3
"""
The Unofficial Guide — the same pipeline, over HTTP.

    python serve.py                          run it locally on port 5000
    gunicorn serve:app                       run it the way a host runs it

Nothing new happens in this file. It is a wrapper: a request comes in, it
hands the question to `app.py::ask_pipeline` — the exact function the command
line uses — and hands the answer back as JSON. Retrieval, the relevance gate
and the grounded prompt all still live where they lived. If you change how
your system answers, you change it in those files and this one follows.

Two routes:

    POST /ask       {"question": "..."} in, the answer and its sources out
    GET  /health    is the service up, and is there an index to search

Why this exists: `app.py` runs once and exits, which is fine on your laptop
and impossible to deploy. A hosted service has to stay up and wait for
requests. This is the smallest thing that does that.

⚠️ There is deliberately no logging, no timing and no metrics in this file.
Unit 9 has you build the structured log yourself — the request line, the
timing field everyone skips, the whole instrument-before-you-deploy exercise.
Shipping a logger here would hand you the answer to that. Add yours in unit 9;
this file stays the bare shell until then.
"""

import os
import re
import threading
import time
from collections import defaultdict, deque

from flask import Flask, jsonify, request

import config
import generate
from obslog import log_event

app = Flask(__name__)

MAX_QUESTION_CHARS = 1000
RATE_LIMIT_PER_MIN = 20
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024  # reject huge bodies outright

# One request through the pipeline at a time: keeps the per-request token
# count (a before/after difference of global totals) honest.
_pipeline_lock = threading.Lock()
_hits: dict[str, deque] = defaultdict(deque)


def _ms(start: float) -> int:
    return round((time.perf_counter() - start) * 1000)


def _rate_limited(ip: str) -> bool:
    """True if this client already made RATE_LIMIT_PER_MIN requests in the last minute."""
    now = time.monotonic()
    q = _hits[ip]
    while q and now - q[0] > 60:
        q.popleft()
    if len(q) >= RATE_LIMIT_PER_MIN:
        return True
    q.append(now)
    return False


HINT = 'Send JSON with a question in it, like {"question": "is the housing lottery random?"}'


def _reject(status: int, message: str, start: float, public: str | None = None, **extra):
    """Log and return a JSON error. Every failure leaves a record."""
    log_event(status=status, latency_ms=_ms(start), error=message, **extra)
    return jsonify({"error": public or message}), status


@app.errorhandler(404)
def _not_found(_e):
    return jsonify({"error": "not found"}), 404


@app.errorhandler(405)
def _bad_method(_e):
    return jsonify({"error": "method not allowed"}), 405


@app.errorhandler(413)
def _too_big(_e):
    log_event(status=413, error="request body too large")
    return jsonify({"error": "request body too large"}), 413


@app.errorhandler(Exception)
def _unexpected(exc):
    # Anything we didn't plan for: record the detail, tell the caller nothing.
    log_event(status=500, error=f"unhandled {type(exc).__name__}: {exc}")
    return jsonify({"error": "internal error"}), 500


@app.get("/health")
def health():
    """Is the service up, and is there an index to search?

    Two different questions, and the second one is the one that bites. A
    freshly deployed service answers this route happily while every /ask
    returns "no index" — hosts give you no disk that survives a restart, so
    the index has to be built as part of getting the service up. Checking
    here means you find that out in one request instead of five.
    """
    from store import index_exists

    ready = index_exists(config.CORPUS)
    return jsonify(
        {
            "status": "ok",
            "corpus": config.CORPUS,
            "index_ready": ready,
            "detail": (
                "ready"
                if ready
                else "no index for this corpus — run `python app.py index`"
            ),
        }
    )


@app.post("/ask")
def ask():
    """One question in, one grounded answer out.

    A refused question is a 200, not an error. The gate refusing is your
    system working — it is an answer, and the JSON says so with
    `"refused": true` so whatever calls this can tell the two apart.
    """
    from app import ask_pipeline
    start = time.perf_counter()

    if _rate_limited(request.remote_addr or "?"):
        return _reject(429, "rate limit exceeded, try again in a minute", start)

    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return _reject(400, "body must be a JSON object", start, public=HINT)

    question = payload.get("question")
    if not isinstance(question, str):
        return _reject(400, "question must be a string", start, public=HINT)
    question = question.strip()

    if not question:
        return _reject(400, "empty question", start, public=HINT)
    if len(question) > MAX_QUESTION_CHARS:
        return _reject(
            400,
            f"question too long (max {MAX_QUESTION_CHARS} characters)",
            start,
            question=question[:200],
        )

    with _pipeline_lock:
        tokens_before = generate.total_tokens()
        try:
            outcome = ask_pipeline(question, corpus=config.CORPUS)
        except generate.QuotaGuard as exc:
            log_event(status=503, latency_ms=_ms(start), question=question,
                      error=f"QuotaGuard: {exc}")
            return jsonify({"error": "service is over its request budget"}), 503
        except Exception as exc:  # noqa: BLE001 — never leak a traceback
            log_event(status=500, latency_ms=_ms(start), question=question,
                      error=f"{type(exc).__name__}: {exc}")
            return jsonify({"error": "internal error"}), 500
        tokens_used = generate.total_tokens() - tokens_before

    cited = sorted(set(re.findall(r"[\w\-]+\.txt", outcome["answer"])))
    cited = [c for c in cited if c in outcome["sources"]]
    log_event(
        status=200,
        latency_ms=_ms(start),
        question=question,
        answer=outcome["answer"],       
        refused=outcome["refused"],
        best_distance=round(outcome["best_distance"], 4),
        sources=outcome["sources"],
        cited=cited,
        tokens=tokens_used,
    )

    return jsonify(
        {
            "question": question,
            "answer": outcome["answer"],
            "refused": outcome["refused"],
            "sources": outcome["sources"],
            "best_distance": round(outcome["best_distance"], 4),
            "threshold": outcome["threshold"],
            "corpus": config.CORPUS,
        }
    )


def main():
    # Hosts tell you which port to listen on through PORT, and they expect you
    # on 0.0.0.0. Binding 127.0.0.1 instead works perfectly on your laptop and
    # then answers nothing at all once deployed, because the host's router
    # can't reach a socket that only accepts connections from inside the
    # container. It is the single most common way a first deploy "succeeds"
    # and is unreachable.
    port = int(os.getenv("PORT", "5000"))

    # Debug mode reloads on save, which is handy, and prints a console that
    # runs arbitrary code, which is not something to leave switched on where
    # strangers can reach it. Off unless you ask for it.
    debug = os.getenv("AI201_DEBUG", "0") == "1"

    print(f"Serving The Unofficial Guide on http://localhost:{port}")
    print(f"Corpus: {config.CORPUS}    (Ctrl-C to stop)\n")
    print("Try it from another terminal:\n")
    print(f"  curl http://localhost:{port}/health")
    print(
        f"  curl -X POST http://localhost:{port}/ask \\\n"
        f"    -H 'Content-Type: application/json' \\\n"
        f"    -d '{{\"question\": \"is the housing lottery random?\"}}'\n"
    )

    app.run(host="0.0.0.0", port=port, debug=debug)


if __name__ == "__main__":
    main()
