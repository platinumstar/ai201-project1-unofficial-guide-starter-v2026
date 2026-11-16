# BEFORE: serve.py with no logging (Sun Nov 15 15:31:27 EST 2026)

## good question
{"answer":"Students can buy permits for the west and east lots, and there is no waitlist (admin_parking_permits.txt).","best_distance":0.3733,"corpus":"campus_life","question":"Which parking lots can students buy permits for, and is there a waitlist?","refused":false,"sources":["admin_parking_permits.txt","advising_registration.txt","dining_verrill_street_grill.txt","money_textbooks.txt","transit_shuttle.txt"],"threshold":0.6}

## out of scope
{"answer":"I don't have enough information about that.","best_distance":0.8246,"corpus":"campus_life","question":"What is the capital of Mongolia?","refused":true,"sources":[],"threshold":0.6}

## empty question (expect 400)
HTTP/1.1 400 BAD REQUEST
Server: Werkzeug/3.1.8 Python/3.13.0
Date: Sun, 15 Nov 2026 20:31:28 GMT
Content-Type: application/json
Content-Length: 101
Connection: close

{"error":"Send JSON with a question in it, like {\"question\": \"is the housing lottery random?\"}"}

## is there a log?
ls: logs: No such file or directory
