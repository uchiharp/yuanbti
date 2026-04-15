import json

with open('questions/sunce.json', 'r') as f:
    existing = json.load(f)

with open('new_questions.json', 'r') as f:
    new = json.load(f)

existing.extend(new)

with open('questions/sunce.json', 'w') as f:
    json.dump(existing, f, ensure_ascii=False, indent=2)

print(f"Added {len(new)} questions, total now {len(existing)}")