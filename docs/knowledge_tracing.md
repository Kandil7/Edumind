# Knowledge Tracing

## Bayesian Knowledge Tracing (BKT)

EduMind uses pyBKT to model per-student mastery of each skill over time.

### Parameters
- **P(L0)**: Prior probability of knowing the skill (default: 0.3)
- **P(T)**: Probability of learning from practice (default: 0.4)
- **P(G)**: Probability of guessing correctly (default: 0.2)
- **P(S)**: Probability of slipping (wrong when known) (default: 0.1)

### Update Formula

For correct answer:
```
P(known|correct) = P(L) × (1 - P(S)) / P(correct)
```

For incorrect answer:
```
P(known|incorrect) = P(L) × P(S) / P(wrong)
```

After each attempt:
```
P(L') = P(known|result) + (1 - P(known|result)) × P(T)
```

### Data Model

**student_skill_state** table:
- `student_id`, `skill_id` (composite PK)
- `p_mastery`: current probability of mastery
- `num_attempts`: total attempts on this skill
- `last_updated`: timestamp

### API

- `POST /v1/tracing/update` → updates mastery after attempt
- `GET /v1/students/{id}/profile` → returns mastery map

### Integration

Every call to `/assessments/grade` triggers BKT update for the associated skill. The Tutor Orchestrator reads mastery values to decide:
- **EXPLAIN** if mastery < 0.4
- **QUESTION** if mastery >= 0.4
- **FINISHED** if all skills mastered
