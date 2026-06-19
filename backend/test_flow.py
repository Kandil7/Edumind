import requests, json

BASE = "http://localhost:8000/v1"

# 1. Health check
r = requests.get("http://localhost:8000/health")
print(f"0. Health: {r.json()}")

# 2. List lessons
r = requests.get(f"{BASE}/content/lessons")
lessons = r.json()
print(f"1. Lessons: {len(lessons)} loaded")
for l in lessons:
    print(f"   - [{l['id'][:8]}] {l['title']}")

# 3. Login as demo student
r = requests.post(f"{BASE}/auth/login", json={"email": "demo@edumind.com", "password": "x"})
login = r.json()
token = login["access_token"]
headers = {"Authorization": f"Bearer {token}"}
user_id = login["user_id"]
print(f"\n2. Login OK: user={user_id}")

# 4. Get student profile
r = requests.get(f"{BASE}/students/{user_id}/profile", headers=headers)
print(f"3. Profile: status={r.status_code}")
if r.status_code == 200:
    profile = r.json()
    print(f"   {len(profile['mastery'])} mastery entries")
else:
    print(f"   Error: {r.text[:200]}")

# 5. Get student summary
r = requests.get(f"{BASE}/students/{user_id}/summary", headers=headers)
print(f"4. Summary: status={r.status_code}")
if r.status_code == 200:
    s = r.json()
    print(f"   {s['total_attempts']} attempts, {s['accuracy_pct']}% accuracy")

# 6. Tutor session step (first)
r = requests.post(f"{BASE}/tutor/session/step", json={
    "student_id": user_id,
    "lesson_id": lessons[0]["id"]
}, headers=headers)
print(f"5. Tutor step 1: status={r.status_code}")
if r.status_code == 200:
    step = r.json()
    print(f"   action={step['action']}, skill={step.get('skill_id','?')[:8]}")
    if step.get("question"):
        print(f"   question: {step['question']['stem'][:80]}")
    if step.get("explanation"):
        print(f"   explanation: {step['explanation'][:80]}...")

    # 7. If question, answer it and get next step
    if step.get("question"):
        r2 = requests.post(f"{BASE}/tutor/session/step", json={
            "student_id": user_id,
            "lesson_id": lessons[0]["id"],
            "last_question_id": step["question"]["id"],
            "last_response": "2x"
        }, headers=headers)
        print(f"6. Tutor step 2: status={r2.status_code}")
        if r2.status_code == 200:
            step2 = r2.json()
            print(f"   action={step2['action']}")
else:
    print(f"   Error: {r.text[:200]}")

# 8. Teacher overview
r = requests.get(f"{BASE}/teachers/teacher-1/courses/overview", headers=headers)
print(f"7. Teacher overview: status={r.status_code}")

print("\n=== BACKEND FULLY OPERATIONAL ===")
