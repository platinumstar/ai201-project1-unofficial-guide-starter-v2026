# AFTER: serve.py with logging (Sun Nov 15 23:38:15 EST 2026)

## good question
{"answer":"Students can buy permits for the west and east lots, and there is no waitlist (admin_parking_permits.txt).","best_distance":0.3733,"corpus":"campus_life","question":"Which parking lots can students buy permits for, and is there a waitlist?","refused":false,"sources":["admin_parking_permits.txt","advising_registration.txt","dining_verrill_street_grill.txt","money_textbooks.txt","transit_shuttle.txt"],"threshold":0.6}

## out of scope
{"answer":"I don't have enough information about that.","best_distance":0.8246,"corpus":"campus_life","question":"What is the capital of Mongolia?","refused":true,"sources":[],"threshold":0.6}

## empty question (expect 400)
HTTP/1.1 400 BAD REQUEST
Server: Werkzeug/3.1.8 Python/3.13.0
Date: Mon, 16 Nov 2026 04:38:16 GMT
Content-Type: application/json
Content-Length: 101
Connection: close

{"error":"Send JSON with a question in it, like {\"question\": \"is the housing lottery random?\"}"}

## log (logs/requests.jsonl)
{"ts": "2026-11-15T23:38:16", "status": 200, "latency_ms": 949, "question": "Which parking lots can students buy permits for, and is there a waitlist?", "answer": "Students can buy permits for the west and east lots, and there is no waitlist (admin_parking_permits.txt).", "refused": false, "best_distance": 0.3733, "sources": ["admin_parking_permits.txt", "advising_registration.txt", "dining_verrill_street_grill.txt", "money_textbooks.txt", "transit_shuttle.txt"], "cited": ["admin_parking_permits.txt"], "tokens": 0}
{"ts": "2026-11-15T23:38:16", "status": 200, "latency_ms": 48, "question": "What is the capital of Mongolia?", "answer": "I don't have enough information about that.", "refused": true, "best_distance": 0.8246, "sources": [], "cited": [], "tokens": 0}
{"ts": "2026-11-15T23:38:16", "status": 400, "latency_ms": 0, "error": "empty question"}
